# Il mercato del "CAPISCE" — chi c'è già

**Data:** 2026-09-12
**Origine:** osservazione dell'utente — *"ToolJet si colloca più su Trustable che
Instruqt, siamo sempre lì app builder, credo sia per sviluppatori... quindi ancora
non abbiamo trovato un clone di Open Nexus."*

**Esito:** la tassonomia è quasi giusta, ma ha un asse collassato. Correggendolo,
emerge che **la casella in cui sta Open Nexus sul lato del job-to-be-done è occupata,
e pesantemente.** Sul lato del meccanismo è vuota. Sono entrambe verità, e servono
entrambe.

---

## 1. L'asse collassato

L'utente ha classificato per **chi costruisce** (sviluppatori vs no). Ma le piattaforme
si distinguono su **cosa fa l'utente finale**. Ci sono tre verbi, non due:

```text
OPERA     inserisce dati, clicca, esegue CRUD, completa un task
IMPARA    segue un percorso guidato, fa pratica, viene valutato
CAPISCE   esplora un corpo di conoscenza e forma una convinzione
```

Matrice corretta:

```text
                        OPERA            IMPARA           CAPISCE
                    ─────────────────────────────────────────────────────
costruisce un dev   Trustable
costruisce author   ToolJet            Instruqt
costruisce agente                                          ← cella VUOTA
non si costruisce                                          AlphaSense
(SaaS chiuso)                                              Hebbia · Rogo
                                                           Aiera · Fintool
```

### Perché ToolJet è OPERA e non CAPISCE

ToolJet costruisce *admin panel, dashboard, operational apps*. Il builder è tecnico
(deve capire data source, query, JS), ma **l'utente finale dell'app costruita è un
impiegato che opera**: inserisce, approva, consulta una riga, clicca un bottone.

L'utente ha ragione che "siamo sempre lì, app builder". Ha ragione anche che è per
sviluppatori — ma solo sul lato builder. Sul lato consumer serve non-tecnici, come
Open Nexus. La differenza non è chi usa: è **cosa fa mentre usa**.

### Perché Instruqt è IMPARA

Lab guidati, task, `check-host`, badge. L'utente finale è uno sviluppatore che viene
addestrato. Ha un esito di apprendimento misurabile. Non forma una convinzione di
mercato: completa un percorso.

### La cella vuota

`costruisce agente × CAPISCE` è vuota. Nessuno dei quattro benchmark analizzati
(Trustable, ToolJet, Instruqt, e i CMS agentici visti in precedenza) ci sta.

**Ma non è vuota perché nessuno l'ha vista.** È vuota *in quella colonna*.
Nella colonna `non si costruisce × CAPISCE` c'è un mercato da centinaia di milioni.

---

## 2. Chi occupa già il "CAPISCE"

### AlphaSense — market intelligence

```text
contenuto      500M+ documenti premium: filing, earnings call, broker research,
               expert transcript, news
               1.000+ fonti sell-side, 240.000+ transcript di expert call,
               4.500+ modelli finanziari auto-aggiornanti
AI             ricerca semantica, smart alerts, summarization,
               "Generative Grid" per confrontare fino a 400 documenti
capitale       $350M raccolti a giugno 2026
prezzo         seat annuali a cinque cifre
maturità       fondata nel 2011, 15 anni di accumulazione
```

La loro stessa formulazione del problema:

> *"Knowledge workers across finance, corporate strategy, and consulting now spend
> more time aggregating and searching fragmented sources than they do actually
> forming conviction."*

**È la frase di positioning di Open Nexus, scritta da loro, con $350M dietro.**

### Hebbia — sintesi multi-documento

```text
prodotto       "Matrix": decompone la query in step agentici, processa TUTTI i
               documenti in parallelo (non top-K), restituisce griglie strutturate
               con catene di ragionamento
tesi tecnica   "early RAG approaches failed on 84% of the complex queries
               financial users actually ask"
volume         1B+ pagine processate
capitale       $130M Series B a valutazione $700M (lug 2024), a16z lead,
               con Index, GV, Peter Thiel, Eric Schmidt, Jerry Yang
stato          profittevole a $13M ARR al momento del raise,
               revenue 15× in 18 mesi,
               generava >2% del volume API giornaliero totale di OpenAI
servizio       forward-deployed engineers che costruiscono workflow firm-specific
```

### Rogo — agente per investment banking

