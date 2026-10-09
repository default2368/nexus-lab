# Open Nexus — Knowledge Acquisition & Ingestion Architecture

**Document ID:** `ON-ACQ-2026-1.0`  
**Revision:** `1.1`  
**Status:** APPROVED — MINIMAL ACQUISITION ARCHITECTURE  
**Implementation authorization:** M0 and M1; M2+ remain gated by milestone evidence  
**Target:** Open Nexus 1.0 Minimal Acquisition Slice  
**Extended connectors:** post-1.0 unless promoted by an explicit release decision

---

## Normative references

- `05-EVALUATION.md`
- `06-STORAGE-AND-VALIDATION.md`
- `07-ACQUISITION-AND-MCP.md`
- `08-RULESETS-AND-AGENT-PROFILES.md`
- `09-DOMAIN-ACQUISITION-AND-CANDIDATE-MODELING.md`
- `ADR-0016-SEMANTIC-ENTITY-PROJECTION-MODEL.md`

Cross-repository implementations must pin the commit or release containing the
normative reference. A filename without a version is not a compatibility contract.

---

# 1. Purpose

Knowledge acquisition is the deterministic chain of custody through which external
content enters Open Nexus without losing:

- origin;
- byte-level integrity;
- acquisition context;
- processing history;
- source locator;
- sensitivity classification;
- review status;
- epistemic status.

Acquisition is not autonomous web roaming and is not equivalent to scraping,
chunking, embedding, interpretation or canonical promotion.

```text
Acquisition preserves and derives.
Brain interprets and proposes.
Human review promotes or rejects.
Indexes project canonical and staging records.
Foundation renders materialized PageData.
```

---

# 2. Non-goals

This architecture does not authorize:

```text
autonomous recursive crawling
automatic canonical promotion
self-training from model output
execution of source-provided instructions
execution of scripts or macros embedded in documents
Foundation-owned fetching or ingestion
unreviewed staging content in default Roy answers
real client data without approved governance
generic cloud connectors in the 1.0 mandatory release gate
```

---

# 3. System boundaries

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Open Nexus Contracts                                                        │
│ Defines acquisition, evidence, extraction, locator and review contracts.    │
├─────────────────────────────────────────────────────────────────────────────┤
│ CLI / UI                                                                    │
│ Explicitly starts acquisition and displays status and receipts.             │
├─────────────────────────────────────────────────────────────────────────────┤
│ Brain Acquisition Module                                                    │
│ Orchestrates policy, quarantine, extraction, staging and promotion flow.    │
├─────────────────────────────────────────────────────────────────────────────┤
│ Acquisition Providers                                                       │
│ Execute upload, HTTP fetch, extraction, chunking and connector operations.  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Evidence Stores                                                             │
│ Preserve content-addressed blobs and append-only observation metadata.      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Canonical Record Store                                                      │
│ Source of truth for promoted knowledge records and review decisions.        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Search / DocsStore / Vector Index                                            │
│ Rebuildable projections for retrieval and experience.                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Foundation Runtime                                                          │
│ Renders PageData and experiences; never fetches or ingests external data.   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Layering invariant

> Foundation does not own or execute fetch, upload or ingestion orchestration.
> Foundation receives only validated records and materialized projections conforming
> to PageData and other approved public contracts.

## Brain implementation invariant

```text
Settings owns declared configuration.
Providers own execution.
Modules own orchestration.
Routes own API contracts.
Settings never owns behavior.
```

---

# 4. Complete chain of custody

```text
Explicit User Trigger
↓
AcquisitionRequest
↓
Security and Classification Gate
↓
Fetch or Upload Adapter
↓
Raw byte stream with hard limits
↓
SHA-256 over raw bytes
↓
RawEvidenceBlob quarantine
↓
SourceObservation append
↓
Deterministic Extraction
↓
ExtractedRepresentation
↓
Structural Chunking and Source Locators
↓
DocumentChunks
↓
Staging Index
↓
Brain Interpretation
↓
Candidate Claims / Candidate Domain Records
↓
Human Review Decision
↓
Canonical Record Promotion
↓
DocsStore / Search / Vector projections
↓
Assistant and Magnifier experiences
```

