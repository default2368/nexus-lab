# NEXUS LAB — Backlog NX

Derivato dall'analisi Trustable/Nuvolaris del 2026-09-10.

## Proprietà del backlog

```text
NESSUNA voce tocca:
  PageController · normalizeToPageData · ApplicationDefinition
  ApplicationContext · BundleCollector · DiscoveryService / DiscoveryServiceV2
  PageData

NX-02 e NX-03 sono X, non Foundation.
```

**Conseguenza operativa:** l'intero backlog è eseguibile in modalità brainstorming
senza rischio architetturale. Vedi `03-WORKFLOW.md` § "Zona sicura".

**Regola di ingaggio:** se durante l'esplorazione una proposta richiede di modificare
uno dei simboli qui sopra, **non è più brainstorming**. Diventa una *Foundation RFC*
e cambia processo: serve audit MCP, serve `deepseek-v4-pro`, serve decisione esplicita
nel Decision Log.

---

## Tabella

| ID | Azione | Pri | Layer | Origine | Stato |
|---|---|---|---|---|---|
| **NX-01** | Spec licenza offline firmata per Nexus CLI (track **on-prem**) | P2 | CLI/Distribuzione | Trustable § 3.1 | aperto |
| **NX-01b** | **Foundation API tokenizzata — split PRODUCE remoto / EXECUTION locale** (track **hosted**) | P2 | Distribuzione | Brainstorm 2026-09-10 | aperto |
| **NX-02** | Workflow Contract: `workflow.md` dentro `ApplicationBundle` | P2 | X | Trustable § 3.3, 3.4 | aperto |
| **NX-03** | Gate `VALIDATE` fra generazione e `BundleCollector` | P2 | X | Trustable § 4.3 | aperto |
| NX-04 | Provider abstraction Brain: validazione URL, catalogo, probe `OK` | P1 | Brain | Trustable § 3.2 | aperto |
| NX-05 | Regole enforced server-side, non solo client | P1 | Brain/API | Trustable § 1.4 | aperto |
| NX-06 | Concorrenza ottimistica sul save remoto dei contratti | P1 | X | Trustable § 3.3 | aperto |
| NX-07 | Narrativa tre tier + pagina pubblica | P2 | Marketing | Trustable § 3.5 | aperto |
| NX-08 | Doc pubblica che difende le decisioni | P2 | Marketing | Trustable § 5.1 | aperto |
| NX-09 | Indice pubblicato per starter/bundle, non query live | P2 | CLI | Trustable § 5.3 | aperto |
| NX-10 | Verifica collisioni marchio / decisione nome pubblico — **assorbito da NX-81** | P1 | Legale/Brand | Dossier § 6.4 + D-052 | aperto |
| **NX-11** | **RIFORMULATO (D-028):** materializzazione manuale → **generata** dal build. Q-005 risolta: `applicationType` è dichiarato in `src/applications/*/package.ts`. Prerequisito di 0.7.0 Authoring, non di 0.6.x | P1 | Bundle | `15-APPLICATION-AUTHORITY-EVIDENZE.md` § 0.3 | aperto |
| **NX-12** | Fallback per `appId` assente nella projection | P1 | X | `05-AF001-VERDETTO.md` § 5.D | aperto |
| NX-13 | Catalog API → superficie Foundation API (da `/api/catalog/*` esistenti) | P1 | Distribuzione | P-007 | aperto |
| **NX-14** | **`nexus-mcp` come repo separato, licenza permissiva, bundle precompilato, plugin Claude Code/Codex/Cursor** | P2 | Distribuzione | ToolJet § 5.4 | aperto |
| NX-15 | Layout a sensibilità: repo pubblico + submodule EE + symlink + sync script idempotente (`--check` in pre-commit) | P1 | Repo/IP | ToolJet § 4.3 | aperto |
| NX-16 | Skill di processo nel repo (`commit`, `create-pr`, `merge`) per strumentalizzare il loop | P2 | DevEx | ToolJet § 6 | aperto |
| NX-17 | Cataloghi di template/renderer **generati** dal BundleCollector ed esposti via MCP | P1 | X | ToolJet § 5.5 | aperto |
| ~~NX-18~~ | ~~Graphic Authority~~ **CHIUSO COME DUPLICATO** — coperto da Primitive / Design / Presentation Authority già esistenti. Resta valida solo la parte gate, che è 0.7.0.2 + NX-34 | — | — | `14-AUTHORITY-ARCHITECTURE.md` § 0 | **chiuso** |
| **NX-19** | **Nessun LLM nell'osservazione continua**: trigger deterministici + batch con tetto | P1 | X/Brain | § 2 | aperto |
| **NX-22** | **RICALENDRIZZATO (D-047):** i due tier non sono "Builder / Decision-maker" ma "chi costruisce" / **CHI DEVE RENDERE CONTO** (= Y) | P1 | Prodotto | § 1.3 + D-047 | aperto |
| NX-20 | Local-first con ping Redis → chiude AF-003 e AF-004 | P1 | Execution | § 4 | aperto |
| NX-21 | Interfaccia plugin per connettori (interfaccia, non libreria) | P1 | X | § 5 | aperto |
| NX-23 | Policy dati locali sensibili per persona finanziaria (TTL, cifratura, consenso) | P1 | Sicurezza | § 4.4 | aperto |
| **NX-24** | **Strumentazione costo per chiamata LLM** (input/cached/output/reasoning + classe 0–4) su `AIRedisLogger` esistente | P1 | Brain | `08-COST-CULTURE.md` § 4 | aperto |
| **NX-25** | Model ID DeepSeek: **CONFERMATO ritirato** `deepseek-v4-flash` → `deepseek-flash`. Doc del workspace bonificati; **mancano le config degli strumenti** (Roo/Cline/Continue/Trae/Brain) | 5 min | Config | `08-COST-CULTURE.md` § 0 | parziale |
| **NX-26** | **Provider Layer per il server nuovo** (base/catalog/routing/budget/reduce) — assorbe NX-04, NX-05, NX-24 | P1 | Brain | `09-SERVER-PROVIDER-LAYER.md` | aperto — finestra refactor |
| NX-27 | **Connector Layer**: interfaccia unica `Fetched`; libreria di scraping esistente → `HttpHtmlConnector`; change detection via `content_sha` + conditional request | P1 | Brain/reduce | `11-CONNECTOR-LAYER.md` | aperto |
| NX-28 | `JsonApiConnector` — per la persona broker/CFO è il connettore a più alto valore | P1 | Brain/reduce | `11-CONNECTOR-LAYER.md` § 4 | aperto |
| NX-29 | `PdfConnector` — filing, bilanci, report | P2 | Brain/reduce | `11-CONNECTOR-LAYER.md` § 4 | aperto |
| **NX-30** | **Scelta del verticale + falsificazione di "il mercato premia il contenuto, non il meccanismo"** | P1 | Prodotto | `12-MERCATO-CONOSCENZA.md`, Q-010 | aperto — non richiede codice |
| **NX-31** | **RIVALUTATO (`20-...` § 9):** era la forma iniziale della capacità di analisi di mercato, non una tassonomia auto-riferita. Output PUBBLICO, non interno | P1 | X | `20-CAPABILITA-ANALISI-MERCATO.md` | riaperto |
| NX-32 | Regola "ogni operazione di X lascia un residuo" come criterio di accettazione nei PRD di X | P1 | X | § 1.3 | aperto |
| NX-33 | Profilo di competenza per NX-30 (**dominio, non architettura**) | P2 | Team | § 2.2 | bloccato da NX-31 |
| **NX-34** | Design Enforcement con ruleset dichiarativo consumato da lint/CI **e** dal gate VALIDATE. **RICALIBRATO da D-034**: per X è vocabulary-check, non palette-check | P1 | Design/X | `14-...` § 3.2 + D-034 | **fatto per il design** (script), manca il lato X |
| NX-35 | Versione del ruleset referenziata nel bundle (come `content_sha` per i contenuti) | P2 | Foundation | `14-...` § 3.3 | aperto |
| NX-36 | Nel censimento primitive, classificare ognuna come OPERA o CAPISCE | P2 | X/UI | `14-...` § 4.3 | **probabilmente già fatto** (ADR-0012) — da confermare |
| NX-37 | Elenco dei "bordi" del refactor authority + verifica fonte vs copia | P2 | Foundation | `14-...` § 5.1 | aperto — **deperibile** |
| **NX-38** | **P0 (D-038)** — Rimuovere `as any` da `src/config/applications/*`: `DiscoveryMetadata` non è enforced nel punto di scrittura | **P1** | Definition | `15-...` § 3.1 · D-035 | aperto — finestra 0.7.0.2b |
| **NX-39** | **P0 (D-038)** — `notFound` accetta `'/'` ma il contratto dichiara *registryId*: stringere il tipo o normalizzare in `factory.ts` | **P1** | Definition | `15-...` § 3.2 | aperto — finestra 0.7.0.2b |
| NX-40 | Documentare il criterio di ripartizione Definition (`src/config/applications`) vs Bundle (`src/applications/*/package.ts`) | P2 | Doc | `15-...` § 1.3 | aperto |
| NX-41 | Collisione di vocabolario: `type:'user'` (visibilità) vs `audience:'user'` (persona) | P2 | Contratti | `15-...` § 2.1 | aperto |
| **NX-42** | **`audience` non contiene il decision-maker** — blocca 0.7.0.3 Presentation Authority | **P1** | Prodotto | D-031 | aperto |
| **NX-43** | Vocabolario status come dato dichiarativo: runtime degrada a muted, build rifiuta. Per X è vocabulary-check (D-034) | **P1** | Design/Primitive | D-033 + D-034 | aperto |
| ~~NX-44~~ | **RISOLTO**: `walk()` con `readdirSync` su tutto `src/`, eccezioni che sottraggono → scope derivato, **fails CLOSED**. Residuo congelato: sovrapposizione vitest/script | — | Test | Q-011 | **chiuso** (trigger: nuova primitiva o chiusura 0.7.0.2) |
| NX-45 | Verificare se PageData ammette escape hatch visuali (`className`, `style`, HTML libero). Determina la forma del gate VALIDATE | **P1** | Contratti | D-034 | aperto |
| **NX-46** | Aggiungere `expires` al DATO `EXCEPTIONS` (oggi sta solo nel doc) e far fallire `--ci` a scadenza superata | **P1** | Design | `16-FOUNDATION-HEALTH.md` § 4.2 | aperto |
| NX-47 | `legacy-frozen:pages` include `src/pages/build/` con match a prefisso: il punto d'ingresso di EXECUTION è esente, e ogni file nuovo lì sotto lo è automaticamente | P2 | Design | § 4.3 | aperto |
| NX-48 | Verificare il meccanismo per-file del gate `--ci`: con 554 errori `--ci` esce 1, quindi il "per-file once migrated" sta altrove | P2 | CI | § 4.3 | aperto |
| **NX-50** | **Bonifica tenant: file CANCELLATI (2026-09-16).** Residuo da verificare: cestino di primo e secondo livello, cronologia versioni, indicizzazione Copilot, eventuali retention policy del tenant | 5 min | IP/Legale | `18-...` § 0 | **parziale** |
| **NX-49** | **Prima applicazione SONDA** (D-041: la sonda non è il verticale). **AGGIORNATO da `24-...` § 8:** se è job-seeker, va MIRATA al payer B2B (career service/outplacement, ~$387/cliente/anno) e non al candidato ($0,25/utente/anno) | P1 | X | D-040, D-041, NX-61 | in corso altrove |
| **NX-52** | **Colmare le 4 lacune del METODO Sonda**: L-1 criterio di arresto · L-2 seconda sonda nominata · L-3 time box · L-4 pubblico nominato | P1 | Metodo | D-041 | aperto |
| **NX-54** | Regola **staleness dell'evidenza esterna**: un campo di evidenza `pending` oltre N giorni → `insufficient-evidence`. Vale per il metodo Sonda anche SENZA script. Chiude L-1 in modo strutturale | **P1** | Metodo | `19-METHOD-AGENT-GIUDIZIO.md` § 5 | aperto |
| NX-53 | `check-proposal.mjs` — generalizzazione di `check-style-authority.mjs` applicata ai proposal record. Classe 0, deterministico, `--json`/`--ci` | P2 | Governance | § 4, § 7 | **non prima di un ciclo di sonda reale** |
| NX-55 | ~~Method Agent come prodotto~~ **RICLASSIFICATO da `20-...` § 4:** il mercato non è agent-governance ma **architecture & market intelligence**. Resta valido il vincolo: niente "prodotto" senza payer verificato | P2 | Prodotto | `20-CAPABILITA-ANALISI-MERCATO.md` § 4 | riclassificato |
| **NX-56** | **Portare le 4 analisi esistenti in PageData e pubblicarle** su `open-nexus/library`·`topics`·`generated-knowledge`. Un artefatto, tre effetti: portfolio + demo di prodotto + dataset per NX-30 | **P1** | X | `20-...` § 7 | aperto — prototipo già scritto |
| **NX-57** | **P0 ↑ — Test di ripetibilità**: analisi su oggetto NUOVO usando SOLO il metodo scritto, senza intervento. **Non è più un test di qualità: è il prerequisito perché la motion NX-104 sia prodotto invece che consulenza** | P0 | Metodo | `20-...` § 8.1 + `32-...` § 3.2A | aperto |
| NX-58 | Schema dell'analysis/proposal record come FILE versionato, con campi `observed` / `inferred` / `recommended` e obbligo di fonte per ogni osservazione | P2 | Governance | `20-...` § 9 | aperto |
| NX-59 | **Tokenizzazione locale prima del confine LLM** — incapsulare Presidio, mappa in IndexedDB+WebCrypto (NON localStorage). **Prerequisito del verticale civico/PA, NON del pilota.** Non prima di NX-30 | P2 | Brain/reduce | `22-PRIVACY-TOKENIZZAZIONE.md` | aperto — bloccato da NX-30 |
| NX-60 | Verifica con **DPO** della formulazione del claim privacy prima che compaia in qualunque documento pubblico o di gara | P3 | Legale | `22-...` § 6 | aperto |
| **NX-61** | **Scansione di mercato per CAPACITÀ** (non per categoria app): assi prioritari doc-20 · C-01 · M-06 · C-07, minimo 5 inserzioni con ricavo dichiarato per asse, matrice con ricavo/testa e multiplo | **P1** | Prodotto | `24-SCANSIONE-PER-CAPACITA.md` | aperto — corregge la scansione già fatta |
| NX-62 | Estensione a piano 2 (Product Hunt, Indie Hackers) — il piano 1 discrimina (§ 8), sbloccato ma dopo NX-63 | P2 | Prodotto | `24-...` § 6 | aperto |
| NX-63 | Portare la sottocapacità **"analyst/developer utility"** (proposizione B) a n≥5. Unica con multiplo alto E vicinanza al gate. Se regge, riordina le sonde | **P1** | Prodotto | `24-...` § 8.4 | aperto |
| NX-64 | **Filtro di sostituibilità**: per ogni inserzione e ogni sonda, dichiarare se l'80% del risultato è ottenibile gratis da un LLM generalista. Se sì, multiplo atteso < 1× | **P1** | Metodo | `24-...` § 8.3 | aperto |
| NX-65 | Banda di valore di riferimento: $11k–$50k ARR · 200–300 sub B2B o ~1.000 prosumer · 2,7–3,0× · asset $30k–$150k | P2 | Prodotto | `24-...` § 8.2c | aperto |
| **NX-66** | **SERIE STORICA** delle inserzioni già raccolte: campi `esito` · `prezzo_finale` · `delta`. Riletture dic-2026 / mar-2027 / giu-2027. **Se non si registra ora, le 7 dell'Asse 1 sono perse** | **P1** | Prodotto | `24-...` § 11 | aperto — deperibile |
| **NX-67** | **SCANSIONE PRODUCT MARKETPLACE** (Envato · Gumroad · boilerplate · Astro Themes · Notion templates · MCP a pagamento · AppSumo). Risponde al track NX-01/NX-14, non al track NX-49 | **P1** | Prodotto | `24-...` § 10 | aperto |
| NX-68 | Registrare la **piattaforma di vendita come variabile di margine**: Envato 30–62,5% vs vendita diretta ~2,9%. Scarto 3–6× sul netto | P2 | Distribuzione | `24-...` § 10.3 | aperto |
| **NX-69** | **Governance come TIER DI PREZZO**: read-only (propone) vs read-write (modifica, con gate + approvazione + audit trail). GoMarble lo vende. Non va costruito, va impacchettato | **P1** | Prodotto | `24-...` § 12.1 | aperto |
| **NX-70** | **Onboarding / curva di apprendimento** — l'unica frizione letale per la persona dichiarata (manager/CFO/broker) senza risposta architetturale. Le 6 authority non la risolvono | **P1** | Prodotto/UX | `24-...` § 12.4 | aperto — non era a backlog |
| NX-71 | Verificare il **pavimento open source** per ogni capacità orizzontale candidata. Regola: se esiste un pavimento mantenuto, l'orizzontale non monetizza in piccolo | P2 | Prodotto | `24-...` § 12.5 | aperto |
| NX-72 | Il **premio di verticale 7–70×** è evidenza quantitativa per NX-30 | P2 | Prodotto | `24-...` § 12.2 | aperto |
| **NX-73** | **LA FRASE** — verbo + oggetto + beneficiario. Candidata: *"Fa le ricerche al posto tuo, e si ricorda dove ha trovato ogni cosa."* Test: dirla a 5 persone (≥3 non tecniche) e chiedere **il giorno dopo** cosa ricordano. È anche la prima conversazione mancante | P1 | Prodotto | `26-CHI-E-Y.md` § 3, § 7 | aperto — costo zero |
| **NX-74** | Regola scritta: **l'AI entra in scena una volta sola, nell'interpretazione**. Ogni altro punto di ingresso va motivato per iscritto. Test: togli l'AI, il prodotto produce ancora qualcosa di utile? | **P1** | Metodo | D-048 | aperto |
| **NX-75** | **Matrice di scoring delle istanze candidate** contro i criteri K1–K8 già stabiliti. Nomenclatura: X → Ambiente → Istanza | P1 | Prodotto | `27-SCORING-ISTANZE.md` | **fatto, da ratificare** |
| NX-76 | **A (pagina personale) riclassificata**: non è istanza, è infrastruttura di pubblicazione. Prerequisito di NX-56 | P1 | X | `27-...` § 4 | aperto |
| NX-77 | Verificare il pavimento open source per E (competitive intelligence con evidenza). **Se esiste, la raccomandazione si inverte a favore di D** | P2 | Prodotto | `27-...` § 5 | aperto |
| **NX-78** | **Test del frame su E**: dopo la pubblicazione, contare le richieste da persone che non sono l'utente. Zero richieste → E era ricerca interna travestita | **P1** | Prodotto | `27-...` § 3 | aperto |
| **NX-79** | **COLLOQUIO CON Y-1** (il volontario). Non per vendere: estrarre la lista ESATTA delle domande tecniche a cui non sapeva rispondere. Doppio uso: specifica di `nexus-builder` + test di completezza delle authority. È la prima conversazione reale | P2 | Prodotto | `27-...` § 6.7 | aperto — costo zero |
| NX-80 | Verificare la convergenza **Y-1/D**: stessa frizione ("non voglio rispondere a domande tecniche"), payer opposti. Se confermata, la proposition va scritta per D | P2 | Prodotto | `27-...` § 6.6 | aperto |
| **NX-81** | **Gerarchia dei nomi**: sei nomi in circolo (OpenFav · Open Nexus · Nexus Lab · nexus-builder · nexus-mcp · opnx) e nessuno decide. Verificare collisioni su `nexus-builder`. NX-10 era P2, questo è P1 perché c'è un nome di prodotto in circolazione | **P1** | Brand | D-052 | aperto |
| NX-82 | Principio **"mostra, non chiede"**: ogni domanda posta all'utente è un default mancante in un'authority. Da scrivere come vincolo di prodotto per nexus-builder e da usare come criterio nei PRD | P1 | Prodotto/Metodo | D-050 | aperto |
| NX-83 | Frasi candidate per nexus-builder (NX-73 applicato): da testare su 5 persone con richiamo il giorno dopo | P1 | Prodotto | § NX-73 | aperto — costo zero |
| **NX-86** | **Prerequisito non negoziabile.** Bonifica eseguita (NX-50 parziale). **Resta la verifica con un legale** su incompatibilità e autorizzazioni per attività extra-istituzionali — e resta il campo mittente vuoto nei documenti per A. | P0 | IP/Legale | `28-...` § 5 | **parziale — resta il legale** |
| **NX-84** | **K4 VERIFICATO**: incumbent forte (Informatica EDP, 3.000+ aziende, €125/utente/mese di listino). Opportunità A ed E **già coperte**. Restano da verificare B, C, D e l'esistenza di un'API | P1 | Prodotto | `29-PROMETEO-ANALISI.md` § 0, § 3 | parziale |
| **NX-85** | **RICALENDRIZZATO (D-056/057):** A. sta in ORBITA, non in pipeline. Non le 13 domande: un piccolo artefatto utile, già fatto, senza pitch. Le domande si fanno solo a condizione di conversione verificata (D-058) | P1 | Prodotto | D-056 → D-058 | aperto |
| ~~NX-87~~ | Documento ricevuto e analizzato in `29-PROMETEO-ANALISI.md` | — | Doc | `28-...` | **chiuso** |
| NX-88 | BRAIN-006 (aggiornare le viste dipendenti da una norma modificata) richiede un **grafo di dipendenza fra contenuti**: unica capacità del pilot non coperta da C-01..C-08 | P2 | X | `28-...` § 6 | aperto |
| **NX-89** | **L'artefatto-dono per A.** (D-057): una knowledge experience su UNA materia delimitata, con fonti, date, versioning. È il pilot di § 9 concepito come dono invece che come prodotto. Stesso lavoro di NX-49, con destinatario reale | P2 | X | D-057 | aperto |
| NX-90 | **ATTIVO ORA.** Condizioni di conversione dell'orbita (D-058): chiede due volte la stessa cosa · presenta qualcuno con budget · dice "quanto costerebbe" · condivide dati interni non richiesti. Cadenza 4–6 settimane con qualcosa di concreto, mai "come va" | P1 | Prodotto | D-058 | in corso — attesa risposta |
| **NX-91** | **IN VIAGGIO.** La domanda è § 7.1 della nota inviata: "quando dicevi 'siamo noi', a chi ti riferivi?". Non più da fare: da aspettare | P1 | Prodotto | `29-...` § 6, D-090 | **in attesa di A.** |
| NX-92 | **Layer forense versionato**: ricostruire cosa era vero in una data, secondo la norma allora vigente, con catena documentale. È ciò che un gestionale non può fare per costruzione. Da validare se A. è lato legale | P1 | X | `29-...` § 4.1 | bloccato da NX-91 |
| NX-93 | Verificare se Prometeo gestisce già la vista multi-azienda per consulenti/associazioni (Opportunità C). Se sì, anche C è coperta | P2 | Prodotto | `29-...` § 3 | aperto |
| ~~NX-94~~ | **RISOLTO dall'utente: "A. è una risorsa"** → modalità ORBITA (D-056), non pipeline e non co-founder. La questione co-founder resta sospesa a NX-86 | — | Team | D-063, D-090 | **chiuso** |
| **NX-95** | **Le tre domande ad A.** (§ sotto). La prima è su cosa intendeva, la seconda è su di lui, la terza è sul dolore di Prometeo | P1 | Prodotto/Team | D-063→D-067 | aperto — costo zero |
| ~~NX-96~~ | **FATTO**: WordPress 7.1 + Elementor SSR, non statico. 153 pagine / 206 post / 855 media, **zero custom post type verticali**. Namespace `mcp` e `wp-abilities/v1` esposti | — | Prodotto | D-068, D-069 | **chiuso** |
| NX-97 | **Condizione di conversione** scritta e datata per il cavallo di Troia: entro X mesi l'accesso deve aver prodotto Y. Senza, è collezionismo di relazioni | P1 | Prodotto | D-066 | aperto |
| **NX-98** | **Ontologia normativa** come asset: `norma ↔ obbligo ↔ ruolo ↔ modulo ↔ caso cliente ↔ versione ↔ CTA`. L'ingestione è commodity (REST + MCP pubblici), l'ontologia no — e richiede dominio | **P1** | X | D-069 | aperto |
| **NX-99** | **Grafo di dipendenza norma → contenuti, versionato nel tempo.** È NX-88/BRAIN-006. **Una capacità, due viste, due payer**: redazione ("ecco le 40 pagine impattate") e legale ("cosa era vero in quella data") | **P1** | X | D-070 | aperto |
| NX-100 | Connettore WordPress: `/wp-json/wp/v2/{pages,posts,media}` + sitemap. Lavoro minimo, il namespace `mcp` esiste già | P2 | Brain/reduce | D-069 | aperto — quasi gratuito |
| **NX-102** | **Pilot in DUE STADI** (sintesi delle due simulazioni). Stadio 1 — *caso*: un caso reale già chiuso che è costato tempo, ricostruzione insieme della catena fatto → documento → norma → versione → ruolo → decisione, si osserva dove si spezza. Stadio 2 — *struttura*: UNA norma specifica, numero limitato di contenuti, si verifica se il grafo regge. Non un progetto, non un preventivo: un esperimento | **P1** | Prodotto | D-086 | aperto — è il secondo incontro |
| NX-103 | **Formalizzare la protezione dati PRIMA di qualunque prova**: chi tratta cosa · per quanto · base giuridica · traccia. § 4.5 ora elenca i quattro punti, ma resta da produrre il documento | P1 | Legale | D-086 | aperto |
| **NX-104** | **Formalizzare la motion `Y-idea-site-knowledge` in sei passi** come procedura scritta, eseguibile da un agente. È NX-57 applicato | **P1** | Prodotto | `32-MOTION-Y-IDEA-SITE-KNOWLEDGE.md` § 1 | aperto |
| **NX-105** | **Definire la PERSONA dietro la condizione.** "Conoscenza accumulata non esprimibile" è il bisogno; chi lo sente E ha voce in capitolo? (CTO ≠ marketing ≠ qualità ≠ titolare: quattro prodotti diversi) | **P1** | Prodotto | `32-...` § 2.1 | aperto |
| NX-106 | La transizione analisi → pilot (NX-102) va proposta nella STESSA conversazione, non dopo. Scrivere la frase | P2 | Prodotto | `32-...` § 5 | aperto |
| **NX-107** | **Far girare il ciclo Foundation → X → Foundation sulla motion**: la vista generata deve passare da riduzione → interpretazione → validazione → PageData → renderer. **Guard (D-092): niente PageData scritta a mano per la demo.** Se un passaggio è manuale, va marcato come debito del ciclo | P1 | Architettura | D-089 → D-092 | aperto |
| ~~NX-101~~ | **INVIATO 2026-09-17** — nota analitica + allegato narrativo + messaggio, da canale personale. Richiesto feedback in forma relazionale. A. ha risposto che lo darà | — | Esterno | D-057, D-090 | **chiuso** |
| NX-51 | Verifica **payer** nel verticale candidato (non del bisogno: del pagamento) + strutturazione del conflitto di interessi come prerequisito | **P1** | Prodotto | § 2.3, 2.4 | aperto |

