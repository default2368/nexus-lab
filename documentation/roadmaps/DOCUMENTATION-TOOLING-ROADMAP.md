# Documentation Tooling Roadmap

**Status:** APPROVED DIRECTION  
**Scope:** `nexus-lab-documentation` and documentation export from technical repositories  
**Purpose:** make inventory, reporting and publication reproducible without allowing scripts or agents to decide canonical authority.

---

## Decision

Open Nexus introduces a small documentation toolchain.

```text
Script measures.
Agent classifies and proposes.
Human owner decides.
Git preserves approved history.
```

Scripts do not:

- assign cross-repository ADR IDs;
- choose canonical documents from modification time alone;
- promote documents;
- commit, push or merge;
- modify source repositories;
- copy secret, personal or unclassified material;
- replace repository-specific documentation authority.

---

## Toolchain V1

```text
tools/documentation/
├── inventory-documents.py
├── report-adr-backlog.sh
└── verify-publication-packet.py
```

Only three tools enter V1.

Automatic consolidation, document rewriting and cross-repository apply are deferred.

---

# DOC-TOOL-001 — `inventory-documents.py`

```text
Priority    P0
Status      CANDIDATE — SYNTHETIC TESTS PASS, FOUNDATION PILOT PENDING
Mode        read-only
Purpose     initial and periodic corpus inventory
```

## Responsibilities

- identify repository, branch and HEAD;
- enumerate text documents under approved roots;
- calculate SHA-256;
- extract document ID, title, type and declared status when available;
- record Git first/last commit metadata;
- classify exact duplicates by hash;
- identify same-name and same-ID candidates without resolving them;
- identify possible secret/PII findings without printing values;
- produce machine-readable inventory and a human report.

## Outputs

```text
DOCUMENT-INVENTORY.jsonl
DOCUMENT-INVENTORY.csv
INVENTORY-REPORT.md
COMMAND-LEDGER.md
```

## Required safety

```text
read-only by default
no apply mode in V1
no source writes
no network
no archive extraction to disk
no secret values in output
exclude .git/node_modules/build/cache/tmp
REVIEW_REQUIRED for ambiguous lineage
```

## Current pilot boundary — owner sequencing correction 2026-10-05

```text
Foundation only
```

The Foundation pilot is authorized before broader CLI integration because the current
need is to bind the active 0.8.x documentation corpus to Git evidence and specialize a
Foundation documentation agent.

Future convergence of documentation/Git workflow into CLI capabilities remains a
candidate direction, not current scope. Brain, stakeholder, business, Nexus Lab and
legacy-source inventories remain unauthorized in this tranche.

---

# DOC-TOOL-002 — `report-adr-backlog.sh`

```text
Priority    P0
Status      CANDIDATE — CODE REVIEW REQUIRED
Mode        dry-run / export
Purpose     ongoing status reporting from technical repositories
```

## Responsibilities

- inspect staged or explicitly selected ADR/backlog changes;
- produce provenance metadata;
- calculate current content hash;
- record project, branch, base commit and HEAD/PENDING;
- extract title and declared status;
- record additions/deletions without copying the diff body;
- produce an INBOX report.

## V1 correction

The script must export to a caller-provided output directory:

```bash
./tools/report-adr-backlog.sh \
  --project cli \
  --output /tmp/documentation-report
```

It must not write directly into another Git repository.

## Project identity

`projectId` must be:

- explicitly supplied; or
- resolved from an approved repository registry.

Unknown project:

```text
BLOCKED_UNKNOWN_PROJECT
```

No inferred cross-repository ADR ID is authoritative.

## First gate

Before real use:

```text
bash -n
shellcheck
source review
synthetic fixture tests
secret-output test
path-with-spaces test
rename/delete test
no-staged-files test
```

## First real pilot

A harmless staged documentation fixture in the CLI repository, dry-run first.

---

# DOC-TOOL-003 — `verify-publication-packet.py`

