# Authority Architecture — stato reale e correzioni

**Data:** 2026-09-12
**Fonte:** report allegato dall'utente (`untitled text.txt`) + conferma a voce
*"dopo il refactoring della source of truth, senza regressioni, andato liscio come
l'olio. No rotture, no regressioni (qualche bordo, ma ci sta)."*

---

## 0. Correzione a verbale: NX-18 era sbagliato

Due messaggi fa ho proposto **Graphic Authority** come "la terza authority", una
novità da formalizzare.

**Era sbagliato.** Non perché l'istinto fosse sbagliato, ma perché:

1. `src/core/design-authority` **esiste già**.
2. La mia "Graphic Authority" era in realtà **tre authority distinte** che tu hai già
   decomposto meglio di me:

```text
LA MIA PROPOSTA (grezza)              LA TUA DECOMPOSIZIONE (reale)
─────────────────────────────────────────────────────────────────────────
"inventario chiuso di blocchi"     →  PRIMITIVE AUTHORITY      (0.7.0.1)
"token di design vincolanti"       →  DESIGN AUTHORITY         (esiste)
"gate che rifiuta i fuori policy"  →  DESIGN ENFORCEMENT       (0.7.0.2)
"identità dell'applicazione"       →  PRESENTATION AUTHORITY   (0.7.0.3)
"stato/tema"                       →  THEME AUTHORITY          (esiste)
```

La tua decomposizione è migliore perché separa **meaning / state / identity**, che
cambiano a velocità diverse e per ragioni diverse. La mia era un calderone.

**NX-18 va chiuso come DUPLICATO**, non come aperto. Registro l'errore: è il secondo
della sessione in cui ho proposto architettura senza verificare cosa esistesse già
(il primo è AF-001). Stessa classe di sbaglio, stessa cura: chiedere prima di
proporre.

---

## 1. Lo stato reale di Foundation

```text
✅ Application Authority    src/config/applications
✅ Content Authority        src/config/discovery/page-registry
✅ Domain Authority         src/core/domain-authority
✅ Design Authority         src/core/design-authority
✅ Theme Authority          ThemeInjector
```

**Cinque authority formalizzate.** Il recap ufficiale del 20 agosto ne nominava una
sola come debito: *"Page Source Authority non formalized"*. In tre settimane è
diventata Content Authority più altre quattro.

Roadmap:

```text
0.7.0      ✅ Application · Domain · Design · Theme Authority
0.7.0.1    Primitive Consolidation      → Primitive Authority
0.7.0.2    Design Enforcement           → il gate
0.7.0.3    Presentation Authority       → Asset Ownership, Presentation Manifest
0.7.0.4    Admin New Era
```

---

## 2. Il pattern Authority È la cura dell'Authority Drift

Il documento allegato contiene la frase più importante della sessione:

> *"finora non state spostando codice. State continuando a rispondere alla stessa
> domanda: **Chi possiede cosa?**"*

Questa è **esattamente** la cura del pattern che avevo nominato in D-013 senza
sapere che la stavi già eseguendo:

```text
D-013  AUTHORITY DRIFT PATTERN
       Ogni volta che un valore che dovrebbe essere derivato dal bundle
       è hardcodato nel sorgente, il bundle smette di essere source authority.

TU     Programma sistematico di assegnazione di ownership per dominio.
       È l'anti-drift applicato a tutto il sistema, non a un singolo campo.
```

Le due derive che avevamo isolato sono casi particolari della stessa domanda:

```text
F-01   Registry ID ≠ Bundle-derived ID
       → di chi è l'identità? Content Authority o bundle?

AF-001 closure   APPLICATION_TYPE_PROJECTION hardcodata
       → di chi è il tipo applicazione? Domain Authority o Application Authority?
```

### 2.1 Q-005 si è ristretta — e probabilmente si risponde da sola

`APPLICATION_TYPE_PROJECTION` sta in `src/core/domain-authority/projections/`.
E tu hai `src/config/applications` = **Application Authority**.

