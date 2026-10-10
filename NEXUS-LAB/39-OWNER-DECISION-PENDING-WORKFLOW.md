# 39 — Workflow OWNER_DECISION_PENDING — Separate Documentation Agent

**Data:** 2026-10-09
**Voto complessivo:** 9/10 (Visione 9.5, Separazione 9.5, Context switching 9, Fattibilità 9, Provenance 9, Tempismo 9, Governance 7.5, Rischio duplicazione 7.5)
**DECIDED:** Separate Documentation Agent → APPROVED OPERATING DIRECTION
**Stato:** CANONICAL — OPERATING MODEL

---

## Modello operativo (da Main Agent)

```text
questa conversazione → brainstorming, architettura, owner reasoning
documentation agent → estrae e formalizza
documentation Git repository → conserva versioni e review
owner → ratifica, corregge, rifiuta
technical repositories → possiedono la verità code-coupled
```

> Agent propone. Owner decide. Git conserva.

### Ruoli

```text
Johnn → co-founder / architect / PM → analizza, propone, identifica decisioni, produce handoff
Documentation Agent → redige, normalizza, controlla link/status, commit/push/PR sul repository documentale
Owner → approva o respinge
Git → conserva fonte, revisioni e decisioni
```

Beneficio: evita di interrompere ragionamento per produrre continuamente file. Workflow è già dogfooding del prodotto: conversation → candidate claims → structured decision → owner review → canonical record → Git history (acquisition, provenance, epistemic status, review, promotion, supersession).

---

## Status

Quando emerge decisione importante, Main Agent restituisce:

```text
OWNER_DECISION_PENDING
```

```yaml
decisionId: NX-D-XXX
title: ...
scope: ...
status: OWNER_DECISION_PENDING
observed: [...]
inferred: [...]
proposed: [...]
conflicting: [...]
unknown: [...]
limits: [...]
recommendedDecision: ...
alternatives: [...]
consequences: [...]
implementationImpact: ...
sourceConversationRef: ...
```

Documentation Agent trasforma in artefatto corretto: ADR, PRD, Epic, backlog, finding, decision record, evidence report.

Dopo ratifica owner:

```text
OWNER_DECISION_PENDING → APPROVED → APPROVED_WITH_CONDITIONS → DEFERRED → REJECTED
```

---

## Tre regole per 9.5/10

### 1. Conversazione non è authority canonica

```text
raw conversation → source evidence / brainstorming source
approved ADR/PRD/decision → governing authority
```

Repository conversazione non deve essere usato come corpus canonicale di Roy senza classificazione.

### 2. Ogni documento estratto conserva fonte

```text
conversationId
turn/range
date
source hash
extractor/agent
target document
approval status
```

Così si torna dal documento alla discussione originaria.

### 3. Nessuna promozione automatica

```text
agent-generated document → CANDIDATE
owner-reviewed → APPROVED
merged → VERSIONED
merged ≠ automaticamente canonicale
```

Status deve governare.

---

## Corpus separation

```text
sources/conversations/ → raw or normalized conversation evidence → not default Roy corpus
docs/candidates/ → agent-produced drafts
docs/approved/ → owner-ratified knowledge
archive/ → superseded/rejected/historical
```

O struttura equivalente basata su metadata, senza necessariamente spostare file fisicamente. Implementato come:

```
NEXUS-LAB/
  SORGENTI/ (legacy, da migrare)
  00-INDICE.md ... 39-... (approved/candidate con status in header)
sources/
  conversations/ (nuovo)
docs/
  candidates/ (nuovo)
  approved/ (nuovo)
archive/ (nuovo)
brain/data/records/ (provenance, già esistente)
```

---

## Sicurezza

Conversazioni possono contenere path locali, branch, commit, stakeholder, finding security, valori mascherati, strategia, naming/IP, ipotesi non ratificate.

Quindi:

```text
repository private
secret scan
PII/sensitivity classification
no automatic public publication
no raw conversation in default Brain retrieval
retention policy
```

---

## Decisione finale

```text
Separate Documentation Agent → APPROVED OPERATING DIRECTION
Conversation Git repository → APPROVED AS SOURCE/REVIEW CONTROL PLANE
Automatic authority promotion → PROHIBITED
OWNER_DECISION_PENDING handoff → APPROVED
Writing every document in this chat → no longer required
```

Quindi Main Agent può dire: "Questa decisione è importante. Restituiscimi OWNER_DECISION_PENDING." Si concentra su architettura e prepara handoff rigoroso. Documentation Agent produce documento e commit. Owner rimane unico gate promozione.

---

## Template OWNER_DECISION_PENDING (per Support Agent)

```yaml
decisionId: NX-D-XXX
title: Titolo decisione
scope: modulo/capacità impattata
status: OWNER_DECISION_PENDING
observed:
  - claim con locator file:linea o comando
inferred:
  - interpretazione marcata con base e falsificazione
proposed:
  - proposta concreta
conflicting: []
unknown: []
limits: []
recommendedDecision: APPROVED / DEFERRED / REJECTED con condizioni
alternatives:
  - alt1 con pro/contro
consequences:
  - se approvato, cosa succede
implementationImpact:
  - file toccati, test, branch
sourceConversationRef:
  conversationId: arena/86a8bf50-nexus-lab
  turnRange: ...
  date: 2026-10-09
  sourceHash: ...
  extractor: documentation-agent v0.1.0
  targetDocument: NEXUS-LAB/XX-...md
  approvalStatus: CANDIDATE
```

---

*Workflow approvato 9/10 — evoluzione modo di lavorare, Main Agent sgravato, Documentation Agent codifica, Owner gate unico*
