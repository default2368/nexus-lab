# NX-26 · Provider Layer per il server nuovo

**Data:** 2026-09-12
**Contesto:** l'utente sta rifattorizzando un server nuovo; il legacy era cresciuto.
**Assunzione:** si tratta del Brain FastAPI. Se è un altro server, la § 2 resta valida
ma la § 3 va adattata.

---

## 0. Perché questo documento esiste adesso

Tre fatti convergono nella stessa settimana:

```text
1. deepseek-v4-flash è stato ritirato sotto i piedi (08-COST-CULTURE § 0)
   → il catalogo del provider cambia senza preavviso, in ~6 settimane

2. Il legacy era cresciuto (DeepSeekManager: 506 righe, god-object)
   → ogni refactor che sposta il codice sposta anche il coupling

3. Il prodotto di fatto non usa AI
   → non c'è niente da districare
```

Il punto 3 è **un vantaggio**, non una mancanza. Stai rifattorizzando un server per
un prodotto che non dipende dall'AI. Significa che il layer AI può nascere come
**sottosistema delimitato, opzionale e meterizzato** invece di essere estratto da
un groviglio dopo.

Trustable e ToolJet hanno entrambi retrofit. Tu puoi costruire giusto la prima volta,
e il costo è qualche ora in più su un refactor che stai già facendo.

**Regola per questo refactor:**

> Il server deve funzionare identico con il layer AI **spento**.
> Se spegnere l'AI rompe qualcosa, quel qualcosa era accoppiato.

---

## 1. Target: struttura

```text
modules/
  providers/
    __init__.py
    base.py          ModelProvider, Capabilities         (protocolli, zero logica)
    catalog.py       CatalogReconciler                   (NX-04, P0)
    deepseek.py      DeepSeekProvider                    (unica implementazione)
    embeddings.py    EmbeddingsProvider + NULL            (D-009: interfaccia, no provider)
    health.py        HealthProbe
    routing.py       CostClass + ROUTING + limiti
    budget.py        metering + guardrail + circuit       (NX-24)
  reduce/
    scores.py        reduction pipeline, classe 0         (§ 2.2 cost culture)
```

Dipendenze ammesse:

```text
routes → routing → base
                   ↑
             deepseek, catalog, health, budget

reduce → (nessuna dipendenza da providers)     ← CLASSE 0, deterministico
```

**`reduce/` non importa `providers/`.** Se lo fa, la reduction pipeline sta
chiamando un LLM e hai perso la leva da 450×.

---

## 2. `base.py` — protocolli

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, runtime_checkable, Literal

CostClass = Literal[0, 1, 2, 3, 4]


@dataclass(frozen=True)
class Capabilities:
    chat: bool
    structured_output: bool
    tool_calling: bool
    thinking: bool
    context_window: int
    max_output: int


@dataclass(frozen=True)
class Usage:
    input_tokens: int
    cached_input_tokens: int      # ← la voce che vale il 97%
    output_tokens: int
    reasoning_tokens: int         # ← fatturati come output, invisibili


@dataclass(frozen=True)
class Completion:
    text: str
    model_id: str                 # RISOLTO dal provider, non configurato
    usage: Usage
    latency_ms: int
    cost_usd: float


@runtime_checkable
class ModelProvider(Protocol):
    name: str

    async def complete(
        self,
        *,
        model_id: str,
        messages: list[dict],
        cost_class: CostClass,
        max_output_tokens: int,
        thinking: bool = False,
        temperature: float | None = None,
    ) -> Completion: ...

    async def list_models(self) -> list[str]: ...


@runtime_checkable
class EmbeddingsProvider(Protocol):
    """D-009: interfaccia dal giorno uno, NESSUNA implementazione a pagamento.
    L'unica implementazione ammessa oggi è NullEmbeddings, che solleva."""

    async def embed(self, texts: list[str], *, model: str) -> list[list[float]]: ...


class NullEmbeddings:
    async def embed(self, texts, *, model):
        raise NotImplementedError(
            "Nessun provider di embedding configurato. "
            "Usa la ricerca FTS/trigram: il testo è source authority, "
            "l'embedding è una proiezione (D-009)."
        )
