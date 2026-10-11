# DECISION — 0.8.2 Release Target — OWNER DECIDED

**Status:** APPROVED
**DecisionId:** NX-D-045-D1
**HandoffId:** 0.8.2-release-target
**Source:** Context 2 + Owner approval + Main Agent recommendation
**ConversationRef:**
  conversationId: arena/86a8bf50-nexus-lab
  turnRange: 2026-10-09T20:45-21:00
  date: 2026-10-09
  sourceHash: 9e06f47 + 6c7d303 + context2
  extractor: documentation-agent v0.1.0
  targetDocument: docs/candidates/DECISION-0.8.2-RELEASE-TARGET-OWNER-APPROVED.md
  approvalStatus: APPROVED

---

## OWNER_DECIDED — D1 e Core Admin package

```text
Foundation 0.8.2 release target
→ simple

Core Admin package
→ excluded dalla release 0.8.2

Classification
→ CORE_ADMIN_PACKAGE_OUT_OF_0_8_2_RELEASE_SCOPE
```

### Risposte owner

**Release target:**
A) Approvo: simple è il package target della 0.8.2

**Core Admin package:**
A) Approvo: escluso da 0.8.2 (CORE_ADMIN_PACKAGE_OUT_OF_0_8_2_RELEASE_SCOPE) — se lo ricostruiamo ci impieghiamo meno tempo, abbiamo tutte le primitive disponibili, se possibile ritirarla meglio ancora

---

## Conseguenze immediate

Per la 0.8.2 non implementiamo:

```text
Distribution Profile framework
manifest profile fields
producer filtering
validator profile rules
Core Admin package fixtures
Core Admin materialization/clean-room
package version transition Core Admin
```

La final release pipeline sarà:

```text
simple bundle
→ producer
→ manifest validation
→ materialization
→ clean-room
→ compatibility
→ release evidence
```

Il diagnostic package Core Admin resta:

```text
PROFILE_UNAPPROVED
NOT RELEASE EVIDENCE
```

---

## Core Admin: package vs applicazione — separiamo due decisioni

**Package Core Admin:**

```text
ritiro dalla 0.8.2
→ immediato e approvato
```

**Applicazione/source core-admin:**

```text
ritiro completo ora
→ NO
```

Oggi core-admin è ancora l'identità tecnica di Operations e possiede superfici attive:

```text
Operations index
Discovery pages
Component Catalog
navigazione
riferimenti runtime
pagine legacy ancora in migrazione
```

Eliminarla adesso romperebbe il repository runtime.

### Direzione futura approvata

```text
non riparare il vecchio Core Admin package
→ ricostruire Operations sull'host approvato
→ riusare primitive e contratti disponibili
→ migrare comportamento utile
→ ritirare Core Admin soltanto dopo parity
```

È coerente con:

> Infrastructure must be reusable; Domain must be replaceable.

### Condizioni di retirement futuro

L'attuale core-admin potrà essere ritirato quando:

```text
□ Operations index ha un successor
□ Discovery/pages ha un successor
□ Template Lab ownership è migrata o esplicitamente differita
□ API/System Control behavior è migrato o superseded
□ Component Catalog ha il proprio host gated/reference
□ navigazione e route compatibility sono decise
□ consumer source/build/package = 0
□ full-suite e package parity sono provate
□ eventuali alias hanno owner e scadenza
```

La ricostruzione probabilmente sarà più semplice del refactor incrementale perché:

```text
le primitive esistono
i contratti sono più chiari
il read model Distribution esiste
sappiamo cosa non trascinare
SystemDebugTemplate e le legacy page non devono essere preservate per identità visiva
```

Ma resta una direzione da dimostrare, non una stima ancora verificata.

---

## Context 2 — Diagnostic API Policy

### /build/sys/system-control

```text
PUBLIC_ALLOW_PUBLIC_AI_PAGES
```

Per ciascuno:

```text
INTENTIONALLY_PUBLIC
AUTH_REQUIRED
PRODUCTION_DENY
DEVELOPMENT_ONLY
UNKNOWN
```

Non un blanket gate.

Target probabile, da verificare:

```text
/api/v1/redis/test
→ PRODUCTION_DENY

/api/redis
/api/redis/test
→ DEVELOPMENT_ONLY / PRODUCTION_DENY

/api/v1/redis/pages
→ AUTH_REQUIRED o production deny

/api/v2/discovery default/list_smart
→ candidate intentionally public

debug/refresh/mutating discovery operations
→ AUTH_REQUIRED

sys/system-control
→ production owner/policy review
```

### Dopo diagnostic policy

```text
backup/snapshot inventory
→ release branch cleanup decision

simple package verification
→ final release candidate

compatibility matrix
→ version + notes

PR finale
→ owner merge
→ tag v0.8.2
```

