# Intervista G. — Audit conto terzi, GMP e Project Management

**Stato:** protocollo interno
**Durata:** 45–60 minuti
**Obiettivo:** capire un workflow reale di audit, dove si perde tempo, dove si perde
provenienza e chi pagherebbe per ridurre il problema.

**Non è:** un pitch, una demo, una richiesta di dati riservati o una proposta
commerciale.

---

## 0. Apertura

Formula suggerita:

> Sto cercando di capire il lavoro reale, non di proporti una soluzione. Non mi
> servono nomi di clienti, documenti o informazioni riservate. Mi interessa il
> processo: cosa entra, cosa devi dimostrare, cosa produci e dove perdi tempo.

Chiedere il permesso di prendere appunti. Non registrare audio senza consenso
esplicito.

---

## 1. Il caso concreto — prima di qualunque astrazione

### Domanda 1

> Raccontami l’ultimo audit conto terzi che puoi descrivere senza rivelare nulla di
> riservato: da quando ti è stato chiesto a quando è stato chiuso.

Lasciarlo parlare. Annotare:

```text
trigger
scope
standard / normativa
soggetti
fonti
fasi
output
approvazioni
follow-up
chiusura
```

### Domanda 2

> Qual era il risultato che il cliente si aspettava da te? Un report, una
> classificazione dei finding, un piano CAPA, un giudizio di readiness, altro?

Scopo: distinguere attività svolta da risultato acquistato.

---

## 2. La catena probatoria dell’audit

### Domanda 3

> Per formulare un finding, quali elementi devi poter collegare fra loro?

Non suggerire subito la risposta. Se serve, usare questo schema soltanto dopo:

```text
requisito / criterio
→ evidenza osservata
→ interpretazione
→ finding
→ gravità / classificazione
→ azione correttiva
→ owner
→ scadenza
→ verifica
→ chiusura
```

### Domanda 4

> Come dimostri, mesi dopo, da quali evidenze derivava un finding e quale versione
> della norma, procedura o SOP era applicabile in quel momento?

Scopo: verificare bisogno di provenance e validità temporale.

### Domanda 5

> Ti è mai capitato che una conclusione fosse ragionevole, ma difficile da sostenere
> documentalmente? Cosa mancava?

Scopo: trovare il confine fra analisi stocastica e prova difendibile.

---

## 3. Fonti, sistemi e frammentazione

### Domanda 6

> Quanti sistemi o formati devi normalmente attraversare per preparare e chiudere
> un audit?

Possibili esempi, soltanto se lui li nomina o chiede chiarimento:

```text
QMS / eQMS
DMS / SharePoint
ERP
LIMS
MES
email
Excel
PDF
SOP e documentazione cartacea
portali cliente
strumenti di project management
```

Per ogni fonte emersa, annotare:

```text
owner
formato
accesso
versione
frequenza
attendibilità
possibilità di export
```

### Domanda 7

> Quale parte del lavoro consiste nel cercare e ricomporre materiale, invece che nel
> giudizio professionale vero e proprio?

Chiedere, se possibile:

```text
ore/giorni per audit
percentuale indicativa del tempo
parte più ripetitiva
parte che non delegherebbe mai
```

---

## 4. Coerenza, riuso e qualità

### Domanda 8

> Come fate a mantenere coerenti finding simili fra clienti, auditor diversi e
> audit svolti in momenti diversi?

Scopo: verificare se esiste memoria organizzativa o se il metodo resta nella testa
dell’auditor.

### Domanda 9

> Quali elementi di un audit riusi nel successivo, e quali devi ricostruire ogni
> volta?

Cercare:

```text
checklist
criteri
pattern di finding
formulazioni
CAPA tipiche
lesson learned
risk ranking
```

### Domanda 10

> Quali errori sono più costosi: evidenza mancante, requisito interpretato male,
> versione documentale errata, follow-up dimenticato, finding incoerente, altro?

Scopo: ottenere il costo del problema, non un’opinione sulla tecnologia.

---

## 5. Project Management

### Domanda 11

> Nel project management, quali decisioni diventano difficili da ricostruire dopo
> settimane o mesi?

Cercare la catena:

```text
decisione
→ motivo
→ evidenza disponibile allora
→ owner
→ dipendenze
→ impatto
→ cambi successivi
```

### Domanda 12

> Quando cambia una condizione — normativa, tecnica, di budget o di pianificazione —
> come individuate deliverable, decisioni e attività impattate?

