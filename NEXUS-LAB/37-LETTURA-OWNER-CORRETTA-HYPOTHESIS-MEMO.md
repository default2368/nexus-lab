# 37 — Lettura Owner Corretta — Hypothesis Memo (non validazione)

**Data:** 2026-10-09
**Correzione:** altro agent — VALIDATA usato troppo presto
**Stato:** CANDIDATE — HYPOTHESIS MEMO — APPROVED PRODUCT HYPOTHESIS, non market validated
**SHA sorgenti:** 582d4373807d (24), fa1615760c8e (35), 1c46e8c (audit finale)

---

## DECIDED (da altro agent, rispettato)

```text
Governed Evidence Dossier → APPROVED PRODUCT HYPOTHESIS
Cross-sector mechanism → APPROVED DIRECTION
Market validated → NO
Method repeatable → INTERNAL PROOF, external test pending
G. → first falsification pilot
One-pager → useful, if clearly marked hypothesis memo
New implementation branch → NO, not during 0.8.2
```

---

## Verdetto corretto

```text
Meccanismo tecnico              DIMOSTRATO IN PARTE
Ripetibilità interna            PROMETTENTE (3/4 match, M0)
Posizionamento funzionale       FORTE
Premio verticale                SEGNALE DI MERCATO (non prova causale)
Disponibilità a pagare          NON VALIDATA
Verticale G.                    IPOTESI PILOTA CONCRETA
Prodotto multi-settore          DIREZIONE ARCHITETTURALE
```

**Formula onesta:**
> Abbiamo un meccanismo tecnico promettente, un primo vertical workflow concreto e segnali economici coerenti. Ora dobbiamo vedere se un buyer reale riconosce valore nel dossier e nella governance.

Non: "Idea validata". Ma: "Ipotesi sufficientemente supportata per un pilot di falsificazione con G."

---

## Cosa regge (OSSERVATO)

### Il payer non compra generazione, compra:

- dossier verificabile
- responsabilità
- fonte / locator
- versione
- approvazione
- riproducibilità
- possibilità di difendere una decisione

Differenza reale rispetto a chatbot, document manager, generic app builder, scraping tool, reportistica manuale.

### Il verticale è funzionale, non settoriale

Non:
```text
software per pharma / rifiuti / PA
```

Ma:
```text
workflow in cui qualcuno deve rendere conto
→ di una decisione
→ sulla base di evidenze
→ dentro un processo governato
```

Coerente con: Infrastructure must be reusable; Domain must be replaceable.

### G. resta wedge corretto

```text
Procedure → questionnaire → response → evidence → feedback → action → verification → approval → closure
```

Sufficientemente concreto per testare meccanismo senza trasformare Open Nexus in "software soltanto per audit".

---

## Dove report precedente esagera (INFERITO corretto)

### 1. Sette inserzioni non validano mercato

Acquire.com è campione piccolo, selezionato, seller-reported, business differenti, non prova prezzo accettato, non prova causalità governance→multiplo.

Classificazione corretta:
```text
OBSERVED MARKET SIGNAL (non VALIDATED PRICING MODEL)
```
Range può guidare conversazione, non listino.

### 2. "Stesso prodotto, 1.500×" non dimostrato

B2C vs B2B differisce per servizio, sales motion, supporto, volume dati, frequenza, rischio, buyer, switching cost.

Conclusione difendibile:
> Il valore unitario osservato è molto più alto quando il payer compra un risultato operativo o governato invece di accesso individuale.

### 3. Visualping vs Particl non isola premio verticale

Differenziale può dipendere da data asset, volume monitorato, reporting, team workflow, supporto, frequenza, buyer budget.

Buon comparabile, non prova causale.

### 4. Repeatability 3/4 è ottimo test interno, non prodotto

Dimostra: un dossier può essere decomposto → rigenerato → conservando buona parte struttura.

Per metodo ripetibile servono:
1. secondo operatore che non ha visto originale
2. secondo dossier
3. corpus altra forma/lingua
4. negative control
5. confronto blind
6. failure criteria predefiniti
7. tempo/costo misurato

È M0, non validazione finale.

### 5. F08 non prova "nessun debito nascosto"

Prova entro scope: kernel drift osservato 0, protected symbols clean, surface findings classificati.

Restano noti: full-suite legacy red, F08-006 debt, debug/recovery surfaces, template migration, branch/document drift.

