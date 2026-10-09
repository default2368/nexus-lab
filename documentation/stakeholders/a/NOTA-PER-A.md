# Nota di analisi — l'ecosistema informativo attorno a un gestionale verticale

**Destinatario:** A.
**Mittente:** ⟪DA COMPILARE — nome e contatto. Non inviare con questo campo vuoto:
un documento senza controparte identificabile non può aprire nessun passo
successivo⟫
**Data:** 15 settembre 2026
**Natura:** risposta all'invito *"guarda questi siamo noi, vedi se riscontri bisogni"*
**Metodo:** analisi di fonti pubbliche. Nessun dato riservato è stato richiesto,
ottenuto o utilizzato. Nessuna superficie non pubblica è stata testata.

---

## 0. Come leggere questo documento

Il documento separa tre livelli, e li marca:

```text
[OSSERVATO]    verificato su fonte pubblica, con riferimento
[INFERITO]     interpretazione, esplicitamente segnalata come tale
[LIMITE]       ciò che non abbiamo potuto determinare
```

Nessuna affermazione fattuale compare senza riferimento. Dove il riferimento manca,
la riga è marcata `[INFERITO]`.

La ragione di questa forma è che la proponiamo anche come **esempio del metodo di
lavoro**: se un documento di analisi non distingue ciò che ha visto da ciò che
suppone, non è verificabile — e un documento non verificabile, in un dominio con
sanzioni, è un rischio invece che un aiuto.

---

## 1. Cosa abbiamo esaminato

```text
[OSSERVATO]  prometeorifiuti.com — home, pagine di ruolo, casi cliente
[OSSERVATO]  /wp-json/ — superficie REST standard del CMS
[OSSERVATO]  /wp-json/wp/v2/{pages,posts,media} — consistenza dei contenuti
[OSSERVATO]  /wp-sitemap.xml, /robots.txt
[OSSERVATO]  header HTTP e asset pubblici (tema, builder, plugin rilevabili)
[OSSERVATO]  scheda prodotto su Capterra
```

**Metodo e limiti del metodo:** rilevazione esterna, su superfici pubbliche. Non
abbiamo accesso a hosting, database, configurazione reale, workflow redazionale
interno, CRM, né a eventuali API private. Un inventario di plugin ricavato da asset
pubblici non è certo: alcuni possono essere inattivi o non caricati sulla home.

---

## 2. Cosa abbiamo osservato

### 2.1 Il prodotto

```text
[OSSERVATO]  gestionale verticale per la gestione amministrativa e operativa
             dei rifiuti: registri di carico/scarico, formulari e XFIR, MUD,
             RENTRI, autorizzazioni e scadenze, giacenze, contratti,
             pianificazione servizi, DDT e rapportini, fatturazione,
             magazzino MPS/EOW, dashboard, integrazione contabilità
[OSSERVATO]  copre più ruoli: produttori, trasportatori, destinatari,
             intermediari, spurghisti, bonifiche, consulenti, associazioni
[OSSERVATO]  il sito dichiara 2.000+ installazioni e 3.000+ aziende
             → dichiarazione del fornitore, non verificata indipendentemente
[OSSERVATO]  Capterra indica una partenza da 125 €/utente/mese, senza
             recensioni pubblicate → dato di listino, non verifica commerciale
```

### 2.2 La presenza web

```text
[OSSERVATO]  WordPress con tema Hello Elementor e Elementor Pro, su Apache/PHP
[OSSERVATO]  HTML renderizzato dal server. Non è una single page application
[OSSERVATO]  plugin di caching, SEO, sicurezza, form e analytics rilevabili
             dagli asset pubblici (non ne elenchiamo i nomi: non è rilevante
             per l'analisi e non vogliamo che questo documento somigli a una
             ricognizione)
[OSSERVATO]  il sito espone superfici standard per la lettura dei contenuti
```

**Nota tecnica, e va detta a favore:** la scelta di un CMS server-rendered con page
builder è **corretta** per questo scopo. È ciò che permette a una redazione non
tecnica di pubblicare rapidamente, mantenere SEO, gestire landing page e incorporare
video e documenti. Non è un difetto e non proponiamo di cambiarla.

### 2.3 Il modello di contenuto

