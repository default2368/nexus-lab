# NEXUS LAB — Cultura di costo

**Data:** 2026-09-10
**Scopo:** costruire la cultura di costo che manca (D-015bis, NX-19)

---

## 0. INCIDENTE CONFERMATO — model ID ritirato (risolto 2026-09-12)

### 0.1 L'evidenza

Ipotesi formulata il 2026-09-10 su fonti terze. **Verificata il 2026-09-12** con
`curl https://api.deepseek.com/v1/models`:

```json
{
  "object": "list",
  "data": [
    { "id": "deepseek-flash",  "object": "model", "owned_by": "deepseek" },
    { "id": "deepseek-v4-pro", "object": "model", "owned_by": "deepseek" }
  ]
}
```

**Esito:**

```text
deepseek-v4-flash   → RITIRATO. Non compare più nel catalogo.
deepseek-flash      → nuovo ID (V4.1)
deepseek-v4-pro     → ancora presente
```

Confronto con l'errore storico del 2026-07-25, che recitava:

```text
400 The supported API model names are deepseek-v4-pro or deepseek-v4-flash,
but you passed deepseek-reasoner.
```

Fra il 25 luglio e il 12 settembre 2026 il catalogo è cambiato **sotto i piedi**,
senza preavviso visibile dalla nostra parte. Sei settimane.

### 0.2 Conseguenza

Ogni configurazione che referenziava `deepseek-v4-flash` era puntata a un modello
inesistente. A seconda del client, il comportamento è uno fra:

```text
· errore 400 esplicito            → te ne accorgi
· fallback silenzioso del provider → non te ne accorgi, paghi un altro modello
· retry con backoff                → non te ne accorgi, perdi tempo
```

Il secondo caso è il peggiore: **il costo cambia e nessuno lo sa.**

### 0.3 Bonifica eseguita

Sostituito `deepseek-v4-flash` → `deepseek-flash` in tutti i documenti operativi
del workspace (11 occorrenze). Questo file conserva l'ID vecchio solo come
documentazione storica.

**Resta da fare sul tuo lato** (NX-25):

```text
□ Roo Code        settings → provider → model ID
□ Cline           settings → model ID
□ Continue        config.yaml / config.json → model
□ Trae            eventuale override per progetto
□ Brain           modules/main/deepseek.py + variabili d'ambiente
□ .clinerules     verificare che non ci siano ID hardcoded
□ AGENTS.md       idem
```

### 0.4 La lezione — e perché NX-04 non era teoria

Questo è esattamente lo scenario che Trustable ha già gestito:

> *"When your provider publishes a new catalog version, Trustable notices on the
> next page load, saves the new list, and sends you back here with a banner asking
> you to re-pick the coding model — because the one you had chosen may no longer exist."*

Noi l'abbiamo scoperto per caso, durante una ricerca sui prezzi, sei settimane dopo.

**NX-04 sale a P0** e cambia natura: non è "validazione dell'endpoint al save",
è **riconciliazione periodica del catalogo con fallback esplicito**.

**Perché è importante oltre l'emergenza:** questo è *esattamente* lo scenario che
NX-04 prevede e che Trustable ha già implementato:

> *"When your provider publishes a new catalog version, Trustable notices on the
> next page load, saves the new list, and sends you back here with a banner asking
> you to re-pick the coding model — because the one you had chosen may no longer exist."*

NX-04 non era teoria. È successo oggi, sul tuo provider principale.

**Avvertenza sulla provenienza:** i numeri qui sotto vengono da aggregatori terzi
(benchlm.ai, chat-deep.ai, techjacksolutions, felloai, coworker.ai), non dalla pagina
ufficiale DeepSeek. Convergono fra loro ma **vanno verificati** sulla console prima
di basare decisioni di prezzo. Il listino DeepSeek è cambiato almeno tre volte nel
2026 (24 apr, 31 mag, 16 ago, 10 set).

---

## 1. I numeri

### 1.1 Rate card osservata (agosto–settembre 2026)

Da più fonti, con fatturazione **peak / off-peak** introdotta il 16 agosto 2026:

```text
V4 FLASH  (deepseek-flash / deepseek-v4-flash)
                    peak        off-peak
  input (cache miss) $0.30–0.44  $0.15–0.22
  input (cache HIT)  $0.006–0.014 $0.003–0.007
  output             $1.20–1.32  $0.60–0.66
  contesto           1M token
  max output         384K token
  concorrenza        2.500 richieste

V4 PRO  (deepseek-v4-pro)
                    peak        off-peak
  input (cache miss) $1.32       $0.66
  input (cache HIT)  $0.044      $0.022
  output             $3.96       $1.98
  contesto           1M token
  max output         384K token
  concorrenza        500 richieste      ← 5× meno di Flash
```

Fasce off-peak riportate: **01:00–04:00 e 06:00–10:00 UTC** (tutte le altre ore = peak).
In ora legale italiana (UTC+2): **03:00–06:00 e 08:00–12:00**.

Extra osservati: **5M token gratuiti** per account nuovi, validità 30 giorni.

### 1.2 Le quattro asimmetrie che governano tutto il costo

```text
1. OUTPUT > INPUT        3–5× più caro
                         Flash peak: $1.20 out vs $0.30 in = 4×
                         → chi ottimizza la lunghezza del prompt e non quella
                           della risposta ottimizza la colonna sbagliata

2. CACHE HIT ≈ GRATIS    ~97% di sconto sull'input, AUTOMATICO
                         $0.30 → $0.006 su Flash peak
                         → ma "even small differences in the system prompt
                           prefix break the cache"
                         → un timestamp nel system prompt azzera lo sconto

3. PEAK vs OFF-PEAK      2× secco, dipende dall'orologio
                         → un batch schedulato alle 09:00 UTC costa la metà

4. REASONING = OUTPUT    i token di thinking sono fatturati come output
                         e possono moltiplicare il costo 3–10×
                         SENZA aumentare l'output visibile
                         → V4 Flash ha modo thinking e non-thinking sotto
                           lo stesso model ID
```

**Il punto 4 è quello che non si vede.** Se hai il modo thinking attivo su una
pipeline ad alto volume, stai pagando output invisibile. Va disattivato
esplicitamente sui percorsi di scoring, e tenuto solo dove serve giudizio.

---

## 2. Il tuo pattern — formalizzato

Hai detto:

> *"si può fare scraping e poi fare analizzare all'LLM se abbiamo dei banali scores."*

Questo non è un trucco. È **il** pattern, e ha un nome:

```text
REDUCTION PIPELINE

sorgente grezza  →  estrazione deterministica  →  riduzione a score  →  LLM
  (grande)             (gratis)                   (piccolissimo)      (pochi token)
```

La regola che ne discende:

> **L'LLM non deve mai leggere la sorgente. Deve leggere la riduzione della sorgente.**

È la stessa proposizione di *Foundation osserva, X interpreta* — vista dal lato
dei token invece che dal lato dell'architettura.

### 2.1 Perché funziona: la matematica

Caso concreto sulla persona dichiarata. Un broker che monitora **50 fonti di
mercato**, con uno sweep ogni 15 minuti (96 sweep/giorno).

**Approccio ingenuo — l'LLM legge il contenuto:**

```text
50 fonti × 20.000 token     = 1.000.000 token input per sweep
1M × $0.30/M (peak)         = $0.30 per sweep
× 96 sweep/giorno           = $28.80/giorno
× 30                        = $864/mese
```

**Approccio reduction pipeline — l'LLM legge gli score:**

```text
scraping + score            = deterministico, $0
input LLM: tabella score    ≈ 500 token  (di cui ~300 system prompt cached)
output LLM: sintesi         ≈ 500 token

input  200 × $0.30/M + 300 × $0.006/M = $0.00006 + $0.0000018 ≈ $0.00006
output 500 × $1.20/M                  = $0.0006
                                        ─────────
                                        $0.00066 per sweep
× 96 sweep/giorno                       = $0.063/giorno
× 30                                    = $1.90/mese
```

**Rapporto: ~450×.**

E se l'LLM gira solo quando uno score supera una soglia — cioè se il trigger è
deterministico, come dice NX-19 — e supponendo che accada sul 5% degli sweep:

```text
$1.90 × 0.05  =  $0.10/mese
```

**Rapporto rispetto all'ingenuo: ~8.600×.**

### 2.2 La lettura strategica di questi numeri

```text
$864/mese   → non sostenibile per un progetto singolo. Ti costringe a limitare
              le fonti, cioè a peggiorare il prodotto.
$1.90/mese  → sostenibile. 50 fonti per un broker.
$0.10/mese  → sostenibile con margine per 500 fonti.
```