Frase corretta: Nessun drift del kernel osservato nel perimetro verificato.

### 6. Prometeo 11/14 vs Bolt 0/14

Bolt dimostra euristica sensibile a lingua, struttura, genere documentale, lessico. Buon refusal, ma anche finding su collector. Non prova generale che "metodo non inventa".

---

## PageData: direzione giusta, contratto non dimostrato

Esempio `claim-list` è buona candidate projection, ma non possiamo dire "già pronto per Template Lab".

Verificare prima:
- block contract esistente
- template consumer
- capability identity
- package membership
- source/provenance shape
- asset requirements
- PageData adapter
- no protected-kernel modification

Target corretto:
```text
ClaimRecord[] + MatrixProjection + Provenance → EntityViewArtifact / knowledge artifact → PageData Adapter → existing or approved template
```
Non inventare nuovi PageData block type senza contract gate.

---

## Modello prodotto che emerge — Governed Evidence Dossier / Istruttoria verificabile

### Input

- procedure
- contratti
- documenti
- questionari
- evidenze
- fonti pubbliche
- decisioni precedenti

### Output

```text
dossier versionato
├── claim
├── evidenze
├── fonte/locator
├── gap
├── conflitto
├── azione
├── approvazione
└── receipt
```

### Buyer

Non "chi vuole sapere qualcosa". Ma: chi deve prendere, approvare o difendere una decisione.

---

## Governance tiers — ipotesi, non pricing

```text
Tier 1 — Observe
dossier navigabile, fonti e locatori, read-only

Tier 2 — Compose
candidate records, matrici/proiezioni, revisioni

Tier 3 — Govern
approval, audit trail, policy gates, receipts, role-specific views
```

Premium Tier 3 è ipotesi da testare con buyer reali.

---

## Hypothesis Memo — one-pager owner corretto

### Tesi

> Open Nexus trasforma fonti documentali frammentate in dossier governati nei processi in cui qualcuno deve rendere conto di una decisione.

### Evidenza osservata (OBSERVED MARKET SIGNAL, non validazione)

- comparabili B2B/B2C: spread $0,25 vs $391 osservato su 7 inserzioni seller-reported
- differenziale horizontal/vertical: Visualping vs Particl comparabile, non prova causale
- repeatability internal proof: 3/4 match su dossier 24, M0
- Foundation distribution/provenance: content_sha + 304 + manifest
- Brain refusal/coverage: 11/14 Prometeo, 0/14 Bolt (finding su euristica)
- G. workflow: Procedure→questionnaire→...→closure concreto

### Ipotesi

```text
H1 buyer values traceability over generic generation
H2 governance supports a higher price tier
H3 same infrastructure supports a second domain
H4 dossier reduces reconstruction/review time
H5 non-technical expert can correct the model
```

### Falsificazione

```text
F1 G. does not recognize the workflow
F2 sources/claim links are not useful during review
F3 dossier production costs more than manual reconstruction
F4 second domain requires kernel changes
F5 buyer will not allocate budget for governance
F6 another operator cannot reproduce the dossier
```

### Pilot proof

```text
one real/sanitized workflow
one complete dossier
one correction session
one repeated run
one second operator
one willingness-to-pay conversation
```

### Metriche

- claim coverage
- percentage with source locator
- gaps/conflicts
- correction count
- review time
- regeneration parity
- source-to-decision traceability
- buyer budget/owner

---

## Cosa NON diciamo

- Idea validata → NO, ipotesi supportata per pilot
- Pricing model validato → NO, observed market signal
- Metodo repeatable → NO, internal proof M0, external test pending
- Nessun debito nascosto → NO, nessun drift kernel osservato nel perimetro verificato
- PageData pronto → NO, candidate projection, verifica contract gate
- Nuovo branch implementazione → NO, not during 0.8.2

---

## Provenance

```
Correzione: altro agent 2026-10-09 — "usa VALIDATA troppo presto"
Tool: repeatability-test-24.py + f08-audit.py + collect-epistemic-records.py
SHA: 582d4373807d (24), fa1615760c8e (35)
Stato: CANDIDATE — HYPOTHESIS MEMO
Promotion: richiede human review esplicita + pilot G. per falsificazione
```

*Segue 05-EVALUATION §9: marcatori, falsificazione, no punteggio confidenza, verdetto con condizioni*
