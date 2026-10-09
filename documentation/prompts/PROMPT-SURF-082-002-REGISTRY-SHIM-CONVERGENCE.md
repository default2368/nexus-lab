# SURF-082-002 — Registry Shim Convergence

Use this prompt in a new clean Arena session attached to the Foundation repository,
after PROV-082-001A is merged to `master`.

---

## Prompt

```text
# SURF-082-002 — Registry Shim Convergence

ROLE:
Foundation Registry Convergence Agent

MODE:
STRICT READ-ONLY PHASE 1

OBJECTIVE:
Identify empty and re-export-only page-registry shims that can be retired without
changing the canonical page ID set, ApplicationBundle ownership, runtime behavior,
package output or 0.8.1 compatibility.

This task does not redesign Discovery or merge registry/provider authorities.

==================================================
PHASE 0 — BASELINE GATE
==================================================

Before analysis run:

pwd
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git remote -v
git fetch origin --prune
git log --oneline --decorate --graph -15

Verify:

- current branch derives from current origin/master;
- defaults retirement is merged;
- PROV-082-001A is merged;
- working tree is clean;
- no merge/rebase active;
- package version remains 0.8.1 until a future release task;
- v0.8.1 remains unchanged.

If not:

STOP
status = BLOCKED_BASELINE

Create/use a dedicated branch:

cleanup/0.8.2-registry-shims

==================================================
PHASE 1 — COMPLETE SHIM INVENTORY
==================================================

Start from the F08-009 candidate groups:

CORE_PAGES
RECOVERY_TEST_PAGES
SIMPLE_PAGES
WELCOME_PAGES
HUB_PAGES

Do not assume the F08-009 state is still current.

For every symbol record:

- declaration file;
- exact exported value;
- cardinality and Page IDs;
- whether empty, re-export, copy or independent map;
- direct importers;
- barrel re-exports;
- build/script consumers;
- package/export consumers;
- tests;
- canonical source/replacement;
- runtime/build reachability;
- compatibility role;
- disposition candidate.

Allowed dispositions:

EMPTY_RETIRE_CANDIDATE
REEXPORT_RETIRE_CANDIDATE
ACTIVE_COMPATIBILITY_SURFACE
CANONICAL
REVIEW_REQUIRED

Commands/evidence must search active paths separately from backups/docs legacy.

Do not count documentation or backup copies as active consumers.

==================================================
PHASE 2 — REGISTRY PARITY SNAPSHOT
==================================================

Before any future mutation, produce the current canonical snapshot:

- ordered and sorted unique registry IDs;
- ID count;
- duplicates;
- owner/app for every ID;
- source map for every ID;
- bundle membership;
- navigation references;
- virtual-provider output IDs;
- distribution package page IDs for the minimal consumer.

Hash the normalized snapshot.

Required baseline facts:

```text
registryIdSetHash
registryIdCount
bundleOwnedCount
outOfBundleCount
duplicateCount
brokenReferenceCount
```

This snapshot becomes the before/after oracle.

==================================================
PHASE 3 — FIRST MUTATION CANDIDATE
==================================================

The first mutating PR may include only symbols proven:

- empty;
- zero active consumers beyond imports/spreads that can be removed mechanically;
- no package/public export role;
- no compatibility role;
- no Page ID contribution;
- no side effect.

Expected first candidates, subject to evidence:

CORE_PAGES
RECOVERY_TEST_PAGES

HUB_PAGES is explicitly excluded from the first mutation.

SIMPLE_PAGES and WELCOME_PAGES are excluded until re-export consumer and compatibility
analysis is owner-reviewed.

Return before coding:

- exact candidate symbols;
- exact source files;
- exact importer edits;
- exact file allowlist;
- before snapshot/hash;
- expected after snapshot/hash;
- tests;
- package/clean-room gates;
- 0.8.1 compatibility impact;
- rollback.

Stop with:

READY_FOR_OWNER_SHIM_MUTATION_APPROVAL

No source changes in Phase 1.

==================================================
NON-GOALS / PROHIBITED
==================================================

Do not:

- retire HUB_PAGES/hub;
- modify Page IDs;
- modify ApplicationBundle membership;
- redesign PAGES_REGISTRY;
- derive virtualProvider from bundles in this task;
- merge page-registry and provider architecture;
- change PageController or DiscoveryService;
- touch Operations;
- touch templates/assets;
- change package version;
- create a tag;
- push before owner approval;
- use mass search/replace;
- remove re-export shims merely because direct canonical files exist.

==================================================
FUTURE MUTATION GATES
==================================================

For an owner-approved empty-shim PR, verify:

- registry ID set hash unchanged;
- virtual-provider output IDs unchanged;
- bundle ownership unchanged;
- navigation/broken refs unchanged or improved;
- public TypeScript unchanged;
- targeted registry/discovery tests;
- contracts suite;
- full failure-identity comparison;
- build;
- distribution package;
- clean room;
- v0.8.1 compatibility fixture;
- protected-kernel diff;
- lockfile unchanged;
- working tree clean.

==================================================
MANDATORY OUTPUT
==================================================

Return:

- repository/branch/HEAD;
- five-symbol inventory matrix;
- active consumer graph;
- canonical replacement map;
- before registry snapshot and hash;
- first mutation candidate;
- exact file allowlist;
- expected no-op parity proof;
- tests and commands;
- compatibility impact;
- risks and rollback;
- open owner decisions.

Final status:

READY_FOR_OWNER_SHIM_MUTATION_APPROVAL
BLOCKED_BASELINE
BLOCKED_ACTIVE_CONSUMER
BLOCKED_COMPATIBILITY_ROLE
BLOCKED_REGISTRY_PARITY
BLOCKED_UNKNOWN_AUTHORITY

No source change.
No push.
No tag.
```
