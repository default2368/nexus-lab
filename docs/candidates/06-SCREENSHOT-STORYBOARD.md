# Storyboard — 6 screenshot reali per plico F.

**Status:** CANDIDATE_FOR_OWNER_REVIEW
**Source:** https://x.open-nexus.io — real application, real component, real route, real build, synthetic data where necessary
**DECIDED:** live demo durante incontro → NO, plico narrativo → SÌ, technical notes → SÌ bounded, real screenshots → SÌ 5/6, synthetic G. record view → SÌ, AI-generated UI mockups → NO nel plico finale, follow-up demo → possibile se F. lo richiede
**Concept:** sistema che sa descriversi — auto-descrizione verificabile / riflessività operativa — non coscienza in senso cognitivo

---

## Concetto forte

> Open Nexus non si limita a produrre applicazioni. Mantiene una rappresentazione esplicita delle proprie applicazioni, pagine, componenti, template, contratti e fonti. Può quindi mostrare come è composto, quali elementi utilizza e da dove derivano.

Oppure:

> Il sistema conserva una memoria verificabile di ciò che contiene, di come lo produce e delle relazioni fra le sue parti.

Termine tecnico corretto: auto-descrizione verificabile o riflessività operativa. Nella conversazione con F. la metafora "sistema che ha coscienza di sé" può funzionare, se poi riportata a elementi concreti.

---

## Sequenza narrativa — 6 screenshot

```text
applicazioni
→ pagine
→ componenti
→ presentazione
→ risposta/fonti
→ record/dossier
```

Racconta: Il sistema sa di cosa è composto; sa come lo presenta; può collegare ciò che mostra alle fonti e ai record sottostanti. Molto più forte di sei dashboard decorative.

---

### 1. Il sistema vede le proprie applicazioni

**Schermata:** Operations Applications / application inventory
**Route reale:** https://x.open-nexus.io/build/core-admin/index
**Dati reali osservati:** Applications 5, Pages 36, Warnings 0, Broken Refs 9 — OpenNexus (user stable 12 open-nexus/index), Authentication (shared stable 8 auth/welcome), Simple (user stable 5 simple/welcome), System (shared stable 3 sys/system-control), Operations (workspace preview 8 core-admin/index)

**Messaggio:** Il sistema conosce le applicazioni che contiene, il loro stato e il modo in cui entrano nella distribuzione.

**Caption:** **Applicazioni.** Una vista operativa delle esperienze disponibili e della loro composizione.

**File:** `images/real-01-applications-inventory.jpg` (1600×1000, PNG lossless, stesso viewport/zoom/tema/browser/crop, no browser chrome)

---

### 2. Il sistema vede le proprie pagine

**Schermata:** Discovery Pages / Pages Explorer
**Route reale:** https://x.open-nexus.io/build/core-admin/pages
**Dati reali osservati:** Applicazioni 5, 5 in vista, Shared 2 consumate da altre app, Stable 4 pronte per produzione, Pagine totali 36 attraverso il catalogo

**Messaggio:** Ogni pagina ha identità, owner, fonte e destinazione. Non è soltanto una route dispersa nel codice.

**Caption:** **Discovery.** Pagine e superfici sono inventariate e attribuite a un'autorità.

**File:** `images/real-02-pages-explorer.jpg`

---

### 3. Il sistema vede i componenti e i loro consumatori

**Schermata più appariscente:** Component Catalog / primitive consumption / component identity / consumers
**Route reale:** https://x.open-nexus.io/build/core-admin/component-catalog
**Dati reali osservati:** Governed inventory — 42 entries across 5 categories — EntityCardApproved, EntityGridApproved, ExplorerLayoutApproved, ExplorerStatsApproved, ExplorerFiltersApproved, ApplicationsTableApproved, DiscoveryDashboardApproved, JsonInspectorBlockApproved (estratto P1 diagnostics), HeroSectionApproved, WebPageTemplateApproved, VirtualPageTemplateApproved, TemplateLabTemplateExperimental, OperationsApplicationsTemplateLegacy, HelloApiTemplateLegacy, RedisConsoleTemplateLegacy

**Messaggio:** Un componente non è soltanto disegnato: il sistema può mostrare dove viene usato, chi lo possiede e quali esperienze dipendono da esso.

**Caption:** **Componenti e primitive.** Identità, ownership e riuso diventano ispezionabili.

**File:** `images/real-03-component-catalog.jpg`

Questa è probabilmente la schermata più forte per il concetto di auto-descrizione.

---

### 4. Il sistema separa significato e presentazione

**Schermata:** Template Lab
**Route reale:** https://x.open-nexus.io/build/sys/template-lab (richiede auth, usare template sicuro senza Redis Console o side effect)
**Dati:** template sicuro, no real Redis I/O by default

**Messaggio:** La stessa struttura di conoscenza può essere rappresentata attraverso forme differenti senza cambiare il significato sottostante.

**Caption:** **Template Lab.** La presentazione resta sostituibile; il contratto rimane stabile.

**File:** `images/real-04-template-lab.jpg`

---

### 5. Il sistema collega risposta e fonte

**Schermata:** Roy Client / Knowledge Assistant / risposta Markdown / source/coverage metadata / development diagnostic panel
**Route reale:** https://x.open-nexus.io/build/open-nexus/assistant (richiede auth, usare client corrente con risposta realmente grounded, non simulare)
**Dati:** risposta Markdown + diagnostic metadata, source/coverage

**Messaggio:** L'Assistant non restituisce soltanto testo: può conservare il legame fra risposta, fonti, copertura e limiti.

