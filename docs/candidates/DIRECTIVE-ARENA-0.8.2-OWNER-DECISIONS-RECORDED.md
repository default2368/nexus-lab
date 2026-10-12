# DIRETTIVA PER ARENA — OWNER DECISION RECORDED — 0.8.2

**Status:** APPROVED DIRECTIVE
**DecisionId:** NX-D-045-DIRECTIVE
**Source:** Context 3 + Context 4 + Context 5 + Owner approval
**Date:** 2026-10-09
**Extractor:** documentation-agent v0.1.0

---

## OWNER DECISION RECORDED

```text
Foundation 0.8.2 release package target:
→ simple

Core Admin package:
→ CORE_ADMIN_PACKAGE_OUT_OF_0_8_2_RELEASE_SCOPE

Do not implement a Core Admin Distribution Profile in 0.8.2.
Do not modify manifest schema, producer, validator, materializer, Admin read model or frontend profile behavior.

Do not delete or retire the core-admin ApplicationBundle/source application in 0.8.2.

Future direction:
rebuild the approved Operations experience using existing primitives/contracts,
migrate useful behavior, then retire the current core-admin identity only after
consumer and parity gates.

The diagnostic eight-page Core Admin package remains PROFILE_UNAPPROVED and is not
release evidence.

The F08-006 Phase A explicit IDs remain approved as current source-authority hygiene.
```

---

## Cosa significa per Arena

### Must NOT in 0.8.2

```yaml
must_not:
  - implement Distribution Profile framework
  - add manifest profile fields (profileId, profileVersion, resolvedPageIds, profileConformant, profileFindings)
  - implement producer filtering (--include-page / --exclude-page manual authority)
  - implement validator profile rules
  - create Core Admin package fixtures (ordinary.valid.json, gated-reference.valid.json, development.valid.json, mismatch.invalid.json)
  - run materialization/clean-room on 8-page Core Admin diagnostic package as release evidence
  - declare package version transition Core Admin 0.8.0→0.8.2
  - modify manifest schema
  - modify producer
  - modify validator
  - modify materializer
  - modify Admin read model
  - modify frontend profile behavior
  - delete or retire core-admin ApplicationBundle/source application
  - implement rendering.kind (D2 deferred)
```

### Must DO — cosa continuiamo a fare su Core Admin

```text
mantenere il source runtime
correggere identity authority (Phase A explicit IDs)
chiudere security finding (diagnostic API policy)
inventariare backup/snapshot disposition
mantenere navigazione e route compatibility
classificare pagine (produzione vs reference gated vs development vs migration/retirement candidate vs legacy)
preservare behavior utile
preparare Operations sull'host approvato
ritirare legacy quando esiste parity
```

Il commit degli ID espliciti resta importante:

```text
source authority
→ corretta

package release
→ differita
```

### Cosa rilascia 0.8.2

```text
Foundation source convergence
security hardening (diagnostic API policy closure)
registry convergence
provenance (GIT_VERIFIED, CLEAN worktree)
simple package
manifest
materialization
clean-room
0.8.1 compatibility
```

Non rilascia:

```text
Core Admin package
Operations V1
Distribution Profile framework
new rendering contract
```

In una frase:

> Non stiamo rinunciando a distribuire Operations. Stiamo evitando di formalizzare e testare come package una versione legacy mentre abbiamo già deciso che sarà più semplice ricostruirla con le primitive e i contratti attuali.

---

## D2 — rendering.kind — OWNER_DECISION_PENDING

Resta D2:

```text
explicit rendering.kind
```

Raccomandazione Main Agent:

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

Raccomandazione resta A — defer.

---

## Provenance

```
Context 3 directive + Context 4 continuation + Context 5 continuation classificare pagine preservare behavior utile preparare Operations ritirare legacy quando esiste parity commit ID espliciti source authority corretta package release differita Cosa rilascia 0.8.2 Foundation source convergence security hardening registry convergence provenance simple package manifest materialization clean-room 0.8.1 compatibility Non rilascia Core Admin package Operations V1 Distribution Profile framework new rendering contract In una frase Non stiamo rinunciando a distribuire Operations Stiamo evitando di formalizzare e testare come package una versione legacy mentre abbiamo già deciso che sarà più semplice ricostruirla con le primitive e i contratti attuali
Status: APPROVED DIRECTIVE
Extractor: documentation-agent v0.1.0
```
