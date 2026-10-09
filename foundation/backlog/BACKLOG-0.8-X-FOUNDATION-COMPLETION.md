# Foundation 0.8.x Operational Backlog

**Ultimo aggiornamento:** 2026-09-28  
**Programma:** Foundation Completion / Distribution Readiness  
**Baseline di riferimento:** `foundation-baseline-green` → `a2183f5`  
**Stato:** ACTIVE

---

## Obiettivo in una frase

> Dimostrare che una capability Foundation può essere composta come pagina di un
> ApplicationBundle, impacchettata con tutte le proprie dipendenze e distribuita in
> un ambiente pulito senza physical application pages, registrazioni duplicate o
> osservazione del repository da parte del Runtime.

```text
Capability Contract
+
Foundation Reference Implementation
+
Bundle Page
+
Foundation Release
        ↓
Distribution Artifacts
        ↓
Execution
```

---

## Risultato atteso della 0.8.x

```text
Foundation implementa capability riutilizzabili.
ApplicationBundle possiede composizione e identity applicativa.
ApplicationDefinition possiede routing e navigation intent.
PageDefinition possiede identity stabile e requisiti di esperienza.
Build risolve route, template, asset e manifest.
Discovery risolve pagine materializzate.
Runtime esegue PageData senza osservare il repository.
```

---

## Non-obiettivi

La 0.8.x non introduce:

```text
EntityRecord
RelationshipRecord
Semantic Projection
request-time projection
Brain / LLM
visual builder
CRUD semantico
provider registry generico
```

La 0.9 rimane una capability separata. L'integrazione finale avverrà soltanto sul
vero target 0.8 e con un nuovo regression gate.

---

## Invarianti

### Kernel protetto

Salvo Foundation RFC esplicita e approvata, non modificare:

```text
PageController
normalizeToPageData
ApplicationDefinition
ApplicationContext
BundleCollector
DiscoveryService
DiscoveryServiceV2
PageData
```

### Authority

```text
Una dichiarazione canonica per pagina.
Provider, bundle, catalogo e manifest sono proiezioni o composizioni derivate.
Nessuna nuova registrazione manuale duplicata.
```

### Physical pages

```text
Physical infrastructure route       ammessa tramite allowlist
Physical application/content page   retirement target
```

### Distribution

```text
Runtime never observes the repository directly.
.nexus is never an application destination.
```

---

## Regole operative

```text
IN_PROGRESS ≤ 3
P0 aperti   ≤ 2
```

I task futuri che diventeranno release blocker restano `P1` finché sono `BLOCKED`.
Vengono promossi a `P0` uno alla volta quando entrano nel percorso attivo; non si
mantiene una coda nominale di P0.

Stati ammessi:

```text
READY
IN_PROGRESS
BLOCKED
PARKED
DONE
```

Ogni task deve produrre:

```text
comando/file di evidenza
risultato misurato
commit o PR
aggiornamento ADR quando richiesto
```

> Zero risultati senza comando non è un dato.

---

# KPI 0.8.x

| ID | KPI | Target |
|---|---|---:|
| KPI-08-01 | Protected kernel files modificati | `0`, salvo RFC |
| KPI-08-02 | Physical application/content pages non gestite | `0` |
| KPI-08-03 | Registrazioni pagina manualmente duplicate | `0` |
| KPI-08-04 | Pagine canoniche senza ID esplicito | `0` |
| KPI-08-05 | Broken page/navigation references | `0` |
| KPI-08-06 | Remote asset dependencies nel package | `0` |
| KPI-08-07 | Template non dichiarati o non risolti | `0` |
| KPI-08-08 | Repository observations durante Execution | `0` |
| KPI-08-09 | Clean-room distribution validation | `PASS` |
| KPI-08-10 | Stessi input → stesso package hash | `PASS` |
| KPI-08-11 | Capability prive di technical ID/version | `0` |
| KPI-08-12 | Page contract con assi policy sovrapposti | `0` |

---

