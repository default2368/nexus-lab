# Foundation Development Agent Handoff — `defaults.ts` Liveness

Copia questo prompt nelle sessioni degli agenti di sviluppo Foundation interessate alla
0.8.x.

---

## Prompt

```text
# Foundation 0.8.x — Discovery Defaults Liveness Handoff

ROLE:
Foundation Development Agent

MODE:
STRICT CONTEXT RECONCILIATION / READ-ONLY FIRST

EXPECTED REPOSITORY:
Open Nexus Foundation

EXPECTED WORKSTREAM:
0.8.x Authority and Contract Convergence

REPORTED WORKING BRANCH:
test2909

Do not assume branch, HEAD or working-tree state. Verify them.

==================================================
PROGRAM CONTEXT
==================================================

The active issue concerns exactly:

src/config/discovery/defaults.ts

It does not concern backup copies under:

backups/discovery-backup-*/defaults.ts

Historical root cause:

src/config/discovery/defaults.ts imported types from the missing module:

@/types/discovery/core.new

The proposed direct replacement was:

Page / PageMeta
→ @/types/discovery/page

PolicyFlags / PolicyName
→ @/types/discovery/policy.new

The direct import patch removed TS2307 but exposed contract-shape errors including
reported TS2367, TS2353, TS2551 and TS2339.

Interpretation:

- the missing type import masked downstream incompatibilities;
- the direct import direction may identify current type authorities;
- it is not a drop-in compatible patch;
- canonical Page/PageMeta/Policy contracts must not be widened merely to satisfy
  defaults.ts.

==================================================
CURRENT PROGRAM STATUS
==================================================

Reported status, to be verified against repository reports and commands:

DONE:
- F08-001 Authority Audit
- CLEANUP-001A Root Cause Audit
- CLEANUP-001B-GATE Decision Gate
- CLEANUP-002 Policy Drift Quantification
- CLEANUP-003 Page/PageMeta Compatibility Audit

IN PROGRESS:
- F08-002 Physical Pages Retirement
- CLEANUP-003B defaults.ts Canonicality Review

ON HOLD:
- CLEANUP-001B direct import patch

BLOCKED:
- F08-003 Capability / Bundle Boundary
- F08-004 Application Page Contract
- F08-005 Single Authority
- F08-006 Explicit IDs / broken references

Do not change these statuses without owner evidence.

==================================================
LIVENESS PROBE — REPORTED RESULT
==================================================

A disposable experiment temporarily renamed:

src/config/discovery/defaults.ts
→
src/config/discovery/defaults.ts.RETIRED-PROBE

Reported observation:

- build appeared to pass;
- dev server appeared to start;
- exercised pages appeared to work.

This is reported evidence, not yet sufficient to declare the file retired.

Current candidate classification:

RETIREMENT_CANDIDATE — HIGH CONFIDENCE

Not:

RETIRED
DELETED
SAFE_TO_REMOVE

==================================================
PROHIBITED ACTIONS
==================================================

Do not:

- apply the direct import patch;
- recreate core.new;
- add optional compatibility fields to Page or PageMeta;
- use any or casts to suppress errors;
- change PolicyFlags or PolicyName;
- modify PageController;
- modify DiscoveryService or DiscoveryServiceV2;
- modify ApplicationDefinition;
- modify normalizeToPageData;
- remove or rewrite tests to make the probe green;
- delete defaults.ts;
- modify backup or legacy files;
- commit, push or merge;
- reset, clean, stash or overwrite pre-existing work.

Any code change requires a separate owner-authorized task.

==================================================
PHASE 0 — GIT AND FILE STATE
==================================================

Run and report:

pwd
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git remote -v
git log --oneline --decorate -15

Verify the current state of:

src/config/discovery/defaults.ts
src/config/discovery/defaults.ts.RETIRED-PROBE

Run:

git ls-files -- src/config/discovery/defaults.ts
git status --short -- src/config/discovery/defaults.ts\
  src/config/discovery/defaults.ts.RETIRED-PROBE

If the working tree contains a live probe rename or unrelated changes:

- do not restore or remove anything automatically;
- report exact paths and status;
- stop with WORKING_TREE_RECONCILIATION_REQUIRED.

==================================================
PHASE 1 — STATIC CONSUMER MAP
==================================================

Build an exact consumer map for defaults.ts.

Search active code only:

src
scripts
tests
package.json
tsconfig files
export maps

Exclude from authority counts:

backups
docs_legacy
archive

Required categories:

PRODUCTION
BUILD
PACKAGE_EXPORT
TEST_CURRENT
TEST_LEGACY
DEBUG
DOC_ONLY
UNKNOWN

For every import/reference record:

path
line
symbol used
category
reason

Check:

- direct imports;
- barrel re-exports;
- dynamic imports;
- glob imports;
- package exports;
- generation/build scripts;
- Astro/server reachability;
- declaration build inclusion.

==================================================
PHASE 2 — PROBE EVIDENCE RECONCILIATION
==================================================

Locate or request the command ledger produced by the liveness probe.

Do not convert “seems to work” into PASS without commands and exit codes.

Required evidence dimensions:

TypeScript legacy pre/post
TypeScript public pre/post
build command and exit code
dev-server startup
representative route matrix
browser/server errors
targeted tests
full-suite failure-set comparison
package/declaration/Contract Bundle checks
protected kernel diff
working-tree restoration

Classify every dimension:

PASS
FAIL
NOT_RUN
INCONCLUSIVE

==================================================
PHASE 3 — CANONICALITY DECISION INPUT
==================================================

Return evidence for exactly one candidate outcome:

A. RETIRED
   No production, build, package or runtime consumer.

B. LEGACY ADAPTER
   Required only by legacy inputs, fixtures or compatibility paths.

C. CANONICAL
   Required by a current production/build/package path.

D. INCONCLUSIVE
   Evidence insufficient or contradictory.

Do not take the owner decision. Recommend one outcome with confidence and limits.

If A is recommended, the future retirement task remains separate and must cover:

- test classification/migration;
- active documentation references;
- comments such as VirtualPageTemplate mapping instructions;
- src/config/discovery/README.md;
- targeted and full regression gates;
- protected kernel diff = 0.

If B is recommended, propose a local legacy adapter boundary without changing
canonical Page/PageMeta contracts.

If C is recommended, list required explicit mappings field by field. Do not implement
them.

==================================================
MANDATORY OUTPUT
==================================================

Return:

Repository / branch / HEAD
Working-tree state
Exact file state
Consumer matrix
Export/package reachability
Probe evidence matrix
Missing evidence
Candidate outcome A/B/C/D
Confidence
Risks
Owner decision required
Recommended next task

Final status must be exactly one of:

READY_FOR_OWNER_CANONICALITY_DECISION
WORKING_TREE_RECONCILIATION_REQUIRED
BLOCKED_MISSING_PROBE_EVIDENCE
BLOCKED_CONFLICTING_EVIDENCE

==================================================
FINAL INVARIANT
==================================================

Do not adapt the platform to defaults.ts until defaults.ts is proven to belong to the
current platform.

The liveness probe may demonstrate a retirement candidate. Only an owner-authorized
retirement task may remove it.
```