---

## Aggiornamento 2026-09-10 (benchmark ToolJet)

Fonte: `../documentation/research/benchmarks/TOOLJET-benchmark.md`.

```text
NX-14  → P0. È l'unico percorso di distribuzione economicamente sostenibile
         per un progetto singolo: l'utente porta il modello, tu paghi solo compute.
NX-11  → CONFERMATO da evidenza esterna: ToolJet usa "generated component and
         datasource catalogs so agents use first-party contracts instead of
         guessing configuration keys". È projection-come-artefatto, già in
         produzione altrove.
NX-09  → CONFERMATO (cataloghi generati, non scritti a mano).
NX-01b → CONFERMATO: PAT con prefisso (tj_pat_), deployment URL, origin API
         separabile. Validato in produzione.
NX-01  → RICALIBRATO: ToolJet non usa licenza offline firmata, usa AGPL + EE
         submodule + cloud. NX-01 resta per il track on-prem/air-gapped.
Q-001  → ha ora un'opzione concreta: schema a tre licenze (vedi Decision Log).
```

**Nessuna nuova voce tocca i simboli vincolati. Restano tutte in zona sicura.**

---

## Aggiornamento 2026-09-10 (persona + authorities + costo)

Fonte: `07-PERSONA-AUTHORITIES-COSTO.md`.

