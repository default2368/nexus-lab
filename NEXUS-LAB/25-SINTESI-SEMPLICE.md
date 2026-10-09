# Nexus Lab in parole semplici

**A cosa serve questo file:** spiegare tutto a qualcuno che non sa niente.
Un collaboratore nuovo, un amico, te stesso fra sei mesi.
Niente sigle, niente codici, niente inglese dove si può evitare.

---

## Cos'è Open Nexus

Una macchina che trasforma **conoscenza** in pagine navigabili.

Tu descrivi il contenuto. La macchina produce le pagine, la navigazione, i permessi,
l'aspetto. Non scrivi il sito: dichiari cosa contiene.

La cosa importante è una sola: **c'è un confine netto fra chi prepara e chi serve.**

```text
CUCINA         prepara i piatti          → cambia spesso, può essere complessa
SALA           serve i piatti            → non sa come funziona la cucina
```

La sala non entra mai in cucina. Questo confine è la ragione per cui il sistema ha
retto cinque riscritture senza rompersi.

---

## Cosa abbiamo imparato in questa sessione

### 1. Nessuno fa esattamente questo, ma alcuni sono molto più grandi

Abbiamo guardato cinque realtà: due che costruiscono applicazioni con l'AI, una che
fa corsi pratici, quattro che vendono analisi a chi lavora nella finanza.

Nessuna ha il tuo confine cucina/sala. Ma quelle della finanza hanno centinaia di
milioni di finanziamento e clienti come Lazard e Rothschild.

**Loro hanno i clienti e i contenuti. Tu hai l'architettura.** Nessuno dei due
profili basta da solo.

### 2. Il rischio vero non è che ti copino

All'inizio la preoccupazione era: qualcuno copia il mio lavoro in dieci giorni.

Risposta onesta: il codice sì, si copia. L'ordine in cui l'hai scritto no.

**Il rischio vero è un altro:** continuare a perfezionare la macchina senza mai
scoprire se qualcuno vuole quello che produce.

### 3. Sei bravissimo a costruire. Non hai ancora prove che qualcuno paghi

Entrambe le cose sono vere, e vanno dette insieme.

```text
macchina           solida, verificata, cinque riscritture senza rotture
clienti            zero
conversazioni      zero
documenti scritti  ventiquattro
```

### 4. L'AI costa poco se fai una cosa sola: non mostrarle il materiale grezzo

Esempio. Devi controllare 50 fonti ogni 15 minuti.

```text
SBAGLIATO   dai all'AI il testo completo delle 50 fonti
            → circa 864 euro al mese

GIUSTO      un programma normale (gratis) legge le fonti e calcola dei numeri
            all'AI dai SOLO i numeri
            → circa 2 euro al mese
            → e se l'AI interviene solo quando un numero supera una soglia,
              circa 10 centesimi al mese
```

**La differenza non è quale AI usi. È quanti dati le fai vedere.**
Scegliere il modello economico fa risparmiare 4 volte. Ridurre i dati fa risparmiare
450 volte.

### 5. La privacy si protegge allo stesso modo

I dati sensibili restano sul tuo computer. All'AI arrivano **codici** al posto dei
nomi, delle cifre, delle date. Il programma che traduce codici in dati resta locale.

Due avvertenze importanti:

- funziona per compiti di **struttura** (chi ha fatto cosa, quando, in che ordine).
  Non funziona per compiti di **contenuto** ("questa clausola è rischiosa?") — per
  quelli serve leggere il testo, e quindi il testo deve uscire.
- per la legge europea, se conservi la tabella di traduzione **sono ancora dati
  personali**. Riduci il rischio, non elimini l'obbligo. Non scrivere "i dati non
  escono dal dispositivo": scrivi "il contenuto non esce, all'AI arrivano pseudonimi".

### 6. Si guadagna molto di più con uno strumento specializzato

Dai listini pubblici:

```text
strumento generico  "ti avviso se cambia una pagina web"      14 – 140 € al mese
strumento specializzato  "intelligence per chi vende al dettaglio"   250 – 1.000 € al mese
```

Stessa logica di funzionamento. Prezzo da **7 a 70 volte** più alto.

E c'è un secondo motivo: per ogni strumento generico esiste quasi sempre una versione
gratuita open source. Per uno specializzato no, perché serve conoscere il settore.

### 7. Puoi farti pagare per il controllo, non solo per il risultato

Un concorrente fa pagare di più la versione in cui l'AI **può modificare le cose**,
rispetto a quella in cui l'AI **può solo proporre**. Con approvazione umana e
registro di chi ha fatto cosa.

Tu questa struttura ce l'hai già. Non va costruita: **va messa in listino.**

### 8. Puoi vendere "a controlli" solo se ogni controllo ti costa zero

Il mercato fa pagare in base a quanti controlli fai, quante pagine sorvegli, quanti
documenti elabori.

Se ogni controllo passa dall'AI, più clienti hai più perdi soldi.
Se ogni controllo è fatto da un programma normale, il margine è quasi totale.

