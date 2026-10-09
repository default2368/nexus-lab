# NX-61 · Design della scansione di mercato per capacità

**Data:** 2026-09-14
**Origine:** scansione Acquire.com prodotta in altra sessione. Buona raccolta, ma
organizzata per **categoria di app**. Qui la riorganizziamo per **capacità di
Open Nexus**, che è la domanda reale.

---

## 1. Il numero che era già nei dati

Dalle inserzioni raccolte, due campi che nessuno ha diviso fra loro:

```text
prodotto                     utenti/clienti   ricavo/anno   ricavo per testa   multiplo chiesto
──────────────────────────────────────────────────────────────────────────────────────────────
job seeker B2C               72.000           $18.000       $0,25              2,8×  ricavo
fintech trading B2C          25.000           $25.000       $1,00              0,48× ricavo
job search/outplacement B2B  51–100 (~75)     $29.000       ~$387              1,55× ARR
text-to-SQL B2B              238              $45.000       $189               3,33× ARR
AI workflow automation       n/d              $4.000        n/d                1,9×  ricavo
AI photo portfolio B2C       n/d              $1.560.000    n/d                0,77× ricavo
                                                                                  3,4× profitto
```

### 1.1 Il contrasto

```text
B2C   $0,25 – $1,00   per utente per anno
B2B   $189 – $387     per cliente per anno

rapporto: da 190× a 1.500×
```

### 1.2 E la valutazione segue

```text
fintech B2C    25.000 utenti    → chiesto 0,48× il ricavo      ($12.000)
text-to-SQL    238 abbonati     → chiesto 3,33× l'ARR           ($150.000)

multiplo:      6,9× a favore dei 238 abbonati
valore assoluto: 12,5× a favore dei 238 abbonati
```

> **238 abbonati valgono più di 25.000 utenti.**
> Non un po': un ordine di grandezza sul multiplo, e oltre un ordine sul prezzo.

### 1.3 Avvertenze oneste

```text
· sono dichiarazioni del venditore, Acquire non fa due diligence
· sono 4-5 punti dati, non una statistica
· Acquire lista ciò che la gente vuole VENDERE → bias verso business piccoli,
  lifestyle o in difficoltà. Non mostra chi ha successo e non vende,
  né chi ha chiuso.
```

Ma il pattern è coerente su inserzioni indipendenti, e soprattutto **il bias è un
vantaggio qui**: Acquire mostra il pavimento del mercato, che è esattamente la
classe di riferimento di un fondatore singolo. Non è la mediana del mercato SaaS,
è la mediana del *tuo* mercato.

### 1.4 Conseguenza immediata sulle sonde

```text
Job Seeker verso il CANDIDATO     → mercato da $0,25/utente/anno
Job Seeker verso CAREER SERVICE   → mercato da $387/cliente/anno
                                    stesso prodotto, 1.500× di differenza
```

La sonda job-seeker non va scartata né promossa: va **mirata**. E il primo inserzione
(72.000 utenti, $18.000) è la dimostrazione empirica di cosa succede a mirare
l'utente invece del payer.

---

## 2. L'errore di impostazione della scansione

La scansione precedente ha cercato **applicazioni simili a quelle che potresti
costruire**. Ma Open Nexus non è un'applicazione: è un insieme di capacità
(`21-CAPACITA-OPENNEXUS.md`, C-01 → C-12).

```text
SBAGLIATO   "cosa c'è in vendita nella categoria job/finance/dev?"
            → produce un elenco di competitor di app che non hai deciso di fare

GIUSTO      "qualcuno guadagna da questa CAPACITÀ, in piccolo, e quanto chiede?"
            → produce il prezzo di mercato di ogni capacità di Open Nexus
```

La differenza pratica: la prima ti dice cosa costruire. La seconda ti dice **cosa
vale** ciò che sai già fare.

---

## 3. La matrice di ricerca per capacità

