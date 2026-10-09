# CLI Operational Backlog

**Ultimo aggiornamento:** 2026-09-20
**Obiettivo:** generare una piattaforma Open Nexus minimale, funzionante e validata.
**Regole operative:** le stesse di `frontend/backlog/README.md`.

---

## Tesi

```text
FE-001 classifica la Foundation corrente
        ↓
set ESSENTIAL
        ↓
baseline minima versionata
        ↓
opnx init <project>
        ↓
Foundation minimale funzionante
        ↓
opnx create app <app>
```

La CLI non deve conoscere la struttura interna del repository. Deve consumare un
artefatto/versione e produrre un progetto conforme ai contratti.

> **Foundation produce, Execution esegue. La CLI materializza il punto di partenza.**

---

## NOW

### CLI-001 · Generare la baseline `minimal` dal set ESSENTIAL

```text
Release    0.8 experiment
Stato      BLOCKED
Priorità   P0
Blocco     FE-001
```

**Problema**

La Foundation corrente contiene applicazioni, reference validation, esperimenti,
legacy e superfici operative. La CLI non deve distribuirli tutti.

**Regola**

```text
SBAGLIATO   copia il repository completo → cancella ciò che non serve
GIUSTO      allowlist ESSENTIAL → genera un template minimo
```

La delete-list dimentica sempre qualcosa. L’allowlist rende ogni dipendenza visibile.

**Contenuto candidato della baseline**

```text
· Runtime e route dinamica
· contratti ApplicationDefinition / ApplicationContext / PageData
· BundleCollector e build artifact necessari
· Discovery minimo sugli artifact
· una Application Authority
· una Content Authority
· Design / Theme / Primitive / Presentation minime
· una applicazione `starter`
· una pagina landing
· un template semantico
· test di contratto indispensabili
· Shared Auth **se richiesto dai contratti correnti**
  (`ApplicationRouting.login` oggi è obbligatorio: l'audit CLI-008 deve stabilire
  se il minimal include Auth o se esiste un default valido senza Auth)
· nessun Redis, AI, Operations, System, debug, catalog console non necessario
```

L’elenco finale viene da FE-001, non da questo documento.

**Artefatti**

```text
templates/minimal/template.manifest.json   allowlist e versioni
templates/minimal/                         file applicativi/configurazione
minimal.lock                               foundation version + schema versions
```

**Definition of Done**

```text
□ baseline prodotta esclusivamente da file/capability ESSENTIAL
□ nessun file REFERENCE/EXPERIMENTAL/LEGACY incluso
□ progetto parte senza Redis, database, provider AI o credenziali
□ una landing è raggiungibile
□ `opnx validate` passa
□ build verde
□ output deterministico: stessi input → stessi file e hash
□ ogni dipendenza implicita mancante diventa errore esplicito, non copia silenziosa
```

---

### CLI-002 · `opnx init <project> --template minimal`

```text
Release    0.8 experiment
Stato      BLOCKED
Priorità   P0
Blocco     CLI-001
```

**UX desiderata**

```bash
opnx init my-project --template minimal
cd my-project
npm install
npm run dev
```

Output:

```text
✓ Foundation <version>
✓ Contracts <schema versions>
✓ Application "main"
✓ Landing page
✓ Validation passed

Next:
  npm run dev
  opnx create app <id>
```

**Principio “mostra, non chiedere”**

L’unico input obbligatorio è il nome del progetto.

La CLI non chiede:

```text
quale auth?
quale database?
quale provider AI?
quale Redis?
quale template CSS?
```

Applica default governati. Le capability opzionali si aggiungeranno con comandi
espliciti futuri; non durante `init`.

**Definition of Done**

```text
□ nome progetto validato e normalizzato deterministicamente
□ nessuna domanda interattiva tecnica
□ nessun secret generato o richiesto
□ output indipendente dal repository sorgente
□ `foundationVersion` e schema version registrati nel lock
□ una seconda esecuzione su directory non vuota rifiuta senza sovrascrivere
□ errori descrivono la correzione, non soltanto il fallimento
```

---

### CLI-003 · Test end-to-end dello scaffold

```text
Release    0.8 experiment
Stato      BLOCKED
Priorità   P0
Blocco     CLI-002
```

**Test in CI**

