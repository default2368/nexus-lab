# Prompt MCP-ready — Q-005 / NX-11 / NX-12

Da incollare in Roo Code. Due prompt separati: **A** per `deepseek-v4-pro`
(giudizio architetturale), **B** per `deepseek-flash` (residui di verifica).

---

## PROMPT A — `deepseek-v4-pro` · Plan mode · Q-005

```text
Questa è una review architetturale read-only.
NON modificare alcun file. NON creare file. Output = report.

CONTESTO
AF-001 risulta chiuso: getApplicationType non chiama più
new BundleCollector().collect(), ma legge APPLICATION_TYPE_PROJECTION[appId],
una Object.freeze con 5 app hardcodate, in
src/core/domain-authority/projections/getApplicationType.ts

Il problema da valutare: un bundle autorato (roadmap 0.7.0, flusso
Human/AI/Importer -> ApplicationBundle -> BundleCollector -> Build Artifacts
-> Runtime) produce un appId non presente nella tabella.

DOMANDA UNICA E DECISIVA
applicationType è un campo DICHIARATO di ApplicationDefinition, o è INFERITO?

PROCEDURA OBBLIGATORIA
1. index_status
   Se non sincronizzato, fermati e riportalo. Non procedere su indice sporco.
2. search_graph per: ApplicationDefinition
3. get_code_snippet su ApplicationDefinition (il type/interface completo)
4. Verificare presenza/assenza di un campo di tipo applicazione.
   Cercare anche: applicationType, appType, type, kind, visibility, audience
5. search_graph per: APPLICATION_TYPE_PROJECTION
6. get_code_snippet su APPLICATION_TYPE_PROJECTION
7. trace_path su getApplicationType (direzione both)
8. get_code_snippet su buildNavigation: cosa fa del valore ricevuto,
   e cosa succede se è undefined
9. Verificare se esiste un test che copre un appId non presente nella tabella

SIMBOLI VINCOLATI - CLAUSOLA DI STOP
PageController, normalizeToPageData, ApplicationDefinition,
ApplicationContext, BundleCollector, DiscoveryService, DiscoveryServiceV2,
PageData.
La review è read-only quindi è safe. Ma se la RISOLUZIONE richiede di modificare
uno di questi, devi fermarti e dichiararlo come FOUNDATION RFC.
Non proporre implementazioni che li tocchino.

GUARDRAIL
Se un simbolo non esiste nel grafo, scrivi NOT FOUND.
Non inferire. Non indovinare percorsi. Non citare codice che non hai estratto
con get_code_snippet.
Distingui rigorosamente FACTS OBSERVED / HYPOTHESES / RECOMMENDATIONS.

OUTPUT RICHIESTO

1. VERDETTO Q-005
   DICHIARATO | INFERITO | PARZIALE | NOT FOUND
   con il file e la riga che lo provano

2. SE DICHIARATO
   - la projection è derivazione pura del bundle?
   - può essere emessa da BundleCollector come Build Artifact senza modifiche
     ai contratti?
   - resta in ZONA SICURA (X) o tocca Foundation?

3. SE INFERITO
   - da cosa viene inferito esattamente?
   - quale campo mancherebbe in ApplicationDefinition?
   - questo è un contract gap: dichiaralo come FOUNDATION RFC e fermati

4. COMPORTAMENTO SU appId ASSENTE (NX-12 / Q-006)
   undefined silenzioso | throw | default | altro
   Cosa fa buildNavigation con quel valore?
   C'è un test che lo copre?

5. CONFRONTO CON F-01
   F-01 è Identifier Authority Drift: Registry ID != Bundle-derived ID,
   causa BundleCollector -> title slugging.
   Verifica se applicationType hardcodato è lo stesso pattern
   (valore derivabile dal bundle ma hardcodato nel sorgente).
   Riporta evidenze, non opinioni.

6. RECOMMENDATION
   APPROVED WITH CONDITIONS | REJECTED | DEFER
   ACCEPTANCE CONDITIONS: elenco numerato
```

---

## PROMPT B — `deepseek-flash` · Plan mode · residui di verifica

