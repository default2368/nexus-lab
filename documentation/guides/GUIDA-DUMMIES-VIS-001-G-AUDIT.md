# VIS-001 e il pacchetto G. — Guida per non addetti ai lavori

**Scopo:** capire che cosa stiamo guardando nella pagina e nelle API del Semantic Proof.  
**Stato:** dimostrazione tecnica su dati sintetici; non è ancora un prodotto e non contiene dati reali di G.

---

## 1. Che cosa stiamo vedendo, in una frase

Stiamo vedendo un piccolo fascicolo di lavoro fittizio trasformato automaticamente in pagine navigabili.

```text
Dati del fascicolo
→ selezione delle informazioni appropriate
→ preparazione della vista
→ traduzione nel formato Open Nexus
→ API
→ pagina visibile
```

Il fascicolo si chiama:

```text
ENG-001 — Pilot Engagement
```

---

## 2. Che cos'è un Engagement

In questo contesto `Engagement` non significa coinvolgimento social.

È un incarico o progetto di lavoro, per esempio:

```text
Un cliente incarica G. di seguire un audit o un'attività GMP.
```

L'Engagement è il contenitore principale del lavoro:

```text
ENG-001
├── procedure utilizzate
├── evidenze raccolte
├── feedback prodotti
├── azioni da eseguire
└── decisioni prese
```

Analogia semplice:

> L'Engagement è il fascicolo principale di una pratica.

Nella fixture attuale:

```text
Titolo          Pilot Engagement
Stato           active
Rischio         42
Nota interna    Escalation pending
```

Sono dati sintetici creati soltanto per il test.

---

## 3. Che cosa sono gli oggetti collegati

### ProcedureVersion — `PV-001`

È una versione precisa di una procedura.

Non basta dire “la procedura”: in contesti regolati bisogna sapere quale versione era valida o utilizzata.

```text
PV-001
status: draft
```

Analogia:

> È l'edizione esatta del manuale o della SOP usata nel fascicolo.

### Evidence — `EV-001`

È una prova, un documento o un elemento che supporta ciò che viene dichiarato.

Nel test:

```text
EV-001
Access Control Policy
kind: document
```

Analogia:

> È un allegato del fascicolo che dimostra qualcosa.

### Feedback — `FB-001`

È un'osservazione, una risposta o un rilievo emerso durante il lavoro.

La fixture è ancora quasi vuota: ne dimostra soprattutto l'identità e il collegamento all'Engagement.

### Decision — `DEC-001`

È una decisione presa nel contesto dell'incarico.

Può rappresentare, per esempio:

```text
approvazione
rifiuto
richiesta di correzione
chiusura
```

Anche questa fixture è ancora minimale.

### Action

Nel Domain Pack G. esiste anche il concetto di azione, ma non compare fra le relazioni mostrate in questa schermata.

Un'Action rappresenterebbe il lavoro da eseguire dopo un feedback o una decisione.

---

## 4. “Sub-entità” in termini semplici

Procedure, Evidence, Feedback e Decision sembrano parti dell'Engagement, ma non sono semplici righe incorporate.

Sono oggetti con identità propria:

```text
ENG-001
EV-001
FB-001
DEC-001
```

Il loro collegamento è espresso da relazioni:

```text
ENG-001 --hasEvidence--> EV-001
```

Questo permette in futuro di:

- aprire l'Evidence separatamente;
- collegarla ad altri oggetti;
- conservarne la provenienza;
- aggiornarla o archiviarla senza riscrivere tutto l'Engagement;
- distinguere “rimuovi il collegamento” da “cancella l'Evidence”.

---

## 5. Che cosa significa Control View

La pagina mostrata nello screenshot è la vista interna:

```text
engagement.control
```

Contiene informazioni operative riservate al gestore del lavoro:

```text
riskScore
internalNotes
relazioni operative
action descriptor
```

Per questo vediamo:

```text
Risk             42
Internal notes   Escalation pending
Approve
Reject
```

Questa pagina deve diventare `PROTECTED`. Nel probe corrente risulta ancora `PUBLIC`: è un finding tecnico già individuato, non un comportamento da portare in produzione.

---

## 6. Che cosa significa Client View

La stessa entità `ENG-001` può essere guardata attraverso un altro profilo:

```text
engagement.client
```

L'obiettivo è mostrare soltanto ciò che il cliente può vedere.

```text
Stessa Entity
+ profilo differente
+ grant differente
= vista differente
```

La Client View non dovrebbe contenere:

