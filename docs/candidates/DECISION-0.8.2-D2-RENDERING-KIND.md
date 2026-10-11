# DECISION — 0.8.2 D2 rendering.kind — OWNER DECISION PENDING

**Status:** OWNER_DECISION_PENDING
**DecisionId:** NX-D-045-D2
**HandoffId:** 0.8.2-rendering-kind
**Source:** Context 3 + Main Agent recommendation + Context 1 D2
**ConversationRef:**
  conversationId: arena/86a8bf50-nexus-lab
  turnRange: 2026-10-09T21:00-21:30
  date: 2026-10-09
  extractor: documentation-agent v0.1.0
  targetDocument: docs/candidates/DECISION-0.8.2-D2-RENDERING-KIND.md
  approvalStatus: PENDING

---

## Prossima owner decision — Resta D2

```text
explicit rendering.kind
```

### Raccomandazione Main Agent

```text
A. DEFERRED_WITH_OWNER_DECISION
→ non entra nella 0.8.2
→ current 0.8 manifest contract invariato
→ PHYSICAL/rendering redesign post-0.8.2
```

Alternativa:

```text
B. mandatory 0.8.2 gate
→ richiede schema/producer/validator/materializer changes
→ allarga la release
```

La mia raccomandazione resta A — defer.

---

## Analisi

### Cosa è rendering.kind

Dalla Context 1: rendering model — contract current valido:

```text
templateRef
policy
ownerBundle
route
```

Proposta rendering.kind sarebbe nuovo campo esplicito che evolve rendering contract — non presente in Distribution 0.8 contract, 0.8.1 rilasciata senza.

### Perché defer

1. **Allarga public contract:** Manifest schema è contratto pubblico/versionato. Aggiungere rendering.kind ora modifica producer, validator, materializer, Admin read model.

2. **Non necessario per simple:** simple package target già dimostrato in 0.8.1 con contratto attuale templateRef/policy/ownerBundle/route. Non blocca 0.8.2 patch release security + authority convergence + distribution reproducibility.

3. **Coerente con D1:** Core Admin package escluso, quindi non serve evolvere rendering model per chiudere 0.8.2.

4. **PHYSICAL finding esplicito:** La finding PHYSICAL / rendering redesign rimane explicit e post-0.8.2 — non falsamente marcata done.

### Cosa significa A

```yaml
renderingKind:
  status: DEFERRED_WITH_OWNER_DECISION
  in_0_8_2: false
  current_contract_valid: [templateRef, policy, ownerBundle, route]
  finding: PHYSICAL remains explicit post-0.8.2
  impact_if_B: [schema, producer, validator, materializer, admin-read-model, frontend]
```

### Cosa significa B

```yaml
renderingKind:
  status: MANDATORY_0_8_2_GATE
  in_0_8_2: true
  requires: [schema-change, producer-filtering, validator-rules, materializer-evolution, admin-read-model, compatibility-matrix-extension]
  risk: allarga release oltre patch scope, confligge con EPIC §18 aspirazionale
```

### Raccomandazione documentata

- **A** — DEFERRED_WITH_OWNER_DECISION
- Non entra in 0.8.2
- Current 0.8 manifest contract invariato
- PHYSICAL/rendering redesign post-0.8.2 con owner decision separata

---

## Dipendenze

- D1 approvato: simple target, Core Admin excluded → D2 defer coerente
- D3 fallback IDs: HISTORICAL_DERIVED_DIAGNOSTIC_IDS → non impatta rendering.kind
- D4 Operations V1 deferred → rendering redesign post-0.8.2 può essere valutato con Operations V1

---

## Owner decision richiesta

```
[ ] A. DEFERRED_WITH_OWNER_DECISION — non entra in 0.8.2 (raccomandato Main Agent)
[ ] B. mandatory 0.8.2 gate — richiede schema/producer/validator/materializer changes
```

---

## Provenance

```
Context 1 D2: rendering.kind DEFERRED_WITH_OWNER_DECISION resto valido templateRef/policy/ownerBundle/route — reason new evolution rendering contract not present in Distribution 0.8 contract 0.8.1 released without introducing now would enlarge public contract — finding PHYSICAL remains explicit post-0.8.2
Context 2 YAML: renderingKind deferred recommended
Context 3: Prossima owner decision Resta D2 explicit rendering.kind Raccomandazione Main Agent A DEFERRED_WITH_OWNER_DECISION non entra nella 0.8.2 current 0.8 manifest contract invariato PHYSICAL/rendering redesign post-0.8.2 Alternativa B mandatory 0.8.2 gate richiede schema/producer/validator/materializer changes allarga la release — raccomandazione resta A defer
Checkpoint: Branch arena/46e97d6d-open-nexus-foundation HEAD 2324a96 — SURF-082-004 IN_ANALYSIS
Status: OWNER_DECISION_PENDING
Extractor: documentation-agent v0.1.0
```