```text
temp directory
  → opnx init test-project --template minimal
  → install da workspace/cache
  → opnx validate
  → build
  → avvio server
  → GET landing = 200
  → Application Catalog contiene "main"
  → stop
```

**Definition of Done**

```text
□ test eseguito da directory esterna al repository Foundation
□ nessun path assoluto o import verso il repository sorgente
□ catalogo prodotto dal bundle generato, non hardcoded
□ zero modifica a PageController, normalizeToPageData, ApplicationDefinition,
  ApplicationContext, BundleCollector, DiscoveryService e PageData
□ snapshot della struttura file sotto test
□ tempo totale e dimensione output registrati
```

---

## AUTHORING TRACK — sviluppo parallelo

Questa traccia può avanzare mentre FE-001 prepara la baseline minima.

### CLI-008 · Audit read-only della catena Application / Page

```text
Release    0.8 experiment
Stato      READY
Priorità   P0
Blocca     CLI-009, CLI-010, CLI-011, CLI-012, CLI-013
Prompt     PROMPT-AUTHORING-AUDIT.md
```

**Domanda**

Quali valori devono essere forniti dall'utente, quali sono derivati, quali hanno un
default e quali file vengono materializzati per creare:

```text
Application → Pages → Registry → Bundle → Catalog → Runtime
```

**Definition of Done**

```text
□ inventario completo dei campi Application e Page
□ ogni campo classificato USER_INPUT | DERIVED | DEFAULT | AUTHORITY_OWNED
□ mappa esatta delle write target attuali
□ distinzione fra authoring config/bundle e AI page persistence
□ catena `generateAiPage` ricostruita senza assumerne la compatibilità
□ identificati default che rendono possibile "mostra, non chiedere"
□ stabilito se il minimal richiede Shared Auth
□ zero modifiche al repository
```

---

### CLI-009 · Contratti di Authoring unificati

```text
Release    0.8 experiment
Stato      BLOCKED
Priorità   P1
Blocco     CLI-008
```

Contratti candidati:

```text
ApplicationAuthoringSpec
PageAuthoringSpec
PageContentDraft
AuthoringResult
ValidationFinding
```

**Principio**

```text
utente / CLI / frontend / AI / importer
  → producono la stessa spec
  → non scrivono file direttamente
```

**Definition of Done**

```text
□ spec indipendenti dai path del repository
□ ID, registry ID, routing e navigation derivati dove possibile
□ campi tecnici non richiesti all'utente se esiste un default governato
□ schema versionato
□ nessun import da React, Astro, route o provider AI
```

---

### CLI-010 · Placeholder Content Provider deterministico

```text
Release    0.8 experiment
Stato      BLOCKED
Priorità   P1
Blocco     CLI-009
```

Il primo provider di contenuto non è AI:

```text
PlaceholderContentProvider
  → produce PageContentDraft minimo e valido
  → output deterministico
  → nessun token, nessuna rete
```

Il placeholder non può essere generico per ogni template. Serve un registry:

```text
template key
  → scaffold contract
  → placeholder minimo compatibile
```

Iniziare con **un solo template semantico**. Il secondo template giustifica
l'astrazione.

**Definition of Done**

```text
□ stessi input → stesso PageContentDraft
□ nessun lorem ipsum obbligatorio: titolo derivato + blocchi vuoti/espliciti
□ output passa il validator del template
□ nessun provider AI importato
□ test snapshot del draft
```

---

### CLI-011 · Application/Page Builder deterministico

```text
Release    0.8 experiment
Stato      BLOCKED
Priorità   P1
Blocco     CLI-009, CLI-010
```

```text
ApplicationAuthoringSpec
+ PageAuthoringSpec[]
+ ContentProvider
        ↓
ApplicationBundle valido
+ PageRecord validi
+ build input
```

**Regola**

Il builder possiede le regole di creazione. Non possiede il filesystem.

**Definition of Done**

```text
□ deriva namespace, registry ID, landing, navigation e default consentiti
□ rifiuta collisioni prima della scrittura
□ produce un risultato in memoria
□ Foundation contracts invariati
□ nessuna conoscenza dei path `src/config/...` o `src/applications/...`
```

---

### CLI-012 · Materializer locale

