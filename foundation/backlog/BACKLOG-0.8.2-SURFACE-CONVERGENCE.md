# Foundation 0.8.2 — Surface Convergence Backlog

**Status:** ACTIVE after `v0.8.1`  
**Baseline:** Foundation 0.8.1 — Distribution Green Line  
**Rule:** one bounded mutation task at a time

---

## NOW

### PROV-082-001 · Dirty Working Tree Provenance

```text
Status      READY after defaults-retirement PR merge
Priority    P0
Scope       distribution producer provenance
```

Target:

```text
clean tree       → GIT_VERIFIED
staged/dirty     → reject by default
explicit override → WORKTREE_UNVERIFIED, release-ineligible
```

This task remains independent from page/template migration.

---

## PARKED / NON-BLOCKING FOR CURRENT TASK

### SURF-082-001 · AI Pages Panel Host Migration

```text
Status      PARKED — evidence discovered, implementation not authorized
Priority    P1
Blocks      retirement of VirtualPageTemplate
Does not block PROV-082-001
```

### Observed direction

The AI Pages panel is injected through `VirtualPageTemplate` together with its current
context. `VirtualPageTemplate` is deprecated but intentionally maintained.

Exact source component, injection path, context provider and consumers must be pinned
by command/file evidence from the Foundation repository before implementation.

### Current classification

```text
AI Pages panel responsibility   ACTIVE
current host                    VirtualPageTemplate
current host lifecycle          DEPRECATED_COMPAT / MAINTAINED
retirement disposition          MIGRATE_CONSUMER_THEN_RETIRE
```

`VirtualPageTemplate` is not an orphan and is not eligible for retirement while this
consumer remains.

### Required future audit

```text
□ source component identified
□ injection point identified
□ context shape and authority identified
□ static/provider/generated consumers inventoried
□ current route/page identities identified
□ target approved host selected
□ PageData/Presentation contract preserved
□ assets and template requirements declared
□ compatibility behavior for existing generated pages defined
□ clean-room and visual parity tests defined
```

### Target decision

The panel must be moved to an approved, non-deprecated host or capability/experience
surface before `VirtualPageTemplate` retirement.

Candidate outcomes:

```text
MIGRATE_TO_WEB_PAGE_HOST
MIGRATE_TO_ASSISTANT_EXPERIENCE
KEEP_BOUNDED_COMPATIBILITY
REVIEW_REQUIRED
```

No target is approved by this backlog entry.

### Non-goals

```text
retire VirtualPageTemplate now
modify the AI page contract during PROV-082-001
redesign the panel
change Brain endpoints
merge this work into the provenance PR
```

### Definition of Done

```text
□ panel renders through the approved target host
□ context contract remains explicit and versioned
□ existing AI/generated pages remain compatible or migrate deterministically
□ VirtualPageTemplate has no remaining active consumer before retirement
□ no silent template fallback
□ package and clean-room behavior verified
□ visual/interaction parity reviewed
□ legacy host compatibility has owner and expiry
```

---

## NEXT AFTER PROV-082-001

### SURF-082-002 · Registry Shim Convergence

```text
Status      READY after PROV-082-001 merge
Priority    P1
Scope       empty and re-export-only page registry shims
Non-goal    registry/provider architecture rewrite
```

Candidate groups from F08-009 evidence:

```text
CORE_PAGES           empty legacy bridge
RECOVERY_TEST_PAGES  empty legacy bridge
SIMPLE_PAGES         re-export shim
WELCOME_PAGES        re-export shim
HUB_PAGES            active compatibility surface — exclude from first mutation
```

Phase 1 is read-only and must determine:

```text
source file
actual value/cardinality
all importers
package/export consumers
runtime/build use
canonical replacement
object/ID parity impact
candidate disposition
```

The first mutating PR should contain only shims proven empty with zero compatibility
value. Re-export shims require a separate owner decision after consumer evidence.

Required invariant:

```text
registry unique ID set before = registry unique ID set after
bundle ownership before       = bundle ownership after
package/clean-room output      = semantically unchanged
```

Do not in this task:

```text
retire hub
merge page-registry and virtual-provider architecture
change Page IDs
change bundle membership
change Operations
change templates/assets
```

After SURF-082-002, next candidate classes are:

```text
stale references
DEV_ONLY test/recovery isolation
```

Do not select `VirtualPageTemplate` retirement until SURF-082-001 is complete.

---

## NEXT AFTER SURF-082-002

### SURF-082-003 · Stale Reference Convergence

```text
Status      READY after registry-shim PR merge
Priority    P1
Scope       references to already-retired pages/helpers/types
Non-goal    retire active debug/recovery surfaces
```

Initial retired identifiers/sources to reconcile:

```text
physical/main/chat             → simple/assistant
physical/main/home-pages       → core-admin/discovery-pages
src/config/discovery/defaults  → retired, no replacement module
@/types/discovery/core.new     → retired/missing historical type source
```

For each occurrence classify:

```text
ACTIVE_RUNTIME_REFERENCE
ACTIVE_BUILD_REFERENCE
COMPATIBILITY_LEDGER
CURRENT_TEST
STALE_TEST_OR_COMMENT
CURRENT_DOCUMENTATION
HISTORICAL_EVIDENCE
BACKUP_OR_ARCHIVE
```

