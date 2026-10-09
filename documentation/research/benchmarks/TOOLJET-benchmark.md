# ToolJet — benchmark architetturale e lezione di distribuzione

**Data analisi:** 2026-09-10
**Fonti:** `github.com/ToolJet/ToolJet` (README, albero repo, `.agents/skills`,
`.claude/skills`, commit history), `docs/versioned_docs/version-3.0.0-LTS/contributing-guide/setup/architecture.md`,
`blog.tooljet.ai/migrating-toojet-from-ruby-on-rails-to-nodejs`,
`tooljet.com/tooljet-vs-appsmith`, `claudepluginhub.com/plugins/tooljet-tooljet-app-builder`

**Metriche:** 40.9k star · 5.4k fork · 17.447 commit · 1.366 branch · 744 tag

---

## 0. Perché questo file esiste

La tesi dell'utente: *"questo mi sembra quello che si avvicina a Foundation"*.

**Confermato, e oltre.** ToolJet non somiglia a Foundation: ToolJet **è** un sistema
Foundation + X già industrializzato, già venduto, già agent-native. Con una differenza
architetturale singola e decisiva che è esattamente il moat di Open Nexus.

---

## 1. Identità

### 1.1 Descrizione del repository

> *"**Open-source foundation of ToolJet AI** - the enterprise app generation platform
> for internal tools, dashboards, business applications, workflows and AI agents.
> Build visually, from a prompt, or from Claude Code, Codex and Cursor over MCP"*

Traduzione nella tua lingua:

```text
ToolJet (repo pubblico, AGPL)   = FOUNDATION
ToolJet AI (Enterprise)         = X
MCP server (repo separato, MIT) = il contratto fra i due
```

### 1.2 Il passaggio del README che è la tua tesi

> *"Build them by prompting. ToolJet AI turns a description into pages, queries, and
> components, and the coding agent you already use can do the same through ToolJet's
> MCP server. **Agents build against ToolJet's real component and data contracts
> rather than emitting free-form code**, so what you get is an actual ToolJet app: one
> your team keeps editing in the visual builder, under the same permissions,
> environments, and version history as everything else."*

Mappatura:

| ToolJet | Open Nexus |
|---|---|
| *"real component and data contracts rather than emitting free-form code"* | *"indeterminismo che diventa determinismo con Foundation"* |
| *"an actual ToolJet app"* | `ApplicationBundle` valido |
| *"same permissions, environments, version history"* | `ApplicationContext`, `ApplicationDefinition` |
| *"keeps editing in the visual builder"* | Experience renderer |

**Non è somiglianza. È la stessa proposizione architetturale, scritta indipendentemente.**

Differenza di dominio: ToolJet fa **internal tools** (admin panel, dashboard, CRUD su
database esistenti). Open Nexus fa **knowledge experiences**. Stesso meccanismo,
mercato diverso — il che lo rende benchmark, non minaccia.

---

## 2. Architettura (fatti)

### 2.1 Due componenti

```text
ToolJet Server   Node.js / NestJS / TypeORM / PostgreSQL
                 "authentication, authorization, persisting application definitions,
                  running queries, storing data source credentials securely"
                 Dipendenze: PostgreSQL, servizio email (SMTP/Sendgrid/Mailgun),
                 PostgREST opzionale (per ToolJet Database)

ToolJet Client   ReactJS
                 "visually editing the applications, building & editing queries,
                  rendering applications, executing events and their trigger"
```

### 2.2 Il ciclo di vita della definizione

Dal blog ufficiale sulla migrazione da Rails a Node:

> *"Whenever a new application is built using ToolJet, the frontend (client) generates
> the definition of the app in JSON and the server persists the **versioned definitions**
> on a PostgreSQL database."*

```text
Builder React → JSON definition → Server → PostgreSQL (app_versions)
                                              ↓
                            Client React interpreta e renderizza
```

Motivo storico della migrazione a NestJS: un plugin richiedeva **due linguaggi**
(Ruby per eseguire le query, JS per gli editor). Con NestJS un solo linguaggio.
Lezione: *il costo di estensione deve essere a un linguaggio solo.*

