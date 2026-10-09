# Capacità di Open Nexus — inventario concreto

**Data:** 2026-09-13
**Metodo:** ogni capacità è marcata con l'**evidenza** che la sostiene. Se l'evidenza
non c'è, la capacità è teorica e va dichiarata tale. Nessuna capacità è elencata per
aspirazione.

Legenda:

```text
VERIFICATA    ho letto il file / visto l'output / c'è un test verde
PARZIALE      esiste il componente, manca un pezzo nomato
TEORICA       è in roadmap, non c'è evidenza
```

---

## 1. Capacità verificate

### C-01 · Rappresentare conoscenza navigabile — `VERIFICATA`

```text
evidenza    openfav.vercel.app live: open-nexus/index · library · topics ·
            architecture · runtime · generated-knowledge · manifest6 · assistant
            hub · simple/documentation · simple/about
contratti   PageData → Template → Experience (D-002)
            "PageData is the language of knowledge experiences"
mancante    nulla di strutturale. Manca contenuto reale: oggi le pagine
            documentano Open Nexus, non un dominio esterno.
```

**È la capacità più matura e la meno esercitata.** Esiste un renderer funzionante per
conoscenza navigabile e non c'è ancora conoscenza che non parli di sé.

### C-02 · Eseguire più applicazioni da un solo runtime — `VERIFICATA`

```text
evidenza    5 reference validation nel recap ufficiale:
            Simple (runtime) · Open Nexus (knowledge) · Authentication (session)
            Operations (platform) · System (shared operational)
            src/applications/{auth,open-nexus,simple,core-admin,system}/
contratti   ApplicationDefinition · ApplicationContext · ApplicationBundle
            boundary dichiarato per divieto in types.ts
mancante    la sesta applicazione. Nessuna app è mai stata aggiunta da qualcuno
            che non fosse tu.
```

**Test implicito non superato:** il sistema esegue cinque app, ma tutte scritte dalla
stessa mano con le stesse convenzioni. La prova vera è la sesta.

### C-03 · Governare l'identità visiva — `VERIFICATA`

```text
evidenza    src/core/ui-primitives/ (ADR-0012) · 21 test verdi in 690 ms
            src/core/design-authority/status-tones.ts React-free
            scripts/design/check-style-authority.mjs — regole come dato,
            scope derivato fails-closed, --json, --ci, exception registry
            baseline pubblicata: 554 violazioni in 33 file evolutive
mancante    scadenza nel dato (NX-46) · il ruleset non è consumabile dal gate
            VALIDATE (NX-34) · 554 da azzerare con Boy-Scout rule
```

**È la capacità più avanti rispetto ai benchmark.** Trustable non ha niente di
equivalente; ToolJet accumula componenti senza Primitive Authority.

### C-04 · Classificare e proiettare per semantica — `VERIFICATA`

```text
evidenza    resolveStatusTone: proietta vocabolari noti, stati sconosciuti
            degradano a muted, mai errori
            isExperienceVisible: funzione pura sul tipo, zero I/O
            APPLICATION_TYPE_PROJECTION: Object.freeze, no I/O, no Discovery
            ApplicationType = "user" | "shared" | "workspace" in
            domain-authority/contracts/application-catalog.ts
mancante    il vocabolario status non è consumato da un gate di build (NX-43)
```

### C-05 · Produrre artefatti dal bundle — `PARZIALE`

```text
evidenza    src/applications/bundle-collector.ts
            src/applications/build-manifest.ts
            src/applications/build-report.ts
            regola Build/Runtime documentata e test-enforced
mancante    materializzazione GENERATA invece che manuale (NX-11)
            firma degli artifacts
            esposizione come API (NX-01b)
            → il build esiste, ma non è un prodotto distribuito
```

### C-06 · Sessione condivisa e accesso policy-driven — `PARZIALE`

```text
evidenza    0.6.3-A closed/freeze · 0.6.3-B matrice Guest/Authenticated
            proiezioni Navbar (Primary Navigation vs Session Action)
            return-to-origin via ?next (D-004)
mancante    AF-003 Server Session Recovery
            AF-004 Client Session Reconciliation
            → entrambi chiusi da NX-20 (local-first + ping Redis)
```

### C-07 · Riduzione deterministica prima dell'AI — `PARZIALE`

```text
evidenza    la CLI fa già estrazione tokens (dichiarazione dell'utente)
            progetto: reduction pipeline 450× (08-COST-CULTURE § 2)
            libreria di scraping esistente (URL → header + HTML)
mancante    interfaccia Connector (NX-27)
            content_sha + change detection
            scoring come stadio esplicito
            → la leva di costo principale esiste in embrione, non come componente
```

**Aggiornamento 2026-09-13 — C-07 ha un terzo stadio.**

