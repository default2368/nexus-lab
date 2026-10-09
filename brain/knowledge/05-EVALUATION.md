# 05 — EVALUATION

**Perimetro:** regole di validazione dell'evidenza e delle conclusioni.
**Natura:** trascrizione di regole **già applicate** nel corpus 2026-09-10 → 2026-09-17.
Non è progettazione. Ogni regola ha un precedente con data.
**Valido per:** qualunque artefatto prodotto dal Brain — analisi, valutazione,
proposta, record.

**Convenzione di citazione.** Ogni regola è **autosufficiente**: si capisce e si
applica senza leggere altro. Ciò che segue la regola fra parentesi — `(D-040)`,
`(NX-57)`, una data — è **provenienza**, non dipendenza. Serve a contestare la
regola risalendo al caso che l'ha prodotta, non a comprenderla.

La risoluzione dei riferimenti sta in `RIFERIMENTI.md`, che **non viaggia con questo
file**: il corpus strategico non entra nel repo (D-014). Chi ha il corpus risolve;
chi non ce l'ha applica comunque le regole.

---

## 0. Il principio

> **Il prodotto non è la risposta. È il record.**

Una risposta si dimentica, non si verifica e non compone. Un record con marcatori,
fonti e limiti si contesta, si riusa e si accumula.

Corollario: un artefatto che non può essere falsificato non è un'analisi. È un'opinione
con una bibliografia.

---

## 1. I tre marcatori

```text
OSSERVATO    verificato su fonte, con riferimento alla fonte
INFERITO     interpretazione. Sempre marcato, mai fuso con l'osservato
LIMITE       ciò che non è stato possibile determinare
```

**Regole:**

```text
R1.1   nessuna affermazione fattuale senza marcatore
R1.2   nessun [OSSERVATO] senza riferimento (URL, file:riga, comando)
R1.3   le stime sono [INFERITO] e dichiarano la base
       precedente: "5% di 359 contenuti × 20 minuti = 6 ore — numeri nostri,
       non misurazioni" (2026-09-15)
R1.4   i limiti vanno in una sezione propria, non omessi
       precedente: 11 [LIMITE] nella nota per A.
```

**Vietato il punteggio numerico di confidenza.** Tre categorie, non 0,7.
Un numero finge una precisione che non esiste; una categoria è falsificabile.

---

## 2. Le cinque trasformazioni e cosa richiede ciascuna

```text
OBSERVATION   → EVIDENCE       → EVALUATION     → INTERPRETATION → PROPOSAL
cosa ho visto    cosa lo prova    quanto vale      cosa significa    cosa fare
```

| Trasformazione | Richiede | Produce | Non può produrre |
|---|---|---|---|
| Observation | fonte accessibile, comando eseguito | dato marcato OSSERVATO | giudizio |
| Evidence | riferimento verificabile da terzi | catena dato→fonte | conclusione |
| Evaluation | criterio dichiarato **prima** | punteggio su criterio | preferenza |
| Interpretation | distinzione esplicita dall'evidenza | ipotesi marcata INFERITO | fatto |
| Proposal | condizione di falsificazione | raccomandazione con condizioni | decisione |

**Regola di confine:** una trasformazione non può saltare. Un'interpretazione senza
valutazione è un gusto. Una proposta senza falsificazione è un desiderio.

---

## 3. Regole di acquisizione dell'evidenza

```text
R3.1   Ogni affermazione su cosa esiste cita il comando che l'ha prodotta.
       ZERO RISULTATI SENZA COMANDO NON È UN DATO.

R3.2   Una ricerca per NOME non prova l'assenza di un CONCETTO.
       Cerca i VALORI, o leggi il TYPE. Solo la lettura del type prova l'assenza.
       precedente: grep "applicationType|appType" → zero risultati; il concetto
       esisteva, dichiarato nel Bundle (2026-09-12)

R3.3   Un grep che restituisce zero richiede sanity check sul path.
       Altrimenti il falso negativo è indistinguibile dal vero negativo.

R3.4   Se un simbolo non esiste nel grafo, scrivi NOT FOUND.
       Non inferire, non indovinare percorsi, non citare codice non estratto.

R3.5   Sequenza MCP obbligatoria:
       index_status → search_graph → trace_path → get_code_snippet
       Mai: leggere directory intere, grep su tutto il codebase, aprire file
       da 500 righe per una funzione.

R3.6   Quattro `cat` valgono più di tutti i grep di una sessione.
       precedente: 2026-09-12, i quattro comandi che hanno risposto a Q-005
```

---

## 4. Regole di validazione

```text
R4.1   Il criterio di valutazione va dichiarato PRIMA di valutare.
       Altrimenti si seleziona il criterio che conferma.

R4.2   Minimo 5 punti dati prima di una conclusione. Sotto i 5 è aneddoto.
       precedente: § 4.1 regola 5, scansione per capacità

R4.3   Il verdetto non è binario.
       RECOMMENDATION: APPROVED WITH CONDITIONS | REJECTED | DEFER
       ACCEPTANCE CONDITIONS: <elenco numerato>

R4.4   Una review è read-only per costruzione.
       "NON modificare alcun file, NON creare file. Output = report."

R4.5   Le dichiarazioni del venditore si marcano come tali.
       precedente: "2.000+ installazioni → dichiarazione del fornitore,
       non verificata indipendentemente"

R4.6   Il prezzo di listino senza recensioni non è verifica commerciale.
       precedente: €125/utente/mese da Capterra, nessuna recensione mostrata
```

---

## 5. Regole di falsificazione

