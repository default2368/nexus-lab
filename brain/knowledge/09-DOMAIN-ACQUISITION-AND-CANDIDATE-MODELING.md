# 09 — Domain Acquisition and Candidate Modeling

**Status:** APPROVED DEVELOPMENT DIRECTION — NOT YET AN IMPLEMENTATION COMMITMENT  
**Approved conceptually:** 2026-09-29  
**Scope:** Brain · Authoring Core · Semantic Entity · Domain Packs · ApplicationBundle

---

## 1. Purpose

Preserve the future development direction through which Open Nexus may transform a
documented professional activity into a candidate domain model that can be reviewed,
corrected and eventually materialized as an application.

The input may be:

- an activity presentation written by a domain expert;
- procedures and operating instructions;
- questionnaires and forms;
- synthetic examples;
- terminology and responsibility matrices;
- sample outputs and decision records;
- interviews or structured answers.

The first target experts are represented by the current research cases:

```text
A.  professional/legal knowledge context
G.  audit/GMP/project-control context
```

No source is considered sufficient merely because it is detailed or authoritative in
tone.

---

## 2. Central statement

> The Brain does not create the domain. The domain already exists in the expert's
> practice. The Brain produces a source-grounded Candidate Domain Definition.

```text
Expert knowledge
+
Documented sources
+
Observed workflow
        ↓
Brain interpretation
        ↓
Candidate Domain Definition
        ↓
Expert correction
        ↓
Validated AuthoringSpec / Domain Pack
        ↓
ApplicationBundle
```

---

## 3. Ecosystem boundary

```text
Brain
    interprets sources, evaluates coverage and proposes candidates

Authoring Core
    validates schemas and builds deterministic results

Domain Pack
    owns domain meaning, vocabulary, rules and profiles

ApplicationBundle
    owns application composition and experience intent

Foundation
    provides the reference implementation and conformance boundary

Execution
    renders materialized PageData

Human owner / domain expert
    corrects meaning and authorizes promotion
```

Invariant:

> Brain interprets and proposes. Authoring validates and constructs. Foundation
> produces. Execution executes. Human authority promotes.

---

## 4. Acquisition pipeline

```text
Source documents
↓
Safe acquisition and normalization
↓
Source Records
↓
Observed Claims and workflow fragments
↓
Domain interpretation
↓
Sufficiency evaluation
↓
Candidate Domain Definition
↓
Expert review and correction
↓
Deterministic validation
↓
Synthetic pilot
↓
Domain Pack / ApplicationBundle candidate
```

Generative AI enters only during interpretation. Acquisition, schema validation,
identity, promotion and materialization remain deterministic or human-authorized.

---

## 5. Required epistemic states

Every extracted or proposed element must be classified as one of:

```text
OBSERVED
INFERRED
PROPOSED
UNKNOWN
CONFLICTING
```

Definitions:

### OBSERVED

Directly supported by an identified source passage, record or expert statement.

### INFERRED

A plausible interpretation supported indirectly by evidence. It is not canonical
until validated.

### PROPOSED

A modeling or product decision suggested by the Brain or an architect.

### UNKNOWN

Required information is absent or insufficient.

### CONFLICTING

Two or more sources or statements provide incompatible descriptions.

No `INFERRED` or `PROPOSED` item may silently become canonical.

---

## 6. Sufficiency levels

The Brain must not reduce sufficiency to a generic yes/no answer.

### INSUFFICIENT

The available material contains isolated terms or aspirations but does not support a
modelable workflow.

### SUFFICIENT_FOR_GLOSSARY

The Brain can produce a sourced vocabulary and initial concept inventory.

### SUFFICIENT_FOR_CANDIDATE_MODEL

The Brain can propose entities, relationships, actors, lifecycle and commands while
making assumptions and gaps explicit.

### SUFFICIENT_FOR_SYNTHETIC_PILOT

The available evidence supports synthetic fixtures, candidate projections and an
experience that a domain expert can correct.

### SUFFICIENT_FOR_IMPLEMENTATION_REVIEW

The candidate model has been reviewed by the expert and can be submitted to the
Authoring Core and architecture gates.

### Not inferable from a single source

```text
SUFFICIENT_FOR_PRODUCTION
```