```text
Release    0.8 experiment
Stato      BLOCKED
Priorità   P1
Blocco     CLI-011
```

Adapter che traduce `AuthoringResult` nella struttura fisica corrente.

```text
Builder      conosce i contratti
Materializer conosce i path
CLI          orchestra
```

**Definition of Done**

```text
□ scrittura atomica in staging directory
□ preview/dry-run del diff prima del commit
□ rollback se una write fallisce
□ nessuna sovrascrittura senza `--force`
□ test golden sulla struttura generata
```

---

### CLI-013 · Adapter CLI e frontend

```text
Release    0.8 experiment
Stato      BLOCKED
Priorità   P1
Blocco     CLI-012
```

```text
CLI       opnx create app / create page → local materializer
Frontend  form minimale → stessa spec → preview/download o Authoring API
AI        propone PageContentDraft → stesso validator → stesso builder
```

**Vincolo**

Il frontend non scrive il repository. Produce una spec e la invia a un adapter
autorizzato oppure scarica un bundle.

---

### CLI-014 · AI Content Provider — dopo il placeholder

```text
Release    post-0.8 deterministic pilot
Stato      PARKED
Priorità   P2
Blocco     CLI-010, CLI-011, primo ciclo deterministico verde
```

L'AI non genera file di configurazione. Produce soltanto una proposta
`PageContentDraft`, marcata `PROPOSED`, che passa dallo stesso gate del placeholder.

```text
prompt
  → proposta contenuto
  → validate
  → preview
  → approvazione
  → builder deterministico
```

---

## NEXT

### CLI-004 · `opnx create app <id>`

```text
Stato      BLOCKED
Priorità   P1
Blocco     CLI-003
```

Genera soltanto il layer applicativo dentro una Foundation inizializzata:

```text
src/applications/<id>/package.ts
src/applications/<id>/pages/
src/applications/<id>/assets/
presentation.manifest.ts
Application Definition
Content/Page Registry
```

La lista esatta deve derivare dai contratti correnti, non essere duplicata nella CLI.

**DoD principale:** la nuova app appare nel catalogo senza modificare una projection
manuale. Questo esercita NX-11 (materializzazione generata).

---

### CLI-005 · `opnx validate`

```text
Stato      READY
Priorità   P1
```

Può essere implementato prima di `create app` perché formalizza il gate.

Controlli iniziali:

```text
· ApplicationDefinition completa
· registry ID coerenti
· template key risolvibili
· source authority unica
· Presentation Manifest compatibile
· nessun riferimento rotto
· schema/ruleset version supportati
```

Output umano + `--json`. Exit code non-zero sui blocchi.

---

### CLI-006 · `opnx doctor`

```text
Stato      PARKED
Priorità   P2
```

Diagnostica ambiente e compatibilità; non corregge automaticamente.

---

### CLI-007 · `opnx upgrade`

```text
Stato      PARKED
Priorità   P2
Blocco     due versioni distribuibili reali
```

Non progettare il motore di upgrade prima di avere due release da migrare.

---

### CLI-015 · Audit del modello `source → destination` della CLI legacy 2.0.3

```text
Release    preparazione 0.8
Stato      IN_PROGRESS
Priorità   P1
Fonte      esecuzione reale CLI legacy 2.0.3
```

**Fatti osservati**

| Comando | Responsabilità osservata | Stato |
|---|---|---|
| `--version` | versione CLI | ✅ 2.0.3 |
| `--help` | elenco comandi | ✅ |
| `validate` | valida configurazione Design/Token | ✅ |
| `setup` | wizard interattivo | non testato |
| `seed-templates` | aggiunge marker `@inject` a `tokens.ts` e `globals.css` | ✅ 59 marker |
| `migrate --dry-run` | simula idratazione/migrazione token | ✅ 2 modifiche simulate |
| `migrate` | applica idratazione token | ✅ 2 valori · 62 warning template incompleti |

**Correzione architetturale**

Il modello legacy è:

```text
Design Source
→ injection points
→ token/template migration plan
→ hydration
→ tokens.ts + globals.css
```

Non è ancora dimostrato che sia generalizzabile a:

```text
project source → arbitrary destination
```

Quindi `source → destination → plan → apply → verify` resta una **ipotesi di
generalizzazione**, da estrarre soltanto dopo l'audit.

