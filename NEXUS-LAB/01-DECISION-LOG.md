# NEXUS LAB — Decision Log

Formato ADR leggero. Ogni voce: **stato**, **contesto**, **decisione**, **conseguenze**.

Stati: `DECISO` · `PROPOSTO` · `APERTO` · `SCARTATO` · `CONGELATO`

---

## DECISIONI PRESE

### D-001 — Foundation + X come split architetturale · `DECISO`

**Contesto:** il sistema deve ospitare sia esecuzione deterministica sia generazione AI.

**Decisione:** due segmenti separati da un boundary di invarianza.
Foundation produce (ApplicationBundle → BundleCollector → Build Artifacts).
Execution esegue (ApplicationDefinition → ApplicationContext → Discovery →
PageData → Template → Experience).

**Conseguenza:** tutto il lavoro su X è esplorabile senza rischio architetturale,
purché non attraversi il boundary. È la proprietà che abilita la modalità brainstorming.

---

### D-002 — PageData come linguaggio, non come renderer · `DECISO`

**Contesto:** rischio di nascondere la conoscenza dentro template specializzati.

**Decisione:** *"PageData is the language of knowledge experiences."*
Non significa che ogni UI debba usare `WebPageTemplate`. Hub, Operations, Auth e
future experience possono avere renderer specializzati. Significa che la conoscenza
non deve essere nascosta dentro quei renderer: **renderer cambiano, PageData resta.**

**Conseguenza:** ogni nuovo renderer è additivo. Ogni modifica a `PageData` è un
evento di Foundation, non di X.

---

### D-003 — Runtime never observes the repository directly · `DECISO`

**Contesto:** invariante assoluto del sistema.

**Stato implementativo:** `architectural invariant / implementation audit pending`.
Dal call graph è emerso `getContext → isExperienceVisible → BundleCollector`.
Non ancora verificato se sia esecuzione vera nel request path o dipendenza statica
transitiva.

**Conseguenza:** `AF-001` è P0, gate per l'Osservatore (0.6.5), chiusura in `0.6.3-C`.

---

### D-004 — Return-to-origin via `next`, nessun `hostApp` · `DECISO`

**Contesto:** dove va l'utente dopo il login.

**Decisione:**
```text
Protected resource → Login(next=resource) → Success → next
Standalone login   → Login(no next)       → Success → auth/welcome
```
*"Return-to-origin already exists for policy-driven authentication through `next`;
no origin is preserved for standalone authentication."*

**NON** aggiungere `afterLogout` ad `ApplicationDefinition`.

**Conseguenza:** `next` è dato di sicurezza → centralizzare in
`validateInternalReturnPath(next)`. Rifiutare URL esterni, protocolli, forme ambigue,
`//`, `/\`. Rimuovere l'hardcoded `/build/core-admin/dashboard` da `auth/pages/success.ts`.
La logica post-auth appartiene al workflow Auth, **non** a `PageController`.

---

### D-005 — Page semantics select the renderer; application identity does not · `DECISO`

**Contesto:** PRD 0.6.3-A-R1, validato in implementazione.

**Decisione:** principio confermato. `WebPageTemplate` per experience informative,
`AuthTemplate` per workflow interattivi — **senza modificare** `ApplicationDefinition`,
`ApplicationContext`, `PageController`, `PageData`, `normalizeToPageData`,
`Discovery`, `BundleCollector`.

**Conseguenza:** il flusso valido è
`Session → Policy → Experience Projection → Semantic Renderer`, senza Runtime V2.

---

### D-006 — Experience Projection, non secondo normalizzatore · `DECISO`

**Contesto:** `projectSessionAwarePageData()`.

**Decisione:** può usare **solo** `PageData` + `UserSession`.
**Non** può: Discovery, accesso al Bundle, valutazione policy, accesso al repository,
creazione di contesto. **Non** può mutare il `PageData` originale.

---

### D-007 — Infrastructure reusable, Domain replaceable · `DECISO`

**Contesto:** PRD 0.6.3.5 Explorer Infrastructure Extraction.

**Decisione:** nuova invariante da validare esplicitamente.
`HomePagesDashboard` contiene due responsabilità accoppiate:
Explorer Infrastructure (toolbar, search, filters, stats, entity cards, grid, layout)
e Discovery Domain Logic (consumer DiscoveryService, filtri source/policy/template,
metadata Redis, AI pages, discovery groups). Vanno separate.

**Vincolo:** `dashboardRegistry` resta nel **layer Experience**, non in
Foundation/Runtime/PageData. Il registry è un router di renderer, **non** un contratto.

---

### D-008 — Nessun motore di workflow adesso · `DECISO`

**Contesto:** Temporal Cloud valutato (~100–500 $/mese, no free tier).

**Decisione:** **non adottare Temporal.** Principio: *prima i contratti, poi i motori.*
Il Brain oggi è FastAPI stateless su Fly con auto-stop: run brevi request/response.
I contratti di workflow si dichiarano e versionano **senza** engine.

**Trigger per riconsiderare:** quando X avrà run di ore/giorni con step resumable.
Ordine di valutazione a quel punto: **Inngest → Trigger.dev → DBOS → Temporal.**

---

### D-009 — Embeddings: interfaccia subito, provider mai (per ora) · `DECISO`

**Contesto:** DeepSeek non ha endpoint embeddings (chiusa come "not planned").

**Decisione:** astrazione `EmbeddingsProvider` dal giorno uno, **nessun provider
a pagamento**. Per corpus solo/piccolo, FTS/trigram Postgres o SQLite FTS5 copre il 95%.

**Schema:** embedding come **proiezione separata**, non colonna su `chunks`.
```sql
chunks(id, source_uri, content_sha, content)
chunk_embeddings(chunk_id, embedding_model, embedding_dim, embedding,
                 PRIMARY KEY (chunk_id, embedding_model))
