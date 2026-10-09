# G — Pilot Bootstrap: Open Nexus costruisce con Open Nexus

**Tipo:** Strategic Workflow / dogfooding strutturale
**Stato:** piano di verifica
**Data:** 2026-09-20
**Collegato a:** `G-AUDIT-ENGAGEMENT-CONTROL.md`

> **Open Nexus costruisce il pilot G. usando il linguaggio, le regole e gli strumenti
> di Open Nexus. La piattaforma verifica la coerenza; G. verifica la realtà.**

---

## 1. Scopo

Il pilot G. è contemporaneamente:

```text
· simulazione verticale sintetica
· test dell’Authoring Core
· test del Brain
· test dei ruleset epistemici
· esercizio Foundation → X → Foundation
· canary dell’architettura Open Nexus
```

Non dimostra da solo che esista un mercato. Dimostra che il ciclo tecnico e
conoscitivo può girare su un dominio non autoreferenziale.

---

## 2. Tre piani separati

### Platform Knowledge

```text
contratti
Authority
ruleset
capability catalog
schema PageData / AuthoringSpec
```

Owner: Open Nexus Contracts / Foundation.

### Application Knowledge

```text
engagement
procedure version
work item
questionnaire
response
evidence
feedback
action
decision
approval
deliverable
```

Owner: pack applicativo G. Nessuna entità entra automaticamente nel core.

### Run Knowledge

```text
cosa ha osservato il sistema
cosa ha proposto il Brain
cosa ha bloccato il gate
cosa è stato corretto manualmente
cosa ha falsificato G.
```

Owner: Brain Run / Evaluation Records.

**Regola:** la collocazione fisica nello stesso repository o database non trasferisce
ownership fra i tre piani.

---

## 3. Ciclo completo

```text
FOUNDATION
  dataset sintetico · contratti · policy
        ↓
X / BRAIN
  interpreta workflow · propone relazioni, viste e contenuto
        ↓
AUTHORING CORE
  costruisce AuthoringResult conforme
        ↓
FOUNDATION
  valida contratti, source, ruoli e output
        ↓
EXECUTION
  Control View · Engagement View · Client Evidence Portal
        ↓
OBSERVATION
  test · errori · debito manuale · reazioni di G.
        ↓
CANDIDATE KNOWLEDGE
  regole/capability candidate
        ↓
HUMAN / DOMAIN REVIEW
  accetta · corregge · rifiuta
```

---

## 4. Autorità delle decisioni

```text
Brain output          → candidate
Foundation gate       → conformant / non-conformant
G. feedback           → domain-valid / domain-invalid
Human decision        → accepted / rejected / defer
```

Vietato:

```text
Brain output → canonical
```

Open Nexus può verificare la conformità interna. G. verifica la corrispondenza al
mondo reale.

---

## 5. Versioni del pilot

### Pilot 0.1 — Internal Bootstrap

```text
dataset sintetico
modello applicativo candidato
PageData prodotta attraverso il ciclo
Roy read-only con canary
nessun feedback esterno
```

Dimostra:

```text
il ciclo gira
```

Non dimostra:

```text
il modello rappresenta il lavoro di G.
```

### Pilot 0.2 — Domain Review

G. vede la simulazione e corregge:

```text
entità
relazioni
ordine del workflow
stati
terminologia
viste
```

Dimostra:

```text
il modello può essere falsificato e corretto dal dominio
```

### Pilot 0.3 — Historical Anonymized Case

Un singolo incarico già chiuso, ridotto e anonimizzato, soltanto dopo accordi e
regole sul trattamento dei dati.

Dimostra:

```text
il modello attraversa materiale reale
```

Non usa automaticamente dati cliente né documenti riservati.

---

## 6. Guard contro il demo-driven development

La vista del pilot deve passare da:

```text
acquisition / dataset
→ reduction
→ interpretation
→ validation
→ PageData
→ renderer
```

Non da:

```text
PageData scritta a mano perché venga più bella
```

Ogni passaggio manuale va marcato:

```text
manual_step
reason
owner
removal_condition
```

Un passaggio manuale non invalida il pilot; invalida la pretesa che quel tratto del
ciclo sia automatizzato.

---

## 7. Cosa può autoalimentarsi

Il pilot può produrre:

```text
· failure mode dell’Authoring
· gap dei contratti
· regole candidate
· nuovi canary
· capability candidate
· pattern UI riutilizzabili
```

Promozione:

```text
finding del pilot
→ candidate rule/capability
→ secondo caso indipendente
→ test
→ authority review
→ eventuale promozione
```

Il fatto che il pilot usi una capability non è sufficiente per promuoverla.

---

## 8. Criteri di successo per versione

### 0.1

```text
□ ciclo Foundation → X → Foundation eseguito senza scrivere PageData a mano
□ ogni passaggio manuale marcato
□ 6 canary Roy con fonti corrette
□ nessun leakage fra engagement sintetici
□ artefatto riproducibile tramite record_set_sha
```

### 0.2

```text
□ G. riconosce il workflow generale
□ G. corregge almeno una relazione o stato
□ almeno una nostra ipotesi viene falsificata
□ nessuna correzione di dominio modifica Foundation direttamente
```

### 0.3

```text
□ autorizzazione e perimetro dati scritti
□ caso reale anonimizzato
□ catena source → evidence → decisione ricostruibile
□ valore e limite riconosciuti da G.
```

---

## 9. Falsificazione

Il pilot fallisce come applicazione se:

```text
· G. non riconosce la struttura
· Notes + AI copre il bisogno con minore costo
· il modello aggiunge manutenzione senza controllo
· i diversi engagement richiedono workflow incompatibili
```

Il pilot fallisce come test architetturale se:

```text
· richiede modifica opportunistica ai contratti protetti
· la PageData viene mantenuta manualmente
· Brain decide invece di proporre
· non è possibile riprodurre l’artefatto dagli input
```

Un fallimento applicativo può comunque produrre conoscenza architetturale. Un
fallimento architetturale invalida la pretesa end-to-end.

---

## 10. Punto di verità

```text
Open Nexus verifica:  “questa esperienza è conforme ai suoi contratti?”
G. verifica:           “questa esperienza rappresenta il mio lavoro?”
```

Servono entrambe le risposte.

---

*Formalizzato il 2026-09-20. Nessun dato reale di G. o dei suoi clienti è richiesto
per Pilot 0.1 e 0.2.*
