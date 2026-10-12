# Governed Evidence Dossier — Istruttoria verificabile

**Status:** CANDIDATE
**DecisionId:** NX-D-041
**Source:** NEXUS-LAB/37-LETTURA-OWNER-CORRETTA-HYPOTHESIS-MEMO.md + 39-OWNER-DECISION-PENDING-WORKFLOW.md
**DECIDED Main Agent:** Governed Evidence Dossier → APPROVED PRODUCT HYPOTHESIS (market validated NO, method INTERNAL PROOF M0)
**ConversationRef:**
  conversationId: arena/86a8bf50-nexus-lab
  turnRange: 2026-10-09T19:00-19:35
  date: 2026-10-09
  sourceHash: adc3f2f + 3882d64 + 6ce2338
  extractor: documentation-agent v0.1.0 (Support Agent)
  targetDocument: docs/candidates/GOVERNED-EVIDENCE-DOSSIER.md
  approvalStatus: CANDIDATE
**Provenance:** 478 records, SHA 582d4373807d (24), fa1615760c8e (35), repeatability 3/4 PASS M0

---

## Tesi

> Open Nexus trasforma fonti documentali frammentate in dossier governati nei processi in cui qualcuno deve rendere conto di una decisione.

Non chatbot, non document manager, non generic app builder, non scraping tool, non reportistica manuale.

---

## Input / Output

**Input:**
- procedure
- contratti
- documenti
- questionari
- evidenze
- fonti pubbliche
- decisioni precedenti

**Output:**
```text
dossier versionato
├── claim (con epistemic_status OBSERVED/INFERRED/PROPOSED)
├── evidenze (excerpt + locator)
├── fonte (source_url + source_locator + content_sha + collected_at)
├── gap (cosa manca)
├── conflitto (CONFLICTING)
├── azione (feedback → action)
├── approvazione (approval record umano)
└── receipt (command + exitCode + verifiedAt + tool_version)
```

---

## Buyer — chi paga

Non "chi vuole sapere qualcosa".

Ma:

> chi deve prendere, approvare o difendere una decisione.

Esempi N-settori (stessa funzione, settori diversi):
- G. audit: deve chiudere istruttoria con evidenze citate
- RENTRI: deve dimostrare formulario → registro con provenance
- Bandi: deve difendere punteggio con fonte
- Acquire.com: deve valutare business con ricavo dichiarato + multiplo

Funzione comune:
```text
workflow in cui qualcuno deve rendere conto → di una decisione → sulla base di evidenze → dentro processo governato
```

Coerente con: Infrastructure must be reusable; Domain must be replaceable.

---

## Governance Tiers — ipotesi, non pricing

```text
Tier 1 — Observe
  dossier navigabile
  fonti e locatori
  read-only
  Valore: vede da dove viene ogni cella

Tier 2 — Compose
  candidate records
  matrici/proiezioni
  revisioni
  Valore: compone dossier, corregge modello

Tier 3 — Govern
  approval
  audit trail
  policy gates (VALIDATE)
  receipts (command + exitCode + SHA)
  role-specific views
  Valore: difende decisione in audit, riduce tempo ricostruzione
```

Premium Tier 3 è ipotesi da testare con buyer reali (H2).

---

## Evidenza osservata — OBSERVED MARKET SIGNAL (non VALIDATED)

- **B2B/B2C spread:** 7 inserzioni Acquire.com seller-reported → $0,25-1/utente/anno B2C vs $189-391/cliente/anno B2B → spread 190-1500× osservato (non stesso prodotto, differisce per servizio, sales motion, supporto, rischio)
- **Horizontal/vertical:** Visualping $14-140/mese vs Particl $500-5000/mese → comparabile 7-70× premio, non prova causale (può dipendere da data asset, volume, reporting, team workflow)
- **Repeatability:** dossier 24 decomposto → 12 claim con 6 campi minimi + content_sha → matrice rigenerata → 3/4 match → PASS REPEATABLE M0 (internal proof, non prodotto — servono secondo operatore blind, secondo dossier, corpus altra lingua, negative control, failure criteria, tempo/costo)
- **Foundation:** content_sha + changed + 304 + manifest + clean-room (F08-014) → distribution/provenance
- **Brain:** Prometeo 11/14 OBSERVED SUFFICIENT, Bolt 0/14 INSUFFICIENT → finding su euristica sensibile a lingua/struttura, non prova generale
- **G. workflow:** Procedure→questionnaire→response→evidence→feedback→action→verification→approval→closure → concreto per pilot

