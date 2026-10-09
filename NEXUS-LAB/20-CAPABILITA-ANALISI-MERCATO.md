# La capacità di analizzare progetti di mercato — correzione di lettura

**Data:** 2026-09-13
**Natura:** correzione a `19-METHOD-AGENT-GIUDIZIO.md`. Il giudizio dato lì colpiva
un bersaglio sbagliato.

---

## 1. L'errore, localizzato con precisione

L'utente dichiara l'intento reale:

> *"aggiungere la capacità di Open Nexus di analizzare progetti di mercato, e di
> vendere questa capacità. Non era implementazione agent tout court."*

Ho letto il documento incollato alla lettera — "Method Agent", "Nexus Governor",
"Feature Proposal Agent" — e ho giudicato **l'implementazione di un agente di
governance interna**. L'intento era un altro: una **capacità di prodotto**.

### 1.1 La parte imbarazzante

Il `13-X-MOAT-E-PRIMA-APPLICAZIONE.md`, righe 278-279, scritto da me:

> *"Nota sull'asse 4: **la classificazione del tipo di moat è la parte che nessuno
> fa.** G2 classifica per categoria e recensioni. Nessuno classifica per
> *meccanismo* e per difendibilità."*

**Quella è la tesi di prodotto.** L'ho scritta, e due paragrafi dopo ho declassato
NX-31 — che era la cosa che la conteneva — come *"comodo e auto-riferito"*.

Poi, in `19-...` § 3, ho rincarato: *"produce un dataset su di sé"*. Falso. Il
dataset è su **Trustable, ToolJet, Instruqt, AlphaSense, Hebbia, Rogo, Aiera**. Sono
oggetti esterni. Auto-riferito era il *motivo* per cui lo producevamo, non il
*contenuto* di ciò che è stato prodotto.

### 1.2 Cosa resta valido di `19-...`

```text
§ 4   il gate deve essere codice deterministico, non LLM
      → RESTA, e vale di più se venduto: un cliente che paga per un'analisi
        ha bisogno che il verdetto sia riproducibile

§ 5   staleness dell'evidenza esterna (NX-54)
      → RESTA, e vale di più: un'analisi di mercato con evidenza scaduta
        è peggio di nessuna analisi

§ 3   la trappola di comfort
      → SBAGLIATA nel bersaglio. Corretta nel meccanismo: vale per qualunque
        lavoro interno che non produce output per qualcuno fuori.
        Ma questa capacità produce output vendibile, quindi non si applica.

§ 6   mercato agent-governance affollato
      → SBAGLIATO. Non è quel mercato. Vedi § 4 di questo documento.
```

---

## 2. La capacità, formulata correttamente

```text
CAPACITÀ
  analizzare un prodotto / piattaforma / progetto di mercato
  e produrre una knowledge experience navigabile che contenga:

    · fatti osservati, con il comando o la fonte che li ha prodotti
    · classificazione per MECCANISMO (non per categoria)
    · classificazione per TIPO DI MOAT (non per funding)
    · posizione rispetto a un'architettura di riferimento
    · delta: cosa rubare, cosa non copiare
    · rischi e ipotesi falsificabili
    · traccia di decisione con stato (deciso / proposto / falsificato)
```

### 2.1 Il differenziatore non è l'analisi

Un LLM produce un'analisi competitiva in dieci minuti. Ce ne sono centinaia.

Il differenziatore è quello che l'utente ha indicato dicendo *"col metodo di
arresto"*:

```text
· ogni affermazione cita il comando o la fonte che l'ha prodotta
· il sistema distingue observed / inferred / proposed
· il sistema può dire "non ho evidenze sufficienti"
· il sistema SI CORREGGE e registra la correzione
· l'analisi è VERSIONATA e si aggiorna quando l'oggetto cambia
```

**La prova è in questa sessione.** Quattro ipotesi formulate dal revisore, quattro
falsificate dai file, quattro correzioni registrate a verbale (D-027 falsificata,
NX-18 chiuso come duplicato, D-033 corretta in D-034, NX-44 risolto smentendo la
proposta). Un'analisi che non può essere falsificata non è un'analisi: è opinione
con una bibliografia.

