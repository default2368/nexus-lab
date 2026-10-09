# MOAT — cosa è difendibile e cosa no

**Data:** 2026-09-13
**Chiude il cerchio:** la sessione è partita da *"sono molto geloso del lavoro fatto"*
e dalla paura del clone. Questo è il rendiconto.

---

## 1. Cosa NON è un moat

Tutto verificato nella sessione, non ipotizzato.

```text
IL CODICE
  "il PageAdapter sarebbe copiato in meno di una decina di giorni"
  → vero. Un normalizzatore è copiabile perché il suo contratto comportamentale
    è osservabile. Non serve il sorgente, serve l'I/O.

LE ASTRAZIONI / I LAYER
  → osservabili dall'API e dalla documentazione.
    Più sono eleganti, più sono facili da capire, quindi più sono copiabili.

LA MINIFICAZIONE / OFFUSCAMENTO
  codice leggibile    → 10 giorni
  codice minificato   → 10 giorni + 2 ore (beautify)
  codice offuscato    → 10 giorni + una settimana
  codice NON SPEDITO  → non copiabile
  → l'offuscamento compra ORE. Costa manutenzione e non protegge niente.

IL METODO SCRITTO
  → leggibile in un'ora. Trustable pubblica la propria doc di prodotto,
    ToolJet pubblica le proprie skill di processo. Non è lì il valore.

I DOCUMENTI
  → copiabili. 23 file si leggono in un pomeriggio.

LE FEATURE
  → ToolJet ha 80+ componenti e 90+ data source. Non è quello che li tiene in piedi.
```

---

## 2. Cosa È un moat

### M-01 · Invariante accumulata — `COSTRUITO`

```text
5 stratificazioni architetturali sopravvissute
pattern Astro+React tenuto attraverso tutte
suite di test vecchie ancora all'80%
refactor authority sulla source of truth senza regressioni
6 authority formalizzate (Application, Content, Domain, Design, Theme, Primitive)
boundary dichiarato per divieto
```

**Perché non è copiabile:** sono anni, non idee. Un clone può copiare la struttura
finale; non può copiare il fatto che ha retto. E la proprietà che la rende tale non
sta in nessun file: sta nell'**ordine** in cui sono stati scritti.

### M-02 · Governance eseguibile — `COSTRUITO`

```text
check-style-authority.mjs    regole come dato · scope derivato fails-closed ·
                             funzione pura · report/--json/--ci
exception registry           4 categorie · reason obbligatorio · scadenza
ADR-0012                     21 test verdi in 690 ms
parity test permanente       artifact-consumption-closure
baseline pubblicata          554 violazioni in 33 file, con target e regola
```

**Perché non è copiabile:** il codice sì, la disciplina no. Un clone può forkare lo
script; non forkare il fatto che qualcuno ha deciso che le eccezioni devono scadere.

### M-03 · Boundary compilato / degradation budget — `COSTRUITO`

```text
PRODUCE remoto/build-time  vs  EXECUTION locale/request-time
gli artifacts servono anche se cade il DB, l'API o il provider
local-first con ping Redis (NX-20)

confronto misurato:
  ToolJet   cade PostgreSQL → NULLA, le app SONO righe di DB
  Open Nexus cade PostgreSQL → gli artifacts compilati continuano a servire
```

**Perché non è copiabile:** richiede di non aver scelto l'interpretazione a runtime.
Loro non possono tornare indietro senza riscrivere il prodotto.

### M-04 · Residuo che compone — `CONDIZIONALE`

```text
ogni operazione di X lascia una traccia che migliora la successiva:
  quali fonti erano utili · quali riduzioni hanno prodotto score confermati
  quali classificazioni sono state corrette · dove il gate ha rifiutato e perché
```

**Stato: non esiste ancora.** Richiede utenti reali. È l'unico moat che **cresce da
solo**, ed è quello che AlphaSense (500M documenti in 15 anni) e Hebbia (1B pagine)
hanno e tu non hai.

**Si attiva con:** NX-24 (strumentazione) + NX-56 (pubblicare) + utenti.

### M-05 · Storia delle falsificazioni — `COSTRUITO, non trasferibile`

