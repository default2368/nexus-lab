# Trustable / Nuvolaris vs OpenFav · Open Nexus

**Data analisi:** 2026-09-10
**Fonte:** scrape diretto di `https://trustable.it` (home, sitemap.xml, documentation/setup, /edit, /config, /list, /chat, /template, architecture, apps)
**Natura:** analisi competitiva + estrazione di pattern riutilizzabili per Nexus Lab

---

## 0. SINTESI IN DIECI RIGHE

Trustable non è un competitor di Open Nexus. È un **workbench AI verticalizzato su
infrastruttura sovrana**: genera *applicazioni* (codice React + backend actions) dentro
starter Git, girando su Nuvolaris (Apache OpenWhisk + Kubernetes + Redis + Milvus +
SeaweedFS + PostgreSQL + Prometheus + Velero + Kafka).

Open Nexus genera e rappresenta **conoscenza** che *poi* si renderizza come applicazione,
con un pavimento contrattuale invariante (`PageData`, `normalizeToPageData`,
`ApplicationBundle`, `BundleCollector`, Runtime).

La differenza non è di features. È di **garanzia**:

- Trustable garantisce **dove gira** (sulla tua infrastruttura, niente esce).
- Open Nexus garantisce **cosa sopravvive** (il modello resta valido dopo la generazione).

Trustable ha risolto tre cose che tu non hai ancora risolto: **licensing, provider
abstraction, narrativa di scala**. Tu hai risolto una cosa che loro non hanno e che
non possono recuperare facilmente: **l'invarianza semantica**.

Da qui: ruba il licensing e la narrativa, non inseguire il workbench.

---

## 1. FATTI OSSERVATI (nessuna inferenza)

### 1.1 Identità e perimetro

```text
Nuvolaris = piattaforma cloud-native serverless completa
  ├── Kubernetes operator
  ├── CLI
  ├── Console (low-code)
  ├── Coding environment
  └── Trustable  ← "Trustable Private AI workbench"
```

Tagline home: **"Build Apps with Local AI on your PC"** — *"Customize and build full
stack applications with prompts, using Local, Private or Sovereign AI."*

Frase chiave: *"It is Nuvolaris technology inside the platform, not a third-party tool:
what it builds runs on your own stack, on your own hardware."*

Versione osservata nella doc: **V0.4.0 · MAIN**. I build Trustable hanno una
**data di scadenza**: oltre quella, l'app chiede di aggiornarsi.

### 1.2 Stack sottostante

Apache OpenWhisk come serverless engine. Servizi integrati dichiarati: Redis, Milvus
(vector DB), SeaweedFS (object storage S3), PostgreSQL, Prometheus, Velero, Kafka,
controller load-balanced, invoker multi-runtime. Deploy su public cloud, private cloud,
bare metal.

### 1.3 Il workbench

Due pane + toolbar:

- **Pane sinistro = TruACP** (Trustable Agent Control Panel). All'avvio riporta:
  `pi v0.82.0`, estensioni caricate, e **`MCP: 8 servers connected (126 tools)`**.
- **Pane destro = l'applicazione live**, non un mockup. Si aggiorna quando l'agente
  modifica codice.
- **Terminale reale** dentro la directory dell'app (pane inferiore, non sostitutivo).
- Message box duale: testo = istruzione all'agente; prefisso `!` = shell command.