**Capability Inventory — osservato sul codice legacy**

| Capability | Classificazione | Nota |
|---|---|---|
| `setup` v2 | ADAPT | wizard valido, schema config legacy |
| `validate-config` | KEEP | validazione Zod riutilizzabile |
| `extractTokensFromCss` | ADAPT | core valido, output legacy |
| `seed-templates` | REPLACE | concetto `@inject` valido, path hardcoded |
| `migrate/hydrate` | REPLACE | pipeline valida, implementazione V4→V6 |
| `injectValue` | KEEP* | comportamento chirurgico; implementazione da isolare/testare |
| `toPureHsl` | KEEP | funzione pura |
| `observe` v3 | KEEP | observer con checksum |
| `interpret` v3 | UNKNOWN | stub, dipende da AI |
| `define` v3 | UNKNOWN | stub, dipende da KnowledgeModel |
| `build` v3 | UNKNOWN | stub |

`KEEP` significa prima di tutto **preservare comportamento e test**. Non autorizza
la copia cieca dell'implementazione. In particolare `injectValue` vive vicino a una
regex segnalata come fragile.

**Pipeline legacy dimostrata**

```text
SOURCE CSS V3/V4
→ extract regex `--name: value`
→ classificazione pattern-based
→ IR { colors, spacing, typography, custom }
→ hydrateTokens
→ DESTINATION V6: tokens.ts + globals.css
```

Questo prova `source → IR → destination` nel dominio Design. Non prova ancora che
lo stesso IR sia valido per Project/Application/Page.

**Fragilità osservate**

```text
seed-templates.js:21-22   path hardcoded
injector-engine.js:14     regex con escaping fragile
css-extractor.js:45-54    classificazione permissiva / falsi positivi
config-loader.js:7-13     V4/V6 hardcoded
```

**Prossima azione**

Completare ciò che l'inventario non prova ancora:

```text
1. classificare per causa i 62 warning
2. verificare idempotenza di seed-templates e migrate
3. congelare una fixture legacy con expected output
4. verificare consumer reali di setup/validate
5. leggere gli stub v3 prima di assegnare ownership
```

Classificazione:

```text
KEEP       comportamento valido nel dominio Design Migration
ADAPT      valido, ma accoppiato a path/marker legacy
EXTRACT    algoritmo generale dimostrato da almeno due comandi
REPLACE    implementazione insicura o fragile
DROP       nessun consumer / residuo
UNKNOWN    manca evidenza
```

**Definition of Done**

```text
□ `validate`, `setup`, `seed-templates`, `migrate` mappati file:riga
□ chiarito cosa significano realmente source e destination nel legacy
□ i 59 marker inventariati: autorità, consumer e motivo
□ i 62 warning classificati per causa, non soltanto contati
□ verificata idempotenza di seed e migrate
□ nessuna generalizzazione approvata con un solo caso d'uso
□ fixture di un progetto legacy preservata
```

---

### CLI-018 · CLI V1 — Domain Orchestrator aware

```text
Release    CLI V1 architecture
Stato      READY
Priorità   P1
Dipende    audit minimo CLI-015, senza attendere la scansione completa
```

**Definizione**

CLI V1 è la nuova architettura di orchestrazione. Non è un downgrade della versione
2.0.3 e non implica, da sola, il numero SemVer del package distribuito.

```text
CLI V1
  → riconosce progetto e Foundation
  → carica Contract Bundle e lock
  → seleziona il dominio
  → chiede al dominio un Plan
  → mostra il Plan
  → Apply
  → Verify
```

La CLI non contiene le regole dei domini. Le orchestra.

### Domini iniziali

```text
DesignDomain
  validate · setup · seed-templates · migrate
  prima implementazione: LegacyDesignAdapter

ProjectDomain
  init · validate · doctor

ApplicationDomain
  create · inspect

PageDomain
  create · inspect · template proposal
```

### Lifecycle comune

```text
inspect(context, input)
  → Plan

apply(context, plan)
  → CommandResult

verify(context, result)
  → ValidationFindings
```

`source/destination` può avere modelli diversi per dominio. La CLI condivide il
lifecycle, non forza tutti i domini dentro la stessa struttura interna.

### Legacy Design Adapter

La prima CLI V1 non riscrive il motore 2.0.3.