# NOW

## F08-001 · Audit delle authority e impatto ADR

```text
Release    0.8.x
Stato      IN_PROGRESS
Priorità   P0
Blocca     F08-003, F08-004, F08-005, F08-006
Owner      Foundation
```

### Problema osservato

Le bozze 0.8 formulano decisioni corrette nella direzione, ma alcune claim devono
essere verificate sul repository corrente:

```text
numerazione ADR
Application/Page authority
firma di page()
policy correnti
route resolution
ownership e navigation
WebPageTemplate consumers
physical infrastructure/application pages
```

`ADR-0016` è già riservato al Semantic Entity Projection Model. Nessun nuovo numero
può essere assegnato prima dell'inventario.

### Prossima azione

Eseguire e conservare almeno:

```bash
find docs -type f -iname 'ADR-*' | sort
git grep -n "createApplicationDefinition"
git grep -n "ApplicationDefinition"
git grep -n "ApplicationBundle"
git grep -n "PageMeta"
git grep -n "WebPageTemplate"
git grep -n "PAGES_REGISTRY"
git grep -n "virtualProvider\|virtual-provider"
git grep -n "PUBLIC\|PROTECTED\|LANDING\|HIDDEN"
git grep -n "physical/main/chat\|physical/main/home-pages"
git grep -n "simple/assistant\|core-admin/discovery-pages"
```

### Definition of Done

```text
□ ADR IDs esistenti inventariati
□ ogni claim 0.8 ha comando, file e stato corrente
□ physical routes classificate infrastructure | application | legacy | unknown
□ authority corrente di page identity, ownership, navigation e route documentata
□ access, lifecycle, visibility e page role distinti
□ doppie registrazioni attive identificate
□ Impact Matrix prodotta come report 0.8, non come overview normativa
□ zero modifica al codice applicativo durante l'audit
```

---

## F08-002 · Ritirare le physical application pages PHY-003 / PHY-004

```text
Release    0.8.x
Stato      IN_PROGRESS
Priorità   P0
Blocca     KPI-08-02, F08-005, F08-016
Owner      Foundation
```

### Migrazioni dichiarate

```text
physical/main/chat
→ simple/assistant

physical/main/home-pages
→ core-admin/discovery-pages
```

Le denominazioni e i path effettivi devono essere confermati dal repository e dai
report della migrazione.

### Regola

```text
Il nuovo modello può leggere il legacy durante la migrazione.
Non può generare nuovo legacy.
```

### Prossima azione

Chiudere una migrazione alla volta con un evidence pack che confronti prima/dopo:
route, registry ID, bundle ownership, template, navigation e riferimenti.

### Definition of Done

```text
□ vecchia physical application page rimossa o resa irraggiungibile
□ nessun import attivo dal vecchio modulo
□ nessun registry ID duplicato
□ nessuna route collision
□ alias/redirect legacy deciso esplicitamente
□ replacement page posseduta da un ApplicationBundle
□ capability implementation priva di route/app identity
□ navigation e catalogo derivano dalle authority correnti
□ protected kernel diff = 0
□ contract/full-suite failure set senza regressioni
```

---

## F08-003 · ADR Capability Contract ↔ Bundle Page Boundary

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1
Blocco     F08-001
Owner      Architecture
ADR        ADR-00XX, ID da assegnare dopo audit
```

### Decisione da formalizzare

```text
Capability Contracts definiscono il behaviour surface.
Foundation fornisce la reference implementation.
ApplicationBundle compone capability come esperienze applicative.
Bundle Page possiede page identity e application context.
```

Una capability possiede:

```text
capabilityId
version
contractVersion
compatibility requirements
```

Una capability non possiede:

```text
page registryId
application route
navigation membership
application policy
bundle identity
```

### Definition of Done

```text
□ linguaggio Contracts distinto dall'implementazione Foundation
□ technical identity/version obbligatoria per capability distribuibili
□ Assistant e Discovery mappati come evidenze, non come assunzioni
□ nessun esempio Future Search trattato come capability esistente
□ capability implementation non importa bundle identity
□ almeno un secondo consumer o conformance fixture dimostra la sostituibilità
□ ADR impact sugli ADR esistenti esplicito
□ owner ratification separata dal commit tecnico
```

---

# NEXT — CONTRACT AND AUTHORITY CONVERGENCE

## F08-004 · ADR Application Page Contract ad assi ortogonali

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1
Blocco     F08-001, F08-003
Blocca     F08-005, F08-006, F08-007, F08-013
ADR        ADR-00XY, ID da assegnare dopo audit
```