### 2.3 Struttura del repo

```text
.agents/skills/     skill per agenti (pubbliche + symlink a EE)
.claude/skills/     symlink per Claude Code
cli/                ToolJet CLI (@tooljet/cli su npm)
cypress-tests/
deploy/  docker/
docs/
frontend/           (contiene il submodule ee/ privato)
marketplace/
plans/              ← piani di lavoro versionati nel repo
plugins/            90+ data source
queryPanel/
release-scripts/
scripts/            (incluso sync-skills.sh)
server/             NestJS
```

### 2.4 Workflow come tipo di app

Dalla commit history: i workflow sono righe in `app_versions` con `type='workflow'`.
Condividono tabella, versioning, slug, import/export con le app. Non sono un sistema
separato: sono **un tipo di definizione**.

---

## 3. LA DIFFERENZA DECISIVA: nessun build step

### 3.1 Confronto

```text
ToolJet
  Definition (JSON) → PostgreSQL → Client React interpreta a RUNTIME
  ─────────────────────────────────────────────────────────────
  Nessuna compilazione. Nessun boundary. La definizione È l'input del runtime.

Open Nexus
  ApplicationBundle → BundleCollector → Build Artifacts → [boundary]
    → ApplicationDefinition → ApplicationContext → Discovery
    → PageData → Template → Experience
  ─────────────────────────────────────────────────────────────
  Compilazione esplicita. Boundary di invarianza. Il runtime consuma ARTEFATTI.
```

### 3.2 Cosa guadagnano

- Editing istantaneo, nessuna deploy
- Multiplayer editing (stessa definizione, più editor)
- Le app sono righe di DB: backup, clone, export banali
- Versioning nativo (`app_versions`)

### 3.3 Cosa pagano — e le prove sono nei commit

Quando la definizione è **dato vivo** invece di **artefatto compilato**, ogni cambio
di schema è una migrazione live sui dati di tutti i clienti.

Evidenza diretta, dalla commit history recente (feature Workflow Meta):

> *"Workflows never carry a branch_id, but the already-merged
> `MakeAppVersionBranchIdNotNullAndGitSyncFlags` migration made branch_id a
> column-level NOT NULL for every app type, **breaking workflow creation outright**.
> Replace it with a trigger that exempts `type='workflow'` rows..."*

E a cascata nello stesso commit:

```text
· trigger di esenzione NOT NULL per type='workflow'
· trigger di slug uniqueness + backfill
· stop auto-fill di apps.slug per i workflow
· metadata spostate da apps.* ad AppVersion
· reject delle collisioni di slug invece di evict silenzioso
· rimozione di overlay guard specifiche per workflow da AppsRepository e VersionRepository
· collisione di DI token su VersionRepository (getRepositoryToken su subclass di
  Repository registrava un secondo provider malformato che vinceva i lookup globali)
· stessa collisione su RolesRepository in TooljetDbModule
· unificazione import/export metadata via __importMetadata staging
· performLegacyAppImport come percorso separato
· ability check che leggevano isPublic/name dalla riga sbagliata
```

**Un solo commit tocca ~12 sottosistemi.** Non è disordine: è il costo strutturale
dell'assenza di boundary. Ogni nuovo tipo di definizione richiede di negoziare con
uno schema DB condiviso e con tutti i dati esistenti.

### 3.4 La stessa cosa in Open Nexus

```text
ToolJet    cambio di schema → migrazione live su tutti i dati dei clienti
Open Nexus  cambio di schema → ricompilazione dei bundle
```

Questo è **il** vantaggio competitivo, ed è misurabile in complessità di commit.

Corollario importante: il **migration engine** che in `04-FOUNDATION-API.md` § 5
indicavo come moat, per ToolJet non è un moat — è una **tassa permanente**. Loro lo
pagano a ogni release. Tu non lo paghi se resti sul modello compilato.

### 3.5 Il rovescio della medaglia (onestà)

Il modello compilato ha un costo reale che ToolJet non ha:

```text
ToolJet    l'utente modifica → vede subito
Open Nexus  l'utente modifica → ricompila → vede
```

Mitigazione già prevista in `04-FOUNDATION-API.md`: `nexus dev` con artifacts cached
e ricompilazione solo dei bundle cambiati (`content_sha`). Ma va progettata
esplicitamente, non data per scontata.

---

## 4. LA LEZIONE DI DISTRIBUZIONE: tre licenze, tre scopi

Questa è la risposta alla domanda Q-001 del Decision Log, e arriva da chi l'ha già
risolta in produzione.

### 4.1 Lo schema

```text
┌─────────────────────────────────────────────────────────────────────┐
│ 1. PIATTAFORMA          AGPL-3.0                                    │
│    repo ToolJet/ToolJet                                             │
│    → copyleft forte: chi fa fork e lo offre come SaaS DEVE aprire   │
│    → è il meccanismo anti-clone                                     │
├─────────────────────────────────────────────────────────────────────┤
│ 2. ENTERPRISE           repo privato, submodule git                 │
│    frontend/ee  (anche server/ee)                                   │
│    → il codice premium NON ENTRA nel repo pubblico                  │
│    → SOC 2, ISO 27001, GDPR, RBAC, SCIM, GitSync, white-label       │
├─────────────────────────────────────────────────────────────────────┤
│ 3. MCP SERVER           MIT (tooljet.com) / ISC (ClaudePluginHub)   │
│    repo ToolJet/tooljet-mcp, v0.3.0, ~50 build tools                │
│    → licenza MASSIMAMENTE permissiva                                │
│    → perché non è il moat: è la PORTA D'INGRESSO                    │
└─────────────────────────────────────────────────────────────────────┘
```

**Nota di precisione:** tooljet.com dichiara il MCP server **MIT**, ClaudePluginHub
riporta **ISC**. Discrepanza da verificare sul repo `ToolJet/tooljet-mcp` prima di
citarla.

### 4.2 Perché il MCP è permissivo e la piattaforma è AGPL

Sembra contraddittorio. È calcolato:

```text
Il MCP server non contiene valore proprietario:
  espone API governate + cataloghi generati di componenti e data source

Il valore sta:
  nella piattaforma che le esegue  → AGPL, protetta
  nelle feature enterprise         → private
```

Regola estraibile:

> **Rendi permissivo ciò che ti porta utenti. Rendi protetto ciò che li serve.**

### 4.3 Il layout dei symlink — dettaglio tecnico geniale

Dal commit *"standardise skill placement and symlink layout"*:

> *"Skills live in one of two places **by sensitivity**: public ones as real
> directories in `.agents/skills`, private ones in the `frontend/ee` submodule.
> Root `.agents/skills` links each private skill (Cursor/Codex) and `.claude/skills`
> links every root entry (Claude Code), so all skills are invokable from repo root
> in every harness **without touching EE files**."*
>
> *"`scripts/sync-skills.sh` reconciles links idempotently; `--check` mode runs in
> pre-commit and tolerates clones without the EE submodule."*

Osservato in `.agents/skills/`:

```text
directory reali (pubbliche)   commit · create-pr · manage-skills · merge
symlink (verso EE)            bug-triage · codebase-question · create-issue
                              manage-dependabot-alerts · page-load-audit
```

**Perché è rilevante per te:** risolve esattamente il problema D-014 (strategia
fuori dal repo) in modo più elegante. Non "due memorie separate" ma **un solo albero
di lavoro con zone a sensibilità diversa collegate da symlink**, e uno script
idempotente che le riconcilia e tollera cloni senza il submodule privato.

Applicabile a `NEXUS-LAB/`: repo pubblico con `docs/` tecnico, submodule privato per
strategia/EE, symlink che rendono tutto invocabile dalla root.

### 4.4 Pricing osservato

```text
Free        $0
Starter     $29/mese
Pro         $79/mese
Team        $199/mese
Enterprise  da $3.000/mese
```

Il salto Team → Enterprise è 15×. È lì che stanno i soldi veri, ed è lì che sta il
codice nel submodule privato.

