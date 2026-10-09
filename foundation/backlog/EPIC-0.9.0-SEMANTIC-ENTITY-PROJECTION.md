# EPIC 0.9.0 — Semantic Entity Projection Model

**Stato:** PROPOSED — READY FOR OWNER APPROVAL
**Target:** Open Nexus Foundation 0.9.0
**Durata stimata:** 3 settimane di sviluppo focalizzato
**Predecessore:** 0.8.x Distribution Readiness / Contract Bundle
**Brain integration:** esplicitamente successiva alla chiusura 0.9.0

---

## 0. Decisione

Open Nexus introduce un Semantic Entity Layer esterno al Runtime.

```text
EntityRecord
+ EntityGraphSlice
+ ProjectionContext
+ EntityViewProfile
        ↓
EntityProjector
        ↓
EntityViewArtifact
        ↓
PageData Adapter
        ↓
PageData
        ↓
Runtime invariato
```

### Invarianti

```text
Entities model knowledge.
Applications organize experiences.
Projectors translate entities into view artifacts.
PageData transports knowledge.
Runtime renders experiences.
```

---

## 1. Obiettivo

Consentire a entità non-Application:

```text
Procedure
Audit / Engagement
Questionnaire
Evidence
Feedback
Action
Decision
```

di produrre PageData senza modificare:

```text
Runtime
PageController
DiscoveryService / DiscoveryServiceV2
ApplicationContext
ApplicationDefinition
PageData
normalizeToPageData
BundleCollector
```

E verificare lo stesso modello su un secondo consumer indipendente:

```text
Application
PageRecord
```

nell’Admin 0.8/0.9.

---

## 2. Scope 0.9.0

### Incluso

```text
· Semantic Contracts minimi
· JsonEntityProvider read-only
· EntityGraphSlice piatto
· ProjectionContext derivato
· EntityViewProfile dichiarativo
· EntityProjector puro
· EntityViewArtifact intermedio
· adapter EntityViewArtifact → PageData
· G Domain Pack sintetico
· due viste G.: control e client
· secondo consumer: Application/Page Admin detail
· conformance suite
· materializzazione build-time
```

### Escluso

```text
· AI / LLM
· Brain integration
· proiezione dinamica per-request
· graph database
· GraphRAG
· persistenza definitiva
· GenericEntityPage
· Entity nel Runtime
· field-level authorization dinamica
· dati reali o riservati
· CRUD completo
· Open Audit / Open GMP come prodotti
```

---

## 3. Contratti candidati

### 3.1 Semantic Layer

```ts
interface EntityReference {
  id: string
  type: string
  namespace: string
  schemaVersion: string
}

interface EntityRecord<TData = unknown> {
  ref: EntityReference
  schemaRef: string
  data: TData

  sourceRefs: SourceReference[]

  validFrom?: string
  validUntil?: string
  recordedAt: string
}

interface RelationshipRecord {
  id: string
  type: string

  source: EntityReference
  target: EntityReference

  sourceRefs: SourceReference[]

  validFrom?: string
  validUntil?: string
}
```

`data` viene validata tramite `schemaRef` del Domain Pack. Non è un escape hatch
`Record<string, any>`.

### 3.2 Graph Slice

```ts
interface EntitySliceQuery {
  root: EntityReference
  relationTypes?: string[]
  maxDepth: number
  maxEntities: number
}

interface EntityGraphSlice {
  root: EntityReference
  entities: Record<string, EntityRecord>
  relationships: RelationshipRecord[]
}
```

Niente `children: Entity[]` ricorsivo.

### 3.3 Projection Context

```ts
interface ProjectionGrant {
  tenantRef?: string
  visibleFields: string[]
  allowedActions: Array<'view' | 'edit' | 'clone' | 'archive' | 'delete'>
}

interface ProjectionContext {
  locale: string
  timezone: string
  asOf: string
  mode: 'view' | 'preview' | 'edit'
  grant: ProjectionGrant
  policyDecisionId: string
}
```

Il Context è derivato da sessione, route e policy decision. Non è input libero del
client e non modifica ApplicationContext.

### 3.4 View Profile