**Cambio di persona dichiarato:** non builder che sposta rettangoli, ma
**decision-maker non tecnico** (manager, responsabile finanziario, broker) che
esplora un dominio guidato da X.

Conseguenze sul backlog:

```text
NX-22  → P0. La persona dichiarata NON usa CLI/MCP/Claude Code.
         Il pivot riporta la riga 2 al centro: servono due tier espliciti.
NX-19  → P0. "Osserva, monitora" è costo per-OROLOGIO, non per-request.
         Regola: Foundation OSSERVA (deterministico, gratis),
                 X INTERPRETA (AI, metered, su evento o domanda).
NX-18  → P0. Graphic Authority senza gate è una linea guida, non un contratto.
NX-20  → chiude AF-003 (Server Session Recovery) e AF-004
         (Client Session Reconciliation) senza infra nuova.
NX-21  → copiare l'INTERFACCIA plugin di ToolJet, non i 90+ connettori.
NX-23  → un CFO/broker lascia tracce locali: va deciso prima, non dopo.
```

**NX-25 è urgente e costa un comando:** se `deepseek-flash` è ritirato, tutte le
config (Roo, Cline, Continue, `.clinerules`, Brain) puntano a un modello inesistente.
È anche la prova dal vivo che NX-04 (rilevamento cambio catalogo provider) non è
teoria.