```text
[OSSERVATO]  consistenza rilevata via REST: circa 153 pagine, 206 articoli,
             855 media
             metodo: totali esposti dall'API nelle intestazioni di risposta,
             non conteggio degli elementi restituiti in una singola pagina
             di risultati. I numeri sono quelli dell'istante della scansione
             e cambiano nel tempo.
[OSSERVATO]  tipi di contenuto esposti: post, page, attachment, nav_menu_item,
             wp_block, wp_template, wp_template_part, wp_global_styles,
             wp_navigation, wp_font_family, wp_font_face,
             elementor_library, elementor_snippet
[OSSERVATO]  nessun custom post type pubblico dedicato a: moduli, ruoli,
             casi cliente, norme, versioni, eventi, webinar, settori
```

Questo è il dato da cui parte tutta l'analisi che segue.

---

## 3. Il finding centrale: una rete di connessioni, rappresentata come pagine

### 3.1 La rete reale

Il dominio non ha una struttura ad albero. Ha una struttura a **grafo di
responsabilità**, con tipi di connessione eterogenei:

```text
connessione                   documenti tipici        obbligo principale
──────────────────────────────────────────────────────────────────────────
produttore → trasportatore    formulario/FIR, RENTRI   tracciamento del passaggio
trasportatore → impianto      formulario, conferma     conferimento
produttore → impianto         contratto, analisi       destinazione corretta
produttore → consulente       mandato                  assistenza continuativa
consulente → N produttori     vista aggregata          multi-tenant, isolata
associazione → N produttori   federazione              coordinamento, aggregazione
intermediario → molti         senza detenzione         intermediazione
tutti → autorità              registro, MUD, RENTRI    dichiarazione periodica
```

Ogni riga ha **documenti diversi, obblighi diversi, responsabilità diverse,
visibilità diversa, conservazione diversa**.

`[INFERITO]` Questa eterogeneità è la ragione per cui il prodotto copre tanti ruoli:
non è un elenco di funzionalità, è la forma del dominio.

### 3.2 Come è rappresentata oggi

```text
[OSSERVATO]  nel modello pubblico, tutto ciò esiste come page, post, attachment,
             elementor_library
[OSSERVATO]  il sito ha pagine per ruolo (produttori, trasportatori, spurghisti),
             casi cliente per settore, articoli normativi, webinar, documentazione
```

`[INFERITO]` Quindi la stessa nozione — un ruolo, un modulo, una norma, un obbligo —
vive in più punti senza legame strutturale:

```text
una norma  →  articolo + pagina prodotto + FAQ + slide webinar + caso cliente
un modulo  →  scheda + pagina per ruolo + articolo + video + documentazione
un ruolo   →  pagina dedicata + casi cliente + articoli + CTA
```

### 3.3 Perché questa impostazione è costosa

`[INFERITO]` — e segnalato come tale perché non abbiamo accesso al workflow interno.

Quando cambia una norma, la domanda operativa non è *"cosa dice la norma"* ma:

```text
quali dei 153 pagine e 206 articoli dipendono da questa norma?
quali vanno aggiornati, quali vanno ritirati, quali restano validi?
quali webinar e quali slide diventano obsoleti?
quale caso cliente cita un comportamento non più conforme?
```

È una ricerca **semantica di dipendenza**, non testuale: una pagina può dipendere da
una norma senza citarne il numero. Con un modello a pagine, questa ricerca si fa a
mano.

Stima, marcata come tale:

```text
[INFERITO]  se un cambiamento normativo tocca anche solo il 5% dei 359 contenuti
            testuali, sono ~18 elementi da valutare singolarmente.
            A 20 minuti di valutazione ciascuno, ~6 ore per cambiamento.
            Il passaggio a RENTRI ha prodotto più cambiamenti.
            I numeri sono ipotesi nostre, non misurazioni.
```

Il costo non è la pubblicazione — Elementor la rende rapida. Il costo è
**trovare cosa va pubblicato di nuovo**, e la garanzia di non aver dimenticato niente.

### 3.4 Il punto che riteniamo più interessante

```text
[INFERITO]  il valore reale dell'organizzazione non è l'elenco delle funzioni,
            è la POSIZIONE nella rete: il fatto che produttore, trasportatore,
            impianto, consulente e associazione passino tutti dallo stesso sistema.
```

