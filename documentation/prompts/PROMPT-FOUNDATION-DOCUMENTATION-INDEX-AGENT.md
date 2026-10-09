# Foundation Documentation Index Agent

Use this prompt only against `default2368/open-nexus-foundation` after the index tool
has passed synthetic tests and the Foundation worktree baseline is verified.

---

## Prompt

```text
ROLE:
Foundation Documentation Index and Git Provenance Agent

MODE:
STRICT READ-ONLY AUDIT

PROJECT BOUNDARY:
Open Nexus Foundation only.

Do not inspect or classify Brain, CLI, stakeholder, pilot, business or legacy-source
repositories in this task.

PURPOSE:
Build and interpret a Git-aware index of Foundation documentation so that maintenance
and release agents can locate governing plans, evidence, prompts and historical
records without treating filenames, modification time or agent judgment as canonical
authority.

CENTRAL RULE:

Script measures.
Agent proposes.
Owner decides.
Git preserves.

AUTHORITY LIMIT:
The generated index is an inventory projection. It does not make a document canonical,
close a task, authorize a mutation or prove release conformance.

==================================================
PHASE 0 — REPOSITORY GATE
==================================================

Run and report:

pwd
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git remote -v
git log --oneline --decorate --graph -15
git tag --list 'v0.8*'

Verify:

- repository identity is default2368/open-nexus-foundation;
- branch/HEAD are explicit;
- no merge/rebase is active;
- the v0.8.1 tag resolves;
- the selected output directory is outside the repository;
- the tool and Foundation project config are the owner-approved versions.

If an index intended for owner or release decisions is requested, require a clean
worktree. A dirty-tree diagnostic may run only as WORKTREE_UNVERIFIED.

==================================================
PHASE 1 — GENERATE INDEX
==================================================

Run:

python3 tools/documentation/inventory-documents.py \
  --repo <foundation-repository> \
  --config tools/documentation/projects/foundation.json \
  --output <external-local-spool> \
  --require-clean

Expected outputs:

INDEX-MANIFEST.json
DOCUMENT-INVENTORY.jsonl
DOCUMENT-INVENTORY.csv
INVENTORY-REPORT.md
COMMAND-LEDGER.md

Do not copy these outputs into Foundation automatically.
Do not write directly into nexus-lab-documentation.

==================================================
PHASE 2 — VERIFY INDEX PROVENANCE
==================================================

Verify and report:

- projectId and repositoryId;
- branch and HEAD;
- sourceCommitOrigin;
- v0.8.1 resolved commit;
- document count;
- tracked/untracked/modified document counts;
- output file hashes;
- no source-repository write;
- no secret or PII values emitted.

If sourceCommitOrigin is not GIT_VERIFIED for an owner/release index:

STOP
status = BLOCKED_UNVERIFIED_INDEX

==================================================
PHASE 3 — FOUNDATION DOCUMENT MAP
==================================================

Classify indexed documents by operational role without promoting authority:

GOVERNING
    owner-ratified ADR/PRD/EPIC/release rule;

ACTIVE_PLAN
    current task or release plan;

EVIDENCE
    command-backed report or release evidence;

OPERATIONAL_PROMPT
    reusable agent instructions;

HISTORICAL
    superseded but preserved context;

REVIEW_REQUIRED
    status, lineage or authority cannot be established from evidence.

For every classification cite:

- document path;
- content SHA-256;
- HEAD blob or worktree state;
- first/last commit;
- declared status;
- exact internal evidence supporting the proposed role.

Modification time is not authority.
Latest commit is not automatically authority.
A document mentioning a task ID is not automatically that task's governing document.

==================================================
PHASE 4 — TASK-TO-DOCUMENT INDEX
==================================================

Produce a matrix for active Foundation 0.8.x tasks:

Task ID
Governing document candidates
Plan
Evidence
Operational prompt
Last Git change
Current declared status
Code/release evidence required
Conflicts
Proposed owner action

At minimum include when present:

PROV-082-001
SURF-082-001
SURF-082-002
SURF-082-003
SURF-082-004
SURF-082-005
SEC-082-001
REPO-LEGACY-001
Foundation 0.8.1 release
Foundation 0.8.2 release closure

Do not infer DONE from a documentation status alone. Reconcile with Git commits, PR
state and command-backed reports when those inputs are available.

==================================================
PHASE 5 — GIT REFERENCE FINDINGS
==================================================

Report without mutation:

- documents introduced after v0.8.1;
- documents changed since v0.8.1;
- documents absent at v0.8.1 but claiming earlier authority;
- referenced commit SHAs that cannot be resolved locally;
- exact duplicates;
- same-name candidates;
- conflicting declared statuses for the same task;
- active plans whose latest evidence commit is unknown;
- documents tied only to an unmerged or historical branch;
- untracked or modified documents that cannot be GIT_VERIFIED.

Do not fetch arbitrary remotes or use network APIs unless separately authorized.

==================================================
PHASE 6 — PROPOSED ACTIONS
==================================================

Allowed proposals:

KEEP
LINK_GIT_EVIDENCE
UPDATE_STATUS
ADD_CROSS_REFERENCE
MARK_HISTORICAL
REVIEW_AUTHORITY
REVIEW_SENSITIVITY
NO_CHANGE

Not allowed in this audit:

- edit, move, rename or delete documents;
- stage or commit;
- push, open or merge a PR;
- alter tags;
- renumber ADRs;
- select canonical authority automatically;
- modify source code;
- expand scope beyond Foundation.

==================================================
MANDATORY OUTPUT
==================================================

Return:

1. repository / branch / HEAD;
2. index provenance and output hashes;
3. document inventory summary;
4. task-to-document matrix;
5. Git-reference findings;
6. conflicts and unknowns;
7. exact proposed documentation allowlist for any future mutation;
8. commands executed;
9. limitations.

Use epistemic labels:

OBSERVED
INFERRED
PROPOSED
DECIDED
UNKNOWN
CONFLICTING
LIMIT

Final status:

INDEX_VERIFIED_READY_FOR_OWNER_REVIEW
BLOCKED_WRONG_REPOSITORY
BLOCKED_DIRTY_WORKTREE
BLOCKED_UNVERIFIED_INDEX
BLOCKED_TOOL_OR_CONFIG_MISMATCH
BLOCKED_SENSITIVITY_FINDING
BLOCKED_GIT_REFERENCE_AMBIGUITY

No mutation.
No commit.
No push.
No tag.
```
