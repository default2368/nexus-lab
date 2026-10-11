# DECISION — 0.8.2 Closure Strategy — Patch release, non framework

**Status:** PARTIALLY APPROVED — D1 APPROVED, D2 PENDING, D3-D6 CONDITIONAL — superseded in part by context 3-8 docs
**DecisionId:** NX-D-045
**HandoffId:** 0.8.2-closure-strategy
**Source:** Context 1 report + Main Agent recommendation + Context 2-8 owner approvals
**ConversationRef:**
  conversationId: arena/86a8bf50-nexus-lab
  turnRange: 2026-10-09T20:30-21:30 + 2026-10-11 context 3-8
  date: 2026-10-09 / 2026-10-11
  sourceHash: 9e06f47 + 6c7d303 + 58caf95
  extractor: documentation-agent v0.1.0
  targetDocument: docs/candidates/DECISION-0.8.2-CLOSURE-STRATEGY.md
  approvalStatus: PARTIALLY APPROVED — see amendment 2026-10-11
**SupersededBy:**
  - docs/candidates/DECISION-0.8.2-RELEASE-TARGET-OWNER-APPROVED.md (D1 APPROVED)
  - docs/candidates/DIRECTIVE-ARENA-0.8.2-OWNER-DECISIONS-RECORDED.md (directive)
  - docs/candidates/EXPLANATION-0.8.2-CORE-ADMIN-PACKAGE-DISTRIBUTION.md (7 points)
  - docs/candidates/DECISION-0.8.2-D2-RENDERING-KIND.md (D2 PENDING, A recommended)
  - docs/candidates/DECISION-0.8.2-SIMPLE-DISTRIBUTION-PROOF-F08-020.md (F08-020 CANDIDATE)
  - docs/candidates/IMPLICATIONS-0.8.2-SIMPLE-DISTRIBUTION-FACTORY.md
  - docs/candidates/STRATEGY-FOUNDATION-BOOTSTRAP-SELF-HOSTING.md
  - docs/candidates/DECISION-0.8.2-RELEASE-STATEMENT-CANDIDATE.md

## AMENDMENT 2026-10-11 — Owner decisions recorded context 3-8

### D1 — APPROVED
```text
release target → simple
Core Admin package → CORE_ADMIN_PACKAGE_OUT_OF_0_8_2_RELEASE_SCOPE
```
- Non implementiamo in 0.8.2: Distribution Profile framework, manifest profile fields, producer filtering, validator profile rules, Core Admin fixtures, Core Admin materialization/clean-room, version transition
- Package vs applicazione: Core Admin continua a esistere e funzionare nel repo ≠ viene distribuito come package 0.8.2
- Future: rebuild Operations su host approvato, riuso primitive, migrazione behavior utile, retirement solo dopo parity gates (8 checklist)

### D2 — PENDING — A raccomandato
```text
rendering.kind → DEFERRED_WITH_OWNER_DECISION
current contract invariato: templateRef/policy/ownerBundle/route
PHYSICAL finding post-0.8.2
```

### D3-D4 — APPROVED as hygiene
- Fallback IDs → HISTORICAL_DERIVED_DIAGNOSTIC_IDS NOT RUNTIME_CANONICAL NOT SUPPORTED
- Operations V1 / Core Admin profile / System→Operations migration → POST_0_8_2

### D5 — Aggiornato
Must close: diagnostic API policy (/api/v1/redis/test→PRODUCTION_DENY, /api/redis→DEVELOPMENT_ONLY, /api/v1/redis/pages→AUTH_REQUIRED, /api/v2/discovery→intentionally public), backup/snapshot disposition, simple full pipeline, 0.8.1→0.8.2 matrix, full-suite rerun, build/typecheck/security guard, release notes/version/tag, branch hygiene
Can defer: indexV1 unique, /debug migration, Hello API/Redis Console retirement, Hub, about-legacy, Template Lab ownership, System/API Control migration, WowPageTemplate uncertainty, package-wide catalog — condition not in simple package or production-gated or explicit disposition

### Nuova definizione 0.8.2
> Foundation 0.8.2 consolida la convergenza di authority e sicurezza necessaria a produrre un package Simple bounded, riproducibile e verificato in clean-room, mantenendo espliciti e non distribuiti i residual source non ancora migrati.

Simple = fabbrica: repository → authoring/compiler/governance, package → prodotto distribuibile, Execution → runtime sottile, Domain Pack → differenzia verticali. Repo può essere complesso, prodotto pulito. Repository-Centric → Artifact-Centric.