**NX-24 è il prerequisito di ogni discorso sui costi:** finché non puoi rispondere a
*"quanto costa una generazione di pagina?"*, la discussione è opinione. Va costruito
su `AIRedisLogger`, che esiste già (fan-in 12 nel grafo MCP).

**Nuovo ordine complessivo:**

```text
0. NX-25  bonifica config model ID              ← fatto nei doc, manca negli strumenti
0b.NX-26  provider layer nel server nuovo       ← FINESTRA APERTA ORA (include NX-04, NX-24, NX-05)
1. NX-22  due tier Builder / Decision-maker     ← decide tutto il resto
2. NX-19  Foundation osserva, X interpreta      ← decide la struttura di costo
3. NX-14  nexus-mcp (tier Builder, riga 4)
4. NX-03  gate VALIDATE
5. NX-18  Graphic Authority + gate
6. NX-01b Foundation API tokenizzata
7. NX-11  projection come Build Artifact        ← bloccato da Q-005
8. NX-20  local-first + ping Redis              ← chiude AF-003/AF-004
```

---

## Aggiornamento 2026-09-10 (post-validazione AF-001)

```text
AF-001   → CHIUSO su feature/catalog-registry-authority (D-012)
NX-01b   → SBLOCCATO. AF-001 non era un prerequisito: l'ipotesi è falsificata.
NX-11    → NUOVO P0. È la risoluzione reale di AF-001 (la closure attuale è un
           placeholder con 5 app hardcodate).
NX-12    → NUOVO P1. Verifica comportamento su appId sconosciuto.
NX-13    → NUOVO P1. I 3 endpoint /api/catalog/* hanno già la forma giusta.
```

