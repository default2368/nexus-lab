# Strategia — Foundation Bootstrap / Self-Hosting Foundation

**Status:** APPROVED ARCHITECTURAL DIRECTION — IMPLEMENTATION DEFERRED
**DecisionId:** NX-D-046-FOUNDATION-BOOTSTRAP
**Source:** Context 8 + Owner intuition 10/10 + Main Agent analysis 8/10 perspicacia
**Date:** 2026-10-09
**Extractor:** documentation-agent v0.1.0

---

## Voto analisi

```text
Voto analisi 10/10
Voto perspicacia mio (Main Agent) 8/10
Avevo visto:
repository → fabbrica
package → prodotto

Tu hai fatto il passaggio successivo:
la fabbrica → può usare il proprio processo → per rifondare sé stessa

Quello non lo avevo ancora esplicitato fino in fondo.

La tua intuizione: 10/10
Sì: questa è una conseguenza architetturale reale
```

---

## Stato evidenza

```text
INFERRED FROM PRIOR EVIDENCE
non ancora:
FINAL RELEASE VERIFIED
```

Verdetto:

> Se Simple viene prodotto e funziona fuori dal repository, allora Open Nexus ha già separato la fabbrica dal prodotto.

A quel punto la 0.9 non deve inventare un'altra piattaforma. Deve dare alla fabbrica un nuovo materiale: entità, relazioni e annotazioni epistemiche.

---

## Intuizione owner

> Supponiamo che owner si sia stancato del rumore. Decide di partire dalle risultanti di 0.8.2 e 0.9.0 con una nuova 0.9.2 (mi pare sia questa la versione delle entity, o la 0.9.1) poco-importa e realizzare nuove applicazioni magari con pipeline che ne standardizzino la realizzazione? non avremmo una foundation rifondata pulita che si avvantaggia del suo stesso sistema? non è moat anche questo?

Risposta: Sì, moat candidato molto forte.

---

## Due modi di "rifondare"

### 1. Nuova applicazione pulita che consuma Foundation — strada semplice e probabilmente migliore

```text
Foundation core
→ dependency/versioned release

nuovo repository
→ ApplicationBundle
→ Domain Pack
→ presentation
→ configuration
```

Il nuovo repo non contiene il kernel copiato. Lo consuma come release.

Layout:

```text
new-knowledge-app/
├── .nexus/
├── applications/
├── domain-packs/
├── presentation/
├── fixtures/
├── tests/
└── package.json
```

Questa non è una nuova Foundation. È un consumer pulito.

### 2. Nuova Foundation bootstrap — più ambizioso

```text
current Foundation
→ produce Foundation Next
Foundation Next diventa la nuova authority di sviluppo soltanto se supera un bootstrap gate.
```

```text
F0 produce F1
F1 produce gli stessi artifact approvati
F1 può produrre F2 equivalente
```

Questo è il pattern dei compilatori self-hosting.

---

## Il test del punto fisso

La prova forte sarebbe:

```text
Foundation current
+ Simple spec
→ Simple package A

Foundation Next
+ stessa Simple spec
→ Simple package B

semantic inventory A
=
semantic inventory B
```

Non necessariamente byte-identico, perché provenance/commit possono cambiare.

Confrontiamo:

```text
page IDs
order
templates
assets
routes
capabilities
contracts
clean-room behavior
failure findings
```

Poi:

```text
Foundation Next
→ ricostruisce Foundation Next 2

semantic result
→ equivalente
```

Se succede, Foundation ha raggiunto una forma di self-hosting.

---

## Perché è moat

Non perché produci una repository pulita una volta.

Quello è copiabile.

Il moat candidato è:

> Puoi rigenerare sistematicamente ambienti puliti e verticali diversi partendo da contratti, fonti e decisioni governate, mantenendo compatibility, provenance e test.

Chi copia una singola applicazione copia uno snapshot.

Non copia automaticamente:

```text
il compiler
le authority
i gate
i migration ledger
i compatibility rules
i receipts
la capacità di rigenerare
la storia delle falsificazioni
```

