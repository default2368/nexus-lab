# NEXUS LAB — Workspace di progetto

**Aperto:** 2026-09-10
**Scopo:** preservare continuità di brainstorming, decisioni e backlog fra sessioni.

---

## Mappa degli artefatti

| File | Cos'è | Quando si tocca |
|---|---|---|
| `NEXUS-LAB/00-INDICE.md` | questo file — mappa e stato | ogni sessione |
| `NEXUS-LAB/01-DECISION-LOG.md` | decisioni prese + domande aperte | quando si decide qualcosa |
| `NEXUS-LAB/02-BACKLOG-NX.md` | backlog NX-01 → NX-107 operativo | quando si aggiunge/sposta lavoro |
| `NEXUS-LAB/03-WORKFLOW.md` | il loop brainstorm → PRD → prompt MCP → esecuzione | quando il metodo cambia |
| `NEXUS-LAB/04-FOUNDATION-API.md` | architettura distribuzione protetta (NX-01b) | quando cambia il modello di distribuzione |
| `NEXUS-LAB/05-AF001-VERDETTO.md` | esito validazione AF-001 + Authority Drift Pattern | congelato |
| `NEXUS-LAB/06-PROMPT-Q005.md` | prompt MCP-ready per Q-005 / NX-11 / NX-12 | quando serve rieseguire |
| `NEXUS-LAB/07-PERSONA-AUTHORITIES-COSTO.md` | persona, tre Authority, modello di costo di X | quando cambia la persona o il modello di costo |
| `NEXUS-LAB/08-COST-CULTURE.md` | rate card, reduction pipeline, classi di costo, guardrail, **§ 7 API vs self-hosting con break-even** | quando cambiano i prezzi o le classi |
| `NEXUS-LAB/09-SERVER-PROVIDER-LAYER.md` | spec provider layer per il server nuovo (NX-26) | durante il refactor del server |
| `NEXUS-LAB/10-PROMPT-NX26.md` | prompt MCP-ready in 5 fasi per Roo Code (NX-26) | quando si esegue il refactor |
| `NEXUS-LAB/11-CONNECTOR-LAYER.md` | connector layer, change detection, riuso della libreria di scraping | quando si tocca l'acquisizione dati |
| `NEXUS-LAB/12-MERCATO-CONOSCENZA.md` | analisi del mercato "CAPISCE": AlphaSense, Hebbia, Rogo, Aiera | quando si discute di posizionamento |
| `NEXUS-LAB/13-X-MOAT-E-PRIMA-APPLICAZIONE.md` | moat di X, team, prima applicazione come reference validation | quando si decide cosa costruire per primo |
| `NEXUS-LAB/14-AUTHORITY-ARCHITECTURE.md` | **stato reale** delle 5 authority, roadmap 0.7.0.x, UX come dimensionamento | ogni volta che si tocca Foundation |
| `NEXUS-LAB/15-APPLICATION-AUTHORITY-EVIDENZE.md` | evidenze dai file: tre layer, Q-005 risolta, odori in `simple.ts` | riferimento, basato su lettura diretta |
| `NEXUS-LAB/16-FOUNDATION-HEALTH.md` | griglia di salute di **Open Nexus** (artefatto) — B+/A− | a ogni milestone |
| `NEXUS-LAB/17-NEXUS-LAB-HEALTH.md` | griglia di salute di **Nexus Lab** (ente) — C+/B− | a ogni milestone |
| `NEXUS-LAB/18-WHY-NEXUS-LAB-EXISTS.md` | **can vs should**, verticale candidato, prima esperienza reale, ⚠️ bonifica tenant | quando si decide cosa costruire per primo |
| `NEXUS-LAB/19-METHOD-AGENT-GIUDIZIO.md` | giudizio su Method Agent — **bersaglio sbagliato**, corretto da doc 20. Resta valido § 4 (gate = codice) e § 5 (staleness) | storico |
| `NEXUS-LAB/20-CAPABILITA-ANALISI-MERCATO.md` | **la capacità di analizzare progetti di mercato**: correzione, mercato, chi paga, perché serve Open Nexus | quando si parla di prodotto |
| `NEXUS-LAB/21-CAPACITA-OPENNEXUS.md` | **inventario capacità** C-01→C-12 con evidenza + il pilota che ne cade fuori | a ogni milestone |
| `NEXUS-LAB/22-PRIVACY-TOKENIZZAZIONE.md` | tokenizzazione locale: convergenza con reduction pipeline, 4 punti di rottura, GDPR | quando entra il verticale civico/PA |
| `NEXUS-LAB/23-MOAT.md` | **rendiconto del moat**: 4 costruiti, 2 condizionali, le 3 mosse che li attivano | quando si riparla di protezione/IP |
| `NEXUS-LAB/24-SCANSIONE-PER-CAPACITA.md` | **scansione di mercato per capacità**: Asse 1 (§8), due mercati (§9), product marketplace (§10), serie storica (§11), pricing e frizioni (§12) | quando si fa ricerca di mercato |
| `../documentation/stakeholders/a/NOTA-PER-A.md` | **documento esterno per A.** — marcato OSSERVATO/INFERITO/LIMITE, nessuna strategia interna | prima di inviarlo: NX-86 |
| `../documentation/stakeholders/a/ALLEGATO-NARRATIVO-PER-A.md` | **allegato narrativo** — registro separato, zero affermazioni fattuali. Prometeo/Ermes, Open Nexus Language, il network ideale | si invia DOPO la nota analitica |
| `NEXUS-LAB/25-SINTESI-SEMPLICE.md` | **tutto in parole semplici** — per un collaboratore nuovo, o per te fra sei mesi | quando serve spiegare il progetto da zero |
| `NEXUS-LAB/26-CHI-E-Y.md` | **chi è Y**, la frase per la nonna, perché lo sviluppatore non ha capito, quando entra l'AI | prima di scrivere qualunque pitch |
| `NEXUS-LAB/27-SCORING-ISTANZE.md` | **matrice K1–K8** sulle istanze candidate + nomenclatura X→Ambiente→Istanza | quando si sceglie l'istanza |
| `NEXUS-LAB/28-PROMETEO-RENTRI.md` | Y-2 / Prometeo / RENTRI: matrice, sequenza vincolante | storico |
| `NEXUS-LAB/32-MOTION-Y-IDEA-SITE-KNOWLEDGE.md` | **la motion di mercato**: l'artefatto di vendita È l'output del prodotto. Y, i due canali, freemium/premium | quando si parla di go-to-market |
| `NEXUS-LAB/33-INDICE-NX.md` | indice generato delle voci `NX-*`, cruscotto, priorità, aree e chiuse | quando cambia il backlog |
| `NEXUS-LAB/34-RIFERIMENTI.md` | manifest privato di risoluzione delle citazioni Brain → corpus strategico | a ogni nuovo ID citato in `brain/knowledge/` |
| `NEXUS-LAB/STRATEGIC-WORKFLOWS/G-AUDIT-ENGAGEMENT-CONTROL.md` | simulazione strategica per G.: procedure → lavoro → feedback → controllo | durante il pilot sintetico di quattro settimane |
| `NEXUS-LAB/STRATEGIC-WORKFLOWS/G-PILOT-BOOTSTRAP.md` | dogfooding strutturale: Open Nexus costruisce il pilot G. usando Open Nexus | a ogni versione 0.1/0.2/0.3 del pilot |
| `../brain/knowledge/08-RULESETS-AND-AGENT-PROFILES.md` | regole general/epistemic/control, profilo Roy e workflow di promozione | quando un failure mode diventa candidate rule |
| `../frontend/backlog/README.md` | regole del backlog operativo frontend: max 3 in corso, DoD verificabile | quando cambia il processo operativo |
| `../frontend/backlog/BACKLOG.md` | backlog frontend eseguibile FE-001→FE-013, separato dal corpus NX | aggiornamento settimanale di 15 minuti |
| `../cli/backlog/BACKLOG.md` | backlog operativo CLI: baseline minimal → `opnx init` → scaffold test → `create app` | durante la transizione 0.7.0.4 → 0.8 |
| `../foundation/backlog/EPIC-0.9.0-SEMANTIC-ENTITY-PROJECTION.md` | Epic 0.9.0: Entity → Projection → Artifact → PageData, G pilot + Admin consumer | branch 0.9, prima dell’integrazione Brain |
| `../foundation/backlog/ADR-0016-SEMANTIC-ENTITY-PROJECTION-MODEL.md` | decisione e boundary del Semantic Entity Layer | stato PROPOSED fino ai gate 0.9 |
| `../foundation/backlog/PRD-0.9.0-SEMANTIC-ENTITY-PROJECTION.md` | requisiti, milestone, test e criteri di uscita della 0.9 | esecuzione ADR-0016 |
| `../brain/knowledge/05-EVALUATION.md` | gate epistemico del Brain: marcatori, validazione, falsificazione, passo 13 | ogni artefatto Brain |
| `../brain/knowledge/06-STORAGE-AND-VALIDATION.md` | ownership dei record, storage, versioning, gate, matrici e snapshot | quando si implementano i contratti Brain |
| `NEXUS-LAB/SORGENTI/AUTHORITY-MODEL.md` | modello delle Authority ricevuto da altra sessione | sorgente architetturale |
| `NEXUS-LAB/SORGENTI/CONTRACTS-REPORT-0.7.5.4C.md` | baseline verificata: 747 test, 26 failure preesistenti, authority 137/137 | gate per 0.7.5.5 → baseline 0.8 |
| `NEXUS-LAB/SORGENTI/25-SCANSIONE-PROMETEO-RIFIUTI.md` | sorgente della scansione prodotto/bisogni/network | congelato |
| `NEXUS-LAB/SORGENTI/SCANSIONE-TECNICA-PROMETEO.md` | sorgente della scansione tecnica del sito | congelato |
| `NEXUS-LAB/SORGENTI/check-style-authority.mjs` | snapshot sorgente Design Enforcement 0.7.0.2 | congelato |
| `NEXUS-LAB/31-QUANTIZZAZIONE-PROMETEO.md` | ⚠️ **NOTA INTERNA** — tempo/denaro/proiezione della collaborazione Prometeo, cosa proteggere, leva negoziale | prima di qualunque accordo |
| `NEXUS-LAB/30-MONETIZZAZIONE.md` | ⚠️ **NOTA INTERNA** — i 5 percorsi, ordinati per tempo di arrivo al ricavo. Non allegare, non inoltrare | quando si parla di soldi |
| `NEXUS-LAB/29-PROMETEO-ANALISI.md` | **analisi della scansione**: incumbent forte, soggetto non deciso, l'apertura forense | prima di qualunque contatto |
| `../documentation/research/benchmarks/TRUSTABLE-vs-OPENNEXUS.md` | dossier competitivo Trustable/Nuvolaris | congelato, riferimento |
| `../documentation/research/benchmarks/TOOLJET-benchmark.md` | benchmark architetturale + lezione di distribuzione | congelato, riferimento |
| `NEXUS-recap-ufficiale.pdf` | recap ufficiale Nexus 0.6.x (2026-08-20) | congelato, autorità |
| `.clinerules` | regole Roo Code / Cline | quando cambiano gli invarianti |
| `AGENTS.md` | regole Google AntiGravity | quando cambiano gli invarianti |

