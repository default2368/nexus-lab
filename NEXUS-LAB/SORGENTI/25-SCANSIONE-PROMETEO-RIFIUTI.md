# Scansione PrometeoRifiuti

**Data:** 2026-09-15
**Fonte principale:** https://www.prometeorifiuti.com/
**Tipo:** scansione di prodotto verticale, bisogni, opportunità, network e connessione
con Open Nexus
**Provenienza:** documento sorgente prodotto in altra sessione, salvato nel workspace
il 2026-09-16 perché esisteva solo nella conversazione. È il documento referenziato
come `25-SCANSIONE-PROMETEO-RIFIUTI.md` da `uploads/26-NEXUS-PROMETEO-BRAIN-NETWORK.txt`.

## 1. Identità del prodotto

PrometeoRifiuti è un gestionale verticale per la gestione amministrativa e operativa
dei rifiuti:

- registri di carico e scarico
- formulari e XFIR
- MUD
- RENTRI
- autorizzazioni e scadenze
- giacenze
- contratti e preventivi
- pianificazione dei servizi
- DDT e rapportini
- fatturazione
- magazzino MPS/EOW
- analisi e dashboard
- integrazione con contabilità
- gestione di produttori, trasportatori, destinatari, intermediari, consulenti e
  associazioni

Il sito dichiara oltre 2.000 installazioni e oltre 3.000 aziende che hanno scelto
PrometeoRifiuti. Questi numeri sono dichiarazioni del fornitore, non dati verificati
indipendentemente.

Fonti: `prometeorifiuti.com/` · `/cosa-fa-prometeo/` ·
`capterra.com/p/189319/Prometeo-Rifiuti/`

Capterra descrive il prodotto come rivolto a produttori, trasportatori, destinatari e
intermediari e riporta una partenza di 125 euro per utente al mese; la pagina non
mostra recensioni utenti, quindi il prezzo va trattato come dato di catalogo, non
come verifica commerciale.

## 2. Bisogni osservabili

### 2.1 Conformità senza errori

```text
movimento di rifiuto → registro → formulario → RENTRI → MUD → conservazione/prova
```

Il costo dell'errore può comprendere: sanzioni; blocchi operativi; contestazioni;
perdita di tracciabilità; tempo amministrativo; rischio per l'amministratore o il
responsabile ambientale.

Prometeo comunica il valore attraverso alert su autorizzazioni scadute, limiti di
giacenza e incongruenze, oltre alla compilazione dei documenti e al dialogo con RENTRI.

### 2.2 Eliminazione della doppia immissione

Le testimonianze pubblicate citano: database anagrafici duplicati; inserimenti
ripetuti; passaggi complessi verso la contabilità; interfacce rigide; dati inviati
lentamente a impianti o clienti.

Un caso di spurghi descriveva duplicazione dei dati, pianificazione inefficiente e
trasferimenti contabili imprecisi; con Prometeo viene gestita la pianificazione delle
attività, la manutenzione e la reportistica.

Fonte: `prometeorifiuti.com/spurghisti/rse/`

### 2.3 Coordinamento operativo

Il problema non è solo il registro. È coordinare: richieste del cliente; ritiro;
autista; mezzo; rifiuto; EER; trasportatore; impianto di destinazione; documento;
conferma; fatturazione.

Per i trasportatori il sito evidenzia modelli di formulari e pianificazione di ritiri
periodici o su date specifiche. Fonte: `prometeorifiuti.com/trasportatori/`

### 2.4 Visibilità sul flusso

Le testimonianze indicano usi per: controllare rifiuti in deposito temporaneo;
monitorare scadenze; ridurre errori di compilazione; analizzare flussi e costi di
smaltimento; individuare opportunità di recupero e circolarità.

Fonti: `/produttori/portovesme/` · `/produttori/bio-energia-guarcino/`

## 3. Il network reale

```text
produttore → trasportatore → destinatario / impianto
           → recupero / smaltimento / materia prima secondaria

intermediario e consulente attraversano più nodi
associazione coordina più produttori
```

**Attori:** produttori iniziali; trasportatori; destinatari e impianti; intermediari
senza detenzione; spurghisti; imprese di bonifica; consulenti ambientali; associazioni
di categoria; amministrazione e autorità; uffici contabili; autisti e operatori sul
campo.

**Network funzionale** — non è necessariamente un social network. È una rete di
responsabilità, documenti e passaggi:

```text
chi ha prodotto cosa · chi lo ha preso · con quale autorizzazione
con quale documento · verso quale impianto · in quale quantità · con quale esito
```

