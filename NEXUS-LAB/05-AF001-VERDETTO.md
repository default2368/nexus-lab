# AF-001 — Verdetto validazione e conseguenza inattesa

**Data:** 2026-09-10
**Branch ispezionato:** `feature/catalog-registry-authority`
**Metodo:** read-only, Plan-mode, `codebase-memory-mcp` + lettura sorgente
**Esito:** ipotesi NX-01b **falsificata nel suo presupposto**, ma con un finding
di valore superiore.

---

## 1. Il verdetto su AF-001

**AF-001 è chiuso.** La catena storica è rotta:

```text
STORICO (violazione)
[...component].astro → PageController.getByPath → getContext
  → buildNavigation → getApplicationType → new BundleCollector().collect()

OGGI
[...component].astro → PageController.getByPath → getContext
  → buildNavigation → getApplicationType → APPLICATION_TYPE_PROJECTION[appId]
                                            ↑ Object.freeze, puro, no I/O
```

Evidenze:

| Hop | Stato | Riferimento |
|---|---|---|
| `getByPath → getContext` | presente | `src/controllers/PageController.ts:49,153` |
| `buildNavigation → getApplicationType` | presente, import cambiato | `src/core/navigation/buildNavigation.ts:20,58` → `@/core/domain-authority/projections/getApplicationType` |
| `getApplicationType → new BundleCollector().collect()` | **ASSENTE** | `src/core/domain-authority/projections/getApplicationType.ts:32-33` |
| `BundleCollector` nel request path | **ASSENTE** | resta solo in 3 API catalog esplicite |

Conferme incrociate:
- `search_code("new BundleCollector")` → 10 hit, **zero** in `controllers/`,
  `core/navigation/`, `core/runtime/`
- `trace_path(getApplicationType, both)` → callers: `buildNavigation`,
  `PageController.getByPath`, `getContext` — **callees: 0**
- `trace_path(BundleCollector, inbound)` → solo i 3 GET catalog
- Guard di parità: `tests/contracts/artifact-consumption-closure.test.ts`
- Doc: `docs/architecture/AF-001-runtime-bundlecollector-boundary-violation.md`

I 3 endpoint che ancora istanziano il collector:
```text
src/pages/api/catalog/applications/index.ts:20
src/pages/api/catalog/applications/[id].ts:46
src/pages/api/catalog/metrics.ts:19
```

**Classificazione corretta:** oggi è dipendenza statica transitiva/documentale,
non esecuzione vera. Lo split PRODUCE/EXECUTION su questo punto è **pulito**.

---

## 2. La correzione accettata

La tesi "AF-001 è prerequisito commerciale di NX-01b" era **condizionale** e il
condizionale è falso:

```text
SE AF-001 fosse esecuzione vera → prerequisito commerciale di NX-01b
MA AF-001 è già chiuso via projection statica
QUINDI → NX-01b NON è bloccato
```

Correzione dell'agente, accettata integralmente:

> *"Non sto pulendo vs sto costruendo: oggi stai mantenendo pulito, non costruendo."*

Giusto. Ed è il workflow che funziona: un'ipotesi architetturale costosa è stata
falsificata in **un solo passaggio read-only**, senza toccare simboli vincolati,
con `flash`, a costo quasi zero. Se avessimo costruito NX-01b sull'ipotesi, avremmo
progettato intorno a un vincolo inesistente.

---

## 3. Il finding che vale più del verdetto

### 3.1 Come è stato chiuso AF-001

Non spostando il calcolo. **Sostituendo il calcolo con una tabella:**

```js
APPLICATION_TYPE_PROJECTION = Object.freeze({
  "open-nexus":  "user",
  "simple":      "user",
  "core-admin":  "workspace",
  "auth":        "shared",
  "system":      "shared"
})
```

Cinque app. Hardcodate nel sorgente, in
`src/core/domain-authority/projections/`.

Per 0.6.x è una **chiusura deliberata e legittima**: il set di app è congelato,
la tabella è pura, niente I/O, il boundary regge, il test di closure fa da guard.

