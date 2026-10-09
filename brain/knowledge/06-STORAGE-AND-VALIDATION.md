# 06 — STORAGE AND VALIDATION

**Perimetro:** chi produce i record del Brain, dove vivono, chi li valida e come
vengono generate le viste.
**Dipende da:** `05-EVALUATION.md` e dal contratto del claim record.
**Natura:** applicazione al Brain di principi già validati in Foundation.

---

## 0. Principio

> **Il record è source of truth. Database, grafo, matrice e report sono proiezioni.**

Lo storage non deve nascondere la provenienza, e la validazione non deve dipendere
dallo stesso agente che propone il contenuto.

```text
azione di acquisizione
        ↓
record nativo e tracciato
        ↓
gate deterministico
        ↓
review assistita
        ↓
ratifica umana, quando necessaria
        ↓
proiezioni rigenerabili
```

Il Brain non è un secondo sistema: applica alla conoscenza lo stesso modello di
Foundation.

---

## 1. Chi compila i record

Nessun singolo attore possiede l'intero record.

### 1.1 Campi derivati dall'azione

Sono prodotti dal tool nel momento stesso dell'acquisizione. Non possono essere
ricostruiti a posteriori né compilati manualmente.

```text
source_url
source_locator
excerpt
collected_at
collection_action
tool_id / tool_version
http_status
content_type
rendering_mode
content_sha / excerpt_sha
```

**Regola:** se un campo può essere derivato, deve essere derivato.

Un `collected_at` scritto a mano non è un timestamp: è un ricordo. Un excerpt
ricostruito dall'agente non è evidenza: è una citazione presunta.

### 1.2 Campi proposti dal Brain

Il Brain può proporre, ma non ratificare autonomamente:

```text
epistemic_status       OBSERVED | INFERRED | LIMIT
claim_type
quantity_type          count | ratio | median | distribution | none
declared_by            primary | vendor | third_party | us
transformation         none | summarized | translated | computed | aggregated
decision_role
interpretation
candidate_relations
```

Ogni campo proposto conserva:

```text
proposed_by
proposed_at
model_id_resolved
prompt_or_capability_version
```

Il modello risolto va registrato, non soltanto quello richiesto: impedisce che un
fallback silenzioso cambi costo o comportamento senza lasciare traccia.

### 1.3 Campi ratificati dall'umano

L'umano interviene soltanto dove esiste una decisione, non per trascrivere dati che
il sistema può derivare.

```text
final_epistemic_status
accepted_interpretation
accepted_decision_role
approval_status
approved_by
approved_at
review_note
```

**Regola:** proposta ≠ decisione. Un agente propone; un gate verifica; una persona
approva gli output sensibili.

---

## 2. Dove vivono i record

### 2.1 Source of truth: file versionati

Formato iniziale consigliato:

```text
brain/records/<corpus>/<date>.jsonl
```

Un record JSON per riga.

Perché file e non database:

```text
diffabile       si vede cosa cambia
versionabile    Git conserva autore, data e storia
portabile       nessun lock-in su database o servizio
auditabile      il record resta leggibile senza runtime
ricostruibile   indici e grafi possono essere rigenerati
```

Il testo e il record sono source authority. Il database è indice derivato.

### 2.2 Indici derivati

A seconda del volume:

```text
SQLite / FTS5        ricerca testuale locale, costo quasi zero
PostgreSQL / trigram ricerca multi-utente
Redis                cache, stato effimero, invalidazione — mai source of truth
grafo                proiezione per relazioni e dipendenze
embeddings           proiezione opzionale, mai fonte
```

Il principio di D-009 resta valido:

> **Il testo è source authority. L'embedding è una proiezione, mai una fonte.**

### 2.3 Il grafo è una vista

Il grafo non possiede i claim. Li collega.

```text
claim_id → source_id
claim_id → derived_from
claim_id → supersedes / superseded_by
claim_id → contradicts
claim_id → supports
claim_id → affects
```

Il grafo può essere cancellato e ricostruito dai record JSONL. Se non può, ha
acquisito ownership che non gli appartiene.

---

## 3. Versionamento e successione

### 3.1 Quando incrementa `claim_version`