```
Cambio provider = inserimento di nuove righe di proiezione, **non** migrazione
distruttiva.

---

### D-010 — Il DB è indice derivato, non source of truth · `DECISO`

**Contesto:** il repo Brain non ha storage; Fly machine 1 vCPU/1GB senza volume.

**Decisione:** se la source authority è git/bundle/contratti, l'indice è
**ricostruibile al boot**. Upgrade path:
```text
1. indice locale/effimero (SQLite/FTS, €0)
2. Neon/Supabase EU       (quando serve pgvector/embeddings)
3. Fly Postgres fra       (quando si vuole single-vendor in produzione)
```

---

### D-012 — AF-001 è chiuso su `feature/catalog-registry-authority` · `DECISO`

**Contesto:** validazione read-only del 2026-09-10 (report completo in
`05-AF001-VERDETTO.md`).

**Decisione:** `Runtime → BundleCollector` **non è più nel request path**. La catena
`getApplicationType → new BundleCollector().collect()` è sostituita da
`APPLICATION_TYPE_PROJECTION[appId]`, `Object.freeze`, puro, no I/O.
`new BundleCollector` resta solo in 3 endpoint `/api/catalog/*`, che sono superficie
PRODUCE, non EXECUTION.

**Evidenze:** `search_code` (10 hit, zero in `controllers/`, `core/navigation/`,
`core/runtime/`), `trace_path` bidirezionale (callees: 0), lettura sorgente diretta,
`tests/contracts/artifact-consumption-closure.test.ts` come guard di parità.

**Conseguenze:**
1. **NX-01b è SBLOCCATO** — lo split PRODUCE remoto / EXECUTION locale è pulito.
2. La tesi "AF-001 come prerequisito commerciale" è **falsificata**. Correzione
   accettata: *oggi stai mantenendo pulito, non costruendo.*
3. Il metodo di chiusura (tabella statica di 5 app) è **strutturalmente incapace di
   rappresentare la sesta** → blocco a 0.7.0. Vedi P-006.
4. Residuo da verificare: freshness indice (2 file `metadata_changed`).

---

### D-013 — Authority Drift Pattern · `DECISO`

**Osservazione:** AF-001 closure e F-01 sono la stessa malattia.

```text
Ogni volta che un valore che dovrebbe essere DERIVATO dal bundle
è HARDCODATO nel sorgente, il bundle smette di essere source authority.
```

| | Valore | Dovrebbe venire da | Viene da |
|---|---|---|---|
| **F-01** | Registry ID | bundle | `BundleCollector → title slugging` |
| **AF-001 closure** | `applicationType` | bundle | tabella frozen nel sorgente |

Coerente col debito già registrato: *"Page Source Authority non formalized."*

**Conseguenza:** AF-001 è stato chiuso **pagando con Source Authority**. Trade
legittimo per 0.6.x (set di app congelato), debito esatto che 0.7.0 deve ripagare.
Da documentare in `ADR-008` insieme all'Identifier Authority Drift.

---

### D-015 — Due percorsi di generazione AI con due strutture di costo · `DECISO`

**Origine:** benchmark ToolJet (`../documentation/research/benchmarks/TOOLJET-benchmark.md` § 5).

ToolJet ha due percorsi:

```text
ToolJet AI (built-in)  → ToolJet paga i token → vende crediti
ToolJet MCP            → l'utente porta il proprio modello → ToolJet paga ZERO
```

**Decisione per Nexus:** adottare la stessa dualità.

```text
Percorso A — Brain paga (FastAPI + DeepSeek)
  per: generazione assistita in-app, utenti senza agente proprio
  costo: token a carico tuo, da meterizzare

Percorso B — BYO model via nexus-mcp
  per: Roo Code / Claude Code / Codex / Cline / Cursor
  costo: intelligenza a carico dell'utente, tu paghi solo compute
```

**Conseguenza:** il Brain non deve essere "il posto dove sta l'AI". Deve essere il
**contract server**. Il vincolo `< 10 €/mese` smette di essere un vincolo sul
percorso B, perché il costo dell'intelligenza si sposta sull'utente.

Ricalibra D-009/D-010: restano validi, ma si applicano al percorso A.

#### CHIARIMENTO CRITICO — "usare un modello economico" NON è il percorso B

Errore di lettura possibile e molto costoso: confondere *ottimizzazione del costo
dei token* con *trasferimento del costo all'utente*. Sono cose diverse.

```text
                     CHI GENERA       CHI PAGA I TOKEN   QUANDO
────────────────────────────────────────────────────────────────────────
1. Roo/Cline oggi    il tuo agente    TU                 sviluppo (tuo IDE)
2. Brain FastAPI     il tuo server    TU                 runtime del prodotto
3. ToolJet AI built  il loro server   LORO               runtime del prodotto
4. ToolJet MCP       l'agente utente  L'UTENTE           runtime del prodotto
────────────────────────────────────────────────────────────────────────
```

- `deepseek-flash` ottimizza le righe **1** e **2**. Abbassa la bolletta.
- **Non crea la riga 4.** La riga 4 richiede `nexus-mcp` esposto agli agenti degli
  utenti → **NX-14**.

Differenza di conseguenza:

```text
riga 2  → il tuo costo CRESCE con il numero di utenti
riga 4  → il tuo costo NON cresce: l'intelligenza la porta chi genera
```

Per un progetto singolo con vincolo `< 10 €/mese`, la riga 4 non è un'ottimizzazione:
è **l'unica struttura di costo sopravvissibile a scala**.

#### "Contract server" — due metà, servono entrambe

```text
metà 1 — IL GATE              l'output passa dai contratti (NX-03 VALIDATE)
metà 2 — IL TRASFERIMENTO     l'intelligenza la porta l'agente dell'utente (NX-14)
```

La metà 1 senza la metà 2 continua a farti pagare i token del Brain.
La metà 2 senza la metà 1 ti rende un proxy inutile: senza gate, l'agente può
generare qualunque cosa e tu non hai nulla da vendere se non compute.

**Servono entrambe, e NX-14 + NX-03 sono la stessa mossa vista da due lati.**

---

### D-016 — Rendi permissivo ciò che ti porta utenti, protetto ciò che li serve · `DECISO`

**Origine:** ToolJet usa AGPL-3.0 per la piattaforma, submodule git privato per l'EE,
licenza MIT/ISC per il MCP server.

**Regola estratta:**

```text
MCP server / contratti / cataloghi  → PERMISSIVO (è la porta d'ingresso, non il moat)
Piattaforma / engine                → PROTETTO  (AGPL o source-available)
Feature enterprise                  → PRIVATO   (submodule, mai nel repo pubblico)
```

Il MCP server non contiene valore proprietario: espone API governate + cataloghi
generati. Il valore sta nella piattaforma che le esegue.

---

### D-014 — Strategia fuori dal repo · `DECISO`

**Contesto:** l'agente ha cercato `04-FOUNDATION-API.md` nel repo e non l'ha trovato.
Comportamento corretto, ma il confine va reso esplicito.

**Decisione:**
```text
nel repo    → docs/architecture/AF-*.md, ADR, test  (debito tecnico, pubblicabile)
fuori repo  → NEXUS-LAB/*  (strategia, IP, licensing, analisi competitiva)
```

**Regola:** nel prompt all'agente si incolla **solo la sezione specifica** necessaria,
mai il documento strategico intero.

**Nota positiva:** l'agente ha dichiarato `NOT FOUND` invece di inventare. I guardrail
anti-allucinazione del § 4 di `03-WORKFLOW.md` stanno funzionando.

---

### D-011 — `AUTH_API_KEY` separata da `DEEPSEEK_API_KEY` · `DECISO`

**Contesto:** le route usano la chiave del provider come chiave API del server
(`routes/agent.py`, `routes/ai_page.py`).

**Decisione:** separare nel primo PR. Nota: **non** rimuovere `gunicorn` alla cieca —
verificare `fly.toml` con grep prima. `nicegui` e `python-multipart` rimuovibili solo
dopo grep.

---

## PROPOSTE (non ancora decise)

### P-001 — Licenza offline firmata per la CLI Nexus · `PROPOSTO` · **NX-01**

Derivata dall'osservazione di Trustable (§ 3.1 del dossier).

```text
nexus init / dev / build / preview locale   → FREE, nessuna licenza
nexus publish                               → licenza + host allowlist
nexus bundle export                         → licenza
Verifica                                    → Ed25519, public key nel binario CLI
Token                                       → nexus_lic_...
Payload                                     → who, issued_at, expiry, hosts[], tier
```

**Perché:** monetizza il confine di **egress**, non l'uso. Nessun license server,
nessun phone-home, funziona air-gapped. Permette **Foundation chiusa/source-available
+ CLI binaria firmata + X premium** senza scegliere una licenza OSS e senza regalare
l'intuizione architetturale. Il kernel non esce; esce il contratto.

---

### P-002 — Workflow Contract dentro il bundle · `PROPOSTO` · **NX-02**

`workflow.md` come working copy alla root del bundle, committato e pubblicato con esso.
*"La ricetta che ha costruito un'applicazione resta con quell'applicazione."*

Da Trustable, semantica step da adottare quasi verbatim:
```text
NOT RUN / RUNNING / RUN     (colore + nome, mai solo colore)
stato persiste attraverso chiusura e ripresa sessione
prompt ri-letto al momento dell'esecuzione
step fallito → termina la run
Stop → selezione resta sullo step fermato → resume da lì
```

Da aggiungere (assente sia in Trustable sia in Instruqt): **gate `VALIDATE`** → NX-03.

---

### P-003 — Narrativa di scala a tre tier · `PROPOSTO` · **NX-07**

```text
One repository   → local:        nexus dev, zero infrastruttura
One team         → hosted:       Vercel/Fly, bundle pubblicati
One organization → sovereign:    engine firmato, host allowlist
```

Riferimento: *"Same platform, same applications, same tooling at every tier — only the
hardware underneath changes. You are never migrating, only growing."*

---

### P-006 — Application Type Projection come Build Artifact · `PROPOSTO` · **NX-11**

**Problema:** `APPLICATION_TYPE_PROJECTION` hardcodata con 5 app. Un bundle autorato
in 0.7.0 produce un `appId` nuovo → `undefined` → `buildNavigation` riceve tipo
indefinito.

**Risoluzione proposta** (è il principio Foundation/Execution applicato a un valore):

```text
ApplicationDefinition dichiara applicationType
        ↓
BundleCollector.collect()          PRODUCE, build-time/remoto
        ↓
Build Artifacts ⊃ application-type-projection.json
        ↓
getApplicationType() legge l'artifact   EXECUTION, read-only, no accesso al repo
```

Rispetta *"Runtime never observes the repository directly"*: l'artifact è dato, non
sorgente.

**Conseguenza strategica:** NX-01b non è bloccato da AF-001. **NX-01b è la
risoluzione di AF-001** — sostituisce il placeholder con il meccanismo reale.

**Dipende da Q-005.**

---

### P-007 — I 3 endpoint `/api/catalog/*` sono l'embrione della Foundation API · `PROPOSTO`

```text
GET /api/catalog/applications        → new BundleCollector().collect()
GET /api/catalog/applications/[id]   → new BundleCollector().collect()
GET /api/catalog/metrics             → new BundleCollector().collect()
```

PRODUCE già esposto come API, già isolato fuori dal path di EXECUTION. NX-01b non
parte da zero: parte da tre endpoint con la forma giusta.

| Stato attuale | Target NX-01b |
|---|---|
| in-process (stessa app Astro) | servizio remoto o engine firmato on-prem |
| nessuna autenticazione | token scoped + metered |
| output non firmato | Build Artifacts firmati + versionati |
| solo lettura catalog | `POST /v1/compile`, `POST /v1/validate` |
| projection hardcodata | projection emessa come artifact |

Il branch si chiama `feature/catalog-registry-authority`: l'asse è già quello.

---

### P-005 — Foundation API tokenizzata, split PRODUCE remoto / EXECUTION locale · `PROPOSTO` · **NX-01b**

Spec completa in `04-FOUNDATION-API.md`.

**Tesi:** Foundation deployata come API tokenizzata; l'utente interagisce solo coi
contratti (pubblici); X → AI → API → Foundation API.

**Correzioni applicate:**
1. La **minificazione non protegge niente** — compra ore, non mesi. L'unica protezione
   reale è non spedire la logica.
2. Foundation **non può essere tutta remota**: ogni render chiamerebbe l'API
   (latenza, costo, single point of failure, contraddice la storia sovereign).

**Soluzione:** lo split corre lungo il boundary già congelato.
```text
FOUNDATION produce   (build-time)   → REMOTO, tokenizzato, mai spedito
EXECUTION esegue     (request-time) → LOCALE, sottile, artifacts firmati
```
L'invariante *"Runtime never observes the repository directly"* è ciò che lo rende
possibile: il Runtime consuma **dati** (Build Artifacts), e i dati possono viaggiare.

**Build-time dependency ≠ runtime dependency:** il server può essere giù e l'app del
cliente continua a servire.

**Pubblica il contratto, nascondi il compilatore** (HTML è pubblica dal 1993, nessuno
ha clonato Blink in dieci giorni). Effetti: il formato diventa standard, il costo di
adozione va a zero, il valore si sposta su compilatore + validator + migration engine
+ telemetria.

**Moat composto:** API tokenizzata = telemetria di compilazione = dataset che nessun
clone può comprare perché si accumula solo servendo utenti reali.

**Due trasporti:**
```text
hosted   → token API, metered, telemetria attiva
on-prem  → engine binario firmato + licenza offline (NX-01), telemetria opt-in
```

**Collegamento critico:** `AF-001` (Runtime → BundleCollector nel request path, P0)
se confermato rende lo split remoto/locale non pulito. In quel caso AF-001 cessa di
essere debito tecnico e diventa **prerequisito commerciale**.

---

### P-004 — Executable Knowledge Contract (da analisi Instruqt) · `PROPOSTO`

```yaml
experience:
  id: lab-soc-agentic
  steps:
    - id: s1
      instruction: "Configura l'agent con il policy file"
      validation: check-host          # gate deterministico
      environment: vertex-sandbox
      on_skip: solve-host
      on_cleanup: cleanup-host
```

**Vincoli:** PageData resta il linguaggio. Si aggiunge un renderer
(`LabExperienceTemplate` / `WorkflowExperienceTemplate`), **non** un contratto core.
`EnvironmentProvider` è un provider di esecuzione, **non** Runtime.

---

## DOMANDE APERTE

### Q-005 — `applicationType` è dichiarato o inferito? · `APERTO` · **RISTRETTA**

**AGGIORNAMENTO 2026-09-12:** `APPLICATION_TYPE_PROJECTION` sta in
`src/core/domain-authority/projections/`, ed esiste `src/config/applications`
= Application Authority (D-022). La domanda diventa:

```text
applicationType è DICHIARATO in src/config/applications/<app>/ ?

SE SÌ  → la projection è una derivazione congelata a mano invece che calcolata.
         NX-11 = sostituire la tabella con la proiezione emessa da BundleCollector.
         ZONA SICURA, nessun cambio di contratto, lavoro piccolo.
SE NO  → Application Authority non copre il tipo → FOUNDATION RFC.
```

Dato che Application Authority è appena stata formalizzata, il caso SÌ è molto più
probabile. Verifica con un comando:

```bash
grep -rn "applicationType\|appType" src/config/applications/ | head -20
```

```text
Se DICHIARATO in ApplicationDefinition
  → la projection è derivazione pura, deve diventare Build Artifact
  → lavoro piccolo, nessun cambio di contratto
  → resta ZONA SICURA

Se INFERITO
  → contract gap: l'authoring 0.7.0 non può esprimerlo
  → serve un campo nuovo in ApplicationDefinition
  → FOUNDATION RFC, esce dalla zona sicura
```

**È l'unica domanda che giustifica `deepseek-v4-pro`.** Tutto il resto di AF-001 è
già stabilito da evidenze.

---

### Q-006 — Fallback per `appId` assente nella projection · `APERTO` · **NX-12**

Oggi `APPLICATION_TYPE_PROJECTION[appIdNonPresente]` → `undefined`.
Comportamento da verificare: `undefined` silenzioso, `throw`, o default?

**Il degrado silenzioso è peggiore del crash**: un crash si vede in test, un
`undefined` che scivola in `buildNavigation` produce navigazione sbagliata senza
errore.

---

### Q-001 — Strategia di distribuzione / licensing · `APERTO` · **opzione concreta disponibile**

Opzioni sul tavolo: MIT open-source · BSL 1.1 / Fair-Code · Elastic License 2.0 ·
PolyForm Noncommercial/Shield · AGPL · dual licensing · binary-only SDK ·
cloud-first zero-distribution · **open spec + closed implementation**.

Vincolo dell'utente: **non regalare l'intuizione architetturale troppo presto**;
paura concreta di cloni/fork/appropriazione. Precedente: OpenFav auth open-source
→ **zero impression**.

P-001 è la risposta tecnica che rende la domanda meno urgente.

**AGGIORNAMENTO 2026-09-10 — schema ToolJet, già validato in produzione**
(`../documentation/research/benchmarks/TOOLJET-benchmark.md` § 4):

```text
┌─ PIATTAFORMA    AGPL-3.0 (o source-available)
│   → copyleft forte: chi fa fork e lo offre come SaaS DEVE aprire
│   → è il meccanismo anti-clone, e non richiede license server
├─ ENTERPRISE     submodule git privato (frontend/ee, server/ee)
│   → il codice premium NON ENTRA nel repo pubblico
│   → symlink + script idempotente lo rendono invocabile dalla root
└─ MCP SERVER     MIT / permissivo, repo separato
    → è la porta d'ingresso, non il moat → si regala
```

**Perché risponde al vincolo dell'utente:** l'AGPL è l'unica licenza OSS che
punisce esattamente lo scenario temuto — il clone che diventa SaaS concorrente.
Un fork interno/privato resta permesso (e va bene: crea adozione), ma offrire il
fork come servizio obbliga ad aprire le modifiche. Chi vuole clonare e vendere
deve o aprire il proprio lavoro o comprare una licenza commerciale.

**Dual licensing** diventa l'ovvia estensione: AGPL per la community, licenza
commerciale per chi non vuole l'obbligo di apertura.

**Resta da decidere:** se Foundation è AGPL o source-available (BSL/Elastic), e se
il submodule privato è accettabile come complessità operativa per un progetto singolo.

---

### Q-002 — Nome pubblico · `APERTO` · **NX-10**

`OpenFav` vs `Open Nexus` vs `Nexus Lab`. Verificare collisioni (Sonatype Nexus,
storico Google, naming `tru*`/`NuvolarIA` di Nuvolaris) su UIBM/EUIPO **prima** di
investire nel brand. Decidere ora evita di migrare SEO + repo + identità dopo.

---

### Q-003 — Sei contract drift da classificare · `APERTO`

```text
CD-01  Open Nexus afterLogin: expected open-nexus/library, actual open-nexus/index
CD-02  Operations Identity:  expected "OpenFav Admin", actual "Operations"
CD-03  Shared Consumers:     0.6.1 contract vs metadata corrente
F-01   Identifier Authority Drift: Registry ID ≠ Bundle-derived ID
       causa: BundleCollector → title slugging → documentare in ADR-008
```
Global Contract Suite 🟡 — baseline non verde, non congelata.

---

### Q-004 — Debito auth aperto · `APERTO`

```text
P0  AF-001  Runtime → BundleCollector nel request path   (gate per 0.6.5)
P1  AF-003  Server Session Recovery (timeout/fallback/availability Redis)
P1  AF-004  Client Session Reconciliation (più producer scrivono userStore)
P2  AF-002  Discovery Amplification (misurare/consolidare chiamate)
P2  Cross-tab Auth Synchronization (solo se requisito di prodotto)
P3  Theme event propagation + monkey patch localStorage
    0.7.0   Identifier / Page Source Authority
```

Nota: **non** esistono `BroadcastChannel` né storage listener. Il comportamento
multi-tab osservato è condivisione server-side della sessione a nuova
request/rehydration, **non** sync cross-tab real-time.

---

## SCARTATI

### S-001 — Temporal Cloud · `SCARTATO`
Costo ~100–500 $/mese, no free tier. Overkill per run request/response. Vedi D-008.

### S-002 — Provider embeddings a pagamento · `SCARTATO` (per ora)
Vedi D-009. Si rivaluta al trigger: corpus grande o ricerca semantica come feature X.

### S-003 — StackBlitz per sviluppo Python in browser · `SCARTATO`
WebContainers è Node-only. GitHub sync rimosso/rotto
(`stackblitz/core#3560`). Alternativa valida se serve: GitHub Codespaces
(120 core-hours/mese free) o `code-server` su Fly (~3–6 €/mese).

### S-004 — `hostApp` state / `afterLogout` in ApplicationDefinition · `SCARTATO`
Vedi D-004. `next` copre già il caso policy-driven.

---

*Ultimo aggiornamento: 2026-09-10*

---

## D-015bis — Delimitare la riga 2, sdelimitare la riga 4 · `DECISO`

**Contesto:** obiezione dell'utente — *"abbiamo usato solo il 5% di AI, il resto può
solo crescere se ci orientiamo bene, ma non ci andiamo a dissanguare con gli ultimi
modelli Claude."*

**Parte corretta dell'obiezione:** se solo il 5% del sistema dipende dall'AI, allora
il 95% del valore (Foundation, contratti, boundary, invarianti) è deterministico e
costa **zero token**. È una posizione genuinamente forte: la maggior parte dei
prodotti AI è dipendente all'80% e ha quindi strutture di costo brutali.

**Parte che non risponde alla domanda:** "quanto spendo oggi" ≠ "cosa succede al
costo quando ho utenti". Sono due conti separati:

```text
COSTO DI SVILUPPO   tu, Roo/Cline, DeepSeek    → una tantum, cresce con le TUE release
COSTO OPERATIVO     il prodotto che serve      → ricorrente, cresce con i LORO utenti
```

Il secondo è l'unico che può uccidere, perché **scala col successo, non con lo sforzo**.

### Evidenza che la riga 2 è già attiva nel prodotto

Dalla scansione MCP del repo Astro, route AI già deployate:

```text
/api/v1/pages/generateAiPage
/api/v1/ai/pages            (e ?userId=public)
/api/v1/chat/aiRequests
/api/refresh-ai-pages
/api/v2/discovery/generate
```

Più le pagine `open-nexus/assistant` e `open-nexus/generated-knowledge` su
`https://openfav.vercel.app`.

**Conclusione:** il prodotto ha già AI nel request path. Non è un'ipotesi futura.

### L'argomento decisivo: la roadmap di X è un moltiplicatore

```text
X cresce da 5% → 50% di AI (è il piano dichiarato: X = AI-governed knowledge OS)

riga 2 (tu paghi)        costo × 10
riga 4 (paga l'utente)   costo × 1
```

**Più X ha successo, più la riga 2 punisce e la riga 4 premia.** La roadmap stessa
è un argomento *a favore* di NX-14, non contro.

### Disciplina vs struttura

```text
Disciplina  "uso flash, non uso Claude"    → regge finché te lo ricordi
Struttura   "l'utente porta il modello"    → regge sempre, anche se te lo dimentichi
```

Con NX-14, se un utente vuole generare un bundle con il modello più caro del
mercato, **paga lui e tu ricevi un bundle generato meglio gratis**. Non limiti la
scelta del modello: la rendi problema e piacere dell'utente. Esci dal business del
costo dei modelli.

### La sintesi: non scegliere, delimitare

ToolJet fa esattamente questo e non sceglie fra i due percorsi:

```text
RIGA 2 — DELIMITATA
  superficie: demo, onboarding, assistant in-app
  natura:     costo di marketing, bounded
  strumento:  crediti / metering / max_output_tokens per classe
  cresce con: il numero di utenti curiosi, non di utenti produttivi

RIGA 4 — SDELIMITATA
  superficie: authoring produttivo via nexus-mcp
  natura:     costo zero per te
  strumento:  NX-14
  cresce con: zero
```

### Onestà sul timing

`flash` a basso volume regge: 100 utenti × 10 generazioni/mese ≈ 6M token/mese,
pochi euro. Il crossover arriva con la scala, non subito.

> **`flash` ti compra tempo. Non ti compra struttura.**

E NX-14 è economico da costruire **adesso** e costoso da retrofit **dopo**, perché
non è una feature: cambia *cosa è il prodotto*.

---

---

### D-017 — Degradation Budget · `DECISO`

**Origine:** osservazione dell'utente — *"Degradazione, non crash. Il server non deve
morire perché DeepSeek ha cambiato un nome — è il presupposto di Foundation."*

L'osservazione è corretta e generalizza oltre il caso del provider.

#### Il principio

> **Un sistema con un core deterministico può degradare.
> Un sistema senza core deterministico può solo fallire.**

Perché: degradare richiede di sapere cosa è **essenziale** e cosa è **miglioramento**.
Se tutto è generato a runtime dall'AI, quando l'AI cade non c'è niente *verso cui*
degradare. Se il core è deterministico, quando l'AI cade resta un prodotto.

#### Definizione

```text
DEGRADATION BUDGET
  la quota di funzionalità che sopravvive alla caduta di una dipendenza esterna
```

#### Misura comparata

| Dipendenza caduta | Open Nexus | ToolJet |
|---|---|---|
| LLM provider | tutto tranne l'interpretazione | tutto (non è nel path) |
| Redis | stato locale (NX-20) | n/a |
| Foundation API | artifacts già compilati (NX-01b) | n/a |
| **PostgreSQL** | artifacts statici serviti | **NULLA — le app SONO righe di DB** |

L'ultima riga è quella decisiva: ToolJet non ha una storia di degradazione perché la
definizione *è* il dato vivo. Se cade Postgres, non hanno prodotto. Le app Open Nexus
sono artefatti compilati: se cade il DB o l'API, gli artifacts continuano a servire.

> **Il boundary non è solo una garanzia semantica. È un budget di degradazione.**

#### Conseguenza: il 5% è un asset

"Di fatto non stiamo usando AI" non è una carenza di adozione. È il budget di
degradazione: **se solo il 5% dipende dall'AI, il 95% continua a funzionare quando
l'AI cade.**

Corollario di progettazione: la quota AI può crescere, ma il degradation budget deve
restare alto. Se X arriva al 50% di AI, il 50% deterministico deve continuare a
servire un prodotto completo — non un prodotto monco.

#### Test di design (da aggiungere al PRD)

```text
Per ogni dipendenza esterna: cosa sopravvive se cade?
Se la risposta è "niente", quella dipendenza è nel core.
Va spostata oltre il boundary.
```

È la stessa forma delle invarianti già congelate — un vincolo espresso come divieto:

```text
già esistente   Runtime never observes the repository directly
nuova           Execution never requires Foundation at request time   (NX-01b)
nuova           No external dependency in the request path
                of a compiled artifact
```

La seconda era già implicita in NX-01b, ma adesso ha una **seconda giustificazione
indipendente**: non solo distribuzione e costo, anche resilienza. Tre ragioni per lo
stesso boundary lo rendono molto più difficile da negoziare in futuro.

#### Pattern ricorrente già riconosciuto dall'utente

```text
Redis       "se redis manda un ping l'applicazione si sincronizza,
             altrimenti resta in locale"                    → NX-20
LLM         "catalogo mancante → 503 sulle route AI,
             server vivo"                                   → NX-26
Foundation  "API giù → artifacts già compilati servono"     → NX-01b
```

Tre dipendenze diverse, **lo stesso pattern**. Non è una coincidenza: è il boundary
che si applica a ogni confine di rete. Va nominato una volta e riusato, non
riscoperto tre volte.

---

### D-018 — Il server Brain è confermato FastAPI · `DECISO`

Il refactor in corso riguarda il **Brain FastAPI**, non il lato Node/Astro.
`09-SERVER-PROVIDER-LAYER.md` si applica come scritto (§ 2–§ 6 incluse).

Punti 4 (`routing.py`, classi di costo enforce server-side) e 5 (`budget.py`,
strumentazione e guardrail) approvati dall'utente.

**Nota:** il repo del Brain ha un path diverso dal repo Astro già indicizzato in
`codebase-memory-mcp`. Va indicizzato separatamente con `index_repository` prima
di qualunque audit — altrimenti `search_graph` restituisce risultati del repo
sbagliato.


---

### Q-007 — Linguaggio della libreria di scraping · `APERTO`

Se Python → vive in `modules/connectors/` del Brain, accanto a `modules/reduce/`.
Se JS/TS → va deciso se il Brain la chiama via subprocess/API o se il connettore
viene riscritto in Python. **Un connettore in due linguaggi è un connettore mantenuto
due volte.**

### Q-008 — Dove sta lo stato della change detection · `APERTO`

Serve uno stato durevole per `source_uri` (ultimo `content_sha` visto, ultimo `ETag`).
D-010 dice che il DB è indice derivato, non source of truth. Con local-first (NX-20)
la risposta coerente è **stato locale, con Redis come replica**.

### Q-009 — Le fonti hanno API o RSS? · `APERTO`

Da verificare **fonte per fonte, prima di scrivere codice di scraping**. Ogni fonte
con un'API ufficiale è una fonte che non devi scrapare — ed è anche la scelta a
minore rischio legale (`11-CONNECTOR-LAYER.md` § 6).

---

### D-019 — La libreria di scraping esistente diventa `HttpHtmlConnector` · `DECISO`

**Contesto:** l'utente ha già una libreria che dato un URL legge header e HTML con
librerie basic.

**Decisione:** si usa. Diventa **un connettore fra N**, non *il* canale di acquisizione.

```text
Connector (interfaccia unica → dataclass Fetched)
  ├── HttpHtmlConnector     ← la libreria esistente
  ├── JsonApiConnector      ← il valore per la persona broker/CFO sta qui
  ├── PdfConnector          ← filing, bilanci
  └── RssConnector          ← costa quasi niente, spesso batte lo scraping
```

Stessa lezione di ToolJet: **copia l'interfaccia del plugin, non la libreria**.

**Unico upgrade bloccante:** change detection — `content_sha` + flag `changed`, con
conditional request HTTP (`ETag` / `If-None-Match` → 304) come ottimizzazione quasi
gratuita, dato che la libreria legge già gli header. Senza, si rianalizza contenuto
identico e si perde la leva da 20× del trigger deterministico (NX-19).

**Esplicitamente esclusi:** headless browser, rotazione proxy, ML per l'estrazione,
infra distribuita di crawling.

**Nota sulla persona:** per manager/CFO/broker l'HTML è il canale **minoritario**.
Dati di mercato → API/feed. Bilanci → PDF. Lo scraping HTML copre news e comunicati.
Non è motivo per scartare la libreria, è motivo per non fermarsi lì.

`content_sha` è un campo solo con tre usi: schema chunks (D-009), cache di
ricompilazione (NX-01b), trigger deterministico (NX-19). Va progettato una volta.


---

### D-020 — CORREZIONE: il verticale "CAPISCE" è occupato · `DECISO`

**Contesto:** `07-PERSONA-AUTHORITIES-COSTO.md` § 1.2 affermava che il supporto alla
decisione per ruoli non tecnici "non ha concorrenti diretti nel set analizzato".

**Correzione:** non ne aveva perché il set analizzato era di **app builder**.
Nel verticale dichiarato (manager / CFO / broker che esplora e forma convinzioni)
i concorrenti esistono e sono fortemente capitalizzati. Analisi in
`12-MERCATO-CONOSCENZA.md`.

```text
AlphaSense   500M+ documenti premium · $350M raccolti giu 2026 · seat a 5 cifre
Hebbia       $130M Series B @ $700M (a16z, Thiel, Schmidt) · 1B+ pagine
             profittevole a $13M ARR, >2% del volume API giornaliero di OpenAI
Rogo         35.000+ professionisti in 250+ istituzioni (Lazard, Rothschild,
             Jefferies, Nomura, Tiger Global, Baird)
Aiera        "Compliant Access Layer" · API enterprise + MCP · entitlement-aware
```

**Il loro moat non è architetturale:** è contenuto, distribuzione, compliance.

**Due conseguenze opposte, entrambe vere:**
```text
BRUTTA   sul contenuto non puoi competere. Nel finanziario head-on si perde.
BUONA    non avendo un moat architetturale, non difendono l'architettura.
         Nessuno ha boundary compilato, PageData portabile, degradation budget,
         Graphic Authority. L'output resta intrappolato nel loro renderer.
```

**Conferme ricevute:**
1. La persona dichiarata è un mercato reale, non una fantasia.
2. La diagnosi coincide: *"more time aggregating and searching fragmented sources
   than actually forming conviction"* (AlphaSense).
3. La soluzione converge: Hebbia dichiara che il RAG naive fallisce sull'**84%**
   delle query complesse e risponde con decomposizione in step agentici + output
   strutturato con reasoning chain. È "indeterminismo che diventa determinismo".
4. **Aiera valida NX-01b + NX-14**: contract server + MCP + entitlement in un
   verticale. L'architettura è giusta; qualcun altro l'ha già industrializzata.

---

### D-021 — Tre verbi, non due: OPERA / IMPARA / CAPISCE · `DECISO`

Tassonomia corretta dei benchmark. L'asse discriminante non è *chi costruisce*
ma *cosa fa l'utente finale*.

```text
                        OPERA            IMPARA           CAPISCE
                    ─────────────────────────────────────────────────────
costruisce un dev   Trustable
costruisce author   ToolJet            Instruqt
costruisce agente                                          ← cella VUOTA
non si costruisce                                          AlphaSense · Hebbia
(SaaS chiuso)                                              Rogo · Aiera
```

ToolJet è OPERA: il builder è tecnico ma l'utente finale dell'app costruita è un
impiegato che inserisce/approva/consulta. Instruqt è IMPARA: percorso guidato con
esito misurabile.

La cella `costruisce agente × CAPISCE` è vuota. **Ma non è vuota perché nessuno
l'ha vista**: nella colonna adiacente (`non si costruisce × CAPISCE`) c'è un mercato
da centinaia di milioni. Uno spazio vuoto non è di per sé un'opportunità — il
precedente personale (OpenFav auth, zero impression) è un data point contrario.

---

### Q-010 — In quale verticale il meccanismo vale più del contenuto? · `APERTO` · **NX-30**

La domanda corretta non è *"esiste un clone di Open Nexus?"* (no sul meccanismo,
sì sul bisogno — e la seconda conta di più).

```text
La finanza ha già risposto: vale il CONTENUTO.
Serve un verticale dove la risposta è opposta:
  · il dato è già del cliente
  · è frammentato e regolamentato
  · ciò che manca è la capacità di attraversarlo

candidati: pubblica amministrazione · farmaceutico/regolatorio · energia
           difesa · assicurazioni · manifatturiero normativo
```

Perché è l'unica opzione realistica per un progetto singolo:

```text
1. il vantaggio è normativo/geografico, non di capitale: residenza del dato,
   procurement pubblico che non può comprare SaaS USA
2. è lo stesso terreno di Nuvolaris/Trustable e Regolo.AI — non è un caso
   che siano europei
3. per un ente pubblico boundary compilato, degradation budget (D-017) e
   local-first (NX-20) non sono raffinatezze: sono REQUISITI DI GARA
4. non devi battere AlphaSense: devi essere l'unica opzione conforme
```

**Da falsificare PRIMA di costruire:** l'ipotesi "il mercato premia il contenuto,
non il meccanismo". Metodo: analisi di come Aiera è entrata (fa il layer sopra
contenuti altrui, quindi il meccanismo HA valore in presenza di compliance),
più 5–10 conversazioni nel verticale candidato.


---

### D-022 — Cinque Authority formalizzate in Foundation · `DECISO`

**Fonte:** report dell'utente del 2026-09-12, conferma a voce *"refactoring della
source of truth senza regressioni, andato liscio come l'olio"*.

```text
✅ Application Authority    src/config/applications
✅ Content Authority        src/config/discovery/page-registry
✅ Domain Authority         src/core/domain-authority
✅ Design Authority         src/core/design-authority
✅ Theme Authority          ThemeInjector
```

Il recap ufficiale del 2026-08-20 ne indicava una sola come debito
(*"Page Source Authority non formalized"*). Analisi in `14-AUTHORITY-ARCHITECTURE.md`.

**Roadmap aggiornata:**

```text
0.7.0      ✅ Application · Domain · Design · Theme Authority
0.7.0.1    Primitive Consolidation     → Primitive Authority
0.7.0.2    Design Enforcement          → il gate
0.7.0.3    Presentation Authority      → Asset Ownership, Presentation Manifest
0.7.0.4    Admin New Era
```

Modello a tre livelli già articolato dall'utente:

```text
Design Authority        → meaning
Theme Authority         → state
Presentation Authority  → identity
```

---

### D-023 — Il programma Authority È la cura dell'Authority Drift · `DECISO`

D-013 nominava il pattern (*valore derivabile dal bundle ma hardcodato nel sorgente*).
Il programma dell'utente è l'anti-drift sistematico:

> *"finora non state spostando codice. State continuando a rispondere alla stessa
> domanda: Chi possiede cosa?"*

**Criterio di accettazione per ogni futura authority:**

```text
1. esiste UNA fonte dichiarativa che possiede il valore
2. tutto il resto è PROIEZIONE derivata, non copia
3. la proiezione è emessa da BundleCollector come artefatto,
   non scritta a mano nel sorgente
4. un gate rifiuta le copie non derivate
```

Il punto 3 è NX-11 generalizzato. Il punto 4 è Design Enforcement generalizzato.

---

### D-024 — Design Enforcement deve girare anche su X · `DECISO` · **NX-34**

**Problema:** Design Enforcement (0.7.0.2) è descritto come controllo su codice
scritto da umani (lint su hex colors, `rgb`, `bg-blue-*`, ecc.).

```text
umano scrive codice    → lint lo blocca        ✅
X genera un bundle     → non passa dal lint     ❌ bypass PER COSTRUZIONE
                         del sorgente
```

**Decisione:** lo stesso ruleset va applicato in **due punti**:

```text
├── lint/CI sul sorgente        → per gli umani
└── gate VALIDATE (NX-03)       → per X, sulla PageData generata
```

**Conseguenza implementativa:** il ruleset deve essere **dato dichiarativo**
(lista di pattern + eccezioni), non configurazione di ESLint. Se è dato, lo consumano
entrambi i punti. Se è config di lint, X non può usarlo.

È la singola decisione più importante di 0.7.0.2: costa poco adesso che il ruleset
va scritto comunque, è costosissima dopo.

---

### D-025 — UX: dimensionata sul verbo, non in ritardo · `DECISO`

Tesi dell'utente: *"la UX potrebbe essere un limite o un'opportunità"*.

**Risoluzione:** D-021 dice che ToolJet è OPERA e Open Nexus è CAPISCE. I due verbi
richiedono superfici diverse, non di quantità diversa.

```text
OPERA richiede        form, input, tabelle editabili, CRUD, drag & drop
                      → 80+ componenti

CAPISCE richiede      testo, evidenza, citazione, confronto, serie storica,
                      score/soglia, alert, timeline
                      → ~12 primitive
```

**Non è ritardo, è dimensionamento.** Costruire 80 primitive per un prodotto CAPISCE
sarebbe l'errore: competizione sul terreno di chi ha 17.447 commit di vantaggio.

**Perché è opportunità strutturale:**

```text
ToolJet    complessità accumulata senza Primitive Authority
           → coerenza dipende dalla review, che dipende dalle persone
Open Nexus  Primitive Authority + Design Enforcement
           → coerenza è enforcement, non disciplina
```

*La complessità UI si aggiunge dopo. La governance della UI va avuta prima.*
Da qui *"è una spugna, puoi prendere tutto"*: con l'inventario chiuso, assorbire un
pattern esterno costa **una primitiva**, non un renderer.

---

### D-026 — Quinta stratificazione sopravvissuta · `DECISO`

```text
stratificazioni 1-4   sopravvissute (pattern Astro+React, test all'80%)
stratificazione 5     authority refactor sulla source of truth, no regressioni
                      ("qualche bordo")
```

È la prova empirica della tesi di invarianza, con cinque punti dati invece di quattro.

**Rilevanza per Q-001 (IP):** un sistema che assorbe un refactor della source of
truth senza rompersi non è clonabile in dieci giorni, perché la proprietà che lo
rende tale non sta in nessun file — sta nella disciplina di assegnare ownership
prima di scrivere codice.

**Residuo da catturare (NX-37):** i "bordi". In un refactor di authority, un caso
bordo è un punto dove un valore ha **due** proprietari. Verificare se la correzione
è stata "allineare la copia" o "cambiare la fonte": se è stata la prima, esiste
ancora una copia non derivata.


---

### D-027 — Formalizzare la posizione non è formalizzare la proprietà · `FALSIFICATO`

**Contesto:** il grep su `src/config/applications` per `applicationType|appType` ha
restituito zero risultati.

**Prima di concludere:** la ricerca era insufficiente per costruzione — cercava due
NOMI e non i VALORI (`user|workspace|shared`), e non aveva sanity check sul path.
Un falso negativo è indistinguibile da un vero negativo. Sequenza corretta in
`06-PROMPT-Q005.md`, appendice 2026-09-12.

**Se l'esito fosse B (concetto non dichiarato da nessuna parte), il finding è questo:**

```text
Domain Authority è marcata ✅ nello stato di Foundation.
Ma APPLICATION_TYPE_PROJECTION contiene un valore che nessun bundle dichiara.

→ una directory può essere creata, popolata e testata, e contenere ancora
  valori congelati a mano senza fonte dichiarativa.
```

**Principio proposto:**

> Formalizzare la **posizione** di un valore non è formalizzarne la **proprietà**.
> Un'authority è completa solo quando ogni valore che esporta è derivato da una
> fonte dichiarativa, non quando la directory esiste.

**Conseguenza operativa:** il programma "Chi possiede cosa?" (D-023) va applicato
anche come **verifica retroattiva** sulle authority già marcate ✅, non solo esteso
ai domini mancanti (Primitive, Presentation).

Controllo generalizzabile:

```text
per ogni valore esportato da src/core/<x>-authority/:
  · è dichiarato in una fonte (src/config/** o bundle)?  → OK
  · è un letterale nel sorgente?                          → candidato drift
```

**STATO: FALSIFICATO dalle evidenze del 2026-09-12.** Vedi D-028.

`application-type-projection.ts` documenta esplicitamente in testa al file:
fonte dichiarativa (`src/applications/*/package.ts`), colonna autorevole
(`ApplicationCatalog.applications[].type` via `BundleCollector.buildCatalog()`),
regola Build/Runtime, e parità enforced permanentemente da
`tests/contracts/artifact-consumption-closure.test.ts`.

Non è un letterale nudo: è una **materializzazione dichiarata come tale**.
La proprietà È formalizzata. L'ipotesi era sbagliata.

Il principio generale resta valido come criterio di verifica, ma non si applica a
questo caso.

---

### Nota di processo — tre errori dell'assistente in una sessione

Da registrare, perché il pattern è lo stesso:

```text
1. AF-001 come prerequisito commerciale di NX-01b
   → falsificato dalla validazione. Ipotesi affermata con sicurezza prima
     dell'evidenza.