### Contratto concettuale

```text
Identity             stable page id
Ownership            exactly one owning bundle/application authority
Experience           capability/experience reference
Presentation         template/profile reference
Access               PUBLIC | PROTECTED
Lifecycle            ACTIVE | INACTIVE | DISABLED | MAINTENANCE
Navigation           application-owned reference + visibility/order metadata
Routing              deterministically resolved path or governed override
Distribution         template/assets/capability dependencies
```

### Proibito

```text
implicit page identity
special/legacy page branches nel kernel
HIDDEN come page kind
LANDING come access policy
COMPONENT come page policy
ownership duplicata e divergente
ad hoc routes fuori dal resolver
```

### Definition of Done

```text
□ assi access/lifecycle/visibility/role separati
□ ApplicationDefinition continua a possedere routing/navigation intent
□ Bundle membership e page ownership non possono divergere
□ route derivata distinta da route implicita non governata
□ physical infrastructure route allowlist formalizzata
□ nessuna modifica ai simboli protetti senza Foundation RFC
□ migration mapping per i contratti esistenti
□ test schema e test negativi definiti prima della migrazione massiva
```

---

## F08-005 · Convergere su una sola Content/Page Authority

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1
Blocco     F08-002, F08-004
Blocca     F08-006, F08-012, F08-014
```

### Problema

Il legacy richiede registrazioni manuali in più punti. La 0.8 deve produrre provider,
bundle, catalogo e manifest da una dichiarazione canonica o da riferimenti alla stessa
istanza contrattuale.

### Definition of Done

```text
□ una sola write authority per PageDefinition
□ virtual provider non richiede registrazione manuale duplicata
□ Bundle usa le stesse PageDefinition canoniche o riferimenti validati
□ Catalog e Manifest sono proiezioni build-time
□ duplicate registry ID bloccati deterministicamente
□ source authority indicata nell'Admin/report
□ test legacy dimostra che il nuovo authoring non ricrea il doppio write
```

---

## F08-006 · Esplicitare tutti i Page ID e chiudere i broken reference

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1
Blocco     F08-004, F08-005
```

### Evidenza nota

La baseline 0.7.5.5 aveva classificato broken reference causate da pagine create con
`page()` senza ID esplicito e da una pagina fuori bundle. Il numero corrente deve
essere rimisurato sul target 0.8.

### Definition of Done

```text
□ tutte le PageDefinition canoniche hanno ID esplicito
□ nessun ID critico derivato da title/slugify
□ routing e navigation references risolvono
□ out-of-bundle page rimossa, posseduta o esplicitamente allowlisted
□ broken references = 0
□ collision report = 0
□ nessun mass replace semantico degli ID
```

---

## F08-007 · Separare access, lifecycle, visibility e page role

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1
Blocco     F08-004
```

### Definition of Done

```text
□ PUBLIC/PROTECTED restano nell'asse access
□ landing è relazione dell'Application routing
□ hidden è navigation visibility, non page kind
□ inactive/disabled/maintenance sono lifecycle
□ component non entra nel Page Contract senza evidenza di route/record semantics
□ buildNavigation applica il contratto senza inferenze ad hoc
□ test combinatori coprono almeno PROTECTED+hidden e MAINTENANCE+visible
```

---

## F08-008 · Capability manifest e compatibility requirements

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1
Blocco     F08-003
Blocca     F08-013
```

