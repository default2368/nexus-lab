# 38 — Regola Chat — Main Agent + Support Agent

**Data:** 2026-10-09
**Richiesta utente:** sgravarlo dallo scrivere documentazione, altro agent è Main Agent, suoi riferimenti sono autorità
**Stato:** CANONICAL — CHAT RULE

## Ruoli
### Main Agent (collega valido, senza controllo git)
- Definisce workflow, DECIDED, APPROVED DIRECTION, REJECTED
- Scrive direzione architetturale, hypothesis memo, falsificazione
- Non deve scrivere documentazione ripetitiva — sgravato
- I suoi blocchi DECIDED sono autorità

### Support Agent (questo agent, con controllo git)
- Esegue Classe 0 deterministica: find, grep, sha, parsing, inventory, f08-audit, scan-project-layout, repeatability-test, collect-epistemic-records
- Codifica risposte in record con 6 campi minimi + content_sha + provenance + COMMAND-LEDGER
- Non produce token senza motivo
- Non fa auto-ingestion, no auto-promotion, no new branch during 0.8.2
- Pusha su arena/86a8bf50-nexus-lab

### Human (owner)
- Propone, corregge, promuove esplicitamente
- Legge matrici, codifica, mette in produzione

## Workflow approvato (da Main Agent)
1. preserva originale + SHA
2. parsing deterministico Classe 0
3. estrai heading/list/table
4. una interpretazione Brain marcata INFERITO
5. candidate claims (6 campi minimi)
6. human review CANDIDATE
7. promuovi solo con approvazione esplicita
8. rigenera matrice
9. confronta → PASS/FAIL + falsificazione
10. PageData via existing template

## DECIDED
Governed Evidence Dossier → APPROVED PRODUCT HYPOTHESIS
Cross-sector mechanism → APPROVED DIRECTION
Market validated → NO
Method repeatable → INTERNAL PROOF M0
G. → first falsification pilot
One-pager → hypothesis memo
New branch → NO during 0.8.2
Auto-ingestion, auto-promotion, headless/proxy/ML → REJECTED
Mescolare binari → REJECTED fino a secondo caso

## Linguaggio
Italiano, OSSERVATO/INFERITO/LIMITE, OBSERVED MARKET SIGNAL vs VALIDATED, formula onesta meccanismo promettente + workflow concreto + segnali coerenti → test buyer reale

---

## Aggiornamento 9/10 — Separate Documentation Agent (2026-10-09)

**Voto:** 9/10 (Visione 9.5, Separazione 9.5, Context switching 9, Fattibilità 9, Provenance 9, Tempismo 9, Governance 7.5, Rischio duplicazione 7.5)

**Modello operativo:**
```
conversazione (brainstorming, architettura, owner reasoning)
→ documentation agent (estrae, formalizza)
→ documentation Git repo (conserva versioni e review)
→ owner (ratifica, corregge, rifiuta)
→ technical repos (verità code-coupled)
```

**Ruoli:**
- Johnn: co-founder/architect/PM → analizza, propone, identifica decisioni, produce handoff OWNER_DECISION_PENDING
- Documentation Agent: redige, normalizza, controlla link/status, commit/push/PR
- Owner: approva/respinge — unico gate promozione
- Git: conserva fonte, revisioni, decisioni

**OWNER_DECISION_PENDING handoff:**
```yaml
decisionId, title, scope, status: OWNER_DECISION_PENDING, observed, inferred, proposed, conflicting, unknown, limits, recommendedDecision, alternatives, consequences, implementationImpact, sourceConversationRef (conversationId, turn/range, date, source hash, extractor, target, approval status)
```
→ ADR/PRD/Epic/backlog/finding/decision record/evidence report → APPROVED/APPROVED_WITH_CONDITIONS/DEFERRED/REJECTED

**Tre regole per 9.5/10:**
1. conversazione non è authority canonica (raw → source evidence, approved ADR/PRD → governing authority)
2. ogni documento conserva fonte (conversationId, turn, date, hash, extractor, target, approval status)
3. nessuna promozione automatica (CANDIDATE → APPROVED → VERSIONED, merged ≠ canonical)

**Corpus separation:**
```
sources/conversations/ → raw, not default Roy corpus
docs/candidates/ → drafts
docs/approved/ → ratified
archive/ → superseded/rejected
```

**Sicurezza:** private repo, secret scan, PII classification, no auto public publication, no raw in default Brain retrieval, retention policy

**DECIDED:**
Separate Documentation Agent → APPROVED OPERATING DIRECTION
Conversation Git repo → APPROVED AS SOURCE/REVIEW CONTROL PLANE
Automatic authority promotion → PROHIBITED
OWNER_DECISION_PENDING handoff → APPROVED
Writing every document in this chat → no longer required

Vedi NEXUS-LAB/39-OWNER-DECISION-PENDING-WORKFLOW.md
