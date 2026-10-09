# DOC-TOOL-002B — Local Documentation Spool Delivery

Usa questo prompt in una sessione Arena collegata al repository privato
`default2368/nexus-lab-documentation`.

---

## Prompt

```text
# DOC-TOOL-002B — Local Documentation Spool Delivery

ROLE:
Documentation Tooling Developer

MODE:
STRICT SCOPED IMPLEMENTATION

OWNER DECISION:
APPROVED DIRECTION

OBJECTIVE:
Extend the candidate `tools/documentation/report-adr-backlog.sh` so that a user
running it locally from a technical repository can deliver a metadata-only YAML
report into an ignored temporary spool inside a local checkout of
`nexus-lab-documentation`.

The spool is transport only.
It is not canonical documentation.
It is not Git staging.
It is not publication.

==================================================
ARCHITECTURE
==================================================

Expected local flow:

technical repository
↓
report-adr-backlog.sh
↓
metadata-only YAML
↓
<documentation-root>/tmp/inbox/reports/
↓
user attaches the YAML to an Arena documentation session
↓
review / owner decision
↓
tracked documentation update

Arena sessions do not share the user's local filesystem. This task does not try to
make the local spool visible automatically to Arena or GitHub.

==================================================
ALLOWED FILES
==================================================

Changes are allowed only in:

.gitignore
tools/documentation/report-adr-backlog.sh
tools/documentation/tests/test-report-adr-backlog.sh
tools/documentation/REVIEW-DOC-TOOL-002.md

Optionally, if it already exists:

docs/governance/REPORT-ADR-BACKLOG-USAGE.md

Do not create or modify any other file.

Do not modify:

README.md
AGENTS.md
PROGRAM-STATE.md
sources/REPOSITORY-REGISTRY.yaml
sources/DOCUMENT-INVENTORY.yaml
canonical docs
inbox tracked content
archive tracked content

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
git log --oneline --decorate -10

Read:

AGENTS.md
docs/governance/INTAKE-AND-QUARANTINE.md
docs/governance/PUBLISHING-WORKFLOW.md
tools/documentation/REVIEW-DOC-TOOL-002.md
tools/documentation/report-adr-backlog.sh
tools/documentation/tests/test-report-adr-backlog.sh
sources/REPOSITORY-REGISTRY.yaml

Report the current implementation before changing it:

- supported options;
- default behavior;
- whether `--target` or `--apply` exists;
- whether report body includes document content or Git diff;
- current tests;
- current safety gaps.

If the working tree is not clean or expected files are absent:

STOP
status = BLOCKED_REALITY_CHECK

==================================================
PHASE 1 — CLI CONTRACT
==================================================

Default behavior remains read-only stdout/dry-run.

Introduce an explicit local delivery option. Preferred interface:

--deliver-local <documentation-root>

Example:

/path/nexus-lab-documentation/tools/documentation/report-adr-backlog.sh \
  --project foundation \
  --deliver-local /path/nexus-lab-documentation

The script is expected to be executed with the technical repository as its current
working directory.

Do not call the option `--apply`: delivery to a temporary spool is not canonical
application.

If legacy options exist:

--target
--apply

remove them or make them fail closed with a clear deprecation message. Do not retain a
mode that writes directly to tracked documentation paths.

==================================================
PHASE 2 — DOCUMENTATION ROOT VALIDATION
==================================================

Before local delivery, resolve the documentation root with a canonical real path.

Require all of:

- directory exists;
- directory is a Git working tree;
- remote identity matches `default2368/nexus-lab-documentation`;
- repository contains `AGENTS.md`;
- repository contains `docs/governance/INTAKE-AND-QUARANTINE.md`;
- repository contains `sources/REPOSITORY-REGISTRY.yaml`;
- target spool resolves inside the documentation root;
- target spool is not a symlink escape;
- `tmp/` is ignored by Git;
- no spool file is tracked by Git.

Validate Git ignore through:

git -C <documentation-root> check-ignore -q tmp/

If `tmp/` is not ignored:

STOP
status = BLOCKED_TMP_NOT_IGNORED

Target path is fixed by the tool:

<documentation-root>/tmp/inbox/reports/

The caller cannot choose another subdirectory.

==================================================
PHASE 3 — PROJECT IDENTITY
==================================================

Require:

--project <project-id>

The project ID must exist in:

<documentation-root>/sources/REPOSITORY-REGISTRY.yaml

Verify the current technical repository remote against the registered identity.

Do not infer an authoritative project ID from the local directory name.

Unknown or mismatched project:

STOP
status = BLOCKED_UNKNOWN_PROJECT

The script may report a suggested ID, but cannot use it for delivery.

==================================================
PHASE 4 — REPORT CONTENT
==================================================

The YAML report contains metadata only.

Required fields:

schemaVersion
reportId
reportType
lifecycle = INBOX
generatedAt

source.projectId
source.repository
source.branch
source.head or PENDING
source.baseCommit when observable

For each changed ADR/backlog document:

document.kind
document.localId when observed
document.path
document.title when safely extracted
document.declaredStatus when safely extracted
document.sha256
change.gitStatus
change.additions
change.deletions
change.contentIncluded = false

The report must not contain:

- document body;
- Git diff body;
- secret value;
- complete personal data;
- binary data;
- automatic cross-repository ID assignment;
- canonical promotion decision.

If a secret-like candidate is detected, record only:

finding type
file
line/location
redacted description

and block delivery unless the finding is proven to be a false positive by an explicit
test fixture.

==================================================
PHASE 5 — SAFE FILE CREATION
==================================================

Create the spool directory only after every validation gate passes.

Use:

- `mktemp` for intermediate output;
- `trap` for cleanup;
- atomic rename into the final spool path;
- restrictive file permissions where supported;
- no overwrite of an existing report;
- deterministic report ID from project/change metadata plus a short content hash;
- sanitized filename components.

Candidate filename:

<UTC timestamp>--<project-id>--adr-backlog--<short-report-hash>.yaml

If an identical report already exists, return its path without creating another copy,
or fail with a deterministic duplicate status. Document the chosen behavior.

Never call:

git add
git commit
git push
gh
curl
network commands

Do not modify the technical source repository.
Do not modify tracked files in the documentation repository during script execution.

==================================================
PHASE 6 — .gitignore
==================================================

Ensure the repository `.gitignore` contains:

/tmp/

or the repository's approved equivalent that ignores the complete local spool.

Do not use an overly broad pattern that hides tracked source or documentation files.

Verify after implementation:

git check-ignore -v tmp/inbox/reports/example.yaml

==================================================
PHASE 7 — TESTS
==================================================

Extend synthetic tests to cover at least:

1. default dry-run writes nothing;
2. valid local delivery creates one YAML under `tmp/inbox/reports/`;
3. documentation root with wrong remote is rejected;
4. documentation root without required markers is rejected;
5. `tmp/` not ignored is rejected;
6. symlink/path escape is rejected;
7. unknown project is rejected;
8. source remote mismatch is rejected;
9. report contains no document body;
10. report contains no Git diff body;
11. file path with spaces is handled;
12. renamed ADR is handled;
13. deleted ADR is represented without reading missing content;
14. no staged documentation produces an explicit no-op result;
15. duplicate delivery behavior is deterministic;
16. source technical repository remains byte-for-byte/Git-status unchanged;
17. documentation tracked working tree remains unchanged;
18. generated spool file is ignored and untracked;
19. secret-like fixture is redacted and blocked;
20. shell arguments cannot inject commands.

Use only synthetic temporary Git repositories in the test suite.
Do not access real Foundation, Backend or CLI repositories during tests.

==================================================
PHASE 8 — QUALITY GATES
==================================================

Run:

bash -n tools/documentation/report-adr-backlog.sh
bash -n tools/documentation/tests/test-report-adr-backlog.sh

If shellcheck is already available:

shellcheck tools/documentation/report-adr-backlog.sh \
  tools/documentation/tests/test-report-adr-backlog.sh

Do not install shellcheck as part of this task.

Run the synthetic test suite.

Then run:

git status --short
git diff --check
git diff --stat
git diff

Verify every changed file belongs to ALLOWED FILES.

==================================================
PHASE 9 — REVIEW RECORD
==================================================

Update `tools/documentation/REVIEW-DOC-TOOL-002.md` with:

- previous state;
- implemented local spool contract;
- commands and exit codes;
- test matrix;
- unresolved risks;
- recommendation: APPROVE / APPROVE_WITH_CONDITIONS / REJECT;
- explicit statement that spool delivery is not canonical publication.

Do not mark the tool approved merely because tests pass. Owner approval remains
separate.

==================================================
MANDATORY OUTPUT
==================================================

Return:

Repository / branch / HEAD
Previous tool behavior
New CLI contract
Changed files
Syntax results
ShellCheck result or NOT_AVAILABLE
Synthetic test results
Source-repository mutation check
Documentation tracked-tree mutation check
Example generated YAML with sensitive values absent
Security findings
Open risks
Owner decision required
Suggested commit message

Suggested commit message:

feat(documentation): add safe local status-report spool

Final status must be exactly one of:

READY_FOR_OWNER_REVIEW
BLOCKED_REALITY_CHECK
BLOCKED_TMP_NOT_IGNORED
BLOCKED_UNKNOWN_PROJECT
BLOCKED_SECURITY_FINDING
BLOCKED_TEST_FAILURE
BLOCKED_ALLOWLIST_VIOLATION

==================================================
FINAL INVARIANT
==================================================

The technical repository produces a metadata report.
The local documentation spool transports it.
The spool never becomes canonical by itself.
Arena receives the report only through explicit user transfer.
The documentation publisher and human owner control promotion.
```