---

## Contesto permanente (non perdere)

### Il progetto

```text
Open Nexus = Foundation + X

FOUNDATION  → parte statica/core, kernel deterministico
              Astro + React, sopravvissuto a 4 stratificazioni architetturali
              suite di test vecchie ancora all'80%
              app live su https://openfav.vercel.app

X           → sistema operativo per visualizzare o creare conoscenza
              versione governata da AI
              "indeterminismo che diventa determinismo con Foundation"
```

### La baseline congelata

```text
FOUNDATION
  ApplicationBundle → BundleCollector → Build Artifacts → [boundary]

EXECUTION
  ApplicationDefinition → ApplicationContext → Discovery / Page Resolution
  → PageData → Template → Experience
```

**FOUNDATION produce, EXECUTION esegue.**
Il confine fra i due segmenti è il punto di invarianza del sistema.

Invariante assoluto: **Runtime never observes the repository directly.**

**PageData is the language of knowledge experiences.**

**Infrastructure must be reusable; Domain must be replaceable.**

### Roadmap

```text
0.6.3-A  Auth Foundation                    CLOSED
0.6.3-B  Auth Experience Closure            in chiusura
0.6.3-C  Artifact Consumption Closure       → elimina AF-001 (P0)
0.6.4    Application Experience Scaffolding
0.6.5    Source Observer V0 (experiment)
0.7.0    ApplicationBundle Authoring        → Human / AI / Importer
1.0      CLI per creare progetti senza toccare contratti o kernel
```

