# Stato di salute di Foundation — 2026-09-12

**Base di evidenze:** file letti direttamente (`src/config/applications/types.ts`,
`simple.ts`, `application-type-projection.ts`, `find src/applications`), output test
(`primitive-authority.test.tsx`, 21/21), sorgente di
`scripts/design/check-style-authority.mjs`, `docs/design/exception-registry.md`,
report dell'utente sullo stato delle authority, recap ufficiale 2026-08-20.

**Limite dichiarato:** non ho visto la suite di test globale, lo stato di F-01 e
CD-01..03, né `docs/design/STYLE-INVENTORY.md`. Le dimensioni che dipendono da quei
dati sono marcate `NON VALUTABILE`.

---

## 0. Prima: la correzione alla mia proposta

Avevo proposto (messaggio precedente) uno `scope` come **elenco di glob da coprire**.
L'implementazione reale fa l'opposto:

```ts
function* walk(dir) { /* readdirSync ricorsivo su tutto src/ */ }
export function exceptionFor(relPath) { /* le eccezioni SOTTRAGGONO */ }
```

```text
LA MIA PROPOSTA    enumera cosa è coperto      → fallisce APERTO
                   (un file nuovo fuori lista non è controllato)

L'IMPLEMENTAZIONE  scansiona tutto, le eccezioni carve-out
                                               → fallisce CHIUSO
                   (un file nuovo in src/ è controllato automaticamente)
```

**Ho sbagliato la polarità.** Q-011/NX-44 è quindi **risolta per lo script**: scope
derivato dal filesystem, non enumerato.

Residuo congelato (da riprendere solo se diventa rilevante): le asserzioni
`AUTHORITY_FILES` in `primitive-authority.test.tsx` ora **sovrappongono** ciò che lo
script fa meglio. `classifySource` è esportata e commentata *"Pure; used by tests"* —
se il test la importa, la sovrapposizione è già risolta; se legge i file per conto
proprio, ci sono due fonti di verità per la stessa regola.

**Trigger per il promemoria:** quando aggiungi una primitiva nuova, o quando
0.7.0.2 chiude. Non prima.

---

## 1. Griglia di salute

| # | Dimensione | Voto | Evidenza |
|---|---|---|---|
| 1 | Integrità del boundary PRODUCE/EXECUTE | **A** | § 2 |
| 2 | Copertura delle authority | **A−** | § 3 |
| 3 | Enforcement dei contratti | **B** | § 4 |
| 4 | Drift | **B−** | § 5 |
| 5 | Postura di verifica | **A−** | § 6 |
| 6 | Tracciabilità delle decisioni | **A** | § 7 |
| 7 | Prontezza alla distribuzione | **B** | § 8 |
| 8 | Onestà sul debito | **A** | § 9 |
| — | Suite globale / F-01 / CD-01..03 | **NON VALUTABILE** | § 10 |

**Sintesi: B+ / A−.** Il punteggio è tirato su da 1, 6, 8 e tirato giù da 3 e 4 —
cioè: l'architettura è avanti, l'enforcement dei contratti è indietro rispetto
all'enforcement del design.

---

## 2. Integrità del boundary — A

```text
AF-001 chiuso           isExperienceVisible è funzione pura sul tipo
                        (src/core/domain-authority/projections/isExperienceVisible.ts:30)
Regola Build/Runtime    documentata in testa ad application-type-projection.ts:
                          Build  → collect() → ApplicationCatalog (authoritative)
                          Runtime → projection (materialized, no collection)
Parità                  enforced permanentemente da
                        tests/contracts/artifact-consumption-closure.test.ts
Layer bundle isolato    src/applications/{bundle-collector, build-manifest,
                        build-report}.ts + <app>/{assets, pages, package.ts}
Boundary per divieto    "An Application does NOT describe:
                          how a page is rendered (Rendering's job)
                          how pages are resolved to URLs (Discovery's job)"
```

Il boundary non è solo dichiarato: ha una regola scritta, un test permanente e una
separazione fisica dei layer. È la dimensione più solida.

**Unica riserva:** la materializzazione è manuale (NX-11). Corretta per 0.6.x,
prerequisito da risolvere per 0.7.0 Authoring.

---

## 3. Copertura delle authority — A−