Generative AI enters only at Brain Interpretation. Fetching, hashing, extraction,
chunking, schema validation, review recording and projection remain deterministic or
human-authorized.

---

# 5. Data model separation

The architecture separates four objects that must never be collapsed.

## 5.1 RawEvidenceBlob

Content-addressed raw bytes. A blob records what was received, not whether its claims
are true.

## 5.2 SourceObservation

The context in which a source was acquired: who requested it, from where, when, under
which tenant and policy, and which blob was observed.

Multiple SourceObservations may reference one blob.

## 5.3 ExtractedRepresentation

A deterministic derivative produced by a versioned extractor. It never replaces the
raw blob.

## 5.4 DocumentChunk

A retrieval unit derived from an ExtractedRepresentation with a precise SourceLocator.
It is not a canonical claim and is not itself domain knowledge.

```text
SourceObservation
        ↓ references
RawEvidenceBlob
        ↓ deterministic extraction
ExtractedRepresentation
        ↓ deterministic chunking
DocumentChunk
```

---

# 6. Processing stage and epistemic status

Technical progress and epistemic confidence are independent axes.

## ProcessingStage

```text
REQUESTED
SECURITY_REJECTED
RAW_CAPTURED
EXTRACTION_PENDING
EXTRACTED_REPRESENTATION
STRUCTURAL_CHUNK
STAGED
INTERPRETED_CLAIM
REVIEWED
CANONICAL_RECORD
PROJECTION_VIEW
```

## EpistemicStatus

```text
SOURCE_UNVERIFIED
EXTRACTED_UNVERIFIED
CANDIDATE
DOCUMENTED
HUMAN_VALIDATED
CONTESTED
REJECTED
SUPERSEDED
```

`CONTESTED` and `REJECTED` are distinct:

- `REJECTED` means a candidate was not accepted;
- `CONTESTED` means material evidence or authorities disagree;
- `SUPERSEDED` preserves a historical record replaced by a later valid record.

## ReviewStatus

Where operationally useful, review state is represented separately:

```text
UNREVIEWED
APPROVED_FOR_STAGING
APPROVED_FOR_CANONICAL_RETRIEVAL
REJECTED
REQUIRES_REVISION
```

A document approved for retrieval does not make every statement in it true.

---

# 7. Contract inventory

The minimal architecture requires:

```text
AcquisitionRequest
AcquisitionReceipt
RawEvidenceBlob
SourceObservation
SecurityAuditRecord
ExtractionJob
ExtractedRepresentation
SourceLocator
DocumentChunk
DocumentReviewDecision
ClaimReviewDecision
DomainModelReviewDecision
PromotionDecision
```

All contracts use versioned URN identifiers until a public schema domain is approved.

```text
urn:open-nexus:schema:<contract>:v1
```

Public schema naming remains subject to brand and IP clearance.

---

# 8. Core contracts

The following JSON examples are illustrative contract shapes. Normative JSON Schema or
Pydantic models must be produced and validated before external use.

## 8.1 AcquisitionRequest

The request records explicit initiative. Payload bytes are transported separately and
must never be embedded in logs or metadata records.

```json
{
  "$schema": "urn:open-nexus:schema:acquisition-request:v1",
  "requestId": "req-01J9AZ6N7E7F0R7Y9V0W1X2Y3Z",
  "tenantRef": "tenant-local-dev",
  "source": {
    "kind": "upload",
    "declaredMediaType": "text/markdown",
    "originalName": "activity-description.md"
  },
  "initiatedBy": "user-owner-01",
  "classification": "internal",
  "requestedAt": "2026-09-29T10:00:00Z",
  "traceId": "tr-01J9AZ7B2G8C1M4P6Q9R0S3T5V",
  "idempotencyKey": "idem-01J9AZ8M4D2K7N1X6Y3Z8W5V0Q",
  "policyProfile": "local-upload-v1"
}
```

