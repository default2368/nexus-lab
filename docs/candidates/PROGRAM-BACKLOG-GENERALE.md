# Program Backlog Generale — North Star G. Vertical Proof

**Status:** CANDIDATE
**DecisionId:** NX-D-043
**Source:** Main Agent — ecosystem governance parked, Foundation 0.8.2 critical path, Assistant/Brain/CLI lanes
**ConversationRef:**
  conversationId: arena/86a8bf50-nexus-lab
  turnRange: 2026-10-09T20:00-20:15
  date: 2026-10-09
  sourceHash: 1224632 + c036d6e
  extractor: documentation-agent v0.1.0
  targetDocument: docs/candidates/PROGRAM-BACKLOG-GENERALE.md
  approvalStatus: CANDIDATE
**DECIDED:** Ecosystem governance → parked, non blocking; Foundation 0.8.2 → proceeds; Assistant evaluate client → parallel; Brain Markdown acquisition → parallel; CLI → contract/design lane, implementation conditional; Everything → oriented to G. vertical proof

---

## North Star comune

Tutte le corsie devono convergere sul primo vertical proof per G.:

```text
upload di una procedura Markdown sintetica/sanificata
→ preservazione byte/hash/provenance
→ estrazione deterministica di struttura
→ domanda epistemica
→ answer + claim + source + gap
→ visualizzazione nel Roy Client
→ correzione da parte di G.
```

Questo prova il meccanismo senza trasformare Open Nexus in un prodotto esclusivamente audit.

> Infrastructure must be reusable; Domain must be replaceable.

---

## Program Board

| Corsia | Priorità | Obiettivo corrente | Classificazione | WIP |
|---|---:|---|---|---|
| Foundation 0.8.2 | P0 | chiusura security/surface convergence/release | `foundation/backlog/EPIC-0.8.2.md` — critical path, mutazione attiva | 1 |
| Assistant development | P1 | `/evaluate`, metadata diagnostici, upload `.md` | `assistant/backlog/` — parallel development, non PR verso master 0.8.2 | 1 |
| Brain | P1 | ClaimEnvelope conformance + acquisition Markdown | `brain/backlog/` — contract conformance + Markdown acquisition M1 | 1 |
| CLI | P2 | contratti, workspace, receipts; implementation solo se sostenibile | `cli/backlog/BACKLOG.md` — contract/design lane, implementation conditional | 0 (design/docs) |
| Documentation | supporto | handoff, decisioni, procedure, status | `docs/candidates/`, `docs/approved/` — supporto, riceve solo handoff | 0 |
| G. pilot | North Star | riconoscimento/correzione del dossier | `NEXUS-LAB/SORGENTI/G-PROCEDURE-SYNTHETIC-001.md` — vertical slice, convergenza | — |

---

## 1. Foundation 0.8.2 — P0 critical path

**Classificazione:** `foundation/backlog/` — EPIC-0.8.2, PR #14, SURF-082

Resta la sola release critical path.

```text
PR #14 debug gate
→ merge e verifica
poi
→ /api/v1/debug/redis read-only security review
→ SURF-082-004/006/007
→ final compatibility closure
→ v0.8.2
```

Non riceve:

- upload
- Brain contracts
- Magnifier
- CLI workspace
- Semantic 0.9

**WIP:** mutazione attiva — 1 repository, 1 mutazione

**DECIDED:** proceeds, non interrotta

---

## 2. Assistant development — P1 parallel

**Classificazione:** `assistant/backlog/` — branch separato, non PR verso master 0.8.2

Sequenza:

```text
aa17567 Assistant reconciled
→ merge current master sul branch Assistant
→ /evaluate response normalizer
→ conversational/epistemic mode
→ development diagnostic console
→ upload Markdown UI
```

La prima UI upload deve fare soltanto:

```text
seleziona file .md
→ mostra nome/tipo/dimensione
→ invia a Brain Acquisition API
→ riceve receipt
→ mostra stato
```

Non:

- interpreta localmente
- scrive DocsStore
- crea record canonici
- esegue macro/script
- salva provider key
- promuove automaticamente

**WIP:** mutazione attiva — 1 repository, 1 mutazione

**DECIDED:** parallel development

---

## 3. Brain — P1 parallel

**Classificazione:** `brain/backlog/` — due sottolavori coerenti

### 3.1 Contract conformance

```text
ClaimEnvelope
EvaluationTrace
outcome/coverage/gaps
source vs retrieval candidates
telemetry unknown vs zero
```

### 3.2 Markdown acquisition M1

```text
explicit upload
→ size/MIME gate
→ SHA-256 raw bytes
→ RawEvidenceBlob
→ SourceObservation
→ AcquisitionReceipt
```

Prima iterazione:

```text
text/markdown
text/plain
synthetic/sanitized only
```

Esclusi:

- PDF
- DOCX
- web crawling
- OCR
- real client documents
- automatic interpretation/promotion

**WIP:** mutazione attiva — 1 repository, 1 mutazione (con Assistant e Foundation = max 3 corsie tecniche con codice attivo)

**DECIDED:** parallel development

---

## 4. Vertical slice G. — North Star

**Classificazione:** `NEXUS-LAB/SORGENTI/G-PROCEDURE-SYNTHETIC-001.md` + `docs/candidates/GOVERNED-EVIDENCE-DOSSIER.md`

Fixture iniziale candidata:

```text
G-PROCEDURE-SYNTHETIC-001.md
```

Contenuto:

- scopo
- attori
- step
- questionario
- evidenze
- feedback
- azione
- verifica
- approvazione
- chiusura

Test:

```text
upload
→ receipt
parse
→ heading/step locator
evaluate
→ answer + sources + gaps
client
→ Markdown response + diagnostic metadata
expert
→ G. corregge struttura e significato
```

Successo:

> G. riconosce o corregge il processo.

Non:

> G. dice che la UI è bella.

**DECIDED:** North Star, punto di convergenza di tutte le corsie

---

## 5. CLI — P2 contract/design lane

**Classificazione:** `cli/backlog/BACKLOG.md` — CLI-008 audit, CLI-009 authoring, CLI-010 PlaceholderContentProvider, CLI-012 Materializer, CLI-015 legacy, CLI-018 orchestrator, CLI-019 ProjectContext + nuovo ECOSYSTEM-GOVERNANCE-PROPOSAL

Per ora può avanzare come contratto/documentazione:

```text
ProjectContext
WorkspaceManifest
WorkspaceLock
GitSnapshot
VerificationReceipt
HandoffReceipt
```

Implementation soltanto se non sottrae owner bandwidth alle prime tre corsie.

Primo futuro uso concreto:

```text
opnx ingest procedure.md
```

Ma inizialmente Assistant può chiamare direttamente l'Acquisition API. Non aspettiamo la CLI per provare il vertical slice.

**WIP:** design/docs soltanto — 0 mutazioni attive

**DECIDED:** contract/design lane, implementation conditional

---

## 6. Documentation Agent — supporto

**Classificazione:** `docs/candidates/`, `docs/approved/`, `NEXUS-LAB/38-REGOLA-CHAT-MAIN-AGENT.md`, `39-OWNER-DECISION-PENDING-WORKFLOW.md`

Riceve soltanto handoff:

```text
OWNER_DECISION_PENDING
DOCUMENTATION_HANDOFF
```

Mantiene:

- decisioni
- procedure
- status
- pilot evidence
- source refs
- supersession

Non apre nuove architetture da solo.

**WIP:** supporto — 0 mutazioni attive

**DECIDED:** supporto, handoff only

---

## 7. Ecosystem Governance — parked, non blocking

**Classificazione:** `docs/candidates/ECOSYSTEM-GOVERNANCE-PROPOSAL.md` — APPROVED PRODUCT HYPOTHESIS, parked

La governance dell'ecosistema è un filone abilitante, non la critical path. La congeliamo senza farle rallentare il prodotto.

