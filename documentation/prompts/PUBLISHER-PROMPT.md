# Reusable Documentation Publisher Prompt

Usa questo prompt in una sessione Arena collegata al repository privato
`nexus-lab-documentation`.

Allega alla sessione:

1. uno o più documenti sorgente;
2. un publication packet YAML con stato `APPROVED`.

Il publisher applica il packet e si ferma prima del commit.

---

## Prompt riutilizzabile

```text
# Documentation Publication Task

ROLE:
Documentation Git Publisher

MODE:
STRICT PACKET-DRIVEN PUBLICATION

INPUTS:
- one approved publication packet YAML;
- every source document referenced by the packet, attached to this session.

The publication packet is read-only input.
Do not modify or commit the packet unless it is explicitly included in allowedFiles.

==================================================
PHASE 0 — REPOSITORY GATE
==================================================

Before changing files run:

pwd
git rev-parse --is-inside-work-tree
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git remote -v
git fetch origin --prune
git symbolic-ref refs/remotes/origin/HEAD
git log --oneline --decorate --graph -10

Verify through the available gh command/API:

- repository identity is the repository declared by packet.target.repository;
- repository visibility is private;
- GitHub Pages is disabled;
- current branch derives from the remote default branch;
- working tree is clean;
- no unrelated history exists.

Do not run git init.
Do not change branch.
Do not merge or rebase.
Do not use reset, clean, stash or force push.

If the repository gate fails:

STOP
status = BLOCKED_REPOSITORY_GATE

==================================================
PHASE 1 — PACKET VALIDATION
==================================================

Read the attached YAML packet.

Required packet fields:

schemaVersion
packetId
source or documents
document or document metadata
target
allowedFiles
approval.status
approval.approvedBy
approval.approvedAt
suggestedCommitMessage
publisherRules

Require:

approval.status = APPROVED
approval.approvedBy is not null
approval.approvedAt is not null

If approval is pending or incomplete:

STOP
status = BLOCKED_OWNER_APPROVAL

Validate that every target path is contained exactly in allowedFiles.

Reject:

- absolute paths;
- ../ traversal;
- symlink escapes;
- writes outside repository root;
- writes outside allowedFiles;
- duplicate target paths;
- ambiguous source attachments.

If validation fails:

STOP
status = BLOCKED_INVALID_PACKET

==================================================
PHASE 2 — SOURCE ATTACHMENT AND HASH GATE
==================================================

For every source entry:

1. locate exactly one attached file corresponding to the source document;
2. calculate SHA-256 over the attachment bytes;
3. compare it with source.sha256 in the packet;
4. record line count and byte size;
5. verify that the file is text and contains no NUL bytes.

Do not reconstruct a missing source from chat text.
Do not normalize line endings.
Do not reformat Markdown.
Do not alter encoding.

If an attachment is missing:

STOP
status = BLOCKED_MISSING_SOURCE

If more than one attachment matches:

STOP
status = BLOCKED_AMBIGUOUS_SOURCE

If any hash differs:

STOP
status = SOURCE_HASH_MISMATCH

==================================================
PHASE 3 — SECURITY AND SENSITIVITY GATE
==================================================

Inspect only the approved source attachments and proposed target metadata.

Check for:

- secret-like values;
- API keys or tokens;
- private key material;
- credentials;
- real personal data;
- unapproved A. or G. data;
- binary or archive content;
- source-repository snapshots;
- paths that expose local credentials or private storage.

Do not print any suspected secret value.
Report only:

- finding type;
- source file;
- line or location;
- redacted description.

If a confirmed or unresolved sensitive finding exists:

STOP
status = BLOCKED_SECURITY_FINDING

==================================================
PHASE 4 — STALE TARGET GATE
==================================================

For every target:

- if target does not exist, record CREATE;
- if target exists and the packet contains expectedTargetSha256, verify it;
- if target exists without an expected target hash, stop unless the packet explicitly
  authorizes replacement;
- never overwrite a CANONICAL document by inference;
- never resolve divergence by choosing the newest modification time.

If the target changed after review:

STOP
status = STALE_TARGET

==================================================
PHASE 5 — EXACT PUBLICATION
==================================================

For each approved source:

1. create required parent directories inside the repository;
2. copy the source bytes exactly to the packet target path;
3. calculate the target SHA-256;
4. require target SHA-256 = source SHA-256.

Do not:

- improve wording;
- change headings;
- add frontmatter;
- alter links;
- change status;
- update dates inside the document;
- convert line endings;
- reinterpret architecture;
- merge with similar documents.

If exact-copy verification fails:

STOP
status = TARGET_HASH_MISMATCH

==================================================
PHASE 6 — INDEX AND INVENTORY
==================================================

Update indexes only when their paths are listed in allowedFiles.

For docs/README.md:

- add a concise link under the correct existing section;
- do not reorganize unrelated entries;
- do not rewrite the whole index.

For sources/DOCUMENT-INVENTORY.yaml:

- preserve the existing schema;
- append or update exactly one entry per published document;
- do not invent missing source provenance;
- include at least:

  documentId
  revision
  lifecycle
  documentType
  authorityScope
  sensitivity
  sourceKind
  sourcePath
  sourceSha256
  targetPath
  targetSha256
  approvedBy
  approvedAt

If the inventory schema is missing, invalid or incompatible:

STOP
status = BLOCKED_INVENTORY_SCHEMA

Do not choose a canonical authority not declared by the packet.

==================================================
PHASE 7 — ALLOWLIST AND DIFF GATE
==================================================

Run:

git status --short
git diff --check
git diff --stat
git diff --name-only
git diff

Verify:

- every changed file is in allowedFiles;
- every expected target is present;
- no attached packet was copied accidentally;
- no temporary file exists;
- no unrelated formatting change exists;
- source and target hashes match;
- working tree contains only this publication task.

If any changed file is outside allowedFiles:

Do not attempt destructive cleanup.
STOP
status = BLOCKED_ALLOWLIST_VIOLATION

==================================================
PHASE 8 — STOP BEFORE COMMIT
==================================================

Do not commit.
Do not push.
Do not open a PR.

Return:

Repository:
Branch:
HEAD:
Packet ID:
Approval status:
Source files:
Source SHA-256:
Target files:
Target SHA-256:
Index changes:
Inventory entries:
Changed files:
Diff summary:
Security findings:
Suggested commit message:

Final status must be exactly one of:

READY_FOR_OWNER_COMMIT_REVIEW
BLOCKED_REPOSITORY_GATE
BLOCKED_OWNER_APPROVAL
BLOCKED_INVALID_PACKET
BLOCKED_MISSING_SOURCE
BLOCKED_AMBIGUOUS_SOURCE
SOURCE_HASH_MISMATCH
BLOCKED_SECURITY_FINDING
STALE_TARGET
TARGET_HASH_MISMATCH
BLOCKED_INVENTORY_SCHEMA
BLOCKED_ALLOWLIST_VIOLATION

==================================================
FINAL INVARIANT
==================================================

The packet authorizes what may be published.
The source hash identifies what was approved.
The allowlist constrains what may change.
The Git diff shows what will be committed.
The human owner authorizes commit and push.
```

---

## Secondo messaggio — commit e PR

Invia questo secondo messaggio soltanto dopo aver verificato il diff:

```text
APPROVE_COMMIT_AND_PUSH

I approve the publication diff produced for packet <PACKET_ID>.

Before committing, verify again:

- current branch and HEAD;
- working tree contains only the approved allowlist;
- source and target hashes still match;
- git diff --check passes.

Commit using packet.suggestedCommitMessage.

Push only the current Arena branch.
Do not push directly to the default branch.
Do not force push.

Open or prepare a PR toward the remote default branch.

Return:

- branch;
- commit SHA;
- remote branch SHA;
- PR URL;
- final git status;
- publication receipt data.

Stop after the PR is ready.
```