Questa struttura è molto vicina a una knowledge graph verificabile.

## 4. Connessione con Open Nexus

Prometeo sembra già avere una Foundation verticale: dati, registri, moduli, workflow,
documenti e vincoli regolatori.

Open Nexus non dovrebbe sostituirlo né ricostruire un gestionale rifiuti generico.
La connessione più plausibile è un **semantic/evidence layer sopra un sistema
operativo già esistente**.

```text
Prometeo    → sistema transazionale e procedurale
Open Nexus  → modello semantico, evidenze, relazioni, viste, query e decisioni governate
```

### 4.1 Source Authority

Fonti possibili: registrazioni di carico e scarico; formulari; documenti RENTRI;
autorizzazioni; contratti; DDT; analisi chimiche; dati di impianto; dati contabili;
documenti caricati; comunicazioni email autorizzate.

Ogni risposta dovrebbe poter risalire a:

```text
affermazione → evento / documento → fonte → data → versione → stato di validazione
```

### 4.2 PageData / knowledge experience

Le stesse informazioni possono produrre viste diverse: dashboard del responsabile
ambientale; vista di un trasportatore; scadenziario autorizzazioni; timeline di un
rifiuto; dossier per un audit; report MUD assistito; vista economica dei costi di
smaltimento; report di circolarità; portale per un'associazione; assistente per il
consulente.

```text
conoscenza strutturata → viste diverse → esperienza specifica per ruolo
```

### 4.3 Determinismo e governance

L'agente non dovrebbe decidere liberamente la classificazione o la conformità.
Dovrebbe invece: leggere dati autorizzati; applicare regole versionate; evidenziare
anomalie; segnalare dati mancanti; distinguere fatto da inferenza; proporre un'azione;
chiedere conferma umana; lasciare traccia della decisione.

```text
Il movimento X non può essere considerato completo perché:
- manca la conferma del destinatario
- l'autorizzazione dell'impianto risulta scaduta
- il peso effettivo non è presente
- la fonte utilizzata è una bozza
```

## 5. Opportunità

### A — Assistente di controllo documentale

Domande naturali su dati reali, con fonte: quali formulari sono incompleti? quali
autorizzazioni scadono nei prossimi 30 giorni? quali rifiuti sono prossimi al limite
di giacenza? quali movimenti non hanno corrispondenza? quali dati MUD sembrano
incoerenti? quali clienti hanno documenti mancanti?

Prima opportunità più coerente: basso rischio operativo se l'assistente è read-only e
produce evidenze.

### B — Dossier di audit

```text
azienda / impianto
├── soggetti coinvolti   ├── autorizzazioni     ├── movimenti
├── documenti            ├── eccezioni          ├── scadenze
├── fonti                ├── azioni correttive  └── cronologia
```

Il valore non è solo il report, ma il rapporto fra ogni conclusione e la fonte
originaria.

### C — Network per consulenti e associazioni

Prometeo ha già un caso d'uso in cui un'associazione o un consulente assiste più
aziende. Un layer Open Nexus potrebbe offrire: vista multi-azienda; knowledge base
normativa; domande e controlli riutilizzabili; alert centralizzati; report per
cliente; separazione rigorosa dei tenant; procedure standardizzate.

### D — Analisi di circolarità e costi

Percorsi alternativi di recupero; confronto tra impianti; trend dei costi; rifiuti
ricorrenti problematici; indicatori di recupero; scenari e spiegazioni.

Area più decisionale e che richiede maggiore cautela: una raccomandazione non deve
essere presentata come conformità o autorizzazione.

### E — Knowledge layer per RENTRI

Il cambiamento normativo genera bisogno continuo di: interpretazione; aggiornamento;
formazione; gestione delle eccezioni; supporto operativo.

Prometeo già produce webinar e documentazione su RENTRI. Open Nexus potrebbe
organizzare fonti normative, procedure, casi e istruzioni in esperienze interrogabili
e citabili.

## 6. Network opportunity

```text
azienda produttrice  → autorizza una vista limitata
trasportatore        → conferma il passaggio operativo
impianto             → conferma ricezione / esito
consulente           → vede eccezioni e documentazione
associazione         → gestisce una federazione di aziende
```

**Regola fondamentale:** il network non implica che tutti vedano tutto. Ogni relazione
dovrebbe avere: proprietario del dato; ruolo del soggetto; scopo dell'accesso; durata;
documenti visibili; azioni autorizzate; log degli accessi.

Caso forte per contratti e ApplicationContext.

## 7. Limiti

