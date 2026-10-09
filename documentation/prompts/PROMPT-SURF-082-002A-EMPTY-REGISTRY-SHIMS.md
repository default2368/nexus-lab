# SURF-082-002A — Empty Registry Shim Retirement

Use this prompt on branch:

```text
cleanup/0.8.2-registry-shims
```

The branch must derive from current `origin/master` after PROV-082-001A.

---

## Prompt

```text
# SURF-082-002A — Empty Registry Shim Retirement

ROLE:
Foundation Registry Cleanup Agent

MODE:
STRICT FOUR-FILE MUTATION

OWNER DECISIONS:

D1 branch/baseline approved.
D2 four-file allowlist approved.
D3 SIMPLE_PAGES/WELCOME_PAGES deferred.
D4 HUB_PAGES/hub untouched.

OBJECTIVE:
Remove only the empty CORE_PAGES and RECOVERY_TEST_PAGES compatibility maps without
changing any Page ID, owner, bundle membership, route, navigation, template, asset,
package surface or runtime behavior.

==================================================
EXACT ALLOWLIST
==================================================

MODIFY:

src/config/discovery/page-registry/index.ts
src/config/discovery/providers/virtual-provider.ts

DELETE:

src/config/discovery/page-registry/pages/home/main.ts
src/config/discovery/page-registry/pages/test/recovery-pages.ts

No other file is allowed in the implementation commit.

==================================================
PROHIBITED
==================================================

Do not modify:

- SIMPLE_PAGES;
- WELCOME_PAGES;
- HUB_PAGES or hub;
- Page IDs;
- ApplicationBundle membership;
- navigation;
- routing;
- templates;
- assets;
- Operations;
- Foundation protected kernel;
- package.json;
- package-lock.json;
- version;
- tags;
- aliases;
- backups or docs legacy.

Do not redesign PAGES_REGISTRY or virtualProvider.
Do not derive registry/provider data from a new source in this task.
Do not format unrelated code.

==================================================
PHASE 0 — BASELINE
==================================================

Run:

pwd
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git remote -v
git fetch origin --prune
git log --oneline --decorate --graph -12

Verify:

- branch is cleanup/0.8.2-registry-shims;
- branch derives from current origin/master;
- PROV-082-001A is present in origin/master;
- working tree is clean;
- no merge/rebase active;
- package version remains 0.8.1.

If not:

STOP
status = BLOCKED_BASELINE

==================================================
PHASE 1 — BEFORE SNAPSHOT
==================================================

Recompute, do not copy from the report:

registryIdCount
uniqueCount
duplicateCount
registryIdSetHash
virtualProviderCount
vpSameSetAsRegistry
bundle owner mapping
brokenReferenceCount

Expected before values:

registryIdCount       = 37
uniqueCount           = 37
duplicateCount        = 0
registryIdSetHash     = sha256:9a4e010c40f0ef478295b6f89d158746a0aa7e951eb35030feb1b5936cba2397
virtualProviderCount  = 37
vpSameSetAsRegistry   = true

Verify again:

CORE_PAGES = {}
RECOVERY_TEST_PAGES = {}

and confirm zero Page IDs contributed by each.

If values differ:

STOP
status = BLOCKED_REGISTRY_PARITY

==================================================
PHASE 2 — MUTATION
==================================================

Apply only:

1. remove CORE_PAGES import/spread/re-export from page-registry/index.ts;
2. remove RECOVERY_TEST_PAGES import/spread/re-export from page-registry/index.ts;
3. remove both names/imports/spreads from virtual-provider.ts;
4. delete the two now-unused declaration files.

Do not change ordering or formatting of unrelated registry entries.

==================================================
PHASE 3 — AFTER SNAPSHOT
==================================================

Recompute the complete snapshot.

Require exact equality:

registryIdCount       37
uniqueCount           37
duplicateCount        0
registryIdSetHash     sha256:9a4e010c40f0ef478295b6f89d158746a0aa7e951eb35030feb1b5936cba2397
virtualProviderCount  37
vpSameSetAsRegistry   true
bundle owner mapping  unchanged
brokenReferenceCount  unchanged or improved

If any semantic value changes:

STOP
status = BLOCKED_REGISTRY_PARITY

==================================================
PHASE 4 — PRE-COMMIT GATES
==================================================

Run:

- targeted page-registry/virtual-provider/discovery tests;
- application contract/smoke tests;
- public TypeScript;
- full failure-identity comparison;
- Foundation build;
- protected-kernel diff;
- lockfile diff;
- exact allowlist diff.

Package generation is not release-eligible while the mutation is uncommitted. Do not
mislabel staged-tree evidence as GIT_VERIFIED.

If gates pass, create one local commit:

refactor(discovery): remove empty legacy registry shims

Commit body:

Remove CORE_PAGES and RECOVERY_TEST_PAGES empty compatibility maps.
The registry ID set, virtual-provider output and bundle ownership remain unchanged.

Do not push yet.

==================================================
PHASE 5 — POST-COMMIT CLEAN-TREE GATES
==================================================

Require:

git status --porcelain → empty
sourceCommitOrigin = GIT_VERIFIED
worktreeState = CLEAN
releaseEligible = true

Then run:

- live producer;
- validator;
- materializer;
- package filesystem inventory;
- clean-room;
- 0.8.1 compatibility fixture;
- Admin read-model verification;
- exact package semantic inventory comparison.

The package byte hash may change because sourceCommit changes.
Compare semantic surfaces:

page ID set
template set
asset set
route set
capability set
package tree shape

They must remain equivalent.

==================================================
FINAL OUTPUT
==================================================

Return:

- branch/base/HEAD;
- commit SHA;
- exact diff;
- before/after registry snapshots and hashes;
- targeted tests;
- public TypeScript;
- full failure identity;
- build result;
- package provenance and hashes;
- semantic package comparison;
- clean-room result;
- 0.8.1 compatibility result;
- protected diff;
- lockfile status;
- git status;
- risks.

Final status:

READY_FOR_OWNER_PR_REVIEW
BLOCKED_BASELINE
BLOCKED_REGISTRY_PARITY
BLOCKED_REGRESSION
BLOCKED_PACKAGE_COMPATIBILITY

Do not push.
Do not tag.
Do not bump version.
```
