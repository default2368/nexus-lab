# Bolt.new — Scansione Layout → Logica → Moat

**Repo:** https://github.com/stackblitz/bolt.new
**Data:** 2026-10-09
**Metodo:** clone --depth 1 + analisi deterministica Classe 0 (file, grep, cat) + brain collector manuale
**Scopo:** se ha logica che ci può servire, creiamo moat e valore

---

## 1. Layout — cosa ha costruito

```
app/
├── components/
│   ├── chat/           Artifact.tsx, BaseChat.tsx, Chat.client.tsx, CodeBlock, Markdown, Messages
│   ├── editor/         CodeMirrorEditor, languages, cm-theme
│   ├── workbench/      Workbench.client.tsx, EditorPanel, FileTree, FileBreadcrumb, Preview, PortDropdown, terminal/Terminal
│   ├── sidebar/        HistoryItem, Menu, date-binning
│   ├── header/         Header, HeaderActionButtons
│   └── ui/             Dialog, IconButton, PanelHeader, ThemeSwitch
├── lib/
│   ├── runtime/        action-runner.ts, message-parser.ts (core)
│   ├── stores/         chat.ts, editor.ts, files.ts, previews.ts, workbench.ts, terminal.ts (nanostores)
│   ├── persistence/    db.ts (IndexedDB), useChatHistory, ChatDescription
│   ├── webcontainer/   index.ts, auth.client.ts (@webcontainer/api 1.3.0-internal.10)
│   └── hooks/          useMessageParser, usePromptEnhancer, useShortcuts
├── routes/
│   ├── _index.tsx, chat.$id.tsx, api.chat.ts, api.enhancer.ts
├── types/
│   ├── actions.ts (FileAction, ShellAction), artifact.ts, terminal.ts
└── styles/ + utils/

Stack:
- Remix 2.10 + Vite 5.3 + pnpm 9.4
- WebContainers (browser Node.js)
- CodeMirror 6 + xterm 5.5
- ai SDK 3.3.4 + @ai-sdk/anthropic 0.0.39
- nanostores 0.10.3
- framer-motion, shiki, react-markdown
```

**Pattern architetturale:**

```
User prompt → api.chat.ts → LLM → streaming text con <boltArtifact> + <boltAction>
  ↓ StreamingMessageParser (deterministico)
  → onArtifactOpen / onActionOpen callbacks
  → ActionRunner.addAction (pending)
  → ActionRunner.runAction → #executeAction → #runShellAction / #runFileAction in WebContainer
  → stores/files.ts aggiornato → FileTree + EditorPanel + Preview + Terminal
  → persistence/db.ts salva chat history
```

---

## 2. Logica — cosa fa davvero

### 2.1 Artifact / Action — il contratto

```ts
// types/artifact.ts
BoltArtifactData { id, title }

// types/actions.ts
FileAction { type: 'file', filePath, content }
ShellAction { type: 'shell', content }
BoltAction = FileAction | ShellAction
```

È **ApplicationBundle** di Open Nexus in miniatura:
- Artifact = Bundle (contenitore con id, title)
- Action = PageDefinition (file o shell)
- FileTree = Discovery

Differenza: Bolt non ha `PageData` come linguaggio intermedio. Va diretto da LLM → file system. Nessun gate.

### 2.2 StreamingMessageParser — reduction pipeline deterministica

```ts
class StreamingMessageParser {
  parse(messageId, input) {
    // Cerca <boltArtifact ...> e <boltAction type="file" filePath="...">
    // Estrae content fino a </boltAction>
    // Emette onActionClose con action: BoltAction
  }
}
```

**È classe 0**, puro, testabile (ha snapshot test). È esattamente `HttpHtmlConnector → extract → score` di Open Nexus, ma applicato a LLM output invece che HTML.

Manca: `content_sha`, `changed`, `source authority`, `provenance`. Se il parser sbaglia, l'azione viene comunque eseguita.

### 2.3 ActionRunner — workflow contract

```ts
type ActionStatus = 'pending' | 'running' | 'complete' | 'aborted' | 'failed'
BaseActionState { status, abort, executed, abortSignal }

class ActionRunner {
  actions: MapStore<Record<string, ActionState>>
  #currentExecutionPromise = Promise.resolve()
  addAction(data) → pending
  runAction(data) → #executeAction → shell/file in WebContainer
}
```