```text
opnx design validate
opnx design setup
opnx design seed
opnx design migrate
        ↓
LegacyDesignAdapter
        ↓
logica legacy funzionante
```

L’adapter normalizza:

```text
output testuale legacy
→ CommandResult

warning legacy
→ ValidationFinding

modifica legacy
→ PlannedChange / AppliedChange
```

### Definition of Done

```text
□ registry dei domini esplicito
□ ogni comando appartiene a un solo dominio
□ Context costruito una volta e passato ai domain handler
□ tutti i comandi restituiscono CommandResult strutturato
□ dry-run disponibile attraverso Plan, non implementato separatamente per comando
□ DesignDomain usa la logica legacy tramite adapter, senza copia
□ Project/Application/Page non importano codice Design legacy
□ la CLI parte e mostra help anche senza un progetto Open Nexus
```

---

### CLI-019 · ProjectContext aware

```text
Release    CLI V1 architecture
Stato      IN_PROGRESS
Priorità   P1
```

La nuova CLI deve sapere **chi è il progetto, quale stack usa e con quale Foundation
sta parlando** prima di eseguire un comando. Questa è `Observe 0 — Identity`, la
prima capability concreta della CLI V1.

```ts
interface ProjectIdentity {
  name: string
  projectKind:
    | 'foundation-workspace'
    | 'consumer-project'
    | 'legacy-project'
    | 'migration-workspace'
    | 'unknown'

  stack: {
    framework?: 'astro' | 'other'
    ui?: 'react' | 'other'
    language?: 'typescript' | 'javascript' | 'other'
    packageManager?: 'npm' | 'pnpm' | 'yarn' | 'other'
  }

  capabilities: string[]
  evidence: IdentityEvidence[]
}

ProjectContext
  identity: ProjectIdentity
  project_root
  environment
  foundation_version
  contract_bundle_version
  authoring_schema_version
  page_data_schema_version
  design_ruleset_version
  template_catalog_version
  application_catalog_ref
  record_store_ref
```

`projectKind` è una classificazione primaria; `capabilities` resta multi-valore. Un
workspace Foundation può contenere applicazioni senza diventare `consumer-project`.

### Discovery del contesto

Ordine di authority:

```text
1. localizza root del progetto
2. manifest / opnx.lock espliciti                 DECLARED, massima authority
3. package metadata e dependency dichiarate      DERIVED
4. file-segnale (astro.config, tsconfig, .nexus)  OBSERVED
5. heuristic fallback                            solo senza segnali forti
6. unknown                                       risultato valido, mai guessing
```

Ogni campo di Identity conserva le evidenze che lo hanno prodotto. Lo stack rilevato
non dimostra da solo che il progetto sia Open Nexus.

`source`, `destination`, `resolver` e `workspace` appartengono al `CommandContext`
legacy/migration, non alla Project Identity.

### Regole

```text
· un comando dichiara quali capability richiede
· se una capability manca: errore esplicito, non fallback
· un comando Design legacy può funzionare anche senza opnx.lock,
  attraverso LegacyProjectContext
· nessun domain handler ricalcola il contesto
· nessun provider AI viene scelto durante la costruzione del context
```

### Definition of Done

```text
□ stesso progetto → stesso ProjectContext serializzato
□ `opnx context --json` espone identity + evidenze
□ `opnx doctor` usa ProjectContext e aggiunge health check; non duplica detection
□ progetto legacy classificato senza fingere che sia Open Nexus corrente
□ incompatibilità Foundation/CLI rilevata prima del Plan
□ unknown non viene forzato in una categoria
□ source/destination separati dalla Project Identity
□ fixture: nessun progetto · legacy token project · Foundation · consumer project · migration workspace
```

---

### CLI-020 · Legacy Design Domain — adapter e hardening

```text
Release    CLI V1
Stato      BLOCKED
Priorità   P1
Blocco     CLI-015, CLI-018
```

**Scopo**

Montare la logica Design legacy dietro `LegacyDesignAdapter` senza riscriverla tutta,
poi sostituire soltanto i punti fragili.

```text
Legacy CSS
→ Observer + checksum                 KEEP
→ Token extraction                   ADAPT
→ DesignMigrationIR                  formalizzare
→ schema-driven template resolver    REPLACE seed hardcoded
→ Plan                               dry-run
→ Apply                              injection idempotente
→ Verify                             warning/error strutturati
```