> *"Zero risultati senza comando non è un dato."* (`03-WORKFLOW.md`)

Questa regola, applicata a un prodotto venduto, **è** il prodotto.

---

## 3. Il prototipo esiste già: sono i quattro dossier

Non è un'ipotesi da costruire. È lavoro già consegnato:

```text
../documentation/research/benchmarks/TRUSTABLE-vs-OPENNEXUS.md    Trustable / Nuvolaris
  33 URL scrape · sitemap · 6 pagine di documentazione
  output: mappa strutturale, licensing offline firmato, il buco del gate
          deterministico, 10 voci di backlog derivate

../documentation/research/benchmarks/TOOLJET-benchmark.md         ToolJet
  repo + README + architecture doc + skills + commit history + MCP
  output: AGPL/EE/MIT a tre licenze, BYO model = costo LLM zero,
          interpretazione runtime vs boundary compilato, la commit da 12
          sottosistemi come evidenza del costo

12-MERCATO-CONOSCENZA.md     AlphaSense · Hebbia · Rogo · Aiera
  output: tassonomia OPERA/IMPARA/CAPISCE, il moat è contenuto non
          architettura, la cella vuota, il verticale candidato

11-CONNECTOR-LAYER.md        (derivato)
  output: interfaccia connettore, change detection, cosa non aggiungere
```

Più `16-FOUNDATION-HEALTH.md` e `17-NEXUS-LAB-HEALTH.md`, che sono la stessa
capacità applicata verso l'interno — e funzionano, il che dimostra che il metodo non
dipende dall'oggetto.

**Quattro analisi complete, con evidenza, in tre giorni, da una persona sola.**
Questo non è un piano di prodotto. È un prodotto che ha già girato.

---

## 4. Dove sta il mercato (correzione a `19-...` § 6)

Avevo indicato il mercato sbagliato (agent governance / eval / observability).
Quello giusto è **architecture & market intelligence**:

```text
Gartner MQ / Forrester Wave    opinione, costosa, nessuna traccia di evidenza,
                               nessuna architettura. Si compra il brand.
CB Insights / PitchBook        funding e dati di mercato, non meccanismo
G2 / Peer Insights             sentimento degli utenti, non architettura
DeepWiki                       genera documentazione architetturale di un repo
                               → IL PIÙ VICINO tecnicamente, ma è sul SINGOLO repo,
                                 non comparativo, e non classifica il moat
CodeScene                      architecture intelligence sul PROPRIO codebase
                               → vende alle enterprise, ma inward-facing
Technical due diligence (M&A)  umana, €30-100k per engagement,
                               obsoleta in un mese
Fractional CTO / consulenza    umana, non scalabile, non versionata
```

**Lo spazio vuoto:** analisi **comparativa** di un mercato per **meccanismo e
difendibilità**, con **traccia di evidenza falsificabile**, **versionata** e resa
come **esperienza navigabile**.

Nessuno degli otto lo fa. E la ragione per cui nessuno lo fa è interessante: richiede
sia competenza architetturale sia un modello di conoscenza strutturato. Chi ha la
prima vende consulenza; chi ha il secondo vende dati.

### 4.1 Chi paga, concretamente

```text
1. VC / PE — technical due diligence
   oggi: pagano umani €30-100k per un report obsoleto in un mese
   valore: analisi governata, con evidenza, aggiornabile, frazionabile
            su più target

2. Corporate strategy / competitive intelligence
   oggi: Gartner (brand) + analista interno (tempo)
   valore: classificazione per meccanismo invece che per categoria

3. Build-vs-buy di un CTO
   oggi: G2 reviews + demo dei vendor
   valore: "cosa rubare, cosa non copiare", con il boundary del proprio sistema

4. System integrator / consulenza
   valore: capacità di produrre la deliverable, non di comprarla
```

Il primo è il più chiaro perché **esiste già una spesa** e la soluzione attuale è
palesemente peggiore. È esattamente il criterio di verifica di NX-30: *un payer che
oggi paga qualcun altro per una soluzione peggiore*.

