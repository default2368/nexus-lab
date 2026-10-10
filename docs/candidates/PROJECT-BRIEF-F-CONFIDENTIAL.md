# Dalla documentazione al dossier governato
## Nota di progetto per confronto

**Open Nexus / Nexus Lab — denominazioni provvisorie**

Bozza riservata · ottobre 2026

---

## 1. Perché questo progetto

Molte attività professionali non soffrono per mancanza di documenti, ma per la difficoltà di ricostruire il rapporto fra attività, fonti, responsabilità e decisioni. Quando arriva il momento di rendere conto, le informazioni sono distribuite fra procedure, file, versioni, messaggi e persone.

Il progetto nasce dall'idea di rendere questa conoscenza attraversabile e verificabile, senza sostituire la decisione umana.

---

## 2. Cosa propone

### Navigabile

Documenti e attività collegati in un percorso comprensibile. Non una cartella di file, ma un dossier dove puoi seguire il filo fra procedura, attività, evidenza e decisione.

### Verificabile

Ogni affermazione importante può conservare fonte, versione e contesto. Puoi tornare dalla decisione alla fonte che l'ha motivata.

### Governabile

Review, approvazioni, eccezioni e responsabilità restano esplicite. Chi ha fatto cosa, su quale base, con quale evidenza, secondo quale versione, chi ha approvato.

Diagramma unico:

```text
fonti
→ record
→ evidenze e relazioni
→ review
→ dossier / applicazione
→ decisione
```

L'intelligenza artificiale viene usata per interpretare fonti e proporre collegamenti. Le fonti, le versioni, le verifiche e le decisioni restano esplicite. Il sistema non promuove automaticamente una risposta a verità o decisione.

---

## 3. Stato del progetto

| Disponibile | In sviluppo | Da validare |
|---|---|---|
| infrastruttura e contratti | acquisizione documenti | uso reale |
| package riproducibili | risposta con metadati epistemici | buyer |
| provenance e security gate | interfaccia per ispezionare risultati | willingness to pay |
| esperienza multi-app | dossier sintetico G. | secondo dominio |

Nota:

> Non esistono ancora clienti paganti o validazione commerciale. Esiste una base tecnica consistente e un primo percorso di verifica con professionisti di dominio.

---

## 4. Primo caso di prova e primi confronti

### G. — workflow operativo

Un professionista coinvolto in attività di audit e controllo ha contribuito a rendere più concreto il primo workflow candidato:

```text
procedura
→ attività
→ evidenza
→ feedback
→ azione
→ verifica
→ approvazione
→ chiusura
```

Non è una semplice raccolta documentale, ma una sequenza governata. Il valore non è soltanto conservare documenti, è mantenere il collegamento fra attività, evidenza, responsabilità e decisione.

Cosa resta da provare: G. non ha ancora utilizzato e corretto un dossier completo. Non esiste ancora un pilot operativo o commerciale.

### A. — ricostruzione di un'operazione

Un secondo confronto ha riguardato un caso diverso: ricostruire una specifica operazione, mostrando chi ha fatto cosa, quali contributi e documenti sono intervenuti e quale norma o versione fosse applicabile.

È emerso che alcune responsabilità adiacenti sono già coperte da strumenti esistenti:

```text
banche dati giuridiche → norme, interpretazioni, applicabilità
document management → raccolta e gestione documentale
```

Il possibile spazio distinto è stato descritto come una sorta di connettore che mette insieme molte informazioni relative a una cosa. Non un duplicato di strumenti esistenti, ma un layer che collega operazione, evidenze e responsabilità.

Cosa resta da provare: nessun pilot, nessuna partnership, nessun payer.

### Cosa sta emergendo

> I due confronti provengono da ambiti differenti, ma convergono su un elemento: il problema non sembra essere semplicemente trovare o conservare documenti. Il problema è ricostruire un'attività o una decisione mantenendo visibili fonti, contributi, responsabilità, versioni ed evidenze. Questa convergenza è un segnale da verificare, non ancora una validazione.

---

## 5. Piano di lavoro

Cinque work package:

```text
WP1  consolidare piattaforma e contratti
  obiettivo: chiudere base tecnica stabile e verificabile
  output: piattaforma stabile, package riproducibili, provenance
  gate: piattaforma stabile

WP2  acquisire e strutturare le fonti
  obiettivo: trasformare documenti in record con fonte e versione
  output: acquisizione documenti, record e relazioni
  gate: documento → record con fonte

WP3  costruire dossier ed esperienza utente
  obiettivo: rendere dossier navigabile e verificabile
  output: interfaccia per ispezionare risultati, evidenze e metadati
  gate: dossier sintetico

WP4  eseguire e correggere il pilot G.
  obiettivo: verificare il modello con un professionista di dominio
  output: dossier corretto, feedback strutturato
  gate: review G. — riconosce o corregge il processo

WP5  verificare secondo dominio e sostenibilità
  obiettivo: testare se infrastruttura resta comune cambiando dominio
  output: secondo caso applicativo, analisi sostenibilità
  gate: repeatability con secondo operatore + decisione sviluppo/pilot
```

---

## 6. Roadmap

```text
M1  piattaforma stabile
M2  documento → record
M3  dossier sintetico
M4  review G.
M5  repeatability con secondo operatore
M6  secondo dominio
M7  decisione di sviluppo / pilot / funding
```

---

## 7. Rischi e domande per F.

### Rischi

- complessità
- dati e access control
- assenza utenti
- mercato non validato
- eccesso di governance
- dipendenza dall'owner
- naming

### Domande

- La forma di progetto è leggibile?
- Chi sono beneficiario e soggetto attuatore?
- Gli output sono verificabili?
- Quale deliverable va mostrato per primo?
- Quali prerequisiti mancano?
- Che tipo di programma o strumento potrebbe ospitarlo?
- Dove stiamo confondendo ricerca, sviluppo e prodotto?

---

## Appendice tecnica opzionale — 2 pagine max (se vorrà approfondire)

Piattaforma: infrastruttura per produrre e verificare applicazioni di conoscenza in modo riproducibile, con contratti, gate e provenance.

Motore documentale: acquisizione con preservazione byte/hash, estrazione struttura, record e relazioni, claim con fonte.

Interfaccia: applicazione per navigare dossier, ispezionare evidenze, vedere gap e conflitti, correggere modello.

Strumenti operativi: workspace esportabile, receipt di verifica, report di divergenza.

Nota: denominazioni interne provvisorie, dettagli implementativi non rilevanti per valutazione progettuale.

---

*Bozza riservata · denominazioni provvisorie · nessun impegno richiesto · nessun dato cliente · nessuna attribuzione a stakeholder · nessuna pretesa di partnership*

---

## Nota personale separata (foglio a parte, scritta a mano o stampata semplice)

> F., te la lascio perché mi interessa il tuo occhio da progettista. Non è una richiesta di impegno: guardala quando vuoi e, se ti va, ne riparliamo davanti a un altro bicchiere.