---

## Ipotesi H1-H5

```text
H1 buyer values traceability over generic generation
H2 governance supports a higher price tier
H3 same infrastructure supports a second domain
H4 dossier reduces reconstruction/review time
H5 non-technical expert can correct the model
```

---

## Falsificazione F1-F6

```text
F1 G. does not recognize the workflow
F2 sources/claim links are not useful during review
F3 dossier production costs more than manual reconstruction
F4 second domain requires kernel changes
F5 buyer will not allocate budget for governance
F6 another operator cannot reproduce the dossier
```

---

## Pilot Proof — cosa serve per falsificare

```text
one real/sanitized workflow (G.)
one complete dossier (versionato con claim+evidenze+fonte+gap+conflitto+azione+approvazione+receipt)
one correction session (non-technical expert corregge modello)
one repeated run (rigenera matrice da record)
one second operator (blind, non ha visto originale)
one willingness-to-pay conversation (Tier 3 premium)
```

---

## Metriche

- claim coverage (quanti claim estratti vs attesi)
- percentage with source locator (quanti con file:linea o URL + excerpt)
- gaps/conflicts (quanti gap aperti, quanti conflitti)
- correction count (quante correzioni non-tecnico)
- review time (tempo review vs ricostruzione manuale)
- regeneration parity (match matrice rigenerata vs originale, target 3/4+)
- source-to-decision traceability (puoi tornare da decisione a fonte?)
- buyer budget/owner (chi paga, quanto)

---

## PageData Target — candidate projection (verifica contract gate prima)

Non inventare nuovi block type senza gate.

Target corretto:
```text
ClaimRecord[] + MatrixProjection + Provenance → EntityViewArtifact / knowledge artifact → PageData Adapter → existing or approved template
```

Esempio PAGEDATA.json (da repeatability-24, già generato):
```json
{
  "schemaVersion": "pagedata/v0.8",
  "pageId": "nexus-lab/24-scansione-per-capacita",
  "blocks": [
    {"type": "claim-list", "claims": [{"id": "NX24-27020D8C", "text": "238 abbonati valgono più di 25.000 utenti", "sha": "0553d2ee8a1d"}]},
    {"type": "matrix", "id": "asse-1", "rows": 7, "provenance": "deterministic parsing + candidate claims"},
    {"type": "metric", "value": "$11k–$50k ARR, 2,7–3,0×"}
  ],
  "provenance": {"sourceSha": "582d4373807d", "recordCount": 12}
}
```

Verificare prima: block contract esistente, template consumer, capability identity, package membership, source/provenance shape, asset requirements, PageData adapter, no protected-kernel modification.

---

## DECIDED

```text
Governed Evidence Dossier → APPROVED PRODUCT HYPOTHESIS
Cross-sector mechanism → APPROVED DIRECTION
Market validated → NO
Method repeatable → INTERNAL PROOF M0, external test pending
G. → first falsification pilot
One-pager → useful, if clearly marked hypothesis memo
New implementation branch → NO, not during 0.8.2
```

Formula onesta:
> Abbiamo un meccanismo tecnico promettente, un primo vertical workflow concreto e segnali economici coerenti. Ora dobbiamo vedere se un buyer reale riconosce valore nel dossier e nella governance.

---

## ADDENDUM 2026-10-11 — Simple come fabbrica + Foundation Bootstrap — context 5-8

**Status addendum:** CANDIDATE ANALYSIS — link a decisioni 0.8.2

### Simple factory — implicazione per dossier

Se catena funziona:

```text
ApplicationBundle Simple
→ Foundation
→ manifest
→ package autonomo
→ clean-room
→ Execution
```

allora Open Nexus è già fabbrica di applicazioni distribuibili, non solo framework.

Per Governed Evidence Dossier significa:

```text
repository → authoring/compiler/governance
package → prodotto distribuibile (dossier app)
Execution → runtime sottile
Domain Pack → differenzia verticali (G audit, A operation reconstruction, F project evidence)
```

Repo può essere complesso, prodotto pulito:

```text
current source residuals → governati e non distribuiti
consumer artifact → pulito, bounded, verificato
```

Repository-Centric → Artifact-Centric — già dimostrato in 0.8.1 con simple 5 pagine 4 template 5 asset producer ACCEPT GIT_VERIFIED CLEAN releaseEligible true validator ACCEPT materialization 0 clean-room ok repositoryObservations 0.

