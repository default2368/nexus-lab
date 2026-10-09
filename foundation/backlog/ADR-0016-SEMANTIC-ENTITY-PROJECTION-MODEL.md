# ADR-0016 — Semantic Entity Projection Model

**Status:** PROPOSED — owner approval required
**Date:** 2026-09-20
**Target:** Open Nexus Foundation 0.9.0

## Context

Open Nexus Runtime esegue il modello:

```text
Application → Page → PageData → Runtime
```

I casi G. e Admin richiedono la rappresentazione di conoscenza non riducibile ad
Application o Page:

```text
Procedure · Audit · Engagement · Evidence · Feedback · Decision
Application · PageRecord come oggetti ispezionabili
```

Forzare questi oggetti dentro Runtime, ApplicationContext, Discovery o PageData
verticalizzerebbe Foundation.

## Decision

1. `PageData` resta l’unico contratto consumato dal Runtime.
2. Le entità di dominio vivono fuori dal Runtime.
3. `EntityRecord` e `RelationshipRecord` sono Semantic Contracts sperimentali.
4. Gli attributi specifici appartengono ai Domain Pack.
5. `EntityProvider` recupera entità e relazioni; non proietta e non autorizza.
6. `EntityProjector` è puro e converte un graph slice autorizzato in
   `EntityViewArtifact`.
7. Un adapter converte `EntityViewArtifact` in `PageData`.
8. `Application` resta execution/experience boundary. Può essere proiettata come
   entità nell’Admin, ma non viene ridotta a `EntityRecord`.
9. La 0.9 usa materializzazione build-time. Nessun provider Discovery semantico.
10. Brain/AI non partecipano alla pipeline 0.9.

## Boundary

```text
EntityRecord + EntityGraphSlice
+ ProjectionContext + EntityViewProfile
        ↓
EntityProjector
        ↓
EntityViewArtifact
        ↓
PageData Adapter
        ↓
PageData
        ↓
Runtime invariato
```

## Protected Contracts

La decisione vieta modifiche opportunistiche a:

```text
Runtime
PageController
DiscoveryService / DiscoveryServiceV2
ApplicationContext
ApplicationDefinition
PageData
normalizeToPageData
BundleCollector
```

Qualunque necessità di modificarli richiede una nuova Foundation RFC.

## Ownership

```text
Domain Pack          schema e significato delle entità verticali
Entity Provider      accesso read-only a entità/relazioni
Policy Gate          grant già risolto
ProjectionContext    condizioni della proiezione
View Profile         forma richiesta
Projector            trasformazione pura
View Artifact        rappresentazione intermedia
PageData Adapter     confine col Runtime
Runtime              rendering, nessuna conoscenza delle entità
```

## Actions

Card e artifact possono esporre action descriptor, ma non modificano entità.

```text
UI action → Domain Command → Policy → Preview/Approval
→ Authoring Core → source state → nuova projection
```

`remove from view`, `edit entity`, `clone entity`, `archive` e `delete` sono azioni
distinte.

## CodeEntity

`CodeEntity` è un’estensione sperimentale e non bloccante:

```text
EntityReference.id   identità tecnica immutabile
CodeEntity.code      identificatore business governato
```

Il code può produrre route alias leggibili, ma non sostituisce il registry ID
canonico. Promozione soltanto dopo due casi indipendenti.

## Consequences

### Positive

- nuovi domini senza modifica Runtime;
- stesse entità proiettate per ruoli differenti;
- provenance e validità temporale preservate;
- Domain Pack sostituibili;
- possibilità futura di Brain/Graph senza coupling al Kernel.

### Negative

- nuovi contratti da governare;
- artifact intermedio aggiuntivo;
- rischio di astrazione prematura;
- necessità di conformance suite e secondo consumer.

## Non-Decisions

```text
Graph database
storage definitivo
AI provider
proiezione request-time
Entity Discovery provider
GenericEntityPage
CRUD completo
field-level authorization dinamica
naming commerciale
```

## Acceptance

L’ADR passa ad `ACCEPTED` soltanto se:

```text
1. Procedure/Audit producono PageData senza Runtime changes
2. stessa Entity produce due viste per ruolo
3. Application/Page funzionano come secondo consumer
4. projectors sono puri e deterministici
5. provenance e validità temporale sopravvivono
6. nessun branch entity-specific entra nel Kernel
7. due consumer confermano il minimo comune
```

Se funziona soltanto per il G Domain Pack, resta `EXPERIMENTAL`.
