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

## 8. Operational Gates — UPDATED 2026-10-11 per owner decisions context 3-8
Program board: Foundation P0 — UPDATED: release target simple APPROVED, Core Admin package CORE_ADMIN_PACKAGE_OUT_OF_0_8_2_RELEASE_SCOPE APPROVED, rendering.kind DEFERRED_WITH_OWNER_DECISION PENDING A raccomandato, diagnostic API policy closure must-close (INTENTIONALLY_PUBLIC/AUTH_REQUIRED/PRODUCTION_DENY/DEVELOPMENT_ONLY/UNKNOWN non blanket gate, /api/v1/redis/test→PRODUCTION_DENY, /api/redis→DEVELOPMENT_ONLY, /api/v1/redis/pages→AUTH_REQUIRED, /api/v2/discovery→intentionally public, debug/refresh/mutating→AUTH_REQUIRED), backup/snapshot disposition, simple full pipeline F08-020 Simple Distribution Release Proof CANDIDATE next (5 pages 4 template 5 asset producer ACCEPT GIT_VERIFIED CLEAN releaseEligible true validator ACCEPT materialization 0 clean-room ok repositoryObservations 0), compatibility matrix v0.8.1→0.8.2, release statement candidate "Foundation 0.8.2 consolida convergenza authority e sicurezza necessaria a produrre package Simple bounded riproducibile verificato in clean-room mantenendo espliciti e non distribuiti residual source non ancora migrati", repo può essere complesso prodotto pulito Repository-Centric→Artifact-Centric, PR #14→/api/v1/debug/redis→SURF-082→v0.8.2, Assistant P1 aa17567→/evaluate→upload UI, Brain P1 ClaimEnvelope+Acquisition M1 size/MIME→SHA-256→RawEvidenceBlob→SourceObservation→AcquisitionReceipt text/markdown synthetic only, CLI P2 contracts ProjectContext/WorkspaceManifest/WorkspaceLock/GitSnapshot/VerificationReceipt/HandoffReceipt + Foundation Release/ApplicationSpec/DomainPackSpec/WorkspaceProfile/Authoring Core + workspace create opnx workspace create --foundation v0.9.x --profile governed-dossier --domain g-audit → plan/apply/verify + bootstrap sequence 0.8.2 Simple Proof→0.9 Semantic Entity→second app Domain Pack N-sectors→Workspace/ApplicationSpec→CLI workspace create→Foundation Bootstrap F0→F1→equivalence gate conditional, Docs supporto handoff only, G. pilot North Star upload→receipt→parse→evaluate→Roy Client→G. correction
Order of value: 0.8.2→/evaluate→upload→receipt→query→G. correction→CLI ingestion→N-sectors proof→bootstrap
Ecosystem governance parked non blocking — Foundation Bootstrap APPROVED ARCHITECTURAL DIRECTION IMPLEMENTATION DEFERRED
Moat: codebase pulita→output copiabile, meccanismo che rigenera→capability, meccanismo che rigenera sé stesso→candidate moat — Infrastructure must be reusable Domain must be replaceable — Foundation produce Execution esegue — factory can use own process to refound itself
Checklist 12 voci: repositoryId+taskId+executionId+resolvedCommit identity, worktree CLEAN/DIRTY, one receipt=one JSON, CLI writer, no JSONL mensile, no auto-promotion, protected kernel, secret scan, fonte conservata, WIP limit max1 per repo max3 corsie, order of value, .nexus/receipts/ spool
Links: DIRECTIVE-ARENA-0.8.2-OWNER-DECISIONS-RECORDED.md, EXPLANATION-0.8.2-CORE-ADMIN-PACKAGE-DISTRIBUTION.md, DECISION-0.8.2-D2-RENDERING-KIND.md, DECISION-0.8.2-SIMPLE-DISTRIBUTION-PROOF-F08-020.md, IMPLICATIONS-0.8.2-SIMPLE-DISTRIBUTION-FACTORY.md, STRATEGY-FOUNDATION-BOOTSTRAP-SELF-HOSTING.md

*Git è authority per commit/ref/history, VerificationReceipt per esecuzione, DecisionReceipt per attestazione, Owner per promozione*