`[OSSERVATO]` La comunicazione pubblica è organizzata per funzioni e per ruoli.
`[INFERITO]` Non troviamo una rappresentazione della rete come tale — cioè di come un
evento attraversa i nodi e chi è responsabile di cosa in ogni passaggio.

Se è così, c'è una distanza fra l'asset reale e come viene raccontato. È
un'ipotesi, non una critica, e potrebbe essere semplicemente una scelta commerciale
legittima.

---

## 4. Dove possiamo essere utili, e dove no

### 4.1 Cosa facciamo

Il sistema si chiama **Open Nexus**. Trasforma conoscenza strutturata in esperienze
navigabili.

L'idea di fondo sta in una riga: **una pagina non è un contenuto, è una
coniugazione.** Il contenuto è il significato strutturato — fonte, obbligo, ruolo,
relazione, stato, versione — e la pagina è uno dei modi in cui quel significato viene
detto a qualcuno. Lo stesso significato si coniuga diversamente per un produttore, un
trasportatore, un consulente, un auditor.

Da questo discendono tre proprietà che consideriamo non negoziabili:

```text
1. ogni affermazione risale a una fonte, una data e una versione
2. lo stesso contenuto produce viste diverse per ruoli diversi
3. la presentazione è governata da regole verificabili, non da abitudini
```

Il sistema è in produzione su un dominio diverso e ha attraversato cinque revisioni
architetturali senza rotture. Ne parliamo volentieri a voce: l'applicazione oggi
pubblica documenta soprattutto sé stessa, e preferiamo non spacciarla per una demo
di dominio quando non lo è.

Se vuoi una descrizione più discorsiva di come ragioniamo, è nell'allegato — che è
marcato come narrativo proprio perché non contiene affermazioni fattuali.

### 4.2 Cosa esiste già, e cosa no

Separazione onesta, perché è l'unica base utile per una conversazione:

```text
ESISTE E FUNZIONA
  · rappresentazione di conoscenza strutturata come esperienza navigabile
  · governance della presentazione con regole eseguite automaticamente
    (verifica su ogni file, con registro delle eccezioni motivate e datate)
  · proiezione semantica: stato → trattamento visivo, con degradazione
    controllata sui valori non riconosciuti invece che errore
  · accesso basato su sessione e policy, con viste diverse per stato utente
  · produzione di artefatti da definizioni dichiarative

PARZIALE
  · riduzione deterministica del contenuto prima di qualunque analisi assistita
  · tracciamento delle decisioni in forma strutturata

DA COSTRUIRE
  · il grafo di dipendenza norma → obbligo → contenuto, versionato nel tempo
  · il connettore per questa fonte
  · le viste specifiche del dominio
```

### 4.3 Perché l'acquisizione non è il valore

I contenuti pubblici di un sito sono leggibili da chiunque: è una proprietà del web,
non una scelta di chi pubblica. Qualunque CMS moderno espone superfici standard di
lettura, e questo vale per il sito in esame come per il nostro.

`[INFERITO]` Ne segue che **acquisire contenuto non è un vantaggio competitivo**.
È il punto di partenza, ed è alla portata di tutti.

Il valore, se esiste, sta nell'**ontologia** — cioè nel sapere che una certa pagina
dipende da una certa norma, che un certo caso cliente dimostra una certa funzione,
che un certo obbligo riguarda certi ruoli. E l'ontologia di un dominio regolamentato
non si deriva automaticamente: richiede conoscenza del dominio.

**Questo è il punto su cui riteniamo di aver bisogno di voi, più di quanto voi
abbiate bisogno di noi.**

### 4.4 Cosa NON proponiamo

```text
· sostituire WordPress o Elementor
  la scelta attuale è corretta per lo scopo

· sostituire o affiancare il gestionale
  la responsabilità transazionale e normativa resta dove sta

· interpretazione normativa automatica
  un sistema non produce pareri. Produce evidenze, relazioni e segnalazioni
  che un professionista valuta

· pubblicazione automatica di contenuto normativo
  ogni pubblicazione passa da approvazione umana

· accesso a dati senza autorizzazione scritta
  questa analisi è stata condotta esclusivamente su fonti pubbliche

· un "chatbot sul sito"
  sarebbe la versione povera di ciò che descriviamo, e produrrebbe risposte
  senza fonte in un dominio dove una risposta senza fonte è un rischio
```