```text
Questa è una review read-only.
NON modificare alcun file. NON creare file. Output = report.

Tre verifiche residue sulla chiusura di AF-001. Nessuna richiede giudizio
architetturale: solo estrazione di fatti.

V-B1  FRESHNESS INDICE
  index_status, poi check_index_coverage.
  Riporta: generation, status, warnings, parse_partial.
  Il report precedente segnalava metadata_changed su 2 file.
  IDENTIFICA QUALI SONO I 2 FILE.
  Se sono file di projection, navigation, o PageController: segnalalo subito,
  il verdetto AF-001 va rieseguito.
  Se sono file non correlati: dichiaralo e procedi.

V-B2  V3 RESIDUO - MAPPA PRODUCE/EXECUTION
  Leggi src/pages/build/[...component].astro intorno alla riga 39.
  Poi get_architecture(aspects=[layers,boundaries,routes]).
  Produci una tabella a due colonne:
    SUPERFICIE PRODUCE   (endpoint/simboli che istanziano BundleCollector)
    SUPERFICIE EXECUTION (path che servono pagine)
  Verifica che nessun simbolo della colonna PRODUCE sia raggiungibile dalla
  colonna EXECUTION. Usa trace_path per confermare, non per esplorare.

V-B3  ALTRE PROJECTION HARDCODATE
  search_graph per il pattern "projections" e per Object.freeze
  dentro src/core/domain-authority/.
  Elenca OGNI tabella frozen analoga ad APPLICATION_TYPE_PROJECTION.
  Per ciascuna: chiave, numero di entry, chi la consuma.
  Scopo: capire se la chiusura di AF-001 ha introdotto altre tabelle statiche
  con lo stesso limite (valide per N app note, incapaci di rappresentare la N+1).

GUARDRAIL
Se un simbolo non esiste nel grafo, scrivi NOT FOUND.
Non inferire. Non citare codice che non hai estratto con get_code_snippet.
Distingui FACTS OBSERVED / HYPOTHESES / RECOMMENDATIONS.

OUTPUT
V-B1: i 2 file, con classificazione correlato/non correlato
V-B2: tabella PRODUCE | EXECUTION + esito della verifica di raggiungibilità
V-B3: elenco completo delle projection frozen con metadati
```

---

## Nota di processo

**Non passare in Act mode.** La validazione era read-only per progettazione e
V1/V2 sono già chiusi da evidenze incrociate (`search_code` + `trace_path`
bidirezionale + lettura sorgente + test di closure come guard). Rieseguire per
"evidenze paginate complete" è spendere per confermare ciò che è confermato.

**Divisione dei costi:** Prompt B (`flash`) prima, perché V-B1 potrebbe invalidare
tutto il resto — se i 2 file `metadata_changed` sono quelli di projection, il
verdetto AF-001 va rieseguito e il Prompt A sarebbe prematuro.

```text
1. Prompt B con flash   → V-B1 freshness, V-B2 mappa, V-B3 altre projection
2. Se V-B1 pulito → Prompt A con pro → verdetto Q-005
3. Q-005 DICHIARATO → NX-11 in zona sicura, si procede
   Q-005 INFERITO   → Foundation RFC, ci si ferma
```

---

*Ultimo aggiornamento: 2026-09-10*


---

# APPENDICE 2026-09-12 — Q-005: ricerca insufficiente, va rifatta

## Cosa è successo

```bash
grep -rn "applicationType\|appType" src/config/applications/ | head -20
→ zero risultati
```

**Questo NON dimostra che il concetto sia assente.** Dimostra che quei due nomi non
compaiono in quella directory. Due errori metodologici:

```text
1. cercati i NOMI, non i VALORI
   il dominio del campo è {user, workspace, shared}
   quei valori sono molto più distintivi dei nomi possibili

2. nessun sanity check sul path
   un grep su path inesistente o vuoto restituisce zero risultati
   → falso negativo indistinguibile da un vero negativo
```

## Sequenza corretta — eseguire in quest'ordine

