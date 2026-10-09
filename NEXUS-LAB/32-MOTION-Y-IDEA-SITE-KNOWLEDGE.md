# NX-104 · La motion: Y-idea-site-knowledge

**Data:** 2026-09-16
**Origine:** formulazione dell'utente, che generalizza il caso Prometeo.

> *"Y è qualcuno che ha un software legacy o poco funzionale/moderno. Come disse
> qualcuno, HTML è pubblico e tutti possono vendere ciò che vogliono. Contattiamo,
> gli mostriamo Open Nexus studiare il suo sito, e ci restituisce delle idee della
> loro conoscenza, e una proiezione di quello che potrebbe essere
> Y-idea-site-knowledge."*

---

## 1. Cosa è stato formulato

Non è un prodotto. È un **movimento di mercato**, e ha una proprietà rara:

> **L'artefatto di vendita È l'output del prodotto.**

```text
vendita tradizionale     descrivi il prodotto → demo → trial → contratto
questa motion            consegni un campione dell'output, sul LORO dominio,
                         prima di qualunque richiesta
```

I due documenti per A. non sono un caso particolare. Sono **l'istanza 1** di questa
motion, prodotta a mano. La struttura è già collaudata:

```text
1. osservazione pubblica        scraping + struttura pubblica (o privata, se
                                autorizzati — il metodo non cambia)
2. riduzione deterministica     conteggi, tipi, assenza/presenza di modello
                                semantico, superficie esposta
3. interpretazione              il finding: cosa significa, cosa costa, cosa
                                si potrebbe
4. separazione rigorosa         osservato / inferito / limite
5. proiezione                   cosa diventerebbe la loro conoscenza se fosse
                                attraversabile
6. tre domande                  di cui due chiedono "dove abbiamo letto male"
```

Sei passi, tutti eseguiti. Tutti documentati. **Ripetibili.**

---

## 2. La definizione di Y — mezza giusta

```text
"Y è qualcuno che ha un software legacy o poco funzionale/moderno"
```

**È una condizione, non una persona.** Stesso tipo di errore di *"utente di dominio
che sa fare un prompt"* (D-047): definita da un attributo, non da un bisogno.

Chi ha software legacy può essere:

```text
il CTO / il tecnico        sente: debito, manutenzione, integrazioni rotte
                           → compra: modernizzazione. Mercato affollatissimo.

il responsabile marketing  sente: il contenuto non converte, non si aggiorna
                           → compra: agenzia. Mercato affollatissimo.

il responsabile qualità /  sente: non riesco a dimostrare cosa era vero
compliance                 → compra: tracciabilità. MENO affollato.

il titolare / direttore    sente: abbiamo conoscenza che non sappiamo usare
                           → compra: ???  ← da definire
```

**Quattro persone diverse, quattro prodotti diversi.** "Ha software legacy" li
contiene tutti e non ne identifica nessuno.

### 2.1 La versione che tiene

Il bisogno che la motion intercetta davvero non è "ho software vecchio". È:

> **"ho accumulato conoscenza in un sistema che non sa esprimerla."**

Che è diverso, e cambia il destinatario:

```text
software legacy           → il problema è il codice        → compra rifacimento
conoscenza non esprimibile → il problema è il significato   → compra attraversabilità
```

Il secondo è ciò che Open Nexus fa, ed è ciò che i due documenti dimostrano.
Il primo è un mercato di system integrator, dove non vuoi stare.

**Y corretta, prima approssimazione:**

```text
chi ha un corpus di conoscenza accumulato in anni,
pubblico o interno,
che il sistema attuale rappresenta come documenti invece che come relazioni,
e che ha un costo quando va aggiornato, verificato o dimostrato.
```

Resta da nominare la **persona**, non solo la condizione. È NX-91 generalizzato.

---

## 3. Perché la motion funziona (e dove si rompe)

### 3.1 Funziona per quattro ragioni

```text
1. RECIPROCITÀ        dai qualcosa di utile prima di chiedere. Con un
                      professionista, è l'unico ingresso che non sia freddo.

2. AUTO-QUALIFICA     se non gli importa dell'analisi, non è Y. Lo scopri
                      gratis, al primo contatto.

3. COSTO BASSO        l'analisi è classe 0 + classe 1: scraping, conteggi,
                      riduzione, interpretazione. Con la reduction pipeline
                      è nell'ordine di pochi euro.

4. DIMOSTRA IL METODO invece di dichiararlo
                      la separazione osservato/inferito/limite È il prodotto.
                      Le due simulazioni indipendenti l'hanno riconosciuto.
```