```text
riskScore
internalNotes
action interne
```

Non vengono create due copie dell'Engagement. Vengono prodotte due rappresentazioni della stessa entità.

Analogia:

> È lo stesso fascicolo visto dall'ufficio interno e dal portale cliente.

---

## 7. Che cos'è un Profile

Un profile è una lente dichiarativa.

Esempi:

```text
engagement.control
engagement.client
evidence.detail
```

Il profile stabilisce:

- quali campi considerare;
- quali relazioni mostrare;
- quali azioni descrivere;
- in quale ordine presentare le sezioni.

Non modifica i dati originali.

---

## 8. Che cos'è un Artifact

L'`EntityViewArtifact` è il dossier preparato dal sistema prima di tradurlo in una pagina Open Nexus.

Esempio:

```text
Entity originale
ENG-001

+ profile
engagement.control

+ contesto autorizzato

= artifact
engagement/ENG-001/engagement-control
```

L'artifact contiene ancora informazioni semanticamente ricche:

- campi;
- relazioni;
- azioni dichiarate;
- contesto;
- provenienza;
- identità dell'entità e del profilo.

Non è ancora la pagina finale.

---

## 9. Che cos'è PageData

`PageData` è il formato che Open Nexus sa trasportare verso il Runtime e i template.

```text
EntityViewArtifact
↓
PageData Adapter
↓
PageData
↓
Template / Runtime
↓
Pagina
```

Nel payload vediamo:

```json
{
  "id": "engagement/ENG-001/engagement-control",
  "path": "/build/engagement/ENG-001/engagement-control",
  "title": "Pilot Engagement",
  "template": "VirtualPageTemplate"
}
```

L'idea centrale è:

> L'Artifact parla il linguaggio semantico; PageData parla il linguaggio delle esperienze Open Nexus.

---

## 10. Perché la risposta API contiene dati apparentemente duplicati

La risposta VIS-001 contiene più livelli contemporaneamente per rendere osservabile il test.

### `artifact`

È il risultato ricco della proiezione semantica.

### `pageData`

È la traduzione destinata alla Foundation.

### `fields`

È una proiezione semplificata usata dal visual probe per mostrare i campi in modo leggibile.

### `actionDescriptors`

Mostra le azioni dichiarate e specifica chiaramente:

```text
execution: not-implemented
```

Questa duplicazione è utile nel probe, ma non è necessariamente il contratto finale di produzione.

---

## 11. Che cosa rappresentano i riquadri della pagina

I riquadri:

```text
procedures
evidence
feedback
decisions
```

sono le relazioni dell'Engagement.

Nello screenshot il loro contenuto appare ancora come JSON grezzo, per esempio:

```text
[{"fields": {...}, "id": "EV-001", "type": "Evidence"}]
```

Questo significa:

```text
Il dato è arrivato correttamente.
La rappresentazione visuale non è ancora stata progettata.
```

Non è così che dovrà apparire il prodotto finale.

Una forma più leggibile potrebbe essere:

```text
Evidence
EV-001 · Access Control Policy · document
```

---

## 12. Che cosa significa “Evidence attraversabile”

Cliccando o aprendo l'Evidence, il sistema può produrre un'altra vista:

```text
ENG-001
→ EV-001
→ evidence.detail
→ /build/evidence/EV-001/evidence-detail
```

L'Evidence diventa quindi una pagina autonoma:

```text
Access Control Policy
Kind: document
```

Questo dimostra che la relazione non è soltanto testo decorativo: conduce a un'altra entità e a un'altra esperienza.

---

## 13. Approve e Reject funzionano?

No, e il sistema lo dichiara.

```json
{
  "id": "approve",
  "label": "Approve",
  "execution": "not-implemented"
}
```

Oggi sono `ActionDescriptor`:

```text
Il sistema sa che l'azione esiste.
Non la esegue ancora.
```

In futuro:

```text
click Approve
→ Domain Command
→ autorizzazione
→ validazione
→ modifica dell'EntityStore
→ nuova revisione
→ nuova proiezione
```

Non verrà modificata direttamente la PageData.

---

## 14. Che cosa è reale oggi

Nel probe è reale e funzionante:

```text
✓ caricamento della fixture sintetica
✓ risoluzione dell'Engagement
✓ attraversamento delle relazioni
✓ Control e Client artifact distinti
✓ PageData con ID e path distinti
✓ ordine delle sezioni definito dal profile
✓ API dedicate
✓ pagina visuale Control
✓ Evidence detail attraversabile
✓ azioni dichiarate come non implementate
```

