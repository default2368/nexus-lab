# NX-75 · Scoring delle istanze candidate

**Data:** 2026-09-14
**Scopo:** scegliere la prima istanza con criteri già scritti, non con preferenza.

**Nomenclatura confermata:**

```text
X          il layer governato da AI          (motore, resta APERTO per sempre)
AMBIENTE   il contesto di utilizzo           (turismo, civico, finanza, dev...)
ISTANZA    il prodotto concreto              (deve CHIUDERSI, una sola, adesso)
```

Regola: **il motore resta aperto, l'istanza si chiude.** D-040 richiede una prima
applicazione perché la regola del due possa scattare.

---

## 1. I criteri — tutti già stabiliti, nessuno inventato qui

```text
K1  Y = chi deve rendere conto?                     D-047
K2  sostituibilità: l'80% si ottiene gratis          NX-64 / § 8.3
    da un LLM generalista?
K3  frequenza: si può prezzare per-check             § 12.3
    a costo marginale ~zero?
K4  pavimento open source                            § 12.5
K5  premio di verticale (7–70×)                      § 12.2
K6  usa solo capacità VERIFICATE (C-01..C-08)?       D-043
K7  prototipo già esistente?                         doc 20 § 3
K8  conversazione accessibile questa settimana?      D-049
```

Punteggio: `✓✓` forte · `✓` sì · `~` parziale · `✗` no · `✗✗` no, aggravato.

---

## 2. La matrice

```text
                          K1   K2   K3   K4   K5   K6   K7   K8
─────────────────────────────────────────────────────────────────
A  pagina esperienza       ✗   ✗✗   ✗    ✗✗   ✗    ✓✓   ✓    ✓
   personale / portfolio
B  personal finance        ✗   ✗    ✓✓   ✗✗   ~    ✗    ✗    ✓
   tracker / cash flow
C  job-seeker lato          ✗   ✗✗   ~    ✗    ✗    ✓    ~    ✓
   candidato
C' job-seeker lato           ✓   ~    ~    ~    ✓    ✓    ✗    ~
   career service
D  developer validation     ✓   ~    ✓✓   ✗    ~    ✓✓   ~    ✓✓
E  analisi di mercato       ✓   ✓    ✓✓   ✓    ✓    ✓✓   ✓✓   ~
   con evidenza
─────────────────────────────────────────────────────────────────
```

### 2.1 Lettura riga per riga

**A · pagina esperienza personale**

```text
K1 ✗     nessuno deve rendere conto
K2 ✗✗    Wix · Carrd · Framer · Notion · GitHub Pages, e ChatGPT genera
         una landing page gratis
K4 ✗✗    centinaia di template Astro gratuiti; il pavimento è zero
K3 ✗     artefatto una-tantum, nessuna frequenza
K6 ✓✓    C-01 è live, è l'istanza più facile di tutte
```

**Verdetto: fattibilità massima, valore minimo.** È l'opzione di comfort.
Ma **non va scartata: va riclassificata.** Non è un prodotto, è l'infrastruttura
di pubblicazione che serve a NX-56. Va fatta, e va fatta come *mezzo*, non come
istanza.

**B · personal finance tracker / cash flow**

```text
K3 ✓✓    le transazioni sono frequenti e l'osservazione è deterministica:
         è il caso ideale per il pricing per-check
K4 ✗✗    Firefly III · Actual Budget · Maybe Finance · Ghostfolio
         → pavimento open source forte e mantenuto
K6 ✗     richiede un connettore bancario. In UE significa PSD2:
         o licenza, o un provider (Tink / TrueLayer / GoCardless) che costa
         per connessione. Non è classe 0.
K1 ✗     il titolare non deve rendere conto a nessuno
```

Più due aggravanti: è il dominio con più dati sensibili, quindi **NX-59 (tokenizzazione)
diventa prerequisito e non optional**; e la scansione precedente aveva già concluso
*"mostrare le spese non è una differenziazione sufficiente"*.

**Verdetto: attraente sulla frequenza, bloccato su pavimento, connettore e privacy.**
Tre blocchi indipendenti. Frizione troppo alta per una prima istanza.

**C / C' · job-seeker**

```text
C   lato candidato
    K1 ✗     il candidato non rende conto a nessuno
    K2 ✗✗    Teal · Rezi · Jobscan, e ChatGPT fa CV gratis
    evidenza dalla scansione: 72.000 utenti → $18.000 → $0,25/utente/anno

C'  lato career service / outplacement
    K1 ✓     deve giustificare il placement al committente
    K5 ✓     $391/cliente/anno, 1,53× — B2B reale
    K7 ✗     nessun prototipo
    K8 ~     richiede un ciclo di vendita verso HR / consulenti
```

