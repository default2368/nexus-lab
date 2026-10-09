# G — Audit Engagement Control

**Tipo:** Strategic Workflow / simulazione applicativa
**Interlocutore:** G. — audit conto terzi, GMP, project management
**Stato:** ipotesi da mostrare e falsificare
**Data:** 2026-09-20

> **Domanda guida:** questa esperienza diventa il posto da cui G. controlla il
> proprio lavoro, oppure aggiunge soltanto un altro posto da controllare?

---

## 0. Stato epistemico

### OSSERVATO

```text
· G. gestisce attualmente tre progetti in outsourcing
· gestisce inoltre un'attività Onlus con caratteristiche di ingegneria gestionale
· ha esperienza precedente in una multinazionale farmaceutica, anche sugli audit
· oggi lavora su audit conto terzi, GMP e project management
· opera attraverso società italiana, olandese e svizzera
· usa Notes e strumenti AI per tenere traccia e interpretare il proprio lavoro
· ha espresso il desiderio di avere "tutto sotto controllo"
· è disponibile a vedere qualcosa di interessante fra circa un mese
```

### INFERITO

```text
· procedure, schede operative, questionari e feedback sono collegati, ma non
  governati da un unico modello
· parte del controllo dipende dalla memoria e dall'ordine personale di G.
· il costo principale potrebbe essere cognitivo, non la perdita esplicita di dati
· le società di outsourcing potrebbero essere payer, canali o semplici committenti
· lo stesso modello potrebbe servire settori diversi dal farmaceutico
```

### LIMITI

```text
· non conosciamo gli strumenti ufficiali usati dalle società di audit
· non sappiamo quali dati G. possa mostrare senza NDA/DPA
· non conosciamo frequenza e costo delle attività manuali
· non sappiamo chi approverebbe o pagherebbe uno strumento
· non sappiamo se Notes + AI sia già sufficiente per G.
· non è stata effettuata un'intervista strutturata
```

---

## 1. Ipotesi di bisogno

> **Governare la trasformazione di procedure e conoscenza di alto livello in lavoro
> operativo, mantenendo la traccia di versioni, invii, risposte, feedback,
> classificazioni, decisioni e chiusure.**

Versione semplice:

> **Sapere sempre cosa è stato chiesto, a chi, in base a quale procedura, cosa è
> tornato indietro e cosa resta da chiudere.**

Il problema non viene formulato come:

```text
"serve un CRM"
"serve un sistema GMP"
"serve un altro project manager"
```

Il problema è la continuità fra conoscenza, lavoro, evidenza e decisione.

---

## 2. Confini della simulazione

### Incluso

```text
· quattro engagement sintetici
· procedure e versioni
· attività e schede operative
· questionari e risposte
· evidenze
· feedback e classificazioni
· azioni, owner e scadenze
· decisioni e approvazioni
· viste differenti per ruolo
· Roy read-only su dati strutturati
```

### Escluso

```text
· dati reali o identificabili
· documenti di clienti
· interpretazione normativa automatica
· decisioni GMP
· generazione automatica di finding
· sostituzione di QMS/eQMS/CRM/PM tool
· integrazioni con sistemi aziendali
· workflow multi-organizzazione reale
· pagamento, pricing o proposta commerciale
```

La simulazione usa esclusivamente dati fittizi e dichiarati tali.

---

## 3. Modello candidato

Queste entità sono applicative. Non entrano in Foundation senza una seconda
applicazione che confermi la stessa necessità.

```text
Engagement
├── Client / Organization
├── Scope
├── Role
├── ProcedureVersion
├── WorkItem
│   ├── owner
│   ├── dueDate
│   ├── status
│   └── dependencies
├── OperationalSheet
├── Questionnaire
│   ├── Question
│   └── Response
├── Evidence
├── Feedback
│   ├── classification
│   ├── severity
│   └── source
├── Action
├── Decision
├── Approval
└── Deliverable
```

Relazioni minime:

```text
ProcedureVersion  → derives       → OperationalSheet
OperationalSheet  → sent_to       → Organization / Role
Questionnaire     → collects      → Response
Response          → supported_by  → Evidence
Feedback          → refers_to     → Response / Deliverable
Feedback          → produces      → Action
Action            → owned_by      → Role
Decision          → based_on      → Evidence / Feedback
Approval          → closes        → Action / Deliverable
```

---

## 4. Workflow principale

```text
PROCEDURA DI ALTO LIVELLO
        ↓ versione applicabile
SCHEDA OPERATIVA
        ↓ assegnazione / invio
QUESTIONARIO
        ↓ compilazione
RISPOSTA + EVIDENZE
        ↓ revisione
FEEDBACK
        ↓ classificazione
AZIONE
        ↓ owner / scadenza
VERIFICA
        ↓ approvazione
CHIUSURA
        ↓
LESSON LEARNED / eventuale aggiornamento della procedura
```

Ogni passaggio conserva:

```text
source
version
actor
timestamp
status
relation to previous step
approval, se richiesta
```

---

## 5. Workflow secondari

### 5.1 Change Propagation

```text
nuova ProcedureVersion
        ↓
OperationalSheet derivate dalla versione precedente
Questionnaire ancora aperti
Feedback classificati col criterio precedente
Action da rivalutare
        ↓
review umana
```

Domanda verificata dalla vista:

> **Cosa devo rivedere se cambia questa procedura?**

### 5.2 Evidence Trace

```text
Decision / Finding
        ↓ based_on
Evidence
        ↓ originates_from
Response / Document
        ↓ governed_by
ProcedureVersion / Requirement
```

Domanda:

> **Da dove deriva questa decisione e quale versione era applicabile?**

