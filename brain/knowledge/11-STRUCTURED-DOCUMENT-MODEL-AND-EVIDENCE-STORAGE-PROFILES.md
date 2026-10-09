# Open Nexus — Structured Document Model and Evidence Storage Profiles

**Document ID:** `ON-DOC-2026-1.0`  
**Revision:** `0.1`  
**Status:** PROPOSED ARCHITECTURE — OWNER RATIFICATION PENDING  
**Owner:** Brain / `open-nexus-backend`  
**Normative parent:** `ON-ACQ-2026-1.0` — Knowledge Acquisition & Ingestion Architecture  
**Scope:** structured document extraction, evidence blob storage, deployment profiles  
**Out of scope:** Foundation runtime, Magnifier UI, autonomous ingestion, production compliance claims  
**Date:** 2026-10-07

---

## Normative references

- `06-STORAGE-AND-VALIDATION.md`
- `07-ACQUISITION-AND-MCP.md`
- `09-DOMAIN-ACQUISITION-AND-CANDIDATE-MODELING.md`
- `10-KNOWLEDGE-ACQUISITION-AND-INGESTION-ARCHITECTURE.md`
- `ON-ACQ-2026-1.0` revision 1.1

This document specializes the acquisition architecture. It does not replace its chain
of custody, security model, review gates or authority boundaries.

```text
10 — Knowledge Acquisition & Ingestion Architecture
    ↓ specialized by
11 — Structured Document Model & Evidence Storage Profiles
```

If this proposal is ratified, the parent architecture should reference its approved
revision and resolve owner decision `17.1 Deployment storage profile` accordingly.

---

# 1. Purpose

Define how Open Nexus can preserve and interrogate documents whose meaning depends on
structure, including:

- contracts and clauses;
- procedures and ordered steps;
- policies and controls;
- lists and nested lists;
- registers and matrices;
- tables and individual cells;
- narrative documentation;
- mixed documents containing several of these forms.

Define also where original uploaded bytes, extracted representations, metadata,
canonical records and retrieval projections live across local development, Fly.io
technical tests and later durable deployments.

The target is not to turn every document into a domain model automatically.

```text
Raw document
→ deterministic structural representation
→ precise locators
→ retrieval projection
→ Brain interpretation
→ candidate claims/records
→ human review
→ canonical promotion
```

---

# 2. Central decisions proposed

## 2.1 Original bytes remain evidence authority

```text
RawEvidenceBlob
→ authority for what bytes were acquired
```

Extraction, normalization, chunks, embeddings and model interpretations never replace
the original blob.

## 2.2 Structure is a deterministic derivative

```text
RawEvidenceBlob
→ ExtractedRepresentation
→ ParsedDocument
→ DocumentBlock[]
```

`ParsedDocument` and `DocumentBlock` are extracted representations. They are not
canonical claims and do not prove that source statements are true.

## 2.3 Structure must survive retrieval

A procedure must not become an unordered paragraph. A table row must retain its header
context. A contract clause must retain its identifier and hierarchy.

## 2.4 Storage providers remain adapters

```text
EvidenceBlobStorePort
→ LocalEncryptedBlobStore
→ FlyVolumeBlobStore profile
→ S3CompatibleBlobStore
```

Fly Volumes, Tigris, S3, R2, B2, MinIO or a local filesystem are infrastructure
choices. No provider enters the evidence-domain contract.

## 2.5 Indexes remain rebuildable projections

```text
DocsStore
Keyword/Search Index
Vector Index
Graph
Matrices
Reports
```

None becomes authority merely because it is convenient to query.

---

# 3. Current baseline

## 3.1 Observed Brain behavior

The current DocsStore baseline parses Markdown primarily by headings and returns:

```text
document
document title
section
score
snippet
```

The current ClaimEnvelope work adds section-level line spans and hashes, but the
retrieval representation remains principally section text.

This baseline is useful for:

- narrative architecture documentation;
- heading-scoped search;
- paragraph citations;
- initial source-grounded answers.

## 3.2 Current limitation

The baseline does not yet guarantee preservation of:

- nested list hierarchy;
- procedure-step identity and ordering;
- table header/cell relationships;
- contract-clause hierarchy;
- row identity;
- obligation, condition and exception semantics;
- document-version applicability.

Therefore:

```text
section + snippet
≠
structured document understanding
```

---

# 4. Authority and projection model