### 4.5 Trattamento dei dati

Va detto prima, non dopo — e va **messo per iscritto prima di qualunque prova**, non
dopo averla concordata. L'elenco che segue è ciò che secondo noi dovrebbe stare in
quel documento; non è ancora quel documento.

```text
· il trattamento resta in capo a chi possiede il dato. Noi opereremmo come
  responsabile su istruzioni documentate del titolare
· minimizzazione: il sistema legge ciò che serve alla domanda posta, non
  l'archivio
· nessuna finalità di addestramento su dati dei clienti
· nessun trasferimento extra-UE del contenuto: l'elaborazione assistita può
  avvenire su inferenza ospitata in UE o in locale
· ciò che è sensibile può restare sul dispositivo dell'utente, con invio al
  modello di soli identificativi non re-identificabili senza la chiave locale
· conservazione, tempi e criteri di cancellazione definiti e datati
```

Quattro cose che un documento del genere dovrebbe nominare esplicitamente, perché
sono quelle che si chiedono dopo e costano di più:

```text
1. chi tratta cosa              titolare, responsabile, eventuali sub-responsabili
2. per quanto tempo             conservazione e criterio di cancellazione
3. con quale base giuridica     esecuzione di contratto, obbligo legale,
                                interesse legittimo, consenso
4. con quale traccia            log degli accessi e delle elaborazioni, e chi
                                può leggerli
```

Questa analisi è stata condotta esclusivamente su fonti pubbliche e non ha trattato
dati personali di terzi.

---

## 5. Le due viste che ci sembrano utili

Entrambe nascono dalla stessa struttura, e la struttura si descrive in una frase:

> **la stessa affermazione, con la stessa fonte, la stessa data e la stessa versione,
> vista da chi ha diritto di vederla, nella forma che gli serve.**

Dentro quella frase ci sono sette cose che di solito vengono costruite separatamente:
il grafo di conoscenza, la provenienza, la dimensione temporale, i ruoli,
l'autorizzazione, la proiezione in viste diverse, la tracciabilità. Non sono sette
funzionalità: sono sette conseguenze della stessa scelta — che il contenuto primario
non è la pagina ma il significato da cui la pagina viene generata.

Concretamente: un grafo in cui una norma implica obblighi, gli obblighi impattano
contenuti e documenti, e ogni elemento ha fonte, data e versione. Le due viste che
seguono non sono due prodotti — sono due letture dello stesso grafo.

Le presentiamo in quest'ordine perché la prima è quella di cui sappiamo dire meno,
ed è probabilmente quella che ti interessa di più.

### 5.1 Vista probatoria

```text
una data, un soggetto, un fatto
        ↓
quale norma era vigente in quella data
quali obblighi ne derivavano per quel ruolo
quale documentazione esisteva e in che stato
        ↓
catena: affermazione → documento → fonte → data → versione
```

Risponde a: *cosa era vero allora, e come lo si dimostra?*

`[INFERITO]` È la vista che interessa a chi assiste un operatore: in un
accertamento, in una contestazione, in un audit, la domanda non è quasi mai
"qual è lo stato attuale" ma "qual era lo stato in quella data, secondo la norma
allora vigente".

**Quello che non sappiamo, e che è la ragione principale per cui ci serve la tua
lettura:** se e come un output di questo tipo sia utilizzabile in sede
contenziosa o procedimentale — catena di custodia, affidabilità della
ricostruzione, certificabilità della versione normativa — è una questione su cui
non abbiamo gli elementi per pronunciarci. Non la dichiariamo risolta: la
dichiariamo aperta, e sappiamo a chi chiederlo.

### 5.2 Vista editoriale

```text
cambia una norma o esce una release
        ↓
il sistema elenca i contenuti dipendenti: pagine, articoli, FAQ,
slide, casi cliente, documentazione
        ↓
propone una modifica, marcando cosa è osservato e cosa è proposto
        ↓
revisione umana
        ↓
pubblicazione nel sistema esistente
        ↓
traccia: chi ha approvato, quando, su quale fonte
```

Risponde a: *cosa devo aggiornare?* È la vista di § 3.3, ed è quella che riguarda
chi pubblica contenuto — sia un vendor, sia un'associazione, sia uno studio che
produce circolari per i clienti.