---

## OWNER_DECISION_PENDING — Release Scope Closure

```yaml
title: Foundation 0.8.2 Release Scope Closure
status: OWNER_DECISION_PENDING
recommendedDecision:
  - releaseTarget: simple
  - coreAdminPackage: excluded
  - renderingKind: deferred
  - coreAdminProfile: deferred
  - operationsV1: deferred
  - formerDerivedCoreAdminIds: unsupported-diagnostic
  - mustClose:
      - diagnostic API policy
      - ID compatibility record
      - backup/snapshot disposition
      - current technical gates
      - simple package clean-room
      - compatibility matrix
      - version/release/tag
  - canDefer:
      - unique reference surfaces
      - Operations ownership migration
      - legacy template retirement without parity
      - semantic rendering redesign
```

---

## Verdetto

```text
BLOCKED_UNKNOWN_RELEASE_SCOPE
→ risolvibile con owner scope decision

code blocker
→ no

architecture blocker
→ no, se rendering/profile vengono differiti

remaining security blocker
→ diagnostic API policy

remaining release blocker
→ simple package + compatibility + metadata

La 0.8.2 può essere chiusa senza costruire altre fondamenta. Ma dobbiamo dichiarare con precisione cosa la release garantisce e cosa lascia intenzionalmente al ciclo successivo.
```

---

## Provenance

```
Context 1: 0.8.2 not blocked by single bug but by too broad and internally conflicting release definition — Main Agent: patch release security + authority convergence + distribution reproducibility with explicit deferrals
Context 2: /build/sys/system-control PUBLIC_ALLOW_PUBLIC_AI_PAGES classification INTENTIONALLY_PUBLIC AUTH_REQUIRED PRODUCTION_DENY DEVELOPMENT_ONLY UNKNOWN not blanket gate — target probable /api/v1/redis/test→PRODUCTION_DENY /api/redis→DEVELOPMENT_ONLY /api/v1/redis/pages→AUTH_REQUIRED /api/v2/discovery→intentionally public debug/refresh mutating→AUTH_REQUIRED sys/system-control→production owner/policy review — After diagnostic policy backup/snapshot inventory→release branch cleanup decision simple package verification→final release candidate compatibility matrix→version+notes PR finale→owner merge tag v0.8.2
Owner approval: Release target A) Approvo simple is package target, Core Admin package A) Approvo excluded CORE_ADMIN_PACKAGE_OUT_OF_0_8_2_RELEASE_SCOPE — if rebuild takes less time have all primitives available if possible retire better
OWNER_DECIDED D1: Foundation 0.8.2 release target → simple, Core Admin package → excluded, Classification CORE_ADMIN_PACKAGE_OUT_OF_0_8_2_RELEASE_SCOPE, Consequences immediate no Distribution Profile framework manifest profile fields producer filtering validator profile rules Core Admin fixtures materialization clean-room package version transition, final pipeline simple bundle→producer→manifest validation→materialization→clean-room→compatibility→release evidence, diagnostic package Core Admin PROFILE_UNAPPROVED NOT RELEASE EVIDENCE
Core Admin package vs applicazione: package ritiro immediate approved, applicazione/source core-admin ritiro complete now NO — today core-admin still technical identity of Operations owns active surfaces Operations index Discovery pages Component Catalog navigation runtime references legacy pages still in migration eliminating now would break runtime — Future direction approved not repair old Core Admin package → reconstruct Operations on approved host → reuse primitives and contracts → migrate useful behavior → retire Core Admin only after parity coherent with Infrastructure reusable Domain replaceable — Conditions retirement future 8 checkboxes Operations index successor Discovery/pages successor Template Lab ownership migrated or deferred API/System Control behavior migrated or superseded Component Catalog own host gated/reference navigation route compatibility decided consumer source/build/package=0 full-suite package parity proven eventual alias have owner and expiry — Reconstruction probably simpler than incremental refactor because primitives exist contracts clearer read model Distribution exists know what not to drag SystemDebugTemplate legacy pages not to be preserved for visual identity but remains direction to demonstrate not yet verified estimate
Checkpoint: Branch arena/46e97d6d-open-nexus-foundation HEAD 2324a96 Worktree clean — SURF-082-004 IN_ANALYSIS indexV0 KEEP_REFERENCE_DISCOVERY indexV1 PRESERVE_TEMPORARILY RETIREMENT BLOCKED_UNIQUE_BEHAVIOR — Next SURF-082-006 Legacy Reference Template Migration
Status: APPROVED for D1, OWNER_DECISION_PENDING for full scope closure
Extractor: documentation-agent v0.1.0
```