La differenza non è "usare un modello economico". È **quanti byte arrivano al
modello**. `flash` rispetto a `pro` ti dava 4×. La reduction pipeline ti dà 450×.
Il trigger deterministico altri 20×.

```text
LEVA                          GUADAGNO     DIPENDE DA
─────────────────────────────────────────────────────────────
modello economico (flash)        4×        disciplina
cache hit sul prefix            50×        disciplina (fragile)
off-peak scheduling              2×        disciplina
reduction pipeline             450×        STRUTTURA
trigger deterministico          20×        STRUTTURA
─────────────────────────────────────────────────────────────
```

**Le prime tre leve sono disciplina: reggono finché te le ricordi.**
**Le ultime due sono struttura: reggono sempre.** E sono quelle che hai già
progettato — la CLI che estrae token è l'embrione della reduction pipeline.

---

## 3. Classi di costo per Nexus

Da usare come tabella di routing. Ogni operazione di prodotto va assegnata a una
classe **prima** di essere implementata.

```text
CLASSE 0 — DETERMINISTICA                    costo $0
  scraping, parsing, estrazione token, hashing
  score, delta, serie storiche, soglie, trigger
  compilazione bundle, validazione di schema
  discovery, rendering, serving
  → DEVE restare qui tutto ciò che è continuo o ad alto volume

CLASSE 1 — RIDUZIONE + SINTESI               ~$0.0007/chiamata
  input: score/estratto già ridotto (< 1K token)
  output: sintesi breve (< 1K token)
  modello: flash, thinking OFF
  cache: system prompt stabile e identico
  → il cavallo di battaglia di X

CLASSE 2 — GENERAZIONE DI CONTENUTO          ~$0.01–0.05/chiamata
  generazione PageData completa, knowledge experience
  modello: flash, thinking OFF, max_output_tokens vincolato
  → su domanda dell'utente, mai in loop

CLASSE 3 — GIUDIZIO                          ~$0.05–0.30/chiamata
  decisioni architetturali, review di contratti, anomalie complesse
  modello: pro, thinking ON se utile
  → solo su gate, mai in automatico ad alto volume

CLASSE 4 — AGENTE ESTERNO                    costo $0 per te
  Roo Code / Claude Code / Codex dell'utente via nexus-mcp
  → NX-14. Il modello lo porta chi genera.
```

Regola di progettazione:

> **Ogni feature che nasce in classe 2 o 3 e potrebbe essere spostata in classe 0
> o 1 va spostata. Ogni feature che nasce in classe 4 non costa niente: va preferita.**

---

## 4. Strumentazione — senza misura non c'è cultura

Oggi non puoi rispondere a *"quanto mi costa una generazione di pagina?"*.
Finché non puoi, ogni discussione sui costi è opinione.

### 4.1 Cosa misurare per ogni chiamata LLM

```text
request_id
timestamp            → per verificare peak/off-peak reale
classe (0–4)         → la tabella del § 3
model_id             → risolto, non configurato (vedi § 0)
input_tokens
cached_input_tokens  ← la voce che nessuno misura e che vale il 97%
output_tokens
reasoning_tokens     ← se il provider li espone, ALTRIMENTI stimarli
latency_ms
esito                ok | error | timeout | circuit_open
user_id / token_id   → per attribuire il costo al tier
```

`reasoning_tokens` è la voce critica: se il provider non la espone, il tuo
`output_tokens` reale è invisibile e la classe 1 può silently diventare classe 3.

### 4.2 Dove metterlo

Hai già `AIRedisLogger` con `logSuccess` / `logRequest` (fan-in 12 nel grafo MCP).
**La strumentazione esiste già.** Manca probabilmente la scomposizione
input/cached/output/reasoning e l'etichetta di classe.

Questo è un lavoro piccolo su codice esistente, non un componente nuovo.

### 4.3 Tre numeri da avere sempre visibili

```text
costo per operazione di prodotto     (es. € per pagina generata)
costo per utente attivo al mese      (è questo che decide il pricing)
quota di token finita in cache hit   (target: > 80% sull'input ripetuto)
```

---

## 5. Guardrail

