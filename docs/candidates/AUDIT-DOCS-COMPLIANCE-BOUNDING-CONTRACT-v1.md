# Audit — Compliance docs/candidates + docs/approved vs Bounding Contract v1.0

```
Status:        REVIEW_REQUIRED — AUDIT per §5, §6, §4, §7, §11, §13, §17
Version:       1.0
Date:          2026-10-11
Scope:         docs/candidates/*.md + docs/approved/*.md
Auditor:       Documentation Agent
Authority:     OWNER_DECIDED bounding contract 2026-10-11 + GIT_VERIFIED file scan
OwnerDecisionRef: 2026-10-11 OWNER-APPROVED OPERATING RULE Bounding Contract — Project Owner
MainAgentHandoffRef: Johnn — context 1-8 + bounding contract registration
LastVerifiedCommit: c35903b + 742c4d2 + a03f24b
Sensitivity:   INTERNAL
```

## Scopo

Rispondere a: "ci sono documenti da aggiornare rispetto quelli che abbiamo? rispetto questa domanda e il boundary appena scritto?"

Verifica rispetto a:

- §4 Lifecycle contract — allowed states: BRAINSTORM_SOURCE, CANDIDATE, OWNER_DECISION_PENDING, APPROVED, APPROVED_WITH_CONDITIONS, VERSIONED, DEFERRED, REJECTED, SUPERSEDED, HISTORICAL, REVIEW_REQUIRED
- §5 Promotion gate — OWNER_DECIDED, APPROVED, APPROVED_WITH_CONDITIONS, DIRECTIVE, OWNER-RATIFIED richiedono ownerDecisionRef non vuoto verificabile, altrimenti → OWNER_DECISION_PENDING o REVIEW_REQUIRED. Non inferire approval da tono Main Agent, recommendation, merged PR, filename DECISION, commit/push, assenza obiezione, repeated mention
- §6 Required document metadata — documentId, documentClass, lifecycle, authority, ownerDecisionRef, mainAgentHandoffRef, sourceRefs, lastVerifiedCommit, lastVerifiedAt, sensitivity — non inventare IDs quando registry unknown, non fabricare conversation IDs/hashes, missing → null/UNKNOWN, source hash valido solo per export canonical completo, commit/path deve identificare actual repository authority
- §7 Main Agent references — MAIN_AGENT_REFERENCE non bypassa Git/code verification, Owner approval, repository/path authority, implementation gates — non rafforzare recommendation→decision, candidate→approved, internal proof→external validation, merged implementation→completed program outcome
- §11 Program/backlog boundary — distinguere CURRENT_OWNER_APPROVED, MAIN_AGENT_RECOMMENDATION, OWNER_DECISION_PENDING, PARKED, NOT_AUTHORIZED, DONE_MERGED, DONE_SOURCE_ONLY, UNKNOWN — non trasformare brainstorming in roadmap attiva — future architecture (Foundation Bootstrap, self-hosting, Distribution Profiles, CLI workspace orchestration, VerificationReceipt, Epistemic Annotation) resta candidate/deferred unless Owner decision esplicita attiva
- §13 No document proliferation — creare solo ADR/PRD/Epic, operational backlog, evidence/report, source preservation, real-recipient artifact, owner-approved decision record, required index/receipt
- §17 Current commit review rule — preserve history, audit authority/lifecycle, correct through follow-up

## Metodo

```bash
for f in docs/candidates/*.md; do head -30 "$f" | grep -E "Status:|DecisionId|Authority|ownerDecisionRef|lifecycle|documentId|APPROVED|CANDIDATE|OWNER_DECISION|MAIN_AGENT|GIT_VERIFIED"
```

+ lettura completa file critici + check metadata YAML

## Risultato — per file

### Compliant — nessuna azione immediata