**7.1 Responsabilità normativa** — un errore su classificazione, documento o
autorizzazione può avere conseguenze legali e operative. Open Nexus non deve
presentarsi come consulente ambientale automatico.

**7.2 Qualità dei dati** — incompleti; duplicati; inseriti manualmente; incoerenti tra
aziende; basati su documenti in bozza; aggiornati con ritardo; soggetti a correzioni
normative.

**7.3 Complessità del dominio** — EER/CER; rifiuti pericolosi e non; ADR; impianti;
recupero; smaltimento; End of Waste; RENTRI; MUD; autorizzazioni; ruoli societari
diversi. Non è verticalizzabile con un semplice chatbot sopra un database.

**7.4 Integrazione con Prometeo** — dal sito si osservano integrazioni con RENTRI e
contabilità in casi cliente, ma **non è stata verificata un'API pubblica generale di
Prometeo**. Non va assunto che l'integrazione sia tecnicamente o commercialmente
disponibile.

**7.5 Potere dell'incumbent** — Prometeo dichiara migliaia di installazioni e possiede
già: dominio; dati; workflow; conoscenza regolatoria; canale clienti; supporto.
Open Nexus non dovrebbe entrare come concorrente frontale senza un vantaggio molto
specifico.

**7.6 Rischio di trasformare il network in un problema** — privacy; segreti
commerciali; responsabilità per dati errati; controllo degli accessi; consenso;
interoperabilità; gestione dei conflitti. Il network è un'opportunità solo dopo aver
dimostrato valore in un singolo ruolo.

## 8. Implementazioni possibili

**Percorso 1 — Overlay read-only** (il più prudente)

```text
export / CSV / PDF / dati autorizzati → Open Nexus → normalizzazione
→ query con evidenze → dashboard / dossier / alert
```

Vantaggi: nessuna modifica al sistema transazionale; rischio operativo contenuto;
dimostrazione rapida del valore; test del layer semantico.

**Percorso 2 — Assistente integrato per Prometeo.** Richiede accordo con Informatica
EDP e accesso ai dati o a un'integrazione supportata.

**Percorso 3 — Knowledge layer per consulenti.** Target: consulenti ambientali;
associazioni di categoria; studi che gestiscono più aziende. Non sostituisce Prometeo:
organizza documenti, norme, procedure e controlli sopra più clienti con isolamento
rigoroso.

**Percorso 4 — Application bundle verticale**

```text
WasteComplianceExperience
├── soggetti  ├── impianti   ├── autorizzazioni  ├── movimenti
├── documenti ├── scadenze   ├── controlli       ├── evidenze
└── viste per ruolo
```

**Percorso 5 — Network federato.** Solo in fase successiva.

## 9. MVP consigliato — Waste Evidence Assistant

**Input:** export CSV o PDF; autorizzazioni; formulari; registro; elenco scadenze;
eventuali contratti.

**Output:** elenco anomalie; scadenziario; movimenti incompleti; dashboard flussi;
dossier con fonti; domande interrogabili; report esportabile.

**Regole:** read-only; nessun invio automatico a RENTRI; nessuna decisione normativa
automatica; ogni risposta con fonte; distinzione tra dato osservato, inferenza e
suggerimento; conferma umana per ogni azione.

## 10. Fit con Open Nexus

| Capacità Open Nexus | Applicazione nel dominio |
|---|---|
| Knowledge model | soggetti, rifiuti, movimenti, impianti, documenti |
| Source Authority | formulari, registri, autorizzazioni, norme |
| PageData | dashboard, dossier, timeline, scadenziario |
| Normalizzazione | dati provenienti da documenti e sistemi diversi |
| Deterministic gate | controllo prima di pubblicare o inviare |
| Workflow | raccolta → verifica → approvazione → report |
| ApplicationContext | produttore, trasportatore, consulente, impianto |
| Versioning | regole, documenti, autorizzazioni, norme |
| MCP | query e controlli da agenti autorizzati |
| Evidence citation | fonte per ogni anomalia o conclusione |

## 11. Valutazione

| Dimensione | Valutazione |
|---|---|
| Bisogno reale | 🟢 forte |
| Ricorrenza | 🟢 alta |
| Costo dell'errore | 🟢 alto |
| Coerenza con Open Nexus | 🟢 molto alta |
| Disponibilità di dati | 🟢 potenzialmente alta |
| Accesso ai dati | 🔴 da verificare |
| Responsabilità | 🔴 alta |
| Complessità del dominio | 🔴 alta |
| Possibile payer | 🟢 software provider, consulenti, associazioni, aziende |
| Entry point prudente | 🟢 read-only evidence layer |
| Network | 🟡 potente ma da rimandare |