**Nuovo ordine:**

```text
0. Q-005   applicationType dichiarato o inferito?   ← PRO, una domanda sola
           decide se NX-11 resta in zona sicura o diventa Foundation RFC
1. NX-01b  Contract Registry + /v1/compile + /v1/validate
2. NX-11   projection → Build Artifact
3. NX-03   Gate VALIDATE come endpoint remoto
4. NX-01   Licenza offline (track on-prem)
5. NX-02   Workflow runner che chiama l'API
```

Nota: `NX-05` (enforce server-side) è **risolto per costruzione** da NX-01b — con il
gate remoto il client non può bypassarlo.

---

## NX-01 · Licenza offline firmata · P0

**Problema risolto:** come distribuire senza aprire il kernel e senza regalare
l'intuizione architetturale.

**Modello osservato (Trustable):**
```text
Tutto locale          → GRATIS
Git push              → licenza
Publish su cluster    → licenza + host in allowlist
Verifica              → offline, public key embedded, zero infrastruttura
```

**Spec proposta:**
```text
Algoritmo     Ed25519
Token         nexus_lic_<base64url(payload)>.<signature>
Payload       { subject, issued_at, expires_at, hosts[], tier, features[] }
Verifica      public key compilata nel binario CLI, nessuna chiamata di rete
Expiry        valida per tutto il giorno indicato, invalida dal successivo
Host check    publish verso host non in lista → rifiutato anche con licenza valida
Dev locale    esente da host check, ma richiede licenza valida solo per publish
```