### 3.2 Perché diventa un blocco a 0.7.0

Il flusso 0.7.0 dal recap ufficiale:

```text
Human / AI / Importer → Authoring → ApplicationBundle
  → BundleCollector invariato → Build Artifacts → Runtime invariato
```

Domanda di fase: *"Possiamo produrre questo modello senza conoscere la struttura
interna del repository?"*

Un bundle autorato produce un `appId` **nuovo**. Allora:

```js
getApplicationType("app-autorata-da-ai")
  → APPLICATION_TYPE_PROJECTION["app-autorata-da-ai"]
  → undefined
```

E `buildNavigation` riceve `undefined` come tipo applicazione.

**La projection statica è corretta per 5 app conosciute e strutturalmente incapace
di rappresentare la sesta.** Non è un bug: è il confine esatto fra 0.6.x (set
congelato) e 0.7.0 (set aperto).

### 3.3 Il pattern — e perché è lo stesso di F-01

```text
AUTHORITY DRIFT PATTERN
Ogni volta che un valore che dovrebbe essere DERIVATO dal bundle
è HARDCODATO nel sorgente, il bundle smette di essere source authority.
```

Confronto:

| | Valore | Dovrebbe venire da | Viene da | Effetto |
|---|---|---|---|---|
| **F-01** | Registry ID | bundle | `BundleCollector → title slugging` | Registry ID ≠ Bundle-derived ID |
| **AF-001 closure** | `applicationType` | bundle | tabella frozen nel sorgente | il bundle non dichiara il proprio tipo |

Stessa malattia, due sintomi. Ed è coerente con quanto il recap ufficiale aveva già
messo a debito:

> *Source Authority: Logical ownership validato. **Page Source Authority non
> formalized.** Debito.*

AF-001 è stato chiuso **pagando con Source Authority**. Trade legittimo per 0.6.x,
debito esatto che 0.7.0 deve ripagare.

### 3.4 La risoluzione corretta — ed è NX-01b stesso

La tabella non deve essere né hardcodata né ricalcolata nel request path.
Deve essere **prodotta**:

```text
ApplicationDefinition dichiara applicationType
        ↓
BundleCollector.collect()  (PRODUCE, remoto/build-time)
        ↓
Build Artifacts contengono application-type-projection.json
        ↓
getApplicationType() legge l'artifact  (EXECUTION, read-only, no I/O sul repo)
```

Questo è **letteralmente** il principio *"FOUNDATION produce, EXECUTION esegue"*
applicato a un singolo valore. E rispetta *"Runtime never observes the repository
directly"*: l'artifact è dato, non sorgente.

Quindi: **NX-01b non è bloccato da AF-001. NX-01b è la risoluzione di AF-001.**
La closure attuale è un placeholder che NX-01b sostituisce con il meccanismo reale.

### 3.5 La domanda decisiva (aperta)

```text
applicationType è un campo DICHIARATO di ApplicationDefinition,
o è INFERITO?

Se DICHIARATO → la projection è derivazione pura, deve diventare Build Artifact.
                Lavoro piccolo, nessun cambio di contratto.

Se INFERITO   → è un contract gap: l'authoring 0.7.0 non può esprimerlo.
                Serve un campo nuovo in ApplicationDefinition
                → FOUNDATION RFC, non brainstorming.
```

**Questa è l'unica domanda che giustifica `deepseek-v4-pro`.** Tutto il resto è
già stabilito da evidenze.

---

## 4. Il secondo finding: la Foundation API esiste già in embrione

I 3 endpoint catalog sono **PRODUCE esposto come API**, già isolato fuori dal
path di EXECUTION:

```text
GET /api/catalog/applications        → new BundleCollector().collect()
GET /api/catalog/applications/[id]   → new BundleCollector().collect()
GET /api/catalog/metrics             → new BundleCollector().collect()
```

Non è poco. Significa che:
- la separazione PRODUCE/EXECUTION è già **operativa**, non solo teorica
- esiste già una superficie HTTP che fa esattamente il mestiere di NX-01b
- il branch si chiama `feature/catalog-registry-authority`: l'asse è già quello

