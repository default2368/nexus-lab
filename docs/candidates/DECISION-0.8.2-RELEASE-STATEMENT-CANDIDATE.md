# Release Statement Candidate — 0.8.2

**Status:** CANDIDATE — requires owner final wording
**DecisionId:** NX-D-045-RELEASE-STATEMENT
**Source:** Context 5 + Context 6 + Context 7 + Context 8
**Date:** 2026-10-09

---

## Statement approvato come direzione

> Foundation 0.8.2 consolida la convergenza di authority e sicurezza necessaria a produrre un package Simple bounded, riproducibile e verificato in clean-room, mantenendo espliciti e non distribuiti i residual source non ancora migrati.

---

## Cosa rilascia 0.8.2 — versione estesa

```text
Foundation source convergence
security hardening (diagnostic API policy closure)
registry convergence
provenance (GIT_VERIFIED, CLEAN worktree)
simple package — 5 pages, 4 templates, 5 assets — bounded
manifest — contratto machine-readable
materialization — filesystem autonomo
clean-room — nessuna dipendenza nascosta dal repo, repositoryObservations 0
0.8.1 compatibility — matrix classificata
```

## Non rilascia — Non-claim espliciti

```text
Core Admin package — CORE_ADMIN_PACKAGE_OUT_OF_0_8_2_RELEASE_SCOPE
Operations V1
Distribution Profile framework
new rendering contract (rendering.kind)
all legacy source removed — FALSE, residuals governati e non distribuiti
all template consumers known — not claimed
backups globally zero — only if disposition explicit, otherwise deferred
```

## Release scope onesto

Forse la release non deve promettere:

```text
Abbiamo eliminato ogni superficie legacy dal repository.
```

Può promettere:

```text
Possiamo produrre un'applicazione Simple pulita e autonoma da una Foundation governata,
con provenienza verificabile e senza leakage delle superfici non approvate.
```

È una promessa:

```text
più piccola
verificabile
utile
coerente con una patch release
direttamente propedeutica alla 0.9
```

---

## Repository vs prodotto — distinzione chiave

```text
Repository-Centric
→ Artifact-Centric

source convergence
→ importante per mantenibilità

package allowlisting
→ importante per il cliente

le due cose
→ correlate ma non identiche
```

Il repository può ancora contenere:

```text
reference experience
Template Lab
test page
compatibility surface
sorgenti legacy governate
strumenti di sviluppo
```

Se il package Simple contiene soltanto:

```text
pagine approvate
template necessari
asset necessari
capability necessarie
manifest verificato
```

allora il prodotto distribuito è pulito.

La release può essere onesta se dichiara:

```text
current source residuals
→ governati e non distribuiti

consumer artifact
→ pulito, bounded, verificato
```

---

## Simple come Hello World industriale

Simple non è importante per il suo dominio.

È importante perché dimostra:

```text
il compiler funziona
il package è bounded
il runtime non vede il repository
il consumer può esistere fuori dalla fabbrica
```

Dopo Simple, il test successivo non è un package più grande.

È:

```text
stessa pipeline
→ Domain Pack differente
→ experience differente
→ zero kernel fork
```

G. è il candidato naturale.

---

## Foundation come fabbrica

Se questa catena funziona:

```text
ApplicationBundle Simple
→ Foundation
→ manifest
→ package autonomo
→ clean-room
→ Execution
```

allora:

> Open Nexus è già una fabbrica di applicazioni distribuibili.

```text
repository
→ ambiente di authoring, compiler e governance
package
→ prodotto distribuibile
Execution
→ runtime sottile
ApplicationBundle / Domain Pack
→ ciò che differenzia i verticali
```

Implicazione commerciale:

```text
la vendita non deve essere per forza accesso mensile a una web app
Può essere:
build verificata
release Foundation
Domain Pack
deployment
aggiornamento
compatibility/migration
governance tier
supporto/hosting opzionale
```

Non scegliamo oggi il business model, ma l'architettura mantiene aperte più possibilità.

---

## Provenance

```
Context 5+6 release statement candidate Foundation 0.8.2 consolida convergenza di authority e sicurezza necessaria a produrre package Simple bounded riproducibile verificato in clean-room mantenendo espliciti e non distribuiti residual source non ancora migrati + distinzione repository complesso prodotto pulito + Simple Hello World modello industriale + Foundation fabbrica
Status: CANDIDATE
```
