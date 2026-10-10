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
