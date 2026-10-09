# PROV-082-001 — Dirty Working Tree Provenance

Use this prompt in a new clean Arena session attached to the Foundation repository,
after the defaults-retirement PR is merged to `master`.

---

## Prompt

```text
# PROV-082-001 — Dirty Working Tree Provenance

ROLE:
Foundation Distribution Provenance Agent

MODE:
STRICT BOUNDED IMPLEMENTATION

OBJECTIVE:
Prevent the distribution producer from labeling an artifact `GIT_VERIFIED` when the
bytes used for production come from a staged, modified or untracked working tree that
does not match HEAD.

Current defect:

working tree dirty
+ producer records HEAD
→ sourceCommitOrigin = GIT_VERIFIED

Required invariant:

clean Git tree matching HEAD
→ GIT_VERIFIED

staged/unstaged/untracked non-ignored content
→ reject by default before artifact creation

explicit development override
→ WORKTREE_UNVERIFIED
→ never release-eligible

==================================================
PHASE 0 — BASE AND REPOSITORY GATE
==================================================

Before modifying:

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
- defaults-retirement PR is present in origin/master;
- working tree is clean;
- no merge/rebase active;
- package version remains 0.8.1 unless an approved 0.8.2 release task says otherwise;
- PROV-082-001 exists in the findings register.

If not:

STOP
status = BLOCKED_BASELINE

Create or use a dedicated branch:

fix/0.8.2-dirty-worktree-provenance

Do not continue in a checkout containing unrelated edits.

==================================================
PHASE 1 — REALITY CHECK
==================================================

Inspect the actual producer command path:

package.json
scripts/distribution-produce.mjs
scripts/distribution-produce.ts
scripts/distribution-producer-core.ts
manifest schema
producer/CLI tests

Return before coding:

- where sourceCommit is obtained;
- where sourceCommitOrigin is assigned;
- when output directories/files are created;
- current exit-code contract;
- current unverified-source override;
- exact file allowlist;
- tests to add;
- whether schema already supports WORKTREE_UNVERIFIED.

Stop with:

READY_FOR_OWNER_IMPLEMENTATION_APPROVAL

No source changes in this first response.

==================================================
TARGET BEHAVIOR
==================================================

## Default release/development behavior

Before reading live ApplicationBundle data or creating output artifacts, execute an
exact Git worktree check equivalent to:

```text
git status --porcelain=v1 -z --untracked-files=all
```

Properties:

- staged tracked change → dirty;
- unstaged tracked change → dirty;
- non-ignored untracked file → dirty;
- ignored file → not dirty;
- output directory must be external/ignored and must not make the source dirty;
- NUL-delimited parsing; no line/whitespace assumptions;
- no shell interpolation from paths.

Dirty default result:

```text
error code: DIRTY_WORKTREE
exit: 1 / REJECT
artifact files created: 0
sourceCommitOrigin: not emitted because no artifact exists
```

Usage/runner errors remain exit 2.

## Explicit override

Candidate option:

```text
--allow-dirty-source
```

Allowed only for development/test, never release mode.

With override:

```text
sourceCommit = current HEAD
sourceCommitOrigin = WORKTREE_UNVERIFIED
releaseEligible = false
```

Record only non-sensitive metadata:

```text
dirtyEntryCount
worktreeStateDigest
```

Do not embed:

- diff body;
- source content;
- secret value;
- full personal path unless already governed.

`worktreeStateDigest` may hash a deterministic inventory of status class, repository-
relative path and file/content hash. The report/manifest must define exactly what it
covers.

If the existing manifest schema cannot represent `WORKTREE_UNVERIFIED` without an
additive compatible change, stop for owner approval before schema modification.

## Release mode

Any command/CI path used for release must reject:

```text
CALLER_UNVERIFIED
WORKTREE_UNVERIFIED
```

Only:

```text
GIT_VERIFIED
```

is release-eligible.

==================================================
TOCTOU SAFETY
==================================================

Check worktree state:

1. before source/model reads and before output creation;
2. immediately before final atomic publication of the artifacts.

If the tree changes during production:

```text
WORKTREE_CHANGED_DURING_BUILD
→ reject
→ remove temporary artifacts
→ publish no final artifact
```

Use temporary output + atomic move where the current producer architecture permits.
Do not silently retain a partially published package.

==================================================
TEST MATRIX
==================================================

Use synthetic temporary Git repositories. Do not mutate the real Foundation checkout
inside tests.

Required tests:

1. clean tree → GIT_VERIFIED;
2. staged modification → DIRTY_WORKTREE, no artifact;
3. unstaged modification → DIRTY_WORKTREE, no artifact;
4. untracked non-ignored source → DIRTY_WORKTREE, no artifact;
5. ignored file → clean/GIT_VERIFIED;
6. dirty tree + explicit override → WORKTREE_UNVERIFIED;
7. unverified artifact → release validator rejects it;
8. clean tree after commit → new HEAD/GIT_VERIFIED;
9. output outside source tree does not dirty the source;
10. paths with spaces/newlines are parsed safely through NUL format;
11. Git unavailable → fail closed unless an existing explicit caller-unverified mode
    is used, and that result remains release-ineligible;
12. tree changes during build → no final artifact;
13. no diff body/source content appears in provenance metadata;
14. existing clean producer/package hashes remain deterministic.

==================================================
PROHIBITED
==================================================

- unrelated page/template cleanup;
- Operations changes;
- Foundation protected-kernel changes;
- new runtime capability;
- package version bump;
- release tag;
- force push;
- direct default-branch push;
- broad `.gitignore` rules hiding source changes;
- weakening GIT_VERIFIED semantics;
- treating only staged changes as dirty while ignoring unstaged/untracked changes.

==================================================
QUALITY GATES
==================================================

After implementation run:

- targeted producer CLI tests;
- distribution hash-model tests;
- live pipeline clean-room tests;
- contract suite;
- public TypeScript;
- build;
- package/clean-room from a clean tree;
- explicit dirty-tree rejection probe;
- protected-kernel diff;
- lockfile diff;
- full failure-identity comparison;
- git status.

Every result records command, cwd, exit code and artifact/log path.

==================================================
DOCUMENTATION
==================================================

Update the existing PROV-082-001 finding with:

- root cause;
- invariant;
- implementation commit;
- tests;
- release impact;
- closure status.

Do not mark CLOSED before the clean and dirty probes both pass.

==================================================
FINAL OUTPUT
==================================================

Return:

- branch/base/HEAD;
- changed files;
- sourceCommit/sourceCommitOrigin behavior;
- dirty-check implementation;
- TOCTOU behavior;
- test matrix results;
- clean package provenance;
- dirty rejection evidence;
- release-validator evidence;
- protected diff;
- lockfile status;
- full failure-set comparison;
- findings-register update;
- PR-ready diff;
- open risks.

Final status:

READY_FOR_OWNER_PR_REVIEW
BLOCKED_BASELINE
BLOCKED_SCHEMA_DECISION
BLOCKED_DIRTY_CHECK
BLOCKED_TOCTOU
BLOCKED_RELEASE_VALIDATOR
BLOCKED_REGRESSION

No push until owner approval.
No version bump.
No tag.
```