Production readiness requires security, legal, operational, storage, lifecycle and
real-user evidence outside the competence of a document interpretation pass.

---

## 7. Sufficiency dimensions

At minimum, the Brain evaluates whether evidence exists for:

| Dimension | Question |
|---|---|
| Purpose | What result does the activity produce? |
| Actors | Who participates and with what responsibility? |
| Objects | What is created, received, modified or preserved? |
| Workflow | What starts the activity and what closes it? |
| States | Which lifecycle states do the main objects traverse? |
| Decisions | Who decides, when and on the basis of what evidence? |
| Evidence | Which documents or facts support actions and decisions? |
| Relationships | What is related to what, and why? |
| Operations | What may be created, changed, linked, archived or approved? |
| Access | Who may see or modify each class of information? |
| Exceptions | What happens when the normal path fails? |
| Examples | Is at least one complete synthetic or sanitized case available? |
| Provenance | Can each material statement be traced to a source? |
| Sensitivity | Does the source contain personal, confidential or regulated data? |

The absence of a dimension does not authorize the Brain to fill it from generic
knowledge.

---

## 8. Candidate Domain Definition

A future `CandidateDomainSpec` may contain:

```text
identity
source references
glossary
actors and roles
candidate entities
candidate relationships
candidate value objects
candidate lifecycle
candidate commands
candidate decisions
candidate evidence requirements
candidate access rules
candidate code policies
candidate profiles and experiences
assumptions
conflicts
gaps
confidence and coverage
```

Illustrative structure:

```yaml
status: SUFFICIENT_FOR_CANDIDATE_MODEL

domain:
  id: g-audit
  title: Audit Engagement Control

actors:
  - auditor
  - client-representative
  - approver

candidateEntities:
  - Engagement
  - ProcedureVersion
  - Evidence
  - Feedback
  - Action
  - Decision

candidateRelationships:
  - source: Engagement
    relation: hasEvidence
    target: Evidence
    epistemicStatus: OBSERVED

  - source: Evidence
    relation: supports
    target: Decision
    epistemicStatus: INFERRED

candidateCommands:
  - CreateEngagement
  - SubmitEvidence
  - ClassifyFeedback
  - CloseAction
  - ApproveDecision

assumptions:
  - statement: An approved Decision requires supporting Evidence.
    epistemicStatus: INFERRED
    confidence: medium

gaps:
  - Who may reopen a closed Action?
  - May an Evidence support more than one Engagement?

sources:
  - sourceId: G-activity-presentation
    sections:
      - workflow
      - responsibilities
```

This structure is illustrative. It is not yet a stable contract.

---

## 9. Response when evidence is insufficient

The Brain must not return only:

> I do not have enough information.

It must return:

```text
What is supported
What is inferred
What cannot yet be modeled
Why it cannot be modeled
Which source or answer would unlock the next sufficiency level
```

Example:

```text
Supported:
- client;
- engagement;
- documents;
- activities.

Not yet modelable:
- engagement lifecycle;
- approval authority;
- closure conditions;
- document access rules.

Highest-value missing evidence:
1. one complete sanitized engagement;
2. the states it traversed;
3. who approved and closed it.
```

---

## 10. “Show, do not interrogate”

When sufficient evidence exists, the Brain presents a candidate model rather than a
large generic questionnaire.

```text
Here is the model I understood.
Here are the source passages supporting it.
Here are the assumptions I may have misunderstood.
Correct these points.
```

When evidence is insufficient, the Brain asks only questions with high information
value.

Bad:

> Describe your entire job.

Better:

> The opening and closure of the engagement are documented, but the approval
> authority is not. Who may approve a Decision?

---

## 11. Expert review

The expert is not required to become a software analyst.

The review interface must allow corrections such as:

```text
This object does not exist.
This is not Feedback; it is a Finding.
Evidence may belong to multiple Engagements.
This Decision belongs to the approver, not the client.
The verification step is missing.
This field is confidential.
This relation is only an inference.
```

Corrections become sourced evidence and new candidate revisions. They do not rewrite
history silently.

---

## 12. Deterministic validation

After interpretation, a deterministic gate validates at least:

```text
schema
identity
namespace
references
relationship endpoints
lifecycle consistency
command targets
required fields
version compatibility
code collisions
access declarations
source references
```

