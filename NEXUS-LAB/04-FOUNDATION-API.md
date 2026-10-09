# NX-01bis · Foundation API — architettura di distribuzione protetta

**Origine:** brainstorming 2026-09-10
**Tesi dell'utente:**

```text
Foundation → deployato → API ← contracts facilmente configurabili dall'utente
           → X → AI → API → Foundation API tokenizzate, codice minificato
           → il runtime è una garanzia in tale senso
```

**Verdetto:** la direzione è corretta. Due correzioni: la minificazione non protegge
niente, e Foundation non può essere *tutta* remota. Il resto regge — e regge perché
il boundary esiste già.

---

## 1. Il principio di copiabilità

> *"il PageAdapter sarebbe copiato in meno di una decina di giorni."*

Vero. E la regola generale è questa:

```text
Tutto ciò che è osservabile dall'esterno (input → output) è copiabile.
Tutto ciò che esiste solo come vincolo accumulato non lo è.
```

Un normalizzatore è copiabile perché il suo contratto comportamentale è visibile:
dagli una page source, guarda la PageData, reimplementa. Non gli serve il tuo codice.
Gli serve il tuo I/O — e quello glielo stai dando tu.

**Conseguenza diretta: la minificazione non serve a niente.**

```text
codice leggibile   → copiato in 10 giorni
codice minificato  → beautificato in 10 minuti, copiato in 10 giorni + 2 ore
codice offuscato   → copiato in 10 giorni + una settimana
codice NON SPEDITO → non copiabile
```

L'offuscamento compra **ore**. Non è una strategia, è un placebo che costa
manutenzione (source map, debugging impossibile, build fragile).

**Non investire in offuscamento. Investi nel non spedire la logica.**

---

## 2. Classificazione degli asset

| Asset | Copiabilità | Va spedito? |
|---|---|---|
| Normalizzatori / adapter (`normalizeToPageData`) | giorni | sì, ma server-side se possibile |
| Provider chain (filesystem/redis/virtual) | giorni | sì |
| Renderer / Template | giorni | sì, minificato è sufficiente |
| CLI plumbing | giorni | sì |
| **Schema dei contratti** (PageData, ApplicationDefinition) | settimane | **sì, PUBBLICATO** |
| BundleCollector + compilatore Bundle → Artifacts | mesi | **NO** |
| Gate `VALIDATE` (NX-03) | mesi | **NO** |
| Motore di migrazione fra versioni di contratto | mesi/anni | **NO** |
| Set di invarianti + debito classificato (AF-00x, CD-0x, F-01) | anni | **NO** |
| Telemetria su quali pattern funzionano davvero | **non copiabile** | **NO** |
| 4 stratificazioni sopravvissute con test all'80% | **non copiabile** | **NO** |

Le ultime due righe sono il moat. Nessuna delle due è codice: sono **conoscenza
accumulata** e **dato osservazionale**.

---

## 3. La scoperta: il boundary logico È la linea di distribuzione

Dal recap ufficiale congelato il 2026-08-20:

```text
FOUNDATION    ApplicationBundle → BundleCollector → Build Artifacts → [boundary]
EXECUTION     ApplicationDefinition → ApplicationContext → Discovery
              → PageData → Template → Experience
```

**FOUNDATION produce, EXECUTION esegue.**

E l'invariante assoluto: **Runtime never observes the repository directly.**

Quell'invariante non è solo una proprietà di pulizia. Ha una conseguenza di
distribuzione enorme:

> Se il Runtime non osserva il repository, allora il Runtime consuma
> **Build Artifacts** — cioè **dati**. I dati possono viaggiare.
> La logica che li produce no.

Quindi:

```text
┌──────────────────────────────────────────────────────────────┐
│  PRODUCE  (build-time)   → REMOTO, mai spedito, tokenizzato  │
│  EXECUTION (request-time) → LOCALE, spedito, sottile          │
└──────────────────────────────────────────────────────────────┘
```

**Il confine che hai congelato il 20 agosto non era solo un confine logico.
Era la linea di distribuzione.** Non devi inventare un boundary nuovo: devi
deployare lungo quello che hai già.

Questo risolve anche il problema che avrebbe ucciso la proposta "tutto remoto":

```text
Tutto remoto     → ogni render chiama la tua API → latenza, costo, single point
                   of failure, e contraddice qualunque storia sovereign
Split al boundary → l'API serve SOLO in authoring/build, mai nel request path
                   → gli artifacts generati sono statici e self-hostable
                   → BUILD-TIME dependency ≠ RUNTIME dependency
```