- **docs/approved/BOUNDING-CONTRACT-DOCUMENTATION-AGENT.md**
  - lifecycle: APPROVED — allowed
  - authority: OWNER_DECIDED
  - ownerDecisionRef: 2026-10-11 OWNER-APPROVED OPERATING RULE — verifiable
  - documentId: BOUNDING-CONTRACT-DOCUMENTATION-AGENT — registry-assigned per Owner
  - metadata YAML presente completo per §6
  - Status: COMPLIANT

- **docs/candidates/AUDIT-a03f24b-BOUNDING-CONTRACT-COMPLIANCE.md**
  - lifecycle: REVIEW_REQUIRED — allowed
  - authority: OWNER_DECIDED + GIT_VERIFIED
  - ownerDecisionRef: 2026-10-11 bounding contract §17
  - documentId: AUDIT-a03f24b-BOUNDING-CONTRACT-COMPLIANCE
  - metadata YAML presente
  - Status: COMPLIANT

- **docs/candidates/DECISION-0.8.2-D2-RENDERING-KIND.md**
  - lifecycle dichiarato: OWNER_DECISION_PENDING — allowed per §4
  - authority: MAIN_AGENT_RECOMMENDATION A DEFERRED + OWNER_DECISION_PENDING — corretto, non promosso a decision
  - ownerDecisionRef: assente — corretto per PENDING, non richiede per §5
  - mainAgentHandoffRef: presente (Context 3)
  - metadata parziale ma presente in header (DecisionId NX-D-045-D2, conversationId, sourceHash)
  - Manca YAML completo per §6 — da aggiungere in follow-up, ma non blocking
  - Status: COMPLIANT con minor correction needed (aggiungere YAML)

### Non compliant — richiede aggiornamento — lifecycle non allowed o promotion gate violato o metadata mancante

#### Gruppo A — Lifecycle non allowed per §4 — da correggere a allowed state

- **docs/candidates/DECISION-0.8.2-CLOSURE-STRATEGY.md**
  - Attuale: PARTIALLY APPROVED — D1 APPROVED, D2 PENDING... — non in allowed list
  - Richiesto: APPROVED_WITH_CONDITIONS (D1 approved, D2 pending, D3-D6 conditional) — allowed
  - ownerDecisionRef: presente in amendment (context 3-8 owner approvals) ma non in YAML standard — da aggiungere YAML per §6
  - Authority: OWNER_DECIDED per D1 + MAIN_AGENT_RECOMMENDATION per D2/F08-020 + APPROVED ARCHITECTURAL DIRECTION per bootstrap — distinzione presente, OK, ma lifecycle label non compliant
  - Azione: aggiornare Status a APPROVED_WITH_CONDITIONS + aggiungere metadata YAML per §6

- **docs/candidates/DECISION-0.8.2-RELEASE-TARGET-OWNER-APPROVED.md**
  - Attuale: APPROVED — allowed per §4, ma richiede ownerDecisionRef per §5
  - ownerDecisionRef: non in YAML standard, solo in testo "Context 2 + Owner approval" — per §5 serve non-empty verifiable ownerDecisionRef esplicito
  - Manca YAML completo §6
  - Azione: aggiungere YAML con ownerDecisionRef: "Context 2 2026-10-09 Release target A) Approvo simple is package target, Core Admin package A) Approvo excluded — Owner" + authority OWNER_DECIDED

- **docs/candidates/DIRECTIVE-ARENA-0.8.2-OWNER-DECISIONS-RECORDED.md**
  - Attuale: APPROVED DIRECTIVE — non allowed, contiene due stati concatenati
  - Richiesto: APPROVED (documentClass DIRECTIVE) o APPROVED_WITH_CONDITIONS — DIRECTIVE per §5 richiede ownerDecisionRef
  - ownerDecisionRef: presente in testo ma non in YAML
  - Azione: Status → APPROVED, documentClass: DIRECTIVE, aggiungere YAML con ownerDecisionRef