```

Nota: `model_id` in `Completion` è **quello risolto**, non quello richiesto. È la
prima difesa contro il caso "fallback silenzioso del provider" (§ 0.2 del doc costi).

---

## 3. `catalog.py` — NX-04, la lezione di oggi

```python
import logging, time

log = logging.getLogger("nexus.providers.catalog")

RECONCILE_INTERVAL_S = 6 * 3600   # il catalogo DeepSeek è cambiato in ~6 settimane


class CatalogError(RuntimeError):
    """Il modello configurato non esiste più. Fail loud, mai fallback silenzioso."""


class CatalogReconciler:
    def __init__(self, provider, configured: dict[str, str]):
        self._p = provider
        self._configured = configured      # {"default": "...", "gate": "..."}
        self._available: set[str] = set()
        self._checked_at: float = 0.0

    async def reconcile(self) -> None:
        available = set(await self._p.list_models())
        missing = {k: v for k, v in self._configured.items() if v not in available}

        self._available = available
        self._checked_at = time.time()

        if missing:
            # NON fare fallback. Un fallback silenzioso cambia il costo
            # e nessuno se ne accorge.
            raise CatalogError(
                f"Modello/i non più nel catalogo del provider: {missing}. "
                f"Disponibili: {sorted(available)}. "
                f"Aggiorna la configurazione."
            )
        log.info("catalog.ok", extra={"available": sorted(available)})

    async def ensure(self) -> None:
        if time.time() - self._checked_at > RECONCILE_INTERVAL_S:
            await self.reconcile()

    @property
    def available(self) -> set[str]:
        return self._available
```

Comportamento richiesto:

```text
startup              → reconcile(). Se fallisce, il server parte ma il layer AI
                       è marcato DEGRADED e le route AI rispondono 503 con motivo.
                       Il resto del server funziona.  ← vedi § 0, "AI spento"
ogni 6h              → reconcile() in background
ogni chiamata        → ensure() (costo zero se già fresco)
400 dal provider     → reconcile() immediato, poi ri-raise
```

**Degradazione, non crash.** Il server non deve morire perché DeepSeek ha cambiato
un nome. Deve rifiutare le operazioni AI e continuare a servire il resto.

---

## 4. `routing.py` — classi di costo enforce server-side

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class RouteSpec:
    model_key: str          # chiave in CatalogReconciler.configured
    max_output_tokens: int
    thinking: bool
    timeout_s: float


# Le classi da 08-COST-CULTURE.md § 3
ROUTES: dict[int, RouteSpec] = {
    # classe 0 non passa di qui: è deterministica, sta in modules/reduce/
    1: RouteSpec("default", max_output_tokens=1_024,  thinking=False, timeout_s=30),
    2: RouteSpec("default", max_output_tokens=4_096,  thinking=False, timeout_s=60),
    3: RouteSpec("gate",    max_output_tokens=8_192,  thinking=True,  timeout_s=120),
    # classe 4 = agente esterno via nexus-mcp: costo zero per noi, non passa di qui
}
```

**NX-05: il client può suggerire, il server decide.** Se una route riceve
`cost_class` dal payload, lo valida; se il payload chiede `max_output_tokens`
superiore al tetto di classe, **vince il tetto**. Mai il contrario.

Pattern già validato da Trustable: *"the rule is enforced on the server too, not
just in the browser, so it holds however you save."*

---

## 5. `budget.py` — NX-24, misura e guardrail

```python
# Rate card da verificare sulla console. Peak/off-peak cambia il 2×:
# le fasce off-peak riportate sono 01:00-04:00 e 06:00-10:00 UTC.
RATE_CARD = {
    "deepseek-flash": {
        "peak":     {"input": 0.30, "cached": 0.006, "output": 1.20},
        "off_peak": {"input": 0.15, "cached": 0.003, "output": 0.60},
    },
    "deepseek-v4-pro": {
        "peak":     {"input": 1.32, "cached": 0.044, "output": 3.96},
        "off_peak": {"input": 0.66, "cached": 0.022, "output": 1.98},
    },
}

def cost_usd(model_id: str, usage, at_utc_hour: int) -> float:
    rates = RATE_CARD.get(model_id)
    if rates is None:
        return 0.0                      # mai crashare sul pricing
    lane = "off_peak" if at_utc_hour in (*range(1, 4), *range(6, 10)) else "peak"
    r = rates[lane]
    fresh = max(usage.input_tokens - usage.cached_input_tokens, 0)
    out = usage.output_tokens + usage.reasoning_tokens   # ← il reasoning È output
    return (fresh * r["input"]
            + usage.cached_input_tokens * r["cached"]
            + out * r["output"]) / 1_000_000
```