```ts
interface RelationProjectionSpec {
  relationType: string
  targetProfile: string
  limit?: number
  depth?: number
}

interface EntityViewProfile {
  id: string
  rootEntityType: string
  artifact: 'card-grid' | 'table' | 'detail' | 'timeline'
  fields: string[]
  relations: RelationProjectionSpec[]
  actions: EntityAction[]
}
```

```text
fields finali  = profile.fields  ∩ grant.visibleFields
actions finali = profile.actions ∩ grant.allowedActions ∩ entity capabilities
```

### 3.5 Projection

```ts
interface EntityProjectionInput<TData = unknown> {
  graph: EntityGraphSlice
  profile: EntityViewProfile
  context: ProjectionContext
}

interface EntityProjector<TData = unknown> {
  supports(entityType: string, profileId: string): boolean
  project(input: EntityProjectionInput<TData>): EntityViewArtifact
}
```

Il Projector è puro: nessun fetch, DB, policy evaluation, LLM o scelta app.

### 3.6 View Artifact

```ts
interface EntityViewArtifact {
  artifactId: string
  entityRef: EntityReference
  profileId: string
  kind: 'card' | 'card-grid' | 'table' | 'detail' | 'timeline'
  fields: Record<string, unknown>
  children: EntityViewArtifact[]
  actions: EntityActionDescriptor[]
  provenance: ProjectionProvenance
}
```

La Card è un artifact, non una Entity.

---

## 4. Provider v0

```ts
interface EntityProvider {
  get(ref: EntityReference): Promise<EntityRecord | null>
  resolveSlice(query: EntitySliceQuery): Promise<EntityGraphSlice>
}
```

Prima implementazione:

```text
JsonEntityProvider
├── entities.json
└── relationships.json
```

Il provider recupera. Non proietta e non autorizza.

---

## 5. Azioni

Il Projector produce soltanto descrittori:

```ts
interface EntityActionDescriptor {
  action: 'edit' | 'clone' | 'archive' | 'delete'
  target: EntityReference
  command: string
  requiresApproval: boolean
}
```

L’esecuzione avviene fuori dal Projector:

```text
UI action
→ Domain Command
→ Policy
→ Preview / confirmation
→ Authoring Core
→ Source state
→ nuova projection
```

Distinzioni obbligatorie:

```text
remove card from view  ≠ delete Entity
clone artifact         ≠ clone Entity
edit PageData          ≠ edit EntityRecord
```

Per audit/GMP, `archive`/`supersede` precedono il delete fisico.

---

## 6. Pilot G. sintetico

Domain Pack applicativo:

```text
Engagement
ProcedureVersion
WorkItem
Questionnaire
Response
Evidence
Feedback
Action
Decision
Approval
Deliverable
```

Profili iniziali:

```text
engagement.control
engagement.client
procedure.detail
work-item.card
feedback.card
```

Viste:

```text
Control View
Engagement View
Client Evidence Portal
```

Dataset: quello definito in
`NEXUS-LAB/STRATEGIC-WORKFLOWS/G-AUDIT-ENGAGEMENT-CONTROL.md`.

---

## 7. Secondo consumer — Admin

```text
Application → application.admin-detail
PageRecord   → page.admin-detail
```

Obiettivo: verificare se identity, schema, source, temporal validity, relationships e
projection sono comuni fra:

```text
Application/Page
Procedure/Audit
```

Nessuna unificazione forzata. Se il minimo comune non regge, il contratto resta
sperimentale.

---

## 8. Impatto Runtime

| Area | 0.9.0 |
|---|---:|
| Runtime | invariato |
| PageController | invariato |
| Discovery | invariato |
| ApplicationContext | invariato |
| ApplicationDefinition | invariato |
| PageData | invariato |
| normalizeToPageData | invariato |
| BundleCollector | invariato |
| Authoring/build | nuovo layer |
| Experience | nuovi projector/profile |

La prima release usa materializzazione build-time:

```text
JSON entities/relations
→ provider
→ projector
→ artifact
→ PageData
→ registry/build artifact esistente
```

---

## 9. Piano di sviluppo — 3 settimane

### Settimana 1 — Contracts + Provider

```text
· ADR PROPOSED
· EntityReference / EntityRecord / RelationshipRecord
· EntityGraphSlice
· ProjectionContext / Grant
· EntityViewProfile
· JsonEntityProvider
· schema e test
```