---

## 5. LA BOMBA ECONOMICA: modello portato dall'utente

Da `tooljet.com/tooljet-vs-appsmith`:

> *"Or let Claude Code, Codex or any MCP client compose it over the MIT-licensed MCP
> server, verified in a browser, **with no credits**."*

E dal README:

> *"operations run on **your own model subscription** rather than drawing down ToolJet
> AI credits."*

### 5.1 Cosa significa

```text
Percorso ToolJet AI (built-in)
  utente → ToolJet → GPT/Claude/Gemini/Grok → ToolJet PAGA i token → crediti

Percorso MCP
  utente → Claude Code / Codex / Cursor → tooljet-mcp → API ToolJet
           ↑
           il modello lo paga L'UTENTE con la sua subscription
           ToolJet paga ZERO token
```

**ToolJet ha due percorsi di generazione AI con strutture di costo opposte.**
Il percorso MCP ha costo marginale LLM **nullo** e contemporaneamente è quello che
gli agenti preferiscono, perché usano il modello che già pagano.

### 5.2 Impatto diretto sulla tua strategia costi

Il tuo Brain FastAPI oggi paga DeepSeek. Questo è il modello "ToolJet AI built-in":
**tu paghi i token.**

Ma se esponi Nexus via MCP con i contratti:

```text
Roo Code / Claude Code / Codex dell'utente
        ↓  (modello suo, costo suo)
   nexus-mcp  →  Foundation API (compile / validate / publish)
        ↓
   tu paghi solo compute, non intelligenza
```

Il vincolo **< 10 €/mese** smette di essere un vincolo e diventa la norma, perché il
costo dell'intelligenza si sposta sull'utente. E la tua CLI già fa estrazione token:
è già un tool MCP-shape.

**Correzione al Decision Log:** D-009/D-010 trattavano il Brain come il posto dove
sta l'AI. ToolJet suggerisce che il Brain dovrebbe essere il **contract server**, e
l'AI può essere quella dell'agente dell'utente. Non sono alternativi: sono due
percorsi con due strutture di costo, esattamente come ToolJet AI vs ToolJet MCP.

### 5.3 Autenticazione osservata

```toml
[mcp_servers.tooljet]
command = "node"
args = ["/absolute/path/to/tooljet-mcp/bundle/index.js"]

[mcp_servers.tooljet.env]
TOOLJET_DEPLOYMENT_URL = "https://your-instance.tooljet.com"
TOOLJET_PAT = "tj_pat_..."
# TOOLJET_URL = "https://api.your-instance.tooljet.com"   # se API su altra origin
```

Conferma puntuale della spec NX-01b:
- **Personal Access Token** con prefisso riconoscibile (`tj_pat_`) → il tuo `nexus_`
- **Deployment URL** → l'istanza è dell'utente, self-hosted o cloud
- **Origin API separabile** dall'origin dell'app → stessa separazione di D-011

### 5.4 Distribuzione del MCP come plugin

```text
tooljet-mcp è un repo AUTO-CONTENUTO che è anche il proprio marketplace:
  .codex-plugin/plugin.json     manifest Codex
  .mcp.json                     lancia bundle/index.js senza install né build
  .agents/plugins/marketplace.json   "makes the repo its own marketplace"

installazione:
  codex plugin marketplace add ToolJet/tooljet-mcp --ref main
  codex plugin add tooljet-app-builder@tooljet

supporta anche Streamable HTTP
```

Da rubare: **`bundle/index.js` precompilato, nessuna build richiesta dall'utente.**
È esattamente il "binary engine" della discussione IP, applicato al solo componente
che può permettersi di essere aperto.

### 5.5 I cataloghi generati

> *"It includes **generated component and datasource catalogs** so agents use
> first-party contracts instead of guessing configuration keys."*

**Generati**, non scritti a mano. È NX-09 (indice pubblicato) + NX-11 (projection
come artefatto) nella stessa frase: il catalogo è un artefatto prodotto dal sistema,
non una tabella hardcodata. È la conferma esterna della tesi P-006.

---

