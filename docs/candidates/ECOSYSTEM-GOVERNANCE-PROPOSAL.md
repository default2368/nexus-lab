# Ecosystem Governance Proposal — Verification Receipts and Exportable Workspace Control Plane

**Status:** CANDIDATE
**DecisionId:** PENDING_REGISTRY_ASSIGNMENT
**HandoffId:** ecosystem-verification-control-plane
**HandoffType:** OWNER_DECISION_PENDING
**Source:** Main Agent evaluation + Documentation Agent formalization
**ConversationRef:**
  conversationId: arena/86a8bf50-nexus-lab
  turnRange: 2026-10-09T19:40-20:00
  date: 2026-10-09
  sourceHash: 6ce2338 + adc423d + c036d6e
  extractor: documentation-agent v0.1.0 (Support Agent)
  targetDocument: docs/candidates/ECOSYSTEM-GOVERNANCE-PROPOSAL.md
  approvalStatus: CANDIDATE
**Target:** EPIC-ECOSYSTEM-VERIFICATION-CONTROL-PLANE.md in nexus-lab-documentation
**Provenance:** Main Agent handoff + targeted refs + owner decisions + open questions (raw conversation NOT passed as operational prompt)

---

## Sì: nuovo agente specializzato, non Documentation Agent

### Nuovo ruolo

```text
Ecosystem Control Plane Agent
oppure
CLI / Workspace / Verification Agent
```

**Responsabilità:**

- ProjectContext
- workspace esportabile
- clone/attach
- Git/worktree
- handoff
- verification receipt
- divergence report
- store derivato
- futura orchestrazione CLI

Il Documentation Agent entra dopo, per formalizzare le decisioni ratificate. Non deve progettare il control plane.

Non passerei al nuovo agente tutta la conversazione grezza come prompt operativo. Gli passerei:

```text
Main Agent handoff
+
riferimenti mirati
+
decisioni owner
+
open questions
```

La conversazione completa può restare nel repository sorgente per provenance.

---

## Valutazione proposta ricevuta

```text
intuizione layer separation    9/10
JSONL come candidato           8/10
SQLite/DuckDB derivato         9/10
repo audit separato ora        6.5/10
branch name come join key      4/10
agent come writer authority    4/10
proposta corretta              circa 7/10
```

Con alcune correzioni arriva a 9/10.

### Cosa condivido

```text
record
≠
read model
≠
report
```

E condivido:

```text
YAML
→ config umana

JSON/JSONL
→ record machine-readable

SQLite/DuckDB
→ projection/query store

Markdown/HTML
→ report/view
```

SQLite non deve essere l'unica authority se vogliamo:

- diff
- blame
- merge
- audit
- portabilità

---

## Correzione 1 — Git resta authority dei fatti Git

Non duplicherei ogni commit/ref come se il JSONL diventasse più vero di Git.

```text
commit esiste?
→ Git è source of truth

branch contiene commit?
→ Git è source of truth

command è stato eseguito con un certo risultato?
→ VerificationReceipt è source of truth dell'esecuzione

owner ha approvato?
→ DecisionReceipt è source of truth dell'attestazione
```

Quindi il record store contiene principalmente:

```text
observations
plans
command receipts
verification receipts
handoff receipts
owner attestations
publication receipts
```

Non una copia completa di ciò che Git sa già.

## Correzione 2 — branch name non è una join key sufficiente

Un branch può essere:

- cancellato
- ricreato
- force-pushato
- presente in repository diversi
- riutilizzato da due sessioni

Join identity candidata:

```text
repositoryId
+
taskId
+
executionId
+
resolvedCommit
```

Il branch rimane metadata:

```yaml
branchRef: arena/23b8d15c-open-nexus-foundation
```

non primary identity.

## Correzione 3 — un JSONL mensile condiviso crea conflitti

```text
Mac append
Linux append
Arena append
→ stesso file mensile
→ merge conflict
```

Preferisco:

```text
one receipt = one immutable JSON file
```

oppure:

```text
one execution/session = one JSONL
```

Layout:

```text
receipts/
└── open-nexus-foundation/
    └── 2026/
        └── 10/
            ├── run-01K...json
            ├── run-01K...json
            └── task-SURF-082-005/
                └── execution-01K....jsonl
```

Il read model DuckDB importa tutti i receipt.

Se vogliamo JSONL:

```text
per execution
→ sì

per project/month con writer concorrenti
→ no
```