### Passo 0 · sanity check (obbligatorio, costa un secondo)

```bash
ls -la src/config/applications/ 2>/dev/null | head -20
find src/config/applications -type f | head -20
find src/config/applications -type f | wc -l
```

Se il conteggio è 0 o il path non esiste, **fermati**: la premessa è falsa e
Application Authority sta altrove. Riportare il path reale trovato con:

```bash
find src -type d -name "applications" 2>/dev/null
```

### Passo 1 · cerca i VALORI, non i nomi

```bash
grep -rn "'workspace'\|\"workspace\"" src/config/ src/core/ | head -30
grep -rn "'shared'\|\"shared\"" src/config/ src/core/ | head -30
```

Se `workspace` o `shared` compaiono in `src/config/applications`, il concetto È
dichiarato, sotto un altro nome. Riportare nome del campo e file.

### Passo 2 · leggi una definizione reale

```bash
# il file di definizione di UNA applicazione, scelto dall'elenco del Passo 0
```

Leggerlo per intero. È il modo più informativo di rispondere: mostra **tutti** i
campi dichiarati, non solo quello che stiamo cercando.

### Passo 3 · trova dove il vocabolario è definito

```bash
grep -rn "user.*workspace.*shared\|ApplicationType" src/ --include=*.ts | head -30
```

Cerca un type/union/enum che enumeri i tre valori. Se esiste, chi lo possiede?

### Passo 4 · via MCP (se il grafo è indicizzato sul branch corrente)

```text
index_status                         → conferma freshness
search_graph   APPLICATION_TYPE_PROJECTION
get_code_snippet  APPLICATION_TYPE_PROJECTION
trace_path     APPLICATION_TYPE_PROJECTION, inbound   → chi la consuma
search_graph   ApplicationDefinition
get_code_snippet ApplicationDefinition                → l'elenco reale dei campi
```

`get_code_snippet` su `ApplicationDefinition` è la risposta definitiva: se il tipo
non contiene un campo di tipo applicazione, il concetto non è dichiarato.

## Interpretazione dei due esiti

### Esito A — il concetto È dichiarato, sotto altro nome

```text
NX-11 = sostituire la tabella frozen con la proiezione derivata
ZONA SICURA · nessun cambio di contratto · lavoro piccolo
```

### Esito B — il concetto NON è dichiarato da nessuna parte

```text
applicationType esiste SOLO dentro una Object.freeze in
src/core/domain-authority/projections/getApplicationType.ts

→ non è "derivazione sbagliata" (come F-01, che almeno deriva da title slugging)
→ è un valore SENZA ALCUNA fonte dichiarativa
→ la risposta a "chi possiede applicationType?" oggi è: NESSUNO
```

Conseguenza di Esito B, ed è la parte che conta:

```text
Domain Authority è marcata ✅ nel report dello stato di Foundation.
Ma contiene un valore senza source authority.

→ FORMALIZZARE LA POSIZIONE NON È FORMALIZZARE LA PROPRIETÀ.

Una directory può essere stata creata, popolata e testata, e contenere ancora
valori congelati a mano che nessun bundle dichiara.

Il programma "Chi possiede cosa?" (D-023) va quindi applicato come VERIFICA
sulle authority già marcate ✅, non solo esteso ai domini mancanti.
```

Da cui un controllo generalizzabile, per ogni authority esistente:

```text
per ogni valore esportato da src/core/<x>-authority/:
  · è dichiarato in una fonte (src/config/** o bundle)?
  · o è un letterale nel sorgente?

Ogni letterale è un candidato Authority Drift, indipendentemente dal fatto
che la directory abbia la spunta.
```

## Guardrail per questa ricerca

```text
· Se un comando restituisce zero risultati, riporta ANCHE il comando eseguito.
  Zero risultati senza comando non è un dato.
· Non concludere "assente" da una ricerca per nome. Solo una lettura del type
  (Passo 4) o dell'elenco campi (Passo 2) lo prova.
· FACTS OBSERVED / HYPOTHESES / RECOMMENDATIONS, separati.
· Read-only. Non modificare file.
```