### F08-020 Simple Distribution Release Proof — CANDIDATE next
- current Foundation → Simple package → external destination → clean-room → compatibility matrix → receipt
- DoD 12 items: clean tree, producer PASS, validator PASS, 5 page IDs, 4 template, 5 asset, no leakage, materialization PASS, external dest atomic, clean-room PASS, repoObservations 0, v0.8.1 compatibility, protected kernel diff 0, receipt generated

### Bootstrap / Self-Hosting — APPROVED ARCHITECTURAL DIRECTION IMPLEMENTATION DEFERRED
- Factory può usare proprio processo per rifondare sé stessa — intuizione owner 10/10
- Due strade: 1) nuova app pulita che consuma Foundation (consumer pulito) 2) nuova Foundation bootstrap F0→F1→F2 self-hosting, fixed-point test semantic inventory A = B
- Moat: codebase pulita→output copiabile, meccanismo che la rigenera→capability, meccanismo che rigenera sé stesso→candidate moat
- Sequence: 0.8.2 Simple Proof → 0.9 Semantic Entity → second app Domain Pack N-sectors → Workspace/ApplicationSpec → CLI workspace create → Foundation Bootstrap experiment → equivalence gate

--- Original decision below — preserved for provenance ---

---

## Observed

- Report 0.8.2: non è bloccata da singolo bug, ma da definizione di release troppo ampia e internamente conflittuale.
- EPIC §18 contiene criteri aspirazionali che allargano 0.8.2 a: profile framework, Operations migration, PageData rendering redesign, legacy mass retirement, security redesign di ogni API, repository cleanup completo — non è più una patch.
- Foundation source: security hardened parziale, page authority converged parziale, explicit current IDs in corso, residuals classified parziale.
- Distribution: simple package proven in 0.8.1 e checkpoint successivi, Core Admin package non conforme, manifest/materialization deterministici.
- Compatibility: v0.8.1 pinned remains valid, 0.8.2 simple package ha deterministic findings, no protected-kernel change.
- Existing findings: indexV0 KEEP_REFERENCE_DISCOVERY, indexV1 PRESERVE_TEMPORARILY RETIREMENT BLOCKED_UNIQUE_BEHAVIOR (checkpoint 2324a96 clean), SURF-082-004 IN_ANALYSIS, SURF-082-006 Legacy Reference Template Migration next.
- Routes: POST /api/redis-test exists, POST /api/redis-console believed absent must be verified, /api/v1/redis/test, /api/v1/redis/pages, /api/redis, /api/redis/test, /api/v2/discovery, /api/v2/discovery/list_smart — classification pending.

## Inferred

- Se si tenta di soddisfare tutti i criteri aspirazionali EPIC §18 ora, 0.8.2 diventa release framework non patch, con rischio di allargare public contract (rendering.kind) e creare nuovi compatibility contract (alias Core Admin).
- Core Admin non è mai stato runtime canonical ID, ma HISTORICAL_DERIVED_DIAGNOSTIC_IDS — aggiungerne alias ora creerebbe nuovo compatibility contract non presente in 0.8.1.
- rendering.kind è nuova evoluzione rendering contract, non presente in Distribution 0.8 contract, 0.8.1 rilasciata senza — introdurlo ora allargherebbe public contract.
- Operations V1, Core Admin profile, System→Operations ownership migration sono POST_0_8_2 — superfici restano nel source tree con disposition esplicita, non parte del package release target.

## Proposed — Decisioni raccomandate Main Agent

### D1 — Package release target

```text
0.8.2 package target → simple ordinary consumer
Usare package già dimostrato in 0.8.1 e checkpoint successivi.

Core Admin → source/runtime application → non release-package target 0.8.2
Nessun package Core Admin viene pubblicato o dichiarato conforme.
```

### D2 — rendering.kind

```text
explicit rendering.kind → DEFERRED_WITH_OWNER_DECISION
Non modificare in 0.8.2: manifest schema, producer, validator, materializer, Admin read model.

Motivo: nuova evoluzione rendering contract, non presente in Distribution 0.8 contract, 0.8.1 rilasciata senza, introdurlo ora allargherebbe public contract.

Per 0.8.2 resta valido contratto corrente:
templateRef
policy
ownerBundle
route

Finding PHYSICAL resta esplicito e post-0.8.2.
```

### D3 — Core Admin fallback IDs

Classificazione:

```text
core-admin/operations
core-admin/dashboard-legacy
core-admin/hello-api-test
core-admin/redis-console-test
→ HISTORICAL_DERIVED_DIAGNOSTIC_IDS
→ NOT RUNTIME_CANONICAL
→ NOT SUPPORTED 0.8.2 PACKAGE CONTRACT

Non aggiungere alias perché: non erano runtime IDs, package Core Admin non entra in release, non abbiamo evidenza artifact pubblicati/consumer, aggiungere alias creerebbe nuovo compatibility contract.

Correggere ledger:
dashboard replacement → core-admin/index
non core-admin/dashboard.
```

### D4 — Operations/System

```text
Operations V1 → POST_0_8_2
Core Admin profile → POST_0_8_2
System → Operations ownership migration → POST_0_8_2

Superfici restano nel source tree con disposition esplicita. Non sono parte del package release target.
```

### D5 — Source convergence — Must close prima release vs Deferrable

**Must close prima della release:**

```text
1. anonymous diagnostic/API production policy
2. compatibility decision/ledger per gli ID Phase A
3. tracked backup/snapshot inventory and disposition
4. simple package full release pipeline
5. 0.8.1 → 0.8.2 compatibility matrix
6. full-suite current rerun
7. build/typecheck/security guard
8. release notes/version/tag
9. release branch/stash hygiene
```

**Deferrable con record esplicito (non entrano nel simple package oppure sono production-gated oppure hanno disposition/owner/follow-up espliciti):**

```text
indexV1 unique behavior
/debug page ownership migration
Hello API retirement
Redis Console retirement/extraction
Hub
about-legacy
Template Lab ownership
System/API Control migration
WowPageTemplate external-consumer uncertainty
package-wide template catalog
```

Condizione: non entrano nel simple package oppure sono production-gated oppure hanno disposition/owner/follow-up espliciti.

### D6 — Release authority

```text
final evidence reviewer → Main Agent / Verification Agent
release approval → Owner
merge/tag → Owner only

Criteri 0.8.2 riscritti onestamente:

Release scope
Foundation source: → security hardened → page authority converged → explicit current IDs → residuals classified
Distribution: → proven simple package → clean provenance → deterministic manifest/materialization → clean-room
Compatibility: → v0.8.1 pinned remains valid → 0.8.2 simple package has deterministic findings → no protected-kernel change

Non-claim — La release non deve dichiarare:
all legacy source removed
Operations V1 complete
Core Admin package conformant
all template consumers known
rendering.kind implemented
repository backups globally zero

Se alcuni backup vengono esplicitamente differiti, il criterio "tracked backup snapshots = 0" deve essere modificato nella release statement, non falsamente marcato done.
```

## Unknown

- Classificazione esatta di /api/v1/redis/test, /api/v1/redis/pages, /api/redis, /api/redis/test, /api/v2/discovery, /api/v2/discovery/list_smart, POST /api/v2/discovery — da verificare in 0.8.2 Production Diagnostic API Policy Closure
- Esistenza POST /api/redis-console — believed absent must be verified
- Unique behavior indexV1 da preservare temporaneamente
- Package-wide template catalog impact

## Conflicting

- EPIC §18 aspirazionale vs patch release security/authority/distribution — conflitto definizione release
- Core Admin come source/runtime application vs release-package target — conflitto scope
- rendering.kind come evoluzione contract vs Distribution 0.8 contract — conflitto public contract
- Backup snapshots = 0 vs deferral esplicito — conflitto criterio release statement

## RecommendedDecision

> APPROVE AS PATCH RELEASE WITH EXPLICIT DEFERRALS — Chiudere 0.8.2 come patch release di security, authority convergence e distribution reproducibility, con deferral espliciti per Operations V1, Core Admin profile, rendering model e retirement non sicuri. Non tentare di soddisfare ora tutti i criteri aspirazionali EPIC §18.

## Alternatives

- Alt1: Full EPIC §18 — chiudere 0.8.2 come framework release con Operations V1, Core Admin profile, rendering.kind, mass retirement, security redesign ogni API, repository cleanup completo — Pro: soddisfa aspirazioni, Contro: non è più patch, allarga public contract, crea nuovi compatibility contract, richiede tempo owner elevato, rischio regressioni
- Alt2: Defer all — rinviare 0.8.2 a dopo Operations V1 e Core Admin profile — Pro: release più pulita, Contro: blocca security hardening e distribution reproducibility già pronte
- Alt3: Simple only con no-deferral record — chiudere solo simple package senza record esplicito deferral — Pro: veloce, Contro: lascia residui non classificati, viola regola provenance

## Consequences