2. Graphic Authority come "terza authority nuova"
   → esisteva già, decomposta meglio. Proposta architettura senza verificare.

3. "scommetto sul primo caso" su Q-005
   → scommessa basata su un grep che cercava i nomi invece dei valori.
```

**Radice comune:** affermare prima di cercare, e cercare nel modo che conferma.

È esattamente ciò che i guardrail di `03-WORKFLOW.md` § 4 servono a impedire — e
valgono per gli agenti quanto per chi scrive i prompt. Regola da aggiungere:

> Ogni affermazione su cosa esiste nel codebase deve citare il comando che l'ha
> prodotta. Zero risultati senza comando non è un dato.


---

### D-028 — ApplicationType: materializzazione manuale da rendere generata · `DECISO`

**Evidenze:** `15-APPLICATION-AUTHORITY-EVIDENZE.md`, lettura diretta dei file.

```text
Fonte dichiarativa   src/applications/*/package.ts        (ApplicationBundle)
Colonna autorevole   ApplicationCatalog.applications[].type
                     prodotta da BundleCollector.buildCatalog()
Consumo a runtime    APPLICATION_TYPE_PROJECTION (Object.freeze, zero I/O)
Parità               tests/contracts/artifact-consumption-closure.test.ts
Regola documentata   Build  → collect() → ApplicationCatalog (authoritative)
                     Runtime → projection (materialized consumption)
```

**Q-005 RISPOSTA.** `applicationType` non è in `ApplicationDefinition`
(`src/config/applications/types.ts`) ma è dichiarato nel **Bundle**
(`src/applications/*/package.ts`). Non è drift: è ripartizione fra due layer.

**Il residuo vero, riformulato:**

```text
oggi    materializzazione MANUALE + test di parità   → corretto per 0.6.x
                                                     (set di app congelato a 5)
0.7.0   Human/AI/Importer producono bundle nuovi
        → la tabella manuale non contiene il nuovo appId
        → il test di parità FALLISCE
        → il test diventa il BLOCCO dell'authoring
```

**NX-11 riformulato:** non "sostituire un hardcode con una derivazione", ma
**sostituire una materializzazione manuale con una materializzazione generata**.
Il commento del file dice già "build-materialized"; oggi è "hand-materialized,
build-verified". La regola Build/Runtime scritta è già quella di NX-01b — manca
solo che il file sia *prodotto* dal build invece che scritto a mano.

**Prerequisito di 0.7.0 Authoring, non di 0.6.x.**

---

### D-029 — Tre layer, non due · `DECISO`

`find src/applications` rivela un layer assente dal report sullo stato di Foundation:

```text
src/applications/          APPLICATION BUNDLE LAYER
  bundle-collector.ts        BundleCollector vive qui
  build-manifest.ts          il build produce già un manifest
  build-report.ts            il build produce già un report
  <app>/{assets, pages, package.ts}    per tutte e 5 le app

src/config/applications/   APPLICATION DEFINITION LAYER
  types.ts (contratti) · factory.ts (bridge) · <app>.ts

src/core/domain-authority/ DOMAIN AUTHORITY
  contracts/ · projections/ · governance/
```

**Conseguenze:**

```text
NX-01b   non parte da tre endpoint catalog (P-007): parte da un layer bundle
         con manifest e report già presenti. Stima al ribasso.