## 12. Distinzione dei bisogni

La prima scansione aveva mescolato due soggetti diversi.

**A. Utenti del software PrometeoRifiuti** — produttori, trasportatori, destinatari,
intermediari, consulenti e associazioni. Bisogni documentati nelle sezioni precedenti.

**B. Gestori del sito e del sistema di comunicazione Prometeo** — il team che deve
spiegare, aggiornare, vendere e supportare il prodotto attraverso il sito e i suoi
contenuti. Bisogni **non dichiarati direttamente**: sono ipotesi osservabili
dall'architettura pubblica del sito, da verificare con una conversazione.

## 13. Bisogni ipotizzati dei gestori del sito

**13.1 Tenere aggiornata la conoscenza normativa**

```text
norma / decreto / istruzione → interpretazione operativa
→ articolo / webinar / slide / procedura → aggiornamento coerente delle pagine collegate
```

**13.2 Riutilizzare lo stesso contenuto in più formati** — pagina prodotto; pagina per
ruolo; caso cliente; articolo; webinar; PDF; aggiornamento versione; demo; FAQ.
Lo stesso concetto può essere riscritto più volte con rischio di incoerenze.

**13.3 Organizzare casi cliente e prova sociale**

> Come trasformare molti casi cliente in percorsi pertinenti per un visitatore
> specifico, invece di presentarli come archivio lineare?

**13.4 Portare il visitatore dalla ricerca alla demo**

```text
problema normativo → modulo/contenuto pertinente → caso simile → fiducia → demo
```

**13.5 Gestire il catalogo di moduli e versioni**

```text
release / modulo → documentazione → pagina prodotto → guida → caso d'uso
→ comunicazione cliente
```

**13.6 Rispondere senza esporre in modo incontrollato la conoscenza** — base di
risposte approvate; fonti e date visibili; distinzione tra informazione generale e
consulenza; aggiornamento centralizzato; controllo umano prima della pubblicazione;
versionamento delle risposte.

**13.7 Governare il network di contenuti**

```text
ruolo ↔ settore ↔ modulo ↔ problema ↔ normativa ↔ caso cliente ↔ demo
```

Passare da un sito composto da pagine a un sistema che conosce le relazioni fra pagine
e contenuti.

## 14. Ricollegamento a Open Nexus

**14.1 Contenuto strutturato:** Modulo · Norma · Obbligo · Ruolo · Settore ·
Caso cliente · Versione · Webinar · Documento · Domanda · CTA

**14.2 Source Authority:** fonte normativa; data; versione; responsabile; stato
(bozza, verificato, pubblicato, superato); collegamenti alle pagine derivate.

**14.3 Contenuto → viste**

```text
knowledge model → website view · support view · sales view
                → webinar view · customer view
```

**14.4 Workflow editoriale governato**

```text
fonte normativa → estrazione → proposta di contenuto → verifica esperto
→ pubblicazione → collegamento alle pagine dipendenti → eventuale ritiro/aggiornamento
```

L'agente può proporre aggiornamenti, ma non dovrebbe pubblicare autonomamente
contenuti normativi senza approvazione.

**14.5 Experience per ruolo:** "Sono un produttore"; "Sono un trasportatore"; "Gestisco
un impianto"; "Sono un consulente"; "Devo capire RENTRI"; "Voglio una demo".

Open Nexus non crea soltanto pagine: crea **percorsi di conoscenza**.

## 15. Possibile applicazione sonda — Prometeo Knowledge Experience

Un layer editoriale e commerciale che: collega moduli, ruoli, problemi, norme e casi
cliente; genera viste diverse dallo stesso contenuto; mantiene fonti, date e versioni;
propone aggiornamenti; crea percorsi verso la demo; supporta il team nella risposta a
domande ricorrenti.

**MVP possibile:** importare una piccola parte delle pagine esistenti; modellare 10
moduli, 5 ruoli e 10 casi cliente; collegare ciascun contenuto a fonte e versione;
generare tre percorsi (produttore, trasportatore, consulente); fornire un assistente
read-only con citazioni; misurare se il team riduce il tempo di aggiornamento e
risposta.

## 16. Limiti specifici di questa ipotesi