Ogni riga testa **una** affermazione su Open Nexus.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ C-01 · conoscenza navigabile                                                │
│ claim: "contenuto strutturato → viste multiple → esperienza pubblicabile"   │
│ cerca:  knowledge base · documentation platform · wiki · content platform   │
│         digital publishing · CMS · internal documentation                   │
│ risponde: il MODELLO ha compratori? a che prezzo?                           │
├────────────────────────────────────────────────────────────────────────────┤
│ doc-20 · analisi di mercato con evidenza                                    │
│ claim: "analisi comparativa per meccanismo e difendibilità, con traccia"     │
│ cerca:  market research · competitive intelligence · due diligence ·        │
│         research automation · report generation · analyst tool              │
│ risponde: la capacità del PILOTA ha mercato a scala piccola?                │
├────────────────────────────────────────────────────────────────────────────┤
│ M-02 · governance eseguibile                                                │
│ claim: "regole come dato, gate deterministici, eccezioni con scadenza"       │
│ cerca:  AI governance · compliance automation · audit trail · policy engine │
│         guardrails · AI risk · SOC2 automation                              │
│ risponde: la governance è vendibile o è solo costo interno?                 │
├────────────────────────────────────────────────────────────────────────────┤
│ M-06 · verticale normativo / PA                                             │
│ claim: "meccanismo > contenuto dove il dato è pubblico ma non navigabile"    │
│ cerca:  legal tech · regtech · regulatory compliance · public sector ·      │
│         government transparency · civic tech · freedom of information       │
│ risponde: esiste un payer piccolo nel verticale candidato?                  │
├────────────────────────────────────────────────────────────────────────────┤
│ C-07 · riduzione deterministica + connector                                 │
│ claim: "scraping → estrazione → score, zero token"                          │
│ cerca:  data extraction · web scraping · document processing · OCR ·        │
│         ETL · parsing API · enrichment                                      │
│ risponde: la reduction pipeline è vendibile come utility?                   │
├────────────────────────────────────────────────────────────────────────────┤
│ NX-01b · contract server / API                                              │
│ claim: "compila, valida, pubblica — il kernel non esce"                     │
│ cerca:  API · developer tool · SDK · infrastructure · white label ·         │
│         headless · build tool                                               │
│ risponde: il modello API/usage ha compratori a scala piccola?               │
├────────────────────────────────────────────────────────────────────────────┤
│ C-09/C-10 · authoring e workflow                                            │
│ claim: "bundle prodotto da agente, workflow con gate"                       │
│ cerca:  workflow automation · AI agent platform · no-code builder ·         │
│         code generation · low-code                                          │
│ risponde: è affollato? (sì, probabilmente — ma a che prezzo?)               │
└────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Priorità degli assi

```text
1. doc-20 (analisi di mercato)     ← è il PILOTA, e la scansione deve decidere
                                     se ha un payer
2. C-01 (conoscenza navigabile)    ← è la capacità più matura e meno esercitata
3. M-06 (verticale normativo)      ← è l'unico moat che il capitale non compra
4. C-07 (reduction/connector)      ← è la utility più stretta e più vendibile
5. M-02 (governance)               ← interessante, ma rischio "costo interno"
6. NX-01b, C-09/C-10               ← per capire l'affollamento, non per entrare
```

---

## 4. La matrice di registrazione

Quella proposta dall'altra sessione è buona. Tre campi mancano, e sono i tre che
discriminano.

```text
già previsti:  società/app · utente · payer · problema · input · output ·
               frequenza · prezzo · ricavi · canale · distribuzione ·
               asset difendibile · limite osservato ·
               capacità riutilizzabile in Open Nexus

DA AGGIUNGERE:
  ★ ricavo per utente / per cliente      ← il numero di § 1. Senza, non confronti.
  ★ multiplo chiesto / ARR o ricavo      ← quanto il mercato valuta QUEL modello
  ★ workflow o feature?                  ← "input → trasformazione → risultato →
                                            uso ricorrente" oppure punto singolo
  ★ capacità Open Nexus mappata           ← C-01..C-12, non testo libero
```

### 4.1 Regole di filtro

```text
1. registra SOLO inserzioni con ricavo dichiarato
   → senza ricavo è marketing, non dato
     (la financial literacy a $175.000 senza ricavi: scartata)

2. calcola SEMPRE ricavo/testa e multiplo
   → sono i due numeri confrontabili; il prezzo assoluto non lo è

3. marca la fonte come "dichiarazione del venditore"
   → mai come dato verificato

4. per ogni inserzione, una riga sola
   → se non riesci a riempire "capacità Open Nexus mappata", l'inserzione
     non è informativa per questa scansione

5. minimo 5 inserzioni per asse prima di trarre una conclusione
   → sotto i 5 è aneddoto
```

---

## 5. Cosa risponderebbe ogni esito

```text
SE sull'asse doc-20 trovi 3+ inserzioni con ricavo e multiplo > 2×
   → il pilota ha un mercato piccolo ma reale. NX-56/57 diventano P0 operativi.

SE sull'asse doc-20 non trovi niente con ricavo
   → la capacità è differenziata ma non monetizzabile a scala piccola.
     Resta interna (supporto a NX-30), non diventa prodotto.

SE sull'asse M-06 trovi payer piccoli (regtech, legal, civic)
   → il verticale candidato ha un pavimento. NX-30 ha una risposta parziale.

SE sull'asse C-01 trovi solo CMS/web builder a multipli bassi
   → conferma che "pubblicare contenuti" è commodity.
     Il valore sta nell'evidenza e nella governance, non nel publishing.

SE dovunque i multipli sono < 1×
   → il mercato delle micro-acquisizioni è depresso, e non dice niente
     sul valore delle capacità. Cambia fonte.
```

L'ultimo caso è importante: **una scansione che non discrimina va abbandonata, non
estesa.**

---

## 6. Fonti oltre Acquire

Acquire copre il pavimento (micro-acquisizioni, $7k–$175k). Per il quadro servono
altri due piani.