Toolbar CONFIG: `Env` (dev/prod separati), `Skills` (abilità pronte clonate nell'app),
`AGENTS.md` ("instructions file the assistant reads before doing anything"; creato e
aggiunto a Git se non esiste).

Toolbar UTILS: `Revert`, `Reload` (solo preview), `Redeploy` (ciclo completo: stop dev
server → deploy backend actions → list → start → wait), `Clean` (rimuove venv,
node_modules, archivi; **non** rebuilda), `Debug` (log live in finestra separata),
`Files`.

### 1.4 Agenti e modelli

Selettore agente: **Claude Code**, **Codex**, **Pi**. Pi è il default.

Tabella modelli per provider con colonne: `MODEL`, `CONTEXT SIZE` (default 128.000),
`MAX OUTPUT` (default 32K), `FOR CODING` (`Available` / `Hidden` + motivo), `ACTIONS`.

Regola osservata: vengono nascosti dalla selezione coding i modelli di embedding,
rerank, vision, e quelli **sotto i 20B parametri minimi raccomandati**.

> *"the rule is enforced on the server too, not just in the browser, so it holds
> however you save."*

**Un solo modello coding configurabile.** Citazione esplicita: *"There is no separate
'small' or 'secondary' model to configure: one choice covers all agent work."*

La doc però ammette il bisogno: *"Switching model mid-project is a normal thing to do:
a larger model for architectural work, a faster one for small mechanical edits."*
→ lo risolvono a mano, per sessione. Non c'è routing automatico per classe di task.

### 1.5 Provider abstraction (3 carte)

| Carta | Cos'è | Serve |
|---|---|---|
| **Cloud AI** | Subscription, Ollama Cloud. Trustable parla al proprio server Ollama内置 che inoltra ai modelli cloud | Account Ollama Cloud gratuito |
| **Sovereign AI** | Credit-based, **Regolo.AI**, modelli hostati in EU | Account Trustable AI (100 crediti gratis) |
| **Private AI** | Qualsiasi endpoint OpenAI-compatible self-hosted (Ollama, vLLM, llama.cpp) | URL endpoint (deve finire in `/v1`) |

**Configuration pass** eseguito dopo la scelta: pull modelli → scrittura config runtime
per l'agente Pi → **probe live `"Reply with exactly: OK"`**. Solo se il probe passa si
procede. Un probe fallito rimanda sempre alla schermata provider.

Validazioni osservate degne di nota:
- Base URL rifiutato se non matcha `http(s)://…/v1`.
- Se URL `https://` e API key vuota → chiede conferma esplicita.
- Al SAVE interroga subito l'endpoint per la model list; endpoint rotto o con zero
  modelli **non viene mai salvato**.
- Se il provider pubblica un nuovo catalogo, Trustable lo rileva al successivo page
  load, salva la nuova lista e rimanda alla config con un banner che chiede di
  riselezionare il modello coding.
- Sovran AI: la registration page si apre **dentro** Trustable come overlay e
  restituisce endpoint + API key direttamente. *"you never copy and paste a key."*
- Se il probe fallisce più tardi (key scaduta/esaurita) → riapre lo stesso overlay.

### 1.6 Licensing — **la parte più interessante per te**

> *"A license enables **Git push and publishing to production**. Everything else —
> creating applications, editing them with the AI assistant, running them locally,
> committing to the local repository — works without one."*

Caratteristiche:
- Token con prefisso **`lic_`**.
- Verifica **completamente offline**: statement firmato, controllato contro una
  **public key incorporata** in Trustable. *"no network call and no license server
  is involved."*
- Codifica: **a chi** è stata emessa e quando; **expiry date** opzionale (valida per
  tutto il giorno indicato, invalida dal successivo); **lista di cluster host** verso
  cui è consentito pubblicare.
- Pubblicare verso un host non in lista è **rifiutato anche con licenza valida**.
- I cluster di sviluppo locale sono esenti dal check host, ma richiedono comunque
  licenza valida.
- Licenza scaduta disabilita sia Git push sia publishing.
- La card appare **solo se il licensing è abilitato sull'installazione**.

Tradotto: **source disponibile, uso locale libero, monetizzazione sul confine di
egress (push + publish verso infra controllata)**. Nessun license server da mantenere,
nessun phone-home, nessuna dipendenza di rete. Resiste anche offline/air-gapped,
che è coerente con la promessa sovereign.

### 1.7 Templates = contratto di workflow già prodotto

Definizione: *"A **template** is an ordered list of prompts — a recipe you run instead
of typing the same sequence of instructions again."*

Formato: **file Markdown ordinari su GitHub**, con `---` a separare un prompt
dall'altro.

Sorgente: repository GitHub configurabile, default **`trustable-ai/templates`**, branch
`main`. Un'applicazione singola può fare **override** del repository (uno starter può
portare il proprio set di template).

**Working copy**: il template caricato nell'app è un file reale, `template.md`, alla
root del checkout dell'app. *"a template travels with the application, is committed
with it, and is published with it, so the recipe that built an application stays with
that application."*

Badge **CHANGED** quando la working copy differisce dalla versione a catalogo — appare
con o senza token GitHub, deliberatamente, *"it is how you find out your edits are
local-only"*.