```text
R5.1   Ogni proposta ha una condizione di falsificazione scritta.
       Senza, non è un'ipotesi: è un'intenzione.

R5.2   Le condizioni di falsificazione si scrivono PRIMA dell'esecuzione.
       Dopo, si trova sempre una lettura che salva l'ipotesi.

R5.3   Una scansione che non discrimina va abbandonata, non estesa.
       precedente: "se dovunque i multipli sono < 1×, la fonte non dice niente"

R5.4   Il test di sostituibilità: se l'80% del risultato si ottiene gratis da
       un LLM generalista, il multiplo atteso è sotto 1×.
       precedente: homework engine, 1M views, 96% margine, multiplo 0,94×

R5.5   Il test del metodo: esegui la procedura senza l'operatore.
       Se il risultato è peggiore, il metodo è incompleto — non l'operatore
       è bravo. (NX-57)
```

---

## 6. Regole di promozione

```text
R6.1   Regola del due: una capacità entra nel core solo se serve ad almeno
       DUE applicazioni nominate. (D-040)

R6.2   Resta valida se il primo mercato fallisce? Se no, è applicativa.

R6.3   È un'invariante o una comodità locale?

R6.4   Riduce un costo reale per l'utente?

R6.5   È osservabile e verificabile?

R6.6   Può essere esposta via MCP?

Una capacità che non passa R6.1 resta nell'adattatore dell'applicazione.
```

---

## 7. Il passo 13 — contraddizione e coincidenza

**È il passo che produce il finding. Senza, un'analisi produce inventario.**

```text
per ogni sezione "opportunità" o "connessione":
   cerca nella sezione "osservato" se esiste già
   → se esiste, l'opportunità è COPERTA dall'incumbent

per ogni sezione "identità" o "posizionamento" del soggetto:
   cerca nel nostro backlog se esiste già
   → se esiste, è un CONCORRENTE, non un target

cerca due affermazioni che non stanno insieme,
o due affermazioni che sono la stessa cosa
```

**Precedenti, entrambi reali:**

```text
Prometeo   § 2.1 "alert su autorizzazioni scadute, limiti di giacenza,
           incongruenze"  vs  § 5 Opportunità A "quali autorizzazioni scadono?
           quali rifiuti prossimi al limite?"
           → la stessa cosa. Il documento lo dichiarava in due punti
             e non li collegava.

Draftbit   § 1-2 "builder visuale con agenti, template, publishing, MCP,
           Astro"  vs  nexus-builder "non ti chiediamo niente perché
           abbiamo già deciso"
           → lo stesso prodotto. Il documento descriveva e non concludeva.
```

In entrambi i casi il finding è arrivato dal lettore, non dal metodo. **R7 esiste
perché il lettore non sia necessario.**

---

## 8. Antipattern osservati

Casi reali della sessione. Sono la parte più utile del documento, perché un
antipattern con data è verificabile e uno senza data è morale.

```text
A1  Affermare prima di cercare
    quattro ipotesi di drift falsificate dai file: AF-001 come prerequisito
    commerciale · Graphic Authority come novità · scommessa su Q-005 ·
    D-027 "valore senza fonte dichiarata"

A2  Cercare nel modo che conferma
    grep sui nomi invece che sui valori (R3.2)

A3  Giudicare la forma invece dell'intento
    "Method Agent" letto come implementazione di un agente; l'intento era
    una capacità da vendere

A4  Chiudere prima dell'evidenza
    NX-30 chiuso tre volte su tre verticali diversi, ogni volta prematuro

A5  Inflazione di priorità
    26 P0 su 101 aperte. Regola: un P0 deve bloccare almeno un'altra voce.

A6  Inflazione di decisioni
    82 "DECISO" su 122 voci, di cui solo il 40% con alternativa scartata.
    Test: "cosa non possiamo più fare, adesso che è deciso?"

A7  Applicare un registro a un altro
    norme da documento B2B applicate a un messaggio fra persone con confidenza

A8  Informazione scaduta trattata come attuale
    "i documenti non sono stati inviati" ripetuto dopo l'invio

A9  Il corpus che cita sé stesso
    rapporto 8,6 : 1 fra riferimenti interni e riferimenti al mondo
```

---

## 9. Checklist per artefatto

Da eseguire prima di considerare chiuso un qualunque output del Brain.

```text
□ ogni affermazione fattuale ha un marcatore
□ ogni [OSSERVATO] ha un riferimento
□ ogni stima è [INFERITO] e dichiara la base
□ i limiti sono in una sezione propria
□ nessun punteggio numerico di confidenza
□ il criterio di valutazione era dichiarato prima
□ almeno 5 punti dati, o la conclusione è marcata come preliminare
□ il verdetto ha condizioni, non è binario
□ c'è una condizione di falsificazione scritta
□ il passo 13 è stato eseguito (contraddizione/coincidenza)
□ c'è una sezione "cosa NON proponiamo" o equivalente
□ le dichiarazioni di terzi sono marcate come tali
□ nessun antipattern di § 8
```

Tredici voci. Se un artefatto non le passa, non è pronto — indipendentemente da
quanto sia ben scritto.

---

## 10. Cosa questo documento non è

```text
· non è un'ontologia          → le entità si estraggono dopo NX-57, non si progettano
· non è un registro di capacità → le capacità reali sono 8-10, non 104
· non è un workflow            → i flussi vengono dopo le regole di validazione
· non è documentazione         → è un gate: o l'artefatto passa § 9, o non esce
```

---

*Trascritto il 2026-09-17 dal corpus 2026-09-10 → 2026-09-17.
Ogni regola ha un precedente. Le regole senza precedente non sono state incluse.*