- Se APPROVED: 0.8.2 diventa patch release onesta, security hardened, page authority converged, explicit current IDs, residuals classified, proven simple package, clean provenance, deterministic manifest/materialization, clean-room, v0.8.1 pinned valid, 0.8.2 simple deterministic findings, no protected-kernel change — non dichiara all legacy removed, Operations V1 complete, Core Admin conformant, all template consumers known, rendering.kind implemented, backups zero — deferral espliciti con disposition/owner/follow-up — sblocca release notes/version/tag e release branch/stash hygiene — permette di procedere a SURF-082-006 Legacy Reference Template Migration senza riaprire decisioni congelate
- Se REJECTED e si tenta full EPIC: 0.8.2 diventa profile framework + Operations migration + PageData rendering redesign + legacy mass retirement + security redesign ogni API + repository cleanup — non è più patch, richiede owner bandwidth elevata, rischio di introdurre breaking change in public contract

## ImplementationImpact

- Foundation: security hardened, page authority converged, explicit current IDs, residuals classified — no protected-kernel change
- Distribution: simple package full release pipeline, compatibility matrix 0.8.1→0.8.2, build/typecheck/security guard, release notes/version/tag, release branch/stash hygiene — Core Admin non release-package target
- Documentation: release statement riscritta onestamente con Non-claim, compatibility decision/ledger Phase A, tracked backup inventory disposition
- CLI/Workspace: none in 0.8.2
- Backend: none in first profile

## Next Task Raccomandato — Prima della release verification

```text
0.8.2 Production Diagnostic API Policy Closure
Read-only, stessa branch/sessione arena/46e97d6d-open-nexus-foundation HEAD 2324a96 clean.

Deve classificare esattamente:
/api/v1/redis/test
/api/v1/redis/pages
/api/redis
/api/redis/test
/api/v2/discovery
/api/v2/discovery/list_smart
POST /api/v2/discovery
POST /api/redis-test (exists)
POST /api/redis-console (believed absent must be verified)

Owner boundaries:
- Hello API and Redis Console are LEGACY_REFERENCE_REVIEW surfaces, neither is production target, do not delete before useful behavior/lessons inventoried
- do not implement generic Redis command endpoint
- arbitrary commands such as FLUSHDB and KEYS must not become production capability
- Template Lab preview must not execute real Redis I/O by default
- JsonInspectorBlock already extracted
- CappedLogPanel and StatusIndicator require approved target/second consumer
- ConsoleBlock and DebugInfoCard remain local unless reuse proven
- do not refactor SystemDebugTemplate merely to improve legacy code
```

## CandidateArtifact

- class: DECISION
- targetRepository: nexus-lab-documentation
- targetPath: docs/approved/DECISION-0.8.2-CLOSURE-STRATEGY.md
- currentPath: docs/candidates/DECISION-0.8.2-CLOSURE-STRATEGY.md

## OwnerGate

- required: true
- decision: PENDING
- final evidence reviewer: Main Agent / Verification Agent
- release approval: Owner
- merge/tag: Owner only

---

## Provenance

```
Report: 0.8.2 not blocked by single bug but by too broad and internally conflicting release definition
Main Agent: patch release of security, authority convergence and distribution reproducibility, with explicit deferrals for Operations V1, Core Admin profile, rendering model and retirement non safe — do not satisfy all aspirational criteria EPIC §18
Checkpoint: Branch arena/46e97d6d-open-nexus-foundation HEAD 2324a96 Worktree clean New commit none — SURF-082-004 IN_ANALYSIS indexV0 KEEP_REFERENCE_DISCOVERY indexV1 PRESERVE_TEMPORARILY RETIREMENT BLOCKED_UNIQUE_BEHAVIOR
Next: SURF-082-006 Legacy Reference Template Migration governing plan docs/plans/0.8/SURF-082-006-LEGACY-REFERENCE-TEMPLATE-MIGRATION.md — STRICT READ-ONLY PLAN FIRST — primary candidates test/hello-api HelloApiTemplate test/redis-console RedisConsoleTemplate — verify exact current IDs source paths consumers routes before using names — owner boundaries LEGACY_REFERENCE_REVIEW surfaces neither production target do not delete before useful behavior inventoried POST /api/redis-test exists POST /api/redis-console believed absent must be verified do not implement generic Redis command endpoint arbitrary commands FLUSHDB KEYS must not become production capability Template Lab preview must not execute real Redis I/O by default JsonInspectorBlock already extracted CappedLogPanel StatusIndicator require approved target/second consumer ConsoleBlock DebugInfoCard remain local unless reuse proven do not refactor SystemDebugTemplate merely to improve legacy code
Status: OWNER_DECISION_PENDING → requires owner approval
Extractor: documentation-agent v0.1.0
```