For URL acquisition, the source variant contains a sanitized URL without persisted
credentials. Sensitive query parameters must be redacted or encrypted according to
policy.

## 8.2 AcquisitionReceipt

```json
{
  "$schema": "urn:open-nexus:schema:acquisition-receipt:v1",
  "requestRef": "req-01J9AZ6N7E7F0R7Y9V0W1X2Y3Z",
  "observationRef": "obs-01J9AZ9V8D6F4H2J0K7M5N3P1Q",
  "blobRef": "evidence-blob:tenant-local-dev:sha256:af7d015e32b3517baff5e3bb8ce13d5856bea7387a5e89f86419cf35cac43e75",
  "duplicateBlob": false,
  "processingStage": "RAW_CAPTURED",
  "extractionStatus": "NOT_REQUESTED",
  "promotionStatus": "NOT_ELIGIBLE",
  "appliedPolicy": {
    "profile": "local-upload-v1",
    "rawSizeLimitBytes": 15728640,
    "redirectLimit": 0
  },
  "completedAt": "2026-09-29T10:00:01Z"
}
```

## 8.3 RawEvidenceBlob

`RawEvidenceBlob` is content-addressed and non-mutating. It contains technical storage
metadata, not source truth, tenant retention or legal meaning.

```json
{
  "$schema": "urn:open-nexus:schema:raw-evidence-blob:v1",
  "blobRef": "evidence-blob:tenant-local-dev:sha256:af7d015e32b3517baff5e3bb8ce13d5856bea7387a5e89f86419cf35cac43e75",
  "blobHash": "af7d015e32b3517baff5e3bb8ce13d5856bea7387a5e89f86419cf35cac43e75",
  "hashAlgorithm": "sha256",
  "byteSize": 142050,
  "sniffedMediaType": "text/markdown",
  "storageRef": "blob-store:tenant-local-dev:af7d015e32b3517baff5e3bb8ce13d5856bea7387a5e89f86419cf35cac43e75",
  "deduplicationScope": "tenant",
  "storageState": "QUARANTINED",
  "storedAt": "2026-09-29T10:00:01Z"
}
```

SHA-256 values must match:

```text
^[a-f0-9]{64}$
```

Hash integrity does not by itself guarantee immutability. The adapter must enforce
non-mutating keys, append-only metadata, versioning or equivalent controls.

## 8.4 SourceObservation

Retention, legal hold, sensitivity and acquisition context belong to the observation
or its governed references, not to a deduplicated blob.

```json
{
  "$schema": "urn:open-nexus:schema:source-observation:v1",
  "observationId": "obs-01J9AZ9V8D6F4H2J0K7M5N3P1Q",
  "blobRef": "evidence-blob:tenant-local-dev:sha256:af7d015e32b3517baff5e3bb8ce13d5856bea7387a5e89f86419cf35cac43e75",
  "sourceType": "upload",
  "sourceLabel": "activity-description.md",
  "tenantRef": "tenant-local-dev",
  "sensitivity": "internal",
  "retentionPolicy": "local-dev-30d",
  "legalHold": false,
  "observedAt": "2026-09-29T10:00:01Z",
  "requestedBy": "user-owner-01",
  "traceId": "tr-01J9AZ7B2G8C1M4P6Q9R0S3T5V",
  "processingStage": "RAW_CAPTURED",
  "epistemicStatus": "SOURCE_UNVERIFIED"
}
```

For HTTP sources, an `httpMetadata` object records sanitized canonical URI, status,
redirect chain, TLS verification and peer-validation outcome.

## 8.5 SecurityAuditRecord

Security rejection produces an append-only audit record without exposing credentials,
secrets or sensitive URL parameters.

