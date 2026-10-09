# Open Nexus Program — Maintenance Workflow

```text
Document class:  cross-repository maintenance governance
Lifecycle state: CANDIDATE FOR OWNER RATIFICATION
Version:          1.0
Date:             2026-10-03
Audience:         owner, PM agents, development agents, release agents
```

---

## 1. Purpose

Define the repeatable manual/agent-assisted workflow used to maintain Foundation,
Brain, CLI and the documentation control plane without mixing tasks, losing provenance
or allowing an agent to promote its own work.

This workflow was extracted from the Foundation 0.8.x convergence, distribution and
surface-cleanup program.

Central formula:

```text
Observe
→ Inspect
→ Plan
→ Owner gate
→ Apply
→ Commit locally
→ Verify from a clean tree
→ Owner PR review
→ Push / PR / merge
→ Verify target branch
→ Close and hand off
```

---

## 2. Authority model

```text
Human owner
    decides scope, mutation, merge, release and canonical promotion

PM / architecture agent
    narrows the problem, defines gates and reviews evidence

Development agent
    implements only the approved allowlist

Verification agent
    reproduces commands and compares before/after state

Git
    preserves approved history and provenance

Technical repository
    owns code-coupled truth

Documentation repository
    owns cross-repository governance and program memory
```

No agent may self-authorize:

- a new architecture decision;
- a wider file scope;
- a merge;
- a tag;
- a release;
- a canonical document promotion.

---

## 3. Task classes

### 3.1 FAST

Use for:

- typo;
- stale comment;
- link correction;
- non-normative wording;
- one-file metadata correction.

Required:

```text
exact file
exact diff
targeted check
owner diff review
```

No full release battery unless executable behavior changes.

### 3.2 AUDIT

Read-only.

Produces:

- inventory;
- consumer map;
- authority map;
- evidence matrix;
- candidate decision;
- limits.

An audit never silently becomes a patch.

### 3.3 MUTATION

Changes source or executable behavior.

Requires:

- approved baseline;
- exact file allowlist;
- protected-file list;
- tests;
- rollback;
- owner authorization.

### 3.4 MIGRATION / RETIREMENT

Requires before/after parity and explicit compatibility handling.

```text
preserve useful behavior
migrate ownership/identity
retire old surface
verify no active consumer remains
```

### 3.5 DISTRIBUTION / RELEASE

Requires clean Git provenance, package artifact, clean-room execution and owner release
decision.

### 3.6 INCIDENT

Contain first. Do not continue ordinary work.

Examples:

- secret;
- personal data;
- wrong repository;
- unrelated Git histories;
- dirty working tree during a release build;
- direct master mutation outside authorization.

---

## 4. Session lifecycle in Arena

Arena sessions are repository-scoped and usually branch-scoped.

```text
new session
→ new branch/worktree
→ task
→ commit/push
→ PR
→ merge
→ session considered complete
```

After merge, do not continue long-lived development in the old session. Open a new
session from updated `origin/master`.

At session start:

```bash
pwd
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git remote -v
git fetch origin --prune
git log --oneline --decorate --graph -15
```

Verify:

- correct repository;
- correct branch;
- correct baseline ancestry;
- clean worktree;
- no merge/rebase;
- expected package version;
- expected tags.

If uncertain:

```text
STOP — BASELINE_RECONCILIATION_REQUIRED
```

---

## 5. Branch model

Recommended prefixes:

```text
audit/<release>-<topic>
feature/<release>-<capability>
fix/<release>-<defect>
cleanup/<release>-<surface>
release/<version>
hold/<reason>-<sha>
```

Rules:

- branch from verified `origin/master` or an approved release tag;
- never use an old task branch as an implicit integration branch;
- never merge a historical branch wholesale because it “contains useful things”;
- classify unique commits and cherry-pick only explicitly approved ones;
- no force push without a separate owner decision.

---

## 6. Worktrees and temporary clones

### 6.1 Why worktrees are used

Worktrees permit:

- baseline comparison;
- clean before/after tests;
- simultaneous read-only audits;
- isolated mutation tasks;
- avoiding stashes and branch switching in a dirty checkout.

### 6.2 Preferred location

Prefer a sibling location outside the source tree:

```text
../.worktrees/open-nexus-foundation/<task-id>/
```

Repository-local worktrees such as:

```text
.prov-worktrees/<task-id>/
```

are acceptable only when:

- the directory is ignored by Git;
- build, indexing and scan tools exclude it;
- the worktree is registered by `git worktree list`;
- no package or report includes it.

### 6.3 `.cloned-open-nexus*` directories

Directories such as:

```text
.cloned-open-nexus-*
```

are ephemeral comparison clones, not source authority.

Allowed purposes:

- detached baseline test;
- release-tag verification;
- clean-install simulation.

Required:

- ignored by Git;
- excluded from codebase indexes and package scans;
- no secret copied intentionally;
- no unpushed commit before deletion.

### 6.4 Cleanup

Before removal:

```bash
git worktree list
git -C <worktree> status --short
git -C <worktree> log --oneline --decorate -5
```

Remove registered worktrees with:

```bash
git worktree remove <path>
git worktree prune
```

Do not use `rm -rf` on a registered worktree.

For a plain clone, delete only after verifying:

- no unique branch;
- no unpushed commit;
- no evidence artifact that exists only there.

---

## 7. Read-only planning phase

Every medium/high-risk task begins read-only.

Required output:

```text
repository / branch / HEAD
observed problem
consumer map
authority map
exact current behavior
candidate disposition
exact file allowlist
protected files
commands/tests
rollback
owner decisions
```

The agent stops with one of:

```text
READY_FOR_OWNER_IMPLEMENTATION_APPROVAL
BLOCKED_<reason>
NO_CHANGE_REQUIRED
```

No source mutation before owner approval.

---

## 8. Exact allowlist

An allowlist names exact paths.

Valid:

```text
src/config/example.ts
tests/contracts/example.test.ts
```

Invalid:

```text
dashboard.ts and/or index.ts
the related tests
src/**
whatever is necessary
```

If implementation reveals a missing file:

```text
STOP
→ request allowlist amendment
```

No `git add .` or `git add -A` for scoped tasks.

Use explicit staging:

```bash
git add <approved-path-1> <approved-path-2>
```

---

## 9. Protected surfaces

Each repository defines protected files/contracts.

Foundation protected symbols include, unless an approved RFC says otherwise:

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

A task that expects zero protected diff must verify the complete protected list, not a
subset.

---

## 10. Pre-commit verification

Before commit:

```bash
git status --short
git diff --check
git diff --stat
git diff
git diff --cached --check
git diff --cached --name-status
git diff --cached
```

Run task-appropriate targeted tests.

For source mutations also run as required:

- public TypeScript;
- full failure-identity comparison;
- build;
- contract suites;
- protected diff.

A count-only comparison is insufficient when a baseline already has failures.

---

## 11. Commit-before-package rule

Release provenance requires the package source to match a commit.

Therefore:

```text
source mutation
→ pre-commit tests
→ local commit
→ clean worktree
→ package generation
→ clean-room verification
→ owner review
→ push
```

Do not produce a `GIT_VERIFIED` package from staged/uncommitted source.

If the tree is dirty:

```text
default           REJECT
explicit override WORKTREE_UNVERIFIED / releaseEligible=false
```

---

## 12. Post-commit verification

After local commit:

```bash
git status --short
git rev-parse HEAD
```

Required for distribution tasks:

```text
sourceCommit       = HEAD
sourceCommitOrigin = GIT_VERIFIED
worktreeState      = CLEAN
releaseEligible    = true
```

Then run package/materialization/clean-room gates.

Package byte hashes may change because provenance includes the new commit. Compare
semantic inventory separately when verifying no-op cleanup:

- Page IDs;
- template set;
- assets;
- routes;
- capabilities;
- package tree shape.

---

## 13. Provenance validation modes

```text
shape
    diagnostic/legacy inspection; never implies release eligibility

release
    default public validator mode; requires complete provenance
```

Release acceptance requires:

```text
sourceCommitOrigin = GIT_VERIFIED
worktreeState = CLEAN
releaseEligible = true
```

Missing fields fail closed.

---

## 14. Push and PR

Push only the task branch:

```bash
git push -u origin <task-branch>
```

No direct push to `master`.

If `gh` is unavailable, open the GitHub compare URL manually. Lack of CLI tooling is not
permission to bypass the PR.