```text
PIANO 1 · pavimento — chi vende adesso
  Acquire.com · Flippa · Microns.io · Tiny Acquisitions
  → cosa: multipli reali, ricavo per testa, asset valorizzati
  → è ciò che hai già iniziato

PIANO 2 · mezzo — chi cresce
  Product Hunt (lanci) · Indie Hackers (revenue pubbliche)
  · GitHub trending per categoria · directory verticali
  → cosa: prezzi di listino, posizionamento, cosa viene copiato in fretta

PIANO 3 · soffitto — chi ha vinto
  i benchmark già fatti: AlphaSense · Hebbia · Rogo · Aiera · ToolJet ·
  Trustable · Instruqt
  → cosa: dove va il valore a scala, e quale moat lo regge
  → già fatto in 12-MERCATO-CONOSCENZA e TOOLJET-benchmark
```

**Il confronto utile è fra piano 1 e piano 3.** Se una capacità appare al piano 3 con
multipli enormi e al piano 1 non appare affatto, significa che richiede capitale.
Se appare al piano 1 con multipli decenti, è alla tua portata.

Esempio già nei dati: text-to-SQL al piano 1 sta a 238 abbonati e $45k ARR con
multiplo 3,3×. Al piano 3 ci sono giocatori finanziati. **Ma il piano 1 esiste** —
quindi è una capacità che si può monetizzare in piccolo. È il segnale che cerchi.

---

## 7. Il limite della scansione, da dichiarare

```text
Acquire mostra prodotti FINITI in vendita.
Non mostra:
  · chi ha chiuso (survivorship bias: i peggiori esiti spariscono)
  · chi non vende perché va bene
  · l'open source che ha azzerato il prezzo di una categoria
  · quanto tempo ci è voluto a raggiungere quel ricavo
```

Quindi la scansione risponde a **"quanto vale oggi un prodotto piccolo che funziona"**,
non a **"quanto è probabile che funzioni"**. Sono due domande diverse e la seconda
richiede le conversazioni di NX-30, non le inserzioni.

---

## 8. ESITO Asse 1 — analisi di mercato con evidenza (2026-09-14)

Scansione eseguita dall'utente in altra sessione. Campione di 7 inserzioni Acquire.

### 8.1 Il campione

```text
capacità                        ricavo      chiesto     multiplo  note dal titolo
──────────────────────────────────────────────────────────────────────────────────
B2B data & sales intelligence   $800.000    $2.472.630   3,09×    go-to-market teams
E-commerce product research     $35.000     $17.000      0,49×    "100% growth,
                                                                   profitable, turnkey"
Job search / outplacement       $29.351     $45.000      1,53×    51–100 clienti,
                                                                   30% growth
AI meeting reports              $33.492     $100.000     2,99×    1k utenti, profitable,
                                                                   83% growth
AI market insights              $11.213     $30.000      2,68×    trade signals
AI research/homework engine     $31.880     $30.000      0,94×    1M views, 96% margin
Text-to-SQL                     $49.800     $150.000     3,01×    238 sub, 88% margin
```

### 8.2 Tre numeri che il campione contiene e che vanno calcolati

**a) Ricavo per testa — i livelli sono tre, non due**

```text
homework engine      1.000.000 views    $31.880   →  $0,03 per view      TRAFFICO
meeting reports      1.000 utenti        $33.492   →  $33 per utente      PROSUMER
text-to-SQL          238 abbonati        $49.800   →  $209 per abbonato   B2B DEV
job/outplacement     ~75 clienti         $29.351   →  $391 per cliente    B2B
──────────────────────────────────────────────────────────────────────────
spread dal traffico al B2B: circa 12.000×
```

La scansione precedente aveva due livelli (B2C $0,25–1 / B2B $189–387). Il campione
nuovo ne aggiunge un terzo, intermedio: **prosumer a $33/utente**, che è dove sta
`meeting reports` con multiplo 2,99×. Non è B2C e non è B2B, ed è redditizio.

**b) Il multiplo misura DURABILITÀ, non dimensione**

```text
$800.000 di ricavo  → 3,09×
$11.213 di ricavo   → 2,68×     ← un settantesimo del ricavo, quasi lo stesso multiplo

$35.000 di ricavo   → 0,49×     ← "100% growth, profitable"
$11.213 di ricavo   → 2,68×     ← cinque volte più piccolo, cinque volte più multiplo
```

Il secondo confronto è quello che conta: **un prodotto più grande e dichiarato in
crescita al 100% vale un quinto del multiplo di uno cinque volte più piccolo.**

Cosa li distingue? Non il ricavo, non la crescita, non il margine. La parola nel
titolo: **"turnkey"** — il venditore segnala che consegna e se ne va. E la categoria:
e-commerce product research è presidiata da incumbent finanziati.

> **Il multiplo è il giudizio del mercato sulla difendibilità, letto direttamente.**
> Non serve un analista: è nel prezzo.

