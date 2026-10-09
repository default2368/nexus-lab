# 08 — RULESETS AND AGENT PROFILES

**Scopo:** trasformare errori, invarianti e metodi osservati durante lo sviluppo in
regole versionate consumabili dal Brain, senza attribuirne l’ownership all’LLM.

**Dipende da:**

```text
05-EVALUATION.md
06-STORAGE-AND-VALIDATION.md
07-ACQUISITION-AND-MCP.md
```

---

## 0. Principio

> **Le regole non appartengono all’LLM. L’LLM le consuma, propone nuove candidate e
> produce output che gate deterministici e persone autorizzate verificano.**

Open Nexus può apprendere dai propri errori, ma non può trasformare autonomamente
una propria interpretazione in regola canonica.

---

## 1. Come nasce una regola

```text
Finding / errore / falsificazione
        ↓
Candidate Rule
        ↓
secondo caso indipendente
        ↓
test di conformità + test di violazione
        ↓
Authority / human review
        ↓
Accepted Rule
        ↓
ruleset versionato
        ↓
regression test
```

Una regola generale deve:

```text
· essere osservata in almeno due casi indipendenti
· non dipendere da un singolo file o prodotto
· descrivere cosa accade quando viene violata
· avere un gate deterministico o approvatore umano esplicito
· essere testabile
· avere ID, versione, authority e stato
```

---

## 2. Tre famiglie di regole

### 2.1 General Rules

```text
GEN-001  Exact before fuzzy
         titolo, ID, glossary term e alias esatti vengono risolti prima
         del retrieval semantico

GEN-002  Derived fields are derived
         timestamp, hash, URL normalizzato e tool version non vengono
         chiesti al modello o all’utente

GEN-003  No silent fallback
         provider, modello, schema o capability incompatibili producono
         errore/degradazione esplicita

GEN-004  One authority per responsibility
         una responsabilità → un owner → una source of truth

GEN-005  Projections are disposable
         DB, grafo, matrice, report ed embedding sono rigenerabili

GEN-006  Unknown is valid
         evidenza insufficiente → UNKNOWN/DEFER, mai risposta obbligatoria
```

### 2.2 Epistemic Rules

```text
EPI-001  Observation requires evidence
EPI-002  Inference must be labelled
EPI-003  Reported is not verified
EPI-004  Local absence is not global absence
EPI-005  Evaluation requires prior criteria
EPI-006  Ratio requires terms or `not_derivable`
EPI-007  Independent corroboration only
EPI-008  Contradictions remain visible
EPI-009  Falsified claims are preserved
EPI-010  Model confidence is not statistical probability
```

### 2.3 Control Rules

```text
CTRL-001  Gate blocks, Brain signals, human decides
CTRL-002  Policy before retrieval
CTRL-003  Read-only profiles have no mutation tools
CTRL-004  answer_sources ⊆ context_sources
CTRL-005  Compatibility before execution
CTRL-006  Sensitive output requires approval
```

---

## 3. Workflow Roy Explain

```text
Request
  ↓
Identity / authorization / read-only profile
  ↓
Query normalization
  ↓
Exact glossary/document/alias resolution
  ↓
Policy-filtered retrieval
  ↓
Evidence assembly
  ↓
Brain interpretation
  ↓
Answer draft
  ↓
Epistemic validation
  ↓
Source integrity
  ↓
Negative-claim coverage gate
  ↓
Answer artifact
```

Invarianti:

```text
selected_results ⊆ context_sources
answer_sources   ⊆ context_sources
exact_match      ⊆ context_sources
```

Un claim negativo sull’intero corpus richiede `coverage: complete`. Altrimenti la
risposta ammessa è soltanto: “non ho trovato informazioni sufficienti nel contesto
recuperato”.

---

## 4. Workflow Web / Market Scan

```text
URL
  ↓ PublicTargetPolicy
AcquisitionRecord
  ↓
Reduction deterministica
  ↓
Claim candidates
  ↓
Epistemic rules
  ↓
Contradiction / coincidence pass
  ↓
Evaluation
  ↓
Proposal
  ↓
Artifact snapshot
```