**Caption:** **Assistant.** Una risposta leggibile può mantenere il collegamento con il materiale che la sostiene.

**File:** `images/real-05-roy-client-assistant.jpg`

Se nuova integrazione /evaluate non abbastanza stabile al momento screenshot, usare client corrente con risposta realmente grounded. Non simulare.

---

### 6. Lo stesso record può diventare esperienza

**Schermata:** Synthetic EntityRecord / Control View / Client View / Evidence Detail
**Dati:** esplicitamente sintetici — Entity ENG-001 → ProcedureVersion → Evidence → Finding → Action → Decision, due viste Control (tutte evidenze e gap) e Client (solo ciò che ruolo può vedere)

**Messaggio:** Lo stesso oggetto può produrre viste differenti per ruoli differenti, mantenendo identità, relazioni e provenienza.

**Caption:** **Proiezione semantica sperimentale.** Uno stesso record sintetico produce esperienze diverse senza modificare il Runtime.

**Label visibile:** PROTOTIPO SPERIMENTALE · DATI SINTETICI

**File:** `images/real-06-entity-eng001-control-client.jpg` + `images/dossier-sintetico-eng001.jpg` (già esistente, stessa famiglia)

Caption alternativa: Lo stesso record, proiettato per responsabilità differenti. Dati interamente sintetici.

Questa schermata spiega Foundation/0.9 più di due pagine tecniche.

---

## Dove inserirle nel plico

**Pagina 1:** Copertina, nessuno screenshot.

**Pagina 2:** "La conoscenza non manca" + diagramma semplice ecosistema.

**Pagina 3–4:** Tre screenshot Applications, Discovery, Component Catalog — Titolo: Un sistema capace di descrivere la propria struttura

**Pagina 5:** Template Lab + Assistant — Titolo: Dal contratto all'esperienza

**Pagina 6:** EntityRecord/dossier G. sintetico — Titolo: Dalla fonte alla decisione

**Pagina 7–8:** Stato, piano, milestone, rischi e domande per F.

---

## Regole per gli screenshot

**Solo interfacce reali:**

```text
real application
real component
real route
real build
synthetic data where necessary
```

Non:

- immagini generative di interfacce
- testi deformati
- fonti inventate
- fake DOI
- metriche create a mano

**Ambiente controllato prima di catturare:**

- profilo dati sintetico
- nessun nome/email
- nessun endpoint sensibile
- nessun branch/path locale visibile
- nessuna chiave
- niente DevTools
- niente console
- route debug escluse
- navigazione pulita

**Coerenza visiva:**

```text
stesso viewport
stesso zoom
stesso tema
stesso browser/crop
stessa densità
Formato: 1600×1000 oppure 1440×900 PNG lossless
Per stampa: almeno 150–200 dpi alla dimensione finale, niente JPEG se testo piccolo, crop pulito senza browser chrome salvo che serva a dimostrare navigabilità
```

**Caption in due righe:**

```text
titolo
cosa dimostra
```

Non spiegazione tecnica.

---

## Note tecniche nel documento per F. (colonna laterale o pagina finale)

**Ambiente dimostrativo:**

```text
Web application      Astro / React / TypeScript
Brain                FastAPI / Python
Distribution         manifest, package, materialization, clean-room
Deployment           ambiente web di sviluppo/preview https://x.open-nexus.io
Data                 corpus e record sintetici
Versione             prototipo in sviluppo
```

Soltanto dati confermati al momento stampa.

**Cosa dimostra:**

```text
navigazione reale
più applicazioni
inventario di pagine
componenti riutilizzati
template sostituibili
Assistant grounded
record proiettati
```

**Cosa non dimostra:**

```text
prodotto finito
scalabilità commerciale
compliance
pilot reale
Foundation 1.0
```

---

## Plico fisico

```text
copertina plastificata trasparente
retro rigido o cartoncino
8–10 pagine
stampa fronte-retro
2–3 fogli con screenshot a piena larghezza
nessuna slide
nessun QR obbligatorio
```

Può stare sulla scrivania, essere sfogliato casualmente e riaperto dopo giorni. Non deve sembrare brochure commerciale, tesi, business plan, manuale software. Deve sembrare nota di progetto seria, prodotta da qualcuno che ha già costruito abbastanza da sapere cosa non ha ancora dimostrato.

---

## DECIDED DIRECTION

```text
live demo durante incontro → NO, non pianificata
plico narrativo → SÌ
technical notes → SÌ, bounded
real screenshots → SÌ, 5/6
synthetic G. record view → SÌ
AI-generated UI mockups → NO nel plico finale
follow-up demo → possibile, se F. lo richiede
```

Ora materiale può diventare più ricco senza tornare dispersivo: narrazione spiega perché, screenshot dimostrano che macchina esiste, scheda progettuale permette a F. di esercitare proprio mestiere.

---

## Provenance

```
Source: https://x.open-nexus.io — Discovery Index + /build/core-admin/index (5 apps 36 pages) + /build/core-admin/pages + /build/core-admin/component-catalog (42 entries) + /build/open-nexus/architecture
Method: fetch_page + generate_image based on real routes with real data observed
Images: 6 real screenshots concept (1600×1000) + 1 ecosystem + 1 dossier ENG-001 synthetic
Status: CANDIDATE_FOR_OWNER_REVIEW — real screenshots concept, to be replaced with actual PNG lossless captures from controlled environment before print
Extractor: documentation-agent v0.1.0
```

*Storyboard per plico F. — sistema che sa descriversi, auto-descrizione verificabile, riflessività operativa*