```text
incrementa          cambia il testo del claim
                    cambia il tipo epistemico
                    cambia il significato sostanziale

non incrementa      si aggiunge una fonte corroborante
                    si precisa il denominatore senza cambiare il claim
                    si corregge un refuso che non cambia il significato

nuovo claim_id      cambia la fonte primaria
                    nasce una diversa interpretazione
                    il nuovo record sostituisce una tesi precedente
```

### 3.2 Successione bidirezionale

Un claim sostituito deve dichiarare:

```text
superseded_by: <claim_id>
```

Il nuovo claim deve dichiarare:

```text
supersedes: <claim_id>
```

Il gate rifiuta:

```text
· puntatori verso claim inesistenti
· catene circolari
· stato superseded senza superseded_by
· claim che supersede sé stesso
```

Un claim sostituito senza puntatore è un orfano. In un corpus accumulativo, gli
orfani rendono il passato illeggibile.

---

## 4. Tipi quantitativi

Non ogni quantità ha un denominatore.

```text
count          "300 interviste", "50.000 app"
ratio          "25% delle app con pagamento"
median         "mediana preventivi di 20.000 dollari"
distribution   "33/27/27/12"
none           claim non quantitativo
```

### 4.1 Campi obbligatori per tipo

```text
count
  value · unit
  population_note opzionale

ratio
  numerator · denominator · formula obbligatori

median
  value · sample_size · sample_definition obbligatori

distribution
  buckets · denominator · sample_definition obbligatori
```

**Regola:** un rapporto senza numeratore e denominatore è metà dell'evidenza.

Se la fonte dichiara soltanto la percentuale:

```text
formula_status: not_derivable
```

Non inventare i termini mancanti.

---

## 5. Temporalità

`as_of` non accetta prosa.

```json
{
  "as_of": null,
  "as_of_note": "report snapshot; exact date not published in excerpt"
}
```

Schema:

```text
as_of        ISO date-time | null
as_of_note   string | null
collected_at ISO date-time, obbligatorio e derivato dal tool
```

`as_of` dice a quando si riferisce il fatto. `collected_at` dice quando lo abbiamo
acquisito. Non sono intercambiabili.

---

## 6. Corroborazione e indipendenza

Due URL non implicano due fonti.

```text
Emergent report → articolo che cita Emergent
```

È una fonte con due URL, non corroborazione.

Ogni fonte corroborante dichiara:

```text
source_id
origin_id
publisher
method
independence_basis:
  different_publisher
  different_method
  different_time
  primary_vs_secondary
  same_origin
```

**Regola:** lo stato `corroborated` richiede almeno una fonte con
`independence_basis` diverso da `same_origin`.

Fonti che condividono `origin_id` non sono indipendenti, anche se hanno publisher o
URL diversi.

---

## 7. Stati del record ed eventi del processo

Non vanno mescolati.

### 7.1 Stati del record

```text
captured
normalized
source_checked
corroborated
superseded
rejected
```

Un record ha un solo stato principale alla volta.

### 7.2 Flag ortogonali

```text
challenged: true | false
needs_human_review: true | false
contains_sensitive_data: true | false
```

`challenged` può colpire un record in qualunque stato. Non è una fase lineare.

### 7.3 Eventi del processo

```text
captured
normalized
source_checked
corroborated
interpreted
challenged
approved
rejected
superseded
```

Gli eventi sono append-only. `interpreted` produce un **nuovo claim derivato**, non
trasforma lo stato epistemico del claim originale.

```text
original_claim_id
        ↓ derived_from
interpretation_claim_id
```

Questo permette interpretazioni multiple della stessa evidenza senza alterare il
record osservato.

---

## 8. Chi valida

### 8.1 Gate deterministico — blocca

Classe 0, nessun LLM.

```text
· JSON schema valido
· campi obbligatori presenti
· enum validi
· excerpt non vuoto
· content_sha / excerpt_sha coerenti
· collected_at non nel futuro
· regole quantitative di § 4 rispettate
· supersedes / superseded_by coerenti
· stato corroborated → indipendenza presente
· as_of date-time o null, mai prosa
```

Se fallisce, il record non entra nel corpus.

### 8.2 Brain — segnala

Classe 1, su richiesta.