- **docs/candidates/EXPLANATION-0.8.2-CORE-ADMIN-PACKAGE-DISTRIBUTION.md**
  - Attuale: APPROVED EXPLANATION — non allowed (due parole)
  - Richiesto: APPROVED (documentClass EXPLANATION)
  - ownerDecisionRef: manca YAML, ma testo contiene directive OWNER DECISION RECORDED — per APPROVED serve ownerDecisionRef per §5
  - Azione: Status → APPROVED, aggiungere YAML

- **docs/candidates/STRATEGY-FOUNDATION-BOOTSTRAP-SELF-HOSTING.md**
  - Attuale: APPROVED ARCHITECTURAL DIRECTION — IMPLEMENTATION DEFERRED — non allowed come singola stringa
  - Richiesto: APPROVED_WITH_CONDITIONS con condition IMPLEMENTATION DEFERRED, oppure DEFERRED con note — per §11 future architecture (Foundation Bootstrap, self-hosting) resta candidate/deferred unless Owner decision esplicita attiva — in context 8 Owner ha approvato architectural direction ma deferred implementation — quindi APPROVED_WITH_CONDITIONS è corretto, con ownerDecisionRef che attesta approval direction
  - Manca YAML
  - Azione: Status → APPROVED_WITH_CONDITIONS, aggiungere YAML con condition

- **docs/candidates/DECISION-0.8.2-SIMPLE-DISTRIBUTION-PROOF-F08-020.md**
  - Attuale: CANDIDATE — MAIN_AGENT RECOMMENDATION — non allowed come lifecycle singolo (contiene extra)
  - Richiesto: CANDIDATE (documentClass DECISION, authority MAIN_AGENT_RECOMMENDATION)
  - ownerDecisionRef: assente — corretto per CANDIDATE (non richiede)
  - Manca YAML
  - Azione: Status → CANDIDATE, aggiungere YAML con authority MAIN_AGENT_RECOMMENDATION

- **docs/candidates/IMPLICATIONS-0.8.2-SIMPLE-DISTRIBUTION-FACTORY.md**
  - Attuale: CANDIDATE ANALYSIS — non allowed
  - Richiesto: CANDIDATE (documentClass ANALYSIS)
  - Azione: Status → CANDIDATE, aggiungere YAML

- **docs/candidates/INDEX-0.8.2-DECISIONS.md**
  - Attuale: INDEX — living document — non allowed
  - Richiesto: CANDIDATE (documentClass INDEX) o REVIEW_REQUIRED — è living index, non governing decision
  - Azione: Status → CANDIDATE, aggiungere YAML, chiarire che non è promotion decision

- **docs/candidates/06-SCREENSHOT-STORYBOARD.md**
  - Attuale: CANDIDATE_FOR_OWNER_REVIEW — non allowed
  - Richiesto: CANDIDATE o REVIEW_REQUIRED
  - Manca YAML
  - Azione: Status → CANDIDATE, aggiungere YAML con authority GIT_VERIFIED + EXTERNAL_SOURCE (screenshot reali da x.open-nexus.io)

#### Gruppo B — Metadata mancante per §6 — da aggiungere YAML

- **docs/candidates/GIT-BOUNDARIES-AND-GATES.md**
  - Status: CANDIDATE — allowed
  - Manca YAML completo §6 — ha DecisionId NX-D-044 ma non ownerDecisionRef, sourceRefs
  - Azione: aggiungere YAML con documentId NX-D-044, lifecycle CANDIDATE, authority DOCUMENTATION_AGENT_INFERENCE + MAIN_AGENT_RECOMMENDATION, ownerDecisionRef null (corretto per CANDIDATE), mainAgentHandoffRef, sourceRefs

- **docs/candidates/PROGRAM-BACKLOG-GENERALE.md**
  - Status: CANDIDATE — allowed
  - Ha DecisionId NX-D-043, approvalStatus CANDIDATE, ma manca YAML §6
  - Azione: aggiungere YAML, distinguere CURRENT_OWNER_APPROVED vs MAIN_AGENT_RECOMMENDATION vs OWNER_DECISION_PENDING per §11 — già fatto in testo ma serve YAML