---

## 15. Che cosa è ancora simulato o incompleto

```text
✗ dati reali di G.
✗ autenticazione e autorizzazione HTTP complete
✗ esecuzione di Approve/Reject
✗ storage persistente approvato
✗ collaborazione multiutente
✗ rendering leggibile delle relazioni
✗ rappresentazione completa di tutte le action in PageData
✗ conferma umana che le viste siano comprensibili e utili
```

LocalStorage, se introdotto nel prossimo Workbench, sarà usato esclusivamente per dati sintetici.

---

## 16. Il flusso completo, senza termini tecnici

```text
1. Abbiamo creato un fascicolo fittizio.
2. Abbiamo collegato procedure, documenti, feedback e decisioni.
3. Abbiamo scelto chi deve guardarlo: interno o cliente.
4. Il sistema ha selezionato le informazioni appropriate.
5. Ha preparato un dossier per quella vista.
6. Ha tradotto il dossier nel formato delle pagine Open Nexus.
7. Ha esposto il risultato attraverso API.
8. Una pagina lo ha mostrato sullo schermo.
9. Da quella pagina possiamo raggiungere un documento collegato.
```

---

## 17. Perché questo è importante

Prima avevamo una formula:

```text
Entities model knowledge.
Projectors produce artifacts.
Adapters materialize PageData.
Runtime renders experiences.
```

Ora ne vediamo un primo risultato concreto:

```text
Engagement
→ Control View
→ Client View
→ Evidence Detail
```

La pagina è ancora brutta e tecnica, ma dimostra che:

- una conoscenza di dominio può essere modellata;
- la stessa entità può produrre esperienze differenti;
- le relazioni possono essere attraversate;
- il Runtime non deve conoscere il dominio G.;
- il dominio può evolvere fuori dal kernel.

---

## 18. La domanda da fare a G., più avanti

Non:

> Ti piace questa interfaccia?

Ma:

> Questo fascicolo rappresenta correttamente come pensi a un incarico? Che cosa manca, che cosa è sbagliato e quali collegamenti non useresti mai?

Il successo del pilot non sarà una UI bella.

Sarà che G. riesca a riconoscere il proprio lavoro, correggere il modello e indicare dove il sistema sta mentendo o semplificando troppo.

---

## 19. Dalla root alla pagina: il viaggio completo dei dati

Questa sezione spiega come si passa da:

```text
ENG-001
```

alla pagina visibile nel browser.

### Passaggio 1 — Si sceglie una root

La root è il punto dal quale iniziamo a osservare la conoscenza.

Nel nostro caso:

```json
{
  "id": "ENG-001",
  "type": "Engagement",
  "namespace": "g-audit"
}
```

Significa:

> Parti dal fascicolo ENG-001 del dominio G. Audit.

La root non contiene necessariamente tutto. È l'indirizzo iniziale con cui chiediamo al provider di recuperare il fascicolo e ciò che gli è collegato.

---

### Passaggio 2 — Il provider recupera il record principale

Il `JsonEntityProvider` cerca l'`EntityRecord` corrispondente.

In forma semplificata:

```json
{
  "ref": {
    "id": "ENG-001",
    "type": "Engagement",
    "namespace": "g-audit"
  },
  "data": {
    "title": "Pilot Engagement",
    "status": "active",
    "riskScore": 42,
    "internalNotes": "Escalation pending"
  }
}
```

Questo è il dato del dominio, non ancora una pagina.

Il provider:

- recupera dati;
- non decide che cosa mostrare;
- non costruisce la UI;
- non autorizza l'utente;
- non modifica l'entità.

---

### Passaggio 3 — Il provider segue le relazioni esplicite

Nel dataset esistono record che collegano le entità.

Esempio semplificato:

```json
{
  "source": "ENG-001",
  "type": "hasEvidence",
  "target": "EV-001"
}
```

Significa:

```text
ENG-001 --hasEvidence--> EV-001
```

Il provider può seguire anche gli altri collegamenti:

```text
ENG-001 → PV-001   ProcedureVersion
ENG-001 → EV-001   Evidence
ENG-001 → FB-001   Feedback
ENG-001 → DEC-001  Decision
```

Non incorpora ricorsivamente gli oggetti uno dentro l'altro. Recupera record distinti e relazioni fra i loro ID.

---

### Passaggio 4 — Viene costruito un GraphSlice

Il risultato del recupero è una porzione limitata del grafo:

```text
EntityGraphSlice
```

Possiamo immaginarla così:

```text
Root
ENG-001

Entities disponibili
├── ENG-001
├── PV-001
├── EV-001
├── FB-001
└── DEC-001

Relationships
├── ENG-001 → PV-001
├── ENG-001 → EV-001
├── ENG-001 → FB-001
└── ENG-001 → DEC-001
```

Il GraphSlice è più ricco della pagina finale.

Può contenere:

- entità che il profilo non mostrerà;
- campi che l'utente non può vedere;
- relazioni escluse dalla vista;
- nodi disponibili per una successiva navigazione.

Questa è una proprietà importante:

```text
Provider ≠ Projection
```

Recuperare una conoscenza non significa automaticamente mostrarla.

---

### Passaggio 5 — Il selection gate controlla il profilo richiesto

Prima della proiezione viene verificato se il contesto può utilizzare il profilo richiesto.

Esempio:

```text
grant interno
+
engagement.control
→ consentito
```

```text
grant client
+
engagement.control
→ negato
```

Il gate non decide quali pixel mostrare. Decide se quella lente può essere utilizzata in quel contesto.

---

### Passaggio 6 — Il ProjectionContext fissa le condizioni

La stessa entità può apparire diversamente in base al contesto.

Il contesto contiene, per esempio:

```text
locale       en
timezone     UTC
asOf         2026-09-27
mode         view/preview/edit
grant        ciò che è consentito
policy id    decisione autorizzativa usata
```

`asOf` è importante perché in futuro una procedura o una relazione potrebbe essere valida in una data e non in un'altra.

---

### Passaggio 7 — Il profile sceglie la vista

Il profile è la lente applicata al GraphSlice.

Per la Control View:

```text
engagement.control
```

può chiedere:

```text
Campi
- title
- status
- riskScore
- internalNotes

Relazioni, in quest'ordine
- procedures
- evidence
- feedback
- decisions

Azioni dichiarate
- approve
- reject
```

La Client View usa invece:

```text
engagement.client
```

con meno campi e nessuna azione interna.

Il profile non crea nuovi dati. Seleziona e organizza ciò che è già presente e consentito.

---

### Passaggio 8 — Il Projector produce l'Artifact

Il `EntityProjector` combina:

```text
GraphSlice
+
Profile
+
ProjectionContext
```

per produrre:

```text
EntityViewArtifact
```

Nel payload VIS-001 vediamo:

```json
{
  "profileId": "engagement.control",
  "root": {
    "id": "ENG-001",
    "type": "Engagement"
  },
  "fields": {
    "title": "Pilot Engagement",
    "status": "active",
    "riskScore": 42,
    "internalNotes": "Escalation pending"
  },
  "relations": {
    "procedures": [],
    "evidence": [],
    "feedback": [],
    "decisions": []
  },
  "actions": [
    {"id": "approve"},
    {"id": "reject"}
  ]
}
```

Nel payload reale gli array non sono vuoti: contengono gli artifact proiettati delle entità collegate.

L'Artifact è ancora ricco e strutturato. Non è ancora `PageData`.

---

### Passaggio 9 — L'Adapter traduce l'Artifact in PageData

Il Runtime Open Nexus non conosce `Engagement`, `Evidence` o `Decision`.

Conosce `PageData`.

Perciò l'adapter traduce:

```text
EntityViewArtifact
↓
PageData
```

Il risultato contiene:

```text
id
path
title
template
policy
sections
cta
props
```

Esempio:

```json
{
  "id": "engagement/ENG-001/engagement-control",
  "path": "/build/engagement/ENG-001/engagement-control",
  "title": "Pilot Engagement",
  "template": "VirtualPageTemplate",
  "sections": [
    {
      "title": "evidence",
      "variant": "semantic-relation",
      "content": "[...]"
    }
  ]
}
```

In questo passaggio stiamo osservando un limite importante: le relazioni strutturate vengono attualmente inserite in `content` come JSON serializzato.

Il contenuto è corretto, ma la presentazione è ancora grezza.

---

### Passaggio 10 — L'API espone il risultato

L'API del probe restituisce più livelli insieme:

```text
artifact
pageData
fields
ActionDescriptor
metadata del probe
```

Questo non serve soltanto al frontend. Serve a noi per confrontare:

```text
Che cosa sapeva l'Artifact?
Che cosa è sopravvissuto in PageData?
Che cosa usa la pagina visuale?
Che cosa si è perso durante la traduzione?
```