**Matrice free / gated (da decidere):**
```text
FREE     nexus init · dev · build · preview · validate · bundle create
GATED    nexus publish · nexus bundle export · nexus deploy
```

**Aperti:** dove vivono le chiavi private di signing · chi emette le licenze ·
se esiste un tier `community` permanente · come si gestisce la revoca senza
license server (lista di revoca firmata nel bundle CLI?).

---

## NX-02 · Workflow Contract · P0

**Problema risolto:** oggi il loop brainstorm → PRD → prompt MCP → esecuzione è
**manuale** e vive nelle chat. Non è riproducibile, non è versionato, non è condivisibile.

**Principio:** il bundle porta con sé la propria ricetta di generazione.

**Formato proposto** (allineato a Trustable: Markdown con `---`, ma con gate):
```markdown
---
id: add-knowledge-page
version: 1
target: ApplicationBundle
---

## 1. Estrai i token dal contenuto sorgente
<prompt>
---
## 2. Genera la PageData
<prompt>
gate: nexus validate --contract pagedata
---
## 3. Registra la pagina nel bundle
<prompt>
gate: nexus validate --contract bundle
```

**Semantica step (da Trustable, quasi verbatim):**
```text
NOT RUN / RUNNING / RUN / FAILED / SKIPPED
stato persiste attraverso chiusura e ripresa sessione
prompt ri-letto al momento dell'esecuzione
step fallito → termina la run
Stop → selezione resta sullo step fermato → resume da lì
```