## 6. Cultura agent-native dello sviluppo

Non è solo prodotto: **sviluppano con gli agenti e lo versionano.**

Commit osservati:

```text
Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01BcVhvZgAz9J6KWfeAR7iY5
```

Skill nel repo, cioè **il loro workflow di sviluppo reso eseguibile da un agente**:

```text
commit       → come si scrive un commit
create-pr    → template del corpo PR; "Forbid footers and attribution lines outside
               the template, and make How to test conditional so docs/tooling PRs
               don't carry an empty checklist"
merge
manage-skills → "covers moving skills between root and EE and repairing links"
bug-triage
codebase-question
create-issue
manage-dependabot-alerts
page-load-audit
```

E la qualità dei messaggi di commit è altissima: quello su Workflow Meta spiega
*perché* ogni fix è necessaria, inclusa la diagnosi della collisione di DI token
(`getRepositoryToken()` su una subclass di `Repository` restituisce la classe stessa
come token, registrando un secondo provider malformato che vinceva i lookup globali).

**È esattamente NX-08** (doc pubblica che difende le decisioni), applicato ai commit
invece che alla doc. E conferma `03-WORKFLOW.md` § 6: il loop manuale va
strumentalizzato. Loro l'hanno fatto — e hanno reso pubblico **solo il layer di
processo**, non l'architettura.

Nota: `plans/` in root. Tengono i piani nel repo. Tu tieni `NEXUS-LAB/` fuori.
Entrambe scelte legittime; la differenza è che i loro piani sono di esecuzione, i
tuoi contengono strategia di licensing.

---

## 7. Tabella di confronto completa

| Dimensione | ToolJet | Open Nexus | Vantaggio |
|---|---|---|---|
| Modello | Definition JSON in Postgres, interpretata a runtime | Bundle → Artifacts → boundary → Runtime | **Open Nexus** (invarianza) |
| Cambio di schema | migrazione live su tutti i dati | ricompilazione | **Open Nexus** |
| Feedback loop | istantaneo | richiede build | **ToolJet** |
| Multiplayer editing | sì, nativo | non previsto | **ToolJet** |
| Contratti per agenti | cataloghi componenti/datasource **generati** | PageData / ApplicationDefinition | pari, loro più avanti |
| MCP | ~50 tool, repo MIT dedicato, plugin Codex | server MCP nel Brain, non esposto come prodotto | **ToolJet** |
| Costo LLM authoring | **zero** (BYO model via MCP) | tu paghi DeepSeek | **ToolJet** |
| Licenza piattaforma | AGPL-3.0 | **non decisa** (Q-001) | **ToolJet** |
| Licenza agent entry | MIT/ISC, repo separato | inesistente | **ToolJet** |
| Codice EE | submodule git privato + symlink | inesistente | **ToolJet** |
| Dominio | internal tools, CRUD, dashboard | knowledge experiences | ortogonali |
| Motore di migrazione | tassa permanente | non necessario | **Open Nexus** |
| Versioning | `app_versions` in DB | Bundle in git | pari, filosofie opposte |
| Workflow | tipo di app in `app_versions` | NX-02, non costruito | **ToolJet** |
| Maturità | 40.9k star, 17.447 commit, SOC 2/ISO 27001 | pre-1.0 | **ToolJet** |

**Lettura:** ToolJet vince su tutto ciò che è **distribuzione, adozione, agent
integration**. Open Nexus vince su tutto ciò che è **invarianza architetturale**.

Non sono in competizione sulle stesse righe della tabella. Il che significa che
puoi copiare le loro righe vincenti **senza toccare le tue**.

---

## 8. Cosa rubare

