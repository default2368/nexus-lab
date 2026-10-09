# Application Authority — evidenze dai file letti

**Data:** 2026-09-12
**Repo:** `/Users/default/Sviluppo/Nodejs/projects/openfav-migration/codebase/open-nexus-foundation`
**Metodo:** lettura diretta dei file, non grep. Quattro comandi, tutti eseguiti.

---

## 0. Esito di Q-005 — e D-027 è falsificata

### 0.1 I fatti

`applicationType` **NON** è in `ApplicationDefinition`:

```ts
// src/config/applications/types.ts
export interface ApplicationDefinition extends DiscoveryMetadata {
  id: string
  namespace: string
  title: string
  contracts: ApplicationContracts
}
```

Ma **È dichiarato**, in un altro posto. Dall'header di
`src/core/domain-authority/projections/application-type-projection.ts`:

```text
// ApplicationType is a statically-declared property of each ApplicationBundle
// (see src/applications/*/package.ts). BundleCollector.buildCatalog() forwards
// `bundle.type` verbatim into ApplicationCatalog.applications[].type.
//
// This projection is the frozen, build-materialized equivalent of that column:
// it exposes appId → ApplicationType WITHOUT instantiating BundleCollector or
// re-running collect() at request time.
//
// Build/Runtime rule:
//   Build  → BundleCollector.collect() → ApplicationCatalog (authoritative)
//   Runtime → this projection (materialized consumption, no collection)
//
// Parity with the authoritative BundleCollector output is enforced permanently
// by tests/contracts/artifact-consumption-closure.test.ts.
```

### 0.2 Verdetto

```text
Fonte dichiarativa      src/applications/*/package.ts   (ApplicationBundle)
Colonna autorevole      ApplicationCatalog.applications[].type
                        prodotta da BundleCollector.buildCatalog()
Consumo a runtime       APPLICATION_TYPE_PROJECTION (materializzazione frozen)
Parità                  test di contratto permanente
I/O a runtime           nessuno. Dichiarato esplicitamente.
```

**D-027 ("formalizzare la posizione non è formalizzare la proprietà") è FALSA in
questo caso.** La proprietà È documentata, la fonte È dichiarativa, la parità È
coperta da test. Non è un letterale nudo: è una **materializzazione dichiarata come
tale**, con la regola Build/Runtime scritta in testa al file.

Quarta autocorrezione della sessione. Registro il pattern: ho ipotizzato drift tre
volte e tre volte il codice era più avanti dell'ipotesi.

### 0.3 Il residuo vero — ed è preciso

La materializzazione è **mantenuta a mano**. Il file è un `Object.freeze` scritto da
una persona, con un test che verifica la parità.

```text
0.6.x   set di app congelato (5)     → tabella manuale + test di parità = corretto
0.7.0   Human / AI / Importer producono bundle NUOVI
        → un bundle nuovo aggiunge un appId
        → la tabella manuale non lo contiene
        → il test di parità FALLISCE
        → il test diventa il blocco dell'authoring
```

**NX-11 cambia natura.** Non è "sostituire un hardcode con una derivazione"
(derivation fix). È:

> sostituire una materializzazione **manuale** con una materializzazione **generata**.

La regola Build/Runtime scritta nel commento è già quella giusta — manca solo che il
file sia *prodotto* dal build invece che *scritto* a mano. Il commento dice
"build-materialized": oggi è "hand-materialized, build-verified".

Questa è la differenza fra 0.6.x e 0.7.0, ed è esattamente NX-01b: il build emette
l'artefatto, il runtime lo consuma.

---

## 1. La scoperta strutturale: tre layer, non due

`find src/applications` rivela un layer che non compariva nel report sullo stato di
Foundation.

```text
src/applications/                     ← APPLICATION BUNDLE LAYER
  bundle-collector.ts                   BundleCollector vive QUI
  build-manifest.ts                     build manifest
  build-report.ts                       build report
  index.ts
  types.ts
  README.md
  auth/{assets, pages, package.ts}
  open-nexus/{assets, pages, package.ts}
  simple/{assets, pages, package.ts}
  core-admin/{assets, pages, package.ts}
  system/{assets, pages, package.ts}

src/config/applications/              ← APPLICATION DEFINITION LAYER
  types.ts                              i contratti (ApplicationDefinition)
  factory.ts                            createApplicationDefinition + bridge
  index.ts
  auth.ts  core-admin.ts  open-nexus.ts  simple.ts  system.ts

src/core/domain-authority/            ← DOMAIN AUTHORITY
  contracts/application-catalog.ts      export type ApplicationType
  projections/application-type-projection.ts
  projections/getApplicationType.ts
  projections/isExperienceVisible.ts
  governance/health.ts
```

### 1.1 Conseguenza su NX-01b: è già a metà