**Gate W1:** graph slice di ENG-001 risolvibile deterministicamente.

### Settimana 2 — Projection + G Pilot

```text
· EntityProjector
· EntityViewArtifact
· adapter → PageData
· engagement.control
· engagement.client
· dataset sintetico
· Control + Engagement View
```

**Gate W2:** stessa Entity produce due PageData differenti senza Runtime changes e
senza leakage.

### Settimana 3 — Second Consumer + Conformance

```text
· Application/Page projections Admin
· Client Evidence Portal
· provenance / asOf tests
· cycle/depth/limit tests
· conformance suite
· build-time materialization
```

**Gate W3:** due domini confermano il minimo comune; Contract Bundle 0.9 esportato.

---

## 10. Branch strategy e collisioni

### Branch

```text
feature/0.8-distribution-readiness
feature/cli-v1-orchestrator
feature/0.9-semantic-entity-projection
brain/refactor-foundation
```

### Ownership prevalente

```text
0.8 branch     packaging · assets · template resolution · contract export
CLI branch     cli/ · adapter legacy · ProjectContext
0.9 branch     semantic contracts · provider · projectors · G pack
Brain branch   FastAPI · DocsStore · Provider Layer · Roy
```

### File/aree a rischio collisione

```text
package.json / lockfile
tsconfig / export map
Contract Bundle manifest
root index/barrel
CI workflows
```

Regole:

```text
· piccoli commit e rebase frequente
· 0.8 merge prima della finalizzazione 0.9
· 0.9 non modifica file 0.8 salvo export manifest concordato
· CLI pinna un Contract Bundle taggato, mai main mobile
· Brain non integra Entity Model prima del Contract Bundle 0.9
```

---

## 11. Brain integration — post 0.9

Durante 0.9 il Brain può essere allenato soltanto come corpus/ruleset candidato.
Non entra nel percorso di build.

Dopo 0.9:

```text
Question
→ Entity retrieval
→ Graph Slice
→ Brain interpretation
→ Candidate relation / summary
→ gate
→ EntityViewArtifact / AnswerArtifact
```

Il Brain propone. Non modifica EntityRecord, RelationshipRecord o PageData.

“Allenare il Brain tramite chat” significa:

```text
chat
→ Candidate Record / Candidate Rule
→ validation
→ eventuale canonicalizzazione umana
```

Non training dei pesi e non promozione automatica della conversazione.

---

## 12. Acceptance Criteria

```text
□ Procedure non-Application → PageData senza Runtime changes
□ Audit/Engagement non-Application → PageData senza Runtime changes
□ stessa Entity → due viste per ruolo
□ Application visualizzabile come Entity projection nell’Admin
□ PageRecord visualizzabile come Entity projection nell’Admin
□ provenance e validità temporale sopravvivono
□ projector puri, deterministicamente testabili
□ relazioni per ID, depth e cycle guard
□ nessun `if entityType` nel Kernel
□ niente `props.epistemic` come escape hatch generico
□ niente PageData manuale per migliorare la demo
□ due consumer indipendenti confermano il contratto
□ Contract Bundle 0.9 esportato
```

---

## 13. Falsificazione dell’Epic

L’Epic viene respinto o riportato a pack applicativo se:

```text
· Application/Page e Procedure/Audit non condividono un contratto utile
· il modello richiede modifiche ai simboli protetti
· i projector devono fare I/O o policy evaluation
· l’artifact intermedio duplica PageData senza valore
· la genericità produce più campi opzionali che invarianti
· la projection non è riproducibile
```

---

## 14. Non-decisioni

```text
· graph database
· storage definitivo
· AI provider
· UI editor
· CRUD completo
· naming commerciale Open Audit/Open GMP
· pricing
· alternative Foundation implementation
```

---

## 15. Decisione di chiusura

Al termine della 0.9.0:

```text
ACCEPTED
  se due consumer confermano il contratto e il Runtime è invariato

EXPERIMENTAL
  se funziona soltanto per il G Domain Pack

REJECTED
  se richiede contaminazione del Kernel o genericità artificiale
```

---

*Epic formalizzato per approvazione del Project Owner. La 0.9.0 non include AI; il
Brain viene integrato soltanto contro il Contract Bundle concluso.*