### Definition of Done

```text
□ ogni capability distribuita ha id e versione
□ dipendenze da Contracts/Foundation Release dichiarate
□ bundle dichiara le capability richieste
□ compatibility gate rifiuta versioni incompatibili
□ manifest non contiene route/navigation appartenenti alla capability
□ Admin può mostrare capability e consumer dai manifest, non dal source scan
```

---

# NEXT — PACKAGING AND DISTRIBUTION

## F08-009 · Derivare il set ESSENTIAL

```text
Release    0.8.x
Stato      READY
Priorità   P1
Dipende    baseline a2183f5
Collega    FE-001, CLI-001
```

### Classificazione

```text
ESSENTIAL
REFERENCE
EXPERIMENTAL
LEGACY
BROKEN
```

### Definition of Done

```text
□ tutte le capability/file necessari al consumer minimale classificati
□ allowlist ESSENTIAL versionata
□ nessuna delete-list usata per costruire il minimal
□ baseline minimale builda e serve una landing
□ Shared Auth inclusa soltanto se richiesta dal routing contract
□ Operations, debug e pilot esclusi salvo dipendenza dimostrata
```

---

## F08-010 · Asset Locality e Asset Resolution

```text
Release    0.8.x
Stato      READY
Priorità   P1
Collega    FE-002
Blocca     F08-012, F08-014
```

### Definition of Done

```text
□ un'unica source authority per ogni asset distribuito
□ nessuna copia manuale public/ ↔ application assets
□ package contiene tutti gli asset richiesti
□ remote asset dependencies = 0
□ asset manifest include path, owner, checksum e consumer
□ asset mancanti bloccano il build
□ stessa resolution in workspace e clean room
```

---

## F08-011 · Template Resolution e Presentation Host boundary

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1
Blocco     F08-003, F08-004
Collega    FE-004, FE-005
Blocca     F08-012
```

### Regola

`WebPageTemplate` è una reference host implementation verificata, non un contratto
universale assunto senza prova.

### Definition of Done

```text
□ template key/version dichiarati nel page/build contract
□ template resolution non dipende da appId branch
□ Experience Profile distinto da Presentation Profile
□ package include host/template necessari
□ undeclared templates = 0
□ template mancante o incompatibile fallisce prima dell'Execution
□ Assistant e Discovery verificati sullo stesso host contract
```

---

## F08-011A · Application-aware Template Asset Resolution

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1 (promuovere a P0 quando entra nel percorso attivo)
Blocco     F08-010, F08-011
Blocca     F08-012
Collega    F08-013, F08-014, FE-004, FE-005
```

### Rischio

Il confine template/asset è un punto di rottura e regressione ad alto impatto.

Senza un contratto esplicito, un template può:

```text
leggere path del repository
hardcodare application ID
usare asset di un'altra applicazione come fallback
funzionare nel workspace e rompersi nel package
trascinare asset legacy dopo il retirement della pagina
rendere il Distribution Manifest incompleto
```

### Decisione da implementare

Il template è application-aware soltanto attraverso un contesto di presentazione e
asset già risolto.

```text
ApplicationBundle
    owns application and brand asset declarations

Presentation Profile
    assigns semantic asset roles/slots

Template Contract
    declares required and optional asset slots

Build Asset Resolver
    resolves references to package-local artifacts

Template
    consumes resolved slots; it never reads bundle internals or repository paths
```

Formula:

```text
ApplicationBundle
+
Presentation Profile
+
Template Requirements
+
Asset Manifest
        ↓
Build-time Asset Resolution
        ↓
Resolved Template Props / existing approved presentation contract
        ↓
Template
```

### Asset ownership classes

```text
TEMPLATE_OWNED
    structural/default assets required by the approved template implementation

APPLICATION_OWNED
    logo, favicon, hero and brand identity declared by the ApplicationBundle

PAGE_CONTENT_OWNED
    content-specific images, evidence previews and page media
```