Quindi la domanda precisa non è più "dichiarato o inferito" ma:

```text
applicationType è DICHIARATO in src/config/applications/<app>/ ?

SE SÌ  → la projection in domain-authority è una derivazione congelata a mano
         invece che calcolata. NX-11 = sostituisci la tabella con la proiezione
         emessa da BundleCollector. ZONA SICURA, nessun cambio di contratto.

SE NO  → Application Authority non copre il tipo. Serve un campo nuovo.
         FOUNDATION RFC.
```

Dato che hai appena formalizzato Application Authority, **il caso SÌ è molto più
probabile**. Il che trasformerebbe NX-11 da "P0 bloccato" a "lavoro piccolo".

Da verificare con un comando solo:

```bash
grep -rn "applicationType\|appType" src/config/applications/ | head -20
```

### 2.2 Regola che emerge

Il criterio di accettazione per ogni futura authority dovrebbe essere esplicito:

```text
Un valore ha un'authority quando:
  1. esiste UNA fonte dichiarativa che lo possiede
  2. tutto il resto è PROIEZIONE derivata, non copia
  3. la proiezione è emessa da BundleCollector come artefatto,
     non scritta a mano nel sorgente
  4. un gate rifiuta le copie non derivate
```

Il punto 3 è NX-11 generalizzato. Il punto 4 è Design Enforcement generalizzato.

---

## 3. Cosa resta valido della mia proposta, e cosa è nuovo

### 3.1 Resta valido: il gate

Avevo scritto: *"Graphic Authority senza gate è una linea guida, non un contratto."*
La tua roadmap lo mette a 0.7.0.2, subito dopo il consolidamento delle primitive.
Ordine corretto: prima sai cosa esiste, poi vieti il resto.

### 3.2 NUOVO e non coperto: Design Enforcement deve girare anche su X

Questo è il punto che nel tuo piano non vedo, ed è importante.

**Design Enforcement come lo descrivi è un controllo su codice scritto da umani:**
hex colors, `rgb`, `rgba`, `bg-blue-*`, `text-blue-*`, `bg-red-*`, `text-red-*`, con
eccezioni `brand` / `decorative` / `legacy`.

Ma X **genera** bundle. Se il controllo sta solo in lint/CI sul sorgente:

```text
umano scrive codice    → lint lo blocca        ✅
X genera un bundle     → il bundle non passa    ❌ bypass per costruzione
                         dal lint del sorgente
```

**X aggirerebbe Design Enforcement per costruzione**, non per errore.

Correzione richiesta: le stesse regole devono essere **anche** nel gate di
compilazione (NX-03 VALIDATE), applicate alla PageData generata, non solo al
sorgente scritto.

```text
Design Enforcement (0.7.0.2)
  ├── lint/CI sul sorgente          → per gli umani
  └── regole nel gate VALIDATE      → per X
      stesso ruleset, due punti di applicazione
```

Conseguenza pratica: il ruleset va definito come **dato dichiarativo** (una lista di
pattern + eccezioni), non come configurazione di ESLint. Se è dato, lo consumano
entrambi i punti. Se è config di lint, X non può usarlo.

**Questa è la singola cosa più importante da mettere in 0.7.0.2**, perché costa
poco adesso (stai già scrivendo il ruleset) ed è costosissima dopo (quando X genera
pagine che nessuno ha lintato).

### 3.3 Resta aperto: versione nel bundle

La mia proposta includeva `graphicAuthority: vN` nel bundle. Il tuo
`presentation.manifest.ts` copre l'identità per applicazione, ma non vedo un
riferimento di **versione del ruleset di design** con cui un bundle è stato validato.

Senza, non puoi rispondere a: *"questo bundle è stato validato con le regole di
design di tre mesi fa, vale ancora?"* È lo stesso problema del `content_sha` per i
contenuti: serve un'ancora di versione.

---

## 4. UX: limite o opportunità