```text
CONNECTOR   fetch, content_sha, change detection        NX-27
REDUCE      estrazione, scoring, riduzione              C-07 / 450×
SANITIZE    tokenizzazione PII prima del confine LLM    NX-59  ← nuovo
LLM         vede solo token e score                     classe 1
DETOKENIZE  riassociazione in locale, mai in transito
```

Costo e privacy hanno **la stessa forma**: trasformazione deterministica, locale,
classe 0, prima dell'unico confine dove il dato lascia il dispositivo. Si compongono
nello stesso stadio. Vedi `22-PRIVACY-TOKENIZZAZIONE.md` § 2.

### C-08 · Governare le decisioni — `PARZIALE`

```text
evidenza    Decision Log con stati DECISO/PROPOSTO/APERTO/SCARTATO/FALSIFICATO
            ADR numerati (ADR-0012) · PRD numerati (PRD-0013)
            exception registry con reason obbligatorio
            guardrail FACTS/HYPOTHESES/RECOMMENDATIONS usato tutta la sessione
            4 falsificazioni registrate a verbale
mancante    il gate non è eseguibile (NX-53)
            lo stato vive in markdown, non in un record strutturato (NX-58)
            → la governance esiste come PRATICA, non come COMPONENTE
```

---

## 2. Capacità teoriche — nessuna evidenza

### C-09 · Authoring agentico di ApplicationBundle — `TEORICA`

```text
roadmap     0.7.0 — Human / AI / Importer → ApplicationBundle
domanda     "Possiamo produrre questo modello senza conoscere la struttura
             interna del repository?"
evidenza    NESSUNA. Non esiste un bundle prodotto da qualcosa che non sia tu.
dipende da  NX-11 (materializzazione generata) — altrimenti il test di parità
             blocca il primo bundle nuovo
```

**È la capacità su cui si regge tutta la visione, ed è la meno verificata.**

### C-10 · Workflow eseguibile — `TEORICA`

```text
evidenza    nessuna. Esiste un'istanza MANUALE: la tabella di backlog, che è
            un workflow con ID, tipo, priorità, stato, blocco, prossimo passo.
dipende da  NX-02 (workflow.md nel bundle) + NX-03 (gate VALIDATE)
nota        la semantica step è già specificata (da Trustable § 3.4):
            NOT RUN / RUNNING / RUN / FAILED, stato persistente,
            failed-step-ends-run, resume dallo step fermato
```

### C-11 · Distribuzione firmata e tokenizzata — `TEORICA`

```text
evidenza    nessuna. NX-01 (licenza offline), NX-01b (Foundation API),
            NX-14 (nexus-mcp) sono tutti spec, zero codice.
nota        il pattern è validato in produzione da Trustable (lic_ offline)
            e ToolJet (tj_pat_ + deployment URL), quindi il rischio tecnico
            è basso. Il rischio è di priorità, non di fattibilità.
```

### C-12 · Local-first con sincronizzazione — `TEORICA`

```text
evidenza    nessuna. Il recap ufficiale dichiara esplicitamente che NON esistono
            BroadcastChannel né storage listener, e che il multi-tab osservato
            è condivisione server-side su nuova request.
nota        il pattern è tuo (ping Redis → sync, altrimenti locale) e chiuderebbe
            AF-003 e AF-004 senza infrastruttura nuova.
```

---

## 3. La tabella che conta

```text
C-01  conoscenza navigabile              VERIFICATA   esercitata da esterni: NO
C-02  multi-app da un runtime            VERIFICATA   esercitata da esterni: NO
C-03  governance visiva                  VERIFICATA   esercitata da esterni: NO
C-04  proiezione semantica               VERIFICATA   esercitata da esterni: NO
C-05  produzione artefatti               PARZIALE     esercitata da esterni: NO
C-06  sessione e policy                  PARZIALE     esercitata da esterni: NO
C-07  riduzione deterministica           PARZIALE     esercitata da esterni: NO
C-08  governance delle decisioni         PARZIALE     esercitata da esterni: NO
C-09  authoring agentico                 TEORICA      —
C-10  workflow eseguibile                TEORICA      —
C-11  distribuzione firmata              TEORICA      —
C-12  local-first                        TEORICA      —
```

**Risultato: 4 verificate, 4 parziali, 4 teoriche, 0 esercitate da qualcuno fuori.**

È D-039 espresso come inventario di capacità: la colonna 1 è piena, la colonna 2 è
vuota. Non è una critica — è la fotografia, e serve a sapere dove mettere il prossimo
sforzo.

---

## 4. L'applicazione pilota che cade fuori dall'inventario

Non va inventata. Va **assemblata** da capacità già verificate.

### 4.1 Combinazione disponibile oggi