0.7.0.3  assets/ esiste già per tutte le app: manca SOLO presentation.manifest.ts
NX-40    il criterio di ripartizione Definition/Bundle NON è documentato
```

Il boundary in `types.ts` è dichiarato per divieto, stessa forma di
*"Runtime never observes the repository directly"*:

```text
// An Application does NOT describe:
//   - how a page is rendered (that's Rendering's job)
//   - how pages are resolved to URLs (that's Discovery's job)
```

---

### D-030 — I contratti configurabili esistono già, ma non sono enforced · `DECISO`

`DiscoveryMetadata` in `src/config/applications/types.ts` È il
*"contracts facilmente configurabili dall'utente"* della tesi NX-01b: già scritto,
già separato dai runtime contracts, già consumato dall'Hub.

```ts
description · icon · category · status · featured · audience
```

**Ma in `simple.ts` il blocco è popolato con `as any`:**

```ts
createApplicationDefinition('simple', 'Simple', {...}, {
  description: '...', category: 'reference', audience: 'developer',
} as any)      // ← il contratto NON è typechecked nel punto di scrittura
```

**Principio:** un contratto senza enforcement nel punto di scrittura è
documentazione. È D-024 applicato ai contratti di Foundation invece che al design.

Più: `notFound: '/'` viola il contratto dichiarato (`/** 404 fallback registryId */`)
ed è accettato solo perché il tipo è `string`. Stessa classe di F-01: **tipo troppo
largo per il contratto documentato**.

→ NX-38, NX-39, proposta di milestone **0.7.0.2b Contract Enforcement**.

---

### D-031 — `audience` non contiene la persona dichiarata · `DECISO`

```ts
audience?: 'developer' | 'user' | 'operator'
```

La persona dichiarata in `07-PERSONA-AUTHORITIES-COSTO.md` è **decision-maker**
(manager, CFO, broker). Nessuno dei tre valori la copre.

```text
O la persona dichiarata non è un'audience di ApplicationDefinition,
O manca un valore nella union.
```

Da decidere **prima di 0.7.0.3**: Presentation Authority esprime identità rispetto
a un pubblico, e il pubblico oggi non è esprimibile.

**Nota positiva per NX-22:** i due tier Builder/Decision-maker hanno già un campo
dove atterrare. Non serve un contratto nuovo, serve un valore.

**Collisione di vocabolario (NX-41):** `ApplicationType` ha valore `user`
(visibilità) e `audience` ha valore `user` (persona). Significati diversi, stessa
parola.

---

### Nota di processo aggiornata — quattro errori, tutti nella stessa direzione

```text
1. AF-001 come prerequisito commerciale          → falsificato dalla validazione
2. Graphic Authority come novità                 → esisteva già, decomposta meglio
3. "scommetto sul primo caso" su Q-005           → grep cercava nomi, non valori
4. D-027 "valore senza fonte dichiarativa"       → la fonte c'è, documentata e testata
```

**Pattern:** ipotesi di degrado formulate prima dell'evidenza, e smentite
dall'evidenza **ogni volta**. Il codice era più avanti dell'ipotesi in tutti e
quattro i casi.

**Regola confermata e rafforzata:** mai affermare architettura su un codebase senza
aver letto i file. E quattro `cat` hanno prodotto più informazione di tutti i grep
della sessione — perché *solo la lettura del type prova l'assenza*.

---

### D-032 — ADR-0012 Primitive Authority: primo dominio che soddisfa D-023 integralmente · `DECISO`

**Evidenza:** `src/test/unit/primitive-authority.test.tsx` — 21 test, tutti verdi.

```text
src/core/ui-primitives/           primitives.tsx · StatusBadge.tsx · index.ts (barrel)
explorer/primitives.tsx           deprecation shim: re-esporta, non definisce
design-authority/status-tones.ts  React-free, non importa componenti
resolveStatusTone                 meaning → runtime, degrada a muted
```

**Scelte architetturali risolte:**

```text
Dove sta l'authority    src/core/ui-primitives — SIBLING di design-authority e
                        domain-authority, non annidato. Corretto: le primitive sono
                        componenti, il design è meaning. Due cose diverse.

Explorer vs Radix       NESSUNO DEI DUE. Terza sede, con explorer ridotta a shim.
                        Risolve la domanda del report meglio di entrambe le opzioni.

Radix                   resta SOTTO come dipendenza tecnica: 9 superfici presidiate
                        hanno il divieto di import diretto da components/ui/*,
                        enforce da test.
```

**Verifica sul criterio D-023:**

```text
1. UNA fonte dichiarativa                    ✅ status-tones.ts
2. tutto il resto è proiezione, non copia    ✅ "nessuna copia locale in explorer"
                                                EntityCard e ApplicationsTable
                                                consumano StatusBadge dall'authority
3. proiezione emessa come artefatto          N/A — la proiezione è una FUNZIONE PURA
                                                (resolveStatusTone), non dato
                                                materializzato
4. gate che rifiuta copie non derivate       ✅ 21 test
```

**Raffinamento di D-023 che ne emerge:**

> Il punto 3 (proiezione generata dal build) si applica solo quando la proiezione è
> **dato**. Quando è **funzione pura**, scriverla a mano è corretto.

È la differenza precisa fra Primitive Authority (funzione, a mano, corretto) e
ApplicationType (dato materializzato, a mano, **NX-11**). Stesso criterio, due esiti
diversi, e adesso si sa perché.

---

### D-033 — Degrada a runtime, rifiuta a build · `PROPOSTO`

`resolveStatusTone`: *"stati sconosciuti/vuoti degradano a muted, mai errori."*

È la **quarta istanza** del pattern D-017 (Degradation Budget):

```text
Redis            ping assente        → resta in locale           NX-20
LLM provider     modello ritirato    → 503 sulle route AI        NX-26
Foundation API   servizio giù        → artifacts già compilati   NX-01b
UI primitive     status sconosciuto  → tone muted                ADR-0012
```

Quattro dipendenze, stesso pattern, applicato coerentemente senza essere nominato.

**Ma la degradazione a runtime è corretta E incompleta.**

```text
X genera un bundle con status: 'pubblished'   (refuso, fuori vocabolario)
  → runtime: rende muted, nessun errore       ✅ resiliente
  → nessuno se ne accorge, MAI                ❌ il drift si accumula in silenzio
```

È lo stesso rischio di Q-006 (appId assente nella projection che scivola come
`undefined`): **il degrado silenzioso è peggio del crash**, perché il crash si vede
nei test.

**Risoluzione — stesso valore, due gate:**

```text
BUILD TIME   gate VALIDATE (NX-03)   → status fuori vocabolario = RIFIUTO
RUNTIME      resolveStatusTone       → status fuori vocabolario = muted
```

È esattamente la struttura di NX-34: **stesso ruleset, due punti di applicazione.**
Il vocabolario degli status deve essere dato dichiarativo consumato sia dal gate di
compilazione sia dalla funzione di proiezione.

Corollario: se il vocabolario sta in `status-tones.ts` ed è React-free (verificato
dal test), allora è già consumabile fuori dal renderer. Manca solo che il gate lo
legga.

---

### Q-011 — L'enforcement di ADR-0012 è enumerato o derivato? · `RISOLTO` (parziale)

I nomi dei test suggeriscono enumerazione esplicita:

```text
"src/core/ui-primitives/primitives.tsx has no raw palette / hex"
"src/core/ui-primitives/StatusBadge.tsx has no raw palette / hex"
"src/core/ui-primitives/index.ts has no raw palette / hex"
+ 9 superfici nominate individualmente per il divieto di import Radix
```

**Due possibilità, con conseguenze opposte:**

```text
A. il test scopre i file via glob/readdir e genera le asserzioni
   → enforcement DERIVATO: un file nuovo è coperto automaticamente
   → va benissimo così

B. i 12 path sono scritti a mano nel test
   → enforcement ENUMERATO: fallisce APERTO
   → una primitiva nuova o una dashboard nuova non sono controllate
   → e il ruleset non è riutilizzabile dal gate VALIDATE (NX-03/NX-34)
```

Da verificare con un comando, **senza concludere prima**:

```bash
grep -n "glob\|readdirSync\|fast-glob\|describe.each\|it.each\|readdir" \
  src/test/unit/primitive-authority.test.tsx
```

Se compare glob/readdir/each → caso A, chiuso.
Se non compare niente → caso B, e il ruleset va estratto a dato.

**ESITO 2026-09-12.** Il grep ha mostrato `it.each(AUTHORITY_FILES)` e
`it.each(PRESIDIATED)`, e il sorgente di `scripts/design/check-style-authority.mjs`
ha chiuso la domanda:

```ts
function* walk(dir) { /* readdirSync ricorsivo su tutto src/ */ }
export function exceptionFor(relPath) { /* le eccezioni SOTTRAGGONO */ }
```

**Scope DERIVATO dal filesystem, eccezioni che sottraggono → fails CLOSED.**
Un file nuovo in `src/` è controllato automaticamente.

**Correzione alla proposta dell'assistente:** era stata suggerita una `scope` come
elenco di glob da coprire, che **fallisce aperto**. La polarità era sbagliata.
L'implementazione reale è superiore.

**Residuo CONGELATO** (su richiesta dell'utente, da riprendere solo su trigger):
le asserzioni `AUTHORITY_FILES` nel vitest ora sovrappongono ciò che lo script fa
meglio. `classifySource` è esportata e commentata *"Pure; used by tests"* — se il
test la importa la sovrapposizione è già risolta, se legge i file per conto proprio
ci sono due fonti di verità per la stessa regola.

**Trigger per il promemoria:** aggiunta di una primitiva nuova, oppure chiusura di
0.7.0.2. Non prima.

---

### D-034 — CORREZIONE a D-033/NX-34: X genera dati, non codice · `DECISO`

D-033 e NX-34 dicevano: *"stesso ruleset, due punti di applicazione — lint/CI per gli
umani, gate VALIDATE per X"*. **Era sbagliato.**

`check-style-authority.mjs` scansiona `.tsx .ts .astro .css` e cerca classi Tailwind
e valori cromatici **nel sorgente**. X non genera sorgente: genera **PageData** che
referenzia primitive per nome.

```text
umano scrive TSX     → PALETTE check     (check-style-authority.mjs) ✅ già esiste
X genera PageData    → VOCABULARY check  (referenzia solo primitive e
                                          status noti?)  ← check DIVERSO
```

Se Primitive Authority è fatta bene, una PageData generata **non può contenere**
`bg-blue-500`: può solo dire `StatusBadge status="stable"`.

**Il gate di build per X verifica:**

```text
· ogni componente referenziato esiste nell'inventario delle primitive
· ogni valore di status esiste nel vocabolario di status-tones.ts
· nessun campo libero che ammetta valori visuali grezzi
```

**Domanda che decide la forma del gate (da verificare, non assumere):**

> PageData ammette escape hatch visuali — `className`, `style`, HTML libero,
> campi `raw`?

```text
SE NO   → il palette check non serve al gate. NX-34 si riduce a vocabulary check,
          già quasi coperto da Primitive Authority.
SE SÌ   → quei campi vanno rimossi, o sottoposti allo stesso ruleset rendendo
          classifySource consumabile sul loro contenuto.
```

Il principio di D-033 (**degrada a runtime, rifiuta a build**) resta valido; cambia
solo l'oggetto del rifiuto: vocabolario, non palette.

---

### D-035 — Un contratto è enforced solo se il punto di SCRITTURA lo verifica · `DECISO`

Dalla griglia di salute (`16-FOUNDATION-HEALTH.md` § 4):

```text
enforcement del DESIGN      avanti  — check-style-authority.mjs, regole come dato,
                                      scope derivato, eccezioni motivate, --ci
enforcement dei CONTRATTI   indietro — `as any` su DiscoveryMetadata in simple.ts,
                                      notFound:'/' accettato da un tipo string
```

> Verificare il punto di **lettura** (renderer, runtime) protegge l'utente.
> Verificare il punto di **scrittura** protegge il contratto.
> Il design ha entrambi. I contratti di Definition non ne hanno nessuno:
> `as any` disattiva TypeScript esattamente dove il contratto viene popolato.

Corollario: le sei authority con ✅ vanno riverificate su questo asse. Una directory
formalizzata con contratti popolati tramite escape hatch è formalizzata a metà.

---

### D-036 — Quinta stratificazione: sopravvissuta per progettazione · `DECISO`

```text
invasività alta + regressioni zero = i boundary tengono sotto stress   ← CASO ATTUALE
invasività alta + regressioni alte = coupling nascosto
invasività bassa + regressioni zero = non stai cambiando niente
```

L'utente definisce l'authority refactor *"uno dei più sanguinosi"*, e il sistema
viaggia senza errori dalla 0.4.x.

Differenza rispetto alle quattro stratificazioni precedenti: questa volta authority
formalizzate e test di parità esistevano **prima** di spostare il codice, non dopo.
Le prime quattro sono sopravvissute per robustezza del pattern; questa è
sopravvissuta **per progettazione**.

Rilevanza per Q-001 (IP): è la risposta empirica. Un sistema che assorbe il refactor
più invasivo della sua storia senza regressioni non è clonabile in dieci giorni,
perché la proprietà non sta nei file — sta nell'ordine in cui sono stati scritti.


---

### D-037 — Governance come sistema immunitario, e le sue due malattie · `DECISO`

**Origine:** feedback esterno sul documento 16 — *"queste non sono feature, sono
anticorpi."* Metafora accolta ed estesa.

Exception registry, scadenze, `reason` obbligatorie, tracciabilità: sistema
immunitario, non funzionalità. Un sistema immunitario fallisce in due modi, ed
**entrambi sono già osservabili nel repo**:

**a) Autoimmunità — l'anticorpo attacca il tessuto nuovo**

```text
artifact-consumption-closure.test.ts garantisce parità fra projection manuale
e output di BundleCollector.
→ oggi protegge dal drift
→ a 0.7.0, un bundle autorato aggiunge un appId, la projection manuale non lo
  contiene, il test FALLISCE e blocca l'authoring        (= NX-11)
```

> **Regola:** ogni garanzia di parità su un artefatto *scritto a mano* scade quando
> l'artefatto smette di essere scritto a mano. Va marcata come temporanea nel
> momento in cui si scrive, non scoperta dopo.

**b) Siti privilegiati — dove il sistema non pattuglia**

```text
legacy-frozen:pages  scope 'src/pages/build/'  expires: frozen
inScope usa startsWith → il punto d'ingresso di EXECUTION è esente,
e qualunque file aggiunto lì sotto lo è automaticamente     (= NX-47)
```

> **Regola:** un'eccezione senza scadenza machine-enforced non è un'eccezione, è una
> zona franca con una data di nascita e nessuna di morte. (= NX-46)

**Perché nominarlo ora:** i sistemi di governance non falliscono per assenza,
falliscono per eccesso di fiducia in se stessi.

---

### D-038 — NX-38 non è cleanup, è cambiamento di statuto · `DECISO`

Dal feedback esterno: *"Un'app tollera `as any`. Una Foundation no, perché una
Foundation vive di contratti."*

Riclassificazione accettata. `as any` su `DiscoveryMetadata` non è sciatteria: è
**residuo di pensiero-da-app sopravvissuto al cambio di natura del sistema**.

Conseguenza: la correzione non è "mettere i tipi giusti" ma decidere che **il punto
di scrittura di un contratto è un confine di piattaforma**. NX-38/39 promossi a
**P0** (il documento 16 li aveva a P1).

---

### D-039 — Open Nexus è più sano di Nexus Lab · `DECISO`

Due griglie, due numeri:

```text
Open Nexus (artefatto)   B+ / A−     16-FOUNDATION-HEALTH.md
Nexus Lab (ente)        C+ / B−     17-NEXUS-LAB-HEALTH.md
```

```text
Capacità di produrre             A
Capacità di misurarsi            A−
Capacità di SCEGLIERE DOVE       D      ← NX-30 aperto, zero conversazioni
Capacità di distribuire          D+     ← NX-01/01b/14 aperti, config su model ID ritirato
Capacità di sostenere            B
Capacità di apprendere esterno   B+     ← tutta ricerca a tavolino
Capacità di riprodursi           n/a    ← correttamente sequenziata
```

> **L'artefatto è più sano dell'ente che lo produce.**

Condizione normale per un fondatore tecnico singolo, ed è la condizione che uccide i
progetti — non il codice.

**Divergenza di backlog registrata:** il feedback esterno propone sei voci, **tutte
interne**. NX-30, NX-45 e NX-14 assenti. Non è un errore del feedback: un PM ottimizza
per l'eseguibile, e l'eseguibile è sempre interno. È la prova che la trappola è
**strutturale**, non disciplinare — non si evita essendo più attenti, si evita avendo
una voce di backlog che non può essere eseguita da soli.

**Contrappeso a verbale:** *coerenza interna non è valore.* La sessione ha prodotto
sedici documenti e zero conversazioni con un potenziale utente. Il rapporto va
invertito, non bilanciato.

**Le tre domande:**

```text
1. Qual è la tesi?                                 → c'è
2. Sopravvive a un refactor violento?              → sì, cinque volte
3. A chi serve, e chi paga?                        → NON ANCORA
```

---

### D-040 — Metodo Sonda: gate di promozione delle capacità nel core · `DECISO`

**Origine:** documenti prodotti dall'utente in altra sessione (2026-09-13),
"Job Seeker & Candidate Apply" e "Prima formulazione — applicazione sonda".

Il merito dell'applicazione specifica NON è valutato qui. Viene registrato il metodo,
che è indipendente dall'applicazione.

#### 40.1 La separazione fondamentale

```text
PERCORSO PIATTAFORMA     non deve dipendere da una singola applicazione
  contratti · PageData · ApplicationBundle · validazione · runtime · renderer
  workflow · MCP · CLI · cataloghi · pubblicazione

APPLICAZIONE SONDA       può cambiare senza contaminare il nucleo
  modello dei contenuti · onboarding · template · tono e pubblico · layout
  pricing · integrazioni · metriche
```

> **"L'app può dimostrare il framework; non può ridefinirlo senza una seconda
> applicazione che confermi la necessità."**

È il boundary Foundation/X applicato alle **decisioni di prodotto**, non al codice.
Estensione reale: finora il boundary governava dove sta la logica, adesso governa
cosa ha il diritto di cambiare il contratto.

#### 40.2 I sei gate di promozione

Una capacità entra nella piattaforma se:

```text
1. serve ad almeno due applicazioni diverse            (regola del due)
2. resta valida anche se il primo mercato fallisce     (disaccoppia rischio
                                                        architetturale da rischio mercato)
