# Foundation 0.8.x — Implementation Closure and Final Conformance Plan

```text
Status:          HOLD FOR F08-019A IMPLEMENTATION CLOSURE
Starting point:  F08-CODE-REALITY-CHECK @ HEAD 2f69e1b
Audit verdict:   PARTIAL_IMPLEMENTATION
Scope:           close the live distribution chain, then execute F08-019B
Feature work:    FROZEN — only readiness wiring is authorized
```

---

## 1. Objective

The F08-CODE-REALITY-CHECK demonstrated that real distribution code and contract tests
exist, but the complete operator path is not yet reproducible from the live Foundation
repository.

Historical F08-018 reconciliation work is complete and is not reopened by this plan.
Phases B–E below remain as the audit trail that led to F08-018 ratification; they are
not active execution steps unless new contradictory evidence appears.

The active sequence is now:

```text
F08-019A Implementation Closure
  live build-time producer CLI
  declared command entrypoints
  live ApplicationBundle → package → clean-room chain
  Operations frontend read-model wiring
↓
F08-019B Final Release Report
  targeted package/clean-room/frontend re-verification
  final KPI and ratification reconciliation
↓
owner release decision
↓
release commit and tag
```

Important terminology:

```text
The producer runs at build/distribution time against the live Foundation model.
It is not a Foundation Runtime responsibility.
```

---

## 2. Operating rules

During this plan:

```text
no new capability
no UI feature
no refactor unrelated to a failed release gate
no 0.9 integration
no package dependency upgrade
no lockfile change without explicit owner approval
no force push
```

Every change must map to one failed or incomplete gate in this plan.

Maximum work in progress:

```text
one mutating task
one read-only verification task
```

---

# F08-019A — Implementation Closure

## Gate 1 — Live producer entrypoint

Current evidence:

```text
distribution-producer-core.ts exists
producer tests pass
no operator CLI emits live manifest.json/discovery.json
```

Required chain:

```text
live ApplicationBundle / approved build model
↓
producer
↓
manifest.json + discovery.json on disk
```

The producer must:

```text
□ consume live Foundation declarations/artifacts, not test fixtures
□ run outside Vitest
□ accept explicit application ID and output directory
□ avoid repository scanning as a source of authority
□ produce deterministic machine-readable output
□ fail on unknown application or incomplete rendering/dependency metadata
□ preserve protected kernel contracts
```

## Gate 2 — Distribution command contract

Existing `node scripts/...` commands prove executable harnesses, but they are not yet a
stable operator contract.

Declare supported repository commands, for example:

```text
distribution:produce
distribution:validate
distribution:materialize
distribution:cleanroom
distribution:admin
distribution:build      composed golden path
```

Exact names require repository review. Requirements:

```text
□ no internal-file knowledge required from the operator
□ no hardcoded paths
□ no new dependency or lockfile mutation
□ exit codes and output locations documented
□ composed command runs produce → validate → materialize → integrity
```

## Gate 3 — Live package E2E

Required golden path:

```text
real simple ApplicationBundle
→ live producer
→ manifest/discovery files
→ materializer
→ package filesystem
→ repository unavailable
→ clean-room landing and second page
```

A test-created manifest is not accepted as the E2E input.

Required evidence:

```text
□ package tree
□ manifest and discovery hashes
□ package integrity result
□ clean-room route matrix
□ actual rendered template identity
□ asset locality
□ PHYSICAL rendering behavior when present
□ generated/AI template behavior when capability included
□ silent fallback count = 0
```

## Gate 4 — F08-017 frontend wiring

Current evidence:

```text
src/react/admin/** exists
component tests pass
route/page imports = 0
```

Required outcome:

```text
Operations-owned page/surface
↓
mounted Admin read-model frontend
↓
reads package/read-model artifact
↓
never scans the repository
```

No new application is required. Use the ratified Operations surface and preserve the
Operations V1 migration direction.

Required evidence:

```text
□ real route/page import
□ rendered component test or E2E
□ package-backed read model
□ screenshot or DOM evidence
□ no hardcoded fixture-only production path
```

