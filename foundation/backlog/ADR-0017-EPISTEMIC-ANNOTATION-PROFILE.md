# ADR-0017 — Epistemic Annotation Profile for Semantic Entity Projection

**Status:** PROPOSED — owner approval required  
**Date:** 2026-10-07  
**Target:** Open Nexus Foundation 0.9 integration train / 0.9.x additive profile  
**Predecessor:** Foundation 0.8.2 Surface Convergence and Hygiene  
**Depends on:** ADR-0016 Semantic Entity Projection Model  
**Brain dependency:** none in the Foundation core; Brain adapter remains a separate integration  
**Implementation authorization:** NOT GRANTED

---

## 1. Context

ADR-0016 establishes an experimental semantic projection pipeline outside the Runtime:

```text
EntityRecord
+ EntityGraphSlice
+ ProjectionContext
+ EntityViewProfile
        ↓
EntityProjector
        ↓
EntityViewArtifact
        ↓
PageData Adapter
        ↓
PageData
        ↓
Runtime unchanged
```

The semantic core has demonstrated that one entity can be projected into different
role-specific experiences without changing the protected Runtime contracts.

Brain and acquisition work introduce a related but distinct requirement: knowledge
records, individual properties and relationships may have different epistemic states.
For example:

```text
Engagement
├── identity              human validated
├── title                 reported and supported
├── closureDate           observed and supported
├── responsibleActor      inferred and unreviewed
└── hasEvidence relation  conflicting
```

One record-level status is insufficient. Embedding all epistemic fields directly into
the domain payload would contaminate Domain Pack schemas and couple Semantic Entity
Projection to Brain implementation details.

The 0.9 integration train is the natural point at which to define an additive,
provider-independent annotation profile, but only after:

```text
Foundation 0.8.2 closes
→ semantic branch is rebased on the selected Foundation target
→ existing semantic baseline is reproduced
→ ADR-0016 core is integrated without regression
```

---

## 2. Decision

Open Nexus introduces a candidate `EpistemicAnnotationSet` as an optional sidecar to
semantic records and relationships.

```text
EntityRecord
+
EpistemicAnnotationSet (optional)
        ↓
EntityGraphSlice
        ↓
EntityProjector
        ↓
EntityViewArtifact
  ├── entity projection
  └── authorized epistemic projection
```

The sidecar may annotate:

- the complete entity record;
- one field or nested property through JSON Pointer;
- one `RelationshipRecord` through stable relation identity.

The profile separates three axes:

```text
derivation
    how the statement/annotation originated

evidenceStatus
    whether available evidence supports, conflicts with or fails to support it

reviewStatus
    whether a human authority has reviewed the annotation
```

The profile is additive:

```text
EntityRecord without EpistemicAnnotationSet
→ remains valid
→ projects exactly as before
```

`EntityRecord.data` remains owned by the Domain Pack and is not rewritten as a generic
epistemic map.

---

## 3. Central invariants

```text
Domain data remains domain data.
Epistemic metadata remains an optional governed sidecar.
Record, field and relationship annotations remain independently addressable.
Model proposal never implies human validation.
Source support never implies source authority or truth.
Summary status is derived deterministically.
Server and client receive policy-filtered projections of the same annotation set.
Foundation core never imports Brain implementation code.
EvaluationTrace never becomes entity state.
PageData remains unchanged unless a separate RFC authorizes an extension.
```

---

## 4. Boundary

```text
Open Nexus Contracts
    EpistemicAnnotation
    EpistemicAnnotationSet
    EpistemicSubject
    EpistemicSummary

Domain Pack
    EntityRecord data/schema meaning

Semantic Provider
    records + relationships + optional annotation sets

Policy/Projection Context
    visibility of fields, relations and epistemic metadata

EntityProjector
    deterministic entity + annotation projection

EntityViewArtifact
    role-appropriate entity view and epistemic projection

PageData Adapter
    maps only approved artifact fields through an existing compatible extension point

Brain Adapter (separate)
    may propose candidate annotations from ClaimEnvelope claims

Human Review
    promotes, rejects, contests or requests revision
```

---

## 5. Relationship to existing provenance

ADR-0016 candidate contracts already include:

```ts
EntityRecord.sourceRefs
RelationshipRecord.sourceRefs
```

Those fields preserve minimal provenance for the source record or relationship. The
new profile does not replace them.