- **docs/candidates/GOVERNED-EVIDENCE-DOSSIER.md**
  - Status: CANDIDATE — allowed
  - Ha DecisionId NX-D-041, approvalStatus CANDIDATE, ma dichiara "DECIDED Main Agent: APPROVED PRODUCT HYPOTHESIS" — per §7 non rafforzare recommendation→decision — file correttamente mantiene CANDIDATE, ma testo DECIDED può essere letto come promotion — va chiarito che è MAIN_AGENT_RECOMMENDATION, non OWNER_DECIDED
  - Manca YAML completo
  - Azione: aggiungere YAML con authority MAIN_AGENT_RECOMMENDATION + OBSERVED market signals, ownerDecisionRef null, chiarire in testo che product hypothesis resta CANDIDATE awaiting owner gate

- **docs/candidates/ECOSYSTEM-GOVERNANCE-PROPOSAL.md**
  - Status: CANDIDATE — allowed
  - DecisionId: PENDING_REGISTRY_ASSIGNMENT — corretto per §6 (non inventare IDs)
  - Manca YAML completo ma ha HandoffType OWNER_DECISION_PENDING — da aggiungere YAML

- **docs/candidates/DECISION-0.8.2-RELEASE-STATEMENT-CANDIDATE.md**
  - Status: CANDIDATE — allowed (con extra "requires owner final wording" va in note, non in status)
  - Manca YAML
  - Azione: Status → CANDIDATE, aggiungere YAML

#### Gruppo C — Plico F — BRAINSTORM_SOURCE o CANDIDATE senza metadata — basso rischio ma non compliant §6

- **docs/candidates/01-NARRATIVE-BRIEF-F.md**
- **docs/candidates/02-PROJECT-SHEET-F.md**
- **docs/candidates/03-SUMMARY-F-A5.md**
- **docs/candidates/04-NOTE-F-PERSONAL.md**
- **docs/candidates/05-TECHNICAL-APPENDIX-F.md**
- **docs/candidates/F-ONE-PAGE-A5.md**
- **docs/candidates/NOTE-F.md**
- **docs/candidates/TECHNICAL-NOTE-F.md**
- **docs/candidates/PROJECT-BRIEF-F-CONFIDENTIAL.md**
- **docs/candidates/PROJECT-BRIEF-F-EXECUTIVE-SUMMARY-FINAL.md**
- **docs/candidates/PROJECT-BRIEF-F-EXECUTIVE-SUMMARY.md**
- **docs/candidates/PROJECT-BRIEF-F-FINAL.md**
- **docs/candidates/PROJECT-BRIEF-F-v3.md**

  - Tutti senza header Status/DecisionId/metadata
  - Per §6: missing values remain null/UNKNOWN, ma per governing/candidate artifact should expose metadata
  - Per §4: se sono brainstorming da conversation → BRAINSTORM_SOURCE, se sono draft formalizzati → CANDIDATE
  - Azione: aggiungere YAML minimo con lifecycle BRAINSTORM_SOURCE o CANDIDATE, authority DOCUMENTATION_AGENT_INFERENCE o EXTERNAL_SOURCE, ownerDecisionRef null, sensitivity INTERNAL — oppure marcarli HISTORICAL se superati da v3 final — non blocking per 0.8.2 ma va sanato per compliance generale

- **docs/candidates/README.md**
  - Status: CANDIDATE — rule — manca YAML, ma è README di policy, non governing decision — basso rischio, aggiungere YAML con lifecycle CANDIDATE, authority DOCUMENTATION_AGENT_INFERENCE

- **docs/approved/README.md**
  - Nessun metadata — README di cartella approved — basso rischio, aggiungere YAML con lifecycle APPROVED, authority OWNER_DECIDED o DOCUMENTATION_AGENT_INFERENCE

## Violazioni potenziali promotion gate §5

