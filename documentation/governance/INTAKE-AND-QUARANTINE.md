# Intake and Quarantine

**Status:** CANONICAL GOVERNANCE RULE  
**Scope:** `nexus-lab-documentation`  
**Purpose:** prevent unreviewed, sensitive, duplicated or code-coupled material from entering the canonical documentation repository.

---

## 1. Central rule

> Inventory is not publication. Copying is not promotion. Historical value does not override security or authority.

The repository is not:

- a backup destination;
- a bulk upload folder;
- a codebase archive;
- an evidence quarantine store;
- a location for secrets, real client data or unclassified personal data.

---

## 2. Intake pipeline

```text
External source
↓
Read-only inventory
↓
Security and privacy gate
↓
Authority and lifecycle classification
↓
Candidate disposition
↓
Publication packet
↓
Owner review
↓
Approved copy/apply
↓
Git diff
↓
Commit and push authorization
```

No step may be skipped because a source is old, internal or apparently useful.

---

## 3. Source handling

Sources remain read-only during intake.

Do not:

- rename source files;
- delete source files;
- modify source repositories;
- merge source histories;
- import `.git` directories;
- preserve a codebase by copying it into this repository;
- extract untrusted archives into the repository workspace.

Record, when available:

```text
source kind
source repository
source path
source commit
content SHA-256
document type
declared status
authority scope
sensitivity
```

---

## 4. Security and privacy gate

The following are denied by default:

```text
API keys
passwords
tokens
private keys
.env files
credentials
real client documents
unclassified personal data
real A. or G. material
CV and contact data
raw evidence
repository backups
ZIP/TAR/7Z archives
codebase snapshots
binary files without explicit approval
```

A suspected secret is never reproduced in reports. Record only:

- file;
- line or archive member;
- redacted type;
- finding ID;
- remediation status.

A confirmed secret is treated as compromised until revoked or rotated. Removing it
from Git does not replace rotation.

---

## 5. Quarantine

Quarantine is external to the canonical Git repository.

Potentially sensitive or unsafe sources may be held only in an approved, access-
restricted staging location for classification. The documentation repository stores
at most:

- sanitized metadata;
- hashes;
- finding records;
- approved references.

Rejected material is not copied into `archive/` merely because it has historical
value.

---

## 6. Candidate dispositions

Every intake item receives one candidate disposition:

```text
KEEP_LOCAL
PROMOTE_CENTRAL
LINK_ONLY
EXACT_DUPLICATE
MERGE_CANDIDATE
SUPERSEDED
ARCHIVE
INBOX
SENSITIVE
REVIEW_REQUIRED
REJECT
```

Definitions:

- `KEEP_LOCAL`: remains authoritative in its technical repository.
- `PROMOTE_CENTRAL`: candidate cross-repository authority.
- `LINK_ONLY`: central repository records a reference, not a copy.
- `EXACT_DUPLICATE`: identical hash; provenance is preserved for every source.
- `MERGE_CANDIDATE`: overlapping documents require editorial review.
- `SUPERSEDED`: historically valid and replaced by an identified successor.
- `ARCHIVE`: approved historical material with provenance.
- `INBOX`: unratified idea, conversation or external suggestion.
- `SENSITIVE`: requires explicit handling and access decision.
- `REVIEW_REQUIRED`: authority, lineage or safety is unresolved.
- `REJECT`: not admitted to the documentation repository.

No agent may promote a disposition automatically to `CANONICAL`.

---

## 7. Duplicate and version policy

The same filename does not prove the same document.

Grouping must consider:

```text
authority scope
project
document ID
document type
title
content hash
explicit revision
supersession metadata
Git history
```

Precedence:

```text
1. explicit supersedes relation
2. owner approval
3. declared authority
4. explicit revision
5. compatible lifecycle status
6. Git commit evidence
7. filesystem modification time only as a fallback
```

If lineage is not demonstrable, status is `REVIEW_REQUIRED`.

---

## 8. Publication packet

A document may be published only with:

```yaml
sourceKind: null
sourceRepository: null
sourcePath: null
sourceCommit: null
sourceSha256: null

documentId: null
documentType: null
documentStatus: null
authorityScope: null
sensitivity: null

targetPath: null
allowedFiles: []
approvedBy: null
approvedAt: null
suggestedCommitMessage: null
```

For documents produced in the review workspace, `sourceRepository` and
`sourceCommit` may be null, but `sourcePath` and `sourceSha256` remain required.

If required provenance is missing, publication stops with:

```text
BLOCKED_INCOMPLETE_PUBLICATION_PACKET
```

---

## 9. Apply rules

Publication is an exact, reviewable operation.

```text
approved source hash
→ verify
→ copy/apply to target
→ verify resulting hash
→ show Git diff
→ owner authorizes commit
→ owner authorizes push
```

The publisher must not reinterpret or improve approved content during publication.

If the source or target changed after review:

```text
STALE_SOURCE or STALE_TARGET
→ stop
→ new review
```

---

## 10. Archive rules

Archive preserves approved historical context. It is not a dump.

Every archived document must retain:

```text
source
hash
historical status
archive date
superseding document, when known
reason for archival
```

Do not archive:

- confirmed secrets;
- unclassified personal data;
- codebase snapshots;
- raw evidence;
- material lacking an approved retention basis.

---

## 11. Agent constraints

Agents performing intake:

- operate read-only on sources;
- produce inventories and candidate plans;
- never delete or move source files;
- never choose a canonical document solely by date;
- never expose secret values;
- never auto-merge conflicting documents;
- stop on unknown authority;
- distinguish `OBSERVED`, `INFERRED`, `PROPOSED`, `DECIDED`, `UNKNOWN`, `CONFLICTING` and `LIMIT`.

---

## 12. Final invariant

```text
Script measures.
Agent proposes.
Human decides.
Git preserves approved history.
```

> A source enters the canonical repository only when it is safe, attributable,
> authority-compatible and explicitly approved for publication.
