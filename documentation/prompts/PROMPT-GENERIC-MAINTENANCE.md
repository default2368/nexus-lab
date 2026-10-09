# Generic Maintenance Agent Prompt

Use this template in an Arena session attached to the target technical repository.
Replace every `<PLACEHOLDER>` before execution.

---

## Prompt

```text
# <TASK_ID> — <TASK_TITLE>

ROLE:
<AGENT_ROLE>

REPOSITORY:
<EXPECTED_REPOSITORY>

TASK CLASS:
<FAST | AUDIT | MUTATION | MIGRATION | DISTRIBUTION | RELEASE | INCIDENT>

MODE:
READ-ONLY PHASE 1, followed by owner-gated mutation when applicable

BASELINE:
<origin/master | release tag | verified commit>

OBJECTIVE:
<ONE SENTENCE — what observable condition must become true?>

OUT OF SCOPE:
- <EXPLICIT NON-GOAL 1>
- <EXPLICIT NON-GOAL 2>
- unrelated refactor;
- version/tag/release unless explicitly authorized.

==================================================
PHASE 0 — REPOSITORY / SESSION GATE
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

- exact repository identity;
- expected branch/baseline ancestry;
- clean working tree;
- no merge/rebase active;
- expected package version/tag;
- no unrelated agent edits;
- worktree/clone directories excluded from Git, indexing and package scans.

If any condition fails:

STOP
status = BLOCKED_BASELINE_OR_WORKTREE

Do not reset, clean, stash, rebase or force push.

==================================================
PHASE 1 — OBSERVE AND CLASSIFY
==================================================

Read the relevant:

- AGENTS.md;
- backlog task;
- ADR/PRD/Epic;
- evidence reports;
- source files;
- tests;
- package/export configuration.

For every codebase claim provide:

command
file:line
result
epistemic classification

Use:

OBSERVED
INFERRED
PROPOSED
DECIDED
UNKNOWN
CONFLICTING
LIMIT

Produce:

1. current behavior;
2. consumer/import graph;
3. authority/owner;
4. before-state metrics/hash;
5. candidate change;
6. compatibility impact;
7. risks;
8. rollback.

==================================================
PHASE 2 — EXACT PLAN
==================================================

Return before coding:

Task outcome target:
<MEASURABLE TARGET>

Exact allowed files:
- <PATH 1>
- <PATH 2>

Protected/forbidden files:
- <PATH OR SYMBOL 1>
- <PATH OR SYMBOL 2>

Commands/tests:
- <COMMAND 1>
- <COMMAND 2>

Expected before/after invariants:
- <INVARIANT 1>
- <INVARIANT 2>

Rollback:
<ROLLBACK PROCEDURE>

Stop with:

READY_FOR_OWNER_IMPLEMENTATION_APPROVAL

No source changes in the first response unless TASK CLASS = FAST and the owner has
explicitly authorized direct execution.

==================================================
OWNER GATE
==================================================

Do not implement until the owner approves:

- baseline;
- exact allowlist;
- protected list;
- expected behavior;
- test plan;
- compatibility impact;
- rollback.

If implementation needs another file:

STOP
status = BLOCKED_ALLOWLIST_AMENDMENT

==================================================
PHASE 3 — MUTATION
==================================================

Apply only the approved diff.

Rules:

- no global formatter;
- no mass replacement;
- no `git add .` / `git add -A`;
- no unrelated cleanup;
- no test weakening;
- no silent fallback;
- no new dependency unless approved;
- no lockfile change unless approved.

Stage exact files only.

==================================================
PHASE 4 — PRE-COMMIT GATES
==================================================

Run:

git status --short
git diff --check
git diff --stat
git diff
git diff --cached --check
git diff --cached --name-status
git diff --cached

Then run the approved targeted/type/build/full-failure gates.

For baseline-red suites compare failing identities, not counts only.

If a protected or unexpected diff appears:

STOP
status = BLOCKED_SCOPE_OR_REGRESSION

==================================================
PHASE 5 — LOCAL COMMIT
==================================================

Commit message:

<APPROVED COMMIT MESSAGE>

Do not push yet.

After commit:

```bash
git status --short
git rev-parse HEAD
```

Expected:

working tree clean

==================================================
PHASE 6 — POST-COMMIT / PROVENANCE GATES
==================================================

For packaging/distribution tasks require:

sourceCommit       = HEAD
sourceCommitOrigin = GIT_VERIFIED
worktreeState      = CLEAN
releaseEligible    = true

Run required package/materialization/clean-room/compatibility gates only from the clean
committed tree.

For no-op cleanup compare semantic inventory separately from byte/package hashes.

==================================================
PHASE 7 — OWNER PR REVIEW
==================================================

Return:

repository / branch / base / HEAD
commit SHA
exact diff
changed files
tests and exit codes
before/after metrics
compatibility result
package/clean-room result when applicable
protected diff
lockfile status
git status
risks
PR-ready description

Final status:

READY_FOR_OWNER_PR_REVIEW
BLOCKED_BASELINE_OR_WORKTREE
BLOCKED_ALLOWLIST_AMENDMENT
BLOCKED_SCOPE_OR_REGRESSION
BLOCKED_COMPATIBILITY
BLOCKED_PACKAGE
BLOCKED_CLEAN_ROOM

No push before owner approval.

==================================================
PHASE 8 — PUSH / PR / MERGE
==================================================

After owner approval:

- push only the task branch;
- open PR toward the approved base;
- verify exact file list;
- merge only after review/checks;
- never substitute direct master push because `gh` is unavailable.

After merge verify:

```bash
git fetch origin --prune
git branch -r --contains <COMMIT_SHA>
```

Expected:

origin/master

Then close the task and create a new branch/worktree for the next task.

==================================================
FINAL RULE
==================================================

Small work should remain small.
High-risk work must remain observable.
No agent decides its own authority, scope, merge or release.
```
