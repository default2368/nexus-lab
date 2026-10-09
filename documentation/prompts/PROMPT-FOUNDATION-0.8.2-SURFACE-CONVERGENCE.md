# Foundation 0.8.2 — Surface Convergence and Compatibility Monitoring

Use this prompt after Foundation 0.8.1 is merged, tagged and verified.

---

## Prompt

```text
# Foundation 0.8.2 — Retired/Deprecated Surface Convergence

ROLE:
Foundation Surface Convergence Agent

MODE:
STRICT MIGRATION + COMPATIBILITY MONITORING

PRECONDITION:
Foundation 0.8.1 Distribution Green Line is merged and tagged as v0.8.1.

OBJECTIVE:
Remove, migrate or isolate retired/deprecated pages, templates, aliases, shims and
tracked legacy surfaces from the active Foundation source tree without breaking the
0.8.1 distribution contract or projects generated from the 0.8.1 line.

This task is not part of the 0.8.1 release.
Target release: 0.8.2, subject to compatibility classification.

==================================================
PHASE 0 — REPOSITORY / RELEASE GATE
==================================================

Verify:

- current branch and HEAD;
- clean working tree;
- v0.8.1 annotated tag exists locally and remotely;
- v0.8.1 points to the approved release commit;
- no merge/rebase active;
- Foundation 0.8.1 package and manifest evidence available.

If not:

STOP
status = BLOCKED_0_8_1_BASELINE

==================================================
PHASE 1 — FREEZE COMPARISON FIXTURES
==================================================

Record, without copying source snapshots into the repository:

- v0.8.1 release commit;
- Distribution Manifest;
- package filesystem inventory;
- package/reproducibility hashes;
- page/application surface inventory;
- template/alias inventory;
- one minimal generated-consumer fixture;
- one Operations/reference fixture.

Fixtures must be synthetic and contain no secret/personal data.

==================================================
PHASE 2 — FINAL DISPOSITION MATRIX
==================================================

For every candidate page/template/alias/shim record:

- current source path;
- current owner;
- active static consumers;
- dynamic/provider/generated consumers;
- navigation/route references;
- package membership;
- target owner;
- replacement;
- compatibility requirement;
- disposition.

Allowed dispositions:

KEEP
MIGRATE
DEV_ONLY
RETIRE
REMOVE_REFERENCE
REMOVE_ALIAS
LEGACY_ADAPTER
REBUILD_ON_APPROVED_MODEL
REVIEW_REQUIRED

No generic ACTIVE state is allowed for a retirement candidate.

Ratified Operations target:

- Operations index;
- discovery/pages;
- Template Discovery/Substitutability experience;
- API/System Control.

Operations V1 preserves behavior, not legacy page/template identity.

==================================================
PHASE 3 — 0.8.1 → 0.8.2 COMPATIBILITY MATRIX
==================================================

For every change record:

0.8.1 identifier/route/template/capability
0.8.2 target
compatibility behavior
alias/redirect expiry
migration finding
unsupported behavior
owner decision

Classify:

BACKWARD_COMPATIBLE
COMPATIBLE_WITH_ADAPTER
SUPPORTED_MIGRATION_REQUIRED
BREAKING
UNKNOWN

A change classified BREAKING cannot be hidden in 0.8.2 without an explicit versioning
decision.

==================================================
PHASE 4 — GENERATION SAFETY
==================================================

The CLI/Authoring path must consume Foundation Release artifacts and Distribution
Contracts, not source-tree copies.

Verify:

- a new 0.8.2 project contains no retired page/template;
- 0.8.1 source noise is not copied into generated projects;
- 0.8.1 pinned projects continue to validate against v0.8.1;
- upgrading a 0.8.1 project to 0.8.2 produces deterministic findings;
- aliases/routes migrate or fail with actionable diagnostics;
- supported Foundation release ranges are explicit.

==================================================
PHASE 5 — MUTATION PLAN
==================================================

No mega-delete.

Group commits/PRs by one surface class:

1. duplicate/re-export registry shims;
2. broken/out-of-bundle references;
3. test/recovery DEV_ONLY isolation;
4. Operations responsibility migration;
5. page/template pair convergence;
6. orphan template/gate/switch/manager cleanup;
7. tracked backup/version snapshots.

For each group return:

- exact file allowlist;
- behavior preserved;
- tests;
- rollback;
- compatibility impact.

Stop before source changes and request owner approval.

==================================================
PHASE 6 — PER-PR GATES
==================================================

Every approved PR must prove:

- targeted tests;
- TypeScript error-set comparison;
- full-suite failure-identity comparison;
- production build;
- package and manifest diff;
- clean-room execution when runtime relevant;
- Page/Template consumer recount;
- broken-reference report;
- 0.8.1 compatibility fixture result;
- protected-kernel diff;
- command ledger.

Retiring a template requires atomic treatment of:

- page consumer;
- gate entry;
- route switch;
- static import;
- manager mapping;
- alias;
- assets.

==================================================
COMPLETION TARGETS
==================================================

- active retired pages = 0;
- active deprecated templates without approved consumer = 0;
- manual duplicate registrations = 0;
- orphan template imports = 0;
- stale aliases without owner/expiry = 0;
- test/recovery pages in consumer package = 0;
- new 0.8.2 generated projects containing retired surface = 0;
- 0.8.1 upgrade findings nondeterministic = 0;
- tracked legacy codebase snapshots = 0;
- protected-kernel unauthorized diff = 0.

==================================================
MANDATORY OUTPUT
==================================================

Return first, read-only:

- repository/branch/HEAD;
- v0.8.1 baseline verification;
- final disposition matrix;
- compatibility matrix;
- generated-codebase impact;
- proposed PR sequence;
- exact first-PR allowlist;
- tests and rollback;
- versioning risks.

Final status:

READY_FOR_OWNER_SURFACE_MUTATION_APPROVAL
BLOCKED_0_8_1_BASELINE
BLOCKED_CONSUMER_AMBIGUITY
BLOCKED_MIGRATION_TARGET
BLOCKED_BREAKING_CHANGE
BLOCKED_GENERATION_COMPATIBILITY

No source change in the first response.
No push.
No tag.
No version bump.
```