## Correzione 4 — lo script può produrre record

Questa frase è troppo assoluta:

> script solo in uscita, mai in ingresso.

Il sistema deve produrre receipt deterministicamente.

```text
command
→ executor
→ CommandResult
→ receipt writer
```

Il punto non è vietare lo script in ingresso. È preservare:

- producer
- versione
- input
- scope
- commit
- exit code
- hash
- timestamp

Un record derivato è valido se dichiara di essere derivato.

```text
DERIVED
≠
RAW
```

## Correzione 5 — agent non scrive il receipt authoritative

Il writer deve essere:

```text
CLI / Verification Core
```

Non il modello.

```text
Agent
→ propone comando/piano

CLI
→ esegue

System
→ registra result/receipt

Owner
→ decide
```

Un agent può invocare la CLI, ma non compilare manualmente:

```json
{"exitCode": 0}
```

Il sistema deve derivarlo dal processo.

---

## Risposta alle tre domande

### 1. Repo separato o dentro Foundation?

```text
Dentro Foundation
→ NO
```

Ma non aprirei immediatamente un quinto repository.

Prima:

```text
.nexus/receipts/
→ local spool

approved receipt packet
→ documentation control plane
```

Quando esistono:

- volume reale
- secondo repository consumer
- query cross-project
- retention diversa

allora:

```text
open-nexus-control-plane
oppure
open-nexus-audit
```

diventa giustificato.

Quindi:

```text
separate authority
→ YES

new repository today
→ REVIEW_REQUIRED
```

### 2. Rotazione

```text
per execution/task
→ SÌ

per progetto/mese
→ NO come primary write unit

per sessione Arena
→ solo se executionId stabile
```

### 3. Chi scrive?

```text
CLI / Verification Core
→ authority writer

Git hook
→ optional canary, non authority

Agent
→ requester/interpreter, non writer
```

Gli hook locali possono essere saltati e non viaggiano automaticamente fra clone. Non possono essere il gate principale.

---

## Contratto candidato — VerificationReceipt v0.1

```ts
interface VerificationReceipt {
  schemaVersion: "verification-receipt/0.1";

  receiptId: string;
  executionId: string;
  taskId?: string;

  repository: {
    repositoryId: string;
    remote: string;
    branchRef?: string;
    sourceCommit: string;
    sourceCommitOrigin: "GIT_VERIFIED" | "WORKTREE_UNVERIFIED";
    worktreeState: "CLEAN" | "DIRTY";
  };

  command: {
    commandId: string;
    argv: string[];
    cwdRole: string;
    toolVersion: string;
  };

  result: {
    startedAt: string;
    completedAt: string;
    exitCode: number;
    outputSha256?: string;
    findingCount?: number;
  };

  scope: {
    mode: "CLOSED_WORLD" | "BOUNDED" | "OPEN_WORLD";
    paths?: string[];
    limitations: string[];
  };
}
```

---

## È moat?

### La complessità da sola non è moat

```text
molti repository
molti ADR
molti agenti
molti layer
```

possono essere semplicemente debito.

Il moat è:

> riuscire a governare quella complessità con contratti, gate, receipt e projection senza perdere authority o riproducibilità.

```text
complexity
+ governance executable
+ accumulated falsifications
+ reusable Foundation
+ domain replaceability
= candidate moat
```

Se il sistema richiede sempre una mattinata dell'owner per riconciliarsi:

```text
complexity
→ liability
```

Se la CLI ricostruisce workspace, verifica branch, produce receipt e mostra divergenze:

```text
complexity
→ governed capability
```

Quindi sì, l'interconnessione è una parte del moat, ma soltanto quando diventa:

- invisibile all'utente
- riproducibile
- verificabile
- delegabile
- fail-closed

### Voto al moat candidato

```text
Foundation invariants                8.5/10
Epistemic governance                 9/10
Cross-layer orchestration attuale    6/10
Cross-layer orchestration futura     9/10
Moat dimostrato commercialmente      4/10
```

Architetturalmente è forte. Commercialmente resta da provare con G.

---

## OWNER_DECISION_PENDING — packet per nuovo agente