- **DECISION-0.8.2-RELEASE-TARGET-OWNER-APPROVED.md** — Status APPROVED ma ownerDecisionRef non in formato verificabile YAML — rischio BLOCKED_MISSING_OWNER_DECISION_REF se letto strettamente — da correggere aggiungendo ownerDecisionRef esplicito: "2026-10-09 Context 2 Release target A) Approvo simple is package target, Core Admin package A) Approvo excluded — Owner approval verbatim + directive 2026-10-11 OWNER DECISION RECORDED"

- **DIRECTIVE-ARENA-0.8.2-OWNER-DECISIONS-RECORDED.md** — APPROVED DIRECTIVE richiede ownerDecisionRef — da aggiungere

- **EXPLANATION-0.8.2-CORE-ADMIN-PACKAGE-DISTRIBUTION.md** — APPROVED EXPLANATION richiede ownerDecisionRef — directive OWNER DECISION RECORDED è ownerDecisionRef valido, ma va in YAML

- **STRATEGY-FOUNDATION-BOOTSTRAP-SELF-HOSTING.md** — APPROVED ARCHITECTURAL DIRECTION — per §11 future architecture resta candidate/deferred unless Owner decision esplicita attiva — Owner ha approvato direction in context 8 con voto 10/10 intuizione — va documentato ownerDecisionRef esplicito per direction, con condition IMPLEMENTATION DEFERRED

## Document proliferation §13 — check

- Nessuna proliferazione critica rilevata per 0.8.2 — 7 nuovi doc context 3-8 sono giustificati come ADR/decision/explanation/index (required index/receipt) — non creati merely perché idea interessante
- Plico F ha molte versioni (v3, final, confidential, executive summary) — potenziale duplicazione — ma sono versioni storiche di recipient-facing artifact, non nuova proliferazione — va eventualmente marcato SUPERSEDED per vecchie versioni, mantenendo una canonica — non blocking ora

## Technical execution boundary §10 — check

- Nessun file in docs/candidates modifica application/source/test/package — compliant
- Nessun file esegue producer/materializer/clean-room come task owner — compliant — F08-020 è CANDIDATE recommendation, non esecuzione
- Audit a03f24b già verificato compliant

## Corrective plan — per rispettare bounding contract senza rewrite history

Per §17 preserve commit, correct through follow-up:

1. **Immediate — update critici 0.8.2 per §4 lifecycle + §5 promotion gate + §6 metadata:**

   Allowlist esatta (per §8):

   ```
   docs/candidates/DECISION-0.8.2-CLOSURE-STRATEGY.md
   docs/candidates/DECISION-0.8.2-RELEASE-TARGET-OWNER-APPROVED.md
   docs/candidates/DIRECTIVE-ARENA-0.8.2-OWNER-DECISIONS-RECORDED.md
   docs/candidates/EXPLANATION-0.8.2-CORE-ADMIN-PACKAGE-DISTRIBUTION.md
   docs/candidates/STRATEGY-FOUNDATION-BOOTSTRAP-SELF-HOSTING.md
   docs/candidates/DECISION-0.8.2-D2-RENDERING-KIND.md
   docs/candidates/DECISION-0.8.2-SIMPLE-DISTRIBUTION-PROOF-F08-020.md
   docs/candidates/IMPLICATIONS-0.8.2-SIMPLE-DISTRIBUTION-FACTORY.md
   docs/candidates/INDEX-0.8.2-DECISIONS.md
   docs/candidates/06-SCREENSHOT-STORYBOARD.md
   docs/candidates/DECISION-0.8.2-RELEASE-STATEMENT-CANDIDATE.md
   ```

   Transizioni:

   - PARTIALLY APPROVED → APPROVED_WITH_CONDITIONS
   - APPROVED DIRECTIVE → APPROVED (documentClass DIRECTIVE)
   - APPROVED EXPLANATION → APPROVED (documentClass EXPLANATION)
   - APPROVED ARCHITECTURAL DIRECTION — IMPLEMENTATION DEFERRED → APPROVED_WITH_CONDITIONS (condition: IMPLEMENTATION DEFERRED)
   - CANDIDATE — MAIN_AGENT RECOMMENDATION → CANDIDATE
   - CANDIDATE ANALYSIS → CANDIDATE
   - INDEX — living document → CANDIDATE
   - CANDIDATE_FOR_OWNER_REVIEW → CANDIDATE

   Aggiungere per ogni file YAML per §6:

   ```yaml
   documentId: <existing or PENDING_REGISTRY_ASSIGNMENT>
   documentClass: <DECISION|DIRECTIVE|EXPLANATION|STRATEGY|INDEX|EVIDENCE|OTHER>
   lifecycle: <allowed>
   authority: <OWNER_DECIDED|MAIN_AGENT_RECOMMENDATION|GIT_VERIFIED|DOCUMENTATION_AGENT_INFERENCE>
   ownerDecisionRef: <verifiable ref or null>
   mainAgentHandoffRef: <ref or null>
   sourceRefs: []
   lastVerifiedCommit: <commit>
   lastVerifiedAt: 2026-10-11
   sensitivity: INTERNAL
   ```

   Non inventare IDs: se registry unknown → PENDING_REGISTRY_ASSIGNMENT — per NX-D-045 series mantenere perché già usati come candidate IDs con provenance, ma aggiungere nota registry pending.