Cosa manca per NX-01b:

| Stato attuale | Target NX-01b |
|---|---|
| in-process (stessa app Astro) | servizio remoto (o engine firmato on-prem) |
| nessuna autenticazione | token scoped + metered |
| output non firmato | Build Artifacts firmati + versionati |
| solo lettura catalog | `POST /v1/compile`, `POST /v1/validate` |
| projection hardcodata | projection emessa come artifact |

NX-01b **non parte da zero**. Parte da tre endpoint che hanno già la forma giusta.

---

## 5. Risposta alla richiesta di Act mode

**No, non passare in Act mode.**

Motivi:

1. **V1 e V2 sono già chiusi da evidenze.** `search_code` + `trace_path` bidirezionale
   + lettura diretta del sorgente + test di closure come guard. Rieseguire per
   "evidenze paginate complete" è spendere per confermare ciò che è confermato.
2. **La validazione era read-only per progettazione.** Passare in Act mode per
   chiudere una validazione read-only contraddice il guardrail che ci ha protetto.
3. **`04-FOUNDATION-API.md` non è nel repo e non deve entrarci** (vedi § 6).

Cosa resta davvero aperto, in ordine di valore:

```text
A. [PRO]  applicationType è dichiarato in ApplicationDefinition o inferito?
          → determina se serve una Foundation RFC
B. [FLASH] reindex + identificare QUALI sono i 2 file metadata_changed
          → se sono i file projection, il verdetto va rieseguito
C. [FLASH] V3 residuo: lettura [...component].astro:39
          + get_architecture(aspects=[layers,boundaries,routes])
D. [FLASH] esiste un fallback per appId assente nella projection?
          → undefined silenzioso, throw, o default?
```

`D` è nuovo e non era nel piano: è quello che determina se oggi un'app sconosciuta
**crolla** o **degrada silenziosamente**. Il degrado silenzioso è peggio.

---

## 6. Confine fra le due memorie

Il report ha evidenziato un problema reale di workflow:

```text
Workspace Arena (NEXUS-LAB/)   → strategia, IP, business, decisioni
Repo locale (docs/)            → codice, debito tecnico, ADR
```

Sono due memorie separate e **devono restare separate**:

- `docs/architecture/AF-*.md`, ADR, test → **nel repo**. È debito tecnico, può
  anche diventare pubblico senza danno.
- `NEXUS-LAB/*` → **fuori dal repo**. Contiene la strategia di distribuzione, la
  tesi di licensing, l'analisi competitiva. Se il repo viene condiviso, aperto,
  o passato a un collaboratore, quella roba esce.

**Regola:** nel prompt all'agente si incolla **solo la sezione specifica** che gli
serve (§ 9, i 4 punti di validazione), mai il documento strategico intero. È
esattamente quello che è stato fatto, e l'agente ha gestito correttamente
l'assenza ricostruendo i punti standard.

Il comportamento corretto dell'agente qui è un buon segnale sul guardrail: ha
dichiarato `NOT FOUND` invece di inventare. I guardrail anti-allucinazione stanno
funzionando.

---

## 7. Aggiornamenti derivati

```text
AF-001  → da "P0 aperto" a "CHIUSO su feature/catalog-registry-authority"
          resta da verificare la freshness dell'indice (2 file metadata_changed)

NX-01b  → SBLOCCATO. Non ha AF-001 come prerequisito.
          Nuovo prerequisito: risoluzione § 3.4 (projection → Build Artifact)

NUOVO   → NX-11 Application Type Projection come Build Artifact
          dipende da § 3.5 (dichiarato vs inferito)

NUOVO   → NX-12 Fallback per appId assente nella projection
          priorità in base a esito di § 5.D

COLLEGAMENTO → § 3.3 unifica AF-001 closure e F-01 sotto un unico pattern.
               Da documentare in ADR-008 insieme all'Identifier Authority Drift.
```

---

*Ultimo aggiornamento: 2026-09-10*