3. è un'invariante o capacità generale, non una comodità locale
4. riduce un costo reale per l'utente
5. è osservabile e verificabile
6. può eventualmente essere esposta via MCP
```

Se serve solo alla sonda → resta nell'adattatore dell'app.

#### 40.3 Sequenza

```text
1. analizzare l'esistente
2. individuare i GAP RICORRENTI, non le feature mancanti
3. scegliere una sonda piccola e dimostrabile
4. testare il modello  contenuto → viste → pubblicazione
5. misurare uso, ritorno, frizione, disponibilità a pagare
6. promuovere nel core SOLO ciò che è confermato da più casi d'uso
```

#### 40.4 Le due frasi che contano di più

> **"La domanda non è se questo modello sia elegante dal punto di vista
> architetturale. La domanda è se consenta all'utente di evitare una frizione reale."**

È la guardia esplicita contro D-039 (*coerenza interna non è valore*). L'utente ha
scritto nel metodo la protezione contro il proprio modo di fallire. È la cosa più
matura dei due documenti.

> **"Il pagamento deve essere collegato a un risultato concreto, non a un generico
> insieme di funzioni AI."**

È la regola che separa un prodotto da una demo, ed è la stessa che ToolJet applica
con i crediti e AlphaSense con il contenuto proprietario.

#### 40.5 Simmetria con il programma Authority

```text
AUTHORITY   governa la proprietà del CODICE       "chi possiede cosa?"
SONDA       governa la promozione delle CAPACITÀ  "cosa merita di essere
                                                   posseduto dal core?"
```

Due programmi di governance allo stesso livello, su oggetti diversi. Il secondo è
l'equivalente per il prodotto del primo per l'architettura — e ha la stessa forma:
regole dichiarate, gate verificabili, eccezioni motivate.

#### 40.6 "Cosa non stiamo dicendo"

Il documento include una sezione di anti-overclaim esplicita:

```text
non stiamo dicendo che il mercato sia quello delle personal page
non stiamo dicendo che serva un altro website builder
non stiamo dicendo che la galleria civica sia il verticale
non stiamo dicendo che una singola applicazione debba dettare l'architettura
non stiamo dicendo che la concretezza tecnica dimostri disponibilità a pagare
```

È NX-08 (doc che difende le decisioni) applicato alla **strategia** invece che al
codice. Stessa postura di Trustable (*"Note what it does NOT do"*) e del recap
ufficiale (*"Non dimostra sincronizzazione cross-tab real-time"*).

---

### D-041 — NX-49 riformulato: sonda, non verticale · `DECISO`

`18-WHY-NEXUS-LAB-EXISTS.md` § 3 proponeva la prima knowledge experience reale sul
dominio civico ("malefatte della mia città").

**Riformulazione:** quella proposta è **una delle candidate**, non la scelta. Il
metodo Sonda (D-040) stabilisce che nessuna singola applicazione definisce il
verticale, e che la galleria civica — come il job seeker — è una sonda.

```text
NX-49   prima applicazione sonda                 (in esplorazione in altra sessione)
        candidate seconde sonde: portfolio · blog · gallery · esperienza civica
NX-30   il verticale si DEDUCE dalle sonde, non si sceglie a priori
        → NX-30 resta aperto finché non c'è una seconda sonda che conferma
```

Conseguenza: **NX-30 non è bloccante per NX-49.** Si può costruire una sonda senza
aver deciso il verticale — è esattamente il punto del metodo.

---

### Quattro lacune del METODO (non dell'idea)

Da colmare perché il metodo non degeneri. Nessuna riguarda il job seeker.

**L-1 · Manca il criterio di arresto.**
La sequenza § 40.3 ha sei passi e nessuna condizione di falsificazione. Senza
*"quale osservazione ci fermerebbe?"*, una sonda diventa un progetto. Confronto: i
guard rail di NX-31 includevano *"se dopo N piattaforme la risposta non emerge,
l'ipotesi è falsificata"*. Qui manca l'equivalente.

**L-2 · La regola del due richiede una seconda sonda nominata.**
Il gate 1 ("serve ad almeno due applicazioni") non è valutabile se la seconda
applicazione non esiste nemmeno come ipotesi. Le candidate sono elencate
(portfolio, blog, gallery) ma non impegnate. Senza una seconda sonda **nominata**,
nulla può mai essere promosso nel core — e la sonda resta sonda per sempre.

**L-3 · Manca il time box.**
Sei passi senza date. Dato il pattern registrato in D-039 (diciassette documenti,
zero conversazioni), una sonda senza scadenza deriva verso il lavoro di
architettura, che è ciò che l'utente sa fare meglio. È il rischio specifico a cui è
più esposto, e il metodo non lo presidia.

**L-4 · Manca il pubblico nominato.**
`18-...` § 6: *lavoro gratis senza pubblico nominato = inventario, non portfolio*.
La sonda ha utenti descritti per categoria ("persona in cerca di lavoro",
"studente") ma non un pubblico con un nome e un canale. Il passo 3 della sequenza
("parlare con persone") è il punto giusto dove fissarlo.

**Le quattro lacune hanno la stessa forma:** il metodo sa cosa osservare ma non sa
quando fermarsi. È la differenza fra una sonda e un'esplorazione indefinita.


---

### D-042 — Inventario di capacità: 4 verificate, 4 parziali, 4 teoriche, 0 esercitate da esterni · `DECISO`

`21-CAPACITA-OPENNEXUS.md`. Ogni capacità è marcata con l'evidenza che la sostiene.

```text
VERIFICATE   C-01 conoscenza navigabile · C-02 multi-app da un runtime
             C-03 governance visiva · C-04 proiezione semantica
PARZIALI     C-05 produzione artefatti · C-06 sessione e policy
             C-07 riduzione deterministica · C-08 governance delle decisioni
TEORICHE     C-09 authoring agentico · C-10 workflow eseguibile
             C-11 distribuzione firmata · C-12 local-first
```

**Dato che conta:** `esercitata da qualcuno fuori = 0` su tutte e otto le capacità
verificate o parziali. È D-039 espresso come inventario.

**C-09 è la capacità su cui si regge l'intera visione ed è la meno verificata.**
Non esiste un bundle prodotto da qualcosa che non sia l'utente. E dipende da NX-11:
senza materializzazione generata, il test di parità blocca il primo bundle nuovo.

---

### D-043 — Il pilota si assembla, non si inventa · `DECISO`

L'applicazione pilota va composta da capacità **già verificate**, senza attraversarne
di teoriche:

```text
C-01  renderer LIVE su openfav.vercel.app        → nessuna UI da costruire
C-07  scraping + estrazione, la CLI esiste
C-08  il metodo di questa sessione
C-04  classificazione per meccanismo / tipo di moat
C-03  matrici e confronti senza deriva visiva
     = capacità di analisi di mercato (doc 20), prototipo già scritto (4 dossier)
```

Perché questa combinazione:

```text
1. non richiede C-09 (authoring agentico)     → teorica
2. non richiede C-11 (distribuzione)          → teorica
3. non richiede NX-30 deciso                  → produce il dataset che lo decide
4. usa renderer già live
5. ha un payer con spesa già in corso
6. il prototipo esiste: va portato in PageData, non prodotto
```

**È l'unica combinazione che trasforma capacità verificate in output per qualcuno
fuori senza attraversare una capacità teorica.**

Gate di qualifica: **NX-57** — un'analisi su oggetto nuovo usando solo il metodo
scritto, senza intervento dell'operatore. Se regge è un prodotto, se non regge è una
performance.

---

### D-044 — Ambizione vs presunzione · `DECISO`

Domanda dell'utente: *"non pecco di presunzione a pensarla più ad alto livello?"*

```text
PRESUNZIONE   credere che il sistema sia più capace di quanto l'evidenza mostri
AMBIZIONE     sapere cosa può fare, e puntare più in alto
```

La differenza è l'inventario. Finché le capacità sono dichiarate con la loro evidenza,
pensare in grande è leggere la tabella e chiedersi cosa manca.

La presunzione nella sessione c'è stata ed è stata nominata quando è accaduta:
*"nessuno è come Open Nexus"* (6/10) e le quattro ipotesi di drift affermate prima
dell'evidenza. In entrambi i casi il problema non era il livello di ambizione: era
l'assenza di un comando a supporto.

**Sui due livelli in parallelo** (pilota piccolo + grandi sistemi):

> Il livello alto deve produrre **VINCOLI** che il pilota deve soddisfare, non solo
> contesto in cui il pilota galleggia.

Qui è accaduto: C-09/C-10/C-11 teoriche **vincolano** il pilota a non dipendere da
loro (D-043 punti 1 e 2). Quando il livello alto non produce vincoli, è fuga.

---

### D-045 — La tabella di backlog è un'istanza manuale di NX-02 · `DECISO`

Lo schema del backlog (ID · Tipo · Area · Pri · Stato · Blocco · Prossimo · Fonte)
è un workflow: ha passi, stati, dipendenze e gate. È la stessa ricorsione di
`03-WORKFLOW.md` § 6, scesa di un livello — dal processo alla tabella che lo traccia.

Conseguenza: quando NX-02 verrà scritto, lo schema del backlog è il primo candidato
di formato. Non va inventato.

**Deriva misurata a 59 voci** (da correggere):

```text
53 "aperto" (90%)          → lista di desideri, non backlog
12 P0                      → inflazione: il massimo sostenibile è 3
33 valori di Layer         → testo libero, non tassonomia
modificatori ad hoc        → "P0 STRATEGICO", "P0 URGENTE", "P2 con prerequisito"
                             = tre informazioni (importanza, urgenza, dipendenza)
                             schiacciate in un campo
ordinamento rotto          → NX-50 prima di NX-49
NX-58 malformata           → 8 colonne invece di 6: i pipe escapati dentro
                             una cella splittano comunque la tabella markdown
voci superate mai rimosse  → NX-04, NX-18, NX-44, NX-31
```

Sintomo riassuntivo: **NX-50 — l'unica cosa urgente della settimana — sta alla riga
50 di 59.**

Correzione proposta: stessi ID (referenziati in 21 documenti), colonne
`Tipo` (AZIONE/DECISIONE/VERIFICA/REGOLA) e `Area` (6 valori: FOUNDATION/X/BRAIN/
PRODOTTO/DISTRIB/METODO), `Blocco` e `Prossimo` come campi propri, massimo 3 P0,
voci chiuse in sezione storica.


---

### D-046 — La persona torna a essere "ME" perché il prodotto è descritto come meccanismo · `DECISO`

**Dato scatenante:** un parente **sviluppatore** ha chiesto *"ma che fa questo sw?"*
e non ha ricevuto una risposta che gli restasse.

Non è un problema di semplificazione per non tecnici: se uno sviluppatore non capisce,
**non esiste la frase**.

```text
tutte le formulazioni usate finora descrivono il MECCANISMO
  "Foundation produce, Execution esegue"
  "PageData is the language of knowledge experiences"
  "indeterminismo che diventa determinismo"
nessuna risponde a "cosa fa per qualcuno?"
```

I benchmark rispondono tutti con **VERBO + OGGETTO + BENEFICIARIO**, e nessuno
menziona l'architettura in home page.

**I due problemi aperti sono uno solo:**

```text
"la persona non deve essere ME"     → non so chi è Y
"spiegalo a tua nonna"              → non ho la frase

SENZA una frase di risultato, l'unica persona che riesci a immaginare
mentre usa il prodotto sei tu.
```

---

### D-047 — Y è chi deve rendere conto · `DECISO`

**Y proposta dall'utente:** *"utente di dominio, sa fare un prompt, ha gli strumenti
base di lavoro."*

**Non tiene, per due ragioni:**

```text
1. è definita da cosa SA FARE (tre competenze), non da cosa DEVE FARE.
   È un segmento demografico, non una persona con un problema.
   Non è falsificabile e non è trovabile.

2. "sa fare un prompt" è esattamente la persona che può ottenere l'80%
   del risultato da un LLM generalista → NX-64, filtro di sostituibilità.
   È il cliente MENO probabile, non il più probabile.
   Evidenza dalla scansione: AI homework engine, 1M views, 96% margine,
   multiplo 0,94×.
```

**Y corretta, derivata dai listini raccolti:**

```text
Y = LA PERSONA CHE DEVE RENDERE CONTO

  compliance officer che deve produrre una traccia verificabile
  analista che deve difendere una conclusione davanti a un comitato
  giornalista che deve citare la fonte
  chi fa due diligence e non può permettersi di sbagliare
  funzionario pubblico che deve rispondere a un consiglio o a un controllo
```

> **La responsabilità è ciò che rende l'evidenza non opzionale.**
> Un LLM generalista dà una risposta senza responsabilità: niente fonte,
> niente versione, niente traccia, non risponde a nessuno.

Chiude il cerchio con tre cose già stabilite: M-04 (il differenziatore è la traccia,
non l'analisi), M-06 (il verticale normativo), NX-69 (audit trail come tier di prezzo).

**E dà a NX-30 un criterio invece di una domanda:**

> il verticale giusto è dove rendere conto è un **obbligo**, non una scelta.
> PA · giustizia · sanità · finanza regolamentata · appalti · sicurezza.

---

### D-048 — L'AI entra in scena una volta sola · `DECISO`

Dall'utente: *"questa AI quando entra in scena? meno lo fa, più la base è solida e
può superare tempeste."*

Confermato, e reso operativo:

```text
TOGLI L'AI. Il prodotto produce ancora qualcosa di utile?
  SÌ  → l'AI è al posto giusto: interpreta ciò che la base ha già raccolto
  NO  → l'AI È la base, e la base è fragile
```

Per Open Nexus senza AI restano: corpus versionato, fonti tracciate, classificazione,
confronto, change detection, esperienza navigabile. **È già un prodotto.**

```text
l'AI sbagliata        → il corpus resta giusto
l'AI indisponibile    → il corpus resta servibile
l'AI cara             → il corpus resta gratuito
l'AI ritirata         → è successo il 10 settembre, il corpus non se n'è accorto
```

**Regola:**

> L'AI entra in scena UNA volta sola: nell'interpretazione.
> Tutto ciò che sta prima (raccolta, riduzione, classificazione, rilevamento)
> e tutto ciò che sta dopo (rendering, navigazione, pubblicazione) è deterministico.
> Se l'AI entra in un altro punto, va motivato per iscritto.

È D-017 (degradation budget) applicato all'AI stessa.

---

### D-049 — Barca ottima ferma in rada, non naufragio · `DECISO`

Immagine dell'utente: *"naufrago nel mare delle startup perse nei flussi della loro
inconcludenza."*

```text
strumentazione   ECCELLENTE   25 documenti · 73 voci · 67 decisioni
                              metodo di falsificazione funzionante
                              inventario di capacità con evidenza
                              scansione di mercato con numeri reali
destinazione     ASSENTE      NX-30 aperto · Y non definita fino a oggi ·
                              nessuna frase di risultato
```

**Diagnosi:** non è un naufragio, è una barca ottima ferma in rada. Condizione
diversa, che si risolve in modo diverso — **non costruendo più strumentazione.**

Rischio specifico, già manifestatosi due volte nella sessione: costruire
strumentazione è piacevole, produce evidenze e dà la sensazione di avanzare.
La destinazione produce solo domande senza risposta finché qualcuno non risponde.

---

### D-050 — "Mostra, non chiedere" · `DECISO`

**Origine:** Y-1 descrive il vibe coding come *"tedioso rispondere a tutte le
richieste tecniche... prompt che macinano sulle intenzioni dell'utente."*

La frizione non è generica. Ha una causa precisa:

```text
l'agente general purpose NON HA DEFAULT
  → deve chiedere
  → chiede PRIMA che l'utente abbia il contesto per decidere
  → ogni risposta è un impegno preso al buio
  → l'utente scopre cosa voleva solo DOPO aver visto qualcosa
```

**Principio di prodotto:**

> **Mostra, non chiedere.**
> Applica il contratto, produci il risultato, lascia che l'utente corregga guardando.
> Ogni domanda posta all'utente è un default mancante in un'authority.

Corollario operativo, ed è misurabile:

```text
ogni domanda che nexus-builder pone a Y-1
  = un buco in una authority
  = una riga nella lista di NX-79
```

Questo trasforma il colloquio con Y-1 da ricerca di mercato in **audit di
completezza di Foundation**. Stesso colloquio, due output.

Coerenza con decisioni esistenti:

```text
D-005   page semantics select the renderer → la semantica decide, non l'utente
D-032   Primitive Authority → l'inventario dei componenti è chiuso
ADR-0012 resolveStatusTone → stato sconosciuto degrada a muted, NON chiede
Trustable § 3.4  "Cancel returns to the carousel rather than closing the dialog,
                 because you are choosing, not aborting" → stessa filosofia
```

`resolveStatusTone` che degrada invece di chiedere è già "mostra, non chiedere"
implementato a livello di primitiva. Va elevato a principio di prodotto.

---

### D-051 — La convergenza dei tentativi su Y · `DECISO`

Tre tentativi, in ordine:

```text
1. broker / CFO / manager che esplora il mercato
   fonte: il mercato che HO TROVATO IO (AlphaSense/Hebbia/Rogo)
   qualità: PRESTATA — era la risposta di un altro mercato

2. "chi deve rendere conto"
   fonte: i listini raccolti nella scansione (GoMarble audit trail, Particl)
   qualità: DERIVATA — corretta ma astratta, non ha un volto

3. Y-1, volontario, con frizione specifica sul vibe coding
   fonte: UNA PERSONA REALE
   qualità: CONCRETA e falsificabile