Questa domanda verifica lo stesso bisogno del grafo norma → contenuti, applicato al
project management.

---

## 6. AI già utilizzata

### Domanda 13

> Per quali attività usi oggi strumenti AI, e dove invece non ti fidi a usarli?

Annotare separatamente:

```text
ricerca
sintesi
confronto
bozza report
classificazione
traduzione
controllo coerenza
project planning
```

### Domanda 14

> Quando fai dialogare più strumenti, come conservi fonti, passaggi e motivazione
> della conclusione finale?

Scopo: verificare il valore di un record governato senza criticare il metodo attuale.

### Domanda 15 — neutra sulla convalida

> Se uno strumento legge soltanto sistemi validati, ma le sue elaborazioni vengono
> usate per una decisione di qualità, quali obblighi di convalida o controllo
> introdurrebbe?

Non anticipare “impatto minimo”. Lasciare che sia G. a definire il confine.

---

## 7. Domanda di valore

### Domanda 16

> Se potessi avere una sola vista che oggi non hai, quale vorresti?

Esempi soltanto dopo la risposta spontanea:

```text
evidence map di un audit
finding → evidenza → requisito
CAPA aging e recidive
versione normativa applicabile a una data
project decision ledger
mappa delle dipendenze impattate da un cambiamento
```

### Domanda 17

> Chi sentirebbe maggiormente il valore di quella vista e chi avrebbe il budget per
> richiederla?

Distinguere:

```text
utente
beneficiario
approvatore
payer
```

Non chiedere “quanto pagheresti?”. Chiedere chi paga oggi il lavoro manuale e quanto
tempo costa.

---

## 8. Possibile secondo incontro — non proporlo automaticamente

Soltanto se G. riconosce un dolore concreto e mostra interesse:

> Potremmo prendere un audit storico già chiuso e anonimizzato, senza dati reali
> identificabili, e ricostruire una sola catena requisito → evidenza → finding →
> azione → chiusura. Non per automatizzare il giudizio, ma per vedere dove oggi si
> perde la traccia. Ti interesserebbe rivedere il risultato?

Non chiedere una lettera di interesse nella prima conversazione.

---

## 9. Confini

```text
✗ nessun dato cliente durante il primo colloquio
✗ nessun documento riservato
✗ nessuna promessa di automazione GMP
✗ nessuna affermazione che read-only significhi automaticamente non-GxP
✗ nessun giudizio legale o regolatorio prodotto dal sistema
✗ nessuna richiesta di budget o partnership

✓ ascolto 70/30
✓ casi reali già chiusi e anonimizzati
✓ distinzione dato / interpretazione / decisione
✓ limiti dichiarati
✓ approvazione umana
```

Un NDA tutela la riservatezza, ma non sostituisce base giuridica, DPA,
minimizzazione e regole di conservazione quando entrano dati personali o aziendali.

---

## 10. Scheda post-intervista — compilare entro 24 ore

```text
Interlocutore: G.
Data:
Ruolo attuale:
Tipi di audit:
Tipi di progetto:

Caso descritto:
Trigger:
Risultato acquistato dal cliente:
Standard / normativa:

Fonti attraversate:
Sistemi:
Formati:
Numero indicativo:

Top 3 attività manuali:
1.
2.
3.

Tempo impiegato:
Costo dell’errore:
Parte non delegabile:

Catena probatoria attuale:
Dove si spezza:

AI utilizzata oggi:
Cosa funziona:
Cosa non è difendibile:

Vista desiderata:
Utente:
Approvatore:
Payer:

Perimetro sicuro per eventuale secondo incontro:
Disponibilità a rivedere un artefatto: sì / no / forse
Altri interlocutori suggeriti:

Claim OSSERVATI:
Inferenze nostre:
Limiti:

Esito:
  NO NEED
  NEED, NO ACCESS
  NEED, NO PAYER
  CANDIDATE PROBE
  DOMAIN PARTNER

Prossimo passo:
Data del prossimo passo:
```

---

## 11. Criterio di riuscita della conversazione

La conversazione è riuscita se produce almeno:

```text
1 workflow reale
1 catena probatoria
1 punto di rottura
1 costo in tempo/rischio
1 persona che approva
1 possibile payer oppure la prova che non esiste
```

Non è riuscita soltanto perché G. trova interessante Open Nexus.