`[INFERITO]` Le due viste usano lo stesso grafo; la seconda aggiunge l'asse
temporale alla prima. Costruirne una costruisce gran parte dell'altra.

---

## 6. Cosa non siamo riusciti a determinare

```text
[LIMITE]  provider di hosting, versione PHP, database
[LIMITE]  configurazione reale della cache e CDN eventualmente presente
[LIMITE]  workflow redazionale interno, chi approva cosa
[LIMITE]  presenza di CRM, knowledge base o marketing automation
[LIMITE]  integrazione fra il sito e il gestionale
[LIMITE]  eventuali API private o superfici non pubbliche
[LIMITE]  traffico, conversioni, metriche reali
[LIMITE]  se i concetti di dominio (moduli, ruoli, norme, casi) esistano già
          in una forma interna non esposta pubblicamente
[LIMITE]  se il costo descritto in § 3.3 sia effettivamente percepito
          da qualcuno, e da chi
[LIMITE]  utilizzabilità in sede contenziosa o procedimentale degli output
          descritti in § 5.1
[LIMITE]  chi sia il destinatario reale: chi produce il software, chi lo usa,
          o chi assiste chi lo usa
```

L'ultimo punto è il più importante. **Tutta l'analisi di § 3 è un'ipotesi coerente
con ciò che è osservabile, non una misurazione.** Se il problema non è sentito,
l'analisi è interessante e inutile.

---

## 7. Le domande che ci servono

Tre, e nessuna riguarda il prodotto.

```text
1. Quando hai scritto "siamo noi", a chi ti riferivi: al tuo mondo di
   professionista che assiste operatori del settore, o ad altro?
   → determina per chi ha senso ciò che abbiamo descritto

2. Tu cosa ci vedi, in questo settore? Cosa ti fa perdere tempo o ti fa
   arrabbiare quando ci lavori attorno?
   → hai gli occhi del dominio, noi no. Questa risposta vale più di
     qualunque nostra analisi

3. Nel tuo lavoro, quante volte ti è capitato di dover ricostruire cosa era
   vero in una certa data per un cliente — e quanto ti è costato in ore?
   → è la domanda su § 5.1. Se la risposta è "spesso" e "molto", la vista
     probatoria è un prodotto. Se è "raramente", è un'idea elegante senza
     domanda, ed è meglio saperlo subito
```

---

## 8. Nota sul metodo, se interessa

Questa analisi è stata prodotta con una disciplina precisa: ogni affermazione
fattuale ha una fonte; ciò che non ha fonte è marcato come inferenza; i limiti sono
elencati invece che omessi; le stime sono dichiarate stime.

Non è una scelta stilistica. In un dominio dove un errore documentale ha conseguenze
amministrative o penali, **un sistema che produce conclusioni senza distinguere ciò
che ha osservato da ciò che ha supposto è un rischio, non uno strumento.**

La stessa disciplina che abbiamo applicato a questo documento è quella che
applicheremmo a qualunque cosa costruita insieme: separazione fra dato,
interpretazione e decisione; approvazione umana sugli output sensibili; traccia di
ogni passaggio.

Se questo documento sarà letto da strumenti automatici, ci sta bene: è scritto
apposta per essere verificabile.

---

## 9. Riferimenti

```text
prometeorifiuti.com/
prometeorifiuti.com/cosa-fa-prometeo/
prometeorifiuti.com/produttori/portovesme/
prometeorifiuti.com/produttori/bio-energia-guarcino/
prometeorifiuti.com/trasportatori/
prometeorifiuti.com/spurghisti/rse/
prometeorifiuti.com/wp-json/          (superficie REST standard del CMS)
prometeorifiuti.com/wp-sitemap.xml
capterra.com/p/189319/Prometeo-Rifiuti/
```

Numeri di versione, conteggi dei contenuti e namespace sono quelli rilevati alla
data di scansione. Sono destinati a cambiare.

---

*Documento prodotto su fonti pubbliche. Nessuna informazione riservata è stata
richiesta o utilizzata. Le sezioni marcate `[INFERITO]` sono interpretazioni e vanno
verificate con chi conosce il dominio — cioè, presumibilmente, con te.*
