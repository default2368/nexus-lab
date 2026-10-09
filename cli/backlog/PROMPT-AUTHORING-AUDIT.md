# Prompt MCP-ready — Audit Application/Page Authoring Chain

**Modello consigliato:** `deepseek-flash`
**Modalità:** Plan / read-only
**Repository:** `open-nexus-foundation`, non il vecchio `openfav-codebase-V1`

---

```text
Questa è una Architecture & Authoring Review READ-ONLY.
NON modificare file. NON creare file. Output = report.

OBIETTIVO

Ricostruire la catena completa con cui Open Nexus definisce e materializza:

Application
  → ApplicationDefinition
  → ApplicationBundle / package
  → Pages / PageRecord
  → Page Registry
  → BundleCollector / Catalog / Build Artifacts
  → Runtime

Scopo finale: progettare UN SOLO authoring layer consumabile da:

Human | CLI | Frontend | AI | Importer
  → ApplicationAuthoringSpec / PageAuthoringSpec
  → builder deterministico
  → materializer

NON progettare ancora il builder. Prima estrarre i fatti.

==================================================
FASE 0 — INDEX AUTHORITY
==================================================

1. list_projects
2. index_status sul progetto `open-nexus-foundation`
3. Riportare:
   - project identifier
   - path
   - generation
   - status
   - warnings
   - parse_partial
4. Se il progetto indicizzato è `openfav-codebase-V1` o un altro checkout:
   FERMATI. Non procedere sul grafo sbagliato.

Verifica repo con search_code su:
  - "APPLICATION_TYPE_PROJECTION"
  - "src/core/ui-primitives"
  - "check-style-authority"

==================================================
FASE 1 — EXISTING GENERATORS
==================================================

Usare search_graph/search_code per trovare:

- generate application
- generate-applications
- createApplicationDefinition
- application factory
- ApplicationBundle
- bundle-collector
- build-manifest
- build-report
- package.ts
- "How to create an application"
- README dentro src/applications

L'utente segnala che esiste un file/generatore con documentazione su come creare
un'applicazione. Trovarlo e leggerlo per intero se è esso stesso la specifica.

OUTPUT 1 — GENERATOR INVENTORY

Per ogni generatore/factory/script:
- simbolo
- file:riga
- input
- output
- side effect
- consumatori
- stato: CURRENT | LEGACY | EXPERIMENTAL | NOT FOUND

==================================================
FASE 2 — APPLICATION CONTRACT SURFACE
==================================================

Leggere con get_code_snippet:

- ApplicationDefinition
- ApplicationRouting
- ApplicationNavigation
- DiscoveryMetadata
- BackwardCompatibleApplication
- createApplicationDefinition
- ApplicationBundle / package contract
- ApplicationType
- presentation manifest contract, se esiste

Per ogni campo produrre:

APPLICATION FIELD MATRIX

| field | declared in | authority | classification | default/derivation | consumers |

classification ammessa:
- USER_INPUT
- DERIVED
- DEFAULT
- AUTHORITY_OWNED
- LEGACY_BRIDGE
- NOT_FOUND

Domande obbligatorie:

1. `id`, `namespace`, `title`: quali derivabili dal nome progetto/app?
2. `landing`, `login`, `afterLogin`, `notFound`: quali required?
3. Il minimal può esistere senza Shared Auth?
   - `ApplicationRouting.login` è required nel type letto in precedenza.
   - verificare i consumer prima di concludere.
4. `type: user|shared|workspace` dove viene dichiarato?
5. Quali valori sono scritti sia in Definition sia in Bundle?
6. Qual è il criterio reale di ripartizione Definition vs Bundle?
7. Esistono `as any` o extension ad-hoc nel punto di scrittura?

==================================================
FASE 3 — PAGE CONTRACT SURFACE
==================================================

Trovare e leggere:

- PageRecord
- PageData
- Page source/registry types
- page registry entry
- template key / template registry
- visibility/policy types
- page factories/helper
- normalizeToPageData (READ-ONLY: non proporre modifiche)

PAGE FIELD MATRIX

| field | declared in | authority | classification | default/derivation | consumers |

Domande obbligatorie:

1. Come si deriva `registryId` da app + slug?
2. Dove vengono dichiarati title, policy, template, order, source?
3. Quali campi minimi rendono valida una pagina?
4. Esiste un placeholder minimo compatibile con ogni template?
5. Il template espone uno scaffold/schema/default?
6. Quali campi PageData sono risultato di normalization e non vanno chiesti
   all'autore?
7. PageRecord e PageData sono correttamente separati?

==================================================
FASE 4 — WRITE TARGETS / MATERIALIZATION
==================================================

Mappare OGNI file che oggi va creato o modificato per aggiungere:

A. una nuova applicazione
B. una nuova pagina a un'applicazione esistente

OUTPUT 4 — WRITE TARGET MATRIX

| operation | file/path | write kind | source authority | required/derived |

write kind:
- CREATE
- APPEND
- UPDATE
- GENERATED_ARTIFACT
- MANUAL_PROJECTION

Segnalare esplicitamente:

- scritture che richiedono conoscere path interni
- registri aggiornati manualmente
- projection manuali (es. APPLICATION_TYPE_PROJECTION)
- file che dovrebbero essere build artifact
- collisioni possibili

==================================================
FASE 5 — AI PAGE PATH
==================================================

Ricercare:

- generateAiPage
- /api/v1/pages/generateAiPage
- /api/v1/ai/pages
- /api/v2/discovery/generate
- refresh-ai-pages
- generate page
- AI Page Engine

Usare trace_path e get_code_snippet.

OUTPUT 5 — AI PAGE FLOW

```text
input
→ provider/model
→ output type
→ normalization
→ persistence
→ discovery visibility
→ runtime consumption
```

Distinguere rigorosamente:

- AI CONTENT GENERATION
- PAGE AUTHORING
- PAGE PERSISTENCE
- BUILD ARTIFACT GENERATION

NON assumere che l'attuale `generateAiPage` produca una ApplicationBundle o una
config page. Verificarlo.

Domande:

1. L'AI genera PageData, PageRecord o altro?
2. Dove salva? Redis, filesystem, virtual provider, altro?
3. L'output sopravvive al rebuild?
4. Può essere riusato come `AIContentProvider` senza dargli ownership della
   configurazione?
5. Quali route/API sono legacy?

==================================================
FASE 6 — TEMPLATE SCAFFOLDING
==================================================

Per ogni template principale trovato:

| template | required PageData fields | minimal valid placeholder | scaffold source |

Classificazione:
- SCAFFOLD_EXISTS
- CAN_DERIVE
- REQUIRES_NEW_CONTRACT
- NOT_SUPPORTED_V0

Obiettivo: stabilire se il primo PlaceholderContentProvider può supportare UN solo
template senza inventare un generic placeholder incompatibile.

==================================================
FASE 7 — RECOMMENDATION
==================================================

Valutare questo modello, senza implementarlo:

Human | CLI | Frontend | AI | Importer
        ↓
ApplicationAuthoringSpec + PageAuthoringSpec
        ↓
Application/Page Builder deterministico (nessun filesystem)
        ↓
AuthoringResult in memoria
        ↓
LocalMaterializer | Authoring API | Bundle Download

ContentProvider interface:
- PlaceholderContentProvider (primo, deterministico)
- AIContentProvider (successivo, propone soltanto PageContentDraft)
- ImportContentProvider (futuro)

Output:
- SUPPORTED
- PARTIAL
- BLOCKED

Per ogni esito, condizioni di accettazione.

==================================================
SIMBOLI VINCOLATI — CLAUSOLA DI STOP
==================================================

La review è read-only.
Se la soluzione richiede modifiche a:

- PageController
- normalizeToPageData
- ApplicationDefinition
- ApplicationContext
- BundleCollector
- DiscoveryService / DiscoveryServiceV2
- PageData

segnalarlo come FOUNDATION RFC e fermare la raccomandazione.
Non proporre una modifica opportunistica.

Nota: usare un contratto esistente non è una modifica. Aggiungere un campo lo è.

==================================================
GUARDRAIL
==================================================

- Se un simbolo non esiste, scrivere NOT FOUND.
- Ogni affermazione su cosa esiste deve citare file:riga o tool output.
- Zero risultati senza comando non è un dato.
- Una ricerca per nome non prova l'assenza di un concetto: leggere il type.
- Distinguere FACTS OBSERVED / HYPOTHESES / RECOMMENDATIONS.
- Non creare file, non modificare file.

==================================================
OUTPUT FINALE OBBLIGATORIO
==================================================

INDEX STATUS
GENERATOR INVENTORY
APPLICATION FIELD MATRIX
PAGE FIELD MATRIX
WRITE TARGET MATRIX
AI PAGE FLOW
TEMPLATE SCAFFOLD MATRIX
HIDDEN RULES THE USER CURRENTLY MUST KNOW
DEFAULTS THAT CAN REMOVE QUESTIONS
MINIMAL PLATFORM REQUIRES AUTH? YES / NO / PARTIAL
SINGLE AUTHORING LAYER: SUPPORTED / PARTIAL / BLOCKED
FOUNDATION CONTRACT CHANGES REQUIRED
FINAL RECOMMENDATION
ACCEPTANCE CONDITIONS
```