## Gate 5 — Scratch and working-tree hygiene

Inspect `_cp1_scratch.mjs` before action. If it is genuinely temporary:

```text
remove it without committing
```

Add an ignore rule only if a recurring, well-defined temporary-file class exists.
Do not hide generic source patterns.

## Commit strategy

Candidate commits:

```text
feat(distribution): add live application manifest producer
chore(distribution): expose package and clean-room commands
test(distribution): cover live bundle to clean-room pipeline
feat(operations): mount distribution admin read model
```

One branch/PR is acceptable; commits remain independently reviewable.

## F08-019A completion

```text
command
→ live Foundation code
→ manifest/discovery artifact
→ package
→ clean-room result
→ package-backed Operations frontend
```

Final status:

```text
READY_FOR_F08_019B
or
BLOCKED_LIVE_PRODUCER
or
BLOCKED_COMMAND_CONTRACT
or
BLOCKED_PACKAGE
or
BLOCKED_CLEAN_ROOM
or
BLOCKED_FRONTEND_WIRING
```

---

# PHASE A — Repository and branch gate

Before modification:

```bash
git fetch origin --prune
git branch --show-current
git rev-parse HEAD
git status --short
git remote -v
git log --oneline --decorate --graph -20
```

Verify:

```text
□ commit 3a1bccd reachable from HEAD
□ current branch is the intended 0.8 release/conformance branch
□ working tree clean
□ no unrelated lockfile change
□ no active merge/rebase
```

If any condition fails:

```text
STOP — BRANCH_OR_WORKTREE_RECONCILIATION_REQUIRED
```

---

# PHASE B — F08-018A Status-count reconciliation [HISTORICAL — COMPLETE]

## Problem

Reported inventory:

```text
records      17
RETIRED       8
ADAPTED       5
ALLOWLISTED   3
```

The sum is 16. A seventeenth `PHANTOM` record is reported but not represented in the
classification summary.

## Action

Read-only first:

- inspect the ledger status enum;
- list every record ID and status;
- calculate deterministic counts;
- compare report, code and tests.

## Decision paths

### Path A — `PHANTOM` is a valid closed status

Update report and count table:

```text
RETIRED      8
ADAPTED      5
ALLOWLISTED  3
PHANTOM      1
TOTAL       17
```

Add/confirm an exact-count test.

### Path B — `PHANTOM` is a flag, not a status

The record must have one valid lifecycle status. Do not invent it automatically.
Return for owner decision.

## Gate

```text
□ every record has exactly one status
□ status count sum = inventory count
□ report, code and test agree
□ no UNKNOWN
```

Suggested commit, only if a change is required:

```text
docs(0.8): reconcile legacy ledger status counts
```

or, if code/test changes are required:

```text
fix(governance): reconcile phantom legacy record status
```

---

# PHASE C — F08-018B Wow/AI template lineage reconciliation [HISTORICAL — COMPLETE]

## Problem

Owner knowledge reported an AI-page consumer of the Wow template. The ledger reports:

```text
WowPageTemplate
→ PHANTOM
→ zero repository occurrences
→ target null
```

Static repository absence does not prove absence from generated/provider/persisted
PageRecords.

## Read-only evidence task

Search exact symbols:

```text
WowPageTemplate
WowLandingTemplate
AiPageTemplate
```

Trace:

```text
generated-page authoring output
AIPagesService or equivalent producer
Redis/provider PageRecord.template contract
fixtures and seeds
compatibility aliases
route-host mapping
template-manager mapping
historical producer defaults
```

Do not access production secrets or real tenant data.

## Decision paths

### Path A — terminology correction

```text
WowPageTemplate was an informal/historical name
canonical component/key = verified symbol
AI/generated records use verified canonical key or declared alias
```

Record the owner correction and preserve the alias if needed.

### Path B — persisted compatibility risk

If old records may contain `WowPageTemplate`:

```text
status: ADAPTED
canonical target: verified Wow template
alias owner: AI/generated-page capability
expiry/migration condition: explicit
```

Do not classify as PHANTOM.