L'indice VIS-001 fornisce gli endpoint già risolti. Il consumer usa `dataEndpoint` e non trasforma l'artifact ID in una URL.

---

### Passaggio 11 — La pagina visuale costruisce lo schermo

La pagina del probe riceve la risposta API e mostra:

```text
Header
→ ENG-001 — Control

Fields
→ title, status, riskScore, internalNotes

Relations
→ procedures, evidence, feedback, decisions

Actions
→ Approve, Reject — non implementate
```

Nello screenshot il JSON compare nei riquadri perché il renderer non possiede ancora una rappresentazione visuale specifica per `semantic-relation`.

Quindi:

```text
Dati corretti
+
traduzione tecnicamente valida
+
renderer ancora minimale
=
JSON grezzo visibile
```

---

### Passaggio 12 — Una relazione può diventare una nuova root

Quando apriamo `EV-001`, il sistema ripete lo stesso ciclo usando una nuova root:

```text
Prima root      ENG-001
Nuova root      EV-001
Profile         evidence.detail
```

Otteniamo:

```text
EV-001
Access Control Policy
Kind: document
```

Questa è la vera attraversabilità:

```text
Engagement
→ relazione hasEvidence
→ Evidence
→ nuova Projection
→ nuova PageData
→ nuova pagina
```

Non abbiamo copiato il documento dentro l'Engagement. Abbiamo seguito un riferimento verso un'altra entità.

---

## 20. Relazioni reali, disponibili e latenti

Qui è importante usare parole precise.

### Relazione reale o esplicita

È una relazione salvata nel dataset come `RelationshipRecord`.

Esempio:

```text
ENG-001 --hasEvidence--> EV-001
```

Il sistema può trattarla come fatto del dataset perché esiste un record che la dichiara.

### Relazione disponibile ma non proiettata

Può esistere nel GraphSlice ma non essere mostrata dal profile corrente.

Esempio concettuale:

```text
Questionnaire presente nel grafo
ma assente da engagement.control
```

Non è una relazione inventata o incerta. È reale nel dataset, ma latente rispetto alla vista corrente.

Formula:

```text
presente nella conoscenza
≠ presente in questa esperienza
```

### Relazione potenziale o inferita

È un collegamento plausibile che non possiede ancora un `RelationshipRecord` canonico.

Esempio:

```text
EV-001 potrebbe supportare DEC-001
```

Se il dataset non contiene:

```text
EV-001 --supports--> DEC-001
```

il sistema non deve presentarlo come fatto.

In futuro il Brain potrebbe proporre:

```text
Candidate Relationship:
EV-001 --supports--> DEC-001
```

con evidenza e motivazione.

Poi:

```text
Candidate Relationship
→ validazione
→ decisione umana
→ RelationshipRecord canonico
```

Soltanto dopo diventa una relazione reale per il sistema.

### Regola epistemica

```text
Explicit Relationship   fatto dichiarato nel dataset
Unprojected Relationship fatto non mostrato nella vista
Candidate Relationship  inferenza da validare
```

Non devono essere confusi.

---

## 21. Perché il JSON grezzo è utile adesso

Nel prodotto finale non vorremo mostrare JSON grezzo agli utenti.

In questa fase, però, funziona come un microscopio.

Ci permette di vedere:

- ID delle entità collegate;
- tipi delle entità;
- campi presenti e assenti;
- valori `null` introdotti dall'adapter;
- profile applicato ai child artifact;
- azioni propagate;
- ordine delle relazioni;
- informazione persa passando da Artifact a PageData.

Senza questo livello grezzo potremmo costruire una pagina gradevole che nasconde una traduzione sbagliata.

Per ora la sequenza corretta è:

```text
prima verificare che la conoscenza arrivi correttamente
poi stabilire il contratto visuale
infine rendere l'esperienza gradevole
```

---

## 22. Il flusso completo in una riga

```text
Root ENG-001
→ EntityProvider
→ EntityGraphSlice
→ Selection Gate
→ ProjectionContext
→ engagement.control
→ EntityProjector
→ EntityViewArtifact
→ PageData Adapter
→ API
→ pagina visuale
→ click EV-001
→ nuova root
→ evidence.detail
→ nuova pagina
```

Oppure, ancora più semplicemente:

> Partiamo da un fascicolo, recuperiamo ciò che gli è realmente collegato, applichiamo la lente autorizzata, traduciamo il risultato nel linguaggio delle pagine Open Nexus e rendiamo ogni collegamento attraversabile come una nuova esperienza.