**Da aggiungere rispetto a Trustable:** il campo `gate:` — vedi NX-03.

**Vincolo:** `workflow.md` è **contenuto** del bundle, non dipendenza.
Il Runtime non lo osserva. Non tocca l'invariante D-003.

---

## NX-03 · Gate VALIDATE · P0 · **il vero differenziatore**

**Il buco osservato in Trustable:**
> *"A step counts as run once it has **produced output**."*

Prodotto output ≠ output corretto. Nessuna validazione dell'artefatto generato.
Loro stessi avvertono: *"a template that goes wrong at step two will otherwise keep
building on that mistake through step five."*

**Il buco in Instruqt:** ha `check-host`, ma è dominio-chiuso sui lab.

**La risposta Nexus:**
```text
Trustable:  prompt → agente → output                    (nessuna verifica)
Instruqt:   step → check-host → gate                    (verifica, dominio chiuso)
Nexus:      prompt → agente → Bundle → VALIDATE → gate contrattuale
                                     ↓
                             BundleCollector invariato
                                     ↓
                               Runtime invariato
```

**Cosa valida il gate:**
```text
1. PageData conforme allo schema versione N
2. Registry ID coerente (attenzione a F-01: Registry ID ≠ Bundle-derived ID)
3. Template risolto e esistente
4. Policy/visibility dichiarata coerentemente
5. Nessun riferimento al repository nel contratto generato
6. content_sha calcolato → source authority tracciabile
```

