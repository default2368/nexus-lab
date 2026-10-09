# PROV-082-001A — Release Eligibility Completeness

Use this prompt on the existing branch:

```text
fix/0.8.2-dirty-worktree-provenance
```

The branch may have an open Draft PR. Do not merge until this amendment is complete.

---

## Prompt

```text
# PROV-082-001A — Release Eligibility Completeness

ROLE:
Foundation Distribution Provenance Agent

MODE:
STRICT AMENDMENT — NO SCOPE EXPANSION

OWNER REVIEW:
PROV-082-001 implementation direction is approved.
Merge remains HOLD because missing provenance fields may bypass R19.

OBJECTIVE:
Make release eligibility fail closed when provenance fields are absent, and separate
shape/diagnostic validation from release validation without duplicating the eligibility
predicate.

==================================================
INVARIANT
==================================================

Release validation requires all of:

sourceCommit
sourceCommitOrigin
worktreeState
releaseEligible

Release ACCEPT requires exactly:

sourceCommitOrigin = GIT_VERIFIED
worktreeState = CLEAN
releaseEligible = true

Any missing or incompatible value:

→ REJECT
→ release validation error

A legacy or diagnostic manifest cannot become release-eligible by omitting fields.

==================================================
PHASE 0 — REALITY CHECK
==================================================

Before editing run:

pwd
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git remote -v
git log --oneline --decorate -12

Verify:

- branch is fix/0.8.2-dirty-worktree-provenance;
- PROV-082-001 commits are present;
- working tree is clean;
- no merge/rebase active;
- no page/template/Operations changes exist in the branch.

Inspect:

- validateManifest implementation;
- R19 implementation;
- producer self-check;
- CLI validator default mode;
- legacy producer tests;
- worktree provenance tests;
- schema requirements.

Return the exact current behavior before modification.

==================================================
VALIDATION MODES
==================================================

The system needs two explicit modes.

## SHAPE / DIAGNOSTIC

Purpose:

- producer self-check;
- legacy compatibility inspection;
- diagnostic artifact generation.

May accept legacy provenance shape if the base schema permits it.

It must never claim release eligibility merely because validation passed.

## RELEASE

Purpose:

- public validator command default;
- package release gate;
- F08 clean-room/release conformance.

Requires complete provenance and applies R19 fail-closed.

Preferred API:

validateManifest(manifest, { mode: 'shape' })
validateManifest(manifest, { mode: 'release' })

If retaining the current options object is materially safer for compatibility, the two
modes must still be explicit and impossible to confuse. Document the choice.

Default for the CLI/public validator:

release

Producer internal self-check:

shape

==================================================
R19 SINGLE SOURCE OF TRUTH
==================================================

Eligibility logic must exist in one function/path.

Do not duplicate this predicate in producer, CLI and validator.

Conceptual result:

releaseEligibilityFindings(manifest)
→ missing fields
→ invalid values
→ non-GIT origin
→ non-CLEAN worktree
→ releaseEligible != true

Release mode appends these findings and rejects.
Shape mode validates field types when present but does not claim release eligibility.

==================================================
OVERRIDE MATRIX
==================================================

Implement and test one explicit policy. Owner-approved default policy:

| Worktree state | Default | Explicit diagnostic override |
|---|---|---|
| CLEAN | GIT_VERIFIED, eligible | same |
| STAGED | REJECT | WORKTREE_UNVERIFIED, not eligible |
| UNSTAGED | REJECT | WORKTREE_UNVERIFIED, not eligible |
| UNTRACKED non-ignored | REJECT | WORKTREE_UNVERIFIED, not eligible |
| WORKTREE_CHANGED_DURING_BUILD | REJECT | REJECT always |
| GIT_ABSENT | REJECT | CALLER_UNVERIFIED, not eligible, only if existing explicit override permits |

Diagnostic artifacts always carry:

releaseEligible = false

and are rejected by release validation.

If the current implementation intentionally applies a stricter policy, report the exact
difference before changing it. Do not silently weaken a stricter rule.

==================================================
MANDATORY TESTS
==================================================

Add or amend tests for:

1. current-schema manifest missing releaseEligible → release REJECT;
2. missing worktreeState → release REJECT;
3. missing sourceCommitOrigin → release REJECT;
4. missing sourceCommit → release REJECT;
5. CALLER_UNVERIFIED with fields omitted → release REJECT;
6. WORKTREE_UNVERIFIED → release REJECT R19;
7. GIT_VERIFIED + CLEAN + true → release ACCEPT;
8. shape mode accepts supported legacy shape but does not produce a release PASS;
9. CLI validator default is release mode;
10. producer self-check uses shape mode;
11. STAGED default and override behavior;
12. UNSTAGED default and override behavior;
13. UNTRACKED default and override behavior;
14. GIT_ABSENT default and explicit diagnostic behavior;
15. WORKTREE_CHANGED_DURING_BUILD rejects even with override;
16. diagnostic artifact cannot pass materialize/release validation;
17. no artifact on default rejection;
18. existing clean package/reproducibility hashes remain deterministic.

Use synthetic Git repositories for worktree-state tests.

==================================================
ALLOWED SCOPE
==================================================

Allowed only:

- existing distribution manifest validator;
- producer provenance/self-check path;
- provenance schema when an additive requirement is necessary;
- PROV worktree/producer/validator tests;
- existing PROV-082-001 finding/review document.

Before editing, return the exact file allowlist.

Forbidden:

- pages/templates;
- Operations;
- Foundation protected kernel;
- unrelated manifest fields;
- version bump;
- package dependency change;
- lockfile change;
- tag;
- merge;
- force push;
- broad refactor.

==================================================
QUALITY GATES
==================================================

Run:

- provenance test suite;
- producer CLI suite;
- manifest negative suite;
- hash-model suite;
- live-pipeline clean-room suite;
- contracts suite;
- public TypeScript;
- build;
- clean package production;
- diagnostic dirty override probe;
- release validator rejection probe;
- full failure-identity comparison;
- protected-kernel diff;
- lockfile diff;
- git status.

Every command includes cwd, exit code and output/log path.

==================================================
PR / COMMIT
==================================================

Candidate amendment commit:

fix(distribution): require complete provenance for release validation

The existing PR may remain Draft until this commit and its evidence are reviewed.

Do not merge.
Do not tag.
Do not bump version.

==================================================
FINAL OUTPUT
==================================================

Return:

- branch/base/HEAD;
- exact file allowlist;
- validation mode contract;
- single R19 predicate location;
- override matrix implemented;
- tests and command results;
- clean manifest ACCEPT evidence;
- missing-field release REJECT evidence;
- dirty diagnostic artifact REJECT evidence;
- changed files;
- commit SHA;
- Draft PR URL;
- protected diff;
- lockfile status;
- open risks.

Final status:

READY_FOR_OWNER_MERGE_REVIEW
BLOCKED_BASELINE
BLOCKED_SCHEMA_DECISION
BLOCKED_RELEASE_GATE_COMPLETENESS
BLOCKED_OVERRIDE_POLICY
BLOCKED_REGRESSION

No merge before owner review.
```