**c) La banda obiettivo per il pilota**

Il data point più vicino alla capacità di analisi di mercato è:

```text
AI market insights    $11.213 di ricavo · $30.000 richiesti · 2,68×
```

Il tetto del piano 1 nel campione è:

```text
Text-to-SQL           $49.800 ARR · 238 abbonati · 88% margine · $150.000 · 3,01×
```

Quindi, con evidenza:

```text
BANDA REALISTICA per una capacità di questo tipo, progetto singolo:
  ricavo        $11k – $50k / anno
  clienti       200 – 300 abbonati B2B, oppure ~1.000 prosumer
  multiplo      2,7× – 3,0×
  valore asset  $30k – $150k
```

**È la risposta alla domanda "cosa vale ciò che so fare"**, con numeri di mercato e
non con stime.

### 8.3 Il filtro che il campione suggerisce — e che non era previsto

`AI research/homework engine`: 1M views, **96% di margine**, e multiplo **0,94×**.

Perché un prodotto al 96% di margine vale meno del suo ricavo annuo?

```text
· il ricavo è da traffico, non da abbonamento → il flusso si ferma se ti fermi
· la domanda è soddisfatta gratis da ChatGPT
· le scuole stanno bloccando attivamente gli AI-homework tool
→ rischio esistenziale di piattaforma
```

Regola che ne discende, ed è la più utile dell'intera scansione:

> **Se un utente può ottenere l'80% del risultato incollando testo in un LLM
> generalista, il multiplo è sotto 1×.**
> Il margine alto non salva: il 96% di margine su un bene sostituibile vale zero.

Applicato alla capacità di analisi:

```text
si può ottenere l'80% incollando in ChatGPT?
  l'analisi singola              → SÌ, in gran parte
  la traccia di evidenza          → NO
  il corpus versionato e comparabile → NO
  l'aggiornamento quando l'oggetto cambia → NO
  la storia delle falsificazioni   → NO
```

**Il differenziatore è esattamente la parte che un LLM generalista non produce.**
Che è M-04 (residuo che compone). Il che significa una cosa precisa:

> per questa capacità, **il moat e il prodotto sono la stessa cosa**.
> Il corpus accumulato è ciò che si vende E ciò che difende.

### 8.4 Due proposizioni di valore, collassate in una

La formulazione proposta dall'utente è:

> *"Trasformare fonti eterogenee in un output operativo, verificabile e riutilizzabile."*

Corretta per tre data point su quattro, ma non per il migliore:

```text
A. "fonti eterogenee → output operativo"
   sales intelligence · meeting reports · market insights
   multipli: 3,09× · 2,99× · 2,68×

B. "elimina una competenza tecnica"
   text-to-SQL: non serve sapere SQL
   (e, nella scansione precedente, PDF API: non serve gestire infrastruttura)
   multipli: 3,01× · n/d
```

**B ha la migliore economia del campione:** 238 abbonati, $49.800 ARR, 88% margine,
3,01×, ed è la più vicina al differenziatore reale di Open Nexus — il **gate**.

```text
B applicata a Open Nexus:
  "non serve conoscere PageData, i contratti o il kernel per produrre
   un'applicazione valida: il gate li fa rispettare"
  → è NX-03 (VALIDATE) + NX-14 (nexus-mcp)
  → è il developer utility probe
```

**Avvertenza disciplinare: B ha n=1.** La regola § 4.1 punto 5 dice minimo 5 per asse.
Il segnale è forte ma non è ancora evidenza. **Non riordina le priorità da solo** —
va confermato prima.

### 8.5 Esito dell'asse

```text
L'asse 1 NON è vuoto.                          → confermato
Il payer tende a essere B2B.                     → confermato, con un terzo livello
                                                   prosumer a $33/utente e multiplo 3×
La banda di valore è $11k–$50k ARR, 2,7–3,0×.   → NUOVO, con evidenza
Il multiplo misura la difendibilità.             → NUOVO, leggibile dai prezzi
Il filtro "sostituibile da un LLM generalista".  → NUOVO, e discrimina le sonde
Due proposizioni di valore (A e B), non una.     → NUOVO, B da confermare con n≥5
```

### 8.6 Prossimo passo dell'asse — corretto

L'utente propone 5 inserzioni per ciascuna sottocapacità:
`research/report · enrichment/connector · knowledge-to-decision · analyst/developer utility`.

Giusto. Con due aggiunte derivanti da § 8.3 e § 8.4:

```text
1. per ogni inserzione registrare SE il risultato è ottenibile gratis da un LLM
   generalista. È il filtro che spiega i multipli sotto 1×.

2. la sottocapacità "analyst/developer utility" (= proposizione B) va portata a
   n≥5 PER PRIMA, perché è l'unica con il multiplo alto E la vicinanza al gate.
   Se regge, riordina le sonde.
```

---

## 9. I due mercati — e perché servono entrambe le scansioni