2. **Second — update backlog/governance per §6 + §11:**

   Allowlist:

   ```
   docs/candidates/PROGRAM-BACKLOG-GENERALE.md
   docs/candidates/GIT-BOUNDARIES-AND-GATES.md
   docs/candidates/GOVERNED-EVIDENCE-DOSSIER.md
   docs/candidates/ECOSYSTEM-GOVERNANCE-PROPOSAL.md
   ```

   Aggiungere YAML, distinguere CURRENT_OWNER_APPROVED vs MAIN_AGENT_RECOMMENDATION vs OWNER_DECISION_PENDING vs PARKED, chiarire che future architecture resta candidate/deferred.

3. **Third — plico F — low priority — BRAINSTORM_SOURCE:**

   Allowlist:

   ```
   docs/candidates/01-NARRATIVE-BRIEF-F.md
   docs/candidates/02-PROJECT-SHEET-F.md
   docs/candidates/03-SUMMARY-F-A5.md
   docs/candidates/04-NOTE-F-PERSONAL.md
   docs/candidates/05-TECHNICAL-APPENDIX-F.md
   docs/candidates/F-ONE-PAGE-A5.md
   docs/candidates/PROJECT-BRIEF-F-CONFIDENTIAL.md
   docs/candidates/PROJECT-BRIEF-F-v3.md
   ```

   Aggiungere YAML minimo con lifecycle BRAINSTORM_SOURCE o CANDIDATE, authority EXTERNAL_SOURCE o DOCUMENTATION_AGENT_INFERENCE, sensitivity INTERNAL, ownerDecisionRef null — oppure marcare SUPERSEDED per versioni vecchie.

4. **No technical rerun:** Nessun F08-020 producer/materializer/clean-room autorizzato da documentation status alone — per §10 serve separate explicit Owner assignment as Verification/Implementation Agent.

## Stop status

```
READY_FOR_OWNER_DOC_REVIEW
```

- Audit completo, compliance gaps identificati, corrective plan definito con exact allowlist per §8
- Nessun BLOCKED_MISSING_OWNER_DECISION_REF critico bloccante immediato, ma 3 file APPROVED richiedono ownerDecisionRef in YAML per piena compliance §5 — da sanare in follow-up
- Nessun BLOCKED_SENSITIVITY, BLOCKED_DUPLICATE_AUTHORITY, BLOCKED_TECHNICAL_EXECUTION_SCOPE
- Awaits Owner decision su corrective plan + Main Agent review

## Metadata per questo audit

