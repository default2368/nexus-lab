# Method Agent / Nexus Governor — giudizio

**Data:** 2026-09-13
**Oggetto:** proposta (da altra sessione) di un agente che applica i metodi condivisi
per governare la propria evoluzione. *"Open Nexus governa anche il proprio sviluppo
applicando i propri contratti."*
**Richiesta:** giudizio sull'idea, indipendente dalla ricerca di mercato.

---

## 1. Verdetto

```text
come capacità INTERNA e dimostrazione dell'architettura
   → eccellente, coerente, soddisfa la regola del residuo (13-... § 1.3)

come PRODOTTO vendibile
   → non adesso, e il mercato è più affollato di quanto la proposta suggerisca

come PROSSIMA COSA DA FARE
   → NO. È un P2 che si traveste da P0 perché è affascinante.
```

E un errore architetturale nella proposta, correggibile e importante: **il gate non
può essere l'agente.** Vedi § 4.

---

## 2. La gemma: l'arresto come dimostrazione

> *"un agente credibile non è quello che costruisce sempre. È quello che sa dire:
> 'Non ho ancora evidenze sufficienti per cambiare il contratto.'"*

Questa è l'intuizione forte, ed è forte per un motivo strutturale, non narrativo:

```text
tutti gli agenti sul mercato sono ottimizzati per PRODURRE
un agente il cui comportamento distintivo è RIFIUTARE
è diverso per costruzione, non per marketing
```

Ed è coerente con Foundation fino in fondo: l'intera premessa è che un kernel
deterministico vincoli un layer non deterministico. **Un agente che si ferma è
Foundation applicata al processo di sviluppo.** Non è una feature aggiunta: è la
stessa tesi in un altro punto del sistema.

Seconda cosa giusta: le **tre separazioni** anti-autoreferenzialità.

```text
Metodo ≠ agente            il metodo è leggibile e versionato indipendentemente
Proposta ≠ decisione       l'agente propone, la persona decide
Evidenza ≠ interpretazione  dato osservato / regola applicata / inferenza /
                            raccomandazione / decisione umana
```

La terza **esiste già**: è il guardrail `FACTS OBSERVED / HYPOTHESES /
RECOMMENDATIONS` di `03-WORKFLOW.md` § 4, usato tutta la sessione. L'idea non è
nuova — è la promozione di una pratica esistente a componente. Il che è il modo
giusto di far nascere un componente.

Terza cosa giusta: il moat 4 e 5 (tracce accumulate, specificità organizzativa) sono
l'unico moat reale fra i cinque elencati, e coincidono con la regola del residuo.
I moat 1-3 (metodo formalizzato, stato strutturato, applicazione automatica) sono
**copiabili**: sono struttura. Il 4 e il 5 non lo sono: sono storia.

---

## 3. Il pericolo: è la trappola di comfort nella sua forma più sofisticata

Va detto senza attenuanti, perché è il rischio specifico di questo progetto.

```text
D-039 registra:  diciassette documenti · zero conversazioni con un potenziale utente
NX-31 (tassonomia dei competitor)  → l'ho declassato perché "comodo e auto-riferito"
                                     ma almeno produceva un dataset sul MONDO ESTERNO

Method Agent  → produce un dataset SU DI SÉ
```

È **architettura sull'architettura**. È il passo intellettualmente più soddisfacente
disponibile, e produce zero segnale di mercato.

La proposta lo intravede — *"non è ancora automaticamente un moat di mercato"* — e
elenca cosa dovrebbe produrre (meno regressioni, meno review, decisioni più rapide,
audit più semplice). Ma non dice la cosa più dura:

> **Questo è il modo più probabile in cui il progetto muore.**
> Non per architettura sbagliata. Per governance perfetta di niente.

Il paradosso: un sistema progettato per impedire le deviazioni può impedire anche
l'unico movimento che conta — parlare con qualcuno che non sia tu.

---

## 4. L'errore architetturale: il gate non può essere l'agente

La proposta attribuisce all'agente il potere di bloccare:

> *"impedire l'implementazione se manca il gate minimo"*
> *"l'agente non si limita a citare il metodo: lo usa per bloccare, chiedere,
> classificare e proporre"*

**Un LLM non può impedire niente in modo affidabile.** Può raccomandare, e una
raccomandazione si ignora. Se il gate è l'agente, allora *"l'agente valuta l'agente"*
è letteralmente vero e le tre separazioni non bastano a risolverlo — perché la
separazione sarebbe implementata dalla stessa cosa che dovrebbe rispettarla.

### 4.1 La correzione: hai già la soluzione, ed è uno script

```js
scripts/design/check-style-authority.mjs
  regole come DATO         EXCEPTIONS, RAW_PALETTE_ROOTS esportati
  scope derivato           walk() su tutto src/ → fails CLOSED
  funzione pura            classifySource(source, relPath) → findings
  tre modalità             report umano · --json · --ci (exit 1)
  eccezioni tipizzate      4 categorie, reason obbligatorio, scadenza nel doc
```

**È un gate deterministico che implementa una policy.** Il Feature Proposal Agent è
la stessa mossa su una policy diversa.

```text
scripts/governance/check-proposal.mjs

INPUT     un proposal record (YAML/JSON), scritto da umano o BOZZATO dall'LLM
REGOLE    i sei gate di D-040
          + lista simboli zona vincolata (02-BACKLOG § "Proprietà del backlog")
          + criterio di arresto della sonda (L-1)
          + regola del due (seconda sonda nominata)
LOGICA    deterministica. nessun LLM.
OUTPUT    report · --json · --ci
VERDETTO  proceed
          needs-second-probe
          touches-core
          insufficient-evidence
          expired-exception
```

### 4.2 Perché questa forma è giusta

```text
1. il gate è CODICE            → la separazione Proposta ≠ Decisione è STRUTTURALE,
                                 non disciplinare
2. classe 0                    → zero token (08-COST-CULTURE § 3)
3. testabile                   → 21 test come primitive-authority
4. riusabile dal gate VALIDATE → stesso pattern di NX-34
5. esistente                   → non è un componente nuovo, è la generalizzazione
                                 di uno script che funziona già
6. l'LLM resta dove deve stare → classe 1: BOZZARE il proposal record, non valutarlo
```

Il punto 6 è la divisione corretta del lavoro:

```text
LLM     legge la richiesta, estrae lo scopo, i contratti toccati,
        formula l'ipotesi utente, propone il test minimo
        → produce un proposal record DRAFT, marcato come tale

SCRIPT  verifica che il record sia completo, che i gate siano soddisfatti,
        che la zona vincolata non sia toccata, che il criterio di arresto esista
        → produce un VERDETTO, non un'opinione

UMANO   decide
```

**Evidenza ≠ interpretazione** diventa così una proprietà del sistema e non una
buona intenzione: il campo `status` del record dice se un valore è `observed`,
`inferred` o `proposed`, e lo script rifiuta i gate marcati `inferred` dove serve
`observed`.

### 4.3 Effetto collaterale utile

Chiude **L-1** (criterio di arresto) della sessione precedente. Un criterio di
arresto scritto in prosa è un desiderio. Un criterio di arresto che fa `exit 1` in
CI è un meccanismo.

---

## 5. La lacuna che le tre separazioni NON coprono

Le tre separazioni risolvono l'autoreferenzialità **epistemica**. Non risolvono
quella **economica**, che è più insidiosa:

```text
se i criteri del gate vengono dai documenti del fondatore,
e il gate decide quali sonde meritano di esistere,
allora il sistema approverà sistematicamente ciò che somiglia
al lavoro che il fondatore ha già fatto.
```

E il gate "serve una seconda sonda" può essere soddisfatto proponendo una seconda
sonda anch'essa interna.

**Correzione: almeno un gate deve richiedere un input che il sistema non può
produrre da solo.**

```text
gate 4 dei sei (D-040)     "riduce un costo reale per l'utente"
misura della sonda         "disponibilità a pagare"
                           → entrambi richiedono dati ESTERNI
```

Regola proposta:

> Un proposal record i cui campi di evidenza esterna sono `pending` non può restare
> `pending` indefinitamente. Dopo N giorni lo script lo marca `stale` e il verdetto
> diventa `insufficient-evidence`.

Senza questo, il Method Agent diventa **una macchina per rimandare il contatto col
mercato con una traccia di audit pulita**. Che è peggio di non averla, perché sembra
rigore.

---

## 6. Sul "prodotto vendibile per team che vogliono governare agenti"

La proposta lo indica come opzione 3, futura. Va ridimensionata adesso, non dopo.

```text
il mercato "governance/observability/eval di agenti AI" esiste ed è affollato e
in movimento rapido: Braintrust, LangSmith, Arize, Galileo, Patronus, Credo AI,
più i cloud generalisti

e il sotto-mercato "governare cosa un agente può cambiare" è già occupato da
convention files: .clinerules · AGENTS.md · Cursor rules · Claude Code skills/hooks
ToolJet ha .agents/skills/ con manage-skills che governa DOVE vivono le skill
in base alla sensibilità — è governance degli agenti, fatta con symlink e uno
script di sync
```

Non uccide l'idea come **capacità interna**. La uccide come ipotesi di prodotto senza
un lavoro di ricerca che al momento non c'è.

**Regola pratica:** non nominarlo "prodotto" finché non ha superato il gate 4 con
evidenza esterna. Fino ad allora è infrastruttura interna che produce una demo.

---

## 7. Cosa farei, in ordine

```text
1. NON costruire un Method Agent.
   Generalizzare check-style-authority.mjs in check-proposal.mjs.
   Un giorno di lavoro, classe 0, testabile, esistente per analogia.

2. Il proposal record è un FILE nel repo (come exception-registry.md),
   non un oggetto in un database. Versionato, diffabile, leggibile da umano.
   Coerente con D-010 (il testo è source authority) e con NX-02
   (il bundle porta la propria ricetta).

3. Il verdetto dello script entra nel template di PR, come il --ci del design.
   Non serve un'interfaccia.

4. L'LLM bozza il record (classe 1). Lo script lo verifica (classe 0).
   L'umano decide. Tre attori, tre responsabilità, nessuna sovrapposizione.

5. Solo DOPO che ha girato su 5-10 proposte reali si valuta se esporlo
   via MCP come capability. Non prima: sarebbe esporre un'abitudine,
   non un contratto.
```

---

## 8. La formulazione che terrei

La proposta ne offre una forte:

> *"Open Nexus non usa gli agenti soltanto per costruire applicazioni. Usa metodi
> condivisi per governare ciò che gli agenti hanno il diritto di cambiare, e rende
> ogni decisione tracciabile."*

Va bene **come descrizione dell'infrastruttura interna**, non come pitch. La
versione che terrei, più onesta sullo stato:

```text
Foundation stabilisce cosa può essere costruito.
I metodi condivisi stabiliscono cosa ha il diritto di cambiare Foundation.
Uno script deterministico lo verifica.
Un agente lo propone. Una persona lo decide.
La traccia resta.
```

Cinque attori, nessuno dei quali è onnipotente. È la stessa struttura delle sei
authority: nessun singolo punto possiede la verità, ogni punto possiede una domanda.

---

## 9. Backlog

```text
NX-53  NUOVO P2 — check-proposal.mjs: generalizzazione di
       check-style-authority.mjs applicata ai proposal record.
       Classe 0, deterministico, --json/--ci, verdetto strutturato.
       PREREQUISITO: che sia passato almeno un ciclo di sonda reale.
       Non prima.

NX-54  NUOVO P1 — regola "evidenza esterna non può restare pending
       indefinitamente": staleness a N giorni → insufficient-evidence.
       Vale per il metodo Sonda anche SENZA lo script.

NX-55  NUOVO P3 — Method Agent come prodotto: vietato nominarlo prodotto
       finché il gate 4 non ha evidenza esterna.
```

**NX-53 è deliberatamente P2 e con prerequisito.** È la cosa più interessante fra
quelle non urgenti, che è esattamente il profilo di ciò che va tenuto indietro.

---

*Ultimo aggiornamento: 2026-09-13*