```text
CandidateDomainSpec
↓
ValidationFinding[]
↓
expert/owner decision
↓
validated AuthoringSpec
```

The Brain never writes directly to canonical Domain Pack files or Runtime contracts.

---

## 13. Privacy and source safety

Before acquisition, sources must be classified.

Initial pilots use only:

```text
synthetic data
sanitized examples
anonymized or tokenized documents
explicitly authorized sources
```

Prohibited by default:

```text
real client documents
legal privileged material
GMP confidential records
credentials or secrets
personal data without an approved handling policy
```

Source usefulness does not override data governance.

---

## 14. Relationship with Semantic Entity Projection

The Semantic Entity layer projects validated records. It does not decide which domain
concepts are true.

```text
Candidate Domain Definition
↓ expert validation
Domain Pack
↓
EntityRecord / RelationshipRecord
↓
Entity Projector
↓
EntityViewArtifact
↓
PageData
```

Candidate and inferred relationships remain outside canonical projection until
promoted.

---

## 15. Relationship with the first vertical application

For G.:

```text
activity sources
→ Candidate G Domain Definition
→ synthetic Engagement model
→ Control / Client profiles
→ G ApplicationBundle
→ pilot correction
```

For A.:

```text
activity sources
→ Candidate legal/professional Domain Definition
→ Contact/Person/Matter hypotheses
→ expert correction
→ synthetic pilot decision
```

Shared concepts are extracted only after evidence from at least two domains. Similar
words do not automatically imply one universal contract.

---

## 16. Future development streams

### DA-01 — Source intake and classification

Safe acquisition, normalization, source identity and sensitivity classification.

### DA-02 — Domain Sufficiency Evaluator

Structured coverage evaluation producing one of the sufficiency levels in this
document.

### DA-03 — CandidateDomainSpec

Versioned candidate schema with evidence, assumptions, conflicts and gaps.

### DA-04 — Domain Modeling Helper

Brain profile that interprets sources and prepares candidate domain models without
writing canonical state.

### DA-05 — Expert Correction Experience

Human review interface for correcting terms, relations, lifecycle and authority.

### DA-06 — Authoring Core Adapter

Deterministic conversion from a validated candidate to AuthoringSpec inputs.

### DA-07 — Synthetic Pilot Generator

Generation of synthetic fixtures and candidate experiences for falsification by the
expert.

### DA-08 — First external domain comparison

Compare G. and A. concepts to determine which contracts are genuinely reusable.

These streams are directions, not active commitments. They require prioritization and
separate Definition of Done before entering an operational backlog.

---

## 17. Candidate future governance artifacts

The evidence may justify, later:

```text
Epic — Domain Acquisition and Candidate Modeling
ADR  — Semantic Entity Authoring and Persistence Boundary
ADR  — Root Selection and Materialization Authority
PRD  — Domain Modeling Helper
```

No ADR number is assigned here. No future artifact is approved merely by being named.

---

## 18. Non-goals of this direction

```text
automatic production application generation
self-training from model answers
automatic canonical promotion
generic CRUD as domain modeling
replacement of the domain expert
legal/GMP compliance certification
real-data pilots without approved governance
universal Contact or Engagement semantics inferred from one domain
```

---

## 19. Promotion gate

This direction may enter an implementation PRD only when:

```text
□ one approved source bundle is available;
□ source privacy classification is complete;
□ expected output is defined;
□ sufficiency criteria are testable;
□ candidate/canonical boundaries are represented in contracts;
□ expert correction is part of the workflow;
□ no direct Brain-to-canonical write exists;
□ a synthetic falsification case is prepared;
□ ownership across Brain, Authoring, Domain Pack and Application is explicit.
```

---

## 20. Final principle

```text
The expert provides practice and evidence.
The Brain interprets and exposes uncertainty.
The human corrects meaning.
The Authoring Core validates and constructs.
The Domain Pack owns the domain.
The ApplicationBundle organizes experience.
Foundation produces.
Execution executes.
```

> The objective is not to generate a plausible application from a document. The
> objective is to make documented professional knowledge modelable, falsifiable and
> governable without losing source, responsibility or uncertainty.