```text
· il marcatore epistemico è corretto?
· l'excerpt supporta davvero il claim?
· il claim è più ampio della fonte?
· due claim si contraddicono?
· un'opportunità proposta è già coperta dall'incumbent?
· una posizione descritta coincide con una nostra capability o istanza?
```

Il Brain produce findings, non verdetti vincolanti.

### 8.3 Umano — decide

Necessario per:

```text
· approvare interpretazioni sensibili
· accettare o rifiutare una proposta
· scegliere tra fonti in conflitto
· autorizzare pubblicazione o azione
· validare classificazioni di dominio
```

**Il gate automatico blocca. Il Brain segnala. L'umano decide. Mai il contrario.**

---

## 9. Matrici, report e PageData

### 9.1 La matrice è una vista generata

```text
record JSONL in Git       source of truth
matrice                   vista rigenerabile, non mantenuta a mano
report Markdown / HTML    renderer della matrice
PageData                  linguaggio della knowledge experience
```

La matrice non va salvata come secondo source of truth.

### 9.2 Snapshot pubblicabili

Un output inviato a un destinatario deve essere riproducibile.

Lo snapshot contiene:

```text
artifact_id
built_at
record_set_sha
claim_ids
ruleset_version
template_version
```

È un artefatto di build, non un documento da aggiornare a mano.

Se i record cambiano, si genera un nuovo snapshot. Il precedente resta leggibile e
verificabile.

---

## 10. Dove stanno struttura e interpretazione

Esempio di layout:

```text
brain/
├── knowledge/
│   ├── 05-EVALUATION.md
│   └── 06-STORAGE-AND-VALIDATION.md
├── contracts/
│   ├── claim-record.schema.json
│   ├── acquisition-record.schema.json
│   └── artifact-snapshot.schema.json
├── records/
│   └── <corpus>/YYYY-MM-DD.jsonl
├── projections/
│   ├── sqlite/
│   └── graph/
└── artifacts/
    └── <artifact-id>/
```

I contratti sono implementazione della conoscenza formalizzata. I record sono dati.
Le proiezioni sono eliminabili. Gli artefatti sono riproducibili.

---

## 11. I sei campi gate minimi

Il contratto completo può avere molti campi. Per evitare che il peso ne impedisca
l'uso, sei sono obbligatori per ogni claim:

```text
claim_id
text
epistemic_status
source_url
excerpt
collected_at
```

Gli altri diventano obbligatori **in base al tipo** o allo stato:

```text
quantity_type = ratio        → numerator, denominator, formula
state = corroborated         → corroborating_source_ids, independence_basis
state = superseded           → superseded_by
transformation ≠ none        → transformation metadata, computed_from
```

**Test di peso:** registrare un claim reale e cronometrare.

```text
≤ 5 minuti     contratto usabile
6–20 minuti    al limite: automatizzare i campi derivabili
> 20 minuti    troppo pesante: ridurre prima di procedere
```

Il peso del contratto è un requisito. Un contratto non usato è peggio di nessun
contratto, perché produce l'illusione della tracciabilità.

---

## 12. Primo test

Prendere un claim del report Emergent:

> "Il 25% delle app del campione ha pagamenti integrati."

Il record deve dichiarare:

```text
chi lo dichiara               Emergent
fonte                         URL + locator + excerpt
quando acquisito              timestamp derivato
status epistemico             OBSERVED / reported-by-vendor
quantity_type                 ratio
numerator / denominator       se pubblicati
formula                       numerator / denominator
formula_status                derivable | not_derivable
verificabilità esterna        no | partial
trasformazione                summarized, se il testo non è verbatim
```

Se il contratto blocca il claim per mancanza di numeratore o denominator, ha fatto il
suo lavoro: ha reso visibile ciò che il report precedente nascondeva nella prosa.

---

## 13. Cosa questo documento non decide

```text
· il database definitivo
· il framework del grafo
· il provider LLM
· la UI di review
· l'ontologia completa del Brain
· il modello commerciale
```

Queste decisioni vengono dopo il primo record nativo e il primo snapshot generato.

---

*Trascritto il 2026-09-18. Applica a conoscenza principi già validati in Foundation:
source authority, proiezioni derivate, gate deterministico, review umana, artefatti
riproducibili.*