```json
{
  "$schema": "urn:open-nexus:schema:security-audit-record:v1",
  "auditId": "sec-01J9AZB4V6C8X0N2M5K7H9F1D3",
  "requestRef": "req-01J9AZ6N7E7F0R7Y9V0W1X2Y3Z",
  "tenantRef": "tenant-local-dev",
  "stage": "SECURITY_GATE",
  "decision": "DENY",
  "reasonCode": "SOURCE_POLICY_VIOLATION",
  "targetFingerprint": "sha256:7e5c2f4c1c2e6b8979f8cf1786890b1d8750c76af0fa9f655bf747f8695d3a64",
  "recordedAt": "2026-09-29T10:00:00Z"
}
```

A request denied before fetch produces no RawEvidenceBlob. A rejection after partial
receipt follows a separate quarantine and short-retention policy.

## 8.6 ExtractionJob

```json
{
  "$schema": "urn:open-nexus:schema:extraction-job:v1",
  "jobId": "extjob-01J9AZC8G4T2Q6W8R0Y3U5I7O9",
  "observationRef": "obs-01J9AZ9V8D6F4H2J0K7M5N3P1Q",
  "blobRef": "evidence-blob:tenant-local-dev:sha256:af7d015e32b3517baff5e3bb8ce13d5856bea7387a5e89f86419cf35cac43e75",
  "extractor": {
    "id": "plain-markdown-extractor",
    "version": "1.0.0",
    "configurationHash": "d4d3c2b1a09876543210fedcba9876543210fedcba9876543210fedcba987654"
  },
  "status": "COMPLETED",
  "startedAt": "2026-09-29T10:01:00Z",
  "completedAt": "2026-09-29T10:01:01Z"
}
```

## 8.7 ExtractedRepresentation

```json
{
  "$schema": "urn:open-nexus:schema:extracted-representation:v1",
  "representationId": "repr-01J9AZD2F4G6H8J0K2L4M6N8P0",
  "observationRef": "obs-01J9AZ9V8D6F4H2J0K7M5N3P1Q",
  "rawBlobRef": "evidence-blob:tenant-local-dev:sha256:af7d015e32b3517baff5e3bb8ce13d5856bea7387a5e89f86419cf35cac43e75",
  "contentRef": "extracted-content:tenant-local-dev:sha256:c8f2b3e198a27d5f4e1b0c9a8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e",
  "extractedContentSha256": "c8f2b3e198a27d5f4e1b0c9a8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e",
  "contentByteSize": 84120,
  "encoding": "utf-8",
  "normalizationProfile": "markdown-structural-v1",
  "extractor": {
    "id": "plain-markdown-extractor",
    "version": "1.0.0"
  },
  "warnings": [],
  "extractedAt": "2026-09-29T10:01:01Z",
  "processingStage": "EXTRACTED_REPRESENTATION",
  "epistemicStatus": "EXTRACTED_UNVERIFIED"
}
```

## 8.8 SourceLocator

`SourceLocator` is a versioned discriminated union. The common envelope is stable;
format coordinates remain format-specific.

```json
{
  "$schema": "urn:open-nexus:schema:source-locator:v1",
  "locatorType": "markdown",
  "locatorVersion": "1",
  "sourceObservationRef": "obs-01J9AZ9V8D6F4H2J0K7M5N3P1Q",
  "representationRef": "repr-01J9AZD2F4G6H8J0K2L4M6N8P0",
  "coordinates": {
    "headingPath": ["Workflow", "Approval"],
    "startLine": 42,
    "endLine": 47
  },
  "excerpt": "The approver validates the decision before closure.",
  "excerptSha256": "8c2c6d95765a94edcf5964608801338a33f32a0f4f98e0bf0cd004f11e974aa2"
}
```

Supported locator variants:

```text
web        canonical URI + heading path + text/DOM anchor
pdf        page + text span or bounding box
DOCX       heading path + paragraph index
markdown   heading path + line range
JSON       RFC 6901 JSON Pointer
CSV        row index + column key
```

## 8.9 DocumentChunk