```text
EntityRecord.sourceRefs
→ sources associated with the record as a whole

EpistemicAnnotation.sourceRefs
→ sources supporting or conflicting with a specific entity, field or relationship
```

References point to an approved `SourceReference` registry/contract. Full excerpts,
provider payloads and operational traces are not duplicated into every entity.

---

## 6. Candidate contracts

The following shapes are illustrative and require normative schema/tests before
implementation.

### 6.1 Epistemic derivation

```ts
type EpistemicDerivation =
  | "OBSERVED"
  | "REPORTED"
  | "INFERRED"
  | "PROPOSED";
```

Definitions:

```text
OBSERVED
    directly established by deterministic observation of an approved source/state

REPORTED
    explicitly asserted by an identified source or actor

INFERRED
    derived from one or more premises/sources through interpretation

PROPOSED
    candidate modeling or domain assertion awaiting validation
```

### 6.2 Evidence status

```ts
type EvidenceStatus =
  | "SUPPORTED"
  | "CONFLICTING"
  | "UNSUPPORTED"
  | "UNKNOWN";
```

`SUPPORTED` means that referenced evidence supports the bounded statement. It does not
mean the source is universally authoritative or that the real-world statement is
independently true.

### 6.3 Review status

```ts
type EpistemicReviewStatus =
  | "UNREVIEWED"
  | "HUMAN_VALIDATED"
  | "REJECTED"
  | "REQUIRES_REVISION";
```

### 6.4 Annotation subject

```ts
type EpistemicSubject =
  | {
      kind: "ENTITY";
      entityRef: EntityReference;
    }
  | {
      kind: "FIELD";
      entityRef: EntityReference;
      path: string; // RFC 6901 JSON Pointer into EntityRecord.data
    }
  | {
      kind: "RELATIONSHIP";
      relationshipId: string;
    };
```

### 6.5 Epistemic annotation

```ts
interface EpistemicAnnotation {
  annotationId: string;
  subject: EpistemicSubject;

  derivation: EpistemicDerivation;
  evidenceStatus: EvidenceStatus;

  sourceRefs: string[];
  claimRefs: string[];
  premiseAnnotationRefs: string[];

  asOf?: string;
  validFrom?: string;
  validUntil?: string;

  review: {
    status: EpistemicReviewStatus;
    decisionRef?: string;
    reviewedAt?: string;
  };

  provenance: {
    producedBy: "SYSTEM" | "MODEL" | "HUMAN";
    producedAt: string;
    capabilityVersion?: string;
    traceRef?: string;
  };
}
```

A `traceRef` may link to an authorized operational trace. The complete trace is not
embedded in the annotation.

### 6.6 Annotation set

```ts
interface EpistemicAnnotationSet {
  schemaVersion: "epistemic-annotation/0.1";
  annotationSetId: string;

  entityRef: EntityReference;
  entityRecordVersion?: string;

  annotations: EpistemicAnnotation[];
  summary: EpistemicSummary;

  recordedAt: string;
  supersedes?: string;
}
```

### 6.7 Summary

```ts
interface EpistemicSummary {
  supportedCount: number;
  inferredCount: number;
  conflictingCount: number;
  unsupportedCount: number;
  unknownCount: number;
  unreviewedCount: number;

  overall:
    | "SUPPORTED"
    | "PARTIAL"
    | "CONFLICTING"
    | "INSUFFICIENT";

  derivationProfile: string;
}
```

The summary is produced by a versioned deterministic aggregation profile. It is never
freely authored by a model.

---

## 7. Property-level annotation

Field annotations use RFC 6901 JSON Pointer against `EntityRecord.data`.

```json
{
  "annotationId": "ann-eng-001-owner",
  "subject": {
    "kind": "FIELD",
    "entityRef": {
      "id": "ENG-001",
      "type": "Engagement",
      "namespace": "g-audit",
      "schemaVersion": "1.0"
    },
    "path": "/responsibleActor"
  },
  "derivation": "INFERRED",
  "evidenceStatus": "SUPPORTED",
  "sourceRefs": ["src-procedure-02-step-06"],
  "claimRefs": ["claim-07"],
  "premiseAnnotationRefs": [],
  "review": {
    "status": "UNREVIEWED"
  },
  "provenance": {
    "producedBy": "MODEL",
    "producedAt": "2026-10-07T10:00:00Z",
    "capabilityVersion": "domain-interpretation/0.1"
  }
}
```

Validation rules include:

```text
FIELD path is a valid JSON Pointer
entityRef exists in the graph slice/provider authority
path resolves against the referenced record version, unless annotation is historical
field visibility cannot exceed ProjectionGrant.visibleFields
annotation visibility cannot reveal a hidden field
```

---

## 8. Relationship-level annotation

```json
{
  "annotationId": "ann-rel-evidence-decision-01",
  "subject": {
    "kind": "RELATIONSHIP",
    "relationshipId": "rel-engagement-evidence-decision-01"
  },
  "derivation": "REPORTED",
  "evidenceStatus": "SUPPORTED",
  "sourceRefs": ["src-procedure-02-step-09"],
  "claimRefs": ["claim-14"],
  "premiseAnnotationRefs": [],
  "review": {
    "status": "HUMAN_VALIDATED",
    "decisionRef": "review-decision-22",
    "reviewedAt": "2026-10-07T10:30:00Z"
  },
  "provenance": {
    "producedBy": "HUMAN",
    "producedAt": "2026-10-07T10:30:00Z"
  }
}
```

Validation rules include:

```text
relationshipId exists
relationship endpoints exist
annotation entity context is compatible with relationship endpoints
hidden relationships do not leak through annotation summaries
```

---

## 9. Deterministic summary rules

The exact aggregation profile is versioned. Candidate baseline:

```text
any visible CONFLICTING
→ overall CONFLICTING

else any visible UNSUPPORTED and no sufficient supported core
→ overall INSUFFICIENT

else mixture of SUPPORTED with UNKNOWN/UNREVIEWED/INFERRED
→ overall PARTIAL

else all visible required annotations SUPPORTED
→ overall SUPPORTED
```

The profile must declare which annotations are required for a given entity/view. A
simple worst-status aggregation over every optional field is not sufficient.

```text
summary
→ derived after policy filtering
```

A server-wide summary must not be copied to the client if it would reveal hidden
annotations.

---

## 10. Server and client projections

### 10.1 Server representation

Authorized server workflows may access:

- complete annotation subjects;
- source and claim references;
- review decision references;
- provenance producer/capability;
- validity and succession;
- conflicts and premises.

### 10.2 Client representation

Default client projection is bounded:

```ts
interface ClientEpistemicProjection {
  schemaVersion: "epistemic-view/0.1";
  entityRef: EntityReference;
  overall: "SUPPORTED" | "PARTIAL" | "CONFLICTING" | "INSUFFICIENT";
  hasEvidence: boolean;
  hasConflicts: boolean;
  reviewStatus: EpistemicReviewStatus | "MIXED";
  visibleAnnotations?: Array<{
    subjectKind: "ENTITY" | "FIELD" | "RELATIONSHIP";
    pathOrRelationRef?: string;
    derivation: EpistemicDerivation;
    evidenceStatus: EvidenceStatus;
    claimRefs?: string[];
  }>;
}
```

Source locators, excerpts and internal paths are included only when policy grants them.
Provider/model telemetry is excluded.

### 10.3 Role-specific projection

The same entity may produce:

```text
Control View
→ field/relation annotations + review/conflict detail

Client View
→ bounded status and approved evidence indicators

Evidence Detail
→ authorized source/claim references and locators
```

The projector applies:

```text
profile request
∩ ProjectionGrant
∩ entity/field/relation visibility
∩ epistemic redaction policy
```

---

## 11. Relationship to ClaimEnvelope

`ClaimEnvelope` and `EpistemicAnnotationSet` solve different lifecycle problems.

```text
ClaimEnvelope
    query/answer-scoped
    may be ephemeral
    explains what supported one Assistant response

EpistemicAnnotationSet
    entity/version-scoped
    revisioned
    explains the governed status of entity data and relationships
```

Candidate promotion flow:

```text
ClaimEnvelope.claim
+ source references
+ candidate entity/field/relation target
        ↓
Candidate EpistemicAnnotation
        ↓
deterministic validation
        ↓
human review decision
        ↓
EpistemicAnnotationSet revision
```

The Brain may propose candidate annotations. It cannot write or promote canonical
annotation sets directly.

A ClaimEnvelope is never embedded wholesale into an entity.

---

## 12. EvaluationTrace boundary

`EvaluationTrace` records how one evaluation run executed:

- retrieval timings;
- provider/model invocation;
- token usage;
- validator timing;
- request identity.

It is operational telemetry, not entity knowledge.