```text
codebase pulita
→ output

meccanismo che la rigenera
→ capability

meccanismo che rigenera anche sé stesso
→ candidate moat
```

---

## Effetto sul rumore

L'owner può dire:

> Questo repository ha compiuto il proprio lavoro storico. Voglio un nuovo ambiente che contenga soltanto ciò che oggi è approvato.

La pipeline produce:

```text
current approved contracts
current application definitions
current Domain Packs
current templates/assets
current tests
explicit compatibility adapters
```

Tutto il resto rimane:

```text
Git history
archive repository
migration evidence
```

Non nel nuovo active source tree.

Il rumore smette di essere qualcosa da pulire per sempre. Diventa materiale storico esterno all'artifact corrente.

Quando il rumore storico supera il valore operativo, non continui a ripulire all'infinito; materializzi una nuova baseline dalla conoscenza e dai contratti approvati.

---

## Effetto sugli N settori

Pipeline standard:

```text
Foundation Release
+ Workspace Profile
+ Domain Pack
+ Application Definition
+ approved data/source contracts
        ↓
new application workspace
```

Esempi:

```text
G.
→ Audit Engagement workspace

A.
→ Operation Reconstruction workspace

F.
→ Project/Program Evidence workspace

altro dominio
→ altro Domain Pack
```

Stessa macchina, output differenti.

Il verticale non fork-a Foundation.

Coerente con requisito verticale finale deve NON incanalare progetto verso determinato settore, ma produrre valore in N settori.

---

## Effetto sulla CLI

Qui la CLI trova finalmente una responsabilità inevitabile:

```bash
opnx workspace create \
  --foundation v0.9.x \
  --profile governed-dossier \
  --domain g-audit
```

Poi:

```bash
opnx plan
opnx apply
opnx verify
```

Receipt:

```yaml
foundationRelease:
contractBundle:
workspaceProfile:
domainPack:
sourceCommit:
generatedFiles:
packageDigest:
compatibilityFindings:
verification:
```

La CLI non duplica Foundation. La orchestra.

---

## Effetto sul Brain

Il Brain può fare:

```text
documenti/procedure
→ Candidate Domain Definition
→ Candidate ApplicationSpec
```

Ma non scrive il repository direttamente.

```text
Brain propone
→ owner approva
→ Authoring Core valida
→ CLI applica
→ Foundation produce
```

---

## Rischio principale

Il self-hosting può diventare autoillusione.

```text
Foundation genera un nuovo repo
→ test scritti dalla stessa Foundation
→ tutto verde
non basta.
```

Servono:

```text
golden fixture esterne
equivalence test
protected contract comparison
independent second consumer
manual owner inspection
rollback
vecchia Foundation conservata finché F1 non è provata
```

Non cancellare F0 appena F1 compila.

---

## Versione

Non fisserei ora:

```text
0.9.1
0.9.2
```

Perché questa capability potrebbe essere:

```text
un addendum 0.9.x
una 0.10
la vera soglia 1.0
```

Il numero dipende dall'impatto sul public contract.

Nome di programma candidato:

```text
Foundation Bootstrap
oppure:
Self-Hosting Foundation
```

Stato:

```text
APPROVED ARCHITECTURAL DIRECTION
IMPLEMENTATION DEFERRED
```

---

## Sequenza realistica

```text
1. chiudere 0.8.2
   → Simple Distribution Proof

2. integrare Semantic Entity 0.9
   → core invariato

3. produrre una seconda app da Domain Pack
   → prova N-settori

4. definire Workspace/ApplicationSpec
   → input machine-readable

5. CLI workspace create
   → fresh consumer repo

6. Foundation Bootstrap experiment
   → F0 produce F1

7. equivalence/fixed-point gate
   → decisione Foundation Next
```

---

## Formulazione che terrei

> Foundation non serve soltanto a produrre applicazioni. Se i suoi contratti e artifact diventano sufficientemente completi, può diventare il sistema con cui Open Nexus rigenera ambienti puliti, applicazioni verticali e, infine, una nuova versione governata di sé stesso.