### Path C — true phantom proven

Allowed only if:

```text
producer contract never emits the key
fixtures/seeds never emit it
provider contract excludes it
no historical supported version emitted it
owner confirms terminology mismatch
```

## Gate

```text
□ canonical AI template key known
□ alias chain known
□ generated/provider consumer contract known
□ package capability requirement known
□ ledger and F08-011A terminology agree
```

Suggested documentation commit:

```text
docs(0.8): reconcile Wow AI template lineage
```

---

# PHASE D — F08-018C Expiry enforcement [HISTORICAL — COMPLETE]

## Objective

Prove that route expiry is executable governance, not metadata.

Required behavior:

```text
active ADAPTED/ALLOWLISTED route
+
expiry before explicit asOf
→ ledger violation / release gate failure
```

Requirements:

```text
□ asOf supplied explicitly in tests
□ no Date.now-dependent fixture
□ expired RETIRED history remains valid
□ active expired route is rejected
□ missing expiry where required is rejected
```

Candidate function, naming subject to actual code:

```text
findExpiredActiveLegacyRoutes(asOf)
```

Suggested commit:

```text
test(governance): enforce legacy route expiry
```

No Runtime import or behavior change.

---

# PHASE E — F08-018 ratification [HISTORICAL — COMPLETE]

After Phases B–D pass:

```text
F08-018 → RATIFIED / DONE
```

Required final evidence:

```text
□ 17/17 records accounted for
□ Wow/AI template lineage reconciled
□ active expired routes = 0
□ retired live consumers = 0
□ ownerless records = 0
□ missing evidence = 0
□ UNKNOWN status = 0
□ legacy ledger audit violations = 0
□ protected kernel diff = 0
```

Documentation-only ratification commit:

```text
docs(0.8): ratify legacy compatibility and retirement ledger
```

---

# PHASE F — Pre-release checkpoint

Only from a clean, pushed, reviewed commit.

Candidate annotated tag:

```text
foundation-0.8-pre-release-conformance
```

Tag message:

```text
Foundation 0.8 pre-release conformance checkpoint.
F08-001 through F08-018 ratified.
F08-019 not yet executed.
Not a public release.
```

Before tag:

```bash
git status --short
git tag -l 'foundation-0.8-pre-release-conformance'
git show --no-patch --decorate HEAD
```

Push the tag only with explicit owner approval.

---

# F08-019B — Final Release Report and Conformance

F08-019B begins only after F08-019A returns `READY_FOR_F08_019B`.

It does not reopen implementation. Failed gates create explicit blockers and stop.

---

# PHASE G — F08-019 Repository conformance

## G1 — Git and provenance

Record:

```text
branch
HEAD
baseline ancestor
pre-release tag
working-tree status
commit range
```

## G2 — Contract suites

Run exact documented commands for:

```text
contract suite
authority suite
legacy ledger suite
distribution/manifest suite
```

Expected known contract result:

```text
739/739 or a documented higher count
```

A changed count is not automatically regression, but every delta must be explained.

## G3 — Full-suite comparison

Compare against the approved 0.8 pre-release parent/baseline:

```text
failure set added      = 0
failure set removed    = measured
passed tests delta     = explained
```

Do not report “no regression” from counts alone; compare failing test identities.

## G4 — TypeScript

```text
public TypeScript surface = 0 errors
legacy TypeScript error set = no new errors
semantic/distribution touched files = 0 errors
```

## G5 — Protected kernel

Verify exact diff for:

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

Target:

```text
unapproved protected diff = 0
```

## G6 — Governance and authority

```text
manual duplicate page write authorities = 0
broken navigation references = 0
canonical pages without explicit ID = 0
ownerless canonical pages = 0
legacy ledger violations = 0
active expired legacy routes = 0
```

---

# PHASE H — Package and manifest conformance

Produce the package twice from the same pinned inputs.

Verify:

