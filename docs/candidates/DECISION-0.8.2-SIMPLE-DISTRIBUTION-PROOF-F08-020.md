# DECISION — F08-020 Simple Distribution Release Proof — CANDIDATE

**Status:** CANDIDATE — MAIN_AGENT RECOMMENDATION
**DecisionId:** NX-D-045-F08-020
**HandoffId:** 0.8.2-simple-proof
**Source:** Context 5 + Context 6 + Main Agent recommendation
**Date:** 2026-10-09
**Extractor:** documentation-agent v0.1.0
**RegistryCheck:** Nome F08-020 da verificare col registry, non ancora canonico

---

## Domanda owner

> se implementassimo IL sistema di distribuzione, attualmente avremmo una distribuzione funzionante per Simple? io direi che sarebbe già un risultato

Risposta Main Agent:

```text
ApplicationBundle Simple
→ producer
→ Distribution Manifest
→ validation
→ materialization
→ clean-room
→ package utilizzabile

SÌ
```

E non sarebbe un risultato piccolo: sarebbe la prima distribuzione Foundation realmente delimitata, riproducibile e verificabile.

---

## OBSERVED — evidenza già disponibile

Nei checkpoint precedenti il package simple ha prodotto:

```text
5 pagine
4 template
5 asset

Con:
producer               ACCEPT
source provenance      GIT_VERIFIED
worktree               CLEAN
releaseEligible        true
manifest validator     ACCEPT
materialization        exit 0
clean-room             ok: true
repositoryObservations 0
```

Le modifiche successive hanno riguardato principalmente:

```text
debug route gate
Redis preview
Core Admin ID
```

Non dovrebbero modificare Simple, ma questo va nuovamente provato sul checkpoint finale.

---

## Cosa significa "funzionante" — 3 livelli

### Livello 1 — Package producibile

```text
simple source
→ manifest valido
→ package filesystem

Già dimostrato.
```

### Livello 2 — Package autonomo e verificabile

```text
package
→ clean-room
→ route/page/template resolution
→ zero repository observation

Già dimostrato nei checkpoint precedenti.
```

### Livello 3 — Prodotto installabile dall'utente

```text
opnx create/install
→ seleziona Foundation release
→ materializza in destination
→ verifica
→ avvia/deploy
→ receipt
```

Questo non è ancora chiuso come esperienza CLI/prodotto.

Ma il motore necessario al livello 3 esiste già.

---

## Il risultato reale

Non sarebbe:

```text
abbiamo costruito tutto Open Nexus.
```

Sarebbe:

> Foundation può produrre un'applicazione Simple come artifact autonomo, validato e riproducibile, senza che Runtime osservi il repository sorgente.

È esattamente la dimostrazione di:

```text
Foundation produce, Execution esegue.
```

### Perché Simple è il target giusto

Simple ha:

```text
bundle delimitato
page identity stabile
template closure conosciuta
asset closure conosciuta
nessuna complessità Operations
nessun profilo GATED/DEV_ONLY
nessuna migration System
package già provato
```

```text
minimal
≠
banale
```

### Cosa dimostra

```text
Repository-Centric
→ Artifact-Centric

ApplicationBundle
→ package closure

manifest
→ contratto machine-readable

materializer
→ filesystem autonomo

clean-room
→ nessuna dipendenza nascosta dal repo

provenance
→ commit e worktree verificabili
```

Questa è una capability Foundation reale, non un mock.

---

## Cosa manca per dichiararlo risultato 0.8.2

### 1. Rerun sul checkpoint corrente

Da clean committed tree:

```text
current release branch
→ simple producer
→ release validator
→ materializer
→ clean-room
```

### 2. Confronto v0.8.1 → 0.8.2

```text
page IDs
templates
assets
routes
capabilities
package tree
compatibility findings
```

### 3. Destination proof

Materializzare in una directory nuova e dimostrare:

```text
nessun source copy
nessuna backup
nessuna route debug
nessun legacy surface
avvio/risoluzione rappresentativa
```

### 4. Receipt

```yaml
foundationRelease:
sourceCommit:
sourceCommitOrigin: GIT_VERIFIED
worktreeState: CLEAN
applicationId: simple
manifestSha256:
packageDigest:
cleanRoom: PASS
releaseEligible: true
```

### 5. User-facing command

Non serve implementare tutta la CLI V1 per la 0.8.2.

Può bastare il comando già disponibile/documentato:

```bash
npm run distribution:produce -- simple
npm run distribution:materialize -- ...
npm run distribution:cleanroom -- ...
```

Oppure uno script bounded che orchestra i core esistenti.

La CLI futura li incapsulerà senza duplicarli.

---

## MAIN_AGENT RECOMMENDATION — F08-020

Dopo aver ratificato le deferral di release, farei del prossimo checkpoint:

```text
F08-020
Simple Distribution Release Proof

Nome da verificare col registry, non ancora canonico.
```

Obiettivo unico:

```text
current committed Foundation
→ Simple package
→ external destination
→ clean-room
→ compatibility matrix
→ release receipt
```

Niente Core Admin, profili, Operations o rendering redesign.

### Definition of Done