```

**La qualità della fonte migliora a ogni tentativo.** Non è oscillazione: è
convergenza. L'ordine è quello giusto — mercato → criterio → persona — ed è
l'unico ordine che produce una Y utilizzabile.

I tentativi 1 e 2 non erano errori da cancellare: erano i passaggi necessari per
arrivare a formulare la domanda in modo che una persona reale potesse rispondere.

**Regola registrata:** i tentativi su Y vanno accettati e registrati tutti, perché
la sequenza delle fonti è essa stessa informazione. Scartare un tentativo senza
registrarlo perde il dato su *come* si stava cercando.

---

### D-052 — Sei nomi, e nessuno decide · `PROPOSTO` · **NX-81**

```text
OpenFav          l'app deployata (openfav.vercel.app)
Open Nexus        l'architettura / il framework
Nexus Lab        l'ente
nexus-builder    il prodotto per Y-1        ← nuovo, comparso oggi
nexus-mcp        il server MCP (NX-14)
opnx             il comando CLI
```

Un utente che vede pubblicità di `nexus-builder` e atterra su `openfav.vercel.app`
è perso. NX-10 (decidere il nome pubblico) era P2: **diventa P1**, perché ora c'è
un nome di prodotto in circolo.

Gerarchia proposta:

```text
NEXUS LAB        l'ente, la firma
  ├── Open Nexus  il framework / la piattaforma      (Foundation + X)
  │     ├── opnx / nexus CLI
  │     └── nexus-mcp
  ├── nexus-builder   il prodotto per chi non vuole decidere   ← istanza
  └── (altre istanze future)

OpenFav          da ritirare o da tenere come ambiente di demo
```

Da verificare: collisioni su "nexus-builder" (NX-10 non è mai stato eseguito).


---

### D-053 — Y-2 / Prometeo / RENTRI è la candidata più forte della sessione · `DECISO`

**Fonte:** `28-PROMETEO-RENTRI.md`. Documento prodotto in altra sessione, persona A.
(avvocato) con segnale **inbound**: *"guarda questi siamo noi, vedi se riscontri
bisogni."*

D-047 aveva stabilito il criterio: *il verticale giusto è dove rendere conto è un
obbligo, non una scelta*. La tracciabilità rifiuti è quel criterio realizzato:

```text
registro elettronico nazionale     → l'obbligo di rendere conto È il prodotto
catena di responsabilità multipla  → produttori, consulenti, trasportatori,
                                     impianti, autorità
sanzioni amministrative e penali   → l'evidenza non è un lusso
fonti normative che cambiano       → serve versioning e grafo di dipendenza
avvocato coinvolto                 → il dominio è giuridico, non tecnico
```

**Matrice:**

```text
                    K1   K2   K3   K4    K5   K6   K7   K8
Y-1 volontario       ~   ✗✗   ✗    ✗✗    ✗    ✗✗   ✗    ✓✓
E  analisi evidenza  ✓   ✓    ✓✓   ✓     ✓    ✓✓   ✓✓   ~
D  dev validation    ✓   ~    ✓✓   ✗     ~    ✓✓   ~    ✓✓
Y-2 Prometeo         ✓✓  ✓✓   ✓✓   ✓?    ✓✓   ~    ✗    ✓
```

**La differenza decisiva è K6:**

```text
Y-1 richiede C-09 (authoring agentico) + C-11 (distribuzione firmata)
    = le DUE capacità meno verificate dell'inventario
Y-2 richiede C-01 + C-04 + C-07 + C-08
    = tutte verificate o parziali, NESSUNA teorica
```

**Primo segnale inbound della sessione.** K8 passa da pianificato a accaduto.

**K4 è l'unica cella non verificata ed è quella che può ribaltare tutto:** il
pavimento open source è quasi certamente assente, ma il pavimento COMMERCIALE
(gestionali rifiuti) è quasi certamente presente e affollato. La domanda non è
"esiste un open source" ma *"cosa fanno i gestionali esistenti, e cosa NON fanno"*.
→ NX-84, prima di qualunque conversazione di prodotto.

---

### D-054 — Il documento Prometeo outruns se stesso · `DECISO`

Contraddizione interna di struttura:

```text
§ 1, § 6, § 11   ecosistema · network · spin-off        ← ambizione
§ 9, § 10        pilot su una materia delimitata,
                 "non partire dal network completo"       ← disciplina
```

§ 9 e § 10 sono giusti. § 1/6/11 sono la stessa malattia di sempre in abiti nuovi:
l'architettura che cresce prima dell'evidenza.

**Decisione: si adotta § 9 come piano. § 1/6/11 si archiviano come scenario
condizionato al successo di § 9.**

Percorso reale:

```text
1 pilot su una materia → 2 secondo caso d'uso (regola del due, D-040)
→ 3 solo allora ecosistema → 4 solo allora spin-off
```

Nota: "spin-off" implica un soggetto giuridico. Per un dipendente pubblico non è una
parola neutra — vedi D-055.

**Convergenze indipendenti da registrare come conferma:**

```text
§ 4  dato ≠ interpretazione ≠ decisione     = D-048 + observed/inferred/recommended
§ 2  "risorsa Brain non è necessariamente   = reduction pipeline + classe 0
     un modello AI"
§ 3  workflow con "quando si arresta"       = L-1, la lacuna del metodo Sonda, chiusa
§ 5  "il network dopo un workflow verticale = regola del due
     funzionante, non prima"
```

Quattro convergenze indipendenti su quattro punti. È il segnale più forte che il
metodo sia corretto — arriva da un'altra sessione, su un altro dominio, senza aver
letto questi documenti.

---

### D-055 — NX-50 diventa prerequisito non negoziabile · `DECISO`

Con un verticale di **compliance in dominio regolamentato**, la collocazione dei
documenti strategici sul tenant del datore di lavoro cessa di essere una questione
di ordine.

```text
1. INCOMPATIBILITÀ / AUTORIZZAZIONI
   attività extra-istituzionali dei dipendenti pubblici: obblighi di comunicazione
   e autorizzazione. "Spin-off" implica un soggetto giuridico.
   → VA VERIFICATO CON UN LEGALE, non con un assistente.

2. PROPRIETÀ DEL MATERIALE
   strategia di un prodotto commerciale su account istituzionale = ambiguità da
   risolvere PRIMA che il progetto abbia valore, non dopo.

3. CONFLITTO PERCEPITO
   un prodotto di compliance venduto a soggetti regolamentati, da un dipendente
   pubblico, genera una domanda scomoda. Meglio averci pensato prima.
```

**Sequenza vincolante:**

```text
NX-86 (bonifica + verifica legale)  →  NX-84 (K4)  →  NX-85 (colloquio con A.)
```

NX-85 è bloccato da NX-86 e NX-84. Non si presenta un progetto commerciale con i
documenti del progetto sul cloud del Ministero.

---

### D-056 — A. sta in orbita, non in pipeline · `DECISO`

**Correzione a D-053/NX-85.** La formulazione dell'utente è precisa e va rispettata:

> *"persona interessante da tenere nell'orbita del Lab"*

**Orbita ≠ pipeline.** Sono due modi di relazione con conseguenze opposte:

```text
PIPELINE   la persona è una fonte di validazione
           si estrae: bisogni, payer, budget
           si chiede
           rischio: la relazione diventa un'intervista e A. si sente minato

ORBITA     la persona è una relazione da mantenere
           si porta: qualcosa di utile
           si mostra
           il bisogno emerge dal contatto ripetuto, non dall'intervista
```

**L'assistente aveva impostato NX-85 in modalità pipeline** (13 domande, obiettivo
payer). È prematuro, e per tre ragioni:

```text
1. A. ha iniziato con generosità ("guarda questi siamo noi").
   Ricambiare con un'interrogatorio è stonato.
2. Il dominio è profondo: non si estrae in un'intervista.
3. In un dominio regolamentato l'asset reale è la FIDUCIA,
   e la fiducia viene dall'essere utili, non dal chiedere.
```

### D-057 — "Mostra, non chiedere" si applica anche alla relazione · `DECISO`

D-050 era un principio di prodotto. Vale anche qui, ed è la risoluzione:

```text
NON   presentare Open Nexus e fare tredici domande
MA    portare un piccolo artefatto utile, già fatto, senza pitch
```

L'artefatto candidato: **una knowledge experience su UNA materia delimitata del
dominio, con fonti, date e versioning.** Cioè il pilot di § 9 del documento Prometeo,
ma concepito come **dono** invece che come prodotto.

Effetti:

```text
· dimostra la capacità senza spiegarla
· risponde a "vedi se riscontri bisogni" mostrando invece di chiedendo
· ricambia la generosità di A.
· produce reazione osservabile, che è il dato che le 13 domande avrebbero prodotto
  — ma senza il costo relazionale
· ed è comunque NX-49: lo stesso lavoro, con un destinatario reale
```

### D-058 — Le condizioni di conversione dell'orbita · `DECISO`

L'orbita ha un rischio specifico, ed è la versione interpersonale della trappola di
comfort: **restare in orbita per sempre sembra progresso e non produce niente.**

Serve una condizione di conversione esplicita:

```text
l'orbita diventa conversazione quando A. fa UNA di queste cose:
  · chiede la stessa cosa due volte
  · ti presenta qualcuno con budget
  · dice "quanto costerebbe"
  · condivide documenti o dati interni senza che tu li chieda

fino ad allora:  portare, non chiedere
quando accade:   chiedere
```

Senza questa condizione, l'orbita è indistinguibile dal rimandare.

**Cadenza:** un'orbita senza periodo decade. Un contatto utile ogni 4-6 settimane,
ogni volta con qualcosa di concreto. Non "come va", ma "ho fatto questo, ti serve?".

### D-059 — Cosa resta valido di D-053 · `DECISO`

Il punteggio sulla matrice resta corretto: Y-2/Prometeo è la candidata più forte per
K1, K2, K3, K5. Quella parte non era prematura.

Era prematuro trattarla come **il verticale scelto**. La distinzione:

```text
"Y-2 ha il punteggio più alto"        → vero, verificabile sulla matrice
"Y-2 è il verticale di Nexus Lab"     → non stabilito, e non si stabilisce
                                        senza K4 (NX-84) e senza una conversazione
```

**NX-86 resta valido e indipendente da tutto questo**: la bonifica del tenant e la
verifica legale non dipendono da come si gestisce la relazione con A. Anzi: si fanno
proprio perché la relazione potrebbe diventare qualcosa.


---

### D-060 — K4 verificato: incumbent forte, non mercato vuoto · `DECISO`

`25-SCANSIONE-PROMETEO-RIFIUTI.md` ricevuta (NX-87 chiuso). Analisi in
`29-PROMETEO-ANALISI.md`.

```text
vendor        Informatica EDP
scala         2.000+ installazioni · 3.000+ aziende (dichiarazione del fornitore)
prezzo        da €125/utente/mese (catalogo Capterra, nessuna recensione
              → listino, non verifica commerciale)
copertura     registri · formulari/XFIR · MUD · RENTRI · autorizzazioni · scadenze
              giacenze · contratti · pianificazione · DDT · fatturazione
              MPS/EOW · dashboard · contabilità · multi-ruolo
```

```text
pavimento open source   ASSENTE            confermato
pavimento commerciale   PRESENTE E FORTE   incumbent verticale maturo
```

**Due opportunità della scansione sono già coperte dall'incumbent:**

```text
Opportunità A (controllo documentale, scadenze, incongruenze)
  → § 2.1 della scansione: "Prometeo comunica il valore attraverso ALERT SU
    AUTORIZZAZIONI SCADUTE, LIMITI DI GIACENZA E INCONGRUENZE"
Opportunità E (knowledge layer RENTRI, formazione)
  → § 5.E: "Prometeo già produce webinar e documentazione su RENTRI"
```

La scansione lo dichiara e non lo collega alle proprie opportunità. Non è errore di
raccolta: è un mancato collegamento.

---

### D-061 — Il soggetto non è deciso · `DECISO`

La scansione produce bisogni per **due soggetti diversi** (§ 12) senza scegliere, e
ammette in § 16 che *"il potenziale cliente potrebbe essere Informatica EDP, non
l'utente finale"*.

L'ambiguità sta in *"guarda questi siamo noi"*:

```text
A. lato vendor        → prodotto = layer editoriale/di conoscenza (§ 13-15)
                        payer = Informatica EDP · ciclo B2B lungo
                        bisogno FUORI dalla competenza core dell'incumbent

A. lato utente        → prodotto = Waste Evidence Assistant (§ 9)
  (consulente/assoc.)   payer = studio/associazione/azienda · ciclo più corto
                        bisogno DENTRO la competenza core dell'incumbent  ⚠

A. lato legale        → prodotto = layer forense versionato (§ 4.1)
  (contenzioso)         payer = studio legale / assicurazione
                        bisogno che NESSUNO dei due copre
```

**Tre prodotti incompatibili. Non si procede senza la risposta.** → NX-91, una riga.

---

### D-062 — L'apertura reale: ciò che un gestionale non può fare per costruzione · `PROPOSTO`

Un gestionale transazionale memorizza **lo stato corrente**. È il suo mestiere e lo
fa bene. Strutturalmente non fa:

```text
RICOSTRUZIONE PROBATORIA VERSIONATA
  "qual era lo stato AL MOMENTO DEL FATTO, secondo la norma ALLORA VIGENTE,
   e con quali prove documentali?"

  richiede: versione della norma applicabile in quella data
            stato del registro in quella data
            catena documentale non alterabile
            distinzione dato / inferenza / conclusione
```

È **forense**, non gestionale. E richiede esattamente ciò che Open Nexus ha e un
gestionale non ha motivo di avere:

```text
Source Authority    ogni affermazione risale a fonte, data, versione
versioning          la norma di allora, non quella di oggi
evidence citation   la traccia che un avvocato può firmare
```

La scansione ci arriva senza nominarla (§ 4.1):
`affermazione → evento/documento → fonte → data → versione → stato di validazione`.
**Quella catena è il prodotto.**

E A. è un avvocato: è l'unica persona del network per cui quella catena è il lavoro,
non un optional.

Seconda apertura: **layer cross-sistema.** L'azienda reale ha Prometeo E fogli E
email E contabilità. Un vendor unifica il proprio sistema; non ha interesse a
unificare ciò che sta fuori. Un overlay su export da qualunque fonte non è nel
mestiere dell'incumbent — ed è il Percorso 1 della scansione visto dal lato giusto.

**Matrice aggiornata:** la riga che tiene K1 ✓✓ e guadagna K4 ✓ è il layer forense.

---

### D-063 — A. è candidato co-founder, non contatto in orbita · `DECISO`

**Correzione a D-056.** L'utente dichiara: *"A. è la persona interessante che citavo
come papabile co-founder."*

```text
ORBITA (D-056)        relazione da mantenere, si porta valore, non si chiede
                      → corretta se A. è un contatto di dominio

CO-FOUNDER            società, quote, responsabilità condivise
                      → richiede verifiche legali, allineamento, e una decisione
```

Le due modalità sono incompatibili nello stesso periodo: trattare un candidato
co-founder come un contatto in orbita spreca l'occasione; trattare un contatto in
orbita come co-founder brucia la relazione.

**Va deciso quale delle due, e la decisione è bloccata da NX-86.** Non si costituisce
niente — nemmeno informalmente — con la posizione di dipendente pubblico non chiarita.

### D-064 — A. corrisponde esattamente al profilo NX-33 · `DECISO`

NX-33 (doc 13 § 2.2) diceva:

```text
X NON ha bisogno di un secondo architetto
X ha bisogno di qualcuno che sappia il VERTICALE
  profilo 1: dominio — qualcuno che ha venduto o comprato software in un
             verticale regolamentato (PA, pharma, energia, assicurazioni)
```

A. è **avvocato in un dominio regolamentato**, con accesso a un network settoriale.
È il profilo 1, non il profilo 2.

**Ma la sequenza si è invertita:**

```text
NX-33 prevedeva     prima la prova (NX-31/49) → poi il verticale → poi la persona
cosa è successo     la persona è arrivata prima della prova
```

Non è necessariamente un male — le persone arrivano quando arrivano. Ma cambia il
rischio: senza una prova, non c'è niente su cui verificare l'allineamento. Un
co-founder scelto prima del prodotto viene scelto per simpatia e competenza
percepita, non per come lavora sotto pressione.

Precedente registrato dall'utente: una collaborazione precedente "finita male".

### D-065 — "Comunicazione esterna debole" è un'osservazione, non un'evidenza · `PROPOSTO`

Tesi dell'utente: Prometeo pecca in comunicazione esterna, sito statico, non comunica
la sensazione di ecosistema che invece è il cuore della loro attività.

**La seconda parte è acuta e probabilmente vera:**

> il loro asset reale è la POSIZIONE DI NETWORK
> (produttore → trasportatore → impianto → consulente → associazione)
> e la comunicazione vende FUNZIONI invece che posizione

È un'osservazione strategica, non di web design, ed è il tipo di cosa che nota un
avvocato perché ragiona in relazioni e responsabilità.

**La prima parte non è verificata:**

```text
"il sito è statico (credo)"        → congettura, non osservazione
"sembrano deboli"                  → impressione
3.000+ aziende che li hanno scelti → le vendite funzionano
```

**La domanda che decide non è "il sito è dinamico?" ma:**

> questa debolezza gli COSTA qualcosa? Chi, dentro Prometeo, sente questo dolore
> e ha budget per risolverlo?

Un difetto visibile che nessuno paga per correggere non è un'opportunità. È il caso
più seduttivo di falso positivo, perché rilevarlo è gratis.

**Concorrente reale per questo tipo di lavoro:** non un altro vendor software, ma
un'agenzia web a 10–30k una-tantum.

### D-066 — Cavallo di Troia: legittimo solo con condizione di conversione · `PROPOSTO`

Tesi dell'utente: *"capisco non monetizziamo subito, ma avremmo un MVP con cavallo di
troia in un network complesso; sarebbe apporto immateriale di network o conoscenze."*

Onesto sul fatto che non monetizza. Ma è lo stesso pattern di D-049 e doc 13 § 3.5:
**lavoro che produce accesso invece di ricavo, e sembra progresso.**

Un cavallo di Troia funziona se:

```text
1. hai una ragione per essere fatto entrare     → § 13-15, da verificare
2. nel network ci sono soldi                    → sì, €125/utente/mese × 3.000 aziende
3. hai un piano per convertire accesso in ricavo → MANCA
4. puoi sopravvivere al tempo necessario        → DA VERIFICARE: dipendente pubblico,
                                                   budget < 10 €/mese, nessuna entità