### 5.3 Feedback Loop

```text
Feedback ricorrenti
        ↓ classificazione
pattern
        ↓ proposta
aggiornamento procedura / scheda / questionario
        ↓ approvazione
nuova versione
```

Il sistema propone il pattern. Un umano decide se modificare la conoscenza.

---

## 6. Le tre esperienze della simulazione

### 6.1 Control View — “ho tutto sotto controllo?”

Prima schermata.

```text
engagement attivi
attività bloccate
questionari in attesa
feedback non classificati
azioni scadute
approvazioni richieste
deliverable in scadenza
procedure cambiate con impatti aperti
```

Ogni numero è cliccabile fino ai record che lo producono.

### 6.2 Engagement View

```text
scope e ruoli
procedura applicabile
workflow corrente
timeline
schede e questionari
risposte ed evidenze
feedback
azioni
decisioni
deliverable
```

### 6.3 Client Evidence Portal

Vista limitata al singolo engagement e al ruolo autorizzato:

```text
questionari da completare
documenti richiesti
feedback ricevuti
azioni assegnate
scadenze
stato di chiusura
```

Stesso modello, proiezione differente. Nessuna visibilità cross-client.

---

## 7. Dataset sintetico

Quattro engagement, deliberatamente differenti:

```text
ENG-001  audit GMP
ENG-002  software validation project
ENG-003  audit / project in settore non pharma
ENG-004  attività gestionale Onlus
```

Dimensione massima:

```text
4 engagement
3 procedure versionate
12 work item
4 questionari
20 risposte
15 evidenze
10 feedback
8 azioni
4 decisioni
4 deliverable
```

Abbastanza per mostrare relazioni e differenze, non abbastanza per simulare un
prodotto completo.

---

## 8. Roy nella simulazione

Roy è read-only. Non decide conformità, gravità o chiusura.

Domande canary:

```text
1. Quali feedback non sono ancora classificati?
2. Quali attività sono bloccate da risposte mancanti?
3. Questa scheda deriva da quale versione della procedura?
4. Quali azioni sono scadute e da quale feedback derivano?
5. Cosa è cambiato dall'ultima review di ENG-002?
6. Quali evidenze supportano DEC-003?
```

Ogni risposta deve includere:

```text
record source
versione
timestamp
relazioni attraversate
limiti
```

Risposte vietate:

```text
"l'audit è conforme"
"devi emettere questo finding"
"questa CAPA è sufficiente"
```

---

## 9. Ciclo Foundation → X → Foundation

```text
FOUNDATION
  dataset strutturato + contratti + policy
        ↓
X
  interpreta domanda, propone relazione o sintesi
        ↓
FOUNDATION
  valida source, relazione, ruolo e output
        ↓
PageData
        ↓
Control / Engagement / Client Experience
```

Guardrail:

```text
· niente PageData scritta a mano per far apparire la demo migliore
· ogni passaggio manuale va marcato come debito del ciclo
· l'AI entra soltanto nell'interpretazione
· le metriche e gli stati sono deterministici
```

---

## 10. Piano di quattro settimane

### Settimana 1 — Modello e dati

```text
· schema applicativo minimo
· dataset sintetico
· regole deterministicamente calcolabili
· nessuna AI
```

### Settimana 2 — Experience

```text
· Control View
· Engagement View
· Client Evidence Portal
· navigazione fra entità e fonti
```

### Settimana 3 — Roy

```text
· indicizzazione dei record sintetici
· 6 domande canary
· citazioni e limiti
· test di leakage fra engagement
```

### Settimana 4 — Restituzione

```text
· pulizia UX
· nota di una pagina: osservato / inferito / non fa
· demo 10 minuti
· nessun pitch commerciale
```

---

## 11. Criteri di successo

La simulazione è utile se G.:

```text
1. riconosce il proprio modo di lavorare almeno nella struttura generale
2. corregge almeno una relazione o uno stato del modello
3. identifica una vista che oggi gli manca
4. ritiene che la Control View riduca il costo mentale del controllo
5. accetta di rivedere una seconda iterazione
```

La simulazione è falsificata se G.:

```text
· la percepisce come un altro posto da mantenere
· Notes + AI copre già il bisogno senza frizione significativa
· il modello è troppo generico per i suoi engagement
· le differenze fra settori richiedono workflow incompatibili
· nessuna vista cambia il suo comportamento o una decisione
```

Il successo non è “gli piace”. Il successo è che corregge il modello e riconosce un
costo ridotto.

---

## 12. Domande da fare soltanto dopo la demo

```text
1. Qual è la prima cosa che apriresti il lunedì mattina?
2. Quale elemento continueresti comunque a tenere in Notes?
3. Cosa manca perché questa vista rappresenti davvero il tuo lavoro?
4. A chi altro sarebbe utile: collega, società di audit, cliente finale?
5. Quale informazione non metteresti mai in un sistema del genere?
```

Nessuna domanda su prezzo, società o collaborazione nella prima restituzione.

---

## 13. Capability candidate al core

Solo se una seconda applicazione conferma:

```text
Evidence Contract
Temporal Validity
Approval Workflow
Feedback Classification
Decision Record
Content / Procedure → Operational Views
Cross-system Reconstruction
```

Restano nel pack G. finché la regola del due non è soddisfatta:

```text
GMP terminology
CAPA / deviation semantics
specific audit classifications
validation lifecycle
questionnaire templates
```

---

## 14. Punto di verità

> **Questa esperienza diventa il posto da cui G. controlla il lavoro, oppure aggiunge
> soltanto un altro posto da controllare?**

Tutto il resto — architettura, AI, mercato, possibili payer — viene dopo questa
risposta.