Correzione di rotta dell'utente (2026-09-14): *"dobbiamo cercare un marketplace non
di vendita SaaS, ma di vendita prodotto"*. Corretto, ma non è una sostituzione.

```text
BUSINESS MARKETPLACE                 PRODUCT MARKETPLACE
Acquire · Flippa · Microns           Envato/CodeCanyon · Gumroad · Lemon Squeezy
Tiny Acquisitions                    boilerplate indipendenti · AppSumo
                                     Astro Themes · Notion templates
──────────────────────────────────────────────────────────────────────────────
vende   ARR + clienti + brand        vende   un artefatto, senza clienti
prezzo  multiplo su ARR (1–4×)       prezzo  one-time $29 – $299
compra  chi vuole GESTIRE            compra  chi vuole COSTRUIRE CON
risponde "quanto vale un'APPLICAZIONE risponde "quanto vale il FRAMEWORK,
         costruita su Open Nexus?"             la CLI, l'engine?"
track   NX-49 (sonda)                track   NX-01 / NX-01b / NX-14
```

**Non sono sostituti: sono i due track che hai già.** La scansione Acquire non è stata
tempo perso — ha risposto alla domanda del track sonda (banda $11k–$50k ARR,
multiplo 2,7–3,0×). La scansione prodotto risponde all'altra.

E c'è una convergenza da notare: `opnx create app my-app` **è un boilerplate**.
Il mercato dei boilerplate è il comparabile diretto di NX-01, molto più di Acquire.

---

## 10. Design della scansione prodotto (NX-67)

### 10.1 Cosa cercare, in ordine di pertinenza

```text
1. BOILERPLATE / STARTER KIT              ← comparabile diretto di `opnx create app`
   ShipFast (Marc Lou, revenue pubblici) · MakerKit · Supastarter · Tailkit
   Cruip · Bulletproof React · Ultimate Courses
   cosa guardare: prezzo, volume dichiarato, cosa include, licenza

2. ASTRO / REACT THEMES                   ← il tuo stack esatto
   Astro Themes (directory ufficiale, sezione paid) · ThemeForest categoria Astro
   cosa guardare: prezzo tipico, quanti prodotti, recensioni come proxy di volume

3. FRAMEWORK / SDK CON LICENZA COMMERCIALE ← comparabile di NX-01 engine firmato
   CodeCanyon scripts · Tailwind UI · Refine (open core) · Filament
   cosa guardare: come si vende un framework che non è SaaS

4. TEMPLATE PER CONOSCENZA / DOCUMENTAZIONE ← comparabile di C-01 PageData
   Notion templates (Gumroad, Notionery) · documentation themes · Starlight
   cosa guardare: si paga per struttura di conoscenza, o solo per estetica?

5. MCP SERVER / AGENT TOOL A PAGAMENTO    ← comparabile di NX-14
   mercato molto nuovo, dati probabilmente scarsi
   cosa guardare: esiste un prezzo per un MCP server? anche solo 3 data point
                  direbbero qualcosa

6. APPSUMO LIFETIME DEAL per dev tool
   cosa guardare: volumi reali e perché il lifetime deal distrugge il ricorrente
```

### 10.2 Metriche — diverse da quelle di Acquire

```text
prezzo unitario                    one-time, subscription, tier
VOLUME STIMATO                     le recensioni sono il proxy: su Envato il
                                   tasso di recensione è basso, quindi
                                   recensioni × 20–30 ≈ vendite
piattaforma e SUA PERCENTUALE      ← la voce che cambia tutto, vedi § 10.3
licenza                            personal / commercial / extended / per-site
aggiornamenti inclusi?             determina se è prodotto o servizio
età del prodotto                   data di pubblicazione
affollamento della categoria       quanti prodotti simili → il multiplo qui
                                   non esiste, esiste la concorrenza di prezzo
```

### 10.3 La percentuale di piattaforma è una decisione di margine, non di distribuzione

```text
Envato / CodeCanyon     storicamente 30–62,5% a seconda dell'esclusività
Gumroad                 ~10% + fee di transazione
Lemon Squeezy / Paddle  merchant of record, ~5% + $0,50
AppSumo                 quota rilevante + prezzo lifetime, uccide il ricorrente
Vendita diretta Stripe  ~2,9% + $0,30
Trustable (riferimento) licenza offline firmata, vendita diretta, ZERO piattaforma
```

**Lo scarto fra Envato e vendita diretta è 3–6× sul netto.** È più grande di
qualunque decisione di prezzo. Quindi la scansione deve registrare la piattaforma
come variabile, non come dettaglio.

Nota di coerenza: il modello di licenza di Trustable (`lic_` firmato offline, host
allowlist, verifica senza license server) esiste precisamente per **vendere diretto
senza marketplace**. È il percorso a margine massimo, e richiede distribuzione propria.

### 10.4 Le tre domande a cui questa scansione risponde