Domanda di fase 0.7.0 — da *"Il modello Nexus funziona?"* a
*"Possiamo produrre questo modello senza conoscere la struttura interna del repository?"*

### Ecosistema strumenti

```text
Trae          → host principale, Roo Code in split editor
Roo Code      → agente pesante/senior, deepseek-v4-pro su compiti complessi
Cline         → task semplici, agente leggero
Continue      → chat/autocomplete/inline edit, non agente autonomo
AntiGravity   → agenti Planner/Coder/Verifier
LMArena       → brainstorming, spec, PRD, review (GPT family in Arena Mode)

codebase-memory-mcp  → grafo semantico locale, UI http://127.0.0.1:9749
                       6.481 nodi / 13.923 archi sul repo Astro
git MCP locale       → working tree: status/diff/log/commit (risparmio token)
GitHub remote MCP    → issue/PR su GitHub.com, NON working tree locale

Brain (FastAPI)      → parte AI + server MCP, fly.io, grandi margini di crescita
CLI                  → già fa estrazione tokens, pilastro per creazione app
```

### Strategia modelli / costi

```text
deepseek-flash  → DEFAULT: extraction, inventory, audit, classificazioni,
                     retrieval-heavy, report preliminari
deepseek-v4-pro    → GATE: giudizio architetturale, refactor pericolosi,
                     commit complessi, decisioni Foundation/Runtime, second opinion

ROUTING = {
  "extraction":   flash,
  "retrieval":    flash,
  "contract":     pro,
  "architecture": pro,
  "embedding":    None,   # nessun provider a pagamento per ora
}
```