Un cliente può avere il tuo server giù e la sua app continua a servire. Questo è
vendibile. "Se il mio server è giù la tua app è giù" non lo è.

---

## 4. Architettura proposta

```text
╔══════════════════════════════════════════════════════════════════╗
║  LOCALE — spedito all'utente                                     ║
╠══════════════════════════════════════════════════════════════════╣
║  EXECUTION SHELL                                                 ║
║   ├── Contratti Runtime (TS types / JSON Schema)   ← PUBBLICI    ║
║   │     ApplicationDefinition · ApplicationContext · PageData   ║
║   ├── Discovery sugli Artifacts                    (locale)      ║
║   ├── Renderer / Template                          minificato    ║
║   └── nexus CLI                                                  ║
║                                                                  ║
║  Serve statico / self-hosted. ZERO rete nel request path.        ║
╚══════════════════════════════════════════════════════════════════╝
                    ▲
                    │  Build Artifacts (firmati, versionati)
                    │
╔══════════════════════════════════════════════════════════════════╗
║  REMOTO — non spedito mai                                        ║
╠══════════════════════════════════════════════════════════════════╣
║  FOUNDATION API  (tokenizzata)                                   ║
║   ├── BundleCollector                                            ║
║   ├── Compiler:  Bundle → Build Artifacts                        ║
║   ├── Validator: gate VALIDATE                      (NX-03)      ║
║   ├── Contract Registry + versioning + MIGRATION ENGINE          ║
║   └── Telemetria di compilazione                                 ║
║                                                                  ║
║  X API  (tokenizzata)                                            ║
║   ├── AI authoring (FastAPI + MCP)                               ║
║   ├── Workflow runner                               (NX-02)      ║
║   └── Extraction / generazione                                   ║
╚══════════════════════════════════════════════════════════════════╝
```

Flusso:

```text
Human / AI / Importer
        ↓
   ApplicationBundle          (dichiarativo, leggibile, PUBBLICO nel formato)
        ↓
   POST /v1/compile           ← token, metered
        ↓
   BundleCollector            (mai spedito)
        ↓
   VALIDATE gate              (mai spedito)
        ↓
   Build Artifacts (firmati)  ← tornano al cliente
        ↓
   Execution Shell locale     → Experience
```

---

## 5. Pubblica il contratto, nascondi il compilatore

La parte controintuitiva. *"contracts facilmente configurabili dall'utente"* significa
che il contratto è **leggibile**, e quindi **imparabile**. Sembra un rischio. Non lo è.

```text
HTML è pubblico dal 1993.
Nessuno ha clonato l'engine di Chrome in dieci giorni.
```

Il formato pubblico **non è** il moat, e pubblicarlo ha tre effetti positivi:

1. **Rende il tuo formato lo standard.** Chi scrive tooling lo scrive per te.
2. **Abbassa il costo di adozione a zero.** Un utente può generare bundle a mano,
   con un altro AI, con uno script — e tu lo compili comunque.
3. **Sposta il valore dove non è copiabile:** il compilatore, il validator, il
   motore di migrazione, la telemetria.

E qui c'è l'argomento che probabilmente non avevi considerato:

> **API tokenizzata = telemetria = moat che compone.**

Ogni compilazione ti dice: quali contratti usano, dove falliscono, quali pattern
producono drift, quali template vengono scelti, quante pagine per bundle, quali
errori di validazione ricorrono. È il dataset che nessun clone può comprare, perché
si accumula solo servendo utenti reali. Dopo 12 mesi sai cosa funziona e loro stanno
ancora indovinando.

**Questo è il vero motivo per cui la tua proposta è giusta.** Non la protezione del
codice — quella è difensiva e vale poco. La protezione che diventa **vantaggio
informativo composto**. È offensiva.

---

## 6. Design del token

```text
Formato        nexus_<tier>_<keyid>.<secret>
Trasporto      Authorization: Bearer
Scope          operations[]: compile · validate · author · publish
               apps[]:       quali ApplicationBundle
               contracts[]:  quali versioni di contratto
Rate limit     per token, per operation (compile costa più di validate)
Metering       per operation + per byte di bundle + per token LLM su X API
Revoca         keyid → blocklist firmata distribuita nel bundle CLI
               (nessun license server necessario per la verifica ordinaria)
Expiry         token brevi + refresh firmato, come NX-01
```