Ownership classes must not silently fall back into each other.

### Semantic slots

Templates request semantic roles rather than physical source paths.

Examples:

```text
brand.logo
brand.hero
page.cover
navigation.icon
empty-state.illustration
```

Prohibited:

```text
src/applications/<app>/assets/...
public/images/applications/<app>/...
if (appId === ...)
implicit lookup by application directory
fallback to another application's asset
runtime repository scan
```

### Resolution behavior

```text
required slot missing
→ deterministic build/package failure

optional slot missing
→ explicit no-render or approved TEMPLATE_OWNED default

asset hash mismatch
→ compatibility/integrity failure

asset source present but not materialized
→ package failure before Execution
```

No silent fallback may make workspace and clean-room behavior diverge.

### Distribution Manifest requirements

For every resolved template/asset binding the manifest must be able to declare:

```text
template ID/version
asset logical ID
semantic slot
owner type and owner ID
package-relative artifact path
MIME type
byte size
SHA-256
required/optional status
source/build provenance
```

Absolute source paths and Foundation workspace paths are forbidden.

### Owner correction — AI/generated-page templates

The static application-page census is not the complete consumer map.

```text
WowPageTemplate / WowLandingTemplate
    active AI/generated-page consumer reported by owner;
    exact canonical symbol must be verified in source.

AiPageTemplate
    compatibility alias candidate;
    must be traced through generated-page authoring/provider output.
```

These templates are not `ORPHAN` merely because no static page under
`src/applications/**` declares them. Packaging must model AI/generated pages as a gated
capability with explicit template and asset requirements.

### Runtime lookup completeness

Template Lab is a reference/conformance experience for substituting template
implementations while preserving the governing Page, Capability and Presentation
contracts.

```text
capability/responsibility  Template Discovery / Substitutability
page owner                 Operations
current implementation     TemplateLabTemplate
resolution mode            RUNTIME_TEMPLATE_CATALOG
```

The current implementation is a distinct dependency class:

```text
getAllTemplates()
→ user selects a template at runtime
→ getComponent(target)
```

The runtime lookup is intentional. The repository-global lookup and silent fallback
are not. Its dependency closure cannot be inferred from one static
`PageMeta.template`.

The Distribution Manifest must distinguish:

```text
resolutionMode: STATIC_TEMPLATE
resolutionMode: RUNTIME_TEMPLATE_CATALOG
```

For `RUNTIME_TEMPLATE_CATALOG`, the package must declare an explicit, package-scoped
catalog. The runtime may enumerate only that catalog.

```text
Operations/Foundation development package
→ catalog may intentionally contain the complete approved template set

minimal consumer package
→ Template Lab excluded, unless a bounded catalog is explicitly packaged
```

A runtime lookup may not enumerate the repository-global template registry. Unknown or
undeclared selections fail closed; they may not silently render
`VirtualPageTemplate`.

### Regression matrix

At minimum verify:

```text
1. same shared template + two ApplicationBundles + different brand assets
2. required application asset missing → fail closed
3. optional hero missing → explicit approved behavior
4. template-owned default cannot shadow an application-owned required slot
5. asset renamed without manifest update → failure
6. package hash changes when a resolved asset changes
7. workspace render and clean-room render resolve the same logical asset IDs
8. retired page/template pair does not retain orphan application assets
9. no asset from a non-target bundle enters the package
10. AI/generated PageRecord resolves its canonical Wow template and declared assets
11. legacy `AiPageTemplate` alias resolves only through an explicit compatibility rule
12. package without the AI-page capability may exclude the Wow template without
    classifying it globally as orphan
13. unknown generated template key fails closed
14. Template Lab enumerates only the package-scoped catalog
15. one PageData/context is rendered through two approved template implementations while preserving the contract
16. selecting a template outside the declared runtime catalog fails closed
17. no runtime lookup silently falls back to VirtualPageTemplate
18. repository unavailable during Execution
```

### Definition of Done

