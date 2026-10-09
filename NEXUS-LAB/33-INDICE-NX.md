# Indice NX — tutte le voci

**Generato:** 2026-09-17 · **Voci:** 108 · NX-01 → NX-107

Generato programmaticamente da `02-BACKLOG-NX.md`. Se i due divergono, vale il backlog.

**Deflazione applicata** — regola: *un P0 deve bloccare almeno un'altra voce*. Prima 26 P0, dopo 3.

---

## Cruscotto

```text
aperte   102
chiuse   6
totale   108
```

**Per priorità (aperte)**

```text
P1         62
P2         35
5 min      2
P0         2
P3         1
```

**Per area (aperte)**

```text
PRODOTTO     37
X            23
FOUNDATION   15
DISTRIB      13
ALTRO        8
BRAIN        5
EXECUTION    1
```

---

## P0 — le tre che bloccano altro

| NX | Titolo | Perché è P0 | Stato |
|---|---|---|---|
| **NX-86** | Prerequisito non negoziabile. Bonifica eseguita (NX-50 parziale). Resta la verifica con un legale su incompatibilità e autorizzazi | blocca ogni passo commerciale e la questione co-founder | parziale — resta il legale |
| **NX-91** | IN VIAGGIO. La domanda è § 7.1 della nota inviata: "quando dicevi 'siamo noi', a chi ti riferivi?". Non più da fare: da aspettare | in viaggio dentro la nota inviata — determina quale dei tre prodotti esiste | in attesa di A. |
| **NX-57** | P0 ↑ — Test di ripetibilità: analisi su oggetto NUOVO usando SOLO il metodo scritto, senza intervento. Non è più un test di qualit | decide se la motion NX-104 è prodotto o consulenza, e sblocca l'ontologia del Brain | aperto |

## In attesa — non richiedono azione

```text
NX-90   orbita attiva: attesa feedback di A. · cadenza 4-6 settimane
NX-91   la domanda è § 7.1 della nota inviata
NX-102  pilot in due stadi: si propone solo se il feedback apre
NX-103  formalizzazione dati: si fa solo se si arriva a un pilot
```

## Da fare e basta — cinque minuti

```text
NX-25   config model ID → deepseek-flash
NX-50   cestini del tenant (regressione del 2026-09-17 spiegata in D-093)
```


---

## FOUNDATION — 17 voci