```text
· i bisogni del team sito sono inferiti, non intervistati
· non sappiamo chi possieda oggi il modello editoriale
· il sito potrebbe essere solo una vetrina e non il collo di bottiglia
· il sistema potrebbe avere già CMS, CRM, knowledge base o procedure interne
· un nuovo layer può creare doppia manutenzione
· la conoscenza normativa richiede revisione professionale
· il potenziale cliente potrebbe essere Informatica EDP, non l'utente finale
· l'integrazione commerciale e tecnica con Prometeo non è verificata
```

## 17. Conclusione

```text
utente Prometeo            → vuole gestire correttamente il ciclo dei rifiuti
gestore del sito Prometeo  → deve organizzare, aggiornare, spiegare e
                             commercializzare la conoscenza del prodotto
```

Per Open Nexus il secondo caso è una connessione più naturale e meno invasiva:

> **Open Nexus potrebbe diventare il sistema che trasforma la conoscenza verticale di
> Prometeo in percorsi pubblici, supporto verificabile e comunicazione commerciale,
> senza sostituire il gestionale transazionale.**

## 18. Domande da validare con il gestore

1. Qual è oggi il costo maggiore nel mantenere aggiornato il sito?
2. Quante volte viene duplicato lo stesso contenuto tra sito, PDF, webinar e assistenza?
3. Come vengono gestite norme, release e contenuti superati?
4. Chi approva una pagina normativa o commerciale?
5. Come viene scelto il caso cliente da mostrare a un nuovo visitatore?
6. Quali domande arrivano più spesso prima della demo?
7. Esiste già un CRM o una knowledge base collegata al sito?
8. Quale metrica dovrebbe migliorare: tempo di aggiornamento, richieste qualificate,
   demo, supporto o conversione?
9. Chi avrebbe budget per un layer del genere?
10. Prometeo preferirebbe usarlo internamente, integrarlo nel prodotto o venderlo ai
    propri clienti?

## 19. Test architetturale della sonda

### Foundation invariata

La sonda dovrebbe consumare, senza ridefinirli: `PageData`; `ApplicationBundle`;
`ApplicationDefinition`; `ApplicationContext`; `BundleCollector`; `DiscoveryService`;
runtime; validazione; renderer; contratti di pubblicazione.

### X / application-specific

Restano nell'esperienza Prometeo: modello di moduli, ruoli, norme e casi cliente;
contenuti RENTRI; percorsi produttore/trasportatore/consulente; relazioni tra pagine
del sito; CTA e funnel demo; workflow editoriale specifico; tono e branding Prometeo.

```text
Prometeo Knowledge Experience
  → application model specifico → PageData → renderer / experience
  → Foundation invariata
```

### Capacità condivise candidabili

Una capacità può entrare nel core soltanto se serve anche a una seconda applicazione
nominata. Candidate: modello di fonte e citazione; stato editoriale (bozza, verificato,
pubblicato, superato); versionamento dei contenuti; relazione contenuto → viste;
workflow proposta → revisione → approvazione → pubblicazione; aggiornamento delle
viste dipendenti; percorsi per ruolo; assistente read-only con evidenze; gestione di
CTA e conversion event; analytics della knowledge experience.

Queste non vanno promosse automaticamente: la sonda deve prima dimostrare quali sono
realmente comuni.

### Criterio di successo

```text
1. produce un'esperienza utile per il gestore del sito
2. usa Foundation senza modificarne i contratti
3. individua almeno una capability riutilizzabile
4. una seconda applicazione conferma la stessa capability
5. la promozione nel core è giustificata da evidenza, non da eleganza
```

> **La sonda deve stressare Foundation, non costringerla a diventare Prometeo.**

La migliore connessione con Open Nexus non è costruire un altro Prometeo. È aggiungere
un livello che renda il sistema:

> **interrogabile, spiegabile, verificabile e navigabile per ruolo, senza togliere al
> gestionale la responsabilità transazionale e normativa.**

La prima opportunità concreta è quindi:

> **Waste Evidence Assistant: un layer read-only che trasforma dati e documenti della
> gestione rifiuti in controlli, dossier, scadenze e decisioni assistite, con ogni
> risultato collegato alla fonte.**

Il prossimo passo di validazione non è implementare. È verificare: quale ruolo soffre
di più il problema; quale fonte dati è realmente esportabile; quale controllo oggi
viene fatto manualmente; chi pagherebbe il layer; se Informatica EDP sarebbe partner,
cliente o concorrente; quale singolo workflow può essere dimostrato senza accesso
produttivo.

---

*Documento sorgente. Analisi derivata e correzioni in `28-PROMETEO-RENTRI.md`,
`29-PROMETEO-ANALISI.md` (D-060 → D-062), `31-QUANTIZZAZIONE-PROMETEO.md`.*