```yaml
handoffType: OWNER_DECISION_PENDING
handoffId: ecosystem-verification-control-plane
decisionId: PENDING_REGISTRY_ASSIGNMENT

title: Ecosystem Verification Receipts and Exportable Workspace Control Plane

scope:
  - CLI V1
  - Git and worktree orchestration
  - Mac/Linux/Arena handoff
  - cross-repository verification
  - documentation control plane

status: OWNER_DECISION_PENDING

observed:
  - Repeated Mac/Linux/Arena reconciliation has required manual branch, worktree and ancestry audits.
  - Foundation already emits deterministic provenance and release eligibility.
  - Existing guards are not always wired to an automatic trigger.
  - Git is authority for commits and refs, but command execution currently lacks a common receipt contract.
  - Current documentation tooling already uses local spools and owner-gated publication.

inferred:
  - A shared VerificationReceipt contract can reduce repeated manual reconciliation.
  - A CLI-controlled workspace can make multi-repository environments reproducible.
  - A queryable derived store is useful, but must not replace Git or receipt authority.

proposed:
  - CLI owns ProjectContext, Git orchestration, worktrees, handoff and receipt writing.
  - Foundation continues to own Distribution Core and Foundation conformance.
  - Verification receipts are immutable per execution/task.
  - Local receipts live under .nexus/receipts.
  - DuckDB or SQLite is a rebuildable read model.
  - YAML is limited to human-authored configuration.
  - A dedicated audit/control-plane repository is deferred until evidence of a second consumer and sufficient volume.

decided:
  - Git remains authority for commits, refs and repository history.
  - Agents do not author authoritative execution results.
  - No direct Foundation source ownership is transferred to CLI.
  - Production and release channels remain separate dimensions.
  - Backend is excluded from the first distribution-workspace profile.

unknown:
  - authoritative CLI repository
  - receipt retention policy
  - signing requirements
  - central repository timing
  - multi-tenant requirements
  - CI integration
  - required receipt fields beyond the first pilot

conflicting:
  - JSONL monthly files are simple but create concurrent-writer merge conflicts.
  - A dedicated repository improves separation but adds another authority and operational surface.
  - Git hooks are cheap but not portable or enforceable enough to be primary gates.

recommendedDecision: >
  APPROVE AS DEVELOPMENT DIRECTION WITH CONDITIONS. Create a specialized CLI/Workspace
  and Verification Agent. Begin with a read-only reality audit and a VerificationReceipt
  v0.1 candidate. Do not create a new central audit repository or implement event
  sourcing until the current CLI authority and second consumer are verified.

alternatives:
  - project-local audit files
  - dedicated audit repository immediately
  - SQLite as primary
  - Git hooks as primary writer
  - documentation repository as receipt store

implementationImpact:
  foundation:
    change: none; remains distribution/conformance authority
  cli:
    change: future workspace, GitProvider, handoff and receipt capabilities
  documentation:
    change: owner-gated receipt publication/index
  backend:
    change: none in first profile

candidateArtifact:
  class: EPIC
  targetRepository: nexus-lab-documentation
  targetPath: docs/candidates/EPIC-ECOSYSTEM-VERIFICATION-CONTROL-PLANE.md

ownerGate:
  required: true
  decision: PENDING
```

---

## Decisione sul nuovo agente

```text
Nuovo agente specializzato
→ SÌ

Documentation Agent
→ riceve il handoff e formalizza dopo owner gate

Main Agent
→ conserva architettura e confini

Foundation roadmap
→ non interrotta
```

Questa conversazione può essere passata al nuovo agente attraverso il packet sopra. Non gli darei mandato di codificare: prima deve verificare il CLI repo reale, gli script esistenti e i worktree contract.

---

## Provenance

```
Main Agent evaluation: 9/10 layer separation, 8/10 JSONL, 9/10 SQLite/DuckDB derivato, 6.5/10 repo audit separato, 4/10 branch join key, 4/10 agent writer authority, 7/10 proposta corretta
Corrections: 5 (Git authority, branch join key, JSONL monthly conflicts, script can produce record DERIVED≠RAW, CLI core writer not agent)
Contract: VerificationReceipt v0.1 candidate
Moat: Foundation 8.5, Epistemic 9, Cross-layer attuale 6, futura 9, commerciale 4
Handoff: ecosystem-verification-control-plane OWNER_DECISION_PENDING
Status: CANDIDATE → requires owner approval → APPROVED AS DEVELOPMENT DIRECTION WITH CONDITIONS
Extractor: documentation-agent v0.1.0
Source: conversation arena/86a8bf50-nexus-lab + Main Agent packet
```

*Formalizzato da Documentation Agent, non progettato — Main Agent conserva architettura e confini*