- Separate authority YES, new repository REVIEW_REQUIRED
- VerificationReceipt v0.1 candidate
- .nexus/receipts/ local spool
- DuckDB rebuildable read model
- CLI/Workspace/Verification Agent specializzato — da creare dopo G. pilot proof

**WIP:** 0 — parked

**DECIDED:** parked, non blocking

---

## WIP Limit

Per una persona con più agenti:

```text
massimo 1 mutazione attiva per repository
massimo 3 corsie tecniche con codice attivo
decisioni owner serializzate
```

Quindi:

```text
Foundation  mutazione attiva
Backend     mutazione attiva
Assistant   mutazione attiva
CLI         design/docs soltanto
Docs        supporto
```

Se una corsia arriva a un owner gate, si ferma senza bloccare le altre.

---

## Ordine di valore

```text
1. chiudere 0.8.2
2. far rispondere /evaluate nel Roy Client
3. upload Markdown → receipt
4. query sul documento caricato
5. G. corregge il modello
6. soltanto dopo: CLI ingestion e UI epistemica avanzata
```

---

## DECIDED (Main Agent)

```text
Ecosystem governance
→ parked, non blocking

Foundation 0.8.2
→ proceeds

Assistant evaluate client
→ parallel development

Brain Markdown acquisition
→ parallel development

CLI
→ contract/design lane, implementation conditional

Everything
→ oriented to G. vertical proof
```

Questa è una buona configurazione: diverse corsie, un solo obiettivo. Il rischio non è lavorare in parallelo; è permettere alle corsie di inventarsi obiettivi diversi. Qui il punto di convergenza è chiaro.

---

## Backlog mapping — dove sta cosa

| Item | File attuale | Classificazione proposta | Priorità |
|---|---|---|---|
| Foundation 0.8.2 closure | `foundation/backlog/` PR #14, SURF-082-004/006/007 | P0 critical path | P0 |
| Assistant /evaluate + upload UI | `assistant/backlog/` + `frontend/` | P1 parallel, non PR verso master 0.8.2 | P1 |
| Brain ClaimEnvelope + Acquisition M1 | `brain/backlog/` + `brain/data/records/` | P1 parallel | P1 |
| G. vertical slice | `NEXUS-LAB/SORGENTI/G-PROCEDURE-SYNTHETIC-001.md` (da creare) + `docs/candidates/GOVERNED-EVIDENCE-DOSSIER.md` | North Star | North Star |
| CLI contracts | `cli/backlog/BACKLOG.md` CLI-008..019 + `docs/candidates/ECOSYSTEM-GOVERNANCE-PROPOSAL.md` | P2 design/docs | P2 |
| Documentation | `NEXUS-LAB/38-39` + `docs/candidates/` + `docs/approved/` | supporto handoff only | supporto |
| Ecosystem governance | `docs/candidates/ECOSYSTEM-GOVERNANCE-PROPOSAL.md` | parked | parked |
| Repeatability + Audit | `brain/data/records/final-audit-0.8.x/` + `NEXUS-LAB/36-AUDIT-FINALE-0.8.X.md` | evidence, non backlog attivo | done |

---

## Provenance

```
Main Agent: North Star G. upload→hash→structure→question→answer+claim+source+gap→Roy Client→G. correction
Program board: Foundation P0, Assistant P1, Brain P1, CLI P2, Docs supporto, G. North Star
WIP: max 1 mutazione per repo, max 3 corsie tecniche attive, decisioni owner serializzate
Ordine valore: 0.8.2 → /evaluate → upload→receipt → query → G. correction → CLI ingestion
DECIDED: ecosystem parked, Foundation proceeds, Assistant parallel, Brain parallel, CLI conditional, everything oriented to G. vertical proof
Source: conversation arena/86a8bf50-nexus-lab 2026-10-09T20:00-20:15 + ECOSYSTEM-GOVERNANCE-PROPOSAL.md
Status: CANDIDATE → requires owner approval
Extractor: documentation-agent v0.1.0
```

*Backlog generale — diverse corsie, un solo obiettivo: G. vertical proof*