Historical evidence and governed Legacy Ledger entries are preserved. Only stale
references in active source, current tests and current operational documentation are
mutation candidates.

`physical/debug/debug-auth` is not part of this task: it is still an active, explicitly
owned debug/recovery surface and belongs to a later DEV_ONLY isolation decision.

Required target:

```text
active references to retired page IDs/files = 0
stale test comments/assertions = 0
current operational docs pointing to retired source modules = 0
historical/provenance records preserved
```

---

## NEXT AFTER SURF-082-003

### SURF-082-004 · Physical Debug and Recovery Surface Disposition

```text
Status      IN ANALYSIS — owner dispositions partially recorded
Priority    P1
Scope       physical/debug routes and recovery/template experiments
```

Owner dispositions:

```text
/debug/status
  PRESERVE_BEHAVIOR_REPLACE_PAGE
  target: Operations API/System Control

/debug/debug-theme
  MOVE_TO_TEMPLATE_LAB
  current route becomes DEV_ONLY until parity

/debug/debug-auth
  RETIRE candidate; future Auth diagnostics redesigned for the current auth flow

/indexV0
  KEEP_REFERENCE_DISCOVERY; candidate future discovery.astro

/indexV1
  RETIRE candidate if parity confirms duplicate behavior

/landing
  KEEP_REFERENCE_PROTOTYPE; migrate layout to approved React/landing host

test/hello-api + HelloApiTemplate
  LEGACY_REFERENCE_REVIEW; first template experiment, inspect and extract lessons before retirement

test/redis-console + RedisConsoleTemplate
  LEGACY_REFERENCE_REVIEW; inspect Operations/integration lessons before retirement
```

`LEGACY_REFERENCE_REVIEW` means:

```text
not production target
not immediate deletion
not generic DEV_ONLY
preserve temporarily for bounded inspection
extract reusable behavior/components
then choose MIGRATE / DEV_ONLY / RETIRE
```

Required next evidence:

```text
□ route status and rendered output for hello-api/redis-console
□ exact template/component/data flow
□ unique behavior compared with debug/status, Template Lab and Operations Control
□ package membership and current consumer set
□ reusable components/patterns identified
□ target host/owner candidate
□ retirement condition
```

No source mutation until the two legacy-reference reviews and file-based Astro route
reality check are complete.

---

## READY — REGISTRY CONSUMER CONVERGENCE

### SURF-082-005 · Registry Consumer Repointing and Re-export Shim Retirement

```text
Status      READY FOR READ-ONLY PLAN
Priority    P1
Depends     SURF-082-002 parity evidence
Scope       consumer path, not PageDefinition authority
```

Corrected premise:

```text
applications/<app>/pages
→ already canonical since 0.7.5.4

page-registry/pages/*
→ compatibility re-exports, not duplicate definitions
```

Residual issue:

```text
page-registry/index
→ imports compatibility shims

virtualProvider
→ imports registry/shim names
→ recomposes the application map manually
```

Target:

```text
page-registry/index
→ imports canonical application page maps directly
→ produces one PAGES_REGISTRY composition

virtualProvider
→ consumes PAGES_REGISTRY only

re-export shims
→ removed after parity
```

Candidate shim retirement set, subject to active-consumer verification:

```text
page-registry/pages/auth.ts
page-registry/pages/core-admin/index.ts
page-registry/pages/open-nexus/index.ts
page-registry/pages/simple/simple-pages.ts
page-registry/pages/welcome.ts
page-registry/pages/hub.ts
page-registry/pages/sys/core.ts
page-registry/pages/sys/tools.ts   (empty/dead)
```

Explicitly excluded:

```text
page-registry/backups/*
hub page retirement
ApplicationBundle membership changes
Page ID changes
Operations migration
template/asset changes
```

Required parity:

```text
registry ID set/hash unchanged
registry insertion/order behavior unchanged where observable
PageMeta object/owner mapping unchanged
virtualProvider output set/order unchanged
bundle ownership unchanged
navigation/broken refs unchanged
package semantic inventory unchanged
clean-room unchanged
no import cycle introduced
```

### Redis Console owner interpretation

```text
classification   LEGACY
role             REFERENCE / DIAGNOSTIC / TEMPLATE_EXPERIMENT
distribution     DEV_ONLY / GATED
current behavior PARTIALLY BROKEN (`/api/redis-console` missing)
disposition      EXTRACT_TARGETED_PATTERNS_THEN_RETIRE
```

Security boundary:

```text
Do not implement the missing arbitrary Redis command endpoint merely to preserve the
legacy page. Commands such as FLUSHDB/KEYS must not become a production Operations
capability without a separate security design and owner decision.
```

Extraction follows the rule of two and the approved target, not visual attractiveness:

```text
CappedLogPanel
  candidate only if required by the future Operations Control target and/or a second
  approved consumer;

StatusIndicator
  candidate shared diagnostic primitive, subject to second-consumer evidence;

ConsoleBlock
DebugInfoCard
  remain local until a second approved consumer/target contract exists;

JsonInspectorBlock
  already extracted; no action.
```

Do not refactor `SystemDebugTemplate` merely to improve legacy code if it is itself
scheduled for rebuild/retirement. Extract a primitive only when the approved target
Operations experience consumes it.

Template Lab must not trigger real Redis side effects during template preview. The
future preview contract must use injected/mocked I/O or an explicitly sandboxed mode.
