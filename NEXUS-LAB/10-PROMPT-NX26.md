# Prompt MCP-ready — NX-26 Provider Layer (Brain FastAPI)

Da incollare in **Roo Code**. Quattro fasi. Modello consigliato in intestazione a
ciascuna fase.

**Prerequisito:** il repo del Brain ha un path diverso dal repo Astro già indicizzato.
La FASE 0 esiste per questo — se la salti, `search_graph` risponde sul repo sbagliato.

---

## FASE 0 · `deepseek-flash` · indicizzazione

```text
Questo è un task di setup. NON modificare alcun file. NON creare file.

Il progetto corrente è il Brain FastAPI, NON il repository Astro già indicizzato.

1. list_projects
   Riporta l'elenco dei progetti già indicizzati.

2. Se il path del Brain NON compare:
   index_repository sul path corrente del Brain.
   Attendi il completamento e riporta il numero di nodi e archi.

3. index_status
   Riporta: project identifier, generation, status, warnings, parse_partial,
   excluded directories.

4. Verifica di essere sul repo giusto con search_code su:
   - "DeepSeekManager"
   - "FastAPI"
   Se DeepSeekManager non compare, FERMATI: stai indicizzando il repo sbagliato.

NON procedere oltre se l'indice non è sul Brain.
```

---

## FASE 1 · `deepseek-flash` · audit read-only del legacy

```text
Questa è una review. NON modificare alcun file, NON creare file. Output = report.

OBIETTIVO
Mappare il god-object DeepSeekManager e tutto ciò che dipende dal provider AI,
per preparare l'estrazione in modules/providers/ senza cambio di comportamento.

PROCEDURA
1. search_graph: DeepSeekManager
2. get_code_snippet: DeepSeekManager (tutti i metodi, uno per uno)
3. trace_path: DeepSeekManager, direzione both
   → chi lo istanzia, chi lo chiama, cosa chiama
4. search_code: "DEEPSEEK_API_KEY"
   → elenca OGNI file che la legge
5. search_code: "X-API-Key"
   → identifica dove la chiave del provider viene usata come chiave API del server
6. search_graph: mcp_tools
7. trace_path: mcp_tools, direzione both
8. search_code: "deepseek-v4-flash" e "deepseek-flash" e "deepseek-v4-pro"
   → CRITICO: identifica ogni model ID hardcoded. "deepseek-v4-flash" è stato
     RITIRATO dal provider il 2026-09-10; il catalogo vivo restituisce solo
     "deepseek-flash" e "deepseek-v4-pro".
9. Leggi requirements.txt e fly.toml (o equivalente) con get_code_snippet/search_code
   → per ogni pacchetto elencato, verifica con search_code se è importato.
     NON proporre rimozioni: riporta solo "importato / non importato".
     Attenzione a gunicorn: potrebbe essere nel comando di start, non nel codice.

OUTPUT OBBLIGATORIO

A. INVENTARIO RESPONSABILITÀ di DeepSeekManager
   Per ogni metodo: nome, righe, cosa fa, a quale delle quattro interfacce
   target appartiene:
     ModelProvider | ToolExecutor | HealthProbe | ContractCompleter | ALTRO
   Marca ALTRO esplicitamente: è ciò che non sappiamo ancora dove mettere.

B. MAPPA DEI CONSUMATORI
   route/file → metodo chiamato → dipendenza (diretta/transitiva)

C. MODEL ID HARDCODED
   tabella: file, riga, valore, è ancora valido?

D. USO DELLE CHIAVI
   dove DEEPSEEK_API_KEY è usata come credenziale del server invece che
   del provider. Riferimenti precisi.

E. REQUISITI
   tabella pacchetto → importato sì/no → dove

F. RISCHI DI ESTRAZIONE
   cosa si rompe se si sposta il codice, in ordine di gravità

GUARDRAIL
Se un simbolo non esiste nel grafo, scrivi NOT FOUND.
Non inferire. Non indovinare percorsi. Non citare codice che non hai estratto
con get_code_snippet.
Distingui rigorosamente FACTS OBSERVED / HYPOTHESES / RECOMMENDATIONS.
```

---

## FASE 2 · `deepseek-v4-pro` · commit 1 — protocolli, nessun cambio di comportamento