```text
1. Un boilerplate/starter kit con contratti validati e CLI ha un prezzo?
   → se sì, NX-01 ha un modello di ricavo immediato, prima ancora di X

2. Si paga per la STRUTTURA di conoscenza o solo per l'estetica?
   → discrimina C-01: se il mercato paga solo temi, PageData non è vendibile
     come prodotto, solo come applicazione costruita sopra

3. Esiste un prezzo per un MCP server?
   → NX-14: se sì, è il canale a costo più basso. Se no, il MCP resta
     la porta d'ingresso gratuita e si monetizza altrove
```

La domanda 2 è la più importante delle tre, ed è quella che nessuna delle due
scansioni ha ancora toccato.

### 10.5 Avvertenza

Il mercato dei boilerplate ha una proprietà che Acquire non ha: **è pubblico e
saturabile in settimane.** ShipFast ha generato cloni entro mesi. Quindi:

```text
se la risposta alla domanda 1 è "sì, $199–299"
   → è un ricavo reale ma NON è un moat
   → vale come finanziamento, non come posizione
   → e va letto insieme a M-04: il moat resta il corpus accumulato,
     non l'artefatto venduto
```

---

## 11. Serie storica — l'unica versione del dataset che compone (NX-66)

Uno snapshot di inserzioni è una commodity: è pubblico, scade, e la 51esima
inserzione non vale più della 50esima.

```text
REGOLA
  Riscansionare le STESSE inserzioni a distanza e registrare l'esito.

CAMPI DA AGGIUNGERE a ogni inserzione già raccolta
  data_rilevazione (la prima: 2026-09-14)
  prezzo_richiesto
  esito                 venduta | ancora_listata | prezzo_scaduto | sparita
  prezzo_finale         se noto
  delta                 chiesto vs realizzato
  data_esito

RILETTURE
  dicembre 2026 · marzo 2027 · giugno 2027
```

**Perché vale:** il delta fra prezzo richiesto e prezzo di realizzo **non è pubblicato
da nessuna parte**, perché pubblicarlo distruggerebbe le aspettative dei venditori.
Chi lo raccoglie per due o tre trimestri ha un dato che nessun competitor ha, ottenuto
senza parlare con nessuno e senza spendere.

Ed è M-04 (residuo che compone) applicato alla ricerca di mercato invece che al
prodotto. Stessa regola: ogni osservazione lascia una traccia che rende migliore la
successiva.

Costo: cinque minuti adesso, dieci a trimestre.

---

## 12. Seconda passata — pricing e frizioni (2026-09-14)

Raccolta dell'utente: Visualping, Particl, Perplexity, BayesLab, GoMarble + frizioni
da G2. Qui l'analisi derivata.

### 12.1 Gli assi di pricing, tabulati

```text
Visualping      check · pagine · frequenza · utenti · integrazioni · API
                Free → Personal $14/mese → Business 20K $140/mese
Particl         competitor · profondità storica · utenti · export · API · benchmark
                $250 / $500 / $1.000 al mese
Perplexity      free → pro → enterprise (per seat)
BayesLab        crediti · task concorrenti · workspace · connettori
GoMarble        read-only vs READ-WRITE · approvazione modifiche ·
                connettori · AUDIT TRAIL
```

Frequenza con cui ciascun asse compare:

```text
volume (check/pagine/competitor/crediti/task)     4 su 5
connettori / integrazioni                          3 su 5
utenti / seat                                      2 su 5
API / export                                       2 su 5
frequenza / profondità storica                     2 su 5
GOVERNANCE (approvazione, audit, read-write)       1 su 5   ← GoMarble
```

**Il finding: la governance è un asse di pricing.** GoMarble fa pagare di più
l'agente **read-write con approvazione e audit trail** rispetto al read-only.

È M-02 (governance eseguibile) e NX-03 (gate VALIDATE) venduti come **livello di
piano**, non come feature. Finora nel progetto la governance era considerata costo
interno o moat difensivo. Il mercato la tratta come **unità vendibile**.

Conseguenza diretta:

```text
read-only   → l'agente propone, non tocca        → tier base
read-write  → l'agente modifica, con gate        → tier superiore
              + approvazione umana
              + audit trail
```

È esattamente la struttura che hai già: Proposta ≠ Decisione (D-037, metodo Sonda),
il gate deterministico (NX-53), la traccia verificabile (M-05). **Non va costruita:
va impacchettata come tier.**

### 12.2 Il premio di verticale, quantificato

```text
Visualping   ORIZZONTALE   qualunque sito, qualunque cambio     $14 – $140/mese
Particl      VERTICALE     retail/ecommerce intelligence        $250 – $1.000/mese
```

Stessa forma di capacità:

```text
sorgenti → rileva cambiamento → struttura → report
```

**Differenza di prezzo: da 7× a 70×.**

Caveat onesto: parte del premio di Particl è **dato proprietario** (POS, panel),
non solo verticalità. Ma la componente strutturale resta: la specificità di dominio
permette di prezzare sul valore della decisione, non sul costo del check.