```text
RawEvidenceBlob
    acquired byte authority

SourceObservation
    acquisition context, tenant, policy, sensitivity, retention

ExtractedRepresentation
    deterministic format derivative

ParsedDocument / DocumentBlock
    structural derivative

DocumentChunk
    retrieval unit with precise locator

Candidate Claim / Candidate Domain Record
    Brain interpretation

Canonical Record
    human-approved knowledge authority

DocsStore / Search / Vector / Graph
    rebuildable projections
```

Core invariant:

> Raw evidence proves what was acquired. Canonical records preserve what was approved.
> Search projections make approved or explicitly staged material retrievable.

---

# 5. Structured document contracts

The examples in this section are candidate contract shapes. Normative JSON Schema or
Pydantic models require a separate implementation gate.

## 5.1 ParsedDocument

```ts
interface ParsedDocument {
  schemaVersion: "parsed-document/v0.1";
  representationRef: string;
  documentId: string;

  metadata: {
    title?: string;
    documentType:
      | "NARRATIVE"
      | "CONTRACT"
      | "PROCEDURE"
      | "POLICY"
      | "TABLE"
      | "REGISTER"
      | "MIXED";
    declaredVersion?: string;
    authority?: string;
    effectiveFrom?: string;
    effectiveTo?: string;
    language?: string;
  };

  blocks: DocumentBlock[];
  parser: {
    id: string;
    version: string;
    configurationHash: string;
  };
  warnings: ExtractionWarning[];
}
```

`documentType` is extraction metadata. It does not authorize canonical promotion or
assign legal meaning.

## 5.2 Common block envelope

```ts
interface DocumentBlockBase {
  blockId: string;
  kind: string;
  order: number;
  parentBlockId?: string;
  headingPath: string[];
  locator: SourceLocator;
  rawTextSha256: string;
}
```

Every block must preserve:

- deterministic order;
- structural parent when applicable;
- source locator;
- hash over the exact represented text or bytes;
- parser identity/version through the parent representation.

## 5.3 Block union

```ts
type DocumentBlock =
  | HeadingBlock
  | ParagraphBlock
  | ListBlock
  | TableBlock
  | ProcedureStepBlock
  | ContractClauseBlock
  | DefinitionBlock
  | CodeBlock;
```

A format adapter may add format-specific fields, but it must not weaken the common
provenance envelope.

---

# 6. Structural block candidates

## 6.1 Heading and paragraph

```ts
interface HeadingBlock extends DocumentBlockBase {
  kind: "HEADING";
  level: number;
  text: string;
}

interface ParagraphBlock extends DocumentBlockBase {
  kind: "PARAGRAPH";
  text: string;
}
```

## 6.2 Nested list

```ts
interface ListBlock extends DocumentBlockBase {
  kind: "LIST";
  ordered: boolean;
  items: ListItem[];
}

interface ListItem {
  itemId: string;
  order: number;
  text: string;
  children: ListItem[];
  locator: SourceLocator;
}
```

Flattening nested items into one paragraph is non-conformant.

## 6.3 Table

```ts
interface TableBlock extends DocumentBlockBase {
  kind: "TABLE";
  columns: Array<{
    columnId: string;
    label: string;
    order: number;
  }>;
  rows: TableRow[];
}

interface TableRow {
  rowId: string;
  order: number;
  cells: Record<string, {
    text: string;
    locator: SourceLocator;
    textSha256: string;
  }>;
}
```

A retrieved cell must retain:

```text
column label
row identity
row order
cell locator
source document/version
```

## 6.4 Procedure step

```ts
interface ProcedureStepBlock extends DocumentBlockBase {
  kind: "PROCEDURE_STEP";
  stepId: string;
  sequence: number;
  actor?: string;
  action: string;
  inputs: string[];
  outputs: string[];
  requiredEvidence: string[];
  nextStepIds: string[];
  exceptions: string[];
}
```

Fields absent from the source remain absent or `UNKNOWN`. A deterministic extractor
must not infer actors, evidence or transitions from generic professional knowledge.

## 6.5 Contract or policy clause

```ts
interface ContractClauseBlock extends DocumentBlockBase {
  kind: "CONTRACT_CLAUSE";
  clauseId: string;
  title?: string;
  actor?: string;
  modality:
    | "MUST"
    | "MUST_NOT"
    | "MAY"
    | "SHOULD"
    | "DECLARATIVE"
    | "UNKNOWN";
  statement: string;
  conditions: string[];
  exceptions: string[];
  references: string[];
}
```