**Decisioni implementative**

```text
· `TagManager` è un modulo/funzioni pure, non obbligatoriamente una classe
· niente factory astratta finché esiste un solo resolver: schema-driven function
  prima, factory soltanto al secondo formato reale
· JSON Schema deve restare language-neutral; `src/shared/types` può generarlo,
  non sostituirlo con soli type TypeScript
· i marker `@inject` restano supporto di MIGRAZIONE, non source authority futura
```

**Definition of Done**

```text
□ output LegacyDesignAdapter equivalente alla CLI 2.0.3 sulla fixture
□ seed e migrate idempotenti
□ path ricavati dal context/schema, non hardcoded
□ classificazione token con regole testate e falsi positivi fixture
□ IR versionato e serializzabile
□ 62 warning trasformati in findings con rule_id e severity
□ nessun import legacy da Project/Application/Page Domain
```

---

### CLI-016 · Contract Bundle e Compatibility Gate

```text
Release    0.8 architecture
Stato      BLOCKED
Priorità   P1
Blocco     CLI-008, CLI-015
```

Foundation deve produrre un artefatto versionato consumabile dalle controparti.
CLI e Brain non lavorano direttamente contro `main` o contro path interni.

```text
foundation-contracts.json
application-authoring.schema.json
page-authoring.schema.json
page-data.schema.json
template-catalog.json
presentation-profiles.json
design-ruleset.json
minimal-template.manifest.json
```

Version vector iniziale:

```text
foundationVersion
authoringSchemaVersion
pageDataSchemaVersion
templateCatalogVersion
presentationSchemaVersion
designRulesetVersion
```

Salvato nel progetto generato:

```text
opnx.lock
```

**Compatibility gate**

```text
CLI legge opnx.lock
→ carica il Contract Bundle target
→ verifica la matrice di compatibilità
→ se incompatibile: FAIL LOUD, mai fallback silenzioso
```

**Definition of Done**

```text
□ Foundation tagga e pubblica Contract Bundle immutabile
□ CLI pinna una versione/tag, mai il branch mobile
□ Brain dichiara le versioni schema supportate in `get_server_info`
□ progetto generato registra il version vector
□ CI testa Foundation current contro CLI stable e CLI next
□ incompatibilità produce errore con percorso di migrazione
```

---

### CLI-017 · Integration Matrix dei tre cantieri

```text
Release    continuo
Stato      BLOCKED
Priorità   P1
Blocco     CLI-016
```

```text
                   Foundation stable   Foundation next
CLI stable         obbligatorio ✓      diagnostico
CLI next           obbligatorio ✓      obbligatorio ✓
Brain stable       schema supportato    non assume compatibilità
Brain next         schema supportato    test contract-first
```

Ogni release Foundation esegue:

```text
1. export Contract Bundle
2. scaffold minimal con CLI next
3. validate + build + smoke
4. test Brain sui JSON Schema pubblicati
```

Nessuna controparte deve scoprire la rottura dopo il merge.

---

## Fuori perimetro 0.8

```text
· scelta provider AI
· auth interattiva
· database provisioning
· deploy automatico
· marketplace di template
· visual builder
· generazione via prompt
· aggiornamento automatico del kernel
```

Queste capacità possono arrivare dopo. Inserirle in `init` ricrea esattamente il
vibe coding tedioso che Open Nexus vuole evitare.

---

## Decisione architetturale da non anticipare

Per il primo esperimento la baseline può essere un template versionato. Prima della
1.0 va deciso se la distribuzione finale sarà:

```text
A. template repo versionato
B. package Foundation + codice applicativo generato
C. engine chiuso/binario + contratti pubblici
D. Foundation API remota + Execution shell locale
```

`opnx init` deve nascondere questa scelta all’utente e registrare abbastanza metadata
da permettere di cambiarla in futuro.

---

## Punto di verità

La CLI ha successo quando:

> **un progetto generato fuori dal repository parte, valida e costruisce una nuova
> applicazione senza conoscere la struttura interna e senza toccare il kernel.**

Quello è il passaggio da Foundation interna a prodotto distribuibile.