È la risposta quantitativa a NX-30, e arriva dai listini pubblici:

> **il verticale vale da 7× a 70× l'orizzontale, a parità di pipeline.**

### 12.3 La chiusura: puoi vendere per-check solo se il check ti costa zero

Questa è la connessione fra la scansione e `07-PERSONA-AUTHORITIES-COSTO.md` § 2.

```text
IL MERCATO PREZZA SULLA FREQUENZA      check · pagine · competitor · crediti
L'OSSERVAZIONE CONTINUA È IL COSTO     "monitora" gira sempre, costo ∝ TEMPO
                                      → se passa da un LLM, è la rovina
```

Le due cose sono lo stesso asse visto dai due lati. Quindi:

```text
se il check è classe 0 (fetch + content_sha + score, deterministico)
   → costo marginale ~zero
   → PUOI prezzare per check con margine ~99%

se il check passa da un LLM
   → costo marginale proporzionale al volume venduto
   → il pricing per check ti mette in perdita all'aumentare dei clienti
```

**NX-19 ("nessun LLM nell'osservazione continua") non è un'ottimizzazione di costo.
È il prerequisito del modello di pricing che il mercato usa.**

Stima comparativa, da verificare ma strutturalmente solida:

```text
Visualping   costo per check = fetch headless + storage     margine forse 70–80%
Open Nexus    costo per check = fetch + hash + score          margine ~99%
             l'LLM scatta solo su soglia superata (una frazione dei check)
```

È un vantaggio di margine strutturale, e viene dalla reduction pipeline che hai già
in embrione nella CLI. Non è una feature: è la ragione per cui puoi permetterti di
prezzare come loro.

### 12.4 Le frizioni mappate sull'architettura

Le nove frizioni ricorrenti, contro ciò che esiste o è progettato:

```text
frizione                              risposta architetturale               stato
──────────────────────────────────────────────────────────────────────────────────
falsi alert                           trigger deterministico su score       NX-19
                                      + soglia dichiarata
dati inaccurati                       Source Authority + citazione fonte    C-01/D-023
valore non immediatamente             riduzione: mostra lo score,           C-07
  dimostrabile                        non il testo grezzo
copertura limitata                    Connector interface, pochi e profondi NX-27/28
setup complesso                       opnx create app · nexus init          NX-01
bundle troppo ampi rispetto           Primitive Authority: composizione     D-032
  al bisogno                          invece di pacchetto
limiti di utilizzo percepiti          classe 0 gratuita, si paga solo       § 12.3
  come artificiali                    l'interpretazione
──────────────────────────────────────────────────────────────────────────────────
curva di apprendimento                NESSUNA                               ✗
integrazioni insufficienti            scelta deliberata di NON copiare      ✗ (strategica)
                                      i 90 connettori di ToolJet
```

**Sette su nove hanno già una risposta progettata.** Non è fortuna: conferma quello
che hai detto tu, che le invarianti sono cicatrici di decisioni obbligate — cioè
costruite contro frizioni reali, non contro eleganza.

**Le due senza risposta sono le più serie.**

```text
CURVA DI APPRENDIMENTO
  Per la persona dichiarata (manager, CFO, broker) è la frizione letale.
  Un framework con contratti, gate e bundle HA una curva.
  È perché ToolJet ha il visual builder e Trustable ha i TUTORIAL integrati
  (tre, con spotlight in-place, citati in ogni pagina di doc).
  → nessuna delle 6 authority risolve questa. Serve un layer di onboarding
    che oggi non è nemmeno a backlog.

INTEGRAZIONI INSUFFICIENTI
  Hai deciso di non copiare i 90 connettori (TOOLJET-benchmark § 9.3).
  La decisione è giusta per il costo, ma la frizione è reale e il mercato
  la punisce nelle recensioni.
  → la risoluzione è "pochi e profondi NEL verticale scelto", che riporta
    a NX-30. Non è risolvibile in astratto.
```

### 12.5 Il pavimento che la scansione non ha visto

Manca il confronto con l'open source, che è ciò che fissa il prezzo minimo.

```text
per il monitoraggio orizzontale esiste changedetection.io
  (open source, self-hostable) → DA VERIFICARE, non confermato in questa sessione
  se esiste ed è mantenuto, il pavimento sotto Visualping è ZERO
```

Regola generale che ne segue:

> **Per ogni capacità ORIZZONTALE esiste un pavimento open source.**
> Per ogni capacità VERTICALE il pavimento non esiste, perché richiede
> conoscenza di dominio.

È un secondo argomento indipendente per il verticale, oltre al premio 7–70× di § 12.2.
E spiega perché "piattaforma generica di conoscenza" non monetizza: è orizzontale
per definizione, quindi ha il pavimento a zero.

---

## 13. Esito aggiornato