Automated modality classification beyond explicit source markers is interpretation,
not deterministic extraction, and must be labelled accordingly.

## 6.6 Definition

```ts
interface DefinitionBlock extends DocumentBlockBase {
  kind: "DEFINITION";
  term: string;
  definition: string;
}
```

---

# 7. Deterministic extraction boundary

## 7.1 Deterministic extraction may derive

- Markdown heading hierarchy;
- list nesting and order;
- explicit table headers, rows and cells;
- explicit step/clause identifiers;
- explicit labels such as `Actor`, `Input`, `Output`, `Evidence`;
- source line/byte positions;
- exact hashes;
- document-declared metadata.

## 7.2 Brain interpretation may propose

- implicit actors;
- unstated workflow transitions;
- clause modality not explicit in the source;
- inferred responsibility;
- domain relationships;
- candidate evidence requirements;
- conflicts and gaps.

These are candidate records with provenance, never parser output silently promoted as
source fact.

## 7.3 One-AI-entry invariant

```text
acquisition
→ deterministic extraction
→ deterministic structural projection
→ retrieval
→ one Brain interpretation
→ deterministic validation
→ human review
```

No LLM is required to upload, hash, store, parse explicit Markdown structure, build
locators or calculate hashes.

---

# 8. Locator and hashing model

The parent architecture defines `SourceLocator` as a versioned discriminated union.
Structured blocks reuse it.

```text
Markdown
→ heading path + line range + optional byte range

PDF
→ page + text span or bounding box

DOCX
→ heading path + paragraph index

CSV
→ row index + column key

JSON
→ RFC 6901 JSON Pointer
```

Hash layers remain distinct:

```text
RawEvidenceBlob.blobHash
    hash over acquired bytes

ExtractedRepresentation.extractedContentSha256
    hash over deterministic extracted content

DocumentBlock.rawTextSha256
    hash over block text represented by the locator

DocumentChunk.chunkSha256
    hash over retrieval-unit text

ClaimEnvelope.excerptSha256
    hash over the exact excerpt emitted to the consumer
```

A hash proves byte equality against an expected digest. It does not prove that the
source is authoritative or true.

---

# 9. Retrieval behavior

Retrieval operates over projections without discarding structure.

## 9.1 Candidate retrieval units

```text
narrative query
→ paragraph/section chunks

procedure query
→ procedure steps + containing procedure identity

contract query
→ clauses + clause hierarchy

table query
→ rows/cells + header map

list query
→ item + ancestor items
```

## 9.2 Required retrieval metadata

Every hit should eventually expose:

```text
documentId
documentType
blockId
blockKind
headingPath
order
source locator
source/blob/representation refs
review/source tier
block/chunk hash
```

## 9.3 Retrieval candidates are not evidence sources

A retrieved block becomes a `ClaimEnvelope` source only when a claim actually
references it. Irrelevant retrieval candidates remain in `EvaluationTrace`, not in the
evidence-source list.

---

# 10. Authoring profile for future governed Markdown

Existing documents remain valid inputs. No repository-wide rewrite is authorized.

For new high-value procedures, contracts and registers, the following profile is
recommended:

```markdown
---
documentId: PROC-AUDIT-001
documentType: PROCEDURE
version: 2.1
authority: Quality Office
effectiveFrom: 2026-10-01
---

# Audit engagement procedure

## STEP-01 — Open the engagement

**Actor:** Engagement Owner  
**Input:** Approved mandate  
**Output:** Engagement Record  
**Evidence:** Signed mandate

1. Verify the mandate.
2. Create the engagement record.
3. Assign the reviewer.
```

Guidelines:

- stable document and clause/step identifiers;
- explicit version and validity dates when meaningful;
- explicit table headers;
- numbered steps;
- explicit actor/input/output/evidence labels;
- no meaning encoded only through color or visual placement;
- avoid merged table cells in material intended for deterministic extraction;
- preserve human readability.

The authoring profile is recommended, not required for acquisition.

---

# 11. Storage topology

## 11.1 Curated text and contracts

Use Git for:

- architecture and governance documents;
- approved Markdown procedures;
- ADR/PRD/Epic/backlog;
- versioned schemas and fixtures;
- small canonical text records where Git remains the approved record store.

Git is not the target for frequent binary uploads or large scans.

## 11.2 Raw uploaded evidence

Use `EvidenceBlobStorePort` for:

- PDF/DOCX/XLSX;
- images and scans;
- uploaded Markdown/plain text when chain of custody matters;
- large attachments;
- immutable raw acquisition bytes.

Candidate content-addressed key:

```text
<tenant>/sha256/<first-2>/<next-2>/<full-sha256>
```

The original filename is metadata, never a storage path.

## 11.3 Evidence metadata

Use `EvidenceMetadataStorePort` for:

- blob and observation refs;
- original labels;
- media type;
- tenant and policy;
- sensitivity;
- retention and legal hold;
- processing state;
- extractor/chunker versions;
- ACL references;
- lifecycle events and tombstones.

## 11.4 Canonical records

`CanonicalRecordStorePort` owns promoted records and review decisions. It is not
selected by convenience from the blob or search provider.

## 11.5 Search and vector projections

Keyword, FTS, vector and graph stores are disposable projections. They may be rebuilt
from approved representations and canonical records.

## 11.6 Redis boundary

Redis is appropriate for:

- cache;
- session state;
- job status;
- queues;
- short-lived retrieval state.

Redis is not document, evidence or canonical-record authority.

---

# 12. Storage ports

The parent architecture already defines the relevant ports. This specialization keeps
them provider-neutral.

```ts
interface EvidenceBlobStorePort {
  put(input: PutEvidenceBlobInput): Promise<StoredEvidenceBlob>;
  get(blobRef: string): Promise<ReadableByteStream>;
  stat(blobRef: string): Promise<StoredEvidenceBlobMetadata>;
  delete(blobRef: string, decisionRef: string): Promise<DeletionReceipt>;
}
```

Required adapter behavior:

```text
streaming writes
SHA-256 verification
non-user-controlled object keys
no overwrite for an existing content-addressed key
bounded reads
private-by-default access
explicit delete decision
structured receipts
```

Reference adapters:

```text
InMemoryEvidenceBlobStore
    unit tests and synthetic fixtures

LocalEncryptedBlobStore
    local development and approved single-node/on-premise profiles

S3CompatibleBlobStore
    distributed and ephemeral-filesystem deployments
```

`FlyVolumeBlobStore` is a deployment configuration of a local adapter, not a new
domain contract.

---

# 13. Deployment storage profiles

## 13.1 TEST_EPHEMERAL

```text
blob adapter       InMemoryEvidenceBlobStore or temporary filesystem
metadata           in-memory / temporary SQLite
persistence        none
allowed data       synthetic only
```

Use for unit, contract and parser tests.

## 13.2 LOCAL_SINGLE_NODE

```text
blob adapter       LocalEncryptedBlobStore
metadata           SQLite / JSONL according to milestone
persistence        local directory
allowed data       synthetic or explicitly authorized internal test data
backup             explicit export when preservation matters
```

Use for workstation development and approved on-premise experiments.

## 13.3 FLY_VOLUME_TECHNICAL_PILOT

```text
blob adapter       LocalEncryptedBlobStore mounted on a Fly Volume
metadata           SQLite or existing minimal metadata adapter
machine count      1
region             1
volume             minimum practical size
availability       non-production
allowed data       synthetic/sanitized only by default
```

Purpose:

- prove persistence across restart/deploy;
- test streaming upload and exact-byte retrieval;
- test hashing and deduplication;
- test parser/receipt lifecycle;
- measure operational cost.

Not suitable as the only authoritative copy of important evidence.

## 13.4 S3_OBJECT_PILOT

```text
blob adapter       S3CompatibleBlobStore
candidate provider Tigris, R2, S3, B2 or MinIO
metadata           SQLite for single-user pilot; Postgres for multi-user
access             private bucket; server-side credentials only
allowed data       governed pilot data after security approval
```

This is the preferred profile for a real upload/acquisition pilot because object bytes
are separated from the lifecycle of one application Machine.

## 13.5 PRODUCTION_DURABLE

Requires a separate production-readiness decision covering:

- provider durability and availability;
- replication and backups;
- tenant isolation;
- encryption and key management;
- retention and deletion;
- legal hold;
- disaster recovery tests;
- access audit;
- regional/data-residency requirements;
- cost and quota monitoring.

This document does not declare any provider production-compliant.

---

# 14. Fly.io technical pilot assessment

## 14.1 Fly Volume suitability

Fly Volumes are local persistent storage tied to a Machine/server and one region. They
are not automatically replicated between volumes. Fly recommends application-level
replication, redundancy and independent backups for important data.