Coerenza con decisioni già prese:

- **D-011:** `AUTH_API_KEY` separata da `DEEPSEEK_API_KEY`. Qui diventa strutturale:
  il token Nexus autorizza l'utente, la chiave DeepSeek autorizza il provider. Non si
  toccano mai.
- **NX-01:** la licenza offline firmata resta necessaria per il caso **on-prem /
  air-gapped** — chi vuole tutto locale non può chiamare la tua API. Stessa logica,
  due trasporti:
  ```text
  hosted    → token API, metered, telemetria attiva
  on-prem   → engine binario firmato + licenza offline, telemetria opt-in
  ```
- **NX-05:** le regole vanno enforce **server-side**. Con il compilatore remoto è
  automatico: il client non può bypassare il gate perché il gate è dall'altra parte.

---

## 7. Rischi e mitigazioni

| Rischio | Mitigazione |
|---|---|
| API giù → nessuno può buildare | Build-time only: gli artifacts già generati continuano a servire. Cache locale degli artifacts. |
| Latenza nel loop di dev | `nexus dev` usa artifacts cached; ricompila solo i bundle cambiati (content_sha). |
| Costo infra per un solo dev | Build-time, non request-time: il traffico è proporzionale alle release, non agli utenti finali. |
| Cliente sovereign/air-gapped | Track on-prem con engine firmato + licenza offline (NX-01). |
| Ogni cambio di schema rompe gli utenti | **Migration engine** versionato. È anche il moat: è la cosa più difficile da copiare. |
| Tentazione di offuscare | Non farlo. Compra ore, costa manutenzione. |
| Contratto pubblico → clone del formato | Il formato non è il moat. Pubblicarlo ti rende lo standard. |
| Metering LLM fuori controllo | `MAX_OUTPUT_TOKENS` per classe + routing flash/pro (già deciso). |

---

## 8. Cosa cambia nel backlog

```text
NX-01  Licenza offline firmata        → resta P0, diventa il track ON-PREM
NX-01b Foundation API tokenizzata     → NUOVO, P0, track HOSTED (questo file)
NX-03  Gate VALIDATE                  → sale: diventa endpoint remoto /v1/validate
NX-02  Workflow Contract              → il runner chiama l'API, non esegue in locale
NX-05  Enforce server-side            → risolto per costruzione (il gate è remoto)
NX-09  Indice pubblicato              → diventa il Contract Registry remoto
```

Ordine rivisto:

```text
1. NX-01b  Contract Registry + /v1/compile + /v1/validate  (il confine diventa API)
2. NX-03   Gate VALIDATE come endpoint                      (il differenziatore)
3. NX-01   Licenza offline per il track on-prem              (il secondo trasporto)
4. NX-02   Workflow runner che chiama l'API                  (X)
```

---

## 9. Domanda di validazione (da girare a `deepseek-v4-pro`)

```text
Data la baseline congelata:
  FOUNDATION  ApplicationBundle → BundleCollector → Build Artifacts → [boundary]
  EXECUTION   ApplicationDefinition → ApplicationContext → Discovery
              → PageData → Template → Experience
e l'invariante "Runtime never observes the repository directly":

è vero che lo split PRODUCE=remoto / EXECUTION=locale non richiede alcuna
modifica ai contratti Runtime?

Verificare specificamente se:
  1. BundleCollector ha oggi dipendenze che assumono filesystem locale
     nello stesso processo del Runtime (vedi AF-001)
  2. DiscoveryService ha provider (filesystemProvider) che richiedono accesso
     al repository e non solo agli Artifacts
  3. Build Artifacts sono già autosufficienti per l'Execution Shell, o
     contengono riferimenti a sorgenti
  4. la firma degli Artifacts richiede un campo nuovo nel contratto

Output: FACTS OBSERVED / HYPOTHESES / RECOMMENDATIONS.
Se un punto richiede modifica a PageController, normalizeToPageData,
ApplicationDefinition, ApplicationContext, BundleCollector, DiscoveryService
o PageData → segnalarlo come FOUNDATION RFC, non procedere.
```

**Nota:** il punto 1 è esattamente `AF-001` (P0). Se `Runtime → BundleCollector` è
nel request path, allora lo split remoto/locale **non è pulito** e `AF-001` smette di
essere debito tecnico e diventa **prerequisito commerciale**. Sarebbe una buona
notizia: il P0 che avevi già identificato è quello che abilita il business model.

---

*Ultimo aggiornamento: 2026-09-10*
