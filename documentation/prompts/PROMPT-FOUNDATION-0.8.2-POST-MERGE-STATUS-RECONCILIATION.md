# Foundation 0.8.2 — Post-Merge Documentation Status Reconciliation

Use this prompt in a new Arena session only after the owner has merged
`incident/0.8.2-client-credential-boundary` and verified that commit `81c4d7b` is an
ancestor of current `origin/master`.

---

## Prompt

```text
# Foundation 0.8.2 — Post-Merge Documentation Status Reconciliation

ROLE:
Foundation Documentation Status Reconciliation Agent

TASK CLASS:
FAST

MODE:
STRICT READ-ONLY VERIFY FIRST, THEN OWNER-GATED TWO-FILE MUTATION

ACTIVE WRITER:
ARENA

PURPOSE:
Reconcile the two governing 0.8.2 ledgers with Git after the merge of:

- PR #9 tracked credential containment;
- PR #8 documentation reconciliation;
- PR #5 AI Pages Panel collision resolution;
- the client credential boundary PR headed by 81c4d7b.

This task updates status only. It does not change architecture, source code or task
scope.

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
git rev-parse origin/master
git log --oneline --decorate --merges -12 origin/master
git worktree list

Required:

- repository = default2368/open-nexus-foundation;
- Arena session branch derives from current origin/master;
- working tree clean;
- no merge/rebase/cherry-pick;
- v0.8.1 annotated tag and peeled commit unchanged.

Verify:

git merge-base --is-ancestor \
  8d7c9f690e8a9be15d12a0baeb56f458a9e00610 \
  origin/master

git merge-base --is-ancestor \
  facddeb239f0d1b187f6c0ab93912bd96f61f039 \
  origin/master

git merge-base --is-ancestor \
  ed8dcc20d43341e6553de97d38b85ba42cdc37d7 \
  origin/master

git merge-base --is-ancestor \
  81c4d7b7864953a80c35cca2b9de9a04893aecbc \
  origin/master

All four commands must exit 0.

If any command fails:

STOP
status = BLOCKED_MERGE_BASELINE

==================================================
EXACT ALLOWLIST
==================================================

docs/reports/0.8/0.8.2-FINDINGS-REGISTER.md
docs/reports/0.8/0.8.2-SURFACE-CONVERGENCE-BACKLOG.md

Exactly two files.

No other path is authorized.

==================================================
PHASE 1 — READ-ONLY STATUS RECONCILIATION
==================================================

Read the two allowlisted documents and compare every relevant status with Git.

At minimum inspect:

SEC-082-002
SURF-082-001
SURF-082-003
SURF-082-005
SURF-082-006
SURF-082-007
PR #5
PR #8
PR #9
client credential boundary merge

Return exact stale lines and proposed replacements.

Required SEC-082-002 status direction:

CLOSED_CURRENT_TREE
HISTORY_REWRITE_DEFERRED

The record must state, without credential details:

- provider credential rotated;
- replacement deployed server-side;
- old credential rejection verified;
- tracked current-tree literal removed;
- hygiene files removed;
- client credential alias retired;
- browser/server boundary enforced;
- guard passing;
- historical Git objects still contain revoked material;
- no history rewrite authorized.

Do not state generic “security incident fully closed” if historical or provider
follow-ups remain.

Required SURF-082-001 direction:

- PR #5 is MERGED;
- cite head ed8dcc2 and merge evidence;
- distinguish merged implementation from any remaining Definition-of-Done observation;
- do not claim VirtualPageTemplate retired unless Git proves it;
- do not claim all AI page migration complete merely because the collision PR merged.

Required SURF-082-005 direction:

READY_FOR_READ_ONLY_EXECUTION

only if:

- SURF-082-002 is merged;
- documentation plan is present;
- current origin/master contains the required predecessors.

Do not mark source mutation started or complete.

Verify no canonical task IDs:

SEC-082-002A
SEC-082-002B

are introduced.

==================================================
PHASE 2 — RETURN PLAN BEFORE EDITING
==================================================

Return:

- current origin/master SHA;
- merge evidence;
- exact stale lines;
- exact replacement text;
- exact two-file diff plan;
- status transitions;
- tests/checks;
- rollback.

Stop with:

READY_FOR_OWNER_DOC_STATUS_MUTATION_APPROVAL

Do not edit in the first response.

==================================================
FUTURE MUTATION — ONLY AFTER OWNER APPROVAL
==================================================

When approved:

- modify exactly the two allowlisted files;
- do not alter task scope;
- do not add architecture;
- do not change source/test/package files;
- do not repeat credential values, prefixes, suffixes, lengths or fingerprints;
- do not renumber tasks;
- do not modify historical evidence outside current status wording.

Verification:

git status --short
git diff --check
git diff --name-status
git diff --stat

Changed set must contain exactly two files.

Stage only with explicit git add paths.

Commit:

docs(0.8.2): reconcile merged task statuses

Push only the Arena session branch.

No direct master push.
No merge by the agent.

==================================================
PROHIBITED
==================================================

No source changes.
No tests/package/lockfile changes.
No tag/version changes.
No history rewrite.
No force push.
No new task.
No Assistant/Brain/CLI work.
No SURF-082-005 source mutation.
No PR merge.

==================================================
MANDATORY OUTPUT
==================================================

Return:

OBSERVED
INFERRED
PROPOSED
DECIDED
UNKNOWN
CONFLICTING
LIMIT

Final statuses:

READY_FOR_OWNER_DOC_STATUS_MUTATION_APPROVAL
READY_FOR_OWNER_DOC_STATUS_PR_REVIEW
BLOCKED_MERGE_BASELINE
BLOCKED_UNEXPECTED_DIFF
BLOCKED_STATUS_AMBIGUITY

No merge.
```

---

## Lifecycle after this task

```text
Arena read-only report
→ owner approval
→ Arena two-file mutation
→ local commit + push Arena branch
→ owner PR review and merge
→ verify current origin/master
→ close Arena session
→ open a new Arena session for SURF-082-005
```

The SURF-082-005 session must use:

```text
documentation/prompts/PROMPT-SURF-082-005-REGISTRY-CONSUMER-REPOINTING.md
```

and must derive from the master that contains this status-reconciliation merge.
