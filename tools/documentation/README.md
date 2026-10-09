# Git-aware Documentation Index — Foundation pilot

This directory contains a read-only documentation inventory tool and the only project
configuration currently authorized for its pilot: Open Nexus Foundation.

```text
Foundation repository
→ deterministic filesystem inventory
→ Git provenance lookup
→ external spool
→ agent interpretation
→ owner decision
```

The index is a projection. It is not documentation authority and does not decide which
document is canonical.

## Files

```text
inventory-documents.py
    generic read-only index generator;

projects/foundation.json
    approved Foundation roots, repository identity and baseline refs;

tests/test_inventory_documents.py
    synthetic Git fixture tests.
```

No Brain, CLI, stakeholder or business corpus is authorized by this pilot.

## Git linkage

The generated manifest records:

- current branch and HEAD;
- sanitized remote identity, checked against the configured Foundation repository path;
- clean or dirty worktree state;
- `GIT_VERIFIED` or `WORKTREE_UNVERIFIED` source origin;
- required baseline refs and resolved commits (`v0.8.1` is fail-closed for this pilot);
- SHA-256 identity of the script and project configuration;
- for every document, first/last commit, HEAD blob, current SHA-256 and presence at the
  configured baseline refs;
- task IDs, version refs and commit SHAs mentioned by the document.

Author names and email addresses are intentionally not copied from Git history.

## Safety boundary

The tool:

- reads only from the selected Git worktree;
- requires an explicit output directory outside the source repository;
- does not use the network;
- does not stage, commit, push, merge or tag;
- does not rewrite documents;
- does not emit matched secret/PII values;
- does not infer canonical authority;
- does not follow symlinks;
- uses only the Python standard library.

A dirty worktree can be inventoried diagnostically and is labelled
`WORKTREE_UNVERIFIED`. Use `--require-clean` for an index intended to support a clean
Git review or release decision.

## Foundation invocation

Run from any directory, using paths valid on the current machine:

```bash
python3 tools/documentation/inventory-documents.py \
  --repo /path/to/open-nexus-foundation \
  --config tools/documentation/projects/foundation.json \
  --output /tmp/open-nexus-foundation-document-index \
  --require-clean
```

Generated files:

```text
INDEX-MANIFEST.json
DOCUMENT-INVENTORY.jsonl
DOCUMENT-INVENTORY.csv
INVENTORY-REPORT.md
COMMAND-LEDGER.md
```

The output directory is a local spool. Outputs are not committed to Foundation and are
not automatically published to `nexus-lab-documentation`.

## Agent contract

An agent may use the generated index to:

- identify documents changed since `v0.8.1`;
- locate documents attached to a task ID;
- find exact duplicates and same-name candidates;
- flag statuses that need code/Git verification;
- propose an owner-reviewed documentation allowlist.

An agent may not use the index alone to:

- declare a task complete;
- choose the canonical document;
- mutate or archive files;
- infer release conformance;
- authorize a commit, merge, tag or release.

## Current lifecycle

```text
Implementation      CANDIDATE
Authorized project  Foundation only
Execution evidence  synthetic fixture required, then real clean-repo pilot
CLI integration     DEFERRED
```