```text
□ template requirements are explicit and versioned
□ semantic asset slots have one declared authority
□ application-owned assets are declared by ApplicationBundle/Presentation Authority
□ template-owned and page-content-owned assets remain distinguishable
□ build resolves every required asset to a package-local artifact
□ templates contain no appId renderer branch for asset selection
□ templates contain no source-repository asset path
□ no cross-application fallback
□ required missing asset fails before Execution
□ optional fallback is explicit, owned and tested
□ Distribution Manifest contains path/hash/owner/slot metadata
□ two applications consume one host contract with different resolved assets
□ static, dynamic-provider and generated-page template consumers are inventoried
□ canonical Wow template key and AiPageTemplate alias policy are explicit
□ AI-page capability declares its template and asset requirements in the manifest
□ runtime template lookup is represented as an explicit package-scoped catalog
□ Template Lab never enumerates a repository-global registry in a consumer package
□ the same governed context/PageData can be rendered through multiple approved template implementations without contract drift
□ unknown runtime template selections fail closed without silent fallback
□ TemplateLabTemplate remains replaceable and is not confused with capability identity
□ workspace and clean-room resolution are equivalent
□ protected PageData/ApplicationContext contracts remain unchanged unless an approved Foundation RFC is opened
□ negative and clean-room tests cover the regression matrix
```

### Owner invariant

> Applications own assets. Presentation Profiles assign semantic roles. Build resolves
> references. Templates consume resolved slots.

---

## F08-012 · Self-contained ApplicationBundle package

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1
Blocco     F08-005, F08-009, F08-010, F08-011, F08-011A
Blocca     F08-013, F08-014, F08-015
```

### Formula

```text
Foundation Release Artifact
+
ApplicationBundle
+
Resolved Pages
+
Resolved Templates
+
Local Assets
        ↓
Self-contained Application Package
```

### Definition of Done

```text
□ package generato da allowlist e manifest
□ nessun path assoluto verso il workspace Foundation
□ nessuna repository read richiesta in Execution
□ page, capability, template e asset dependency complete
□ package include canonical Distribution Manifest
□ package hash deterministico a parità di input
□ package verificabile senza server di sviluppo
```

---

## F08-013 · Contract Bundle e Distribution Manifest 0.8

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1
Blocco     F08-004, F08-008, F08-012
```

### Contenuto minimo

```text
Foundation release/version
contract schema versions
application identity
page identities e resolved routes
page rendering kind: TEMPLATE | PHYSICAL
capability requirements
presentation/template requirements
template resolution mode: STATIC_TEMPLATE | RUNTIME_TEMPLATE_CATALOG
package-scoped runtime template catalog and allowed aliases
asset checksums
compatibility constraints
build provenance
```

### Definition of Done

```text
□ Semantic Entity 0.9 non esportata accidentalmente
□ manifest canonico viaggia con il package, non soltanto in .nexus
□ schema versionato e validato
□ TEMPLATE and PHYSICAL rendering are represented explicitly; `PHYSICAL` is not treated as a templateRef
□ runtime template catalogs are finite, package-scoped and complete
□ aliases are explicit, versioned and cannot hide a missing canonical template
□ compatibility gate fail-closed
□ manifest diff machine-readable
□ Admin e CLI consumano lo stesso contratto
□ backward compatibility policy dichiarata
```

---

## F08-014 · Clean-room distribution validation

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1
Blocco     F08-012, F08-013
```

### Scenario

```text
workspace Foundation
→ build package
→ copia in directory pulita
→ repository Foundation non disponibile
→ validate
→ build/start
→ GET landing
→ inspect da Admin/CLI
```

### Definition of Done

```text
□ repository Foundation non accessibile durante validate/start
□ landing e almeno una seconda page risolvono
□ Application Catalog deriva dal package
□ asset/template resolution completa
□ representative pages render the declared component, not merely any fallback component
□ Template Lab, when included, enumerates and renders only its manifest-declared catalog
□ PHYSICAL pages/routes are validated through explicit rendering kind and packaged artifact
□ manifest e hash validi
□ Runtime repository observations = 0
□ silent template fallback occurrences = 0
□ stessi input producono lo stesso package hash
□ log e command ledger conservati
```

---

# NEXT — ADMIN AND CLI CANARY

## F08-015 · Admin read model da artifact e manifest

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1
Blocco     F08-008, F08-013
Collega    FE-011
```