Tesi dell'utente:

> *"la UX potrebbe essere un limite, o un'opportunità. Un limite perché non raggiunge
> la complessità dei competitors, un'opportunità perché la macchina cammina."*

### 4.1 La risposta sta nel verbo

D-021: ToolJet è **OPERA**, Open Nexus è **CAPISCE**. I due verbi richiedono superfici
diverse, e la differenza non è di quantità.

```text
OPERA richiede                    CAPISCE richiede
──────────────────────────────────────────────────────────────
form, input, validazione          testo leggibile
tabelle editabili                 evidenza e citazione
CRUD, azioni bulk                 confronto fra entità
dashboard configurabili           serie storica e variazione
80+ componenti                    score e soglia
drag & drop                       alert e anomalia
                                  timeline
                                  ────────────────
                                  ~12 primitive
```

**Non sei indietro. Sei dimensionato su un verbo diverso.** Ottanta componenti
esistono perché OPERA ha bisogno di ottanta modi di inserire dati. CAPISCE ha
bisogno di dodici modi di mostrare evidenza.

Costruire ottanta primitive per un prodotto CAPISCE sarebbe il vero errore: ti
metterebbe in competizione sul terreno di ToolJet, dove hanno 17.447 commit di
vantaggio, e diluirebbe la superficie che ti rende leggibile.

### 4.2 Perché è un'opportunità, strutturalmente

```text
ToolJet   80+ componenti accumulate nel tempo, senza Primitive Authority
          → ogni componente nuovo è una decisione locale
          → la coerenza dipende dalla review, che dipende dalle persone

Open Nexus Primitive Authority (0.7.0.1) + Design Enforcement (0.7.0.2)
          → ogni componente nuovo passa da un inventario chiuso e da un gate
          → la coerenza è enforcement, non disciplina
```

**La complessità UI puoi aggiungerla dopo. La governance della UI devi averla prima.**
Tu stai facendo la governance. Loro hanno fatto la complessità.

Da qui "è una spugna, puoi prendere tutto": con Primitive Authority in posto,
assorbire un pattern da ToolJet o da Instruqt significa **aggiungere una primitiva
all'inventario**, non riscrivere un renderer. Il costo di assorbimento crolla.

### 4.3 Sequenza corretta per Phase 4

Il documento allegato dice già la cosa giusta: *"Non la sposterei subito. Prima
censimento. Poi authority map. Poi consolidamento."*

Con una aggiunta: il censimento deve produrre **anche** la domanda di § 4.1 — cioè,
per ogni primitiva esistente: *serve a OPERA o a CAPISCE?*

```text
Explorer layer      → quasi tutto CAPISCE (toolbar, filters, stats, entity card,
                      grid). È il candidato naturale, e coincide con la lettura
                      del tuo agente.
Radix/UI layer      → misto. Alcune primitive sono OPERA pura (input, select,
                      form controls) e per un prodotto CAPISCE sono zavorra.
Common              → Navbar, TemplateHeader, ThemeToggle = infrastruttura,
                      va in Primitive Authority senza discussione.
```

Risultato atteso: **Explorer diventa Foundation Primitive Layer** (come ipotizza il
report) e Radix resta dipendenza tecnica sotto, non authority sopra. Cioè: Radix
fornisce il comportamento accessibile, Explorer fornisce il vocabolario. Due piani,
non due candidati in competizione.

---

## 5. "No regressioni" — il dato più forte della sessione

Phase 1, 2, 3 sulla source of truth, senza rotture. *"Qualche bordo, ma ci sta."*

Questo vale più di qualunque diagramma ho prodotto in tredici documenti:

```text
stratificazione 1-4   sopravvissute (pattern Astro+React, test all'80%)
stratificazione 5     authority refactor sulla source of truth, no regressioni
```