### Moat — Foundation compiler/control plane

Execution Shell riproducibile 80%. Moat meno copiabile:

```text
contratti
authority
BundleCollector
profile resolution
validation
compatibility
materialization
provenance
release receipts
migration findings
```

Ovvero Foundation compiler/control plane. Modello:

```text
Execution → sottile distribuibile
Foundation release/producer → governato
CLI → orchestratore (opnx workspace create --foundation v0.9.x --profile governed-dossier --domain g-audit)
Brain → propone Domain Pack/record candidati
umano → approva
Foundation → compila
```

Risponde a osservazione owner 80% riproducibile — Foundation messa in mezzo spiega stranezze codificate.

### Brain come authoring assistant

```text
documenti/procedure → Brain interpreta → Candidate Domain Definition → umano corregge → Domain Pack approvato → Foundation produce package → Execution esegue
```

AI entra una volta interpretazione. Resto deterministico: schema, identity, package, hash, compatibility, deployment receipt.

Non vendiamo risposta AI. Vendiamo applicazione prodotta da conoscenza governata.

### Bootstrap — moat candidato forte

Intuizione owner 10/10: fabbrica può usare proprio processo per rifondare sé stessa.

Due strade:

1. **Nuova app pulita che consuma Foundation** — `new-knowledge-app/.nexus/applications/domain-packs/presentation/fixtures/tests/package.json` — non copia kernel, lo consuma come release — consumer pulito — strada semplice migliore

2. **Nuova Foundation bootstrap** — F0 produce F1, F1 produce stessi artifact approvati, F1 può produrre F2 equivalente — self-hosting compiler pattern — fixed-point test semantic inventory A = B (page IDs, order, templates, assets, routes, capabilities, contracts, clean-room behavior)

Moat:

```text
codebase pulita → output (copiabile)
meccanismo che la rigenera → capability (più difficile)
pipeline governata che produce N domini → forte
Foundation che può riprodurre semanticamente sé stessa → molto forte
```

Quando rumore storico supera valore operativo, non pulisci infinito — materializzi nuova baseline da conoscenza e contratti approvati.

Sequence realistica:

```text
1. chiudere 0.8.2 → Simple Distribution Proof F08-020
2. integrare Semantic Entity 0.9 → core invariato
3. produrre seconda app da Domain Pack → prova N-settori
4. definire Workspace/ApplicationSpec → input machine-readable
5. CLI workspace create → fresh consumer repo
6. Foundation Bootstrap experiment → F0 produce F1
7. equivalence/fixed-point gate → decisione Foundation Next
```

Status bootstrap: APPROVED ARCHITECTURAL DIRECTION IMPLEMENTATION DEFERRED

### Link

- DECISION-0.8.2-RELEASE-TARGET-OWNER-APPROVED.md
- DIRECTIVE-ARENA-0.8.2-OWNER-DECISIONS-RECORDED.md
- EXPLANATION-0.8.2-CORE-ADMIN-PACKAGE-DISTRIBUTION.md
- IMPLICATIONS-0.8.2-SIMPLE-DISTRIBUTION-FACTORY.md
- STRATEGY-FOUNDATION-BOOTSTRAP-SELF-HOSTING.md
- DECISION-0.8.2-SIMPLE-DISTRIBUTION-PROOF-F08-020.md
- DECISION-0.8.2-RELEASE-STATEMENT-CANDIDATE.md

---

## Provenance finale

```
Tool: brain-collector.py + collect-epistemic-records.py + repeatability-test-24.py + scan-project-layout.py
Tool version: 0.1.0
Model_id: none (Classe 0)
Collected_at: 2026-10-09T19:35:00Z derivato
Source: 24-SCANSIONE-PER-CAPACITA.md SHA 582d4373807d + 37-LETTURA-OWNER-CORRETTA + 38-REGOLA + 39-WORKFLOW
Addendum 2026-10-11: context 5-8 Simple factory + bootstrap + moat + CLI workspace create + N-sectors + release statement candidate Foundation 0.8.2 consolida convergenza authority e sicurezza necessaria a produrre package Simple bounded riproducibile verificato in clean-room mantenendo espliciti e non distribuiti residual source non ancora migrati
Status: CANDIDATE → richiede owner approval → APPROVED → VERSIONED + addendum CANDIDATE
Promotion: explicit human approval required, no auto-canonical (PROHIBITED)
```

*Prodotto, non performance — da validare con pilot G. — con factory e bootstrap come moat candidato*