Il passaggio contradiction/coincidence confronta:

```text
opportunità proposte vs capability già possedute dall’incumbent
posizionamento del soggetto vs istanze/capability Open Nexus
claim diversi che condividono la stessa origine
```

---

## 5. Workflow Authoring

```text
Intent
  ↓
Brain propone AuthoringSpec
  ↓
Proposal record
  ↓
Compatibility gate
  ↓
Authoring Core
  ↓
Validation
  ↓
Preview
  ↓
Human approval
  ↓
Materialization
```

Il Brain non scrive file e non modifica il Runtime. Propone spec.

---

## 6. Collocazione

```text
brain/
├── rules/
│   ├── general.rules.json
│   ├── epistemic.rules.json
│   ├── control.rules.json
│   └── ruleset.manifest.json
├── agents/
│   └── roy.profile.json
├── contracts/
└── knowledge/
```

```text
JSON/YAML   source machine-readable
Markdown    documentazione generata per umani
```

Mai due source of truth mantenute manualmente.

---

## 7. Contratto minimo di una regola

```json
{
  "id": "EPI-004",
  "title": "Local absence is not global absence",
  "kind": "deterministic",
  "phase": "post-retrieval",
  "appliesTo": ["claim", "answer"],
  "authority": "knowledge-governance",
  "status": "candidate",
  "version": "0.1.0",
  "when": {
    "claimPolarity": "negative"
  },
  "requires": [
    {
      "field": "retrieval.coverage",
      "equals": "complete"
    }
  ],
  "onFailure": {
    "severity": "block",
    "action": "rewrite",
    "template": "Non ho trovato informazioni sufficienti nel contesto recuperato."
  },
  "evidenceRefs": [
    "roy-authentication-false-negative-2026-09"
  ]
}
```

`status` diventa `accepted` soltanto dopo secondo caso, test e review.

---

## 8. Agent Profile — Roy

```json
{
  "agentId": "roy",
  "role": "knowledge-interpreter",
  "mode": "read_only",
  "usesRulesets": [
    "open-nexus-general@0.1.0",
    "open-nexus-epistemic@0.1.0",
    "open-nexus-control@0.1.0"
  ],
  "allowedCapabilities": [
    "knowledge.search",
    "knowledge.retrieve",
    "knowledge.explain",
    "evidence.compare"
  ],
  "allowedTools": [
    "docs_search",
    "glossary_lookup",
    "get_document_section"
  ],
  "deniedTools": [
    "write_file",
    "publish",
    "update_canonical_knowledge",
    "execute_action"
  ],
  "produces": {
    "contract": "answer-artifact.schema.json",
    "defaultStatus": "interpreted"
  },
  "requires": {
    "sourcesForObservedClaims": true,
    "coverageForNegativeClaims": true,
    "humanApprovalForSensitiveOutput": true
  }
}
```

L’identità Roy non possiede la logica. Seleziona capability, tool, ruleset e contratto
di output.

---

## 9. Primo caso di implementazione

```text
EPI-004 — Local absence is not global absence
```

Input reale:

```text
“parlami di authentication”
```

Bug osservato:

```text
Authentication presente in DocsStore e trovata dalla search
→ context errato
→ Roy afferma che la documentazione non copre Authentication
```

Il primo ciclo completo delle regole sarà:

```text
errore
→ observation record
→ candidate rule
→ secondo caso indipendente
→ test di violazione
→ gate
→ regressione impedita
```

---

## 10. Memoria — unico vincolo anticipato

```text
Brain output → Candidate Record
```

Mai:

```text
Brain output → Canonical Knowledge
```

Il modello di memoria futuro dovrà distinguere almeno:

```text
run effimero
candidate record
accepted record
canonical rule
superseded/falsified record
```

La tecnologia di storage non è decisa qui.

---

*Formalizzato il 2026-09-20 da regole e failure mode osservati nello sviluppo di
Open Nexus. Non contiene ancora ruleset implementati.*