```text
utenti         35.000+ professionisti in 250+ istituzioni:
               Lazard, Rothschild, Jefferies, Moelis, Nomura, Tiger Global,
               GTCR, Raymond James, Baird
prodotto       "Felix": accetta delega di task via email come un junior analyst,
               restituisce output formattato in Excel/PowerPoint/Word,
               itera sulle risposte, opera in continuo
distribuzione  enterprise-only, single-tenant, nessun self-serve
compliance     SOC2, ISO 27001, GDPR, CCPA, EU AI Act
integrazioni   LSEG, FactSet, Capital IQ, PitchBook, Preqin, Quartr,
               Dow Jones, Third Bridge
```

### Aiera — **il segnale più pericoloso**

```text
posizionamento "The Compliant Access Layer for Proprietary Financial Content"
delivery       "Enterprise-Level APIs ... through enterprise APIs and
                Model Context Protocol integrations"
componenti     "Embed AI-enhanced research experiences directly into existing
                workflows with modular components for search, discovery,
                summaries, company intelligence, and event analysis"
governance     entitlement-aware, permissioned, auditable, transparently sourced
scala          15k+ equity globali monitorate, 50k+ eventi tracciati,
               99,9% transcript human-reviewed
```

**Aiera sta già facendo NX-01b + NX-14 in un verticale.** Contract server, API
enterprise, esposizione via MCP, componenti modulari embeddabili, entitlement e
audit. Non è un app builder: è un layer di accesso governato.

È la conferma che l'architettura proposta in `04-FOUNDATION-API.md` è giusta —
ed è la notizia peggiore del documento, perché significa che qualcun altro l'ha
già industrializzata dentro un verticale con i soldi.

### Il resto

```text
Fintool · Fiscal.ai · Quartr · Koyfin · WarrenAI/InvestingPro · FinChat
edmundSEC · Boosted.ai · ChatFin (AI CFO)
+ incumbent: Bloomberg Terminal · FactSet · LSEG Workspace · Morningstar Direct
             S&P Capital IQ Pro · PitchBook
```

### Il soffitto "good enough"

Da una survey su CFO e team finance:

```text
ChatGPT Enterprise      lo strumento più usato per ricerca, analisi, reporting,
                        memo writing, automazione agentica
Microsoft 365 Copilot   due agenti ready-built (Researcher e Analyst) che
                        automatizzano planning, variance analysis,
                        visualizzazione dati senza scrivere codice
```

Sotto il livello enterprise dedicato, c'è un pavimento di strumenti generalisti già
nelle mani dei CFO. Qualunque proposta deve battere "ho già ChatGPT Enterprise".

---

## 3. Di che cosa è fatto il loro moat

Questa è la tabella che conta.

```text
AlphaSense   moat = 500M documenti proprietari + 1.000 accordi sell-side
                    + 240.000 expert transcript + 15 anni
Hebbia       moat = 1B pagine processate + forward-deployed engineers
                    + integrazione nativa con i provider che le firme già pagano
Rogo         moat = 250 istituzioni + workflow IB codificati + single-tenant
Aiera        moat = entitlement/compliance layer sopra contenuti ALTRUI
```

**Nessuno di questi moat è architetturale.** Sono tutti: contenuto, distribuzione,
o compliance.

Due conseguenze opposte, entrambe vere:

```text
BRUTTA   Non puoi competere sul contenuto. 500M documenti e 15 anni di accordi
         non si replicano. Se entri nel verticale finanziario head-on, perdi —
         non sull'architettura, sui contenuti e sulla distribuzione.

BUONA    Il loro moat non è difendibile con l'architettura, quindi non stanno
         difendendo l'architettura. Nessuno di loro ha un boundary compilato,
         una PageData portabile, un degradation budget, una Graphic Authority.
         Il loro output è intrappolato nel loro renderer — esattamente la critica
         che avevamo mosso a Instruqt.
```

---

## 4. La lettura onesta

### Cosa conferma

```text
1. La persona dichiarata (manager, CFO, broker che esplora e forma convinzioni)
   NON è una fantasia. È un mercato con round da $350M e seat a cinque cifre.

2. La diagnosi del problema è identica alla tua: troppo tempo ad aggregare,
   poco a formare convinzione.

3. La soluzione tecnica verso cui convergono è la tua: orchestrazione
   deterministica sopra l'AI. Hebbia dice esplicitamente che il RAG naive fallisce
   sull'84% delle query complesse e risponde con decomposizione in step agentici
   + processamento parallelo + output strutturato con reasoning chain.
   È "indeterminismo che diventa determinismo", con altre parole.

4. Aiera valida il modello contract server + MCP + entitlement in un verticale.
```

