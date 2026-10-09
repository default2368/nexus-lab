# NX-27 · Connector Layer — la libreria di scraping è sufficiente?

**Data:** 2026-09-12
**Domanda:** *"ho fatto una libreria di scraping, prende un indirizzo e con librerie
basic vede header e codice HTML. Serve qualcosa di più sofisticato o possiamo usare
quella?"*

**Risposta breve:** usala. È **classe 0** (deterministica, zero token) ed è
esattamente dove deve stare. Ma va inquadrata come *un connettore fra N*, e le va
aggiunta **una** cosa, che vale più di tutte le altre messe insieme.

---

## 1. Perché "basic" è corretto, non un limite

```text
classe 0  scraping, parsing, estrazione, hashing, score, trigger
          → costo: banda + compute, NON token
          → deve restare semplice, prevedibile, testabile

classe 1+ riduzione → sintesi → LLM
          → costo: token
```

Un scraper sofisticato non costa token. Ma uno scraper **sbagliato** sì, in due modi:

```text
1. estrazione sporca   → score calcolati su nav + footer + pubblicità
                       → l'LLM analizza spazzatura e tu paghi per farlo

2. nessuna detection   → rianalizzi contenuto identico a ieri
   del cambiamento       → perdi la leva da 20× del trigger deterministico
```

Il secondo è quello che costa davvero. Ed è l'unico upgrade obbligatorio.

---

## 2. L'upgrade che vale tutto il resto: change detection

### 2.1 Il flusso

```text
fetch
  ↓
content_sha diverso dall'ultimo visto?
  ├── NO  → STOP. Zero token. Zero estrazione. Zero score.
  └── SÌ  → extract → score → soglia superata? → LLM
```

Senza il primo ramo, la reduction pipeline gira a vuoto sul 90% dei fetch: la
maggior parte delle fonti non cambia fra uno sweep e l'altro.

### 2.2 Due livelli, e il primo è gratis

**Livello 1 — conditional request HTTP.** Tu leggi già gli header. Usali:

```text
prima risposta    ETag: "abc123"        Last-Modified: Wed, 10 Sep 2026 ...
                  → li memorizzi per URL

fetch successivo  If-None-Match: "abc123"
                  If-Modified-Since: Wed, 10 Sep 2026 ...

server risponde   304 Not Modified      → NESSUN BODY, pochi hundred byte
                  200 + contenuto       → cambiato, procedi
```

**Hai già tutto quello che serve.** È la change detection più economica che esista:
non scarichi nemmeno il contenuto. Per 50 fonti ogni 15 minuti fa una differenza
enorme in banda e in tempo.

Caveat: non tutti i server rispettano `ETag`/`Last-Modified`. Alcuni non li mandano,
alcuni li mandano sempre diversi. Va gestito come *ottimizzazione*, non come garanzia.

**Livello 2 — hash del contenuto estratto.** Per i server che non supportano il 304,
e per rispondere a *cosa* è cambiato e non solo *se*:

```text
content_sha = sha256(normalize(contenuto_estratto))
```

`normalize` prima dell'hash, altrimenti un timestamp in pagina o un ordine di
attributi diverso producono un falso positivo a ogni fetch. Al minimo:
whitespace collassato, tag rimossi, minuscolo.

### 2.3 Dove si collega

```text
content_sha  →  è lo stesso campo già previsto nello schema chunks di D-009
                (source_uri, content_sha, content)
             →  è la chiave della cache di ricompilazione in NX-01b
             →  è ciò che rende deterministico il trigger di NX-19
```

Un solo campo, tre usi. Va progettato una volta.

---

## 3. Il framing corretto: un connettore, non "lo scraper"

La domanda "serve qualcosa di più sofisticato?" presume che lo scraping sia **il**
canale di acquisizione. Non lo è — è uno fra diversi.

```text
Connector (interfaccia unica)
  │
  ├── HttpHtmlConnector     ← LA TUA LIBRERIA. Va bene così.
  ├── JsonApiConnector      ← feed di mercato, REST, GraphQL
  ├── RssConnector          ← news (spesso più affidabile dello scraping)
  ├── PdfConnector          ← bilanci, filing, report
  └── (futuri)
```

Tutti producono **la stessa forma d'uscita**:

```python
@dataclass(frozen=True)
class Fetched:
    source_uri:      str
    fetched_at:      datetime
    status:          int
    content_sha:     str | None      # None se 304 / non cambiato
    changed:         bool
    text:            str | None      # None se non cambiato
    raw_headers:     dict
    content_type:    str
    error:           str | None
```

È la stessa lezione di ToolJet: **copia l'interfaccia del plugin, non la libreria dei
plugin** (`../documentation/research/benchmarks/TOOLJET-benchmark.md` § 5.3). Vale identico qui.

Con l'interfaccia in posto, "serve qualcosa di più sofisticato?" diventa una domanda
banale: aggiungi un connettore, non riscrivi lo scraper.

---

## 4. Reality check sulla persona dichiarata

La persona è manager / responsabile finanziario / broker che esplora il mercato.
Le fonti reali di quel dominio:

```text
dati di mercato      → API e feed, spesso WebSocket. NON HTML.
bilanci e filing     → PDF. NON HTML.
news                 → HTML o RSS. Qui lo scraping serve.
report di settore    → PDF.
comunicati           → HTML.
```

**Conclusione scomoda ma utile:** per quella persona l'HTML scraping è il canale
**minoritario**. `HttpHtmlConnector` copre news e comunicati — importante, ma non è
dove sta il valore decisionale.

Priorità reale dei connettori:

```text
1  JsonApiConnector      il valore sta qui
2  PdfConnector          filing e report
3  HttpHtmlConnector     ← il tuo, news e comunicati
4  RssConnector          costa quasi niente, spesso batte lo scraping
```

Non è un motivo per scartare la tua libreria: è un motivo per **non fermarti lì**.

---

## 5. Checklist del connettore minimo

### 5.1 Bloccante — senza, la reduction pipeline non funziona

```text
□ content_sha + changed            (§ 2 — l'unico vero must)
□ timeout esplicito                un connettore che si appende ferma lo sweep
□ gestione status != 200           4xx/5xx come dato, non come eccezione silenziosa
□ estrazione del contenuto         via nav/footer/ads/script/style prima dello score
□ encoding dichiarato              dai header, con fallback
□ fallimento esplicito             error popolato, mai testo vuoto scambiato per successo
```

L'estrazione del contenuto **non** richiede sofisticazione: `main`/`article` come
prima approssimazione, rimozione di `script`/`style`/`nav`/`footer`/`aside`, poi
testo. Va bene così per la classe 0. Se la qualità degli score lo richiede, si
migliora dopo — con misura, non a intuito.

### 5.2 Importante, ma non blocca il primo giro

```text
□ conditional request (ETag / Last-Modified)     ← gratis, hai già gli header
□ retry con backoff + jitter                     max 2-3 tentativi
□ rate limit PER DOMINIO, non globale
□ robots.txt rispettato + Crawl-delay
□ User-Agent identificativo                      non un browser fasullo
□ cache locale dei Fetched per source_uri
```

### 5.3 Da NON aggiungere

```text
✗ headless browser (Playwright/Puppeteer)
   lento, costoso, fragile. Serve SOLO se una fonte è una SPA client-rendered
   e non ha API né RSS. Prima verifica: guarda se il contenuto è nell'HTML
   che già scarichi. Se sì, non serve.

✗ rotazione di proxy
   è scraping adversarial su scala. Non è il tuo caso, ed è un campo minato
   legale per un prodotto commerciale venduto a broker.

✗ infrastruttura distribuita di crawling
   50 fonti ogni 15 minuti stanno in un processo singolo.

✗ ML per l'estrazione
   è classe 3 dentro la classe 0. Rompe il principio.
```

---

## 6. Due questioni legali, da decidere prima non dopo

Per un prodotto venduto a responsabili finanziari e broker:

```text
1. Terms of Service delle fonti
   Lo scraping può violare i ToS. Per news e comunicati il rischio è basso,
   per dati proprietari è alto. La risposta architetturale è preferire
   API ufficiali e RSS quando esistono — ed è anche la risposta tecnica
   migliore (§ 4).

2. Copyright sul contenuto estratto
   Il testo estratto resta dell'editore. Nel tuo modello questo è già gestito
   bene: D-009 dice che il testo è source authority e va tracciato con
   source_uri. Se mostri solo score, sintesi e link — non il testo integrale —
   l'esposizione è molto minore.

   Regola pratica: X produce SINTESI e RIFERIMENTI, non ripubblicazione.
   Vale anche per la qualità percepita: un broker vuole il segnale, non l'articolo.
```

Non è consulenza legale. È il motivo per cui la scelta dei connettori (§ 4) è anche
una scelta di rischio, non solo tecnica.

---

## 7. Risposta diretta

```text
La tua libreria va usata. Diventa HttpHtmlConnector.

Le va aggiunto UNA cosa prima di tutto il resto:
  content_sha + changed, con conditional request HTTP come ottimizzazione.

Le va tolta una presunzione:
  non è il canale principale per la persona dichiarata.
  JsonApiConnector e PdfConnector valgono di più.

Non le va aggiunto:
  headless browser, proxy, ML, infra distribuita.
```

---

## 8. Domande aperte

```text
Q-007  In che linguaggio è la libreria?
       Se Python → vive in modules/connectors/ del Brain, accanto a modules/reduce/
       Se JS/TS  → va deciso se il Brain la chiama via subprocess/API
                   o se il connettore viene riscritto in Python
       Non è un dettaglio: un connettore in due linguaggi è un connettore
       mantenuto due volte.

Q-008  Dove sta lo stato (content_sha visto l'ultima volta)?
       D-010 dice che il DB è indice derivato, non source of truth.
       Per la change detection serve uno stato durevole per source_uri.
       Opzioni: file locale / SQLite / Redis. Con local-first (NX-20)
       la risposta coerente è locale, con Redis come replica.

Q-009  Le fonti hanno API o RSS?
       Va verificato fonte per fonte PRIMA di scrivere codice di scraping.
       Ogni fonte con un'API è una fonte che non devi scrapare.
```

---

## 9. Collegamenti

```text
classe 0                 08-COST-CULTURE § 3
reduction pipeline       08-COST-CULTURE § 2
trigger deterministico   NX-19
content_sha              D-009 (schema chunks) + NX-01b (cache ricompilazione)
interfaccia plugin       TOOLJET-benchmark § 5.3
local-first              NX-20
DB come indice derivato  D-010
```

**Zona sicura:** nessun connettore tocca `PageController`, `normalizeToPageData`,
`ApplicationDefinition`, `ApplicationContext`, `BundleCollector`, `DiscoveryService`
o `PageData`. Un connettore produce dati normalizzati; il bundle li dichiara; il
Runtime osserva l'artefatto. Se un connettore finisce nel request path del Runtime,
si ricrea AF-001 in un altro punto — e questa volta non lo chiudi con una tabella
frozen, perché i connettori sono aperti per definizione.

---

*Ultimo aggiornamento: 2026-09-12*