---

## 5. Perché serve Open Nexus, e non un PDF

La domanda va posta, perché se la risposta è "non serve", la capacità è una
consulenza con un template.

```text
un PDF           è fermo. Trustable è a V0.4.0 oggi, a V0.6 fra tre mesi,
                 e il modello DeepSeek è stato ritirato in sei settimane.
                 Un'analisi statica è obsoleta prima di essere letta.

PageData         è versionata, navigabile, confrontabile, aggiornabile.
                 Le quattro analisi di questa sessione condividono assi
                 (OPERA/IMPARA/CAPISCE, tipo di moat, mechanism) e quindi
                 sono CONFRONTABILI fra loro. Quattro PDF non lo sono.

Source Authority ogni affermazione ha una fonte. È ciò che rende l'analisi
                 difendibile davanti a un cliente che paga.

Graphic Authority  densità e confronto governati: una matrice di 7 piattaforme
                 × 12 dimensioni non si impagina a mano senza deriva.

Gate VALIDATE     un'analisi che afferma qualcosa senza il comando che l'ha
                 prodotta viene RIFIUTATA. È la garanzia vendibile.
```

**Il prodotto non è l'analisi. È l'analisi che resta vera.** Ed è la stessa
proposizione di Foundation applicata a un contenuto invece che a un'applicazione.

Nota: questa è la prima volta nella sessione in cui il valore di PageData come
"linguaggio delle knowledge experience" (D-002) ha un caso d'uso che non sia
documentazione interna.

---

## 6. La proprietà che lo rende superiore a NX-31 e alla sonda

```text
NX-30 chiedeva: in quale verticale il meccanismo batte il contenuto?

questa capacità RISPONDE a NX-30 come sottoprodotto.
Ogni analisi eseguita aggiunge un dato alla risposta.
```

Non serve scegliere il verticale prima. Il verticale **emerge** dal corpus di
analisi, che è esattamente la logica del metodo Sonda (D-040): *"il verticale si
deduce dalle sonde, non si sceglie a priori"* (D-041).

Confronto con le due sonde candidate:

```text
sonda job-seeker         richiede: modello contenuti nuovo, onboarding,
                         pubblico B2C, mercato affollato (Teal, Rezi, Jobscan)
                         produce: apprendimento sul modello contenuto→viste

sonda analisi mercato    richiede: connector + reduction + classificazione
                         (tutti già progettati: NX-27/28, reduction pipeline)
                         pubblico B2B con spesa esistente
                         produce: apprendimento SUL VERTICALE + output vendibile
                         + il prototipo esiste già (4 dossier)
```

Non è detto che la seconda vinca — la B2B ha cicli di vendita lunghi e richiede
credibilità che oggi non c'è. Ma ha tre proprietà che la prima non ha: **il
prototipo esiste**, **risponde a NX-30**, e **ha un payer con spesa già in corso**.

---

## 7. La sintesi operativa: pubblicare le quattro analisi

Risolve insieme tre problemi che erano separati.

```text
1. PORTFOLIO / DISTRIBUZIONE  (doc 18 § 6: gratis senza pubblico nominato
                               = inventario)
   → pubblico nominato: CTO, founder, valutatori tecnici, VC analyst
   → canale: le analisi stesse, pubblicate come knowledge experience
     su openfav.vercel.app, che già rende library / topics / generated-knowledge

2. DEMO DI PRODOTTO
   → non serve costruire una demo: la demo è il corpus
   → "guarda come abbiamo analizzato ToolJet, con evidenza e correzioni"

3. DATASET PER NX-30
   → ogni analisi pubblica aggiunge un dato al corpus che risponde
     alla domanda sul verticale
```

**Tre obiettivi, un solo artefatto, costo marginale zero** (le analisi sono già
scritte, vanno solo portate in PageData).

E c'è un effetto di secondo ordine: un'analisi pubblica e corretta di ToolJet o di
AlphaSense è **leggibile dal soggetto analizzato**. È il modo in cui Aiera e Hebbia
sono entrate nei loro mercati — contenuto tecnico pubblico che dimostra competenza.