```json
{
  "$schema": "urn:open-nexus:schema:document-chunk:v1",
  "chunkId": "chk-01J9AZE6R4T2Y8U0I3O5P7A9S1",
  "representationRef": "repr-01J9AZD2F4G6H8J0K2L4M6N8P0",
  "chunkIndex": 3,
  "locatorRef": "locator-01J9AZF8D6S4A2P0O9I7U5Y3T1",
  "text": "The approver validates the decision before closure.",
  "chunkSha256": "3a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b",
  "tokenization": {
    "tokenizerId": "none",
    "tokenizerVersion": null,
    "tokenCount": null
  },
  "processingStage": "STRUCTURAL_CHUNK",
  "epistemicStatus": "EXTRACTED_UNVERIFIED"
}
```

Structural chunking must not require a model-specific tokenizer. Token metadata is an
optional derived projection.

## 8.10 Review and promotion decisions

Review is separated by target kind.

```text
DocumentReviewDecision
    approves or rejects a representation for canonical retrieval

ClaimReviewDecision
    accepts, rejects, contests or supersedes a candidate claim

DomainModelReviewDecision
    approves or rejects a candidate domain-model revision

PromotionDecision
    records who promoted which revision, under which policy and evidence
```

A review decision is append-only. Corrections produce a new decision or revision; they
do not rewrite history silently.

---

# 9. Storage, retention and deletion

## 9.1 Record source of truth

```text
Canonical Record Store       source of truth for promoted records
DocsStore                     document projection
Keyword/Search Index          retrieval projection
Vector Index                  similarity projection
Reports / Matrices / Graphs   derived projections
```

Search and vector indexes must be rebuildable from governed records and approved
representations.

## 9.2 Blob adapters

The contract is `EvidenceBlobStorePort`.

Reference deployment adapters:

```text
LocalEncryptedBlobStore
    local development, test, single-node and approved on-premise deployments

S3CompatibleBlobStore
    distributed or ephemeral-filesystem deployments
```

No database vendor is part of the evidence contract.

## 9.3 Tenant-scoped deduplication

Default:

```text
deduplication scope = tenant
```

Cross-tenant deduplication requires a separate security decision and must not expose a
blob-existence oracle.

## 9.4 Retention

Retention and legal hold are observation/reference concerns. A shared blob can be
removed only when:

```text
no active observation requires it
and
no legal hold applies
and
all applicable retention periods have elapsed
```

Deletion produces governed lifecycle records or tombstones. “Content-addressed” does
not mean “retained forever.”

---

# 10. Security and threat model

All acquired content is:

```text
UNTRUSTED SOURCE CONTENT
```

## 10.1 URL and SSRF controls

Mandatory properties for URL acquisition:

```text
only explicitly allowed http/https schemes
no embedded credentials
A and AAAA resolution before connection
block private, loopback, link-local, reserved and metadata IP ranges
validate every candidate address
connect only to an approved address
preserve hostname for TLS SNI and certificate verification
verify the connected peer address
repeat validation on every redirect
hard redirect limit
proxies disabled unless explicitly approved
no cookies or ambient credentials by default
```

DNS rebinding defenses are an adapter conformance requirement. The architecture does
not mandate an unsafe “replace hostname with IP” shortcut.

## 10.2 Resource exhaustion

Settings define and receipts record:

```text
raw size limit
timeout
redirect limit
decompression ratio limit
maximum extracted size
maximum pages/entries
maximum chunk count
```

Reference defaults such as 15 MB or a 10:1 decompression ratio are deployment
settings, not universal contracts.

## 10.3 MIME and parser isolation

```text
declared MIME is untrusted
magic-byte/content sniffing is required
filenames are labels, never storage paths
macros and embedded scripts are never executed
extractors run with resource limits
archive traversal is rejected
parser warnings are preserved
```

## 10.4 Prompt injection

Source content cannot:

- change system or agent policy;
- invoke tools;
- obtain credentials;
- authorize acquisition or promotion;
- convert staging data into canonical knowledge.