È **NX-02 Workflow Contract** quasi verbatim:
```
NOT RUN / RUNNING / RUN / FAILED / SKIPPED
+ abort + executed flag + promise chain sequenziale
```

Manca: gate VALIDATE, content_sha, staleness, approval, audit trail. Se un'azione fallisce, logga e continua. Nessun `FAILED → termina run`.

### 2.4 Stores — state

```
chat.ts, editor.ts, files.ts, previews.ts, workbench.ts, terminal.ts, settings.ts
```

Nanostores, client-side, nessun ApplicationContext con grant, nessuna visibility policy, nessun tenant isolation.

### 2.5 WebContainer — environment control

```
@webcontainer/api 1.3.0-internal.10
  → filesystem, node server, package manager, terminal, browser console
  → tutto in browser, no local setup
```

È il moat di Bolt: **AI with Environment Control**. L'AI non solo genera codice, controlla l'ambiente.

Open Nexus ha l'opposto: **Runtime never observes repository directly**. Bolt fa l'opposto: Runtime OSSERVA e MODIFICA tutto.

---

## 3. Cosa è clonabile in 10 giorni, cosa no

| Asset | Clonabilità | Open Nexus equivalente |
|---|---|---|
| Artifact/Action tags `<boltArtifact>` | giorni | ApplicationBundle / PageDefinition — più maturo (ha PageData) |
| StreamingMessageParser | giorni | Connector Layer + reduction — simile, ma Open Nexus ha content_sha + gate |
| ActionRunner | giorni | NX-02 workflow contract — Bolt più semplice, manca VALIDATE |
| Workbench UI (FileTree+Editor+Preview+Terminal) | settimane | Template Lab / Operations — Bolt più ricco per code, Open Nexus per knowledge |
| WebContainers | **non clonabile** | È infra StackBlitz, non codice. Moat di distribuzione |
| Chat persistence (IndexedDB) | giorni | Brain records JSONL — diverso scopo |

**80% clonabile**, come dicevi tu. WebContainers è il 20% non clonabile di Bolt.

---

## 4. Moat Opportunities — dove Open Nexus crea valore sopra Bolt

### 4.1 Governance come tier (M-02 + NX-03)

**Bolt oggi:**
```
LLM output → parser → ActionRunner → WebContainer.fs.writeFile (nessun gate)
```

**Con Open Nexus:**
```
LLM output → parser → VALIDATE gate (PageData schema, registry ID, template, policy, no repo refs, content_sha)
  → se fallisce: rifiuta, logga, mostra finding
  → se passa: ActionRunner
```

Valore: elimina allucinazioni che scrivono file fuori policy, path traversal, file sovrascritti. Bolt non ha nulla di simile. È vendibile come tier "read-write con approvazione + audit trail" (GoMarble pattern).

### 4.2 Evidence layer / Provenance (M-05 + 06-STORAGE)

**Bolt oggi:** azione eseguita, nessun record di perché, da dove, chi ha approvato.

**Con Open Nexus:**
```
Action → SourceObservation (prompt, model_id_resolved, collected_at derivato)
  → AcquisitionRecord (content_sha, excerpt, tool_version)
  → Claim (OBSERVED/INFERRED/LIMIT) + provenance
  → Approval record umano
```

Valore: per team, enterprise, compliance: chi ha generato cosa, quando, con quale modello, con quale evidenza. Bolt è single-user, no audit.

### 4.3 Residuo che compone (M-04)

**Bolt oggi:** ogni chat è isolata. Nessun residuo.

**Con Open Nexus:**
```
ogni ActionRunner run lascia:
- quali file sono stati utili / corretti dall'utente
- quali azioni hanno fallito e perché
- quali template hanno retto
→ il giro dopo il parser è più preciso
```

Valore: dopo 200 progetti, sai quali prompt producono file validi. È dataset che nessun clone compra.

### 4.4 Distribution / Clean-room (F08-014)

**Bolt oggi:** tutto in browser, ma package non validato in clean-room, nessun manifest con hash, nessuna asset locality.

**Con Open Nexus:** `Contract Bundle + Distribution Manifest + clean-room validation` — package generato da allowlist, hash deterministico, template resolution esplicita, no silent fallback.