```text
Contesto: la FASE 1 ha prodotto l'inventario. Ora si estrae.

REGOLA DEL REFACTOR (non negoziabile)
Il server deve funzionare identico con il layer AI SPENTO.
Se spegnere l'AI rompe qualcosa, quel qualcosa era accoppiato: segnalalo,
non aggirarlo.

VINCOLI
· NESSUN cambio di comportamento in questo commit
· NESSUNA modifica alle route esistenti
· I file esistenti restano funzionanti: il nuovo codice si aggiunge,
  DeepSeekManager resta al suo posto e delega

CREA
modules/providers/base.py
  Capabilities (dataclass frozen): chat, structured_output, tool_calling,
    thinking, context_window, max_output
  Usage (dataclass frozen): input_tokens, cached_input_tokens, output_tokens,
    reasoning_tokens
  Completion (dataclass frozen): text, model_id, usage, latency_ms, cost_usd
    → model_id è quello RISOLTO dal provider, non quello richiesto
  CostClass = Literal[0,1,2,3,4]
  ModelProvider (Protocol, runtime_checkable):
    async complete(*, model_id, messages, cost_class, max_output_tokens,
                   thinking=False, temperature=None) -> Completion
    async list_models() -> list[str]
  EmbeddingsProvider (Protocol): async embed(texts, *, model) -> list[list[float]]
  NullEmbeddings: solleva NotImplementedError con messaggio che rimanda a D-009
    (il testo è source authority, l'embedding è una proiezione)

modules/providers/routing.py
  RouteSpec (dataclass frozen): model_key, max_output_tokens, thinking, timeout_s
  ROUTES: dict per classe
    1 → default, 1024, thinking False, 30s
    2 → default, 4096, thinking False, 60s
    3 → gate,    8192, thinking True,  120s
  funzione resolve(cost_class, requested_max_output) -> RouteSpec
    che applica min(tetto_di_classe, richiesto): il client suggerisce,
    il server decide. Mai il contrario.

modules/reduce/__init__.py
  vuoto per ora

TEST
· test che modules/reduce/ NON importa modules/providers/ (ispezione AST o
  import guard). Questo test è il guardrail della reduction pipeline: se salta,
  abbiamo perso la leva di costo principale.
· test che NullEmbeddings solleva
· test che resolve() non permette max_output sopra il tetto di classe
· test che le route esistenti rispondono come prima (regression)

COMMIT
"refactor(brain): introduce provider protocols and cost-class routing (no behavior change)"

Se qualcosa in questo commit richiede di modificare una route esistente,
FERMATI e segnalalo: significa che l'accoppiamento è più profondo del previsto.
```

---

## FASE 3 · `deepseek-v4-pro` · commit 2 — CatalogReconciler e degradazione

```text
CREA
modules/providers/catalog.py
  CatalogError(RuntimeError)
  CatalogReconciler(provider, configured: dict[str,str])
    RECONCILE_INTERVAL_S = 6 * 3600
    async reconcile() -> None
      chiama provider.list_models()
      se un modello configurato non è disponibile: RAISE CatalogError
      con l'elenco dei disponibili. NESSUN FALLBACK SILENZIOSO.
    async ensure() -> None
      riconcilia solo se sono passate più di RECONCILE_INTERVAL_S
    property available -> set[str]

modules/providers/health.py
  HealthProbe: probe minimo sul modello configurato
  circuit breaker: su N fallimenti o latenza oltre soglia → stato OPEN
  stato OPEN → le chiamate AI non partono, rispondono degradate

COMPORTAMENTO RICHIESTO
· startup: reconcile(). Se solleva CatalogError:
    - il server PARTE
    - il layer AI è marcato DEGRADED
    - le route AI rispondono 503 con motivo esplicito e leggibile
    - il resto del server serve normalmente
· ogni 6h: reconcile() in background
· ogni chiamata: ensure()
· su errore 400 dal provider che nomina model ID: reconcile() immediato,
  poi ri-raise

MODEL ID
Gli unici ID configurati devono essere quelli verificati sul catalogo vivo
il 2026-09-12: "deepseek-flash" e "deepseek-v4-pro".
"deepseek-v4-flash" NON deve comparire da nessuna parte.

TEST
· modello mancante → CatalogError, non fallback
· CatalogError a startup → server vivo, route AI in 503, route non-AI in 200
· ensure() non richiama list_models se l'intervallo non è scaduto
· circuit breaker: dopo N fallimenti lo stato è OPEN e le chiamate non partono

COMMIT
"feat(brain): catalog reconciliation with explicit degradation, no silent fallback"
```

---

## FASE 4 · `deepseek-v4-pro` · commit 3 — separazione chiavi

```text
OBIETTIVO
Il legacy usa DEEPSEEK_API_KEY come X-API-Key sulle route
(vedi FASE 1, sezione D). Le due credenziali vanno separate.

· DEEPSEEK_API_KEY   → parla col provider
· AUTH_API_KEY       → autorizza chi chiama il nostro server
· le due non si toccano mai

VINCOLO
Nessun cambio di comportamento per i client già configurati correttamente.
Se la separazione rompe un client esistente, segnalalo invece di compensare.

TEST
· test_auth_key_is_not_provider_key: assert settings.AUTH_API_KEY != settings.DEEPSEEK_API_KEY
· una richiesta con X-API-Key pari a DEEPSEEK_API_KEY deve essere RIFIUTATA
  (questo è il test che conta: oggi probabilmente passerebbe)
· AUTH_API_KEY assente → il server rifiuta di partire sulle route protette,
  non usa un default vuoto

COMMIT
"fix(brain): separate AUTH_API_KEY from DEEPSEEK_API_KEY"
```

