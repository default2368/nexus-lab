# F08-019A — Live Distribution Implementation Closure

Use this prompt in the Arena session attached to the Open Nexus Foundation repository.

---

## Prompt

```text
# F08-019A — Live Distribution Implementation Closure

ROLE:
Foundation Distribution Implementation Agent

MODE:
STRICT BOUNDED IMPLEMENTATION

OWNER DECISION:
F08-CODE-REALITY-CHECK verdict PARTIAL_IMPLEMENTATION is accepted.
F08-019A is active.
F08-019B and release tagging remain blocked.

OBJECTIVE:
Close only the three observed live-integration gaps:

1. no live producer CLI;
2. no declared operator command contract;
3. F08-017 frontend read model not mounted.

Target chain:

live ApplicationBundle / approved build model
→ manifest.json + discovery.json
→ validate
→ materialize package
→ clean-room execution
→ package-backed Admin read model
→ Operations frontend route

==================================================
PHASE 0 — REPOSITORY AND EVIDENCE GATE
==================================================

Before modifying anything run:

pwd
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git remote -v
git log --oneline --decorate --graph -20

Read:

AGENTS.md
Foundation 0.8 backlog F08-019A
F08-CODE-REALITY-CHECK report
F08-013 evidence/report
F08-014 evidence/report
F08-015 evidence/report
F08-017 evidence/report
existing distribution scripts and tests
package.json
Operations page/application declarations

Verify:

- working tree is clean, except explicitly identified pre-existing files;
- no merge/rebase is active;
- current branch derives from the intended 0.8 target;
- existing contract suites are green at the recorded baseline;
- no package-lock modification exists for this task.

If not:

STOP
status = BLOCKED_REPOSITORY_STATE

==================================================
PHASE 1 — EXACT IMPLEMENTATION PLAN
==================================================

Before coding, return:

1. exact live producer input boundary;
2. exact CLI command contract;
3. exact package.json scripts proposed;
4. exact Operations target route/page for F08-017;
5. exact file allowlist;
6. tests to add/change;
7. expected generated package tree;
8. protected-kernel diff expectation;
9. scratch-file disposition for `_cp1_scratch.mjs`;
10. risks and rollback.

Do not use test-created manifest/discovery as the live producer input.
Do not propose repository scanning as authority.

Stop with:

READY_FOR_OWNER_IMPLEMENTATION_APPROVAL

No source change in this first response.

==================================================
IMPLEMENTATION AUTHORIZATION BOUNDARY
==================================================

After explicit owner approval of the file allowlist, implement through separate,
reviewable commits.

Candidate commit sequence:

1. feat(distribution): add live application manifest producer
2. chore(distribution): expose package and clean-room commands
3. test(distribution): cover live bundle to clean-room pipeline
4. feat(operations): mount distribution admin read model

Do not combine unrelated cleanup.

==================================================
GATE 1 — LIVE PRODUCER CLI
==================================================

Required behavior:

- runs outside Vitest;
- consumes a real ApplicationBundle or approved live build artifact;
- uses existing distribution-producer core;
- accepts explicit application ID;
- accepts explicit output directory;
- writes manifest.json and discovery.json;
- deterministic for pinned inputs;
- fails on unknown application;
- fails on missing page/template/asset/capability/rendering metadata;
- does not modify source files;
- does not depend on absolute Foundation workspace paths in output;
- does not modify protected kernel contracts.

The producer is build/distribution tooling. It is not Runtime behavior.

==================================================
GATE 2 — OPERATOR COMMAND CONTRACT
==================================================

Expose stable commands in package.json, exact naming subject to owner-approved plan.
Candidate responsibilities:

- distribution:produce
- distribution:validate
- distribution:materialize
- distribution:cleanroom
- distribution:admin
- distribution:build

Requirements:

- no new dependency;
- no lockfile diff;
- no internal script-path knowledge required by the operator;
- explicit application/output arguments;
- documented exit codes;
- composed build runs produce → validate → materialize → integrity;
- commands fail closed.

==================================================
GATE 3 — LIVE END-TO-END TEST
==================================================

Golden path:

real `simple` ApplicationBundle
→ live producer CLI
→ manifest/discovery files on disk
→ validator
→ materializer
→ package filesystem
→ Foundation repository unavailable
→ clean-room runner
→ landing and second page

The E2E test must not construct its manifest/discovery input in test scope.

Verify:

- package tree;
- manifest/discovery hashes;
- integrity metadata;
- no absolute source paths;
- no undeclared assets/templates;
- actual rendered template identity;
- PUBLIC/PROTECTED behavior;
- not-found behavior;
- runtime repository observations = 0;
- silent template fallback occurrences = 0.

Conditional scenarios when present:

- Template Lab with manifest-declared package-scoped catalog;
- PHYSICAL rendering with route artifact and no template lookup;
- AI/generated pages with canonical Wow template key and explicit aliases.

==================================================
GATE 4 — OPERATIONS FRONTEND WIRING
==================================================

Mount the existing F08-017 frontend read model in an approved Operations-owned page.

Requirements:

- no new application;
- use current Operations/core-admin application ownership;
- preserve future Operations V1 migration direction;
- frontend consumes package/read-model artifact;
- no repository scan;
- no production fixture hardcode;
- real route/page import;
- component/route test or E2E;
- DOM/screenshot evidence;
- keyboard/basic failure state preserved where already required.

Do not redesign the UI in this task.

==================================================
SCRATCH HYGIENE
==================================================

Inspect `_cp1_scratch.mjs` before action.

If verified temporary and untracked:

- remove it;
- do not commit it.

Add an ignore rule only for a recurring, precisely defined temporary-file class.
Do not add broad `_*.mjs` or equivalent patterns.

==================================================
PROHIBITED
==================================================

- new capability;
- new architecture audit;
- new dependency;
- lockfile change;
- version bump;
- release tag;
- 0.9 integration;
- protected kernel modification;
- hardcoded absolute path;
- fixture manifest as live E2E input;
- direct push to default branch;
- force push;
- unrelated refactor;
- changing test expectations merely to obtain green.

==================================================
QUALITY GATES
==================================================

Run and record:

- targeted producer/validator/materializer/clean-room tests;
- Admin read-model tests;
- frontend route/component tests;
- live E2E;
- contract suite;
- public TypeScript;
- legacy TypeScript error-set comparison;
- full-suite failure identity comparison;
- protected-kernel diff;
- package filesystem inventory;
- git diff and status.

Every result includes command, cwd, exit code and artifact path.

==================================================
MANDATORY FINAL OUTPUT
==================================================

Return:

- branch / HEAD / base;
- commits;
- changed files;
- command contract;
- live producer evidence;
- generated package tree;
- manifest/discovery hashes;
- clean-room route matrix;
- actual rendered-template evidence;
- Admin read-model output;
- Operations route/frontend evidence;
- tests and TypeScript results;
- protected diff;
- lockfile status;
- scratch-file disposition;
- git status;
- open risks.

Final status:

READY_FOR_F08_019B
BLOCKED_REPOSITORY_STATE
BLOCKED_LIVE_PRODUCER
BLOCKED_COMMAND_CONTRACT
BLOCKED_PACKAGE
BLOCKED_CLEAN_ROOM
BLOCKED_FRONTEND_WIRING
BLOCKED_REGRESSION

Do not tag or release.
Stop before push unless separately authorized.
```