```text
C-01  conoscenza navigabile        → i renderer sono LIVE su openfav.vercel.app
C-07  riduzione deterministica     → scraping + estrazione, la CLI esiste
C-08  governance delle decisioni   → il metodo di questa sessione
C-04  proiezione semantica         → classificazione per meccanismo/tipo di moat
C-03  governance visiva            → matrici e confronti senza deriva
```

Cinque capacità, **tutte verificate o parziali, nessuna teorica**. Il risultato è
esattamente la capacità di analisi di mercato (`20-...`), e il prototipo esiste già:
quattro dossier.

### 4.2 Perché questa e non un'altra

```text
1. non richiede C-09 (authoring agentico), che è teorica
2. non richiede C-11 (distribuzione), che è teorica
3. non richiede un verticale deciso (NX-30): produce il dataset che lo decide
4. usa renderer già live: non c'è UI da costruire
5. ha un payer con spesa già in corso (technical due diligence)
6. il prototipo è scritto: vanno portati in PageData, non prodotti
```

È l'unica combinazione che trasforma capacità verificate in output per qualcuno
fuori **senza attraversare una capacità teorica**.

### 4.3 Il test che la qualifica

`NX-57`: eseguire un'analisi su un oggetto **nuovo** usando solo il metodo scritto,
senza intervento dell'operatore.

```text
se regge    → la capacità è un prodotto
se non regge → è una performance, e il prodotto è un altro
```

Costa un'analisi. È il gate più economico dell'intero backlog e quello che dà più
informazione.

---

## 5. Risposta alla domanda sulla presunzione

> *"non pecco di presunzione a pensarla più ad alto livello?"*

No, e il motivo è preciso.

```text
PRESUNZIONE   credere che il sistema sia più capace di quanto l'evidenza mostri
AMBIZIONE     sapere cosa il sistema può fare, e puntare più in alto
```

La differenza è tutta nell'inventario qui sopra. Finché le capacità sono dichiarate
con la loro evidenza — 4 verificate, 4 parziali, 4 teoriche — pensare in grande non è
presunzione: è leggere la tabella e chiedersi cosa manca.

La presunzione nella sessione c'è stata, e l'ho nominata quando è accaduta:
*"nessuno è come Open Nexus"* (voto 6/10), e le quattro ipotesi di drift affermate
prima dell'evidenza. In entrambi i casi il problema non era il livello di ambizione:
era l'assenza di un comando a supporto.

**Regola:** si può pensare a qualunque altezza, purché ogni affermazione su cosa
esiste citi la sua evidenza. È la stessa regola di `03-WORKFLOW.md`, e vale per la
visione esattamente come vale per un grep.

E sui due livelli in parallelo — *"piccola applicazione pilota e allo stesso tempo i
grandi sistemi"* — va bene, a una condizione:

> il livello alto deve produrre **vincoli** che il pilota deve soddisfare,
> non solo contesto in cui il pilota galleggia.

Qui è successo: C-09/C-10/C-11 sono teoriche, e questo **vincola** il pilota a non
dipendere da loro (§ 4.2 punti 1 e 2). Il livello alto ha fatto il suo lavoro.
Quando non produce vincoli, è fuga.

---

## 6. Cosa manca, in una riga per capacità

```text
C-01  contenuto reale, non auto-descrittivo          → NX-56
C-02  una sesta app scritta da qualcun altro          →NX-22, NX-31
C-03  scadenza nel dato + ruleset per il gate        → NX-46, NX-34
C-04  vocabolario consumato a build, non solo runtime→ NX-43
C-05  materializzazione generata + firma             → NX-11
C-06  local-first                                    → NX-20
C-07  interfaccia Connector + content_sha            → NX-27
C-08  gate eseguibile + record strutturato           → NX-53, NX-58
C-09  tutto                                          → 0.7.0
C-10  tutto                                          → NX-02
C-11  tutto                                          → NX-01, NX-01b, NX-14
C-12  tutto                                          → NX-20
```

---

## 7. Nota sul flusso registrato

> *"la richiesta di registrare il flusso delle discussioni è knowledge preziosa."*

Vero, e non per ragione sentimentale. È la **regola del residuo** (`13-...` § 1.3)
applicata alla sessione:

```text
il metodo (come si analizza)          è visibile, copiabile in un giorno
i documenti (cosa si è concluso)      sono leggibili, copiabili
la storia delle falsificazioni        NON è riproducibile senza viverla
```

Quattro ipotesi del revisore falsificate dai file, una scommessa sbagliata su un
grep, una proposta di authority già esistente, un giudizio dato sul bersaglio
sbagliato e corretto. Questa sequenza è ciò che rende il metodo credibile invece che
solo dichiarato — ed è esattamente l'asset che un clone non può comprare.

È anche la risposta operativa a *"cosa vende Nexus Lab"*: non il metodo, non i
documenti. **La traccia verificabile di un metodo che si è corretto da solo.**

---

*Ultimo aggiornamento: 2026-09-13*