**Verdetto: i dati hanno già risposto.** Il lato candidato è una trappola ($0,25/utente).
Il lato outplacement funziona ma richiede vendita B2B e non ha prototipo.

**D · developer validation utility**

```text
K1 ✓     il developer/CTO risponde di ciò che l'agente ha prodotto
K3 ✓✓    ogni build, ogni generazione → frequenza altissima, classe 0
K6 ✓✓    il gate esiste già: check-style-authority.mjs dimostra il pattern
K8 ✓✓    lui È l'utente, e i developer sono raggiungibili
K4 ✗     ESLint e validatori vari. Ma "validare output di agente contro
         un contratto" è più sottile e meno presidiato
K2 ~     un LLM può validare? sì, ma non in modo riproducibile — e la
         riproducibilità è il prodotto
```

**Verdetto: miglior aderenza strutturale** (frequenza + responsabilità + gate già
esistente) **ma massima esposizione competitiva**: i tool di AI coding stanno
aggiungendo validazione nativa, e i developer sono i compratori più capaci di
farselo da soli.

**E · analisi di mercato con evidenza**

```text
K1 ✓     analista, VC, CTO in build-vs-buy devono difendere la conclusione
K2 ✓     l'analisi singola è sostituibile; il corpus versionato con traccia
         di evidenza NO (§ 8.3 — verificato)
K3 ✓✓    monitorare piattaforme/competitor è per-check, classe 0
K4 ✓     non esiste un open source per "intelligence comparativa con
         traccia falsificabile"
K5 ✓     competitive intelligence è verticale: Particl $250–1.000/mese
K6 ✓✓    C-01 · C-04 · C-07 · C-08, nessuna capacità teorica
K7 ✓✓    IL PROTOTIPO ESISTE: quattro dossier già scritti
K8 ~     pubblicando si vede chi risponde
```

**Verdetto: punteggio più alto, ed è l'unica con prototipo esistente.**

---

## 3. Il bias dell'assistente, dichiarato

**E è ciò che ho proposto io in doc 20 e doc 24.** Ho un interesse nella risposta e
va dichiarato, perché in questa sessione ho chiuso prematuramente cinque volte.

Il rischio specifico su E è quello di doc 13 § 3.5: **è comoda.** Analizzare
piattaforme è ciò che all'utente piace fare, ed è auto-riferito.

Ma la distinzione che salva o condanna E è una sola:

```text
E come RICERCA INTERNA    → trappola di comfort. Parli di piattaforme
                            a chi costruisce piattaforme.

E come PRODOTTO           → il compratore è chi deve rendere conto di una
                            conclusione: analista, CTO, investitore.
                            Pubblico diverso, bisogno diverso, denaro diverso.
```

**Stesso lavoro, frame diverso.** E il frame si verifica in un modo solo: se qualcuno
che non sei tu lo chiede, lo usa o lo paga. Se dopo la pubblicazione non succede
niente, era ricerca interna travestita.

---

## 4. Raccomandazione

```text
1. A non è un'istanza: è l'infrastruttura di pubblicazione.
   → va fatta come prerequisito di NX-56, non come prodotto

2. B è bloccata tre volte (pavimento OSS, connettore PSD2, privacy).
   → da rivalutare solo se il verticale diventa finanza personale
     e si accetta di pagare un provider di open banking

3. C lato candidato è scartata dai dati ($0,25/utente).
   C' lato outplacement resta viva ma richiede vendita B2B senza prototipo

4. D ha la miglior struttura e la peggior esposizione competitiva.
   → è la seconda istanza naturale, non la prima: la regola del due
     si soddisferebbe con D dopo E

5. E ha il punteggio più alto E il prototipo esistente.
   → candidata prima istanza, CONDIZIONATA al test del frame (§ 3)
```

**Sequenza proposta:**

```text
passo 1   A come infrastruttura (pubblicazione)          → NX-56
passo 2   E come prima istanza, pubblicata                → NX-56 + NX-57
passo 3   test del frame: qualcuno che non sei tu risponde?
passo 4   se sì → D come seconda istanza (regola del due)
          se no → E era ricerca interna, e si passa a C' o D
```

Il passo 3 è il gate, e non è tecnico. È la conversazione che manca da D-039.

---

## 5. Cosa cambierebbe la raccomandazione

