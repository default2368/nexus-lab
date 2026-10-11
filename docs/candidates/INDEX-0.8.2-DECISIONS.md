# Index — 0.8.2 Decisions — Stato aggiornato 2026-10-11

**Status:** INDEX — living document
**Source:** Context 1-8 + owner approvals
**Last update:** 2026-10-11

---

## Decisioni owner registrate

| ID | Titolo | Status | File |
|---|---|---|---|
| NX-D-045 | Closure Strategy patch release non framework | PARTIALLY APPROVED — D1 approved, D2 pending | DECISION-0.8.2-CLOSURE-STRATEGY.md |
| NX-D-045-D1 | Release target simple, Core Admin excluded | APPROVED | DECISION-0.8.2-RELEASE-TARGET-OWNER-APPROVED.md + DIRECTIVE-ARENA-0.8.2-OWNER-DECISIONS-RECORDED.md |
| NX-D-045-D2 | rendering.kind explicit | OWNER_DECISION_PENDING — A DEFERRED_WITH_OWNER_DECISION raccomandato | DECISION-0.8.2-D2-RENDERING-KIND.md |
| NX-D-045-D1-EXPL | Perché non implementiamo Distribution Profile framework etc | APPROVED EXPLANATION | EXPLANATION-0.8.2-CORE-ADMIN-PACKAGE-DISTRIBUTION.md |
| NX-D-045-F08-020 | Simple Distribution Release Proof | CANDIDATE — MAIN_AGENT RECOMMENDATION | DECISION-0.8.2-SIMPLE-DISTRIBUTION-PROOF-F08-020.md |
| NX-D-045-IMPL | Simple come fabbrica — implicazioni | CANDIDATE ANALYSIS | IMPLICATIONS-0.8.2-SIMPLE-DISTRIBUTION-FACTORY.md |
| NX-D-046 | Foundation Bootstrap / Self-Hosting | APPROVED ARCHITECTURAL DIRECTION IMPLEMENTATION DEFERRED | STRATEGY-FOUNDATION-BOOTSTRAP-SELF-HOSTING.md |
| NX-D-045-RELEASE | Release statement candidate | CANDIDATE | DECISION-0.8.2-RELEASE-STATEMENT-CANDIDATE.md |

---

## Cosa è approvato

```text
Foundation 0.8.2 release package target → simple
Core Admin package → CORE_ADMIN_PACKAGE_OUT_OF_0_8_2_RELEASE_SCOPE
Do not implement in 0.8.2: Distribution Profile framework, manifest profile fields, producer filtering, validator profile rules, Core Admin fixtures, Core Admin materialization/clean-room as release evidence, version transition Core Admin, rendering.kind, manifest schema change, producer/validator/materializer/Admin read model/frontend profile behavior change, delete core-admin ApplicationBundle/source application
Future direction: rebuild approved Operations experience using existing primitives/contracts, migrate useful behavior, retire current core-admin identity only after consumer and parity gates (8 checklist)
Diagnostic 8-page Core Admin package remains PROFILE_UNAPPROVED NOT RELEASE EVIDENCE
F08-006 Phase A explicit IDs remain approved as current source-authority hygiene
```

## Cosa è pending

```text
D2 rendering.kind — A DEFERRED_WITH_OWNER_DECISION vs B mandatory 0.8.2 gate — raccomandazione A
F08-020 naming — da verificare col registry
Release statement wording finale — owner final wording
Diagnostic API policy classification — must close before release: /api/v1/redis/test→PRODUCTION_DENY, /api/redis→DEVELOPMENT_ONLY, /api/v1/redis/pages→AUTH_REQUIRED, /api/v2/discovery→intentionally public, debug/refresh/mutating→AUTH_REQUIRED, sys/system-control→owner/policy review — non blanket gate INTENTIONALLY_PUBLIC/AUTH_REQUIRED/PRODUCTION_DENY/DEVELOPMENT_ONLY/UNKNOWN
```

## Must close prima release

```text
anonymous diagnostic/API production policy
ID compatibility record Phase A
backup/snapshot disposition
simple package full pipeline F08-020
0.8.1→0.8.2 compatibility matrix
full-suite current rerun
build/typecheck/security guard
release notes/version/tag
branch/stash hygiene
```

## Can defer con record esplicito

```text
indexV1 unique behavior
/debug page ownership migration
Hello API retirement
Redis Console retirement/extraction
Hub
about-legacy
Template Lab ownership
System/API Control migration
WowPageTemplate external-consumer uncertainty
package-wide template catalog
Condition: not in simple package or production-gated or explicit disposition/owner/follow-up
```

## Cosa rilascia 0.8.2

```text
Foundation source convergence
security hardening
registry convergence
provenance GIT_VERIFIED CLEAN
simple package bounded 5 pages 4 template 5 asset
manifest machine-readable
materialization filesystem autonomo
clean-room repositoryObservations 0
0.8.1 compatibility
```

Non rilascia:

```text
Core Admin package
Operations V1
Distribution Profile framework
new rendering contract
all legacy source removed (FALSE)
all template consumers known
backups globally zero if deferred
```

## Release statement candidate

> Foundation 0.8.2 consolida la convergenza di authority e sicurezza necessaria a produrre un package Simple bounded, riproducibile e verificato in clean-room, mantenendo espliciti e non distribuiti i residual source non ancora migrati.