```text
4 ipotesi del revisore esterno falsificate dai file
1 scommessa sbagliata su un grep
1 authority proposta che esisteva già
1 giudizio dato sul bersaglio sbagliato e corretto
tutte registrate a verbale
```

**Perché è un moat:** un metodo che si è corretto da solo, con traccia, è credibile;
un metodo dichiarato non lo è. *"Zero risultati senza comando non è un dato"* applicato
a un prodotto venduto **è** il prodotto.

**Limite onesto:** vale solo se qualcuno la vede. È un asset di credibilità, non di
barriera. Diventa barriera quando è pubblico (NX-56).

### M-06 · Posizione normativa e geografica — `CONDIZIONALE`

```text
EU / PA italiana / settori regolamentati
residenza del dato · procurement che non può comprare SaaS USA
cloud EU come parte della promessa commerciale (Regolo.AI, Aruba, OVH)
```

**Perché non è copiabile con capitale:** AlphaSense, Hebbia e Rogo sono statunitensi
e non possono diventarlo. Non si compra: si sceglie.

**Si attiva con:** NX-30 (il verticale). Finché il verticale non è scelto, questo moat
non esiste.

---

## 3. Il rendiconto

```text
M-01  invariante accumulata          COSTRUITO
M-02  governance eseguibile          COSTRUITO
M-03  boundary compilato             COSTRUITO
M-05  storia delle falsificazioni    COSTRUITO (ma invisibile finché non pubblico)
M-04  residuo che compone            CONDIZIONALE — richiede utenti
M-06  posizione normativa            CONDIZIONALE — richiede il verticale
```

**Quattro costruiti, due condizionali.** E i due condizionali sono **gli unici due che
crescono senza il tuo lavoro**.

I quattro costruiti sono reali ma sono **necessari, non sufficienti**: rendono il
sistema solido, non rendono il sistema venduto. AlphaSense non ha nessuno dei quattro
e ha $350M e 500M di documenti.

Questa è la fotografia onesta, ed è la stessa di D-039 e D-042 letta da un altro lato:

```text
colonna "cosa ho costruito"      piena
colonna "chi lo usa"             vuota
```

---

## 4. Le tre mosse che attivano i moat condizionali

Non sono nuove. Sono quelle già a backlog, viste da qui.

```text
NX-56   portare le 4 analisi in PageData e pubblicarle
        → attiva M-05 (diventa visibile) e avvia M-04 (il corpus inizia a comporre)
        → costo marginale zero: gli artefatti esistono

NX-57   test di ripetibilità: un'analisi su oggetto nuovo, solo col metodo scritto
        → decide se M-01/M-02 sono un prodotto o una performance
        → costa un'analisi

NX-30   il verticale
        → attiva M-06, l'unico che il capitale dei concorrenti non può comprare
        → non richiede codice, richiede conversazioni
```

Tre mosse. Nessuna richiede architettura. Due su tre non richiedono codice.

---

## 5. In una frase

> **Il moat non è ciò che hai costruito. È ciò che hai costruito più ciò che il
> sistema impara usandosi — e la seconda parte non esiste ancora.**

oppure, nella forma che hai usato tu all'inizio della sessione:

```text
il PageAdapter si copia in dieci giorni
l'ordine in cui l'hai scritto no
e la storia di ciò che il sistema ha imparato su se stesso
non si copia affatto — ma prima deve averla
```

---

## 6. Riferimenti

```text
M-01  16-FOUNDATION-HEALTH § 2, 3, 6 · D-022, D-036
M-02  16-FOUNDATION-HEALTH § 4.1 · D-024, D-032, D-035
M-03  04-FOUNDATION-API § 3, 7 · D-017 · TOOLJET-benchmark § 3
M-04  13-X-MOAT § 1.3 · TOOLJET-benchmark § 5 · NX-24
M-05  01-DECISION-LOG nota di processo · 03-WORKFLOW § 4 · 20-... § 2.1
M-06  12-MERCATO-CONOSCENZA § 5 · 18-... § 2 · 08-COST-CULTURE § 7.7
```

---

*Ultimo aggiornamento: 2026-09-13*