```text
□ canonical Distribution Manifest present
□ Foundation release/version present
□ contract versions present
□ page identities/routes complete
□ capability identities/versions complete
□ rendering kind TEMPLATE/PHYSICAL explicit
□ runtime template catalogs finite and package-scoped
□ templates present with hashes
□ assets present with hashes
□ discovery index present with hash
□ build provenance present
□ no absolute source path
□ no Foundation repository dependency
□ no undeclared remote asset
□ no target file outside allowlist
□ package integrity validation PASS
```

Determinism:

```text
same semantic inputs
→ same content hashes and package inventory
```

Non-semantic timestamps must not invalidate content determinism.

Verify the legacy ledger source/test tooling is excluded from the consumer package
unless explicitly required by the package contract.

---

# PHASE I — Clean-room execution

Create an execution directory outside the Foundation repository.

```text
Foundation repository unavailable
→ install/validate package
→ start
→ exercise route matrix
```

Required route/experience checks:

```text
landing = 200
at least one second canonical page = 200
PUBLIC policy behavior
PROTECTED policy behavior
not-found behavior
asset loading
template identity
```

## Template correctness

Do not accept HTTP 200 alone.

```text
manifest declares template X
→ runtime/DOM evidence proves component X rendered
```

## Template Lab scenarios

### Package without Template Lab

```text
Template Lab absent
runtime catalog absent
package remains valid
```

### Operations package with Template Lab

```text
catalog manifest-declared
catalog finite
all declared templates materialized
UI enumerates only declared catalog
selection outside catalog fails closed
no silent VirtualPageTemplate fallback
repository-global registry unavailable
```

## PHYSICAL rendering

```text
rendering.kind = PHYSICAL
→ route artifact present
→ route works
→ no template lookup attempted
```

## Generated/AI page capability

When included:

```text
canonical Wow template key resolves
aliases explicit
required assets present
unknown generated template key fails closed
```

---

# PHASE J — Release report

Produce:

```text
docs/reports/0.8/F08-019-FOUNDATION-0.8-CONFORMANCE-AND-RELEASE.md
```

Required sections:

1. Executive verdict
2. Git/provenance
3. Contract test ledger
4. Full-suite comparison
5. TypeScript
6. Protected-kernel diff
7. Authority/page/template/asset conformance
8. Distribution Manifest
9. Package inventory and determinism
10. Clean-room route matrix
11. Legacy ledger
12. Known limitations
13. Deferred work
14. Owner release decision
15. Command ledger

Allowed final verdicts:

```text
READY_FOR_OWNER_RELEASE_DECISION
BLOCKED_CONTRACT_REGRESSION
BLOCKED_TYPE_REGRESSION
BLOCKED_PROTECTED_DIFF
BLOCKED_MANIFEST_INCOMPLETE
BLOCKED_PACKAGE_NONDETERMINISM
BLOCKED_CLEAN_ROOM
BLOCKED_LEGACY_GOVERNANCE
```

---

# PHASE K — Owner release decision

No version bump, release commit or release tag before owner approval of F08-019.

If approved:

```text
release commit candidate:
release(0.8.1): Foundation distribution readiness

tag candidate:
v0.8.1
```

Version rationale:

```text
v0.8.0 already exists as an annotated Foundation Experience Model release tag
(commit 8fe20ca, tag object 94a80d0).

The Distribution Readiness release therefore advances to 0.8.1.
The existing v0.8.0 tag is preserved and never moved or replaced.
```

Before push:

```text
working tree clean
release commit reviewed
annotated tag points to release commit
remote branch/tag collision check
```

After release:

```text
update central program state
publish Foundation status report
begin final 0.9 rebase/integration against v0.8.1
```

---

## Immediate execution order

```text
1. PHASE A branch/worktree gate
2. F08-019A Gate 1 — live producer entrypoint
3. F08-019A Gate 2 — declared operator commands
4. F08-019A Gate 3 — live bundle-to-clean-room E2E
5. F08-019A Gate 4 — Operations frontend wiring
6. F08-019A verdict
7. PHASE F pre-release checkpoint
8. F08-019B / PHASE G–J final conformance report
9. PHASE K owner release decision
```

Historical Phases B–E remain evidence only and are not rerun absent contradictory
findings.