## Implicazioni strategiche

- **Factory:** repository→authoring/compiler/governance, package→prodotto distribuibile, Execution→runtime sottile, Domain Pack→differenzia verticali — repo può essere complesso prodotto pulito — Repository-Centric→Artifact-Centric
- **N settori:** stessa macchina output differenti — Simple Domain Pack→Simple app, G→Audit Engagement, A→Operation Reconstruction, F→Project Evidence — verticale non fork-a Foundation
- **Distribuzione vs hosting:** Foundation produce artifact firmato/versionato, cliente esegue locale/cloud/on-premise, dati restano perimetro cliente — interessante per enti pubblici, audit, dati regolati, sovranità
- **Moat:** Execution Shell riproducibile 80%, moat in Foundation compiler/control plane — contracts, authority, BundleCollector, profile resolution, validation, compatibility, materialization, provenance, receipts, migration findings — codebase pulita→output copiabile, meccanismo che rigenera→capability, meccanismo che rigenera sé stesso→candidate moat molto forte
- **Brain:** authoring assistant non prodotto finale — docs→Brain interpreta→Candidate Domain Definition→umano corregge→Domain Pack approvato→Foundation produce→Execution esegue — AI entra una volta
- **Bootstrap:** factory può usare proprio processo per rifondare sé stessa — 2 strade: 1) nuova app pulita che consuma Foundation (consumer pulito, migliore) 2) nuova Foundation bootstrap F0→F1→F2 self-hosting fixed-point test semantic inventory A=B — quando rumore storico supera valore operativo non pulisci infinito materializzi nuova baseline
- **Sequence:** 0.8.2 Simple Proof → 0.9 Semantic Entity → second app Domain Pack N-sectors → Workspace/ApplicationSpec → CLI workspace create → Foundation Bootstrap experiment → equivalence gate

## Documenti aggiornati 2026-10-11

- DECISION-0.8.2-CLOSURE-STRATEGY.md — amendment D1 approved D2 pending factory bootstrap
- PROGRAM-BACKLOG-GENERALE.md — Foundation P0 updated simple target Core Admin excluded diagnostic API policy F08-020 DoD release statement, CLI P2 updated workspace create bootstrap sequence
- GIT-BOUNDARIES-AND-GATES.md — operational gates updated diagnostic API classification F08-020 bootstrap moat
- GOVERNED-EVIDENCE-DOSSIER.md — addendum factory + bootstrap + moat + CLI + N-sectors

## Documenti non necessitano aggiornamento

- 06-SCREENSHOT-STORYBOARD.md — storyboard 6 screenshot reali ancora valido
- ECOSYSTEM-GOVERNANCE-PROPOSAL.md — parked, non blocking, ma potrebbe ricevere addendum workspace create in futuro — per ora ok
- F-ONE-PAGE-A5.md, 01-05 briefs — plico F dispensa 8-12 pagine — separato da 0.8.2, non impattato
- NOTE-F.md, TECHNICAL-NOTE-F.md — note personali F — non impattate

## Prossimi passi raccomandati Main Agent

1. Owner approval D2 rendering.kind A DEFERRED
2. Diagnostic API Policy Closure — classificare /api/v1/redis/test etc + owner boundaries LEGACY_REFERENCE_REVIEW
3. Backup/snapshot inventory disposition
4. F08-020 Simple Distribution Release Proof rerun su checkpoint corrente clean committed tree
5. Compatibility matrix v0.8.1→0.8.2
6. Release notes/version/tag
7. PR finale owner merge → tag v0.8.2

Dopo 0.8.2:
- 0.9 Semantic Entity Projection
- Second app Domain Pack N-sectors proof (G candidato naturale)
- Workspace/ApplicationSpec machine-readable
- CLI workspace create
- Foundation Bootstrap experiment

---

## Provenance

```
Context 1-8 owner decisions: D1 simple target approved, Core Admin excluded, 7 points not implemented explanation, D2 rendering.kind pending A recommended, diagnostic API policy classification, simple distribution proof F08-020, factory implications, bootstrap self-hosting moat, release statement candidate
Updated docs: DECISION-0.8.2-CLOSURE-STRATEGY amendment, PROGRAM-BACKLOG-GENERALE, GIT-BOUNDARIES-AND-GATES, GOVERNED-EVIDENCE-DOSSIER addendum
New docs: DECISION-0.8.2-RELEASE-TARGET-OWNER-APPROVED, DIRECTIVE-ARENA-0.8.2-OWNER-DECISIONS-RECORDED, EXPLANATION-0.8.2-CORE-ADMIN-PACKAGE-DISTRIBUTION, DECISION-0.8.2-D2-RENDERING-KIND, DECISION-0.8.2-SIMPLE-DISTRIBUTION-PROOF-F08-020, IMPLICATIONS-0.8.2-SIMPLE-DISTRIBUTION-FACTORY, STRATEGY-FOUNDATION-BOOTSTRAP-SELF-HOSTING, DECISION-0.8.2-RELEASE-STATEMENT-CANDIDATE
Status: INDEX living document
Extractor: documentation-agent v0.1.0
Date: 2026-10-11
```