Therefore:

```text
single-machine technical test
→ APPROPRIATE

sole copy of important evidence
→ NOT APPROPRIATE

production authority without replication/backup
→ NOT AUTHORIZED
```

## 14.2 Fly Volume cost reference

As of 2026-10-07, Fly publishes approximately:

```text
Volume capacity          USD 0.15 / provisioned GB / month
Volume snapshots         USD 0.08 / stored GB / month
Snapshot allowance       first 10 GB / month free
Smallest running Machine about USD 2.19 / month if continuously running
```

Volumes continue billing while detached or attached to a stopped Machine.

These prices are operational references, not architecture constants. Verify the Fly
Cost Explorer before provisioning.

## 14.3 Bounded Fly pilot profile

Candidate limits:

```text
volume size              1 GB
retained payload target  <= 500 MB
max raw file             10 MB
retention                7–30 days
machine count            1
region                   one EU region selected explicitly
source classes           text/plain, text/markdown initially
sensitive/real data      prohibited unless separately authorized
```

A scheduled export or external backup is required for any fixture that cannot be
recreated.

---

# 15. Tigris / S3-compatible pilot assessment

Tigris is available through Fly as an S3-compatible object storage extension. The
architecture treats it only as a candidate `S3CompatibleBlobStore` adapter.

## 15.1 Current pricing reference

As of 2026-10-07, Tigris publishes approximately:

```text
Standard storage         first 5 GB free
Beyond allowance         USD 0.02 / GB / month
Class A allowance        first 10,000 requests / month
Class B allowance        first 100,000 requests / month
Provider egress          advertised as free
```

Fly bills extensions at provider list price and may separately meter applicable data
transfer from Fly Machines to third-party extension services. Real pilot cost must be
observed in the Fly dashboard.

## 15.2 Proposed use

```text
synthetic parser/unit tests
→ in-memory/local

persistence mechanics test
→ 1 GB Fly Volume acceptable

first real governed upload pilot
→ private S3-compatible bucket preferred
```

Tigris is the first operational candidate because it is S3-compatible and can be
provisioned through Fly. It is not embedded in domain contracts and is not yet an
approved production dependency.

---

# 16. Cost and lifecycle controls

Every non-ephemeral deployment must enforce:

```text
tenant quota
per-file size limit
total retained-byte limit
request rate limit
retention policy
quarantine TTL
failed-extraction TTL
orphan-blob collection policy
object-count metrics
storage-byte metrics
request metrics
budget alerts
```

Cost reduction priorities:

1. deduplicate within one tenant by raw SHA-256;
2. do not duplicate raw bytes for each observation;
3. keep search/vector projections rebuildable;
4. expire rejected/quarantined partial blobs;
5. archive or delete synthetic pilot data on schedule;
6. avoid retaining raw model prompts/responses unless explicitly governed;
7. measure before introducing mandatory embeddings.

Cross-tenant deduplication remains prohibited without a separate security decision.

---

# 17. Upload and parser security gate

Every uploaded object is untrusted.

Required before normal staging:

```text
explicit authenticated trigger
tenant and classification
streaming size enforcement
SHA-256 over received bytes
MIME sniffing
extension treated only as a label
archive traversal rejection
decompression limits
macro/script non-execution
parser CPU/memory/time limits
quarantine state
private-by-default storage
structured audit receipt
prompt-injection isolation
```

Initial mandatory media types remain:

```text
text/plain
text/markdown
```

PDF, DOCX, XLSX, images and OCR require their own extractor/security milestones. The
existence of object storage does not authorize their ingestion.

---

# 18. Pilot roadmap

## D0 — Current-structure reality audit

Read-only inventory of:

- DocsStore parser and search hit shape;
- current document corpus;
- Markdown tables/lists/procedures;
- current line/hash behavior;
- current storage and deployment settings;
- current Fly volumes and data directories.

## D1 — Structural Markdown parser

```text
Markdown bytes
→ ParsedDocument
→ heading/paragraph/list/table blocks
→ stable locators and hashes
```

No Brain/model call.

## D2 — Procedure/contract authoring profile

Test explicit identifiers and labels on synthetic G./A. fixtures. Do not migrate the
whole corpus.

## S0 — Storage adapter conformance fixtures

One fixture suite shared by:

```text
InMemoryEvidenceBlobStore
LocalEncryptedBlobStore
S3CompatibleBlobStore
```