Before merge verify:

- expected base/head repository;
- exact file list;
- CI/checks or documented local gate battery;
- no unrelated commits;
- no version/tag unless authorized.

After owner approval, merge through the PR.

---

## 15. Post-merge closure

Verify the commit is contained in remote master:

```bash
git fetch origin --prune
git branch -r --contains <commit-sha>
```

Expected:

```text
origin/master
```

Then:

- mark task DONE;
- update the project backlog/report;
- close/delete task branch according to policy;
- create a new branch/worktree for the next task;
- never continue implicitly from the old branch.

---

## 16. Release tags

Create tags only after:

- PR merged;
- final master tree verified;
- release report approved;
- smoke/conformance run on the final tree.

Annotated immutable tag:

```bash
git tag -a vX.Y.Z <release-commit> -m "..."
git push origin vX.Y.Z
```

Never move or replace an existing release tag.

Use release labels such as “Stable” or “Green Line” in release metadata rather than a
moving `stable` tag.

---

## 17. Documentation and control-plane reporting

Technical repositories retain:

- implementation reports;
- test evidence;
- code-coupled ADR/backlogs.

The documentation control plane receives:

- project status;
- provenance reports;
- cross-repository decisions;
- links/hashes to technical evidence.

Do not copy complete technical report trees into the central repository.

Fast status flow:

```text
technical repo
→ metadata report YAML
→ local documentation tmp spool
→ Arena documentation session
→ owner-reviewed CURRENT-STATE / PROGRAM-STATE update
```

---

## 18. Maintenance fast path vs strict path

### Fast path

For comment/typo/non-executable changes:

```text
exact diff
one targeted test/check
commit
PR
```

Do not run clean-room for a comment-only patch.

### Strict path

For source, contract, migration, packaging, provenance, security and release:

```text
read-only plan
owner gate
exact allowlist
pre-commit tests
local commit
clean-tree package
clean-room
owner PR review
```

---

## 19. Failure and stop conditions

Stop rather than improvise when:

```text
wrong repository/branch
working tree contains unrelated edits
baseline/tag ancestry differs
allowlist is incomplete
protected diff appears
new failure identity appears
package source is dirty
consumer/authority is ambiguous
security/personal data is encountered
remote history is unrelated
```

Return a precise `BLOCKED_*` status and the evidence required for the owner decision.

---

## 20. Current Foundation 0.8.x state

Verified program direction at the time of this document:

```text
v0.8.1
    Distribution Green Line
    artifact-centric package, manifest, clean-room, Admin/Frontend

0.8.2
    Surface Convergence and Hygiene
    one bounded cleanup class per PR

PROV-082-001/A
    dirty-worktree provenance gate implemented; merge status must be verified in Git

SURF-082-002
    empty registry shim convergence implemented; merge status must be verified

SURF-082-003
    stale-reference comment cleanup implemented/pushed; merge status pending verification

SURF-082-001
    AI Pages panel host migration PARKED; blocks VirtualPageTemplate retirement only

Operations V1
    Component Catalog → Discovery promotion PARKED

0.9
    Semantic Entity Projection frozen pending the selected 0.8.x integration target
```

This state section is a snapshot. Git commands and repository reports remain the
technical authority.

---

## 21. Owner checklist

Before authorizing implementation:

```text
□ correct repository/branch
□ clean tree
□ baseline/tag verified
□ exact allowlist
□ authority/consumer evidence
□ protected files listed
□ tests and rollback
□ no hidden scope expansion
```

Before authorizing push/PR:

```text
□ commit SHA
□ exact diff
□ tests/gates
□ package/clean-room when required
□ provenance clean
□ lockfile explained
□ no unrelated files
```

Before authorizing release:

```text
□ master contains all approved commits
□ final tree tested
□ report ratified
□ version correct
□ immutable tag target verified
□ deferred observations recorded
```

---

## 22. Milestone

This workflow is itself a program milestone:

> Maintenance has moved from ad-hoc founder memory and agent initiative to a
> reproducible, evidence-driven, owner-gated operating model.

The objective is not maximum ceremony. The objective is to make small work fast and
high-risk work safe while allowing a new agent to continue without reconstructing the
project from chat history.