```

I punti 3 e 4 sono quelli che mancano. Regola proposta:

> L'accesso si compra solo con una **condizione di conversione scritta e datata**.
> "Entro X mesi, questo accesso deve aver prodotto Y." Altrimenti è collezionismo
> di relazioni.

### D-067 — Riframing della proposizione editoriale · `PROPOSTO`

Se si propone qualcosa a Prometeo, la leva non è la qualità della comunicazione
(offensivo, e compete con le agenzie) ma il **costo di produzione**:

```text
SBAGLIATO   "il vostro sito è statico e non comunica l'ecosistema"
            → critica + concorrenza con agenzie + budget marketing

GIUSTO      "ogni contenuto che producete su RENTRI genera automaticamente
             le viste per ruolo, le FAQ, le note di release — e resta coerente
             quando cambia la norma"
            → tempo risparmiato a un team piccolo + nessuna agenzia lo fa
```

La scansione § 13.2 lo documenta già: *"lo stesso concetto può essere riscritto più
volte con rischio di incoerenze e duplicazione."* Quello è un costo di produzione
ricorrente, non un difetto estetico una-tantum.

E § 13.1 è la parte forte: quando cambia una norma vanno aggiornati articolo,
webinar, slide, procedura E le pagine collegate. È BRAIN-006, ed è ricorrente.

---

### D-068 — Prometeo web: l'impressione era giusta, il motivo era sbagliato · `DECISO`

Scansione tecnica eseguita (NX-96 chiuso). Due correzioni in direzioni opposte.

**SBAGLIATO — "il sito è statico":**

```text
WordPress 7.1 + Elementor 4.2.4 + Hello Elementor 3.5.1, Apache/PHP
HTML server-rendered, non SPA (nessun _next/, __NEXT_DATA__, Nuxt, Vite)
WP Rocket 3.23.3.3 attivo · SEOPress · sitemap attiva · REST API attiva
→ per un sito editoriale è la scelta CORRETTA: SEO, link condivisibili,
  redazione non tecnica, aggiornamenti frequenti
```

**GIUSTO — "non comunica la sensazione di ecosistema":**

```text
153 pagine · 206 articoli · 855 media
custom post type verticali per moduli / ruoli / casi cliente / norme /
versioni / eventi / webinar / settori:  NESSUNO
tipi osservati: post, page, attachment, nav_menu_item, wp_block, wp_template,
                elementor_library, elementor_snippet
```

**Il loro business È una rete di responsabilità a cinque nodi. Il loro modello di
contenuto è `page`.** La mancanza di fluidità percepita non è rendering: è assenza
di modello semantico. § 8.1 della scansione lo dice correttamente.

Caso da manuale del perché `observed ≠ inferred` (D-037): l'inferenza ("è statico")
era falsa, l'osservazione soggettiva ("non sento l'ecosistema") era vera, e solo la
verifica le ha separate.

### D-069 — Il namespace `mcp` in `/wp-json/` · `DECISO`

Dalla scansione: i namespace esposti includono **`mcp`** e `wp-abilities/v1`.

```text
conseguenza 1   WordPress espone già una superficie agent-accessible.
                Il connettore per questa fonte è quasi gratuito:
                REST /wp-json/wp/v2/{pages,posts,media} + sitemap.
                NX-27/28 per WordPress = lavoro minimo.

conseguenza 2   L'INGESTION È COMMODITY. Se REST e MCP sono pubblici,
                chiunque può costruire un overlay semantico sui loro contenuti.
                La barriera "è difficile integrarsi" non esiste più.

conseguenza 3   Quindi il moat si sposta: NON è l'ingestione, è L'ONTOLOGIA.
                  norma ↔ obbligo ↔ ruolo ↔ modulo ↔ caso cliente ↔ versione ↔ CTA
                E l'ontologia richiede conoscenza di dominio.
                Che è esattamente ciò che A. ha e tu non hai.
```

Il punto 3 chiude un cerchio aperto in D-064: il profilo co-founder non è più
ipotetico, è il collo di bottiglia identificato da una scansione tecnica.

### D-070 — La stessa capacità serve due compratori · `PROPOSTO`

Due bisogni emersi separatamente convergono:

```text
BISOGNO EDITORIALE (scansione § 13.1 del doc Prometeo)
  cambia una norma → vanno aggiornati articolo, webinar, slide, procedura
  E le pagine collegate
  → serve: grafo di dipendenza norma → contenuti

BISOGNO FORENSE (D-062)
  "qual era lo stato al momento del fatto, secondo la norma allora vigente?"
  → serve: grafo di dipendenza norma → contenuti, VERSIONATO nel tempo
```

**È la stessa struttura.** Il secondo è il primo con l'asse temporale.

```text
        norma (versionata)
             ↓ dipende
        obbligo
             ↓ impatta
   ┌─────────┼─────────┬──────────┐
 pagina    articolo   webinar   procedura
                                 ↓ dimostra
                            caso cliente
```

Due viste dello stesso grafo:

```text
vista REDAZIONE   "questa norma è cambiata: ecco le 40 pagine impattate"
vista LEGALE      "in quella data, questa norma diceva questo,
                   e questi erano gli obblighi allora vigenti"
```

È `contenuto → viste` (D-002) applicato a un grafo normativo. Ed è NX-88
(BRAIN-006) — l'unica capacità del pilot non coperta da C-01..C-08.

**Due compratori diversi, una capacità sola.** È la prima volta nella sessione che
una singola capacità ha due payer identificati, ed è il criterio di NX-31/regola del
due (D-040 punto 1) soddisfatto per la prima volta con evidenza.


---

### D-071 — Prometeo non è incatenato: narrativa fra pari, non di salvataggio · `DECISO`

**Correzione dell'utente:** *"Prometeo è un progetto con un moat, un mercato, una
narrativa importante per il tipo di settore, e già un network."*

La prima stesura dell'allegato narrativo impostava Prometeo incatenato ed Ermes come
soccorritore. **Sbagliato nei fatti e offensivo nella forma.**

Correzione applicata in `ALLEGATO-NARRATIVO-PER-A.md`:

```text
Prometeo   ha fuoco, fucina, mercato, narrativa, network. Non gli manca niente
           che Open Nexus possa portargli.
Ermes      non è un soccorritore. È un pari su un piano ORTOGONALE.

Prometeo   costruisce e registra      risponde a: cosa è successo?
Ermes      attraversa e collega       risponde a: cosa significa, da dove viene,
                                      chi ne risponde?
```

Coerente con § 4.3 della nota analitica (*"riteniamo di aver bisogno di voi più di
quanto voi abbiate bisogno di noi"*) e con D-069 (l'ingestione è commodity,
l'ontologia richiede dominio).

### D-072 — Perché Ermes · `DECISO`

```text
dio della SOGLIA            confini e loro attraversamento
                            → il dominio è fatto di passaggi fra soggetti diversi
dio dei MESSAGGI            → traduzione fra nodi che non condividono contesto
dio degli SCAMBI            → rete di responsabilità
e soprattutto:
da Ermes deriva ΕΡΜΗΝΕΥΤΙΚΗ → ERMENEUTICA, l'arte di interpretare
                            → per un avvocato è il mestiere, non una metafora
```

Il registro narrativo è legittimo e coerente con la sensibilità dichiarata
dall'utente (P.K. Dick, Asimov, "attinenza fra il brand e queste cose").

### D-073 — Due documenti, due registri, mai mescolati · `DECISO`

```text
NOTA-PER-A.md                  analitico · OSSERVATO/INFERITO/LIMITE · fonti
ALLEGATO-NARRATIVO-PER-A.md    narrativo · ZERO affermazioni fattuali · dichiarato
```

**Regola:** se la narrazione entra nel documento analitico, gli toglie credibilità.
Se sta da sola ed è dichiarata come narrativa, aggiunge desiderio senza costare
rigore.

Ordine di invio: **prima la nota analitica, poi l'allegato.** Un avvocato legge la
narrazione dopo aver verificato i fatti; se arriva prima, viene classificata come
marketing.

L'allegato contiene deliberatamente la stessa ammissione onesta della nota (§ 6:
l'acquisizione dei contenuti pubblici è banale, l'ontologia è vostra). Coerenza fra i
due registri: la verità non cambia col registro.


---

### D-074 — Cosa "Y = ?" invalida dell'audit di mercato · `DECISO`

Correzione dell'utente: con Y indefinita, parte dell'audit si basa su dati prematuri.

```text
RESTA VALIDO — intelligence di mercato, indipendente da Y
  assi di pricing osservati · premio di verticale 7–70× · tre livelli di
  ricavo per testa · filtro di sostituibilità · governance come asse di prezzo ·
  banda $11k–50k ARR come RIFERIMENTO

NON È VALIDO — proiezione su di noi
  qualunque stima di NOSTRO ricavo · la scelta del payer · il nostro pricing ·
  NX-65 usato come obiettivo invece che come paragone
```

**Regola:** la scansione dice cosa paga il mercato, non cosa incasseremmo noi.
Stesso tipo di errore di "il sito è statico": dato buono, conclusione non supportata.

### D-075 — Quantizzazione della collaborazione Prometeo · `DECISO`

`31-QUANTIZZAZIONE-PROMETEO.md`. Sintesi:

```text
costo monetario      €200–500 avvio (di cui la verifica legale è la voce vera)
                     < €30/mese ricorrenti
costo di lavoro      8–14 settimane concentrate; versione minima 5–7
costo di CALENDARIO  5–8 mesi, dato un impiego a tempo pieno
                     (320–560 ore a 10 ore/settimana reali)
costo opportunità    IL VERO COSTO: il primo ricavo che non arriva
                     (P4 in 2–4 settimane, P5 in 4–8)
```

Tre scenari, con probabilità dichiarate come inferite:

```text
A  la collaborazione funziona      12–24 mesi, fee €5–20k poi licenza   prob. bassa-media
B  riferimento riutilizzabile      18–30 mesi, €4.5–20k/mese            prob. media
C  non decolla                     5–8 mesi, nessun ricavo,
                                   MA NX-99 entra in Foundation,
                                   M-06 parziale, relazione, riferimento  prob. LA PIÙ ALTA
```

> **Lo scenario più probabile è quello senza ricavo.** Un piano che non lo contempla
> non è un piano.

### D-076 — La questione delicata: la nota insegna all'incumbent · `DECISO`

> Più la nota di analisi è convincente, più insegna a un incumbent con 3.000 clienti
> e un team di sviluppo esattamente cosa gli manca e come chiuderlo.

```text
GIÀ DATO              analisi del sito (pubblica, rifacibile) · osservazione sul
                      modello piatto · le due viste concettuali · l'ammissione che
                      l'ingestione è commodity

DA NON DARE           ontologia specifica · design del grafo · il motore
                      (Foundation non si spedisce) · metodo di riduzione e numeri
                      di costo · contratti interni

DA FIRMARE PRIMA      chi possiede l'ontologia prodotta insieme
                      chi possiede il grafo
                      DIRITTO DI RIUSO per altri clienti      ← il punto critico
                      cosa succede se la collaborazione finisce
```

**Senza clausola di riuso, si regala M-06 a un incumbent.** Con la clausola, si ha un
riferimento e un asset.

### D-077 — Leva negoziale sbilanciata, da accettare · `DECISO`

```text
LORO   3.000 aziende · dominio · dati · canale · team · cassa
TU     software funzionante e visibile · analisi di qualità · velocità ·
       un motore che non devono costruire
```

> **Non negoziare da pari.** Negoziare da fornitore specializzato che porta una cosa
> che loro non hanno tempo di fare. È l'unica posizione credibile.

### D-078 — Tre condizioni prima di iniziare il pilot · `DECISO`

```text
1. NX-86 risolto          posizione di dipendente pubblico chiarita con un legale
2. NX-91 risposto         chi è A. rispetto a Prometeo. Se non è collegato,
                          la controparte non esiste e il documento va riscritto
3. accordo scritto minimo anche una pagina: proprietà dell'ontologia, proprietà
                          del grafo, diritto di riuso, uscita
```

Senza le tre, il pilot è *"il modo più affascinante di perdere otto mesi"*.

---

### D-079 — MVP: i quattro criteri non sono dello stesso tipo · `DECISO`

Definizione dell'utente: *"l'MVP sarà pronto quando l'esperienza Open Nexus sarà
completa, Roy in grado di rispondere sulla piattaforma, UX intrigante con librerie
accattivanti, domande come 'analizzami questo sito e dimmi cosa faresti'."*

```text
1. "l'esperienza Open Nexus sarà completa"        COMPLETEZZA
   → non è una definizione, è un aggettivo. "Completa" non chiude mai.
   → MVP = Minimum Viable Product: se è completa non è minima.

2. "Roy in grado di rispondere sulla piattaforma"  CAPACITÀ
   → necessaria, ma non delimita lo scope. Rispondere a cosa, con che accuratezza,
     a che costo, con che latenza?

3. "UX intrigante con librerie accattivanti"      QUALITÀ
   → non bounded. E in tensione con D-025: CAPISCE richiede ~12 primitive,
     non 80 componenti. "Accattivante" è la strada verso le 80.

4. "analizzami questo sito e dimmi cosa faresti"  IL TEST
   → l'unico dei quattro che è FALSIFICABILE. Ed è la definizione.
```

**Decisione: il punto 4 è la definizione di MVP. I punti 1–3 sono quality gate, e
vanno resi numerici o non chiuderanno mai.**

```text
"completa"       → elenco di N pagine, contabile
"Roy risponde"   → % di domande, latenza, costo per domanda
"intrigante"     → 5 persone, gli dai 5 URL, tornano con un sesto?
```

### D-080 — Roy · `PROPOSTO`

Roy è l'assistente che risponde sulla piattaforma. Nota:

```text
· è il settimo nome in circolo (OpenFav · Open Nexus · Nexus Lab ·
  nexus-builder · nexus-mcp · opnx · Roy) — NX-81 peggiora
· Roy richiede un'interfaccia conversazionale = RIGA 2 di costo (D-015bis):
  il Brain paga i token. Va instrumentato (NX-24) e delimitato.
· `open-nexus/assistant` esiste già (PROTECTED) e `physical/main/chat` esiste:
  da verificare lo stato reale, non assumere
· il nome Roy non si collega alla mitologia Nexus/Prometeo/Ermes.
  Può essere deliberate (nome umano amichevole, come Alexa/Siri) — ma va deciso,
  non accumulato
```

### D-081 — La correzione è reciproca · `DECISO`

L'utente: *"ogni tanto ti correggo io."*

Vero, e va registrato come dato di processo:

```text
correzioni dell'utente accettate in questa sessione
  · X può essere altro (contro la mia chiusura su un verticale)
  · A. è candidato co-founder, non contatto in orbita
  · Prometeo ha moat/mercato/narrativa/network — non è incatenato
  · la domanda era malformulata: Y = ? invalida le proiezioni
  · l'MVP non è ciò che ho descritto io

correzioni dell'assistente accettate dall'utente
  · riduzione 450× invece di modello economico
  · il gate deve essere codice, non LLM
  · Y = chi deve rendere conto, non "sa fare un prompt"
  · la scansione per capacità invece che per categoria
  · K6: Y-1 richiede capacità teoriche
```

Il metodo funziona quando entrambe le direzioni sono attive. Registrato perché è la
prova operativa di D-037/M-05: **un sistema che ti dà sempre ragione non ti sta
rispondendo.**

---

### D-082 — Grafia del nome · `DECISO`

```text
PROSA           Open Nexus        (separato)
IDENTIFICATORI  open-nexus        (kebab: percorsi, registry ID, directory)
                open-nexus/library · open-nexus/index · src/applications/open-nexus
                open-nexus-foundation (repo)
REPO STORICO    OPENNEXUS nei nomi file già esistenti
                (../documentation/research/benchmarks/TRUSTABLE-vs-OPENNEXUS.md, 21-CAPABILITA-OPENNEXUS.md)
                → non rinominati: romperebbero i riferimenti incrociati
```

Bonifica eseguita: **105 sostituzioni** in 25 file. I 20 identificatori kebab-case
sono intatti.

Collega a NX-81 (gerarchia dei nomi): `Open Nexus` con lo spazio è la forma di prosa,
ma la gerarchia completa (Nexus Lab / Open Nexus / nexus-builder / nexus-mcp / opnx /
Roy) resta da decidere.

### D-083 — Come si dice quello che Open Nexus fa per Prometeo · `DECISO`

Tre candidati proposti dall'utente, tutti con punto di domanda:

```text
"modernizzazione"            ✗ implica che siano indietro. Non lo sono:
                               3.000 aziende, RENTRI-ready, dominio maturo.
                               Falso e offensivo.