XML-like delimiters may improve readability but are not a security boundary. Content
must be passed as typed, escaped data under a tool policy independent from source text.
Prompt-injection indicators may be recorded as findings.

## 10.5 Security audit behavior

```text
pre-fetch denial
→ SecurityAuditRecord
→ no RawEvidenceBlob

post-receipt rejection
→ SecurityAuditRecord
→ temporary quarantine according to a short-retention policy
```

Audit metadata must redact secrets and sensitive URL parameters.

---

# 11. Ports and reference adapters

Libraries and vendors are replaceable reference adapters.

```text
AcquisitionPolicyPort
UploadInputPort
HttpFetchPort
EvidenceBlobStorePort
EvidenceMetadataStorePort
ExtractorPort
StructuralChunkerPort
StagingIndexPort
CanonicalRecordStorePort
SearchProjectionPort
VectorIndexPort
ReviewDecisionStorePort
```

Reference adapter candidates:

```text
WebExtractorPort          → TrafilaturaWebExtractor
PdfExtractorPort          → PyMuPdfExtractor / PdfPlumberAdapter
DocxExtractorPort         → PythonDocxExtractor
EvidenceBlobStorePort     → LocalEncryptedBlobStore / S3CompatibleBlobStore
EvidenceMetadataStorePort → PostgresMetadataAdapter
VectorIndexPort           → PgVectorAdapter / InMemoryVectorAdapter
```

Candidates become approved adapters only after fixture benchmarks, security tests and
failure-mode evaluation. “State of the art” is not an acceptance criterion.

`httpx` is an HTTP provider implementation detail. MCP is a connector protocol, not a
trust boundary.

---

# 12. Retrieval separation

## 12.1 Canonical retrieval

Default Roy answers consult only records and representations eligible under the
canonical retrieval policy.

Eligibility is not inferred from one status string. It is derived from:

```text
review decision
record lifecycle
access policy
tenant
sensitivity
validity time
contested/superseded state
```

## 12.2 Staging preview

Staging is available only through explicit, authorized preview/research mode.

Responses must declare:

```text
sourceTier = staging
reviewStatus
observationRef
ingestionTimestamp
extractorId/version
```

Staging mode cannot silently affect default Assistant answers.

## 12.3 Index authority

Indexes do not promote records. Promotion occurs in the canonical record/review layer,
then triggers projection rebuild or incremental update.

---

# 13. Determinism and conformance properties

For the same inputs and pinned versions:

```text
same raw bytes
+ same extractor version/configuration
→ same extracted content hash

same extracted representation
+ same chunker version/configuration
→ same ordered chunk hashes and locators
```

Conformance must verify:

```text
raw-byte roundtrip equality
64-hex SHA-256 validation
observation preservation during deduplication
append-only review history
no model call before interpretation
no Foundation import
no automatic canonical promotion
staging/canonical retrieval separation
precise locator survival
index rebuildability
policy and tenant isolation
```

---

# 14. Incremental roadmap

## M0 — Storage and acquisition reality audit

Read-only inventory of current Brain:

```text
DocsStore
Settings
routes
providers
storage adapters
Neon usage
tenant handling
test fixtures
data directories
```

No code changes.

## M1 — Raw Evidence Capture

Mandatory initial media types:

```text
text/plain
text/markdown
```

Implement:

```text
AcquisitionRequest
minimal policy/classification gate
SHA-256 over raw bytes
tenant-scoped content-addressed blob
SourceObservation
AcquisitionReceipt
exact-byte retrieval
```

Explicitly excluded:

```text
web fetch
PDF
LLM
chunking
DocsStore write
canonical promotion
```

## M2 — Deterministic text extraction

```text
RawEvidenceBlob
→ ExtractionJob
→ ExtractedRepresentation
```

Includes content reference, extractor version, normalized hash and warnings.

## M3 — Structural chunking and locators

```text
Markdown headings
plain-text paragraph boundaries
stable source locators
chunk hashes
```

