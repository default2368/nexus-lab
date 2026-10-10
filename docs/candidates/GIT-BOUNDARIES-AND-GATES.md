# Git Boundaries and Gates — Operativi
**Status:** CANDIDATE
**DecisionId:** NX-D-044
**Source:** ECOSYSTEM-GOVERNANCE-PROPOSAL + 38-39 + AGENTS.md + PROGRAM-BACKLOG
**DECIDED:** Git authority per commit/ref/history, VerificationReceipt per esecuzione, DecisionReceipt per attestazione, Owner unico gate promozione

## 1. Authority Boundaries
Git È authority per: commit esiste GIT_VERIFIED, branch contiene commit, tag, history, worktree CLEAN/DIRTY
Git NON È authority per: command execution result → VerificationReceipt, owner approval → DecisionReceipt, claim verità → ClaimEnvelope, dossier valido → Governed Evidence Dossier

## 2. Branch Boundaries
Branch name NON è join key (cancellato/ricreato/force-push/repo diversi/riutilizzato) → join identity = repositoryId+taskId+executionId+resolvedCommit, branchRef metadata
Types: master protected, arena/* sessione, feature/surf/fix task, docs/* documentation lane

## 3. Commit Boundaries
Commit SHA preservato in VerificationReceipt.sourceCommit, origin GIT_VERIFIED vs WORKTREE_UNVERIFIED
Agent propone, CLI esegue, System registra result/receipt (exitCode derivato), Owner decide — Agent non scrive manualmente exitCode
Conventions: feat/fix con scope+provenance+decisionId+status

## 4. Worktree Boundaries
CLEAN/DIRTY + GIT_VERIFIED/WORKTREE_UNVERIFIED, max 1 mutazione per repo, max 3 corsie tecniche attive (Foundation, Backend, Assistant), clone/attach via ProjectContext+WorkspaceManifest+GitSnapshot, divergence report, WorkspaceLock, exportable workspace

## 5. Verification Boundaries
VerificationReceipt v0.1: receiptId, executionId, taskId, repository{repositoryId, remote, branchRef, sourceCommit, sourceCommitOrigin, worktreeState}, command{commandId, argv, cwdRole, toolVersion}, result{startedAt, completedAt, exitCode, outputSha256, findingCount}, scope{mode CLOSED_WORLD/BOUNDED/OPEN_WORLD, paths, limitations}
Storage: one receipt=one immutable JSON file non JSONL mensile condiviso (Mac/Linux/Arena append → merge conflict) → layout receipts/open-nexus-foundation/2026/10/run-01K...json → DuckDB rebuildable read model
Writer: CLI/Verification Core authority, Git hook optional canary, Agent requester
Local spool: .nexus/receipts/ non committato, approved packet in doc control plane, new central audit repo REVIEW_REQUIRED fino a volume+secondo consumer

## 6. Promotion Gates
Nessuna promozione automatica CANDIDATE→APPROVED→VERSIONED merged≠canonical Status governa
OWNER_DECISION_PENDING handoff → ADR/PRD/Epic/backlog/finding → APPROVED/CONDITIONS/DEFERRED/REJECTED — Owner unico gate
Protected kernel: PageController, normalizeToPageData, ApplicationDefinition, ApplicationContext, BundleCollector, DiscoveryService/V2 forbidden without explicit consent + OWNER_DECISION_PENDING + verification receipt CLEAN+GIT_VERIFIED + owner approval + contract test

## 7. Security Gates
Repository private, secret scan (GITHUB_TOKEN, AWS_ACCESS_KEY, PRIVATE_KEY_BLOCK, BEARER_TOKEN), PII/sensitivity classification, no auto public, no raw conversation in default Brain retrieval, retention policy
Conversations: sources/conversations/ raw not default Roy corpus not canonical authority
Corpus: sources/conversations/ raw, docs/candidates/ CANDIDATE drafts must have conversationId/turn/date/hash/extractor/target/approval status, docs/approved/ APPROVED ratified, archive/ superseded, brain/data/records/ provenance JSONL 6 campi minimi+content_sha

## 8. Operational Gates
Program board: Foundation P0 PR #14→/api/v1/debug/redis→SURF-082→v0.8.2, Assistant P1 aa17567→/evaluate→upload UI, Brain P1 ClaimEnvelope+Acquisition M1 size/MIME→SHA-256→RawEvidenceBlob→SourceObservation→AcquisitionReceipt text/markdown synthetic only, CLI P2 contracts ProjectContext/WorkspaceManifest/WorkspaceLock/GitSnapshot/VerificationReceipt/HandoffReceipt conditional, Docs supporto handoff only, G. pilot North Star upload→receipt→parse→evaluate→Roy Client→G. correction
Order of value: 0.8.2→/evaluate→upload→receipt→query→G. correction→CLI ingestion
Ecosystem governance parked non blocking
Checklist 12 voci: repositoryId+taskId+executionId+resolvedCommit identity, worktree CLEAN/DIRTY, one receipt=one JSON, CLI writer, no JSONL mensile, no auto-promotion, protected kernel, secret scan, fonte conservata, WIP limit max1 per repo max3 corsie, order of value, .nexus/receipts/ spool

*Git è authority per commit/ref/history, VerificationReceipt per esecuzione, DecisionReceipt per attestazione, Owner per promozione*