### Scope

```text
Applications
→ Application Detail
→ Pages
→ Page Detail
→ Capability / Template / Asset / Health references
```

### Definition of Done

```text
□ Admin non scansiona il repository
□ legge catalogo, manifest e report build-time
□ mostra source authority e provenance
□ nessuna lista applicazioni/pagine locale
□ nessun branch per application ID
□ broken refs e incompatibilità visibili
□ nessun CRUD universale introdotto
```

---

## F08-016 · Application canary per Authoring/CLI V1

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1
Blocco     F08-005, F08-012, F08-014
Collega    CLI-008, CLI-009, CLI-011, CLI-012, CLI-019
```

### Scopo

Trasformare il workflow valido di `APPLICATION-GUIDE-01` in una prova eseguibile:

```text
inspect
→ Plan
→ apply in staging
→ verify
→ package
→ clean-room
→ CommandResult
```

La canary 0.8 non dipende dal Semantic Entity layer 0.9.

### Regole

```text
.nexus = CLI workspace
.nexus ≠ application destination
nessuna nuova physical application page
nessuna doppia registrazione
ID pagina espliciti
```

### Definition of Done

```text
□ ApplicationAuthoringSpec minimo validato
□ dry-run produce piano senza scrivere application-dest
□ LocalMaterializer scrive in staging atomico
□ generated application usa una sola Page Authority
□ output package passa F08-014
□ cancellare .nexus non invalida l'applicazione
□ copiare application-dest senza .nexus mantiene manifest ed esecuzione
□ protected kernel diff = 0
```

---

## F08-017 · Frontend Admin Applications → Pages → Details

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1
Blocco     F08-015
Collega    FE-011, FE-012
```

### Definition of Done

```text
□ frontend consuma il read model F08-015
□ Application Detail mostra release, contract, capability e health
□ Page Detail separa access/lifecycle/navigation/presentation
□ template change è proposal/authoring flow, mai Runtime mutation
□ tastiera, focus e responsive verificati sulle superfici di riferimento
```

---

# RELEASE GATE