### Cosa smentisce

```text
1. "Non abbiamo trovato un clone di Open Nexus" è vero solo sul meccanismo.
   Sul job-to-be-done i clone ci sono, hanno funding enorme e clienti nominali
   che sono esattamente la tua persona.

2. La cella vuota (agente × CAPISCE) potrebbe essere vuota perché il mercato
   premia chi possiede il contenuto, non chi possiede il meccanismo.
   È l'ipotesi da falsificare prima di costruirci sopra.

3. Il tuo precedente personale è un data point: OpenFav auth open-source,
   spazio non occupato, zero impression. Uno spazio vuoto non è di per sé
   un'opportunità.
```

---

## 5. Le quattro opzioni, onestamente

```text
A. COMPETERE SUL VERTICALE FINANZIARIO
   contro $350M di capitale e 500M di documenti
   → persa in partenza. Non farlo.

B. ESSERE IL SUBSTRATO
   "costruisci la tua AlphaSense per il tuo dominio"
   → coerente con l'architettura, ma chi compra un substrato?
     richiede un ecosistema di builder che oggi non esiste.
     rischio: vendi pale durante una corsa all'oro a cui nessuno partecipa.

C. ESSERE L'ACCESS/EXPERIENCE LAYER sopra contenuti altrui
   → è quello che fa Aiera, e funziona perché sta DENTRO un verticale
     con la compliance come valore primario.
     richiede accordi sui contenuti. Da solo, è difficile.

D. PORTARE IL MECCANISMO IN UN VERTICALE NON FINANZIARIO E SOVRANITÀ-SENSIBILE
   → pharma/regolatorio, energia, settore pubblico, difesa, assicurazioni,
     normative tecniche
   → meno affollato, più sensibile a "niente esce dalla tua infra"
   → e qui hai un vantaggio che non è architetturale ma geografico/normativo:
     AlphaSense, Hebbia e Rogo sono tutte statunitensi
```

### Perché D è l'unica realistica per un progetto singolo

```text
1. Il vantaggio è difendibile senza capitale: normativa EU, residenza del dato,
   procurement pubblico che non può comprare SaaS USA.
2. È lo stesso terreno di Nuvolaris/Trustable (sovereign AI) e di Regolo.AI
   (inferenza EU) — che infatti sono italiani/europei. Non è un caso.
3. Il meccanismo compilato + degradation budget + local-first (NX-20) vale
   MOLTO di più per un ente pubblico che per un hedge fund: un hedge fund
   compra il contenuto, un ente pubblico compra la garanzia.
4. Non devi battere AlphaSense. Devi essere l'unica opzione conforme.
```

---

## 6. Cosa cambiare nei documenti esistenti

```text
07-PERSONA-AUTHORITIES-COSTO § 1.2
  Diceva: "il più vicino è Instruqt, ma Instruqt è didattica per sviluppatori.
  Qui si parla di supporto alla decisione per ruoli non tecnici. Non ha
  concorrenti diretti nel set analizzato."
  → CORREZIONE: non ha concorrenti nel set analizzato perché il set era di
    app builder. Nel verticale dichiarato i concorrenti esistono e sono forti.

NX-22 (due tier Builder / Decision-maker)
  → il tier Decision-maker ha un mercato validato ma presidiato.
    Va definito il VERTICALE, non solo la persona.

NX-28 (JsonApiConnector)
  → sale di priorità se il verticale è D: le fonti regolatorie hanno API.

NUOVO  NX-30 — scelta del verticale e verifica dell'ipotesi
       "il mercato premia il contenuto, non il meccanismo"
       va falsificata PRIMA di costruire, con 5-10 interviste o con
       l'analisi di come Aiera è entrata.
```

---

## 7. La domanda da porsi

Non *"esiste un clone di Open Nexus?"* — la risposta è no sul meccanismo, sì sul
bisogno, e la seconda conta di più.

La domanda giusta è:

> **In quale verticale il meccanismo vale più del contenuto?**

La finanza ha già risposto: vale il contenuto. Bisogna trovarne uno dove la risposta
è opposta — dove il dato è già del cliente, è frammentato, è regolamentato, e ciò
che manca è la capacità di attraversarlo. Pubblica amministrazione, farmaceutico,
energia, manifatturiero normativo.

Lì nessuno ha 500M di documenti da vendere, perché i documenti sono del cliente.
E lì un boundary compilato, un degradation budget e un local-first non sono
raffinatezze: sono requisiti di gara.

---

*Ultimo aggiornamento: 2026-09-12*
