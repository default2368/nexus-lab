# PRD 0.9.0 — Semantic Entity Projection Model

**Status:** READY FOR OWNER REVIEW — executes ADR-0016
**Decision recommendation:** APPROVED WITH MINOR EDITS (edits applied 2026-09-20)
**Priority:** P1
**Target:** Foundation 0.9.0
**Dependency:** Foundation 0.8 Contract Bundle / packaging boundaries
**Epic:** `EPIC-0.9.0-SEMANTIC-ENTITY-PROJECTION.md`

---

## 1. Release Statement

> Open Nexus 0.9 può rappresentare entità di conoscenza non-Application come
> esperienze PageData, mantenendo Runtime e contratti protetti invariati.

### ASSUMPTION-01 — Build-time Materialization

```text
The Semantic Entity Layer enters Execution through build-materialized
PageData artifacts.

Discovery remains unchanged.
Runtime remains unchanged.
Request-time semantic projection is explicitly deferred.
```

Questa assunzione è un gate della release. Se viene violata, il lavoro esce dal
perimetro 0.9 e richiede una Foundation RFC separata.

---

## 2. Problem

Application e Page non sono il modello universale della conoscenza. I pilot Admin e
G. richiedono:

```text
Application · PageRecord
Procedure · Engagement · Evidence · Feedback · Decision
```

come entità indipendenti, collegate e proiettabili in viste per ruolo.

---

## 3. Goals

```text
G1  Semantic Entity contracts minimi e versionabili
G2  graph slice read-only da JSON
G3  projection pura Entity → View Artifact
G4  adapter View Artifact → PageData
G5  due viste G. sulla stessa entità
G6  secondo consumer Application/Page nell’Admin
G7  provenance, temporalità, cycle/depth guard
G8  conformance suite e Contract Bundle 0.9
```

## 4. Non-Goals

```text
AI / Brain integration
proiezione dinamica request-time
graph database
Discovery provider semantico
Discovery provider extensibility / provider registry
PageSource += semantic
modifiche a getProviderPriority() o DiscoveryServiceV2 provider aggregation
PageData changes
GenericEntityPage
CRUD completo
dati reali
Open Audit / Open GMP productization
```

---

## 5. Requirements Traceability

| ADR Boundary | Requirement | Verification |
|---|---|---|
| Runtime sees only PageData | R-08 adapter boundary | protected-file diff + build test |
| Entity outside Runtime | R-01/R-02 contracts | dependency test |
| Projector pure | R-06 | unit test, no forbidden imports |
| Context derived | R-04 | context factory test |
| Profiles cannot grant access | R-05 | intersection tests |
| Actions outside projector | R-09 | command boundary test |
| Build-time only | R-10 | no request-path imports |
| Two consumers | R-12/R-13 | conformance matrix |

---

## 6. Functional Requirements

### R-01 · Entity Contracts

Implementare:

```text
EntityReference
EntityRecord<TData>
RelationshipRecord
SourceReference
```

Campi dominio validati tramite `schemaRef`, non `any` non governato.

### R-02 · EntityGraphSlice

```text
root
entities map
relationships list
maxDepth
maxEntities
cycle guard
```

Relazioni tramite ID; nessun nesting ricorsivo di Entity.

### R-03 · JsonEntityProvider

```text
get(ref)
resolveSlice(query)
```

Read-only, nessuna projection, policy o AI.

### R-04 · ProjectionContext

Derivato da sessione/route/policy decision. Non input libero del client.

```text
locale · timezone · asOf · mode · grant · policyDecisionId
```

Nessuna modifica `ApplicationContext`.

### R-05 · EntityViewProfile

Definisce:

```text
rootEntityType · artifact kind · fields · relations · actions
```

```text
final fields  = requested ∩ visible
final actions = requested ∩ allowed ∩ capabilities
```

Profili G. hanno una sola source authority nel Domain Pack.

### R-06 · EntityProjector

Puro e deterministico.

Vietati:

```text
I/O · fetch · DB · policy evaluation · LLM · app selection
```