```text
Priority    P1
Status      PLANNED
Mode        read-only verification
Purpose     validate an approved packet before publisher execution
```

## Responsibilities

- validate packet schema;
- require owner approval and timestamp;
- validate repository and target allowlist;
- reject absolute paths, traversal and duplicate targets;
- calculate attachment SHA-256;
- compare source hash;
- check lifecycle, authority scope and sensitivity fields;
- emit a deterministic verification receipt.

## Output

```text
VALID
VALID_WITH_WARNINGS
INVALID
```

The script does not copy files in V1. The publisher prompt remains responsible for the
reviewable apply step.

---

# Existing non-script artifacts

```text
documentation/prompts/PUBLISHER-PROMPT.md
    packet-driven publication instructions

documentation/prompts/PROMPT-BOOTSTRAP-NEXUS-LAB-DOCUMENTATION.md
    clean repository bootstrap

documentation/governance/INTAKE-AND-QUARANTINE.md
    intake and security rules

documentation/publication-packets/
    candidate or approved packet inputs
```

These are governance inputs, not executable tools.

---

# Delivery order

## M0 — Governance foundation — DONE

```text
clean private repository
single Git root
13-file scaffold
lifecycle
publishing workflow
evidence rules
intake/quarantine
```

## M1 — Manual publication proof

Publish one approved cross-repository document using:

```text
source document
+ approved packet
+ reusable publisher prompt
```

Gate:

```text
source hash = target hash
only allowlisted files changed
owner-reviewed diff
PR merged to main
inventory updated
```

## M2 — Review existing ADR/backlog reporter

Obtain and audit the actual `report-adr-backlog.sh` source. Do not approve based only
on its design document.

Apply the V1 corrections:

```text
no diff body
no direct cross-repo write
explicit project identity
export-only output
```

## M3 — Implement inventory tool

Implement `inventory-documents.py` with synthetic fixtures and read-only guarantees.

## M4 — Foundation Git-aware index pilot

Run the read-only inventory against a clean Foundation worktree using an explicit
Foundation project configuration and an output spool outside the repository.

Produce only:

```text
Git-aware inventory
human report
command ledger
candidate task-to-document index
```

Expected focus:

```text
v0.8.1 baseline linkage
active 0.8.2 plans and evidence
0.9 documents frozen pending integration
release/baseline history
same-ID and same-name candidates
untracked or branch-only documentation
```

No bulk copy and no automatic publication.

## M5 — CLI convergence — DEFERRED

Candidate future direction:

```text
CLI project identity
+ Git provenance
+ documentation index contract
+ explicit local spool
```

No CLI implementation is authorized by the Foundation pilot.

## M6 — Backend audit

Additional security and privacy gates are mandatory because the backend corpus may
contain acquisition fixtures, uploads and domain research.

## M7 — Legacy inventory

Legacy sources are inventoried last and remain external by default.

---

# Deferred tooling

Not part of V1:

```text
plan-consolidation.py
apply-consolidation.py
automatic latest-version selection
automatic document merge
automatic ADR renumbering
automatic archive movement
cross-repository commit or PR creation
```

These capabilities require evidence from the first three tools and explicit owner
approval.

---

# Program gate

The toolchain is successful when:

```text
source repository writes           0
secret values emitted              0
automatic canonical promotions     0
ambiguous lineage                  REVIEW_REQUIRED
exact duplicate detection          deterministic
project identity                   explicit
publication source/target hashes   equal
owner decision                     preserved
```

---

# Immediate next actions

```text
1. Review the Foundation-only index implementation and project configuration.
2. Preserve synthetic test evidence.
3. Run the tool from a clean Foundation worktree with v0.8.1 available locally.
4. Review the external-spool index and task-to-document matrix.
5. Decide whether the index becomes a maintained Foundation/CLI contract.
6. Keep CLI implementation and all non-Foundation repositories deferred.
```

No additional project inventory or Git-workflow automation is opened during the
Foundation pilot.