```text
□ clean committed tree
□ producer release-mode PASS
□ manifest validator PASS
□ 5 page IDs attesi
□ 4 template attesi
□ 5 asset attesi
□ no debug/test/legacy leakage
□ materialization PASS
□ external destination created atomically
□ clean-room PASS
□ repositoryObservations 0
□ v0.8.1 compatibility classified
□ protected kernel diff 0
□ receipt generated
```

### Valore

```text
tecnico       alto
architetturale molto alto
commerciale   ancora da validare
dimostrativo  molto alto
```

Per F., G. o un futuro interlocutore potrai dire una cosa concreta:

> La piattaforma è già capace di trasformare un'applicazione dichiarata nel repository in un package autonomo, verificato e riproducibile. Il prossimo lavoro non è dimostrare che il meccanismo funziona, ma applicarlo a un dominio reale e renderlo utilizzabile senza conoscere l'infrastruttura.

Quindi sì: una distribuzione Simple funzionante è già una milestone forte e probabilmente il miglior perimetro onesto per chiudere la 0.8.2.

---

## Provenance

```
Context 5: domanda se implementassimo sistema distribuzione attualmente avremmo distribuzione funzionante per Simple io direi che sarebbe già un risultato Sì E non sarebbe risultato piccolo sarebbe prima distribuzione Foundation realmente delimitata riproducibile verificabile Risposta breve ApplicationBundle Simple→producer→Distribution Manifest→validation→materialization→clean-room→package utilizzabile SÌ Questa pipeline esiste già tecnicamente ed è stata provata più volte OBSERVED evidenza già disponibile Nei checkpoint precedenti package simple ha prodotto 5 pagine 4 template 5 asset Con producer ACCEPT source provenance GIT_VERIFIED worktree CLEAN releaseEligible true manifest validator ACCEPT materialization exit 0 clean-room ok true repositoryObservations 0 Le modifiche successive hanno riguardato principalmente debug route gate Redis preview Core Admin ID Non dovrebbero modificare Simple ma questo va nuovamente provato sul checkpoint finale Cosa significa funzionante Dobbiamo distinguere tre livelli Livello 1 Package producibile simple source→manifest valido→package filesystem Già dimostrato Livello 2 Package autonomo e verificabile package→clean-room→route/page/template resolution→zero repository observation Già dimostrato nei checkpoint precedenti Livello 3 Prodotto installabile dall'utente opnx create/install→seleziona Foundation release→materializza in destination→verifica→avvia/deploy→receipt Questo non è ancora chiuso come esperienza CLI/prodotto Ma motore necessario al livello 3 esiste già Il risultato reale Non sarebbe abbiamo costruito tutto Open Nexus Sarebbe Foundation può produrre un'applicazione Simple come artifact autonomo validato e riproducibile senza che Runtime osservi il repository sorgente È esattamente dimostrazione di Foundation produce Execution esegue Perché Simple è target giusto Simple ha bundle delimitato page identity stabile template closure conosciuta asset closure conosciuta nessuna complessità Operations nessun profilo GATED/DEV_ONLY nessuna migration System package già provato minimal ≠ banale Cosa dimostra Repository-Centric→Artifact-Centric ApplicationBundle→package closure manifest→contratto machine-readable materializer→filesystem autonomo clean-room→nessuna dipendenza nascosta dal repo provenance→commit e worktree verificabili Questa è capability Foundation reale non un mock Cosa manca per dichiararlo risultato 0.8.2 1 Rerun sul checkpoint corrente Da clean committed tree current release branch→simple producer→release validator→materializer→clean-room 2 Confronto v0.8.1→0.8.2 page IDs templates assets routes capabilities package tree compatibility findings 3 Destination proof Materializzare in directory nuova e dimostrare nessun source copy nessun backup nessuna route debug nessun legacy surface avvio/risoluzione rappresentativa 4 Receipt YAML foundationRelease sourceCommit sourceCommitOrigin GIT_VERIFIED worktreeState CLEAN applicationId simple manifestSha256 packageDigest cleanRoom PASS releaseEligible true 5 User-facing command Non serve implementare tutta CLI V1 per 0.8.2 Può bastare comando già disponibile/documentato npm run distribution:produce -- simple npm run distribution:materialize -- ... npm run distribution:cleanroom -- ... Oppure script bounded che orchestra core esistenti CLI futura li incapsulerà senza duplicarli MAIN_AGENT RECOMMENDATION Dopo aver ratificato deferral di release farei del prossimo checkpoint F08-020 Simple Distribution Release Proof Nome da verificare col registry non ancora canonico Obiettivo unico current committed Foundation→Simple package→external destination→clean-room→compatibility matrix→release receipt Niente Core Admin profili Operations o rendering redesign Definition of Done checklist 12 items Valore tecnico alto architetturale molto alto commerciale ancora da validare dimostrativo molto alto Per F G o futuro interlocutore potrai dire cosa concreta La piattaforma è già capace di trasformare applicazione dichiarata nel repository in package autonomo verificato riproducibile Prossimo lavoro non è dimostrare che meccanismo funziona ma applicarlo a dominio reale e renderlo utilizzabile senza conoscere infrastruttura Quindi sì una distribuzione Simple funzionante è già milestone forte e probabilmente miglior perimetro onesto per chiudere 0.8.2
Status: CANDIDATE — awaits owner approval for F08-020 naming and execution
Extractor: documentation-agent v0.1.0
```