```text
EvaluationTrace
→ separate operational store / authorized trace endpoint

EpistemicAnnotation.provenance.traceRef
→ optional reference only
```

No `EvaluationTrace` payload enters:

- `EntityRecord.data`;
- relationship data;
- client entity projection by default;
- PageData without explicit policy and contract.

---

## 13. PageData and protected-kernel boundary

This ADR does not authorize changes to:

```text
PageData
PageController
normalizeToPageData
ApplicationDefinition
ApplicationContext
BundleCollector
DiscoveryService
DiscoveryServiceV2
Runtime
```

Candidate pipeline:

```text
EntityRecord
+ EpistemicAnnotationSet
→ EntityViewArtifact
→ PageData Adapter
→ existing compatible PageData extension point, if proven
```

If no compatible extension point exists:

```text
STOP
→ Foundation RFC required
```

The adapter must not smuggle unversioned generic metadata into PageData.

---

## 14. Foundation/Brain dependency rule

The annotation contracts must remain implementation-neutral.

Foundation semantic code may depend on:

```text
shared Open Nexus contract definitions
```

It may not depend on:

```text
FastAPI
DocsStore
DeepSeek/provider code
Brain routes
ClaimEnvelope assembler
EvaluationTrace implementation
```

Brain integration remains an adapter outside the semantic projector core.

Candidate contract ownership after a second consumer is demonstrated:

```text
Open Nexus Contracts
→ EpistemicAnnotation v0.1
→ EpistemicAnnotationSet v0.1
→ EpistemicViewProjection v0.1
```

Until that promotion decision, the contracts remain experimental and co-located with
the 0.9 semantic work.

---

## 15. Integration sequence

No implementation begins before Foundation 0.8.2 closes.

### Phase E0 — Rebase and reproduce semantic baseline

```text
select Foundation target
rebase/integrate feature/0.9-semantic-entity-projection
run semantic suite
run protected-kernel diff
run build/integration
```

Required historical baseline:

```text
213 semantic tests
0 new failures
0 protected-kernel changes
```

The exact current baseline must be remeasured after integration.

### Phase E1 — Semantic core integration

Integrate ADR-0016 contracts/provider/projectors without epistemic annotation changes.

```text
EntityRecord
→ EntityViewArtifact
→ PageData
```

### Phase E2 — Annotation contract profile

Add only:

- annotation contracts;
- schema validation;
- fixture annotation sets;
- deterministic summary;
- no Brain adapter.

### Phase E3 — Projector support

```text
EntityRecord + annotation set
→ role-filtered EntityViewArtifact
```

Prove:

- no annotation = old projection;
- Control and Client projections differ without leakage;
- property/relation granularity survives.

### Phase E4 — Shared contract decision

Promote to Open Nexus Contracts only if at least two independent consumers confirm the
minimal common contract.

Candidate consumers:

```text
G. semantic projection
Application/Page Admin semantic projection
Brain candidate-annotation adapter
```

### Phase E5 — Brain adapter

Separate post-core integration:

```text
ClaimEnvelope
→ Candidate EpistemicAnnotation
→ review
→ annotation-set revision
```

No Brain call occurs inside `EntityProjector`.

---

## 16. Security and authorization

Mandatory properties:

```text
annotation visibility cannot reveal a hidden field
relationship annotation cannot reveal a hidden relationship
sourceRefs do not grant source access
claimRefs do not grant ClaimEnvelope access
summary is recomputed after policy filtering
client projection excludes internal trace/provider metadata
review decision identity follows access/audit policy
model-produced annotation remains UNREVIEWED
```

A source reference visible to a client must be resolved through the same authorization
policy as the source/excerpt endpoint.

---

## 17. Validation and conformance

Candidate deterministic rules:

```text
A1  annotationId unique within set/revision
A2  entityRef matches annotation-set root
A3  FIELD path is valid RFC 6901 JSON Pointer
A4  FIELD path resolves for active record version or is explicitly historical
A5  RELATIONSHIP subject exists
A6  sourceRefs and claimRefs use valid reference shapes
A7  INFERRED requires sourceRefs, claimRefs or premiseAnnotationRefs
A8  SUPPORTED requires at least one approved evidence/premise reference
A9  CONFLICTING requires at least two conflicting references or conflict record
A10 HUMAN_VALIDATED requires decisionRef and reviewedAt
A11 MODEL-produced annotation cannot be HUMAN_VALIDATED
A12 validity interval is ordered
A13 supersedes reference is acyclic and points to a prior set/revision
A14 summary equals deterministic recomputation
A15 client projection contains no unauthorized subject/source/claim reference
```