---

## 8. I rischi onesti

```text
1. RIPETIBILITÀ
   Le quattro analisi sono riuscite anche perché l'operatore ha fatto domande
   nette e ha contestato le risposte. Prodotizzare significa far fare il lavoro
   al metodo, non all'operatore.
   → verifica: eseguire un'analisi SU UN OGGETTO NUOVO usando solo il metodo
     scritto, senza intervento. Se il risultato è peggiore, il metodo è
     incompleto. Questo è il test, ed è economico.

2. ACCESSO ALLE FONTI
   Questa sessione ha usato scraping di siti pubblici e repo pubblici.
   Per la due diligence servono anche fonti non pubbliche (codebase del target,
   contratti, metriche). Lì il prodotto cambia natura e serve un accordo.
   → perimetro iniziale: SOLO fonti pubbliche. Va dichiarato, non lasciato
     ambiguo.

3. ESPOSIZIONE LEGALE
   Un'analisi comparativa pubblicata che dice "il moat di X è debole" è
   opinione su un concorrente identificabile. In Italia c'è diffamazione e
   concorrenza sleale.
   → forma: fatti citati + giudizio marcato come giudizio. La separazione
     observed/inferred/recommended che serve al prodotto serve anche qui.
     Non è un caso: è la stessa struttura.

4. CREDIBILITÀ B2B
   Vendere due diligence a un VC senza track record è difficile.
   → il corpus pubblico È il track record. Motivo in più per § 7.

5. IL CONFLITTO CON LA SONDA
   Due sonde in parallelo sono troppe per una persona sola.
   → non scegliere adesso. Fare § 7, che costa quasi zero perché gli artefatti
     esistono, e lasciare che il segnale decida.
```

---

## 9. Revisione del backlog

```text
NX-31  RIVALUTATO. Era "reference validation di X, tassonomia dei competitor",
       declassato come comodo. Riletto correttamente: è la FORMA INIZIALE della
       capacità di analisi di mercato. Torna P1, con output PUBBLICO e non
       interno.

NX-53  check-proposal.mjs — resta P2 con prerequisito. La correzione del gate
       deterministico vale, ma non è la priorità.

NX-56  NUOVO P1 — portare le 4 analisi esistenti in PageData e pubblicarle.
       Il prototipo esiste già come markdown; manca la trasformazione.
       È § 7: portfolio + demo + dataset, un artefatto solo.

NX-57  NUOVO P1 — test di ripetibilità (§ 8.1): eseguire un'analisi su un
       oggetto NUOVO usando solo il metodo scritto, senza intervento
       dell'operatore. È il gate che dice se la capacità è un prodotto
       o una performance.

NX-58  NUOVO P2 — schema del proposal/analysis record come FILE versionato,
       con campi status: observed | inferred | recommended, e requisito che
       ogni `observed` citi la fonte. È la struttura vendibile.

NX-30  non più bloccante e non più da decidere a priori: la capacità di analisi
       produce il dataset che risponde alla domanda. Confermato D-041.
```

**Zona sicura:** nessuna voce tocca i simboli vincolati. NX-56 usa renderer
esistenti (`open-nexus/library`, `topics`, `generated-knowledge`) già live.

---

## 10. Cosa ho imparato dall'errore

Non è solo "ho letto male". È un pattern:

```text
quando una proposta arriva incollata da un'altra sessione, ha già una FORMA.
La forma era "agent implementation". Ho giudicato la forma.
L'intento era "capability to sell".
```

E avevo già gli elementi per accorgermene, nello stesso documento incollato:

> *"La funzionalità potrebbe essere un vero prodotto"*
> *"eventualmente, in futuro, un prodotto vendibile"*

Li ho letti come concessioni marginali. Erano il punto.

Regola da aggiungere a `03-WORKFLOW.md`:

> Quando si giudica una proposta che arriva da un'altra sessione, chiedere
> **cosa si vende** prima di chiedere **cosa si costruisce**.
> La seconda domanda è più facile e per questo produce risposte sbagliate.

---

*Ultimo aggiornamento: 2026-09-13*
