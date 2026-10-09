# SURF-082-005 — Registry Consumer Repointing and Shim Retirement

Use this prompt in a new clean Arena session after the currently active documentation
or route-reality task is safely separated. This task may proceed independently from
Hello API/Redis reference review only if the repository worktree and branch are clean.

---

## Prompt

```text
# SURF-082-005 — Registry Consumer Repointing and Re-export Shim Retirement

ROLE:
Foundation Registry Consumer Convergence Agent

MODE:
STRICT READ-ONLY PLAN FIRST

OWNER CORRECTION:
The PageDefinition write authority is already single and canonical under:

src/applications/<app>/pages

The files under src/config/discovery/page-registry/pages are compatibility re-exports,
not a second definition authority.

OBJECTIVE:
Make page-registry/index import canonical application page maps directly, make
virtualProvider consume one PAGES_REGISTRY composition, then retire re-export-only
shims without changing any Page ID, PageMeta object, owner, order, bundle, navigation,
package or runtime behavior.

==================================================
PHASE 0 — BASELINE GATE
==================================================

Run:

pwd
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git remote -v
git fetch origin --prune
git log --oneline --decorate --graph -15
git worktree list

Verify:

- branch derives from current origin/master;
- provenance hardening is merged;
- defaults retirement is merged;
- empty CORE_PAGES/RECOVERY_TEST_PAGES shim retirement is merged;
- stale-reference cleanup is merged or explicitly independent;
- working tree clean;
- no merge/rebase;
- package version remains 0.8.1;
- v0.8.1 tag unchanged.

Create/use:

cleanup/0.8.2-registry-consumer-repointing

If not:

STOP
status = BLOCKED_BASELINE

==================================================
PHASE 1 — VERIFY THE CORRECTED PREMISE
==================================================

For each symbol verify declaration identity and all importers:

AUTH_PAGES
CORE_ADMIN_PAGES
HUB_PAGES
OPEN_NEXUS_PAGES
SIMPLE_PAGES
WELCOME_PAGES
SYSTEM_PAGES
TOOLS_PAGES

Candidate canonical sources:

src/applications/auth/pages
src/applications/core-admin/pages
src/applications/open-nexus/pages
src/applications/simple/pages
src/applications/system/pages

Candidate shim files:

src/config/discovery/page-registry/pages/auth.ts
src/config/discovery/page-registry/pages/core-admin/index.ts
src/config/discovery/page-registry/pages/open-nexus/index.ts
src/config/discovery/page-registry/pages/simple/simple-pages.ts
src/config/discovery/page-registry/pages/welcome.ts
src/config/discovery/page-registry/pages/hub.ts
src/config/discovery/page-registry/pages/sys/core.ts
src/config/discovery/page-registry/pages/sys/tools.ts

For every shim record:

- exact source text;
- export type: re-export / export-star / empty map / independent value;
- direct importers;
- barrel importers;
- package/public export role;
- tests;
- compatibility role;
- canonical replacement import;
- disposition.

Do not assume zero consumers from the file content alone.

==================================================
PHASE 2 — IMPORT CYCLE AND IDENTITY CHECK
==================================================

Before proposing direct canonical imports, verify:

- no circular import is introduced;
- canonical application page modules do not import the registry barrel;
- object identity/shape remains equivalent;
- app/owner fields remain unchanged;
- import order does not change observable PageRecord order;
- AUTH_PAGES no longer requires a special path;
- HUB_PAGES remains active and is not retired in this task.

If direct imports introduce a cycle:

STOP
status = BLOCKED_IMPORT_CYCLE

==================================================
PHASE 3 — BEFORE SNAPSHOT
==================================================

Produce normalized before-state:

- ordered registry entries;
- sorted unique Page IDs;
- registry ID hash;
- Page ID → owner/app map;
- Page ID → source canonical module map;
- virtualProvider ordered output;
- virtualProvider sorted ID hash;
- duplicate count;
- broken-reference count;
- bundle membership;
- package semantic inventory for the minimal consumer.

Record both sorted-set parity and observable order parity.

==================================================
PHASE 4 — PROPOSED MUTATION
==================================================

Candidate target:

1. page-registry/index imports canonical maps directly from applications/*/pages;
2. page-registry/index produces the same PAGES_REGISTRY ordering and IDs;
3. virtualProvider imports/consumes PAGES_REGISTRY only;
4. re-export-only shim files are deleted;
5. empty sys/tools.ts is deleted if zero compatibility/public consumers;
6. backups directory remains untouched.

Before coding return:

- exact file allowlist;
- exact import replacement matrix;
- exact deleted files;
- cycle analysis;
- before snapshot/hashes;
- expected after snapshot/hashes;
- tests;
- package/clean-room impact;
- v0.8.1 compatibility impact;
- rollback.

Stop with:

READY_FOR_OWNER_REGISTRY_REPOINTING_APPROVAL

No source changes in the first response.

==================================================
PROHIBITED
==================================================

Do not:

- retire hub/HUB_PAGES;
- change Page IDs;
- change object fields;
- change ApplicationBundle membership;
- modify ApplicationDefinition;
- redesign Discovery;
- modify PageController or DiscoveryService;
- modify templates/assets;
- touch page-registry/backups;
- change Operations;
- change version/tag;
- use broad search/replace;
- retain a second manually composed allPages list in virtualProvider.

==================================================
FUTURE MUTATION GATES
==================================================

For an approved implementation:

- exact source allowlist;
- targeted page-registry/virtual-provider tests;
- import-cycle check;
- public TypeScript;
- full failure-identity comparison;
- build;
- before/after ordered registry parity;
- sorted registry hash parity;
- virtualProvider ordered/set parity;
- bundle ownership parity;
- broken-reference parity;
- package semantic inventory parity;
- clean-room;
- v0.8.1 compatibility fixture;
- protected-kernel diff;
- lockfile unchanged;
- clean-tree GIT_VERIFIED provenance.

After mutation, commit locally before package generation.

==================================================
MANDATORY OUTPUT
==================================================

Return:

- repository/branch/HEAD;
- corrected authority proof;
- shim/importer matrix;
- public/package compatibility findings;
- cycle analysis;
- before registry/provider snapshots;
- exact proposed diff/allowlist;
- deleted-file list;
- test/gate plan;
- compatibility/rollback;
- open owner decisions.

Final status:

READY_FOR_OWNER_REGISTRY_REPOINTING_APPROVAL
BLOCKED_BASELINE
BLOCKED_ACTIVE_SHIM_CONSUMER
BLOCKED_PUBLIC_IMPORT_COMPATIBILITY
BLOCKED_IMPORT_CYCLE
BLOCKED_ORDER_PARITY
BLOCKED_UNKNOWN_AUTHORITY

No source change.
No push.
No tag.
No version bump.
```