"valore aggiunto"            ✗ vuoto. Lo dice ogni vendor. Zero informazione.
"aiuto / governance          ~ direzione giusta, ma "aiuto" è debole e "governance
 della conoscenza"             della conoscenza" è gergo da consulenza.
```

**Formulazione decisa:**

> **Open Nexus non modernizza e non aggiunge: rende attraversabile e dimostrabile
> ciò che già esiste.**

Tre proprietà: non offensiva (niente di ciò che hanno è sbagliato), specifica (due
verbi verificabili), onesta (non creiamo conoscenza, strutturiamo quella che c'è).

Declinata per interlocutore:

```text
a chi pubblica     "cosa dipende da cosa, e cosa va aggiornato
                    quando cambia una norma"
a chi assiste      "cosa era vero in quella data, e come lo dimostro"
```

Nessuna delle due contiene la parola "AI", "innovazione" o "digitale".

### D-084 — Direzione naturale di Prometeo · `PROPOSTO` (ipotesi da verificare)

**Osservato:**

```text
206 articoli vs 153 pagine      → è un'operazione editoriale, pubblicano di continuo
namespace elementor-ai/v1       → Elementor AI disponibile/attivo sul CMS
namespace mcp                   → il CMS è già leggibile da agenti
producono webinar e documentazione su RENTRI
coprono 6+ ruoli distinti
transizione RENTRI ancora in corso → cambiamento normativo continuo
```

**Inferito — quattro direzioni probabili:**

```text
1. velocità di contenuto     RENTRI continua a cambiare, devono continuare a spiegare
2. funzioni AI nel gestionale ogni SaaS verticale le sta aggiungendo;
                             elementor-ai suggerisce che hanno già cominciato
                             dal lato contenuto
3. approfondimento per ruolo  hanno già 6+ ruoli, la crescita è in profondità
4. interoperabilità di filiera la catena è intrinsecamente multi-soggetto
```

**Il punto che conta:**

```text
un'AI dentro un gestionale risponde a: "qual è lo stato?"
non risponde a:                      "cosa era vero allora, secondo la norma
                                      allora vigente, e come lo dimostro?"
```

La vista probatoria **non è sulla loro traiettoria naturale**, perché un sistema
transazionale registra lo stato corrente per mestiere. È buona notizia (non si
compete) e cautela insieme (potrebbero non vedere il bisogno).

**Da verificare con A.**, non da assumere. È la domanda § 7.2 della nota.


---

### D-085 — Bonifica tenant eseguita, con residuo tecnico · `DECISO`

2026-09-16: l'utente conferma la cancellazione dei file dal tenant istituzionale.
NX-50 passa da P0 urgente a P1 parziale.

**La cancellazione è necessaria ma potrebbe non essere sufficiente.** Residui da
verificare, in ordine di probabilità:

```text
1. CESTINO DI PRIMO LIVELLO      OneDrive/SharePoint conserva gli elementi eliminati
                                 (tipicamente ~93 giorni) finché il cestino non è svuotato
2. CESTINO DI SECONDO LIVELLO    a livello di site collection, per i file su SharePoint
3. CRONOLOGIA VERSIONI           se il file è stato modificato, le versioni precedenti
                                 possono essere conservate
4. INDICIZZAZIONE COPILOT        il file stava in "File chat di Microsoft Copilot":
                                 se Copilot lo ha elaborato, possono esistere log
                                 dell'interazione indipendenti dal file
5. RETENTION POLICY del tenant   se il tenant ha policy di conservazione (Purview),
                                 gli elementi eliminati possono essere preservati
6. AUDIT LOG                     la registrazione dell'esistenza del file e della sua
                                 cancellazione può persistere anche dopo l'eliminazione
```

I punti 1–3 si risolvono svuotando i cestini. I punti 4–6 **non sono sotto il
controllo dell'utente** e dipendono dalla configurazione del tenant: vanno chiesti,
non verificati in autonomia.

**Nota di proporzione:** per una cartella OneDrive personale in un tenant
istituzionale, cancellazione + svuotamento cestino è nella pratica sufficiente.
I punti 4–6 contano se il contenuto era sensibile o se il progetto diventa
commerciale. Non vanno trattati come emergenza, vanno trattati come domanda da
porre insieme a NX-86.

**Ciò che resta davvero aperto di NX-86 non è tecnico:**

```text
· verifica con un legale su incompatibilità e autorizzazioni per attività
  extra-istituzionali
· il campo MITTENTE vuoto nei due documenti per A.
· la scelta del canale di invio (personale, mai istituzionale)
```


---

### D-086 — Due simulazioni del destinatario: cosa hanno prodotto · `DECISO`

L'utente ha eseguito due simulazioni indipendenti del destinatario A., con due modelli
diversi, entrambe con la cornice *"mi hanno inviato questo"*.

```text
simulazione 1 (ChatGPT)   giudizio "sono seri" + tre criteri
                          → ha prodotto: l'esercizio della catena come secondo incontro
simulazione 2 (DeepSeek)  piano in 6 punti dal punto di vista di chi riceve
                          → ha prodotto: pilot in due stadi + formalizzazione
                            dati PRIMA della prova
```

**Convergenze fra le due (quindi robuste):**

```text
· leggere prima la nota analitica, poi l'allegato      → conferma D-073
· il finding di § 3 va verificato contro la percezione del destinatario
· la domanda 3 di § 7 è quella che decide
· § 4.5 è stata notata da entrambe come segno positivo
```

**Punti in cui la simulazione 2 è migliore di quanto avessi proposto:**

```text
PUNTO 4   "mini-pilot, non un progetto, non un preventivo. Esperimento
           controllato su UNA norma specifica e un numero limitato di contenuti"
           → più delimitato della mia formulazione. "Una norma" è il vincolo
             che mancava.

PUNTO 5   "metterei per iscritto data protection e limiti PRIMA di qualunque prova"
           → § 4.5 diceva cosa faremmo. Non diceva che va formalizzato prima.
             Corretto: ora § 4.5 elenca i quattro punti (chi tratta cosa · per
             quanto · base giuridica · traccia) e dichiara che l'elenco non è
             ancora il documento.  → NX-103
```

**Sintesi dei due stadi di pilot (NX-102):**

```text
STADIO 1 · CASO        un caso reale già chiuso che è costato tempo
                       ricostruzione insieme della catena
                       fatto → documento → norma → versione → ruolo → decisione
                       si osserva DOVE SI SPEZZA
                       → serve a scoprire se il problema esiste

STADIO 2 · STRUTTURA   UNA norma specifica, numero limitato di contenuti
                       si verifica se il grafo norma → obbligo → contenuto →
                       documento sta in piedi
                       → serve a verificare se la soluzione regge
```

Ordine corretto: prima il caso, poi la struttura. Fare il contrario significa
costruire la soluzione prima di aver visto il problema.

### D-087 — L'ambiguità del destinatario è comparsa in ENTRAMBE le simulazioni · `DECISO`

Nella simulazione 2, il punto 2 chiede al destinatario di verificare se *"quando
cambia una norma ti tocca ricostruire a mano quali pagine, articoli, FAQ, slide,
casi cliente dipendono da quella norma"*.

**Quella è la § 5.2 editoriale — il dolore di chi pubblica il sito.** Ma il punto 3
della stessa simulazione chiede della ricostruzione probatoria, che è il dolore di
un avvocato.

Due lettori simulati indipendenti, due modelli diversi, hanno entrambi assunto che
il destinatario avesse **entrambi** i dolori.

```text
lettura 1   i documenti sono ambigui sul destinatario        → NX-91 ancora aperto
lettura 2   i due dolori coesistono nella stessa persona      → possibile, se A.
            (un avvocato che assiste un'associazione che       pubblica contenuto
             pubblica circolari)                              normativo per i soci
```

La lettura 2 è plausibile e non va scartata: uno studio legale o un'associazione di
categoria **pubblica** contenuto normativo e ha anche bisogno di **ricostruzione
probatoria**. Se A. sta in quel punto, i documenti sono corretti così come sono.

Ma è un'ipotesi, e resta la domanda 1 di § 7 a risolverla.

**Conseguenza pratica:** se i documenti verranno inoltrati a terzi, l'oscillazione
sul destinatario si ripresenterà. Non blocca l'invio.

### D-088 — Limite delle simulazioni · `DECISO`

Due simulazioni convergenti sono più robuste di una, e hanno prodotto miglioramenti
reali ai documenti (§ 4.5, promozioni, metodo del conteggio).

Ma hanno un limite strutturale condiviso:

```text
entrambe simulano un lettore COOPERATIVO, ARTICOLATO, ANALITICO
nessuna delle due può produrre il numero che decide:
   quante ore costa ad A. ricostruire cosa era vero in una certa data
```

Il "sono seri" di entrambi i modelli è un certificato di qualità sul manufatto.
Non è un anticipo della risposta.

**Valore marginale di una terza simulazione: prossimo a zero.**
**Valore marginale dell'invio: alto.**

---

### D-089 — La motion è il primo esercizio end-to-end del ciclo Foundation → X → Foundation · `DECISO`

Osservazione dell'utente: *"stiamo cercando di plasmare il materiale che abbiamo, e
al least avremmo pure realizzato il flusso completo Foundation → X → Foundation."*

Mappatura dei sei passi della motion (NX-104) sul ciclo:

```text
PASSO                          LIVELLO        CAPACITÀ
────────────────────────────────────────────────────────────────────────
1. osservazione pubblica       FOUNDATION     connector, classe 0     C-07 ~
2. riduzione deterministica    FOUNDATION     reduce, classe 0        C-07 ~
3. interpretazione             X              classe 1–2              —
4. separazione osservato /     FOUNDATION     governance              C-08 ~
   inferito / limite
5. proiezione → vista          FOUNDATION     PageData → Template →   C-01 ✓
   generata                                    Experience
6. output strutturato          FOUNDATION     artefatti               C-05 ~
────────────────────────────────────────────────────────────────────────
        FOUNDATION  →  X  →  FOUNDATION
```

**Il ciclo non ha mai girato.** Foundation produce ed Execution esegue è verificato
(due segmenti). X esiste come concetto e come pratica manuale (questa sessione).
Ma **il loop chiuso** — Foundation alimenta X, X produce, Foundation valida e
renderizza — non è mai stato eseguito su materiale esterno.

### D-090 — La motion esercita C-09, parzialmente · `DECISO`

C-09 (authoring agentico di ApplicationBundle) era marcata TEORICA e identificata
come *"la capacità su cui si regge l'intera visione ed è la meno verificata"*.

```text
cosa ESERCITA la motion      X produce contenuto semantico entro contratti
                             esistenti → Foundation valida → renderizza
                             → è la metà INTERNA di C-09

cosa NON esercita            X che autori un ApplicationDefinition completo
                             (routing, navigation, contracts, type)
                             → è la metà ESTERNA di C-09

e non esercita               NX-11 (materializzazione generata), che resta
                             prerequisito di 0.7.0 Authoring
```

**È la metà giusta da esercitare per prima.** La metà esterna richiede che la
interna funzioni.

### D-091 — La proprietà notevole: artefatto di vendita = integration test · `DECISO`

```text
la motion produce UN artefatto che è contemporaneamente:
  · il campione gratuito per il prospect        (go-to-market)
  · l'esercizio end-to-end del ciclo            (verifica architetturale)
  · il test di ripetibilità NX-57               (il metodo senza l'operatore)
  · contenuto pubblico per l'inbound            (NX-56)
```

Quattro funzioni, un artefatto. Non è efficienza: è il segno che la motion è
allineata con l'architettura invece che aggiunta sopra.

### D-092 — Il guard: niente demo-driven development · `DECISO`

Rischio specifico della doppia natura (vendita + test):

> Se la demo deve essere bella, la tentazione è scrivere la PageData a mano invece
> di produrla attraverso il ciclo. A quel punto hai venduto e non hai testato niente.

**Regola:**

```text
la vista generata deve passare da:
  riduzione → interpretazione → validazione → PageData → renderer

NON deve passare da:
  qualcuno che scrive la PageData a mano perché venga meglio

se un passaggio va fatto a mano per la demo, va MARCATO come manuale
e contato come debito del ciclo, non come risultato del ciclo.
```

Corollario: il primo ciclo girerà male. Va accettato. Una demo prodotta dal ciclo
reale è meno brillante e vale cento volte di più — perché è la prova, non la
rappresentazione della prova.


---

### D-090 — Documenti inviati ad A. · Modalità orbita confermata · `DECISO`

2026-09-17: nota analitica + allegato narrativo + messaggio di accompagnamento
**inviati**. Richiesto feedback in modo relazionale, non formale. A. ha risposto che
lo darà.

Framing usato dall'utente, ed è corretto:

> *"mi interessa in generale, il feedback; se non può essere Prometeo può essere
> Open Nexus (Nexus Lab)."*

**Perché funziona:** disaccoppia la relazione dall'affare. A. può dare valore anche
se Prometeo non è un prospect. Toglie a entrambi l'onere di una risposta commerciale,
che è ciò che fa morire i primi contatti.

> **"A. è una risorsa."**

Chiude NX-94: modalità = **orbita** (D-056), non pipeline e non co-founder. La
questione co-founder resta sospesa a NX-86.

**Errore dell'assistente:** ha ripetuto "i documenti non sono stati inviati" per più
turni dopo l'invio, su informazione scaduta. È esattamente il failure mode che la
regola di `03-WORKFLOW.md` serve a prevenire — affermare senza verificare — applicato
non al codebase ma allo stato del mondo. La regola va estesa: *ogni affermazione su
cosa è accaduto cita la fonte o chiede.*

**Stato:** attesa. NX-90 attivo. Nessuna azione richiesta fino alla risposta o fino
alla scadenza della cadenza (4–6 settimane).

---

### D-091 — Chiusura della sessione 2026-09-10 → 2026-09-17 · `DECISO`

**L'arco, in due righe:**

```text
APERTURA   "sono molto geloso del lavoro fatto" · paura del clone in dieci giorni
           domanda: come proteggo ciò che ho costruito

CHIUSURA   due documenti consegnati a una persona reale, con fonti, limiti
           dichiarati e tre domande di cui due chiedono "dove abbiamo letto male"
           domanda: di cosa ha bisogno chi ha davanti questo
```

La protezione non è stata risolta con una licenza. È stata risolta distinguendo ciò
che è copiabile (l'analisi, il codice, le astrazioni) da ciò che non lo è (l'ordine
in cui sono stati scritti, le cinque stratificazioni, il corpus che compone) — e poi
**distribuendo gratis il primo per vendere il secondo**.

**Cosa ha portato A.:** la verticalità. Non come settore scelto, ma come persona con
una pratica, abbonamenti propri, strumenti che fa dialogare, e un modo di lavorare
forense stocastico che è esattamente ciò che Open Nexus rende deterministico e
difendibile.

Prima di A. il verticale era un **criterio** (D-047: dove rendere conto è un obbligo).
Dopo A. è un'**istanza**. È la differenza fra una tesi e un interlocutore.

**Perché la proposta era seria** — non per tono, per struttura:

```text
· fonti per ogni affermazione fattuale
· undici limiti dichiarati in una sezione propria
· una sezione "cosa NON proponiamo"
· l'ammissione che l'acquisizione è banale e l'ontologia è loro
· tre domande, di cui nessuna chiede una decisione commerciale
· nessuna richiesta di budget, nessun preventivo, nessuna scadenza
```

**Stato alla chiusura:**

```text
inviato         NX-101 ✓
in attesa       NX-90 (orbita attiva), NX-91 (in viaggio dentro la nota)
aperti e soli   NX-86 parte legale · NX-57 ripetibilità del metodo
non aperti      niente che richieda A.
```

Nessuna azione richiesta fino alla risposta di A. o alla scadenza della cadenza
(4–6 settimane). L'unica P0 che non dipende da nessuno è NX-57.


---

### D-092 — `05-EVALUATION.md` scritto come trascrizione, non come progettazione · `DECISO`

`brain/knowledge/05-EVALUATION.md`. Primo file del layer di conoscenza del Brain.

**Scelta di perimetro:** un file, non otto. E non `02-CAPABILITIES.md` come proposto,
perché:

```text
05-EVALUATION   esiste già nella pratica → va trascritto
02-CAPABILITIES richiede l'ontologia     → va estratta DOPO NX-57
```

**Contenuto:** 3 marcatori · 5 trasformazioni cognitive con i loro confini · 6 regole
di acquisizione · 6 di validazione · 5 di falsificazione · 6 di promozione · il passo
13 (contraddizione/coincidenza) · 9 antipattern datati · checklist di 13 voci.

**Ogni regola ha un precedente con data.** Le regole senza precedente non sono state
incluse: sarebbe stato progettazione, e la progettazione prima dell'evidenza è
l'antipattern A1.

**Tre rifiuti motivati:**

```text
✗ punteggio numerico di confidenza     tre categorie sono falsificabili, 0,7 no
✗ mappare 104 NX come capacità         le capacità reali sono 8-10, il resto compiti
✗ ontologia a 16 entità                Foundation esiste già (6), Cognitive sono 5,
                                       Operational (5) si dissolve: Document/Source,
                                       Answer/Interpretation/Proposal, Agent, Context
```

**Sequenza confermata:** `05-EVALUATION` → NX-57 (esecuzione cieca del metodo) →
estrazione dell'ontologia dal risultato. Non il contrario.

### D-093 — NX-50: regressione spiegata e risolta · `DECISO`

I link al tenant istituzionale ricomparsi il 2026-09-17 erano file caricati come
contesto per un agente, destinati a cancellazione immediata. Non è una ripresa
dell'abitudine.

Regola pratica che ne segue: **quando un agente chiede contesto, il contesto si
incolla nel prompt, non si carica sul suo storage.** È la stessa regola di D-014
applicata agli strumenti invece che ai repository.