```text
✅ Application Authority    src/config/applications
✅ Content Authority        src/config/discovery/page-registry
✅ Domain Authority         src/core/domain-authority
✅ Design Authority         src/core/design-authority
✅ Theme Authority          ThemeInjector
✅ Primitive Authority      src/core/ui-primitives          ← ADR-0012, 21 test
⬜ Presentation Authority   0.7.0.3 — assets/ esiste già per tutte e 5 le app,
                            manca solo presentation.manifest.ts
```

**Sei authority formalizzate** contro una sola indicata come debito il 20 agosto
(*"Page Source Authority non formalized"*).

Riserve:

```text
· il criterio di ripartizione Definition (src/config/applications) vs
  Bundle (src/applications/*/package.ts) NON è documentato (NX-40)
· `audience` non contiene il decision-maker dichiarato come persona (NX-42)
· collisione di vocabolario: type:'user' (visibilità) vs audience:'user'
  (persona) — NX-41
```

---

## 4. Enforcement dei contratti — B

Qui c'è l'asimmetria più interessante dello stato di salute.

### 4.1 Enforcement del DESIGN — avanti

`check-style-authority.mjs` è di qualità superiore a quello che avevo proposto:

```text
regole come DATO        EXCEPTIONS e RAW_PALETTE_ROOTS esportati
scope DERIVATO          walk() su tutto src/, eccezioni che sottraggono → fails closed
funzione PURA           classifySource(source, relPath) → findings, "used by tests"
tre modalità            report umano · --json machine-readable · --ci exit 1
eccezioni tipizzate     4 categorie: external-brand · decorative-effect ·
                        legacy-frozen · presentation-candidate
motivo obbligatorio     ogni eccezione ha `reason`
specchio documentale    docs/design/exception-registry.md
regola di governance    "every exception must be documented, scoped,
                         and expire or be formalized"
```

### 4.2 Enforcement dei CONTRATTI — indietro

```text
`as any` su DiscoveryMetadata in simple.ts
  → il contratto NON è typechecked nel punto di scrittura (NX-38)

notFound: '/' con contratto che dichiara "registryId"
  → il tipo string è troppo largo per il contratto documentato (NX-39)

BackwardCompatibleApplication & { shared?: Record<string, boolean> }
  → tipo di fuga ad-hoc mentre types.ts dice "No backward compatibility
    bridge here. See factory.ts for the bridge"

eccezioni con scadenza nel DOC ma non nel DATO
  → `Expires: 0.7.0.3` compare in exception-registry.md, non in EXCEPTIONS
  → nulla machine-enforces la scadenza
  → un'eccezione che non scade diventa legacy-frozen per inerzia
```

**Regola generale che ne emerge:**

> Un contratto è enforced solo se il punto di **scrittura** lo verifica.
> Verificare il punto di lettura (renderer, runtime) protegge l'utente,
> non protegge il contratto.

Il design ha entrambi i punti. I contratti di Definition ne hanno zero: `as any`
disattiva TypeScript esattamente dove il contratto viene popolato.

### 4.3 Tre finding puntuali sullo script

**a) `--ci` non può passare oggi.** Con 554 errori, `report()` restituisce 554 e
`--ci` fa `process.exit(1)`. Il doc dice *"gate enabled per-file once migrated"* —
quindi il meccanismo per-file sta altrove (wrapper CI o STYLE-INVENTORY). Non è in
questo file. **Da verificare**, non da assumere.

**b) `src/pages/build/` è dentro un'eccezione frozen.**

```ts
{ key: 'legacy-frozen:pages',
  scope: [..., 'src/pages/build/', ...] }
```

`inScope` usa `startsWith`. `src/pages/build/` contiene `[...component].astro` —
**il punto d'ingresso di EXECUTION**. Qualunque file visuale aggiunto lì in futuro è
esente per costruzione. È una tasca fails-open dentro un sistema fails-closed.

Probabilmente corretto oggi (è una route, non una superficie visuale), ma lo scope a
prefisso di directory è più largo dell'intento. Meglio: enumerare i file, o
restringere a `src/pages/build/[...component].astro`.

**c) Duplicazione potenziale con il vitest** — vedi § 0, congelato.

---

## 5. Drift — B−