---

## FASE 5 · `deepseek-v4-pro` · commit 4 — strumentazione e cleanup

```text
CREA
modules/providers/budget.py
  RATE_CARD con lane peak/off_peak per deepseek-flash e deepseek-v4-pro
    (valori da 08-COST-CULTURE § 1.1, da riverificare sulla console)
    fasce off-peak: 01:00-04:00 e 06:00-10:00 UTC
  cost_usd(model_id, usage, at_utc_hour) -> float
    fresh = input_tokens - cached_input_tokens
    out   = output_tokens + reasoning_tokens   ← il reasoning È fatturato come output
    se model_id non è in RATE_CARD → ritorna 0.0, mai crashare sul pricing

STRUMENTAZIONE
Agganciati all'esistente AIRedisLogger (logSuccess / logRequest) se presente,
altrimenti crea un logger dedicato. Per OGNI chiamata LLM registra:

  request_id · timestamp · cost_class
  model_id_richiesto · model_id_risolto
  input_tokens · cached_input_tokens · output_tokens · reasoning_tokens
  latency_ms · cost_usd · esito (ok|error|timeout|circuit_open) · principal_id

Le due coppie model_id_richiesto/risolto e la presenza di cached_input_tokens
e reasoning_tokens sono obbligatorie: senza, la cultura di costo non esiste.

CLEANUP requirements.txt
Rimuovi SOLO i pacchetti che la FASE 1 ha classificato "non importato"
E che non compaiono in fly.toml / Dockerfile / script di start.
gunicorn in particolare: verifica il comando di start prima di toccarlo.
Un pacchetto per riga nel commit message, con la giustificazione.

TEST
· cost_usd con cache hit parziale produce il valore atteso
· cost_usd con model_id sconosciuto ritorna 0.0 senza sollevare
· una chiamata registra tutti i 13 campi
· il logging non fallisce se il provider non restituisce reasoning_tokens
  (campo opzionale, default 0)

COMMIT
"feat(brain): per-call cost instrumentation and dependency cleanup"
```

---

## DEFINIZIONE DI FATTO (verificare alla fine, nell'ordine)

```text
□ Il server parte e serve tutto con NEXUS_AI_ENABLED=0
□ CatalogReconciler gira a startup e ogni 6h
□ Modello mancante → 503 sulle route AI, server vivo, nessun fallback silenzioso
□ "deepseek-v4-flash" non compare in nessun file del repo (grep di verifica)
□ "deepseek-flash" e "deepseek-v4-pro" sono gli unici ID configurati
□ Ogni chiamata LLM logga i 13 campi, inclusi cached e reasoning
□ cost_class enforce server-side; il tetto di classe vince sul client
□ thinking=False su classi 1 e 2
□ modules/reduce/ non importa modules/providers/ (test verde)
□ AUTH_API_KEY separata, con test che rifiuta DEEPSEEK_API_KEY come chiave API
□ EmbeddingsProvider esiste come protocollo, unica impl NullEmbeddings
□ system prompt byte-identico per classe (niente timestamp, niente ID,
  chiavi in ordine stabile) — verificare nei prompt esistenti
□ requirements.txt ripulito solo dopo verifica, gunicorn incluso
□ suite di test esistente verde
```

---

## GUARDRAIL GENERALI (valgono per tutte le fasi)

```text
· Usa sempre index_status → search_graph → trace_path → get_code_snippet
  prima di qualunque conclusione.
· Non leggere file interi: estrai il simbolo.
· Se un simbolo non esiste, scrivi NOT FOUND. Non inventare percorsi.
· Questo refactor riguarda il Brain. NON toccare il repository Astro e NON
  toccare PageController, normalizeToPageData, ApplicationDefinition,
  ApplicationContext, BundleCollector, DiscoveryService, PageData.
· Ogni commit deve essere revertabile da solo.
· Se una fase richiede una decisione architetturale non prevista da questo
  prompt, FERMATI e chiedila. Non sceglierla tu.
```

---

## Nota di sequencing

```text
FASE 0 + 1   con deepseek-flash     (setup + audit, retrieval-heavy)
FASE 2–5     con deepseek-v4-pro    (estrazione di un god-object: refactor
                                     pericoloso, giudizio richiesto)
```

La FASE 1 è l'unica che può essere ripetuta senza costo: se il report è debole,
rifalla prima di passare alla FASE 2. **Non iniziare a scrivere codice su un
inventario incompleto** — è così che un god-object diventa due god-object.

---

*Ultimo aggiornamento: 2026-09-12*