Principio embeddings: **Il testo è source authority. L'embedding è una proiezione,
mai una fonte.**

Budget target: **< 10 €/mese** finché non si accendono servizi pesanti.

### Segnali di mercato raccolti

```text
Instruqt   → valida "knowledge as experience"   (SaaS chiuso, enterprise)
Nuvolaris  → valida "sovereign AI workbench"    (infra privata, licensing offline)
Trustable  → il buco: NESSUN gate deterministico sull'artefatto generato
```

---

## Stato corrente

**Grafia del nome (D-082):** in prosa **Open Nexus** (separato). Negli identificatori
`open-nexus` (kebab: percorsi, registry ID, directory, repo). Bonifica eseguita su
105 occorrenze in 25 file.

**Formulazione decisa (D-083):** *Open Nexus non modernizza e non aggiunge: rende
attraversabile e dimostrabile ciò che già esiste.*

**Modalità:** BRAINSTORMING (zona sicura X — vedi `03-WORKFLOW.md`)

**Metodo Sonda (D-040, 2026-09-13):** separazione percorso-piattaforma /
applicazione-sonda, sei gate di promozione nel core, sequenza in sei passi.
È il boundary Foundation/X applicato alle **decisioni di prodotto**.
Simmetria: *Authority governa la proprietà del codice, Sonda governa la promozione
delle capacità.* Quattro lacune del metodo registrate (L-1..L-4) → NX-52.

**Doppia griglia di salute (2026-09-12):**
```text
Open Nexus (artefatto)   B+ / A−   boundary A · authority A− · enforcement contratti B
Nexus Lab (ente)        C+ / B−   produrre A · misurarsi A− · scegliere dove D
```
**L'artefatto è più sano dell'ente che lo produce** (D-039).
**Stato dichiarato dall'utente:** *"ancora nulla di deciso, stiamo ancora festeggiando
di essere vivi."* Nessuna decisione di prodotto presa. Tutto il materiale è
orientamento, non impegno.

**Sessioni 2026-09-10:**

1. Analisi Trustable/Nuvolaris → backlog NX-01 → NX-10
2. P-005 Foundation API tokenizzata (NX-01b) → split PRODUCE remoto / EXECUTION locale
3. Validazione AF-001 → **CHIUSO**, ipotesi falsificata, NX-01b sbloccato.
   Finding: Authority Drift Pattern (D-013), NX-11 projection come Build Artifact
4. Benchmark ToolJet → conferma esterna della tesi Foundation + X.
   D-015 (due percorsi di costo), D-016 (permissivo/protetto), Q-001 con opzione
   concreta a tre licenze. Nuove voci NX-14 → NX-17.

**Prossimo filo:** `06-PROMPT-Q005.md` — Prompt B con `flash` (freshness indice,
quali sono i 2 file `metadata_changed`), poi Prompt A con `pro` (Q-005:
`applicationType` dichiarato o inferito). Se DICHIARATO → NX-11 resta in zona
sicura. Se INFERITO → Foundation RFC, ci si ferma.