```yaml
documentId: AUDIT-DOCS-COMPLIANCE-BOUNDING-CONTRACT-v1
documentClass: EVIDENCE
lifecycle: REVIEW_REQUIRED
authority: OWNER_DECIDED + GIT_VERIFIED
ownerDecisionRef: 2026-10-11 OWNER-APPROVED OPERATING RULE Bounding Contract — Project Owner — question "ci sono documenti da aggiornare rispetto quelli che abbiamo? rispetto questa domanda e il boundary appena scritto?"
mainAgentHandoffRef: Johnn — bounding contract v1.0
sourceRefs:
  - docs/approved/BOUNDING-CONTRACT-DOCUMENTATION-AGENT.md v1.0
  - docs/candidates/DECISION-0.8.2-CLOSURE-STRATEGY.md
  - docs/candidates/DECISION-0.8.2-RELEASE-TARGET-OWNER-APPROVED.md
  - docs/candidates/DIRECTIVE-ARENA-0.8.2-OWNER-DECISIONS-RECORDED.md
  - docs/candidates/EXPLANATION-0.8.2-CORE-ADMIN-PACKAGE-DISTRIBUTION.md
  - docs/candidates/STRATEGY-FOUNDATION-BOOTSTRAP-SELF-HOSTING.md
  - docs/candidates/DECISION-0.8.2-D2-RENDERING-KIND.md
  - docs/candidates/DECISION-0.8.2-SIMPLE-DISTRIBUTION-PROOF-F08-020.md
  - docs/candidates/IMPLICATIONS-0.8.2-SIMPLE-DISTRIBUTION-FACTORY.md
  - docs/candidates/INDEX-0.8.2-DECISIONS.md
  - docs/candidates/06-SCREENSHOT-STORYBOARD.md
  - docs/candidates/PROGRAM-BACKLOG-GENERALE.md
  - docs/candidates/GIT-BOUNDARIES-AND-GATES.md
  - docs/candidates/GOVERNED-EVIDENCE-DOSSIER.md
  - docs/candidates/ECOSYSTEM-GOVERNANCE-PROPOSAL.md
  - docs/candidates/01-NARRATIVE-BRIEF-F.md
  - docs/candidates/02-PROJECT-SHEET-F.md
  - docs/candidates/03-SUMMARY-F-A5.md
  - docs/candidates/04-NOTE-F-PERSONAL.md
  - docs/candidates/05-TECHNICAL-APPENDIX-F.md
  - docs/candidates/F-ONE-PAGE-A5.md
  - docs/candidates/NOTE-F.md
  - docs/candidates/TECHNICAL-NOTE-F.md
  - docs/candidates/PROJECT-BRIEF-F-CONFIDENTIAL.md
  - docs/candidates/PROJECT-BRIEF-F-FINAL.md
  - docs/candidates/PROJECT-BRIEF-F-v3.md
  - docs/approved/BOUNDING-CONTRACT-DOCUMENTATION-AGENT.md
  - docs/approved/README.md
lastVerifiedCommit: c35903b
lastVerifiedAt: 2026-10-11
sensitivity: INTERNAL
```

## Provenance

```
Question: ci sono documenti da aggiornare rispetto quelli che abbiamo? rispetto questa domanda e il boundary appena scritto?
Boundary: docs/approved/BOUNDING-CONTRACT-DOCUMENTATION-AGENT.md v1.0 OWNER-APPROVED OPERATING RULE
Scope audited: docs/candidates/*.md (27 files) + docs/approved/*.md (2 files)
Method: GIT_VERIFIED file scan + lifecycle allowed list §4 + promotion gate §5 + metadata §6 + Main Agent refs §7 + backlog boundary §11 + proliferation §13 + technical execution §10
Result: 2 COMPLIANT, 1 COMPLIANT with minor correction, 12 NON-COMPLIANT lifecycle non allowed or metadata missing or promotion gate risk, 14 plico F BRAINSTORM_SOURCE without metadata low risk
Corrective plan: 3 phases with exact allowlist per §8, no rewrite history, follow-up commits, no technical rerun authorized
Status: READY_FOR_OWNER_DOC_REVIEW
Extractor: documentation-agent v0.1.0
Date: 2026-10-11
```