```text
1. max_output_tokens per classe, enforce SERVER-SIDE (NX-05)
   il client può suggerire, il server decide

2. system prompt byte-identico per classe
   niente timestamp, niente ID di richiesta, niente ordine variabile di chiavi
   → altrimenti la cache si rompe e perdi il 97%

3. circuit breaker via HealthProbe
   provider giù o lento → degrade a classe 0, non retry a oltranza

4. tetto di spesa giornaliero per token_id
   superato → le chiamate passano a classe 0 o vengono rifiutate

5. thinking mode OFF di default, ON solo per classe 3

6. off-peak per i batch (08:00–12:00 ora italiana)
   2× di sconto solo spostando lo scheduler

7. nessun LLM in loop temporizzato senza trigger (NX-19)
```

---

## 6. Le cinque domande prima di ogni feature AI

Da mettere nel template di PRD, come sezione obbligatoria.

```text
1. In quale classe di costo nasce questa feature?          (§ 3)
2. Può nascere in classe 0 o 1 invece che 2 o 3?           (reduction pipeline)
3. Quanti byte arrivano al modello, e chi li ha ridotti?   (§ 2)
4. Il costo cresce con gli utenti, col tempo, o con le richieste?
   → col TEMPO è la risposta sbagliata, sempre              (D-015bis)
5. Chi paga: tu o l'agente dell'utente?                    (NX-14)
```

Se la risposta alla 4 è "col tempo", la feature non va costruita così.

---

## 7. Infrastruttura: API vs self-hosting

**Aggiunta 2026-09-13.** Prezzi verificati su fonti terze a settembre 2026, con data
e provenienza. Il listino GPU cambia meno spesso di quello LLM ma va riverificato.

### 7.1 La distinzione che manca quasi sempre

```text
RAG / RETRIEVAL     embeddings → NESSUNO (D-009: NullEmbeddings)
                    retrieval  → SQLite FTS5 / Postgres trigram → CPU
                    → costo ~zero, gira sulla macchina Fly esistente

GENERAZIONE LLM     → API, oppure GPU
                    → è qui che stanno i soldi
```

**Il RAG progettato in D-009/D-010 è già gratuito.** La reduction pipeline (§ 2)
rende il retrieval semantico *meno* necessario, non di più: se riduci a score prima
dell'LLM, serve una lookup deterministica, non una ricerca vettoriale.

"Non possiamo permetterci RAG locali" è un falso vincolo.

### 7.2 Prezzi GPU cloud (settembre 2026)

```text
GPU                   VRAM    $/hr        $/mese always-on (730h)
─────────────────────────────────────────────────────────────────
RTX 3090              24GB    0.22        ~161
RTX 4090 community    24GB    0.34        ~248
RTX 4090 spot         24GB    0.11        ~80    (preemptible)
RTX 4090 secure       24GB    0.74        ~540
NVIDIA L4             24GB    0.70        ~504
NVIDIA A10G           24GB    1.00        ~720
L40S / RTX6000 Ada    48GB    0.74-0.79   ~540-577
A100 PCIe             80GB    1.19        ~869
A100 SXM              80GB    1.39        ~1.015
H100 PCIe             80GB    1.99-2.39   ~1.453-1.745
H100 SXM              80GB    2.69        ~1.963
H200                  141GB   3.59        ~2.621
─────────────────────────────────────────────────────────────────
AWS p4d.24xlarge      8×A100  21.96       ~16.029  (nodo intero, AWS non
                                                  vende unità più piccole)
AWS g5.xlarge         1×A10G  1.006       ~734
```

Serverless / scale-to-zero:

```text
Modal                     $30/mese di crediti gratuiti, paga al secondo
RunPod serverless 4090    $0.77-1.10/hr attivo
RunPod serverless A100    $2.17-2.72/hr attivo
HF Inference Endpoints    10 GPU-hr ~$13
```

Acquisto hardware (una tantum):

```text
RTX 3090 usata    ~$800      7-13B, 70B con quantizzazione spinta
RTX 4090          ~$1.600    7-13B a piena velocità, 70B a 4-bit
Mac M4 Max 128GB  ~$4.000    70B in unified memory, throughput limitato
```

Provenienza: getdeploying.com/gpus/nvidia-rtx-4090 · northflank.com/blog/runpod-gpu-pricing ·
devtk.ai/en/blog/self-hosting-llm-vs-api-cost-2026 · markaicode.com/pricing/runpod-vs-aws-ec2-gpu-inference-cost ·
buildmvpfast.com/api-costs/gpu

### 7.3 Break-even contro `deepseek-flash`