**È lo stesso punto del numero 4, visto dal lato del prezzo invece che dal lato del
costo.**

---

## Cosa sappiamo che non funziona

### Le cose che abbiamo scoperto sbagliate strada facendo

Quattro volte, in questa sessione, qualcuno ha affermato una cosa sul sistema e i
file hanno dimostrato il contrario. Ogni volta la correzione è stata scritta.

Questo conta, perché è la prova che il sistema risponde. **Un sistema che ti dà
sempre ragione non ti sta rispondendo.**

### Le due frizioni che non abbiamo risolto

Abbiamo confrontato i difetti di cui si lamentano gli utenti dei prodotti simili.
Sette su nove hanno già una risposta nel progetto. Due no:

```text
"è difficile da imparare"
   Per un direttore finanziario o un broker è la frizione che uccide il prodotto.
   Un sistema con contratti e regole HA una curva di apprendimento.
   I concorrenti la risolvono con tutorial dentro l'app e trascinamento visuale.
   Noi non abbiamo niente di simile, e non è nemmeno in elenco.

"si collega a poche cose"
   Abbiamo deciso di non costruire 90 collegamenti come fa un concorrente.
   Scelta giusta sui costi. Ma la lamentela è reale.
   Si risolve solo scegliendo il settore: pochi collegamenti, ma quelli giusti.
```

---

## Cosa fare, in ordine

### Oggi, due cose che non sono codice

```text
1. SPOSTA I FILE RISERVATI
   I documenti con la strategia sono sul cloud del tuo datore di lavoro.
   Regole altrui, e possibile ambiguità su di chi sia il lavoro.
   Mettili su un posto tuo. Verifica anche cosa prevede il tuo ente per le
   attività personali.

2. AGGIORNA IL NOME DEL MODELLO AI NEI TUOI STRUMENTI
   Il fornitore ha ritirato il nome vecchio il 10 settembre.
   I tuoi programmi puntano ancora a quello.
   Il rischio peggiore non è l'errore: è che funzioni comunque con un modello
   diverso, e il costo cambi senza che tu lo sappia.
```

### Questa settimana

```text
3. SALVA LE SETTE INSERZIONI CHE HAI TROVATO, CON LA DATA
   Fra tre mesi riguardale: vendute? ancora lì? prezzo abbassato?
   La differenza fra prezzo chiesto e prezzo ottenuto non la pubblica nessuno.
   Se non la registri adesso, non potrai più.

4. PUBBLICA LE QUATTRO ANALISI CHE HAI GIÀ SCRITTO
   Sono già fatte. Vanno solo messe come pagine sul sito, che già esiste.
   Servono a tre cose insieme: sono il tuo curriculum, sono la dimostrazione
   del prodotto, e sono l'inizio dell'archivio che nessuno può copiarti.

5. PROVA SE IL METODO FUNZIONA SENZA DI TE
   Fai fare un'analisi nuova usando solo le istruzioni scritte, senza intervenire.
   Se il risultato è buono, hai un prodotto. Se è mediocre, hai una tua abilità.
   Costa un'analisi. È la prova più economica e più importante di tutte.
```

### Poi

```text
6. SCEGLI IL SETTORE
   Non con un'opinione: guardando dove uno strumento specializzato viene pagato
   e dove i dati sono pubblici ma impossibili da attraversare.
   Pubblica amministrazione, giustizia, settori regolamentati sono i candidati.
   Lì conta la garanzia, non il contenuto — e la garanzia è ciò che hai.

7. PARLA CON UNA PERSONA
   Non dieci. Una.
   Chiedi: quanto ti costa oggi fare questa cosa, e cosa ti fa più rabbia del
   come la fai?
   È l'unica informazione che non puoi ottenere leggendo.
```

---

## La frase che riassume tutto

> **Il fossato non è quello che hai costruito.**
> **È quello che hai costruito più quello che il sistema impara usandosi.**
> **La prima parte è piena. La seconda non esiste ancora, e si riempie solo con
> persone che lo usano.**

E la versione operativa:

```text
la macchina funziona
il metodo funziona
i soldi sono pochi e si sa come tenerli pochi
manca una sola cosa: qualcuno che non sia tu
```

---

## Per orientarsi nei file

```text
se vuoi capire COSA È il progetto        → 00-INDICE.md
se vuoi capire COSA È STATO DECISO       → 01-DECISION-LOG.md
se vuoi capire COSA C'È DA FARE          → 02-BACKLOG-NX.md
se vuoi capire COME SI LAVORA qui        → 03-WORKFLOW.md
se vuoi capire SE REGGE                  → 16 e 17 (salute di Open Nexus e del Lab)
se vuoi capire COSA SI PUÒ VENDERE       → 24 (scansione di mercato)
se vuoi capire COSA CI DIFENDE           → 23 (il fossato)
```

---

*Scritto il 2026-09-14. Sintesi di 24 documenti, 72 voci di elenco, 45 decisioni.*