---

## 18. Acceptance criteria

This ADR may move to `ACCEPTED` only when:

```text
□ Foundation 0.8.2 is closed
□ ADR-0016 semantic core baseline is reproduced on the selected Foundation target
□ EntityRecord without annotations projects identically to the existing 0.9 baseline
□ one entity contains record-level, field-level and relationship-level annotations
□ same entity produces Control and Client epistemic projections
□ hidden fields/relations do not leak through annotation or summary
□ deterministic summary and A1–A15 validation pass
□ model proposal remains UNREVIEWED until a human decision
□ ClaimEnvelope is not embedded into EntityRecord
□ EvaluationTrace remains outside entity state
□ PageData/protected-kernel unauthorized diff = 0
□ Foundation semantic core imports no Brain implementation
□ at least two consumers validate the minimal shared contract before promotion
```

---

## 19. Consequences

### Positive

- property- and relation-level epistemic status;
- same entity can support auditor, operator and client views;
- Brain claims can become governed candidate annotations through review;
- Domain Pack data remains free from infrastructure metadata;
- client/server projections share one contract while enforcing different visibility;
- annotation/history can evolve independently from entity payload revisions;
- future Magnifier and dossier experiences gain a stable entity-level substrate.

### Negative

- additional contracts and validation rules;
- sidecar versioning and succession must be governed;
- projection/redaction logic becomes more complex;
- summary can mislead if aggregation profiles are not explicit;
- field paths can break across schema migrations;
- source/claim references introduce lifecycle dependencies;
- shared-contract promotion requires cross-repository governance.

---

## 20. Alternatives considered

### 20.1 Embed epistemic fields inside `EntityRecord.data`

Rejected because it contaminates Domain Pack schemas, duplicates infrastructure fields
and makes domain payloads depend on Brain/governance concerns.

### 20.2 Add one `epistemicStatus` field to EntityRecord

Rejected because different properties and relationships can have different states.

### 20.3 Reuse ClaimEnvelope directly

Rejected because ClaimEnvelope is query/answer-scoped and may be ephemeral, while
entity annotations are versioned and entity-scoped.

### 20.4 Store EvaluationTrace in the entity

Rejected because execution telemetry is not canonical entity knowledge and may expose
provider/internal details.

### 20.5 Put epistemic metadata directly in PageData

Rejected because PageData is a protected Runtime boundary and would become the source
of epistemic meaning instead of a transport projection.

### 20.6 Defer all epistemic representation to UI state

Rejected because server validation, review, policy and reproducible projection require
a shared backend contract.

---

## 21. Non-decisions

This ADR does not select or authorize:

```text
storage backend for annotation sets
graph database
request-time projection
automatic Brain promotion
LLM/provider
Magnifier UI
badge/color/layout conventions
public source endpoint
PageData extension
field-level dynamic authorization engine
real client/GMP/legal data
history rewrite of existing entity fixtures
```

---

## 22. Required follow-up artifacts

If approved after 0.8.2 closure:

```text
PRD amendment or 0.9.x PRD addendum
EPIC 0.9 integration sequence update
normative JSON Schema / TypeScript contracts
annotation conformance fixtures
summary aggregation profile
projection redaction policy
Brain candidate-annotation adapter contract
client epistemic projection contract
command/evidence ledger
```

No follow-up artifact authorizes implementation by implication.

---

## 23. Owner decision

```text
ADR status: PROPOSED

Project Owner:
  [ ] APPROVED DIRECTION
  [ ] APPROVED WITH CONDITIONS
  [ ] DEFERRED
  [ ] REJECTED

Conditions:

Date:
```

---

## 24. Final principle

```text
EntityRecord
    owns domain state

EpistemicAnnotationSet
    owns governed epistemic metadata about record, fields and relationships

EntityProjector
    produces deterministic, policy-filtered views

ClaimEnvelope
    explains one Assistant answer

EvaluationTrace
    records one execution

Human review
    promotes or rejects candidate annotations
```

> Open Nexus should not merely represent entities. It should be able to represent what
> is known, reported, inferred, contested and approved about each entity property and
> relationship without coupling domain state to Brain implementation or changing the
> Runtime contract.