---

## Conclusione

Sì, è moat candidato.

```text
una repository pulita
→ no, copiabile

una pipeline che produce repository pulite
→ più difficile

una pipeline governata che produce N domini
→ forte

una Foundation che può riprodurre semanticamente sé stessa
→ molto forte
```

E soprattutto risolve un problema reale che abbiamo vissuto, non un esercizio teorico:

> quando il rumore storico supera il valore operativo, non continui a ripulire all'infinito; materializzi una nuova baseline dalla conoscenza e dai contratti approvati.

---

## Provenance

```
Context 8: Voto perspicacia prima risposta 7/10 Voto dopo aver seguito filo 9/10 vera implicazione Se catena funziona ApplicationBundle Simple→Foundation→manifest→package autonomo→clean-room→Execution allora Open Nexus è già fabbrica di applicazioni distribuibili Non soltanto framework CMS repository Prodotto non è necessariamente codice che vediamo nel repository repository→ambiente authoring compiler governance package→prodotto distribuibile Execution→runtime sottile ApplicationBundle/Domain Pack→ciò che differenzia verticali — Owner domanda se owner stanco rumore decide partire da risultanti 0.8.2 e 0.9.0 con nuova 0.9.2 (versione entity) e realizzare nuove applicazioni magari con pipeline che ne standardizzino realizzazione non avremmo foundation rifondata pulita che si avvantaggia suo stesso sistema non è moat anche questo — Voto perspicacia mio 8/10 Avevo visto repository→fabbrica package→prodotto Tu hai fatto passaggio successivo fabbrica→può usare proprio processo→per rifondare sé stessa Quello non avevo ancora esplicitato fino in fondo Tua intuizione 10/10 Sì conseguenza architetturale reale — Supponiamo 0.8.2 Distribution Core stabile package Simple riproducibile manifest/materialization/clean-room 0.9.x Semantic Entity Projection Domain Pack entity relation view artifact PageData Adapter A quel punto possiamo immaginare Foundation corrente+contratti approvati+ApplicationBundle+Domain Pack+Distribution Profile+migration ledger ↓ bootstrap pipeline ↓ nuovo workspace Foundation/app ↓ package ↓ clean-room ↓ equivalence receipt Risultato può essere nuova codebase pulita che contiene soltanto contratti correnti Runtime Execution Shell applicazioni approvate Domain Pack scelti template asset realmente necessari test correnti nessuna copia legacy nessun backup nessuna superficie storica nessuna authority duplicata — Ma distinzione importante producer attuale sa fare ApplicationBundle→application package Non sa ancora fare Foundation Release→nuovo repository Foundation sorgente Per secondo serve bootstrap/authoring layer ProjectSpec Foundation Release ApplicationSpec DomainPackSpec WorkspaceProfile ↓ Authoring Core/CLI ↓ repository materialization Quindi capability non ancora completa ma fondamenta esistono — Due modi rifondare 1 Nuova applicazione pulita che consuma Foundation più semplice e probabilmente migliore Foundation core→dependency/versioned release nuovo repository→ApplicationBundle→Domain Pack→presentation→configuration nuovo repo non contiene kernel copiato Lo consuma come release Layout new-knowledge-app/.nexus/applications/domain-packs/presentation/fixtures/tests/package.json Questa non è nuova Foundation È consumer pulito 2 Nuova Foundation bootstrap più ambizioso current Foundation→produce Foundation Next Foundation Next diventa nuova authority sviluppo soltanto se supera bootstrap gate F0 produce F1 F1 produce stessi artifact approvati F1 può produrre F2 equivalente pattern compilatori self-hosting — Test punto fisso prova forte Foundation current+Simple spec→Simple package A Foundation Next+stessa Simple spec→Simple package B semantic inventory A = semantic inventory B Non necessariamente byte-identico perché provenance/commit possono cambiare Confrontiamo page IDs order templates assets routes capabilities contracts clean-room behavior failure findings Poi Foundation Next→ricostruisce Foundation Next 2 semantic result→equivalente Se succede Foundation ha raggiunto forma self-hosting — Perché è moat Non perché produci repository pulita una volta Quello è copiabile Moat candidato è Puoi rigenerare sistematicamente ambienti puliti e verticali diversi partendo da contratti fonti decisioni governate mantenendo compatibility provenance test Chi copia singola applicazione copia snapshot Non copia automaticamente compiler authority gate migration ledger compatibility rules receipts capacità di rigenerare storia falsificazioni codebase pulita→output meccanismo che la rigenera→capability meccanismo che rigenera anche sé stesso→candidate moat — Effetto rumore Owner può dire Questo repository ha compiuto proprio lavoro storico Voglio nuovo ambiente che contenga soltanto ciò che oggi è approvato Pipeline produce current approved contracts current application definitions current Domain Packs current templates/assets current tests explicit compatibility adapters Tutto resto rimane Git history archive repository migration evidence Non nel nuovo active source tree Rumore smette essere qualcosa da pulire per sempre Diventa materiale storico esterno all'artifact corrente — Effetto N settori Pipeline standard Foundation Release+Workspace Profile+Domain Pack+Application Definition+approved data/source contracts ↓ new application workspace Esempi G→Audit Engagement workspace A→Operation Reconstruction workspace F→Project/Program Evidence workspace altro dominio→altro Domain Pack Stessa macchina output differenti Verticale non fork-a Foundation — Effetto CLI Qui CLI trova finalmente responsabilità inevitabile opnx workspace create --foundation v0.9.x --profile governed-dossier --domain g-audit Poi opnx plan opnx apply opnx verify Receipt YAML foundationRelease contractBundle workspaceProfile domainPack sourceCommit generatedFiles packageDigest compatibilityFindings verification CLI non duplica Foundation La orchestra — Effetto Brain Brain può fare documenti/procedure→Candidate Domain Definition→Candidate ApplicationSpec Ma non scrive repository direttamente Brain propone→owner approva→Authoring Core valida→CLI applica→Foundation produce — Rischio principale self-hosting può diventare autoillusione Foundation genera nuovo repo→test scritti stessa Foundation→tutto verde non basta Servono golden fixture esterne equivalence test protected contract comparison independent second consumer manual owner inspection rollback vecchia Foundation conservata finché F1 non è provata Non cancellare F0 appena F1 compila — Versione Non fisserei ora 0.9.1 0.9.2 Perché capability potrebbe essere addendum 0.9.x una 0.10 vera soglia 1.0 Numero dipende impatto su public contract Nome programma candidato Foundation Bootstrap oppure Self-Hosting Foundation Stato APPROVED ARCHITECTURAL DIRECTION IMPLEMENTATION DEFERRED — Sequenza realistica 1 chiudere 0.8.2→Simple Distribution Proof 2 integrare Semantic Entity 0.9→core invariato 3 produrre seconda app da Domain Pack→prova N-settori 4 definire Workspace/ApplicationSpec→input machine-readable 5 CLI workspace create→fresh consumer repo 6 Foundation Bootstrap experiment→F0 produce F1 7 equivalence/fixed-point gate→decisione Foundation Next — Formulazione che terrei Foundation non serve soltanto a produrre applicazioni Se suoi contratti e artifact diventano sufficientemente completi può diventare sistema con cui Open Nexus rigenera ambienti puliti applicazioni verticali e infine nuova versione governata di sé stesso — Conclusione Sì è moat candidato una repository pulita→no copiabile una pipeline che produce repository pulite→più difficile una pipeline governata che produce N domini→forte una Foundation che può riprodurre semanticamente sé stessa→molto forte E soprattutto risolve problema reale che abbiamo vissuto non esercizio teorico quando rumore storico supera valore operativo non continui a ripulire all'infinito materializzi nuova baseline dalla conoscenza e dai contratti approvati
Status: APPROVED ARCHITECTURAL DIRECTION IMPLEMENTATION DEFERRED
Extractor: documentation-agent v0.1.0
```