### 4.5 Knowledge Experience invece di code experience

**Bolt produce:** codice eseguibile.

**Open Nexus produce:** dossier navigabile con evidenza citata.

Opportunità N-settori: applicare pattern Bolt (Artifact/Action) a domini non-code — RENTRI, audit, bandi — dove l'output non è file TS ma `EntityViewArtifact → PageData`.

---

## 5. Glossario etimologico — binario di sviluppo suo

| Termine | Occorrenze Bolt | Prima apparizione (euristica) | Binario sviluppo | Epistemic |
|---|---|---|---|---|
| Artifact | ~50 | app/types/artifact.ts | bolt-artifact-domain | OBSERVED |
| Action | ~80 | app/types/actions.ts | bolt-action-domain | OBSERVED |
| WebContainer | ~20 | app/lib/webcontainer/index.ts | webcontainer-infra (non clonabile) | OBSERVED |
| ActionRunner | ~15 | app/lib/runtime/action-runner.ts | runtime-orchestration-domain | OBSERVED |
| MessageParser | ~15 | app/lib/runtime/message-parser.ts | parser-reduction-domain | OBSERVED |
| Store (nanostores) | ~40 | app/lib/stores/*.ts | state-management-domain | OBSERVED |
| FileTree | ~10 | app/components/workbench/FileTree.tsx | workbench-presentation-domain | OBSERVED |
| Preview | ~15 | app/components/workbench/Preview.tsx | workbench-presentation-domain | OBSERVED |
| Chat History | ~20 | app/lib/persistence/db.ts | persistence-domain | OBSERVED |

**Regola:** non mescolare binari prima che due casi indipendenti confermino minimo comune. Artifact/Action di Bolt ≠ ApplicationBundle/PageDefinition di Open Nexus finché non c'è secondo consumer che conferma.

---

## 6. Valutazione K1-K8 per Bolt come base per moat

```
K1 obbligo rendere conto    ✗  Bolt è per builder, non deve rendere conto
K2 non sostituibile da LLM  ✗  LLM generalista fa 80% di Bolt (genera file)
K3 osservazione continua    ✗  no trigger deterministico, tutto via LLM
K4 pavimento open source    ✗  esiste: WebContainers è open? No, ma ci sono alternative (CodeSandbox)
K5 verticale                ✗  orizzontale: full-stack generico
K6 capability esistente     ✓✓ C-01, C-07, C-08 già parziali in Open Nexus, ma Bolt ha Workbench ricco
K7 prototipo                ✓  repo clonato, layout estratto
K8 persona inbound          ~  nessuna inbound, ma StackBlitz ha distribuzione enorme
```

**Verdetto:** Bolt.new come prodotto **non è** verticale con moat per Open Nexus. Ma come **layout e pattern** è utilissimo: ActionRunner e MessageParser sono reference implementation per NX-02 e Connector Layer.

**Moat si crea non clonando Bolt, ma aggiungendo ciò che Bolt non ha:** VALIDATE gate, provenance, audit trail, residuo che compone, clean-room.

---

## 7. Proposta concreta — cosa rubare e cosa aggiungere

### Rubare (layout utile):

```
- Artifact/Action come contratto dichiarativo (già meglio in Open Nexus con PageData)
- StreamingMessageParser come esempio di parser deterministico con snapshot test
- ActionRunner con abort + promise chain per workflow sequenziale
- Workbench layout FileTree+Editor+Preview+Terminal per Template Lab
```

### Non rubare:

```
- WebContainers (non clonabile, infra)
- Tutto in browser senza gate (fragile)
- Stores senza ApplicationContext/grant
```

### Aggiungere (moat):

```
1. VALIDATE gate prima di ActionRunner.runAction
2. SourceObservation + content_sha + collected_at derivato
3. Approval record + audit trail
4. Residuo che compone (quali azioni utili)
5. Distribution Manifest + clean-room
6. Proiezione in PageData per N-settori non-code
```

Questo è `opnx scan` che volevi: scansiona progetto, prende layout, se logica utile → crea moat.

---

*Report generato da scan-project-layout.py + analisi manuale, Classe 0 + interpretazione Brain, con provenance e command ledger*
