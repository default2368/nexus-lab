# SURF-082-004 — Legacy Reference Template Review and Migration

Use this prompt in a new clean Arena session after SURF-082-003 is merged to `master`.

---

## Prompt

```text
# SURF-082-004 — Hello API / Redis Console Legacy Reference Migration

ROLE:
Foundation Template and Diagnostic Surface Agent

MODE:
STRICT PHASED IMPLEMENTATION — PLAN FIRST

OWNER DECISIONS

The following classifications are ratified:

1. test/hello-api + HelloApiTemplate

   lifecycle: LEGACY
   role: REFERENCE / TEMPLATE_EXPERIMENT
   distribution: GATED / non-production by default
   disposition: REVIEW_AND_EXTRACT_THEN_RETIRE

2. test/redis-console + RedisConsoleTemplate

   lifecycle: LEGACY
   role: REFERENCE / DIAGNOSTIC / TEMPLATE_EXPERIMENT
   distribution: GATED / non-production by default
   current behavior: PARTIALLY BROKEN because POST /api/redis-console is absent
   disposition: EXTRACT_TARGETED_PATTERNS_THEN_RETIRE

3. The missing generic Redis command endpoint must NOT be implemented in this task.

4. Template Lab must not execute real Redis side effects during template preview.

5. Extraction is target-driven. Do not improve legacy templates for their own sake.

6. Do not refactor SystemDebugTemplate merely to make legacy implementations share
   components. Extract only what the approved Operations Control target will consume.

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
git log --oneline --decorate --graph -15

Verify:

- branch derives from current origin/master;
- SURF-082-003 is merged;
- working tree is clean;
- no merge/rebase active;
- package version remains 0.8.1;
- v0.8.1 tag unchanged;
- PROV release gate is active.

Create/use a dedicated branch:

cleanup/0.8.2-legacy-reference-templates

If not:

STOP
status = BLOCKED_BASELINE

==================================================
PHASE 1 — EXACT CURRENT BEHAVIOR
==================================================

Treat the existing repository document as the canonical planning/status source:

```text
docs/reports/0.8/0.8.2-SURFACE-CONVERGENCE-BACKLOG.md
```

Do not create another Surface Convergence backlog or duplicate its classifications.
Read it and report only evidence that confirms or contradicts it.

Inspect and trace:

- test/hello-api PageMeta/page declaration;
- test/redis-console PageMeta/page declaration;
- HelloApiTemplate;
- RedisConsoleTemplate;
- TemplateLabTemplate scenarios/catalog;
- autoComponentLoader mapping;
- template-manager mapping;
- JsonInspectorBlock;
- SystemDebug operation-log pattern;
- Redis clients/endpoints;
- package and manifest membership;
- navigation and route access;
- Template Lab preview execution behavior.

For every source claim provide command and file:line.

Explicitly verify:

- POST /api/redis-test exists;
- POST /api/redis-console does not exist, or report contrary evidence;
- whether Template Lab mounting RedisConsoleTemplate triggers checkConnection/fetch;
- whether command execution can occur in preview;
- whether HelloApi has any unique executable behavior;
- exact autoComponentLoader path mismatch and whether it is live.

==================================================
PHASE 2 — TARGET RESPONSIBILITY MATRIX
==================================================

Classify each observed pattern:

| Pattern | Current owners/consumers | Target owner | Decision |
|---|---|---|---|
| JsonInspectorBlock | current shared consumers | existing diagnostics authority | KEEP_SHARED |
| capped operation/history log | Redis/SystemDebug | Operations Control candidate | EXTRACT_IF_TARGET_CONSUMES |
| status indicator | Redis + potential health surfaces | Operations Control candidate | EXTRACT_IF_SECOND_CONSUMER |
| console input/execute | Redis only | none approved | KEEP_LOCAL / RETIRE |
| debug key-value card | Redis only | unknown | REVIEW_REQUIRED |
| HelloApi themed capability/code block | HelloApi only | approved host? | REVIEW_REQUIRED |

Use only:

KEEP_SHARED
MOVE_TO_DOMAIN
MOVE_TO_DEVTOOLS
MOVE_TO_LEGACY_COMPAT
KEEP_LOCAL_UNTIL_RETIRE
DELETE
REVIEW_REQUIRED

Do not create generic primitives solely because extraction is possible.

==================================================
PHASE 3 — SAFE TEMPLATE LAB PREVIEW PLAN
==================================================

Design the smallest boundary that ensures:

```text
Template Lab preview
→ no real Redis network call by default
→ no destructive command execution
→ deterministic synthetic state
```

Candidate mechanisms to evaluate:

- injected Redis/diagnostic I/O adapter;
- explicit previewMode;
- scenario-provided mock status/history;
- disabled execute controls in preview.

Do not implement before returning:

- exact props/contract already available;
- exact files;
- whether PageData/Template props change is required;
- whether a protected contract would be touched;
- test plan;
- target behavior for direct legacy route vs Template Lab preview.

If a protected contract change would be required:

STOP
status = BLOCKED_PROTECTED_CONTRACT

==================================================
PHASE 4 — DISPOSITION PLAN
==================================================

Return a staged plan, not one large refactor.

Candidate sequence:

A. Evidence reconciliation
   - verify the existing LEGACY_REFERENCE_REVIEW classifications;
   - propose amendments to the canonical Surface Convergence document only if the
     code evidence contradicts or materially extends it;
   - do not create a second backlog/report.

B. Template Lab preview isolation
   - no network/destructive effects;
   - synthetic deterministic scenarios.

C. Target-driven extraction
   - only components required by approved Operations Control or a second consumer.

D. Page/template retirement
   - only after extracted behavior is used and parity proven;
   - remove page, template, gate, switch/import, manager entry, assets and aliases atomically.

For each step return:

- exact file allowlist;
- tests;
- package impact;
- v0.8.1 compatibility impact;
- rollback;
- owner decision.

==================================================
SECURITY RULES
==================================================

Forbidden:

- implementing POST /api/redis-console;
- exposing FLUSHDB/KEYS* as a production Operations capability;
- adding arbitrary Redis command execution;
- real Redis calls during Template Lab preview;
- embedding credentials/endpoints;
- weakening auth or middleware;
- silent error/fallback;
- moving everything to src/react/legacy;
- extracting one-consumer components without a target contract.

==================================================
NON-GOALS
==================================================

- Operations V1 implementation;
- SystemDebug redesign;
- Component Catalog migration;
- VirtualPageTemplate retirement;
- Brain/API changes;
- version bump/tag;
- broad UI redesign;
- package architecture changes unrelated to these surfaces.

==================================================
PHASE 5 — FIRST RESPONSE
==================================================

No source changes.

Return:

- repository/branch/HEAD;
- exact behavior/consumer graph;
- endpoint/security findings;
- Template Lab side-effect result;
- pattern responsibility matrix;
- safe preview options and recommendation;
- staged implementation sequence;
- first mutation exact allowlist;
- tests/rollback;
- open owner decisions.

Final status:

READY_FOR_OWNER_PREVIEW_ISOLATION_APPROVAL
READY_FOR_OWNER_DOC_CLASSIFICATION_APPROVAL
BLOCKED_BASELINE
BLOCKED_PROTECTED_CONTRACT
BLOCKED_ACTIVE_CONSUMER
BLOCKED_TARGET_RESPONSIBILITY
BLOCKED_SECURITY_BOUNDARY

No code change.
No push.
No tag.
No version bump.
```