```text
F-01  Registry ID ≠ Bundle-derived ID        NON VALUTABILE (non ho letto i file)
CD-01 Open Nexus afterLogin                   NON VALUTABILE
CD-02 Operations Identity                    NON VALUTABILE
CD-03 Shared Consumers                       NON VALUTABILE

nuovi candidati trovati leggendo i file:
  · type:'user' vs audience:'user'                       NX-41
  · commento auto-contraddittorio in simple.ts
    (header "About (auth required)" vs inline "About (public)")
  · `as any` come meccanismo di fuga dal contratto        NX-38
  · notFound:'/' vs contratto registryId                  NX-39
  · scadenza eccezioni nel doc ma non nel dato            § 4.2
```

Il pattern ricorrente è uno solo ed è già nominato (D-013): **valore il cui tipo è
più largo del contratto documentato**. F-01, `notFound`, `as any` sono la stessa
malattia a tre livelli diversi (identità, routing, metadata).

---

## 6. Postura di verifica — A−

```text
21 test mirati su Primitive Authority, 690 ms
test di parità permanente sulla materializzazione (artifact-consumption-closure)
classifySource pura ed esportata esplicitamente per i test
STYLE-INVENTORY con categorie A/B/C/D/E
baseline pubblicata: 554 errori in 33 file evolutive
ADR-0012 e PRD-0013 referenziati nel codice, non solo nei doc
```

Il commento `/** Classify one file's source → list of findings. Pure; used by tests. */`
è il dettaglio che dice tutto: la logica di enforcement è stata resa testabile
**prima** di essere usata. È la disciplina che produce i 21 test verdi.

Riserva: lo stato della **suite globale** non mi è noto. Ad agosto era 🟡 con 6
fallimenti di drift classificandi.

---

## 7. Tracciabilità delle decisioni — A

```text
ADR numerati (ADR-0012), PRD numerati (PRD-0013)
exception-registry.md che specchia EXCEPTIONS
regola di governance scritta: "expire or be formalized"
commenti in testa ai file che spiegano la regola Build/Runtime
boundary dichiarati per divieto
```

È **NX-08 già in pratica**: documentazione che difende le decisioni invece di
descriverle. Un clone può copiare `check-style-authority.mjs` in un giorno; non può
copiare il motivo per cui `external-brand:google` scade `never (by design)` e
`legacy-frozen:webpage-template` è escluso dalla Boy-Scout rule.

---

## 8. Prontezza alla distribuzione — B

```text
✅ layer bundle isolato con collector, manifest, report
✅ regola Build/Runtime documentata e testata
⬜ materializzazione generata invece che manuale        NX-11 (blocco 0.7.0)
⬜ firma degli artifacts
⬜ tokenizzazione / PAT
⬜ Foundation API remota                                  NX-01b
⬜ nexus-mcp                                              NX-14
```

La struttura c'è; manca la superficie esterna. È la dimensione più indietro
rispetto all'ambizione dichiarata, ed è coerente: stai finendo l'interno prima di
aprire l'esterno, che è l'ordine giusto.

---

## 9. Onestà sul debito — A

```text
"554 errors in 33 evolutive-surface files → target 0 via Boy-Scout rule"
"--ci gate is enabled per-file once migrated"
"legacy-frozen ... excluded from Boy-Scout migration"
"qualche bordo, ma ci sta"
```

Pubblicare il numero 554 invece di nasconderlo, con un target e una regola di
migrazione, è esattamente la postura di Trustable (*"Note what it does NOT do"*) e
del tuo recap ufficiale (*"Non dimostra sincronizzazione cross-tab real-time"*).

Nota operativa: **554 in 33 file è un numero bounded e conoscibile.** Non è debito
infinito, è una lista di 33 file. A ~17 violazioni per file, con la Boy-Scout rule,
è lavoro di settimane non di mesi — e ogni file migrato abilita il gate su quel file,
quindi il debito non può ricrescere.

---

## 10. Non valutabile senza altri dati

```text
□ stato della suite di test globale (era 🟡 con 6 fallimenti ad agosto)
□ classificazione di CD-01, CD-02, CD-03
□ stato di F-01 Identifier Authority Drift / ADR-008
□ AF-002 Discovery Amplification
□ AF-003 Server Session Recovery / AF-004 Client Session Reconciliation
□ contenuto di docs/design/STYLE-INVENTORY.md (categorie A–E e meccanismo per-file)
□ se PageData ammette valori visuali grezzi (vedi § 11)
□ indicizzazione codebase-memory sul repo open-nexus-foundation
  (il grafo attuale osserva openfav-codebase-V1)
```