```text
· se NX-71 trovasse un open source mantenuto per competitive intelligence
  con evidenza → K4 di E crolla e D diventa prima scelta

· se il turismo ("banca servizi tra operatori turistici") producesse
  una conversazione reale questa settimana → K8 pesa più di K7,
  e il turismo diventerebbe competitivo nonostante sia una forma di bisogno
  diversa da Y

· se emergesse che l'utente ha accesso diretto a un career service
  o a un outplacement → C' salta la coda, perché K8 è il criterio
  più scarso di tutti
```

**K8 è il criterio più scarso e quello che vale di più.** Tutti gli altri si possono
soddisfare scrivendo codice. K8 richiede che esista una persona.

---

## 6. Y-1 — il volontario (aggiunta 2026-09-14)

Descrizione dell'utente:

> *"Y-1 vuole realizzare una piccola applicazione per l'attività di volontariato che
> vuole fare. Ha provato con il vibe coding ma ritiene tedioso rispondere a tutte le
> richieste tecniche: autenticazioni, Supabase, prompt che macinano sulle intenzioni
> dell'utente. Prova nexus-builder, ha visto qualche pubblicità. Zero problemi di
> deploy: deve solo scegliere se vuole qualche feature a pagamento oppure scordarsi
> di averla pubblicata."*

### 6.1 La frizione, nominata correttamente

Y-1 non ha un problema di "costruire un'app". Ha un problema preciso:

> **l'agente gli fa domande a cui non sa rispondere.**

```text
"quale provider di autenticazione?"
"che schema Supabase?"
"questa route va protetta?"
"dove rimanda dopo il login?"
"che componenti uso per questa vista?"
```

Ogni domanda è una **decisione di contratto**. Ed è qui che sta la differenza
strutturale:

```text
Bolt / Lovable / v0 / Cursor     general purpose → DEVONO chiedere
Open Nexus                        governato da contratti → HA GIÀ DECISO
```

Verifica sui file, non sulla teoria:

```text
ApplicationDefinition     routing: landing · login · afterLogin · notFound   DECISO
ApplicationType           user / shared / workspace                          DECISO
Primitive Authority       quali componenti esistono                          DECISO
Design Authority          quali token, quali colori                          DECISO
Theme Authority           come appare                                        DECISO
Auth 0.6.3-A/B            sessione, policy, proiezione navbar                DECISO
factory.ts                createApplicationDefinition con default            DECISO
```

**La proposition per Y-1 non è "un altro app builder". È:**

> **"Non ti chiediamo niente, perché abbiamo già deciso."**

Ed è la ragione per cui il vibe coding generico non può copiarla senza smettere di
essere generico.

### 6.2 La "comfort zone di ricchezza di templates" — confermata dagli ADR

L'osservazione dell'utente è corretta e va collegata a D-025:

```text
D-025   "la complessità UI si aggiunge dopo, la governance della UI va avuta prima"
ADR-0012  Primitive Authority esiste, 21 test, inventario chiuso
0.6.4     Application Experience Scaffolding → convenzioni Experience,
          /build/[app]/[page]
1.0       CLI per creare progetti senza toccare contratti o kernel
```

**La governance è costruita. Quindi la ricchezza di template può crescere adesso —
e può crescere più di un free-for-all, perché il gate la mantiene coerente.**

Il roadmap punta già a Y-1. Non è un'invenzione: è 0.6.4 + 1.0.

### 6.3 Il modello di monetizzazione è già validato

```text
"deve solo scegliere se vuole qualche feature a pagamento
 oppure scordarsi di averla pubblicata"
```

È **esattamente** il modello Trustable (§ 3.1 del dossier): licenza che abilita
Git push e publishing, tutto il resto libero. Indipendente, e corretto.

### 6.4 Ma il punteggio è il peggiore della matrice — tranne un criterio

```text
                          K1   K2   K3   K4   K5   K6   K7   K8
E  analisi con evidenza    ✓   ✓    ✓✓   ✓    ✓    ✓✓   ✓✓   ~
D  dev validation          ✓   ~    ✓✓   ✗    ~    ✓✓   ~    ✓✓
Y-1 volontario             ~   ✗✗   ✗    ✗✗   ✗    ✗✗   ✗    ✓✓
```

**K1 ~** — il volontario risponde al direttivo dell'associazione, non a un
controllore. Responsabilità debole, nessuna pressione di compliance.

**K2 ✗✗** — il sostituto non è ChatGPT: è Bolt, Lovable, v0, Replit Agent.
Finanziati, veloci, e stanno risolvendo esattamente questa frizione adesso.

**K3 ✗** — non c'è frequenza: è una build una-tantum più hosting.

**K4 ✗✗** — static site generator, temi Astro gratuiti, WordPress, e i free tier
dei vibe builder. Pavimento a zero, presidiato.