**Nota:** la CLI fa già estrazione tokens. Il gate è l'estensione naturale di
quello che esiste già. Non è un componente nuovo da zero.

---

## NX-04 → NX-06 · Brain / X (P1)

**NX-04 — Provider abstraction.** Da Trustable § 3.2:
- validare la forma dell'URL al save, non al primo errore runtime
- se `https://` e key vuota → conferma esplicita (quasi sempre un errore)
- interrogare il catalogo modelli al save; zero modelli = non salvare
- probe minimo `"Reply with exactly: OK"` come gate di **usabilità**, non di qualità
- **rilevare il cambio catalogo del provider** e forzare la riselezione del modello

Si aggancia al PR #1 Brain Contract Extraction già specificato:
`ModelProvider` · `EmbeddingsProvider` (protocollo vuoto) · `HealthProbe` ·
`ToolExecutor` · `ContractCompleter` + `ROUTING` + `MAX_OUTPUT_TOKENS`.

**NX-05 — Enforce server-side.** Da Trustable: la regola `FOR CODING`
*"enforced on the server too, not just in the browser, so it holds however you save."*
Applicare lo stesso principio al `ROUTING`: il client può suggerire, il server decide.

**NX-06 — Concorrenza ottimistica.** Verifica che il contratto remoto non sia cambiato
dal caricamento; se sì, **rifiuta il save** invece di sovrascrivere.
Più: badge `CHANGED` sempre visibile anche senza credenziali (onestà di stato),
token **write-only** mai riverificato, mai nel file di config condiviso.

---

## NX-07 → NX-10 · Narrativa / Legale (P2)

**NX-07 — Tre tier:**
```text
One repository   → local:        nexus dev, zero infrastruttura
One team         → hosted:       Vercel/Fly, bundle pubblicati
One organization → sovereign:    engine firmato, host allowlist
```

**NX-08 — Doc pubblica che difende le decisioni.** Formato osservato:
*"That is deliberate: ..."* · *"on purpose"* · *"because you are choosing, not
aborting"*. Un clone può copiare le features, **non può copiare il perché** — e senza
il perché reintroduce i bug già risolti. È la stessa postura del
`NEXUS-recap-ufficiale.pdf` (Validato / Debito / Roadmap), solo pubblicata.

**NX-09 — Indice pubblicato**, non query live: *"so the list is identical on every
installation."* Determinismo dell'onboarding, nessuna dipendenza da servizi terzi
a runtime.

**NX-10 — Nome pubblico + collisioni.** `OpenFav` / `Open Nexus` / `Nexus Lab`.
Check UIBM/EUIPO prima di investire.

---

## Sequenza consigliata

**Revisione 2026-09-10** dopo P-005 (Foundation API tokenizzata):

```text
1. NX-01b  Contract Registry + /v1/compile + /v1/validate
           → il confine Foundation/Execution diventa un'API
2. NX-03   Gate VALIDATE come endpoint remoto
           → il differenziatore; con il gate remoto, NX-05 è risolto per costruzione
3. NX-01   Licenza offline firmata
           → secondo trasporto (on-prem / air-gapped / sovereign)
4. NX-02   Workflow runner che chiama l'API, non esegue in locale
5. NX-04/05/06 → Brain, in parallelo, nessun blocco
6. NX-07/08/09/10 → quando c'è qualcosa da raccontare
```

Motivo per cui NX-01b viene prima di tutto: **finché non decidi come esce il
prodotto, ogni feature di X rischia di essere ripensata in funzione della
distribuzione.** E NX-01b è quello che trasforma il boundary logico in confine
commerciale.

**Dipendenza critica da verificare subito:** `AF-001`. Se `Runtime → BundleCollector`
è davvero nel request path, lo split remoto/locale non è pulito e AF-001 diventa
prerequisito di NX-01b, non solo gate per 0.6.5.

Prompt di validazione pronto in `04-FOUNDATION-API.md` § 9.

---

*Ultimo aggiornamento: 2026-09-10*
