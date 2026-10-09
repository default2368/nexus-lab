# SURF-082-003 — Stale Reference Convergence

Use this prompt in a new clean Arena session after the SURF-082-002 registry-shim PR is
merged to `master`.

---

## Prompt

```text
# SURF-082-003 — Stale Reference Convergence

ROLE:
Foundation Reference Hygiene Agent

MODE:
STRICT READ-ONLY PHASE 1

OBJECTIVE:
Identify and classify active references to page IDs, modules and type authorities that
have already been retired. Preserve governed compatibility and historical evidence.
Remove only references proven stale in active code, current tests or current operational
documentation.

This task does not retire additional pages.

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
git log --oneline --decorate --graph -15

Verify:

- branch derives from current origin/master;
- defaults retirement is merged;
- provenance hardening is merged;
- empty registry shims retirement is merged;
- working tree is clean;
- no merge/rebase active;
- package version remains 0.8.1;
- v0.8.1 tag remains unchanged.

Create/use:

cleanup/0.8.2-stale-references

If not:

STOP
status = BLOCKED_BASELINE

==================================================
PHASE 1 — RETIRED REFERENCE SET
==================================================

Start with these owner-ratified retired references:

physical/main/chat
  canonical replacement: simple/assistant

physical/main/home-pages
  canonical replacement: core-admin/discovery-pages

src/config/discovery/defaults
@/config/discovery/defaults
  module retired; no replacement module

@/types/discovery/core.new
src/types/discovery/core.new
  historical missing/retired type source; canonical current types live elsewhere

Do not assume this list is complete. Add only identifiers proven retired by the Legacy
Ledger or merged retirement commits.

==================================================
PHASE 2 — COMPLETE OCCURRENCE INVENTORY
==================================================

Search separately in:

- src;
- scripts;
- tests;
- package/export/config files;
- current operational docs;
- governance/legacy ledger;
- historical reports;
- backups/docs legacy/archive.

For every occurrence record:

identifier
path
line/context
consumer type
whether executable
current owner
replacement/meaning
disposition
reason

Classify as exactly one:

ACTIVE_RUNTIME_REFERENCE
ACTIVE_BUILD_REFERENCE
COMPATIBILITY_LEDGER
CURRENT_TEST
STALE_TEST_OR_COMMENT
CURRENT_DOCUMENTATION
HISTORICAL_EVIDENCE
BACKUP_OR_ARCHIVE
REVIEW_REQUIRED

Do not count historical reports/backups as active consumers.

==================================================
PHASE 3 — PRESERVATION RULES
==================================================

Preserve:

- Legacy Ledger identifiers and evidence;
- retirement reports;
- commit provenance;
- historical ADR/PRD/report statements;
- explicit route alias/redirect records with owner/expiry;
- backups/archive outside the active-authority count.

Do not rewrite history to make old documents appear current.

Current docs may link to historical evidence, but must not instruct users/agents to use
retired modules or routes.

==================================================
PHASE 4 — MUTATION CANDIDATE
==================================================

Mutation candidates may include only:

- active imports of retired modules;
- active navigation/routing references to retired page IDs;
- current test assertions/comments that describe retired behavior as current;
- current README/guides that instruct use of retired paths;
- current code comments used as authoring guidance that point to retired sources.

Explicitly excluded from this task:

- physical/debug/debug-auth;
- test/hello-api;
- test/redis-console;
- hub;
- simple/about-legacy;
- templates;
- Operations migration;
- AI Pages panel/VirtualPageTemplate;
- Legacy Ledger entries;
- historical reports.

Before mutation return:

- complete occurrence matrix;
- exact active stale set;
- exact preserve set;
- exact replacement text/ID when applicable;
- exact file allowlist;
- test plan;
- package/clean-room impact;
- rollback.

Stop with:

READY_FOR_OWNER_REFERENCE_MUTATION_APPROVAL

No source change in Phase 1.

==================================================
FUTURE MUTATION GATES
==================================================

For an owner-approved patch verify:

- active stale references after = 0;
- Legacy Ledger/historical evidence unchanged;
- navigation/broken refs unchanged or improved;
- targeted tests;
- public TypeScript;
- full failure-identity comparison;
- build;
- live package;
- clean room;
- v0.8.1 compatibility fixture;
- protected-kernel diff;
- lockfile unchanged;
- clean-tree GIT_VERIFIED provenance.

Create one local commit before package generation, because release provenance rejects a
dirty worktree.

==================================================
MANDATORY OUTPUT
==================================================

Return:

- repository/branch/HEAD;
- retired reference set and evidence;
- occurrence matrix;
- active stale references;
- preserved historical/ledger references;
- candidate patch allowlist;
- expected diff;
- tests and commands;
- risks/rollback;
- compatibility impact;
- owner decisions.

Final status:

READY_FOR_OWNER_REFERENCE_MUTATION_APPROVAL
BLOCKED_BASELINE
BLOCKED_ACTIVE_CONSUMER
BLOCKED_REPLACEMENT_AMBIGUITY
BLOCKED_HISTORICAL_AUTHORITY
NO_ACTIVE_STALE_REFERENCES

No source change.
No push.
No tag.
No version bump.
```
