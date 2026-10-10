# Dalla documentazione al dossier governato
## Nota di progetto per confronto

**Open Nexus / Nexus Lab — denominazioni provvisorie**
Bozza riservata · ottobre 2026

---

### Pagina 1 — Il problema e la proposta

Molte attività professionali non soffrono per mancanza di documenti, ma per la difficoltà di ricostruire il rapporto fra attività, fonti, responsabilità e decisioni. Quando arriva il momento di rendere conto, le informazioni sono distribuite fra procedure, file, versioni, messaggi e persone.

Il progetto nasce dall'idea di rendere questa conoscenza attraversabile e verificabile, senza sostituire la decisione umana.

**Cosa propone**

**Navigabile** — Documenti e attività collegati in un percorso comprensibile.

**Verificabile** — Ogni affermazione importante può conservare fonte, versione e contesto.

**Governabile** — Revisioni, approvazioni, eccezioni e responsabilità restano esplicite.

```text
Fonti e procedure
        ↓
Record
        ↓
Evidenze e relazioni
        ↓
Revisione
        ↓
Dossier o applicazione
        ↓
Decisione
```

> L'intelligenza artificiale viene usata per interpretare fonti e proporre collegamenti. Le fonti, le versioni, le verifiche e le decisioni restano esplicite. Il sistema non promuove automaticamente una risposta a verità o decisione.

---

### Pagina 2 — Cosa significa concretamente

Questo esempio non rappresenta un cliente o un caso reale. Mostra il tipo di output che il primo pilot dovrà produrre e far correggere.

#### Dossier sintetico — Engagement ENG-001 (dati sintetici)

```text
Procedura
PROC-04 · versione 2.1

Attività
Verifica documentale del controllo C-07

Responsabile
Auditor

Evidenza richiesta
Documento di autorizzazione
Registro attività
Risposta al questionario

Evidenze ricevute
E-012 · autorizzazione
E-013 · registro
E-014 · risposta

Finding
F-003 · evidenza incompleta

Azione
A-007 · integrazione richiesta

Stato
IN VERIFICA

Decisione
Non ancora approvata
```

A lato:

```text
Fonte
Documento / versione / sezione

Provenienza
chi ha caricato
quando
hash

Stato di revisione
in verifica / approvato / respinto

Gap
manca evidenza E-015
```

Questa schermata fa capire in trenta secondi cosa significa "dossier governato".

---

### Pagina 3 — Cosa esiste e cosa manca

| Disponibile | In sviluppo | Da validare |
|---|---|---|
| infrastruttura e contratti | acquisizione dei documenti | uso reale |
| artefatti distribuibili | risposta con fonti e metadati | committente e sostenibilità |
| provenienza e controlli | interfaccia di ispezione | tempi di adozione |
| esperienza su più applicazioni | dossier sintetico per G. | secondo dominio |

> Non esistono ancora clienti paganti o validazione commerciale. Esiste una base tecnica consistente e un primo percorso di verifica con professionisti di dominio.

#### Come è stata preparata questa nota

Questa nota è stata redatta con il supporto di strumenti di intelligenza artificiale a partire dal materiale prodotto durante lo sviluppo: decisioni, piani, test, report, problemi e correzioni. L'AI ha aiutato a collegare e sintetizzare questi contenuti; la selezione delle affermazioni e la forma finale restano sottoposte a revisione umana. È un piccolo esempio dello stesso metodo proposto dal progetto: utilizzare ciò che è già documentato senza perderne origine, contesto e limiti.

---

### Pagina 4 — Primo caso di prova e primi confronti

#### G. — workflow operativo

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

Un professionista coinvolto in attività di audit e controllo ha contribuito a rendere più concreto il primo workflow candidato. Dal confronto è emerso che il valore non è soltanto conservare documenti, ma mantenere il collegamento fra attività, evidenza, responsabilità e decisione.

Cosa resta da provare: nessun dossier completo utilizzato e corretto, nessun pilot operativo o commerciale.

#### A. — ricostruzione di un'operazione

Un secondo confronto ha riguardato la ricostruzione di una specifica operazione: chi ha fatto cosa, quali contributi e documenti sono intervenuti e quale norma o versione fosse applicabile.

È emerso che alcune responsabilità sono già coperte da strumenti esistenti:

```text
banche dati giuridiche → norme, interpretazioni, applicabilità
gestione documentale → raccolta e gestione
```

Il possibile spazio distinto è stato descritto come un connettore che mette insieme molte informazioni relative a una cosa.

Cosa resta da provare: nessun pilot, nessuna partnership, nessun committente.

#### Cosa sta emergendo

> I due confronti provengono da ambiti differenti, ma convergono su un elemento: il problema non sembra essere semplicemente trovare o conservare documenti. Il problema è ricostruire un'attività o una decisione mantenendo visibili fonti, contributi, responsabilità, versioni ed evidenze. Questa convergenza è un segnale da verificare, non ancora una validazione.

---

### Pagina 5 — Piano di lavoro e domande per F.

**Piano**

```text
WP1  consolidare piattaforma e contratti
WP2  acquisire e strutturare le fonti
WP3  costruire dossier ed esperienza utente
WP4  eseguire e correggere il pilot G.
WP5  verificare secondo dominio e sostenibilità

M1  piattaforma stabile
M2  documento → record
M3  dossier sintetico
M4  review G.
M5  ripetibilità con secondo operatore
M6  secondo dominio
M7  decisione di sviluppo / pilot / finanziamento
```

**Rischi**

- complessità
- dati e controllo degli accessi
- assenza utenti
- mercato non validato
- eccesso di governance
- dipendenza dal promotore
- denominazione

**Domande per F.**

- La forma di progetto è leggibile?
- Chi sono beneficiario e soggetto attuatore?
- Gli output sono verificabili?
- Quale deliverable va mostrato per primo?
- Quali prerequisiti mancano?
- Che tipo di programma o strumento potrebbe ospitarlo?
- Dove stiamo confondendo ricerca, sviluppo e prodotto?

---

*Bozza riservata · denominazioni provvisorie · nessun impegno richiesto · nessun dato cliente · nessuna attribuzione a stakeholder · nessuna pretesa di partnership*