```text
build-manifest.ts      → il build produce già un manifest
build-report.ts        → il build produce già un report
bundle-collector.ts    → il collector è già isolato nel layer bundle
regola Build/Runtime   → già documentata e test-enforced
```

NX-01b non parte da tre endpoint catalog come stimato in P-007. Parte da un **layer
di bundle con manifest e report già presenti**. La stima va rivista al ribasso.

### 1.2 Conseguenza su Presentation Authority (0.7.0.3)

```text
src/applications/<app>/assets/     ← ESISTE GIÀ, per tutte e cinque le app
```

L'esempio del report dell'utente era:

```text
applications/core-admin
├── assets
├── logo.svg
└── presentation.manifest.ts
```

La directory `assets/` c'è già. Manca **solo il manifest**. 0.7.0.3 è più piccolo di
quanto sembri — ma vedi § 4 sulla sequenza.

### 1.3 Conseguenza su `src/config` vs `src/applications`

Due layer con responsabilità distinte e un confine scritto bene in `types.ts`:

```text
// An Application describes:
//   - its identity (id, namespace, title)
//   - which pages exist (navigation: registryId[])
//   - how they are connected (routing: landing, login, afterLogin, notFound)
//   - what are the system entry points
//
// An Application does NOT describe:
//   - how a page is rendered (that's Rendering's job)
//   - how pages are resolved to URLs (that's Discovery's job)
```

**Questo è un boundary dichiarato per divieto**, stessa forma di
*"Runtime never observes the repository directly"*. Va citato come tale.

Ma la divisione fra `src/config/applications/*.ts` (Definition) e
`src/applications/*/package.ts` (Bundle) **non è documentata** in quello che ho letto.
`type` sta nel Bundle, `routing`/`navigation`/`audience` stanno nella Definition.
Il criterio di ripartizione va scritto, o il prossimo campo finisce in uno dei due
a caso.

---

## 2. `DiscoveryMetadata` — i contratti configurabili esistono già

```ts
export interface DiscoveryMetadata {
  description: string
  icon?: string
  category?: 'knowledge' | 'reference' | 'platform' | 'developer' | 'experimental'
  status?:  'experimental' | 'preview' | 'stable' | 'deprecated'
  featured?: boolean
  audience?: 'developer' | 'user' | 'operator'
}
```

Con il commento:

```text
// Metadata for application discovery, classification and presentation.
// Separated from runtime contracts so the Hub Page can consume these
// independently from routing/navigation implementation details.
```

**È esattamente "contracts facilmente configurabili dall'utente"** della tesi NX-01b,
già scritto, già separato dai runtime contracts, già consumato dall'Hub.

Nota per NX-22 (due tier): `audience` esiste già con tre valori
`developer | user | operator`. **Nessuno dei tre è il decision-maker** (manager,
CFO, broker) dichiarato come persona in `07-PERSONA-AUTHORITIES-COSTO.md`.

```text
O la persona dichiarata non è un'audience di ApplicationDefinition,
O manca un valore.
```

Da decidere prima di 0.7.0.3, perché Presentation Authority esprimerà identità
rispetto a un'audience.

### 2.1 Collisione di vocabolario

```text
ApplicationType    user | shared | workspace      → semantica di visibilità
audience           developer | user | operator    → persona target
```

**`user` compare in entrambi con significati diversi.** È una trappola di lettura:
`type: 'user'` non c'entra niente con `audience: 'user'`. Da rinominare uno dei due
prima che qualcuno li confonda in un prompt o in una PR.

---

## 3. Odori concreti in `src/config/applications/simple.ts`

Letto integralmente. Quattro finding, tutti verificabili.

### 3.1 `as any` sul metadata — il contratto non è verificato

```ts
export const SimpleApplication: BackwardCompatibleApplication & { shared?: Record<string, boolean> } =
  createApplicationDefinition('simple', 'Simple', {
    routing: {...}, navigation: {...},
  }, {
    description: '...',
    icon: 'Box',
    category: 'reference',
    status: 'stable',
    featured: false,
    audience: 'developer',
  } as any)      // ← qui
```

`as any` sul quarto argomento significa che **il blocco DiscoveryMetadata non è
typechecked**. Il contratto esiste e non viene fatto rispettare nel punto in cui
viene popolato.

È un caso di D-024 generalizzato: *un contratto senza enforcement nel punto di
scrittura è una documentazione*. E se `simple.ts` ha `as any`, probabilmente anche
gli altri quattro.

Verifica:
```bash
grep -rn "as any" src/config/applications/
```

### 3.2 `notFound: '/'` viola il contratto dichiarato

```ts
export interface ApplicationRouting {
  /** 404 fallback registryId (e.g. 'open-nexus/not-found') */
  notFound: string
}
```

Il contratto dice **registryId**. L'esempio nel commento è `open-nexus/not-found`.
Il valore in `simple.ts` è:

```ts
notFound: '/',
```