No mandatory embeddings.

## M4 — Staging and review

```text
staging index
preview-only retrieval
DocumentReviewDecision
PromotionDecision
```

## M5 — Canonical projections

```text
Canonical Record Store
→ DocsStore
→ keyword/search index
→ optional vector index
```

## M6 — Assistant and Magnifier integration

```text
source tier
review status
precise citation
extractor version
coverage
canonical-only default answers
```

## M7 — Safe single-URL acquisition

Requires the complete HTTP threat-model conformance suite:

```text
SSRF
IPv4/IPv6
redirect validation
DNS rebinding
TLS peer verification
size/decompression limits
MIME controls
```

## M8 — Text-based PDF

Requires:

```text
page locators
extraction warnings
encrypted/scanned PDF refusal
resource limits
```

OCR remains post-1.0 unless explicitly promoted.

## M9 — CLI and UI adapters

```text
opnx ingest
UI upload
status and receipt display
```

CLI and UI consume the same Acquisition API and contracts.

---

# 15. Open Nexus 1.0 scope

## Mandatory release gate

```text
M0 through M6
```

This demonstrates:

```text
explicit upload
→ raw evidence
→ deterministic extraction
→ structural chunks
→ staging review
→ canonical promotion
→ Assistant/Magnifier citation
```

## Conditional 1.0 gate

```text
M7 safe URL
M8 text-based PDF
M9 complete CLI/UI adapters
```

Conditional milestones enter 1.0 only if security, conformance and integration gates
are green. Otherwise they move to 1.0.x without invalidating the architecture.

## Post-1.0 extended scope

```text
sitemap and recursive batch acquisition
OCR for scanned documents
complex DOCX/XLSX processing
Notion / Google Drive / Microsoft 365 connectors
generic network MCP connectors
automatic unsupervised domain-model generation
cross-tenant blob deduplication
```

---

# 16. M1 acceptance criteria

```text
□ acquisition starts only from an explicit request
□ only text/plain and text/markdown are accepted
□ bytes are hashed before extraction or normalization
□ SHA-256 contains exactly 64 lowercase hexadecimal characters
□ filenames never become storage paths
□ same bytes in one tenant reuse one blob
□ two requests for the same bytes create two SourceObservations
□ exact bytes can be retrieved and verified
□ size and media policy failures create structured findings
□ pre-storage failure leaves no valid SourceObservation
□ no LLM/provider call occurs
□ no extraction or chunking occurs
□ no DocsStore/canonical write occurs
□ storage adapters remain replaceable
□ Foundation imports = 0
□ command ledger and tests are preserved
```

---

# 17. Remaining owner decisions

These decisions do not block M0 or the contract-only part of M1.

## 17.1 Deployment storage profile

Choose the reference adapter per environment:

```text
local encrypted filesystem
or
S3-compatible object storage
```

The architecture supports both.

## 17.2 Numeric security defaults

Approve environment defaults for:

```text
raw size
extracted size
timeout
redirects
decompression ratio
chunk count
```

They remain Settings, not schema constants.

## 17.3 Canonical record backend

Select the first `CanonicalRecordStorePort` adapter before M5. Search and vector stores
must not be selected as canonical by convenience.

## 17.4 Review experience

Define whether M4 review is initially exposed through:

```text
API-only owner workflow
CLI
Admin UI
```

The decision does not change the review contracts.

---

# 18. Final principles

```text
Raw evidence proves what was acquired, not that its claims are true.
Source observations preserve acquisition context.
Extraction produces derivatives, never replacements.
Chunks serve retrieval; they are not canonical knowledge.
Brain interprets and proposes.
Human review promotes, rejects or contests.
Canonical records are source of truth.
DocsStore, search and vector stores are projections.
Foundation renders materialized experiences.
```

> The objective is not to make external content immediately answerable. The objective
> is to establish a chain of custody through which content can become interrogable,
> reviewable and eventually canonical without losing source, integrity, responsibility
> or uncertainty.