È la prova empirica della tesi di fondo, e adesso hai cinque punti dati invece di
quattro. Ed è anche la risposta pratica alla domanda IP: **un sistema che assorbe un
refactor della source of truth senza rompersi non è clonabile in dieci giorni**,
perché la proprietà che lo rende tale non è in nessun file — è nella disciplina di
assegnare ownership prima di scrivere codice.

### 5.1 I "bordi"

*"Qualche bordo, ma ci sta"* — vale la pena elencarli comunque. In un refactor di
authority, i casi bordo sono esattamente i punti dove un valore ha **due** proprietari
e nessuno se n'è accorto. Sono candidati F-01 in attesa di nome.

Da catturare prima che la memoria sfumi:

```text
□ quali componenti/pagine hanno mostrato comportamento inatteso
□ se il comportamento inatteso riguardava identità, tipo, visibilità o stile
□ se la correzione è stata "allineare la copia" o "cambiare la fonte"
   → se è stata la prima, c'è ancora una copia non derivata da qualche parte
```

---

## 6. L'avvertenza onesta

```text
0.7.0.1  Primitive Consolidation      interno
0.7.0.2  Design Enforcement           interno
0.7.0.3  Presentation Authority       interno
0.7.0.4  Admin New Era                interno
```

Quattro sub-release di architettura interna, **zero validazione esterna**.

È lo stesso pattern di rischio di NX-31 (la reference validation comoda) e vale la
pena nominarlo: il programma di authority è il lavoro che sai fare meglio, su un
sistema che conosci, senza dover parlare con nessuno. È il posto più confortevole
del progetto, ed è dove un autodidatta bravo può restare due anni.

Non sto dicendo di fermarlo — 0.7.0.1 e 0.7.0.2 sono prerequisiti veri per X, e
§ 3.2 mostra che 0.7.0.2 ha una decisione da prendere adesso che costa poco.

Sto dicendo che **NX-30 (il verticale) non può aspettare 0.7.0.4**. Deve correre in
parallelo, e non richiede codice: richiede conversazioni.

Ordine suggerito:

```text
0.7.0.1  Primitive Consolidation    ← fallo, è prerequisito di X
0.7.0.2  Design Enforcement         ← fallo, MA col ruleset come dato (§ 3.2)
NX-30    ricerca del segmento       ← in parallelo, non dopo
0.7.0.3  Presentation Authority     ← ha senso DOPO aver saputo chi è l'utente:
                                       "come un'applicazione esprime la propria
                                       identità" dipende da chi la guarda
0.7.0.4  Admin New Era              ← ultimo, ed è il meno urgente di tutti
```

Nota su 0.7.0.3: Presentation Authority risponde a *"come un'applicazione esprime la
propria identità"*. Ma l'identità si definisce rispetto a un pubblico. Progettarla
prima di sapere il pubblico significa progettarla per te stesso.

---

## 7. Voci di backlog

```text
NX-18  CHIUSO COME DUPLICATO → coperto da Primitive / Design / Presentation
       Authority. Resta valida solo la parte "gate", che è 0.7.0.2.

NX-34  NUOVO P0 — Design Enforcement con ruleset DICHIARATIVO, consumato sia
       dal lint/CI sia dal gate VALIDATE di NX-03. Altrimenti X bypassa
       l'enforcement per costruzione. (§ 3.2)

NX-35  NUOVO P2 — versione del ruleset di design referenziata nel bundle,
       come il content_sha per i contenuti. (§ 3.3)

NX-36  NUOVO P2 — nel censimento Phase 4, classificare ogni primitiva come
       OPERA o CAPISCE. Le primitive OPERA pure sono zavorra per la persona
       dichiarata. (§ 4.3)

NX-37  NUOVO P2 — elenco dei "bordi" del refactor authority, con verifica che
       la correzione sia stata sulla fonte e non sulla copia. (§ 5.1)

Q-005  RISTRETTA — applicationType è dichiarato in src/config/applications?
       Un grep risponde. Probabilmente sì → NX-11 diventa lavoro piccolo.
```

---

*Ultimo aggiornamento: 2026-09-12*