```text
CONFERMATO   la capacità ha mercato anche in piccolo
CONFERMATO   il payer è B2B (con livello intermedio prosumer)
NUOVO        la GOVERNANCE è un asse di pricing → impacchettabile come tier
NUOVO        il premio di verticale è 7–70×, misurato su listini pubblici
NUOVO        NX-19 è prerequisito del modello di pricing, non ottimizzazione
NUOVO        7 frizioni su 9 hanno già risposta progettata
NUOVO        2 frizioni non hanno risposta: curva di apprendimento (letale per
             la persona dichiarata) e integrazioni (scelta strategica)
NUOVO        ogni capacità orizzontale ha un pavimento open source a zero
```

Conclusione dell'utente, confermata e precisata:

> *"Il mercato paga una pipeline di conoscenza quando è legata a una frequenza,
> a un volume e a un'azione verificabile."*

Precisione aggiunta: **la frequenza è l'asse di prezzo E il rischio di costo.
Chi ha l'osservazione deterministica può venderla; chi ce l'ha via LLM no.**

---

## 14. Backlog

```text
NX-61  NUOVO P1 — scansione per capacità sui 4 assi prioritari
       (doc-20, C-01, M-06, C-07), minimo 5 inserzioni per asse,
       con matrice § 4 e regole di filtro § 4.1.
       È la versione corretta della scansione già iniziata.

NX-62  NUOVO P2 — estensione a piano 2 (Product Hunt, Indie Hackers)
       solo se il piano 1 discrimina.
       AGGIORNATO 2026-09-14: il piano 1 DISCRIMINA (§ 8). Sbloccato, ma resta
       dopo NX-63.

NX-63  NUOVO P1 — portare la sottocapacità "analyst/developer utility"
       (proposizione B, § 8.4) a n≥5. È l'unica con multiplo alto E vicinanza
       al gate VALIDATE. Se regge, riordina le sonde.

NX-64  NUOVO P1 — filtro di sostituibilità: per ogni inserzione e per ogni sonda,
       dichiarare se l'80% del risultato è ottenibile gratis da un LLM
       generalista. Se sì, il multiplo atteso è < 1× (§ 8.3).
       Va aggiunto alla matrice di registrazione § 4.

NX-65  NUOVO P2 — banda di valore di riferimento per il business plan:
       $11k–$50k ARR · 200–300 abbonati B2B o ~1.000 prosumer ·
       multiplo 2,7–3,0× · valore asset $30k–$150k (§ 8.2c).
       Da usare come sanity check su qualunque proiezione.

NX-66  NUOVO P1 — SERIE STORICA delle inserzioni già raccolte (§ 11).
       Campi: data_rilevazione · esito · prezzo_finale · delta.
       Riletture: dic 2026 · mar 2027 · giu 2027.
       È l'unica versione del dataset che compone. Costo: 5 minuti adesso.
       NOTA: se non si registra ORA, le 7 inserzioni dell'Asse 1 vanno perse
       e la serie non può iniziare.

NX-67  NUOVO P1 — SCANSIONE PRODUCT MARKETPLACE (§ 10).
       Sei categorie in ordine di pertinenza, metriche § 10.2,
       tre domande § 10.4. La domanda 2 ("si paga per la struttura di
       conoscenza o solo per l'estetica?") è la più importante e non è ancora
       stata toccata da nessuna scansione.
       Risponde al track NX-01/NX-14, non al track NX-49.

NX-68  NUOVO P2 — registrare la PIATTAFORMA di vendita come variabile di margine
       (§ 10.3). Lo scarto Envato vs vendita diretta è 3–6× sul netto:
       più grande di qualunque decisione di prezzo.

NX-69  NUOVO P1 — GOVERNANCE COME TIER DI PREZZO (§ 12.1).
       read-only (propone) vs read-write (modifica, con gate + approvazione
       + audit trail). Non va costruito: va impacchettato. Esiste già come
       Proposta≠Decisione (D-037) e NX-53.

NX-70  NUOVO P1 — ONBOARDING / curva di apprendimento (§ 12.4).
       È l'unica frizione letale per la persona dichiarata senza alcuna risposta
       architetturale. Le 6 authority non la risolvono. Riferimenti: i TUTORIAL
       in-place di Trustable, il visual builder di ToolJet.
       Oggi non è nemmeno a backlog.

NX-71  NUOVO P2 — verificare il pavimento open source per ogni capacità
       orizzontale candidata (§ 12.5). changedetection.io per il monitoring.
       Regola: se esiste un pavimento open source mantenuto, la capacità
       orizzontale non è monetizzabile in piccolo.

NX-72  NUOVO P2 — il premio di verticale 7–70× (§ 12.2) è evidenza quantitativa
       per NX-30. Da usare come argomento quando si sceglie il verticale.

AGGIORNAMENTO NX-49  la sonda job-seeker va MIRATA al payer B2B
       (career service / outplacement), non al candidato.
       Evidenza: $0,25/utente B2C vs $387/cliente B2B sullo stesso dominio.
```

---

*Ultimo aggiornamento: 2026-09-14*