**K5 ✗** — "piccola app per il volontariato" è massimamente orizzontale.

**K6 ✗✗ — IL CRITERIO DECISIVO.** Il bisogno di Y-1 richiede:

```text
C-09  authoring agentico di bundle          TEORICA  ← la meno verificata di tutte
C-11  distribuzione firmata                 TEORICA
C-05  produzione artefatti                  PARZIALE
C-06  sessione e policy                     PARZIALE (AF-003/AF-004 aperti)
più   autenticazione, database, hosting, dominio custom
      = esattamente le cose che Y-1 ha trovato tediose
```

**Y-1 chiede ciò che non hai, nel punto in cui sei più debole.**

**K8 ✓✓** — ed è l'unico criterio forte. Y-1 è probabilmente una persona reale che
puoi chiamare. È il criterio più scarso della matrice.

### 6.5 La trappola specifica di "zero problemi di deploy"

```text
"zero problemi di deploy" per Y-1
      =
TUTTI i problemi di deploy per te
```

Ogni app pubblicata è: uptime tuo, infrastruttura tua, casella di supporto tua,
responsabilità tua. Per un progetto singolo con vincolo `< 10 €/mese`, è la direzione
opposta a quella della reduction pipeline — dove il costo marginale tende a zero.

Il gate a pagamento (publish = paid) mitiga, ma non risolve: il segmento che ha più
bisogno di "gratis e facile" è quello che paga meno.

E il churn del volontariato è brutale: i progetti muoiono, le app restano pubblicate,
il costo resta.

### 6.6 La risoluzione: tieni la frizione, cambia il payer

La frizione di Y-1 — *"l'agente mi fa domande a cui non so rispondere"* — è
**generale e preziosa**. Il segmento di Y-1 è **il peggior payer disponibile**.

È esattamente il pattern già misurato nella scansione:

```text
job-seeker lato candidato       $0,25 per utente per anno
job-seeker lato career service  $391 per cliente per anno
                                stesso prodotto, 1.500× di differenza
```

Chi altro è torturato dalle domande tecniche del vibe coding?

```text
· freelance e piccole agenzie che costruiscono siti per clienti
· associazioni CON un dipendente pagato (non volontariato puro)
· chi costruisce internal tool in una piccola azienda
· SVILUPPATORI che usano il vibe coding e odiano il boilerplate
  di auth / db / deploy                        ← è l'istanza D
```

**L'ultima riga è la convergenza:** D (developer validation) e Y-1 hanno la STESSA
frizione e payer opposti. D ha K1 ✓, K3 ✓✓, K6 ✓✓, K8 ✓✓.

```text
Y-1   "non voglio rispondere a domande tecniche"     non paga
D     "non voglio rifare auth/db/deploy ogni volta"  paga $209/abbonato
                                                               (text-to-SQL, 3,01×)
```

### 6.7 Verdetto

> **Y-1 è la conversazione giusta e il cliente sbagliato.**

```text
DA FARE     parlare con Y-1. Estrarre la lista ESATTA delle domande che il
            vibe coding gli ha fatto e a cui non sapeva rispondere.
            Quella lista è la specifica di nexus-builder, e vale più di
            qualunque PRD scritto a tavolino.

DA NON FARE costruire per Y-1 come primo cliente. Richiede C-09 + C-11 +
            auth + db + hosting (tutte teoriche o parziali), compete con
            Bolt/Lovable sul loro terreno più forte, e aggiunge costo
            ricorrente invece di toglierlo.
```

E c'è un uso terzo, che è il migliore:

```text
la lista delle domande di Y-1 è il test di completezza delle AUTHORITY.
Ogni domanda a cui un'authority risponde = una domanda in meno da fare.
Ogni domanda senza authority = un buco nella governance.

→ Y-1 come STRUMENTO DI MISURA di Foundation, non come mercato.
```

Questo costa una chiacchierata e produce una mappa dei buchi. È probabilmente il
miglior rapporto informazione/tempo disponibile oggi.

---

## 7. Backlog

```text
NX-75  NUOVO P0 — questa matrice. Da rieseguire se cambia un criterio.
NX-76  NUOVO P1 — A riclassificata: infrastruttura di pubblicazione, non istanza.
NX-77  NUOVO P2 — verificare il pavimento open source per E (NX-71 applicato).
                   Se esiste, la raccomandazione si inverte.
NX-78  NUOVO P1 — test del frame su E (§ 3): dopo la pubblicazione,
                   contare le richieste da persone che non sono l'utente.
                   Zero richieste → E era ricerca interna.
```

---

*Ultimo aggiornamento: 2026-09-14*