## S1 — Fly Volume technical pilot

Synthetic Markdown/plain-text only, bounded by the profile in section 14.

## S2 — S3-compatible object pilot

Private bucket, content-addressed keys, exact-byte roundtrip, lifecycle cleanup and
cost observation.

## S3 — Governed upload pilot

Requires approved security policy, retention, authorization and review workflow.

---

# 19. Acceptance criteria

## 19.1 Structured document model

```text
□ original bytes remain retrievable and hash-verifiable
□ parser is deterministic for pinned version/configuration
□ heading hierarchy survives
□ nested list hierarchy survives
□ table header/row/cell relationships survive
□ explicit procedure step IDs/order survive
□ explicit clause IDs/hierarchy survive
□ every block has a precise source locator
□ block/chunk hashes are reproducible
□ absent semantics remain absent/UNKNOWN
□ parser performs no model call
```

## 19.2 Blob-store adapters

```text
□ same bytes produce same SHA-256
□ same-tenant duplicate upload reuses one blob
□ separate observations remain separate
□ exact-byte roundtrip succeeds
□ overwrite of content-addressed key is rejected
□ filename cannot escape storage root or define object key
□ private-by-default access
□ deletion requires a decision reference
□ failed writes leave no valid observation
□ adapter-specific errors map to stable contract errors
```

## 19.3 Fly Volume pilot

```text
□ restart/deploy persistence demonstrated
□ data-loss limitations stated
□ volume/snapshot cost recorded
□ export/restore test demonstrated
□ storage and object quotas enforced
□ no sensitive/real client data used without approval
□ no production-readiness claim
```

## 19.4 S3-compatible pilot

```text
□ private bucket
□ credentials server-side only
□ multipart/streaming limits
□ content-addressed keys
□ exact-byte roundtrip
□ tenant prefix isolation
□ lifecycle cleanup
□ cost metrics recorded
□ provider replacement demonstrated through the port contract
```

---

# 20. Owner decisions required

Before implementation beyond read-only audits, ratify:

## 20.1 Contract scope

```text
ParsedDocument / DocumentBlock
→ approved as ExtractedRepresentation specialization?
```

## 20.2 First structural media profile

Proposed:

```text
text/markdown
text/plain
```

## 20.3 Technical persistence pilot

Choose:

```text
A. Fly Volume first
B. S3-compatible/Tigris first
C. both, in sequence
```

Recommended:

```text
C
→ Fly Volume for persistence mechanics
→ S3-compatible for the first real upload pilot
```

## 20.4 Initial metadata store

```text
SQLite for single-user technical pilot
Postgres for multi-user/governed pilot
```

## 20.5 Initial data classification

Proposed:

```text
synthetic and sanitized internal documents only
```

Real client, privileged, regulated or personal data remains prohibited until a
separate governance decision.

---

# 21. Non-goals

This proposal does not authorize:

- autonomous crawling;
- arbitrary file upload in production;
- OCR;
- macros or scripts;
- recursive archive extraction;
- automatic claim truth classification;
- automatic canonical promotion;
- mandatory vector search;
- cross-tenant deduplication;
- Foundation-owned ingestion;
- provider-specific storage contracts;
- legal, GMP or regulatory compliance claims;
- public Magnifier UI implementation.

---

# 22. External operational references

Pricing and operational characteristics must be rechecked before provisioning.

- Fly.io resource pricing: <https://fly.io/docs/about/pricing/>
- Fly Volume overview and limitations: <https://fly.io/docs/volumes/overview/>
- Fly.io Tigris integration: <https://fly.io/docs/tigris/>
- Tigris pricing: <https://www.tigrisdata.com/pricing/>

These references inform deployment profiles. They are not normative Open Nexus
contracts.

---

# 23. Final principles

```text
Original bytes remain evidence authority.
Structure is preserved, not flattened away.
Explicit structure is extracted deterministically.
Implicit meaning remains candidate interpretation.
Raw blobs, canonical records and indexes have different ownership.
Storage providers remain adapters.
Fly Volume is acceptable for a bounded technical pilot.
Object storage is preferred for the first real governed upload pilot.
Search and vector indexes remain rebuildable.
Brain interprets and proposes.
Human review promotes or rejects.
Foundation does not ingest.
```

> A document becomes useful to Open Nexus not when it is merely uploaded, but when its
> bytes, structure, source, processing history and review state remain inspectable
> throughout every projection and interpretation.