Save to GitHub con **controllo di concorrenza ottimistica**: verifica che il file non
sia cambiato su GitHub dal caricamento; se qualcuno ha pushato nel frattempo, **il
save viene rifiutato** invece di sovrascrivere.

Token GitHub **write-only**: mostra se esiste, non lo rivisualizza mai; campo vuoto =
mantieni quello salvato; spunta esplicita per rimuoverlo. Conservato come *protected
file* nel workspace, **mai nel file di configurazione condiviso**.

Stati step: **NOT RUN** / **RUNNING…** / **RUN**. Colore *e* nome (muted / amber /
green) per accessibilità. *"A step counts as run once it has produced output, which
means the states survive closing and resuming the session rather than resetting."*

Esecuzione:
- Run / Run next step / Run all steps (dalla selezione corrente alla fine).
- Gli step girano **strettamente uno alla volta**, condividono una singola sessione.
- Ogni prompt è **ri-letto al momento dell'esecuzione** (una modifica mid-run è la
  versione che gira).
- **Uno step fallito termina la run** invece di sparare i prompt restanti in uno stato
  rotto.
- `Stop` interrompe l'intera run e **lascia la selezione sullo step fermato**, così
  Run all steps riprende da lì.
- Durante la run: `AGENT RESPONSE` (con `Reasoning` sotto disclosure) + `ACTIVITY`
  (lista tool call in finestra scrollabile che segue l'ultima mantenendo lo storico).

Modifica: ogni step ha Run / Edit / Move / Remove. Move è keyboard-driven (frecce per
spostare, Enter committa e scrive la working copy, Esc ripristina e non scrive nulla).
Edit e Move sono modali su un singolo nodo. Nessuno dei due è offerto mentre uno step
gira.

Creazione: *"There is deliberately **no 'new template' form**."* Un template si crea
**promuovendo messaggi già inviati** — lo scrivi facendo il lavoro una volta e tenendo
i prompt che hanno funzionato.

Nota rivelatrice dal sample: un template finisce con *"Do not implement the pages"* —
*"templates are often written to constrain the assistant as much as to instruct it,
keeping each step to one reviewable change."*

E dal log di esempio: l'agente *"works out that the pages already exist and decides to
replace them with placeholders, because the prompt said not to implement them"*.

### 1.8 Applicazioni

Un'app = **repository Git**. Due vie di creazione:

1. **STARTER** — repo minimi convention-compatible mantenuti per Trustable:
   `truchat` (AI chat UI con RAG), `trudemo` (demo), `trureact` (React generico),
   `My Application Starter` (repo proprio, sempre ultima riga).
   Nome app: **6–20 caratteri alfanumerici, iniziale lettera**, no collisioni.
   Prefill del repo `org/repo` dallo starter. CREATE clona lo starter in un repo
   durevole proprio dell'app. Se lo starter dichiara env vars senza valore, Trustable
   chiede di compilarle prima di procedere.
   Gli starter sono scoperti da un **indice pubblicato**, non interrogando GitHub,
   quindi la lista è identica su ogni installazione. Se non carica, lo dice e lascia
   disponibile `My Application Starter`.
2. **Catalogo ready-made** — tab CHAT / DEMO / EXAMPLES / UTILITIES, carousel con una
   app alla volta, titolo linkato al repo GitHub, screenshot, descrizione. Collisioni
   di nome risolte col numero libero più piccolo (`tetris`, `tetris1`, `tetris2`).
   Un'app può stare in più gruppi; ogni entry crea dal **proprio** repository.

Le 13 app a catalogo:

```text
CHAT       Document Ingestion
DEMO       Kubernetes Manager · Security Checker · Tetris Game
EXAMPLES   API Status Monitor · Simple Productivity App suite · Mini CRM
           News Aggregator · Project Dashboard
UTILITIES  JSON Formatter · PostgreSQL Console · REDIS Console · URL MetaData
```

Home screen = App List con 4 bande: header (logo, prodotto, release tag `V0.4.0 · MAIN`
con branch/build label on-hover), summary row (APPLICATIONS / PRODUCTION / DEVELOPMENT
/ REPOSITORIES), card WORKBENCH INVENTORY (search + sort + view switch + 3 filtri
segmentati All / Production / Development only), footer (build identifier, expiry date,
hash dell'ops task set).

Pill **Credits** sotto il titolo solo con provider Sovereign AI, refresh ogni minuto.

### 1.9 Env vars condivise

> *"It is a **palette, not a source**... Nothing is applied automatically — you confirm
> them in the application's own environment editor."* *"A predefined value never
> silently reaches an application."*

### 1.10 Narrativa di scala

```text
One desk          → Local AI      (appliance NuvolarIA sulla scrivania)
One organization  → Private AI    (GPU server nel tuo rack, dietro il firewall)
One country       → Sovereign AI  (data centre come AI provider, tua giurisdizione)
```

Chiusa: *"Same platform, same applications, same tooling at every tier — only the
hardware underneath changes. **You are never migrating, only growing.**"*

---

## 2. MAPPA STRUTTURALE

| Trustable / Nuvolaris | Open Nexus / Foundation + X | Stato |
|---|---|---|
| Nuvolaris (OpenWhisk/K8s operator, CLI, Console) | **Foundation** — deterministic kernel | ✅ equivalente concettuale |
| Trustable workbench (TruACP + Pi + MCP) | **X** — AI-governed layer | ✅ equivalente concettuale |
| Starter repo / app repo | `ApplicationBundle` | ✅ hai il contratto, loro hanno solo Git |
| `template.md` (ordered prompts, `---`) | **manca** → Workflow Contract | ❌ gap tuo |
| Pane di preview live | Experience renderer | ⚠️ diverso: loro eseguono codice, tu esegui PageData |
| `MCP: 8 servers / 126 tools` | FastAPI + MCP server | ⚠️ loro più avanti sul conteggio |
| Provider a 3 carte + probe `Reply with exactly: OK` | `ModelProvider` / `HealthProbe` (da estrarre in PR #1) | ⚠️ loro spedito, tu progettato |
| Tabella modelli con `FOR CODING` enforced server-side | `ROUTING` matrix flash/pro | ✅ **tu più avanti** (loro: 1 modello solo) |
| Licenza `lic_` offline firmata, host allowlist | **strategia IP non decisa** | ❌ gap tuo, e loro hanno la risposta |
| Catalogo 13 app pronte | Reference validations (Simple / Open Nexus / Auth / Operations / System) | ✅ entrambi, finalità diverse |
| Local / Private / Sovereign | local dev → Vercel/Fly → ? | ❌ gap tuo di narrativa |
| `AGENTS.md` per-app, Skills, Env dev/prod | `.clinerules` + `AGENTS.md` globali | ⚠️ loro per-app, tu per-workspace |
| Build con expiry date | n/a | pattern loro |

---

## 3. DOVE SONO DAVANTI LORO (e cosa rubare)

### 3.1 Licensing offline firmato — **priorità massima**

Hanno risolto esattamente il problema su cui tu stai girando da settimane
(MIT vs BSL vs binary closed vs cloud-only) con una **risposta tecnica, non legale**:

```text
Tutto locale          → GRATIS, nessuna licenza
Git push              → licenza
Publish su cluster    → licenza + host in allowlist
Verifica              → offline, public key embedded, zero infrastruttura
```

Perché funziona per te:
- Non richiede di aprire il sorgente.
- Non richiede license server (costo zero, nessuna superficie di attacco).
- Funziona air-gapped → coerente con qualunque promessa sovereign tu voglia fare.
- Il confine di monetizzazione è **l'egress**, non l'uso. Un developer può provare
  tutto, il valore si paga quando esce dalla sua macchina.

**Porting su Nexus Lab:**

```text
nexus init / dev / build / preview locale   → free, nessuna licenza
nexus publish                               → licenza + host allowlist
nexus bundle export (distribuzione)         → licenza
Verifica                                    → Ed25519, public key nel binario CLI
Token                                       → nexus_lic_...
Payload                                     → who, issued_at, expiry, hosts[], tier
```

Questo ti dà **Foundation chiusa/source-available + CLI binaria firmata + X premium**
senza dover scegliere una licenza OSS e senza regalare l'intuizione architetturale.
Il kernel non esce; esce il contratto.

### 3.2 Provider abstraction già spedita

Conferma puntuale del PR #1 Brain Contract Extraction: interfaccia provider + probe
di salute + validazione dell'endpoint *prima* del salvataggio + rifiuto di persistere
config rotte. Loro fanno anche una cosa che tu non avevi previsto: **rilevare il
cambio catalogo del provider al page load e forzare la riselezione del modello**.

Da rubare:
- Validazione forma URL al save, non al primo errore runtime.
- Se `https://` e key vuota → conferma esplicita (è quasi sempre un errore).
- Interrogare il catalogo modelli al save; zero modelli = non salvare.
- Probe minimo `"Reply with exactly: OK"` come gate di usabilità, non di qualità.

### 3.3 Template come working copy dentro l'artefatto

`template.md` alla root del checkout, committato e pubblicato con l'app.
**La ricetta che ha costruito un'applicazione resta con quell'applicazione.**

Questo è un principio che vale anche per te ed è coerente con la tua invariante:

```text
Il bundle porta con sé la propria ricetta di generazione.
ApplicationBundle + workflow.md → versione, diff, riproducibilità.
```

Con un vantaggio tuo: se la ricetta sta nel bundle, allora
`BundleCollector` resta invariato e il Runtime non osserva il repository —
la ricetta è *contenuto*, non *dipendenza*.

Da rubare anche:
- **Concorrenza ottimistica sul save remoto** (rifiuta invece di sovrascrivere).
- **Badge CHANGED sempre visibile**, anche senza credenziali: dice all'utente che le
  sue modifiche sono local-only. Onestà di stato > UI che sembra funzionare.
- **Token write-only**, mai riverificato, mai nel file di config condiviso.
- **Nessun form "nuovo template"**: si crea promuovendo messaggi già inviati.
  → Per X: nessun form "nuovo workflow", si crea promuovendo operazioni riuscite.

### 3.4 Semantica degli step

```text
NOT RUN / RUNNING / RUN   (colore + nome, non solo colore)
stato persiste attraverso chiusura e ripresa sessione
prompt ri-letto al momento dell'esecuzione
step fallito → termina la run
Stop → selezione resta sullo step fermato → resume da lì
```

È una specifica di workflow runner già collaudata sull'utente. Copiala quasi verbatim
nel Workflow Contract di X, **aggiungendo quello che a loro manca** (vedi 4.3).

### 3.5 Narrativa di scala a tre tier

*"You are never migrating, only growing"* è la frase più forte di tutto il sito.
Tu non hai un equivalente. Il tuo sarebbe:

```text
One repository   → local: nexus dev, zero infrastruttura
One team         → hosted: Vercel/Fly, bundle pubblicati
One organization → sovereign/self-hosted: engine firmato, host allowlist
```

Stessa piattaforma, stessi contratti, stesso Runtime. Cambia solo sotto.

---

## 4. DOVE SEI DAVANTI TU (e perché è difendibile)

### 4.1 Loro non hanno un pavimento semantico

Il loro agente scrive codice arbitrario dentro uno starter React. Non esiste un
contratto che sopravviva alla generazione. La loro stessa doc lo mostra: l'agente
*"decides to replace them with placeholders"* — cioè **riscrive pagine esistenti**
perché un prompt glielo ha chiesto in un certo modo.

Non c'è `PageData`. Non c'è `normalizeToPageData`. Non c'è niente che dica
*"questo è il linguaggio, i renderer cambiano"*.

La loro garanzia è **infrastrutturale**: *niente esce dalla tua infra*.
La tua è **semantica**: *il modello resta valido dopo quattro stratificazioni*.

Sono garanzie ortogonali. La loro si compra con l'hardware. La tua si compra con
gli anni di refactoring — e infatti le tue vecchie suite girano ancora all'80%.
**Quello non è nostalgia, è l'unico asset che non si può clonare in un weekend.**

### 4.2 Loro generano codice, tu generi conoscenza

Output Trustable: un repo React + backend actions che **poi devi manutenere tu**.
Output Open Nexus: `PageData` che **sopravvive ai renderer**.

Conseguenza economica: il loro prodotto ha un costo di manutenzione che cresce con
il numero di app generate (ogni app è codice divergente). Il tuo ha un costo che
cresce con il numero di *contratti*, non di pagine. È la differenza fra vendere
mattoni e vendere la forma.

### 4.3 Il gate deterministico — **il vero vuoto**

Rileggi la definizione di step eseguito:

> *"A step counts as run once it has **produced output**."*

Prodotto output ≠ output corretto. Non esiste nessuna validazione dell'artefatto
prodotto. Instruqt ha `check-host` (script di verifica). Trustable non ha nulla di
equivalente. Un template che sbaglia allo step 2 *"will otherwise keep building on
that mistake through step five"* — lo scrivono loro, come avvertimento all'utente.

Tu hai già la CLI che fa **estrazione tokens** e validazione dei contratti.
Quello è il gate che manca a entrambi i tuoi riferimenti di mercato.

```text
Trustable:  prompt → agente → output            (nessuna verifica)
Instruqt:   step → check-host → gate            (verifica, ma dominio chiuso ai lab)
Nexus:      prompt → agente → Bundle → VALIDATE → gate contrattuale
                                  ↓
                          BundleCollector invariato
                                  ↓
                            Runtime invariato
```

**"Indeterminismo che diventa determinismo con Foundation"** non è uno slogan:
è esattamente il buco che Trustable ha nel mezzo del suo prodotto principale.

### 4.4 Routing per classe di task

Loro: **un solo modello coding**, cambio manuale per sessione, e la doc stessa
consiglia *"a larger model for architectural work, a faster one for small mechanical
edits"*. Cioè riconoscono il bisogno e lo lasciano all'utente.

Tu: `deepseek-flash` di default per extraction/audit/retrieval,
`deepseek-v4-pro` come gate per giudizio architetturale e commit complessi.
Con `ROUTING` per classe di task e `MAX_OUTPUT_TOKENS` per classe.

È più sofisticato. Diventa un vantaggio di costo misurabile nel momento in cui
loro pagano un modello grande per operazioni meccaniche.

Nota di coerenza: anche loro **nascondono i modelli di embedding dalla selezione
coding** e li mostrano comunque in tabella. È lo stesso istinto del tuo principio
*"Il testo è source authority. L'embedding è una proiezione, mai una fonte."*
Due team indipendenti arrivati alla stessa conclusione = la conclusione è giusta.

### 4.5 Invarianza testata nel tempo

Non hanno nessuna storia equivalente alle tue 4 stratificazioni architetturali con
le suite che reggono all'80%, perché **non hanno un'invariante da preservare**.
Le loro app sono rigenerabili e quindi sacrificabili. Le tue no.

---

## 5. LEZIONI NON TECNICHE

### 5.1 La doc è il prodotto

Ogni pagina di `trustable.it/documentation/` spiega **perché** una cosa è fatta in
quel modo, non solo come:

- *"That is deliberate: a template travels with the application..."*
- *"The badge appears whether or not a GitHub token is configured, **on purpose**"*
- *"Cancel returns to the carousel rather than closing the dialog, **because** you are
  choosing, not aborting."*
- *"Redeploy is in this menu **on purpose**: the toolbar reaches it only through a
  modifier key, so this is the discoverable path to it."*
- *"Only Enter writes, which is what makes Esc a true cancel rather than a second edit."*

Questa è documentazione che **difende le decisioni**. È esattamente la forma del tuo
`NEXUS-recap-ufficiale.pdf` (Validato / Debito / Roadmap). Stesso istinto. Tu lo fai
per te, loro lo pubblicano. **Pubblicare il ragionamento è una barriera competitiva**:
un clone può copiare le features, non può copiare il perché — e senza il perché
reintroduce i bug che tu hai già risolto.

### 5.2 Onestà sul debito come asset di marketing

Dicono esplicitamente cosa **non** fa una funzione:

> *"Note what it does **not** do: it does **not** rebuild. Cleaning stops the dev
> server, so the preview goes down and stays down until you redeploy."*

> *"It asks for confirmation, and it means what it asks: reverting removes untracked
> new files as well as edits. Anything not committed is gone."*

È la stessa postura del tuo recap: *"Non dimostra sincronizzazione auth cross-tab
real-time."* Chi dichiara i limiti sembra più affidabile di chi non ne ha. Per un
prodotto che si chiama **Trustable**, è coerente. Per un prodotto che si chiama
**Nexus**, vale uguale.

### 5.3 Il catalogo come indice pubblicato, non come query live

*"Starters are discovered from a published index rather than by querying GitHub, so
the list is identical on every installation."*

Determinismo dell'esperienza di scoperta. È la tua stessa filosofia applicata alla
onboarding: niente dipende dallo stato di un servizio terzo a runtime.

---

## 6. POSIZIONAMENTO NEXUS LAB

### 6.1 Cosa NON fare

- **Non costruire contro Trustable.** Un prodotto costruito per dimostrare qualcosa a
  una persona specifica sceglie le feature in funzione di un pubblico di uno. È la
  strada più rapida per costruire la cosa sbagliata molto bene.
- **Non posizionarti pubblicamente come "quello che Trustable non è".** Regali a loro
  la cornice e fai leggere il progetto come risentimento.
- **Non inseguire il workbench.** Due pane + terminal + live preview + 126 tool MCP è
  un lavoro da team con una piattaforma serverless sotto. Non è la tua battaglia e non
  è dove sta il tuo vantaggio.

### 6.2 Cosa fare

Il segnale di mercato è adesso **doppio e indipendente**:

```text
Instruqt    → valida "knowledge as experience"  (SaaS chiuso, enterprise, adozione)
Nuvolaris   → valida "sovereign AI workbench"   (infra privata, licensing offline)
```

Due aziende con soldi e clienti hanno confermato due metà della tua intuizione.
Nessuna delle due ha la **terza** metà: il contratto deterministico che sta in mezzo.

Posizionamento proponibile:

> **Nexus Lab — il contratto fra l'AI che genera e il sistema che esegue.**
> Foundation produce, Execution esegue. PageData is the language of knowledge experiences.

Non "un altro app builder". Non "un altro CMS". Il **pavimento** su cui gli app
builder e i knowledge builder possono generare senza rompere l'invariante.

### 6.3 Sequenza suggerita

```text
1. Licenza offline firmata (Ed25519, nexus_lic_, host allowlist)
   → sblocca la distribuzione senza aprire il kernel
2. Workflow Contract dentro il bundle (workflow.md) + gate VALIDATE
   → è il buco di Trustable E di Instruqt
3. Narrativa a tre tier (repository / team / organization)
   → asset di marketing, costo quasi zero
4. Doc pubblica che difende le decisioni
   → barriera competitiva reale
```

### 6.4 Avvertenza pratica sul nome

Prima di investire nel brand **Nexus Lab**: verifica collisioni. "Nexus" è usato da
Sonatype Nexus Repository, da una lunga storia di prodotti Google, e Nuvolaris stessa
ha un ecosistema di naming proprio (`tru*`, `NuvolarIA`). Un check su EUIPO / UIBM
(Toscana→Italia: Ufficio Italiano Brevetti e Marchi) costa poco rispetto al costo di
rinominare dopo. Vale anche per `Open Nexus` vs `OpenFav`: decidere **ora** quale dei
due è il nome pubblico evita di dover migrare SEO, repo e identità più tardi.

---

## 7. BACKLOG DERIVATO

| ID | Azione | Priorità | Origine |
|---|---|---|---|
| NX-01 | Spec licenza offline firmata per Nexus CLI (Ed25519, `nexus_lic_`, host allowlist, expiry, tier) | **P0** | § 3.1 |
| NX-02 | Workflow Contract: `workflow.md` dentro `ApplicationBundle`, stati step, failed-step-ends-run, resume | **P0** | § 3.3, 3.4 |
| NX-03 | Gate `VALIDATE` fra generazione e `BundleCollector` (il buco di Trustable) | **P0** | § 4.3 |
| NX-04 | Provider abstraction Brain: validazione URL al save, catalogo modelli, probe `OK`, rilevamento cambio catalogo | P1 | § 3.2 |
| NX-05 | Regola enforced server-side, non solo client (pattern `FOR CODING`) | P1 | § 1.4 |
| NX-06 | Concorrenza ottimistica sul save remoto dei contratti | P1 | § 3.3 |
| NX-07 | Narrativa tre tier + pagina pubblica | P2 | § 3.5, 6.2 |
| NX-08 | Doc pubblica che difende le decisioni (formato "deliberate / on purpose / because") | P2 | § 5.1 |
| NX-09 | Indice pubblicato per starter/bundle, non query live | P2 | § 5.3 |
| NX-10 | Verifica collisioni marchio Nexus Lab / decisione nome pubblico | P2 | § 6.4 |

Nessuna voce di questo backlog tocca `PageController`, `normalizeToPageData`,
`ApplicationDefinition`, `ApplicationContext`, `BundleCollector`, `DiscoveryService`.
NX-02 e NX-03 sono **X**, non Foundation.

---

*Fine dossier.*