---

## 11. Correzione a D-033 / NX-34 — X genera dati, non codice

Avevo scritto: *"stesso ruleset, due punti di applicazione — lint/CI per gli umani,
gate VALIDATE per X"*. **Era sbagliato**, e il tuo script mostra perché.

`check-style-authority.mjs` scansiona `.tsx .ts .astro .css` — cerca **classi
Tailwind e valori cromatici nel sorgente**. Ma X non genera sorgente: genera
**PageData**, che referenzia primitive per nome.

```text
umano scrive TSX        → palette check     (check-style-authority.mjs) ✅ esiste
X genera PageData       → VOCABULARY check  (referenzia solo primitive
                          e status noti?)   ← è un check DIVERSO
```

Se Primitive Authority è fatta bene, una PageData generata **non può contenere**
`bg-blue-500`: può solo dire `StatusBadge status="stable"`. Quindi:

```text
il gate di build per X verifica:
  · ogni componente referenziato esiste nell'inventario delle primitive
  · ogni valore di status esiste nel vocabolario di status-tones.ts
  · nessun campo libero che ammetta valori visuali grezzi
```

**La domanda che decide tutto (da verificare, non da assumere):**

> PageData ammette escape hatch visuali — `className`, `style`, HTML libero,
> campi `raw`?

```text
SE NO   → il palette check non serve al gate. NX-34 si riduce a vocabulary check.
          Più semplice di quanto pensavo, e già quasi coperto da Primitive Authority.
SE SÌ   → quei campi vanno o rimossi o sottoposti allo stesso ruleset,
          e allora `classifySource` va resa consumabile anche sul contenuto
          di quei campi.
```

Resta valido il principio di D-033 (**degrada a runtime, rifiuta a build**), ma il
rifiuto a build per X è sul vocabolario, non sulla palette.

---

## 12. Sul "refactoring più sanguinoso dal 0.4.x"

Hai detto: authority refactor fra i più invasivi, e si viaggia senza errori dalla
0.4.x.

I due fatti insieme sono la misura reale della salute, e valgono più della griglia:

```text
invasività alta  +  regressioni zero  =  i boundary tengono sotto stress
invasività alta  +  regressioni alte  =  coupling nascosto
invasività bassa +  regressioni zero  =  non stai cambiando niente
```

Sei nel primo caso. Ed è la **quinta** stratificazione che regge, con una differenza
rispetto alle quattro precedenti: questa volta avevi authority formalizzate e test di
parità **prima** di spostare il codice, non dopo. Le prime quattro sono sopravvissute
per robustezza del pattern; questa è sopravvissuta per progettazione.

È anche la risposta empirica alla domanda IP che apriva la sessione: un sistema che
assorbe il refactor più sanguinoso della sua storia senza regressioni non si clona in
dieci giorni, perché la proprietà non sta nei file — sta nell'ordine in cui li hai
scritti.

---

## 13. Priorità che escono dalla griglia

```text
1. NX-38 / NX-39 — enforcement nel punto di scrittura dei contratti
   È l'unica dimensione con voto B su un layer già dichiarato ✅.
   Costa poco adesso che i file di Definition sono cinque.
   Proposta: milestone 0.7.0.2b "Contract Enforcement".

2. NX-42 — `audience` senza decision-maker
   Blocca 0.7.0.3, e 0.7.0.3 è già quasi pronto (assets/ esiste).

3. NX-11 — materializzazione generata
   Non urgente per 0.6.x, prerequisito duro per 0.7.0 Authoring.

4. § 11 — verificare se PageData ammette valori visuali grezzi
   Determina la forma del gate VALIDATE. Una domanda, non un progetto.

5. § 4.3 — scadenza eccezioni nel dato, scope di src/pages/build/
   Piccoli, ma il primo è quello che impedisce alle eccezioni di diventare
   permanenti per inerzia.
```

**Non prioritario:** NX-14 / NX-01b restano giusti ma sono superficie esterna.
L'interno non è finito: ha sei authority e un enforcement dei contratti ancora da
chiudere.

---

*Ultimo aggiornamento: 2026-09-12*