```text
1. Tre licenze, tre scopi
   piattaforma AGPL/source-available · EE submodule privato · MCP permissivo
   → chiude Q-001

2. BYO model via MCP
   il contract server non paga l'intelligenza
   → ristruttura la strategia costi del Brain

3. Cataloghi GENERATI, non hardcodati
   conferma esterna di P-006 / NX-11

4. PAT con prefisso (tj_pat_) + deployment URL + origin API separabile
   conferma NX-01b e D-011

5. MCP come repo autonomo che è anche il proprio marketplace
   bundle precompilato, zero build per l'utente

6. Symlink per sensibilità (pubblico/EE) + sync script idempotente con --check
   risolve D-014 meglio di "due memorie separate"

7. Skill di processo nel repo (commit, create-pr, merge, manage-skills)
   → NX-02 applicato al tuo stesso sviluppo

8. Commit message che difendono la decisione
   → NX-08, ma nei commit invece che nella doc
```

## 9. Cosa NON copiare

```text
1. Il modello a interpretazione runtime.
   È la loro tassa permanente, non il loro vantaggio. Tu hai il boundary: tienilo.

2. Un solo schema DB condiviso per tutti i tipi di definizione.
   La commit history mostra il costo. Se NX-02 introduce workflow, non metterli
   nella stessa tabella delle page: bundle separati, contratti separati.

3. Costruire il visual builder.
   80+ componenti drag-and-drop è lavoro da team. Il tuo utente è un agente,
   non un operatore che trascina rettangoli.

4. Il dominio internal tools.
   CRUD su database esistenti è un mercato affollato (Retool, Appsmith, Budibase).
   Knowledge experiences no.
```

---

## 10. Deltas sul backlog

```text
NX-01b   CONFERMATO e rafforzato. Il pattern PAT + deployment URL è validato
         in produzione da ToolJet.
         AGGIUNGERE: percorso BYO-model (costo LLM zero) accanto al percorso
         Brain-paga-token.

NX-01    RICALIBRATO. ToolJet non usa licenza offline firmata: usa AGPL + EE
         submodule + cloud. NX-01 resta valido per il track on-prem/air-gapped,
         ma il track principale potrebbe essere AGPL/source-available + EE.
         → Q-001 ha ora un'opzione concreta in più.

NX-02    RAFFORZATO. ToolJet ha i workflow come tipo di app in app_versions.
         Lezione: NON fare lo stesso (vedi § 9.2).

NX-09    CONFERMATO. I cataloghi ToolJet sono generati, non scritti a mano.

NX-11    CONFERMATO da evidenza esterna: "generated component and datasource
         catalogs so agents use first-party contracts instead of guessing".
         È esattamente projection-come-artefatto.

NX-14    NUOVO — nexus-mcp come repo separato, licenza permissiva, bundle
         precompilato, ~N tool, plugin per Claude Code/Codex/Cursor.

NX-15    NUOVO — layout a sensibilità: repo pubblico + submodule EE + symlink
         + sync script idempotente con --check in pre-commit.

NX-16    NUOVO — skill di processo nel repo (commit, create-pr, merge) per
         strumentalizzare il loop di § 03-WORKFLOW.md.

NX-17    NUOVO — cataloghi di template/renderer GENERATI dal BundleCollector
         ed esposti via MCP, perché gli agenti non indovinino i contratti.
```

Nessuna delle nuove voci tocca `PageController`, `normalizeToPageData`,
`ApplicationDefinition`, `ApplicationContext`, `BundleCollector`, `DiscoveryService`
o `PageData`. **Restano tutte in zona sicura.**

---

## 11. La domanda strategica che ne esce

ToolJet impiega un team, ha 17.447 commit, SOC 2, ISO 27001, e ha comunque scelto
di **regalare il livello MCP** per vincere l'adozione degli agenti.

Tu sei solo, con < 10 €/mese e una CLI che estrae token.

```text
Loro possono permettersi di regalare il MCP perché vendono Enterprise a $3.000/mese.
Tu puoi permetterti di regalare il MCP perché ti costa zero — se l'AI la porta l'utente.
```

**Il percorso MCP non è una feature. È l'unico percorso di distribuzione che un
progetto singolo può sostenere economicamente.** E tu ce l'hai già a metà: la CLI,
il server FastAPI, il server MCP.

Quello che manca non è tecnologia. È decidere che il MCP è il prodotto d'ingresso
e la Foundation API è ciò che si paga.

---

*Ultimo aggiornamento: 2026-09-10*