```text
opzione always-on più economica: RTX 4090 community = $248/mese

con $248 su deepseek-flash ($0.30/M input peak) si comprano:
   ~827M token di input
   ~460M token misti input+output (rapporto 5:1, tipico della reduction)
   di più con cache hit sul prefisso stabile
```

Volume reale di riferimento (§ 2.1): broker con 50 fonti e 96 sweep/giorno =
**6M token/mese naive**, **$1.90/mese con reduction**, **$0.10/mese con trigger**.

```text
BREAK-EVEN  ~400-800M token/mese
VOLUME ATTUALE stimato  10-60M token/mese anche con uso intenso

→ sei 10-80× sotto il break-even
→ e una 4090 ci gira un 7-14B, peggiore di deepseek-flash sul ragionamento
→ pagheresti di più per qualità inferiore
```

**Conclusione: il self-hosting dell'LLM è sbagliato di due ordini di grandezza, e
resterà sbagliato finché non c'è una base utenti reale.**

### 7.4 Costo del pilota (capacità di analisi di mercato)

```text
Connector (HTTP fetch)        CPU, macchina esistente          €0
Reduce (estrazione, score)    CPU                              €0
Sanitize (Presidio, NX-59)    CPU, Python                      €0
LLM (deepseek-flash)          con reduction pipeline           €2–20/mese
Storage (SQLite FTS5)         volume Fly esistente             €0–2
Rendering                     Vercel, già live                 €0
                                                             ─────────
                                                          < €25/mese
                                                          probabile < €10
```

Il vincolo di budget non è un vincolo.

### 7.5 Quando il self-hosting diventa giusto

In ordine di arrivo probabile per questo progetto:

```text
1. un cliente richiede contrattualmente che nessun dato vada a terzi
   → per il verticale PA/giustizia ARRIVA PRIMA di tutte le altre
   → e la risposta probabilmente NON è "montare su un cloud":
     è "girare sull'infrastruttura del cliente" (tier Private/on-prem, NX-01)
2. volume > ~400M token/mese                    → break-even economico
3. latenza che l'API non garantisce
4. un modello che l'API non offre
```

### 7.6 L'hedge costa zero, ed è già in NX-26

Non serve decidere oggi. Serve non precluderselo:

```python
ModelProvider(Protocol)
    async complete(*, model_id, ...) -> Completion
    async list_models() -> list[str]
```

Qualunque endpoint OpenAI-compatible che finisce in `/v1` è un provider. Un domani
vLLM / Ollama / TGI / llama.cpp — su AWS, su un cloud EU, su un rack del cliente — è
**una riga di configurazione**, non un refactor. È la carta "Private AI" di Trustable:
*"any OpenAI-compatible endpoint you run yourself"*.

### 7.7 La scelta del cloud è posizionamento, non ops

Se il verticale è PA italiana ed EU sovereignty-sensitive:

```text
Alibaba     provider cinese: per una gara PA italiana è peggio di AWS, non meglio.
            Non è una questione morale, è di procurement.
AWS         US CLOUD Act: gestibile con garanzie, ma va argomentato.

alternative EU:
  Regolo.AI     inferenza EU, credit-based — ciò che Trustable usa per Sovereign AI
  Aruba         ITALIANO — percorso di minima resistenza per una PA italiana
  OVHcloud      francese
  Scaleway      francese
  Hetzner       tedesco, economico (niente GPU cloud)
  AWS / Azure   hanno offerte "EU sovereign cloud" dedicate
```

Trustable/Nuvolaris vende "Sovereign AI" e appoggia l'inferenza su Regolo.AI per
questo motivo preciso. Il cloud fa parte della promessa commerciale.

---

## 8. Sintesi

```text
Il modello economico è la leva più debole: 4×
La struttura è la leva più forte: 450× × 20×

Non "usiamo il modello più economico".
Ma "facciamo arrivare meno byte al modello, e solo quando serve".

La CLI che estrae token non è un tool di sviluppo.
È il primo stadio della reduction pipeline, ed è il componente
che tiene il costo di X vicino a zero mentre X cresce.
```

---

*Ultimo aggiornamento: 2026-09-10*
*Provenienza prezzi LLM: aggregatori terzi, da verificare sulla console DeepSeek.*
*Provenienza prezzi GPU: § 7.2, verificata settembre 2026 su cinque fonti.*
*Riverificare prima di qualunque decisione di infrastruttura: nel 2026 il listino*
*LLM è cambiato quattro volte (24 apr, 31 mag, 16 ago, 10 set).*