`'/'` non è un registryId, è un path URL. È accettato solo perché il tipo è `string`.

Stessa classe di F-01: **il tipo è troppo largo per il contratto documentato**.
Correzione possibile: tipo branded o union, oppure normalizzazione in factory.

Da verificare se è sistematico:
```bash
grep -rn "notFound" src/config/applications/
```

### 3.3 Tipo di fuga ad-hoc

```ts
: BackwardCompatibleApplication & { shared?: Record<string, boolean> }
```

Un'intersezione con un campo `shared` non documentato, aggiunto inline sul tipo di
ritorno. `types.ts` dice esplicitamente:

```text
// Clean contract. No backward compatibility bridge here.
// See factory.ts for the bridge.
```

Il bridge dovrebbe stare in `factory.ts`. Qui invece il tipo di ritorno di
`simple.ts` porta un'estensione ad-hoc fuori dal bridge.

### 3.4 Commento auto-contraddittorio

```ts
// Navigation:
//   - About (auth required)          ← header del file
...
'simple/about',        // About (public)   ← inline, 20 righe dopo
```

Due affermazioni opposte nello stesso file. Sembra CD-02 (Operations Identity:
spec storica vs implementazione) in miniatura.

---

## 4. Roadmap rivista alla luce delle evidenze

```text
0.7.0      ✅ Application · Domain · Design · Theme Authority
           CONFERMATO, con due asterischi:
             · il confine Definition/Bundle non è documentato (§ 1.3)
             · i contratti non sono enforced nel punto di scrittura (§ 3.1)

0.7.0.1    Primitive Consolidation
           invariato. Aggiungere la classificazione OPERA/CAPISCE (NX-36).

0.7.0.2    Design Enforcement
           invariato, MA con NX-34: ruleset come DATO dichiarativo, consumato
           sia da lint/CI sia dal gate VALIDATE di NX-03.

0.7.0.2b   NUOVO — Contract Enforcement
           rimuovere `as any` da src/config/applications/*, stringere
           notFound a registryId, riportare il bridge in factory.ts.
           Costa poco adesso che i file sono cinque.

0.7.0.3    Presentation Authority
           assets/ esiste già per tutte e cinque le app: manca solo il manifest.
           MA richiede prima la decisione su `audience` (§ 2):
           l'identità si esprime rispetto a un pubblico.

0.7.0.4    Admin New Era
           ultimo, invariato.

0.7.0.x    NX-11 — materializzazione GENERATA invece che manuale
           non è urgente per 0.6.x (test di parità copre), ma è PREREQUISITO
           di 0.7.0 Authoring: con bundle prodotti da AI/Importer la tabella
           manuale non scala e il test di parità diventa un blocco.
```

---

## 5. Voci di backlog

```text
NX-11  RIFORMULATO — da "derivazione mancante" a "materializzazione manuale →
       generata". Prerequisito di 0.7.0 Authoring, non di 0.6.x.

NX-38  NUOVO P1 — rimuovere `as any` da src/config/applications/*.
       Il contratto DiscoveryMetadata non è enforced nel punto di scrittura.

NX-39  NUOVO P1 — `notFound` accetta '/' ma il contratto dichiara registryId.
       Stringere il tipo o normalizzare in factory. Verificare se sistematico.

NX-40  NUOVO P2 — documentare il criterio di ripartizione fra
       src/config/applications (Definition) e src/applications/*/package.ts (Bundle).

NX-41  NUOVO P2 — collisione di vocabolario: `type: 'user'` vs `audience: 'user'`.
       Rinominare uno dei due.

NX-42  NUOVO P1 — `audience` non contiene il decision-maker dichiarato come
       persona. Blocca 0.7.0.3 (Presentation Authority).

NX-22  AGGIORNATO — i due tier Builder/Decision-maker hanno già un campo
       (`audience`) dove atterrare. Non serve un contratto nuovo, serve un valore.
```

**Zona sicura:** NX-38/39/41 toccano `src/config/applications`, che è Definition
Layer, non Runtime. NX-40 è documentazione. NX-42 aggiunge un valore a una union —
va verificato se `audience` è consumato da Discovery o solo dall'Hub: se solo
dall'Hub, è zona sicura; se entra in Discovery, è Foundation RFC.

---

## 6. Nota sul metodo

Quattro comandi, tutti `cat` o `find`, nessun grep per nome. Hanno prodotto più
informazione di tutti i grep precedenti della sessione.

```text
grep per nome     → "questo nome non c'è"          (debole)
cat del contratto → "questi sono TUTTI i campi"    (definitivo)
```

Conferma la regola aggiunta a `03-WORKFLOW.md`: solo la lettura del type prova
l'assenza.

E conferma il valore del guardrail NOT FOUND: tre ipotesi di drift formulate, tre
smentite dai file. Il codice era più avanti delle ipotesi ogni volta.

---

*Ultimo aggiornamento: 2026-09-12*