Cosa loggare per ogni chiamata — **tutto, o la cultura di costo non esiste**:

```text
request_id · timestamp · cost_class · model_id_richiesto · model_id_risolto
input_tokens · cached_input_tokens · output_tokens · reasoning_tokens
latency_ms · cost_usd · esito (ok|error|timeout|circuit_open) · principal_id
```

Guardrail:

```text
· tetto di spesa giornaliero per principal_id → superato: classe 0 o 429
· circuit breaker su HealthProbe → provider lento/giù: degrade, non retry
· cache_hit_ratio monitorata → se < 60% sull'input ripetuto, il prefix non è stabile
· alert se reasoning_tokens > 3× output_tokens su classe 1 (thinking attivo per errore)
```

Il `cache_hit_ratio` è il numero che nessuno guarda e che vale il 97%: se il system
prompt non è byte-identico, lo sconto non scatta e non te ne accorgi.

---

## 6. Separazione chiavi — D-011, nel refactor

```text
DEEPSEEK_API_KEY    → parla col provider
AUTH_API_KEY        → autorizza chi chiama il TUO server
NEXUS_PAT_*         → tier Builder via nexus-mcp (NX-14, futuro)
```

Il legacy usava `DEEPSEEK_API_KEY` come `X-API-Key` sulle route. Nel server nuovo
le due cose non si toccano mai, e va scritto nei test:

```python
def test_auth_key_is_not_provider_key():
    assert settings.AUTH_API_KEY != settings.DEEPSEEK_API_KEY
```

---

## 7. Definizione di fatto

```text
□ Il server parte e serve tutto con il layer AI SPENTO (env NEXUS_AI_ENABLED=0)
□ CatalogReconciler gira a startup e ogni 6h; su modello mancante → 503 sulle
  route AI, server vivo, log esplicito, NESSUN fallback silenzioso
□ deepseek-flash e deepseek-v4-pro sono gli unici ID configurati (verificati
  sul catalogo vivo il 2026-09-12)
□ Ogni chiamata LLM logga i 13 campi di § 5, inclusi cached_input_tokens
  e reasoning_tokens
□ cost_class è enforce server-side; max_output_tokens del client non può
  superare il tetto di classe
□ thinking=False su classi 1 e 2
□ modules/reduce/ non importa modules/providers/ (test di import)
□ AUTH_API_KEY separata da DEEPSEEK_API_KEY, con test
□ EmbeddingsProvider esiste come protocollo; unica implementazione NullEmbeddings
□ system prompt byte-identico per classe (niente timestamp, niente ID,
  chiavi in ordine stabile)
□ requirements.txt ripulito SOLO dopo grep, gunicorn incluso (verificare fly.toml)
```

---

## 8. Cosa NON fare in questo refactor

```text
· Non aggiungere un secondo provider "per sicurezza".
  Un provider, ben astratto. Il secondo si aggiunge quando serve.

· Non mettere embedding reali. NullEmbeddings e FTS/trigram. D-009.

· Non costruire un motore di workflow. D-008: prima i contratti, poi i motori.

· Non toccare i simboli vincolati di Foundation. Questo è un server X/Brain:
  resta in zona sicura.

· Non offuscare niente. 04-FOUNDATION-API § 1.
```

---

## 9. Ordine di esecuzione suggerito

```text
commit 1   protocolli + routing + budget (nessun cambio di comportamento)
commit 2   CatalogReconciler + degradazione 503
commit 3   separazione AUTH_API_KEY + test
commit 4   strumentazione completa + cleanup requirements
```

Quattro commit piccoli, ciascuno revertabile. Il commit 2 è quello che ti protegge
dal prossimo ritiro di modello — che ci sarà, perché è già successo.

---

*Ultimo aggiornamento: 2026-09-12*