### R-07 · EntityViewArtifact

Rappresentazione intermedia con:

```text
artifactId · entityRef · profileId · kind · fields · children · actions · provenance
```

Card è artifact, non Entity.

### R-08 · PageData Adapter

Converte artifact validato in PageData senza modificare PageData, Runtime o
normalizer.

### R-09 · Commands Boundary

Edit/clone/archive/delete esposti come descriptor; esecuzione fuori dal projector.

### R-10 · Build-Time Materialization

```text
fixtures → provider → projector → artifact → PageData → build artifact esistente
```

Nessuna modifica Discovery/provider chain.

### R-11 · G Domain Pack

Schemi e profili per:

```text
Engagement · ProcedureVersion · WorkItem · Questionnaire
Evidence · Feedback · Action · Decision
```

Dataset esclusivamente sintetico.

### R-12 · G Consumer

Stessa Engagement Entity produce:

```text
engagement.control
engagement.client
```

con grant differenti e zero leakage.

### R-13 · Admin Consumer

```text
Application → application.admin-detail
PageRecord   → page.admin-detail
```

Consumer applicativo; non entra nel semantic core.

### R-14 · CodeEntity Experimental

Non bloccante:

```text
CodeEntity identificatore business
EntityReference ID tecnico
route alias da code
registryId canonico stabile
```

Promozione soltanto con secondo caso.

---

## 7. Milestones

### M0 — Scaffolding & Boundaries

```text
ADR PROPOSED
una root semantic-entity
contratti minimi
pack e fixture separati
boundary test reale
Admin e Brain fuori dal core
```

### M1 — Contracts & Provider

```text
Entity/Relationship/GraphSlice
JsonEntityProvider
schema validation
ENG-001 slice deterministico
```

### M2 — Projection & G Pilot

```text
Projector
View Artifact
PageData Adapter
control/client profiles
stessa Entity → due PageData
```

### M3 — Second Consumer & Conformance

```text
Application/Page Admin projection
provenance/asOf tests
cycle/depth guards
Contract Bundle 0.9
```

### M4 — Decision

```text
ACCEPTED | EXPERIMENTAL | REJECTED
```

---

## 8. Protected Files Gate

Il PR è bloccato se modifica senza nuova RFC:

```text
PageController
normalizeToPageData
ApplicationDefinition
ApplicationContext
BundleCollector
DiscoveryService / DiscoveryServiceV2
PageData
Runtime contracts
```

---

## 9. Test Plan

```text
T-01 schema entity valido/invalido
T-02 relationship target inesistente
T-03 cycle + depth limit
T-04 asOf seleziona versione valida
T-05 profile fields ∩ grant
T-06 profile actions ∩ grant
T-07 projector deterministico
T-08 no I/O / forbidden imports
T-09 G control vs client: no leakage
T-10 artifact → PageData compatibility
T-11 Application/Page secondo consumer
T-12 protected files diff = 0
T-13 build/runtime regression = 0
T-14 clone/archive CodeEntity experiment
```

---

## 10. Release Exit Criteria

```text
□ tutti i requisiti R-01→R-13 completati
□ R-14 può restare experimental senza bloccare
□ tutti i test T-01→T-13 verdi
□ G Control e Client Experience renderizzate
□ Admin Application/Page Detail renderizzate
□ Runtime invariato
□ Contract Bundle 0.9 pubblicato
□ decisione M4 registrata
```

---

## 11. Rollback

Tutto il codice 0.9 vive fuori dai contratti protetti. Il rollback rimuove:

```text
semantic-entity root
G Domain Pack
fixtures
Admin projection consumer
Contract Bundle additions 0.9
```

La Foundation 0.8 continua a funzionare senza migrazione dati.

---

## 12. Owner Approval

```text
ADR-0016 status: PROPOSED
PRD status: DRAFT

Project Owner approval:
  [ ] APPROVED
  [ ] APPROVED WITH CONDITIONS
  [ ] REJECTED

Date:
Notes:
```