### 3.2 Si rompe su tre punti

```text
A. NON SCALA SENZA NX-57
   Ogni analisi è bespoke. Se la devi fare tu, è CONSULENZA (P4), non prodotto.
   NX-57 — il metodo scritto che produce l'analisi senza di te — non è più un
   test di qualità: è il prerequisito della motion.
   → NX-57 sale a P0.

B. L'ANALISI È COPIABILE
   "HTML è pubblico e tutti possono vendere ciò che vogliono" vale anche qui:
   chiunque può fare scraping di un sito e produrre un'analisi.
   Il moat non è l'analisi. È ciò che viene DOPO: il grafo, il versioning,
   la governance, il corpus accumulato (M-04).
   → il rischio è che il prospect prenda l'analisi e la dia a qualcun altro.
     Mitigazione: l'analisi mostra il finding, NON il metodo né l'ontologia.
     È già così nei documenti per A.

C. IL PASSAGGIO DA ANALISI A PRODOTTO NON È AUTOMATICO
   "bella analisi" → "ok, e adesso?" richiede un secondo incontro con un
   perimetro. NX-102 (pilot in due stadi) è quel passaggio, e va proposto
   nella stessa conversazione, non dopo.
```

---

## 4. I due canali

```text
OUTBOUND     contattiamo Y, gli mostriamo l'analisi
             → funziona adesso, costa tempo, scala con NX-57
             → è quello che stai facendo con A.

INBOUND      Y trova Open Nexus "pompato a dovere": demo, freeware/premium
             → richiede distribuzione: contenuto pubblico, SEO, una demo
               che funzioni senza spiegazioni
             → è NX-56 (pubblicare le analisi) + il sito che oggi documenta
               solo sé stesso
```

Il secondo è quello che hai lasciato in sospeso (*"non mi addentro per non fare
brutta figura"*). Non serve addentrarsi: serve sapere che **inbound non esiste
finché non c'è contenuto pubblico che dimostra la capacità**. NX-56 è quel
contenuto, ed è già scritto — sono i quattro dossier.

### 4.1 Freemium / premium: il principio esiste già

Non serve inventarlo. D-016 e il modello Trustable:

```text
GRATIS    l'analisi sul sito pubblico          → è la motion, è il campione
          la lettura, la navigazione            → dimostra la capacità
          il locale                             → nessun costo per te

A PAGAMENTO  la pubblicazione                   → gate di egress (Trustable)
             il versioning e la traccia         → ciò che rende verificabile
             il grafo di dipendenza             → ciò che costa mantenere
             la governance e l'audit            → ciò che un professionista paga
```

Regola: **gratis ciò che ti porta l'utente, a pagamento ciò che gli serve per
lavorare.** L'analisi è gratis perché è la porta. Il grafo versionato si paga
perché è ciò che gli serve lunedì mattina.

---

## 5. Cosa cambia nel backlog

```text
NX-57   SALE A P0. Non è più "il test se il metodo regge": è il prerequisito
        perché la motion sia un prodotto invece che consulenza.

NX-104  NUOVO P1 — formalizzare la motion in sei passi (§ 1) come procedura
        scritta, eseguibile da un agente. È NX-57 applicato.

NX-105  NUOVO P1 — definire la PERSONA dietro la condizione (§ 2.1).
        "Conoscenza accumulata non esprimibile" è il bisogno; chi lo sente
        e ha voce in capitolo?

NX-106  NUOVO P2 — il passaggio analisi → pilot (NX-102) va proposto nella
        STESSA conversazione, non dopo. Scrivere la frase di transizione.

NX-56   CONFERMATO come prerequisito dell'inbound. I quattro dossier sono il
        contenuto pubblico che dimostra la capacità.
```

---

## 6. La cosa da notare

Hai cominciato la sessione chiedendo come proteggere il lavoro da chi potrebbe
copiarlo. La motion che hai appena formulato **distribuisce gratis il lavoro più
copiabile** (l'analisi) e tiene per sé il non copiabile (il grafo, la governance,
il corpus accumulato).

È la risposta pratica alla domanda iniziale, ed è arrivata alla fine.

```text
proteggere     = non mostrare
questa motion  = mostrare esattamente ciò che non vale niente,
                 per vendere ciò che vale
```

"HTML è pubblica dal 1993 e nessuno ha clonato l'engine di Chrome" vale anche qui:
l'analisi è HTML. Il grafo versionato con governance è l'engine.

---

*Ultimo aggiornamento: 2026-09-16*