## F08-018 · Legacy compatibility e retirement ledger

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P1
Blocco     F08-002, F08-005, F08-006
```

### Definition of Done

```text
□ ogni legacy page ha stato RETIRED | ADAPTED | ALLOWLISTED
□ route alias/redirect hanno owner e scadenza
□ nessun consumer dipende da physical application pages ritirate
□ legacy adapter legge ma non genera il vecchio formato
□ retirement ledger collegato a commit e test
```

---

## F08-019A · Live Distribution Implementation Closure

```text
Release    0.8.x
Stato      IN_PROGRESS
Priorità   P0
Fonte      F08-CODE-REALITY-CHECK → PARTIAL_IMPLEMENTATION
Blocca     F08-019B
```

### Obiettivo

Chiudere esclusivamente i tre gap di implementazione osservati:

```text
1. producer senza CLI live
2. toolchain senza command contract npm
3. frontend F08-017 non montato
```

Golden path richiesto:

```text
live ApplicationBundle / build model
→ manifest.json + discovery.json
→ validate
→ materialize package
→ clean-room
→ Admin read model
→ Operations frontend route
```

### Scope mutante autorizzato

```text
live distribution producer CLI
package.json command entrypoints, senza nuove dipendenze
live E2E distribution test
mount del read model frontend in una superficie Operations approvata
scratch-file cleanup verificata
```

### Vietato

```text
nuova capability
nuovo audit architetturale
fixture manifest come input del live E2E
hardcoded output path
lockfile change
protected-kernel change
version bump
tag release
0.9 integration
unrelated refactor
```

### Commit candidati

```text
feat(distribution): add live application manifest producer
chore(distribution): expose package and clean-room commands
test(distribution): cover live bundle to clean-room pipeline
feat(operations): mount distribution admin read model
```

### Definition of Done

```text
□ producer eseguibile fuori da Vitest
□ producer consuma ApplicationBundle/build model reali, non fixture test
□ application ID e output directory sono input espliciti
□ manifest.json e discovery.json scritti su disco
□ command contract dichiarato in package.json
□ composed command produce → validate → materialize → integrity
□ nessuna nuova dipendenza e nessun lockfile diff
□ package generato dal bundle reale
□ Foundation repository non disponibile durante clean-room
□ landing e seconda pagina risolvono
□ componente template realmente renderizzato = manifest declaration
□ asset locali e hash validi
□ Template Lab usa soltanto catalogo package-scoped quando incluso
□ PHYSICAL usa rendering kind e route artifact, non template lookup
□ generated/AI template capability risolve canonical key/alias dichiarati
□ Admin read model consuma il package reale
□ frontend admin montato in una route Operations reale
□ production route non usa fixture hardcoded
□ protected kernel diff = 0
□ command ledger, package tree e route matrix conservati
```

### Verdict

```text
READY_FOR_F08_019B
BLOCKED_LIVE_PRODUCER
BLOCKED_COMMAND_CONTRACT
BLOCKED_PACKAGE
BLOCKED_CLEAN_ROOM
BLOCKED_FRONTEND_WIRING
```

---

## F08-019B · Foundation 0.8.x Final Conformance and Release Report

```text
Release    0.8.x
Stato      BLOCKED
Priorità   P0 quando F08-019A è DONE
Blocco     F08-019A
```

### Gate finale

```text
□ KPI-08-01 … KPI-08-12 misurati sul target finale
□ Ratification Ledger backlog → evidence → outcome → KPI completo
□ contract + authority suite senza regressioni
□ full-suite failure set confrontato con baseline ufficiale
□ public TypeScript surface = 0 errori
□ protected-kernel diff verificato
□ live producer/package command riproducibile
□ package filesystem e Distribution Manifest conformi
□ clean-room PASS dal bundle reale
□ rendered-template identity verificata, non soltanto HTTP 200
□ Legacy Expiry Gate = [] con asOf esplicito
□ governance/test artifacts esclusi dal consumer package
□ Application Catalog/Admin leggono package artifact reali
□ semantic-entity 0.9 assente dalla superficie 0.8
□ GAP-2 PHYSICAL e GAP-3 undefined rendering classificati PASS/OBSERVATION/BLOCKER con evidenza
□ command ledger e release report conservati
□ owner approval separata dal commit tecnico
```

### Verdict

```text
READY_FOR_OWNER_RELEASE_DECISION
PASS_WITH_OBSERVATIONS
BLOCKED_KPI
BLOCKED_RATIFICATION
BLOCKED_CONTRACT_REGRESSION
BLOCKED_TYPE_REGRESSION
BLOCKED_PROTECTED_DIFF
BLOCKED_MANIFEST_INCOMPLETE
BLOCKED_PACKAGE_FILESYSTEM
BLOCKED_CLEAN_ROOM
BLOCKED_LEGACY_GOVERNANCE
```

---

# PARKED

## F08-020 · Integrazione Semantic Entity 0.9 sul target 0.8

```text
Stato      PARKED
Priorità   P1
Blocco     release target 0.8 disponibile
```

Quando la 0.8 muove il target:

```text
rebase feature/0.9 sul vero target 0.8
→ semantic suite
→ full regression comparison
→ distribution surface diff
→ semantic-proof canary
→ owner merge decision
```

Non anticipare Entity/Relationship/Semantic Projection dentro gli ADR 0.8.

---

# DONE

```text
— nessuna voce chiusa in questo backlog 0.8.x al 2026-09-28 —
```