5. Persona dichiarata: **decision-maker non tecnico** (manager, CFO, broker) che
   esplora un dominio guidato da X. Introdotta **Graphic Authority** come terza
   authority. Pattern local-first con ping Redis → chiude AF-003 e AF-004.
   Nuove voci NX-18 → NX-23.

**Prossimo filo (rivisto):** `NX-22` — definire i due tier Builder / Decision-maker.
È la voce che decide tutto il resto: la persona dichiarata non usa CLI né MCP,
quindi il pivot riporta la riga 2 al centro e rende NX-19 (Foundation osserva,
X interpreta) un P0 di sopravvivenza, non un'ottimizzazione.

6. Cultura di costo: rate card DeepSeek verificata su fonti terze, pattern
   **reduction pipeline** formalizzato (450× e non 4×), classi di costo 0–4,
   cinque domande obbligatorie nel PRD.

11. **Il verticale ha una candidata** (NX-30 ristretto): conoscenza pubblica /
    civica / giuridica. È il caso in cui il contenuto è **pubblico ma non
    navigabile** — quindi il meccanismo batte il contenuto, che era la domanda
    di Q-010.
12. **NX-49**: la prima knowledge experience reale sostituisce NX-31 (declassato:
    era comodo e auto-riferito).

> ⚠️ **NX-50 — AZIONE CHE PRECEDE TUTTO.** I documenti strategici `NEXUS-LAB/*`
> risultano salvati sul tenant SharePoint del datore di lavoro
> (`mingiustizia-my.sharepoint.com`). Governance altrui, ambiguità di proprietà,
> contraddizione con D-014. Spostare su supporto personale e verificare le policy.
> Vedi `18-WHY-NEXUS-LAB-EXISTS.md` § 0.

**Sessione 2026-09-14 — ricerca di mercato.**

Scansione Acquire (Asse 1, 7 inserzioni) → ricavo per testa su tre livelli
(traffico $0,03 · prosumer $33 · B2B $189–391); il multiplo misura la
**difendibilità**, non la dimensione; banda obiettivo $11k–50k ARR a 2,7–3,0×.

Seconda passata su pricing e frizioni (Visualping · Particl · Perplexity ·
BayesLab · GoMarble) → **la governance è un asse di prezzo** (read-only vs
read-write + approvazione + audit trail); **premio di verticale 7–70×** misurato
sui listini; NX-19 è prerequisito del modello di pricing, non ottimizzazione;
7 frizioni su 9 già risolte, 2 no (curva di apprendimento, integrazioni).

Nuove voci: NX-63 → NX-72.

**Chiusura sessione 2026-09-13.**

Inventario capacità (`21-...`): 4 verificate · 4 parziali · 4 teoriche ·
**0 esercitate da qualcuno fuori**.

Moat (`23-...`): **4 costruiti** (invariante accumulata, governance eseguibile,
boundary compilato, storia delle falsificazioni) · **2 condizionali** (residuo che
compone, posizione normativa) — e i due condizionali sono gli unici che crescono
senza lavoro.

Infrastruttura (`08-... § 7`): il self-hosting LLM è sbagliato di **10-80×**
(break-even ~400-800M token/mese contro un volume stimato di 10-60M). Il RAG
progettato in D-009 è già gratuito. Il pilota costa **< €25/mese**, probabilmente
< €10. L'hedge per il self-hosting futuro è già in NX-26 e costa zero.

**Le tre mosse che attivano tutto:**
```text
NX-56   pubblicare le 4 analisi in PageData   → attiva M-05, avvia M-04, costo ~zero
NX-57   test di ripetibilità del metodo       → decide prodotto vs performance
NX-30   il verticale                          → attiva M-06, l'unico che il capitale
                                                dei concorrenti non può comprare
```
Nessuna richiede architettura. Due su tre non richiedono codice.

> ⚠️ **AZIONE IMMEDIATA (NX-25):** `deepseek-flash` risulta **ritirato il
> 10 settembre 2026**, sostituito da `deepseek-flash` (V4.1); `deepseek-v4-pro`
> verrebbe instradato a V4.1 Flash dal 14 settembre. Verificare con
> `curl https://api.deepseek.com/v1/models` e aggiornare Roo / Cline / Continue /
> `.clinerules` / Brain. Vedi `08-COST-CULTURE.md` § 0.
> È la validazione dal vivo di NX-04: il catalogo del provider cambia sotto i piedi.