| NX | Pri | Titolo | Stato |
|---|---|---|---|
| NX-11 | P1 | RIFORMULATO (D-028): materializzazione manuale → generata dal build. Q-005 risolta: applicationType è dichiarato in src/… | aperto |
| NX-34 | P1 | Design Enforcement con ruleset dichiarativo consumato da lint/CI e dal gate VALIDATE. RICALIBRATO da D-034: per X è voca… | fatto per il design (script), manca il lato X |
| NX-35 | P2 | Versione del ruleset referenziata nel bundle (come content_sha per i contenuti) | aperto |
| NX-37 | P2 | Elenco dei "bordi" del refactor authority + verifica fonte vs copia | aperto — deperibile |
| NX-38 | P1 | P0 (D-038) — Rimuovere as any da src/config/applications/*: DiscoveryMetadata non è enforced nel punto di scrittura | aperto — finestra 0.7.0.2b |
| NX-39 | P1 | P0 (D-038) — notFound accetta '/' ma il contratto dichiara *registryId*: stringere il tipo o normalizzare in factory.ts | aperto — finestra 0.7.0.2b |
| NX-40 | P2 | Documentare il criterio di ripartizione Definition (src/config/applications) vs Bundle (src/applications/*/package.ts) | aperto |
| NX-41 | P2 | Collisione di vocabolario: type:'user' (visibilità) vs audience:'user' (persona) | aperto |
| NX-43 | P1 | Vocabolario status come dato dichiarativo: runtime degrada a muted, build rifiuta. Per X è vocabulary-check (D-034) | aperto |
| ~~NX-44~~ | — | ~~RISOLTO: walk() con readdirSync su tutto src/, eccezioni che sottraggono → scope derivato, fails CLOSED. Residuo congela…~~ | chiuso (trigger: nuova primitiva o chiusura 0.7. |
| NX-45 | P1 | Verificare se PageData ammette escape hatch visuali (className, style, HTML libero). Determina la forma del gate VALIDAT… | aperto |
| NX-46 | P1 | Aggiungere expires al DATO EXCEPTIONS (oggi sta solo nel doc) e far fallire --ci a scadenza superata | aperto |
| NX-47 | P2 | legacy-frozen:pages include src/pages/build/ con match a prefisso: il punto d'ingresso di EXECUTION è esente, e ogni fil… | aperto |
| NX-48 | P2 | Verificare il meccanismo per-file del gate --ci: con 554 errori --ci esce 1, quindi il "per-file once migrated" sta altr… | aperto |
| NX-53 | P2 | check-proposal.mjs — generalizzazione di check-style-authority.mjs applicata ai proposal record. Classe 0, deterministic… | non prima di un ciclo di sonda reale |
| NX-58 | P2 | Schema dell'analysis/proposal record come FILE versionato, con campi observed / inferred / recommended e obbligo di font… | aperto |
| ~~NX-87~~ | — | ~~Documento ricevuto e analizzato in 29-PROMETEO-ANALISI.md~~ | chiuso |

---

## X — 23 voci

| NX | Pri | Titolo | Stato |
|---|---|---|---|
| NX-02 | P2 | Workflow Contract: workflow.md dentro ApplicationBundle | aperto |
| NX-03 | P2 | Gate VALIDATE fra generazione e BundleCollector | aperto |
| NX-06 | P1 | Concorrenza ottimistica sul save remoto dei contratti | aperto |
| NX-12 | P1 | Fallback per appId assente nella projection | aperto |
| NX-17 | P1 | Cataloghi di template/renderer generati dal BundleCollector ed esposti via MCP | aperto |
| NX-19 | P1 | Nessun LLM nell'osservazione continua: trigger deterministici + batch con tetto | aperto |
| NX-21 | P1 | Interfaccia plugin per connettori (interfaccia, non libreria) | aperto |
| NX-27 | P1 | Connector Layer: interfaccia unica Fetched; libreria di scraping esistente → HttpHtmlConnector; change detection via con… | aperto |
| NX-28 | P1 | JsonApiConnector — per la persona broker/CFO è il connettore a più alto valore | aperto |
| NX-29 | P2 | PdfConnector — filing, bilanci, report | aperto |
| NX-31 | P1 | RIVALUTATO (20-... § 9): era la forma iniziale della capacità di analisi di mercato, non una tassonomia auto-riferita. O… | riaperto |
| NX-32 | P1 | Regola "ogni operazione di X lascia un residuo" come criterio di accettazione nei PRD di X | aperto |
| NX-36 | P2 | Nel censimento primitive, classificare ognuna come OPERA o CAPISCE | probabilmente già fatto (ADR-0012) — da conferma |
| NX-49 | P1 | Prima applicazione SONDA (D-041: la sonda non è il verticale). AGGIORNATO da 24-... § 8: se è job-seeker, va MIRATA al p… | in corso altrove |
| NX-56 | P1 | Portare le 4 analisi esistenti in PageData e pubblicarle su open-nexus/library·topics·generated-knowledge. Un artefatto,… | aperto — prototipo già scritto |
| NX-59 | P2 | Tokenizzazione locale prima del confine LLM — incapsulare Presidio, mappa in IndexedDB+WebCrypto (NON localStorage). Pre… | aperto — bloccato da NX-30 |
| NX-76 | P1 | A (pagina personale) riclassificata: non è istanza, è infrastruttura di pubblicazione. Prerequisito di NX-56 | aperto |
| NX-88 | P2 | BRAIN-006 (aggiornare le viste dipendenti da una norma modificata) richiede un grafo di dipendenza fra contenuti: unica … | aperto |
| NX-89 | P2 | L'artefatto-dono per A. (D-057): una knowledge experience su UNA materia delimitata, con fonti, date, versioning. È il p… | aperto |
| NX-92 | P1 | Layer forense versionato: ricostruire cosa era vero in una data, secondo la norma allora vigente, con catena documentale… | bloccato da NX-91 |
| NX-98 | P1 | Ontologia normativa come asset: norma ↔ obbligo ↔ ruolo ↔ modulo ↔ caso cliente ↔ versione ↔ CTA. L'ingestione è commodi… | aperto |
| NX-99 | P1 | Grafo di dipendenza norma → contenuti, versionato nel tempo. È NX-88/BRAIN-006. Una capacità, due viste, due payer: reda… | aperto |
| NX-100 | P2 | Connettore WordPress: /wp-json/wp/v2/{pages,posts,media} + sitemap. Lavoro minimo, il namespace mcp esiste già | aperto — quasi gratuito |

---

## BRAIN — 5 voci

| NX | Pri | Titolo | Stato |
|---|---|---|---|
| NX-04 | P1 | Provider abstraction Brain: validazione URL, catalogo, probe OK | aperto |
| NX-05 | P1 | Regole enforced server-side, non solo client | aperto |
| NX-24 | P1 | Strumentazione costo per chiamata LLM (input/cached/output/reasoning + classe 0–4) su AIRedisLogger esistente | aperto |
| NX-25 | 5 min | Model ID DeepSeek: CONFERMATO ritirato deepseek-v4-flash → deepseek-flash. Doc del workspace bonificati; mancano le conf… | parziale |
| NX-26 | P1 | Provider Layer per il server nuovo (base/catalog/routing/budget/reduce) — assorbe NX-04, NX-05, NX-24 | aperto — finestra refactor |

---

## PRODOTTO — 38 voci

| NX | Pri | Titolo | Stato |
|---|---|---|---|
| NX-22 | P1 | RICALENDRIZZATO (D-047): i due tier non sono "Builder / Decision-maker" ma "chi costruisce" / CHI DEVE RENDERE CONTO (= … | aperto |
| NX-30 | P1 | Scelta del verticale + falsificazione di "il mercato premia il contenuto, non il meccanismo" | aperto — non richiede codice |
| NX-33 | P2 | Profilo di competenza per NX-30 (dominio, non architettura) | bloccato da NX-31 |
| NX-42 | P1 | audience non contiene il decision-maker — blocca 0.7.0.3 Presentation Authority | aperto |
| NX-51 | P1 | Verifica payer nel verticale candidato (non del bisogno: del pagamento) + strutturazione del conflitto di interessi come… | aperto |
| NX-52 | P1 | Colmare le 4 lacune del METODO Sonda: L-1 criterio di arresto · L-2 seconda sonda nominata · L-3 time box · L-4 pubblico… | aperto |
| NX-54 | P1 | Regola staleness dell'evidenza esterna: un campo di evidenza pending oltre N giorni → insufficient-evidence. Vale per il… | aperto |
| NX-55 | P2 | Method Agent come prodotto RICLASSIFICATO da 20-... § 4: il mercato non è agent-governance ma architecture & market inte… | riclassificato |
| NX-57 | P0 | P0 ↑ — Test di ripetibilità: analisi su oggetto NUOVO usando SOLO il metodo scritto, senza intervento. Non è più un test… | aperto |
| NX-61 | P1 | Scansione di mercato per CAPACITÀ (non per categoria app): assi prioritari doc-20 · C-01 · M-06 · C-07, minimo 5 inserzi… | aperto — corregge la scansione già fatta |
| NX-62 | P2 | Estensione a piano 2 (Product Hunt, Indie Hackers) — il piano 1 discrimina (§ 8), sbloccato ma dopo NX-63 | aperto |
| NX-63 | P1 | Portare la sottocapacità "analyst/developer utility" (proposizione B) a n≥5. Unica con multiplo alto E vicinanza al gate… | aperto |
| NX-64 | P1 | Filtro di sostituibilità: per ogni inserzione e ogni sonda, dichiarare se l'80% del risultato è ottenibile gratis da un … | aperto |
| NX-65 | P2 | Banda di valore di riferimento: $11k–$50k ARR · 200–300 sub B2B o ~1.000 prosumer · 2,7–3,0× · asset $30k–$150k | aperto |
| NX-66 | P1 | SERIE STORICA delle inserzioni già raccolte: campi esito · prezzo_finale · delta. Riletture dic-2026 / mar-2027 / giu-20… | aperto — deperibile |
| NX-67 | P1 | SCANSIONE PRODUCT MARKETPLACE (Envato · Gumroad · boilerplate · Astro Themes · Notion templates · MCP a pagamento · AppS… | aperto |
| NX-69 | P1 | Governance come TIER DI PREZZO: read-only (propone) vs read-write (modifica, con gate + approvazione + audit trail). GoM… | aperto |
| NX-71 | P2 | Verificare il pavimento open source per ogni capacità orizzontale candidata. Regola: se esiste un pavimento mantenuto, l… | aperto |
| NX-72 | P2 | Il premio di verticale 7–70× è evidenza quantitativa per NX-30 | aperto |
| NX-73 | P1 | LA FRASE — verbo + oggetto + beneficiario. Candidata: *"Fa le ricerche al posto tuo, e si ricorda dove ha trovato ogni c… | aperto — costo zero |
| NX-74 | P1 | Regola scritta: l'AI entra in scena una volta sola, nell'interpretazione. Ogni altro punto di ingresso va motivato per i… | aperto |
| NX-75 | P1 | Matrice di scoring delle istanze candidate contro i criteri K1–K8 già stabiliti. Nomenclatura: X → Ambiente → Istanza | fatto, da ratificare |
| NX-77 | P2 | Verificare il pavimento open source per E (competitive intelligence con evidenza). Se esiste, la raccomandazione si inve… | aperto |
| NX-78 | P1 | Test del frame su E: dopo la pubblicazione, contare le richieste da persone che non sono l'utente. Zero richieste → E er… | aperto |
| NX-79 | P2 | COLLOQUIO CON Y-1 (il volontario). Non per vendere: estrarre la lista ESATTA delle domande tecniche a cui non sapeva ris… | aperto — costo zero |
| NX-80 | P2 | Verificare la convergenza Y-1/D: stessa frizione ("non voglio rispondere a domande tecniche"), payer opposti. Se conferm… | aperto |
| NX-83 | P1 | Frasi candidate per nexus-builder (NX-73 applicato): da testare su 5 persone con richiamo il giorno dopo | aperto — costo zero |
| NX-84 | P1 | K4 VERIFICATO: incumbent forte (Informatica EDP, 3.000+ aziende, €125/utente/mese di listino). Opportunità A ed E già co… | parziale |
| NX-85 | P1 | RICALENDRIZZATO (D-056/057): A. sta in ORBITA, non in pipeline. Non le 13 domande: un piccolo artefatto utile, già fatto… | aperto |
| NX-90 | P1 | ATTIVO ORA. Condizioni di conversione dell'orbita (D-058): chiede due volte la stessa cosa · presenta qualcuno con budge… | in corso — attesa risposta |
| NX-91 | P0 | LA DOMANDA: "quando dici 'siamo noi', intendi chi fa il software, chi lo usa, o chi assiste chi lo usa?" Una riga. Deter… | aperto — costo zero |
| NX-93 | P2 | Verificare se Prometeo gestisce già la vista multi-azienda per consulenti/associazioni (Opportunità C). Se sì, anche C è… | aperto |
| ~~NX-96~~ | — | ~~FATTO: WordPress 7.1 + Elementor SSR, non statico. 153 pagine / 206 post / 855 media, zero custom post type verticali. N…~~ | chiuso |
| NX-97 | P1 | Condizione di conversione scritta e datata per il cavallo di Troia: entro X mesi l'accesso deve aver prodotto Y. Senza, … | aperto |
| NX-102 | P1 | Pilot in DUE STADI (sintesi delle due simulazioni). Stadio 1 — *caso*: un caso reale già chiuso che è costato tempo, ric… | aperto — è il secondo incontro |
| NX-104 | P1 | Formalizzare la motion Y-idea-site-knowledge in sei passi come procedura scritta, eseguibile da un agente. È NX-57 appli… | aperto |
| NX-105 | P1 | Definire la PERSONA dietro la condizione. "Conoscenza accumulata non esprimibile" è il bisogno; chi lo sente E ha voce i… | aperto |
| NX-106 | P2 | La transizione analisi → pilot (NX-102) va proposta nella STESSA conversazione, non dopo. Scrivere la frase | aperto |

---

## DISTRIB — 14 voci

| NX | Pri | Titolo | Stato |
|---|---|---|---|
| NX-01 | P2 | Spec licenza offline firmata per Nexus CLI (track on-prem) | aperto |
| NX-01b | P2 | Foundation API tokenizzata — split PRODUCE remoto / EXECUTION locale (track hosted) | aperto |
| NX-09 | P2 | Indice pubblicato per starter/bundle, non query live | aperto |
| NX-13 | P1 | Catalog API → superficie Foundation API (da /api/catalog/* esistenti) | aperto |
| NX-14 | P2 | nexus-mcp come repo separato, licenza permissiva, bundle precompilato, plugin Claude Code/Codex/Cursor | aperto |
| NX-15 | P1 | Layout a sensibilità: repo pubblico + submodule EE + symlink + sync script idempotente (--check in pre-commit) | aperto |
| NX-23 | P1 | Policy dati locali sensibili per persona finanziaria (TTL, cifratura, consenso) | aperto |
| NX-50 | 5 min | Bonifica tenant: file CANCELLATI (2026-09-16). Residuo da verificare: cestino di primo e secondo livello, cronologia ver… | parziale |
| NX-60 | P3 | Verifica con DPO della formulazione del claim privacy prima che compaia in qualunque documento pubblico o di gara | aperto |
| NX-68 | P2 | Registrare la piattaforma di vendita come variabile di margine: Envato 30–62,5% vs vendita diretta ~2,9%. Scarto 3–6× su… | aperto |
| NX-81 | P1 | Gerarchia dei nomi: sei nomi in circolo (OpenFav · Open Nexus · Nexus Lab · nexus-builder · nexus-mcp · opnx) e nessuno … | aperto |
| NX-86 | P0 | Prerequisito non negoziabile. Bonifica eseguita (NX-50 parziale). Resta la verifica con un legale su incompatibilità e a… | parziale — resta il legale |
| NX-101 | P1 | NOTA-PER-A.md scritto. Prima di inviarlo: (a) NX-86 bonifica tenant e verifica legale, (b) rileggere e togliere qualunqu… | pronto, bloccato da NX-86 |
| NX-103 | P1 | Formalizzare la protezione dati PRIMA di qualunque prova: chi tratta cosa · per quanto · base giuridica · traccia. § 4.5… | aperto |

---

## EXECUTION — 1 voci

| NX | Pri | Titolo | Stato |
|---|---|---|---|
| NX-20 | P1 | Local-first con ping Redis → chiude AF-003 e AF-004 | aperto |

---

## ALTRO — 10 voci

| NX | Pri | Titolo | Stato |
|---|---|---|---|
| NX-07 | P2 | Narrativa tre tier + pagina pubblica | aperto |
| NX-08 | P2 | Doc pubblica che difende le decisioni | aperto |
| NX-10 | P1 | Verifica collisioni marchio / decisione nome pubblico — assorbito da NX-81 | aperto |
| NX-16 | P2 | Skill di processo nel repo (commit, create-pr, merge) per strumentalizzare il loop | aperto |
| ~~NX-18~~ | — | ~~Graphic Authority CHIUSO COME DUPLICATO — coperto da Primitive / Design / Presentation Authority già esistenti. Resta va…~~ | chiuso |
| NX-70 | P1 | Onboarding / curva di apprendimento — l'unica frizione letale per la persona dichiarata (manager/CFO/broker) senza rispo… | aperto — non era a backlog |
| NX-82 | P1 | Principio "mostra, non chiede": ogni domanda posta all'utente è un default mancante in un'authority. Da scrivere come vi… | aperto |
| NX-94 | P1 | Decidere la modalità con A.: orbita (D-056) o co-founder (D-063). Sono incompatibili nello stesso periodo. Bloccato da N… | bloccato da NX-86 |
| NX-95 | P1 | Le tre domande ad A. (§ sotto). La prima è su cosa intendeva, la seconda è su di lui, la terza è sul dolore di Prometeo | aperto — costo zero |
| NX-107 | P1 | Far girare il ciclo Foundation → X → Foundation sulla motion: la vista generata deve passare da riduzione → interpretazi… | aperto |

---

## Chiuse, risolte, superate

| NX | Esito |
|---|---|
| ~~NX-18~~ | chiuso |
| ~~NX-44~~ | chiuso (trigger: nuova primitiva o chiusura 0.7.0.2) |
| ~~NX-87~~ | chiuso |
| ~~NX-94~~ | chiuso |
| ~~NX-96~~ | chiuso |
| ~~NX-101~~ | chiuso |

---

## Risoluzione dei riferimenti

```text
NX-*   questo file                                    (tutte le 108 voci)
D-*    01-DECISION-LOG.md                             (D-001 → D-093)
Q-*    01-DECISION-LOG.md, sezione "Domande aperte"
C-*    21-CAPACITA-OPENNEXUS.md                       (C-01 → C-12)
AF-*   recap ufficiale PDF + 05-AF001-VERDETTO.md
K1-K8  27-SCORING-ISTANZE.md
M-*    23-MOAT.md                                     (M-01 → M-06)
```

Per le citazioni dentro `brain/knowledge/`: `34-RIFERIMENTI.md`.
