# Contracts Report

> **Version:** `0.7.5.4C` · **Date:** 2026-09-24 · **Branch:** `master` @ `2d48d82` (`v0.7.5.4C`)
> **Scope:** snapshot of the contract + authority test surface of `open-nexus-foundation`.

---

## 1. Executive summary

| Metric | Value |
|---|---|
| Total suites | **24** (16 contracts + 8 authority-unit) |
| Total tests | **747** |
| Passing | **721 (96.5%)** |
| Failing | **26 — all pre-existing** |
| Contracts only (`tests/contracts`) | 16 files · **610 tests** · 584 pass · 26 fail |
| Authority-unit only (`src/test/unit`) | 8 files · **137 tests** · all pass |

The 26 failures are pre-existing: verified by stashing the `0.7.5.4C` working tree and
re-running the identical suite at clean HEAD `b0c9d40` (same 26 failures across the
same 5 files). They are concentrated on open-nexus / core-admin expectations and are
unrelated to the Simple bundle work.

## 2. Contract suites

| Suite | Contract focus | Tests | Result |
|---|---|---:|---|
| `application-contract.test.ts` | L1 ApplicationDefinition + L2 Nav ↔ Discovery | 69 | 1 fail |
| `application-smoke.test.ts` | E2E pipeline per app (canary) | 39 | green |
| `application-catalog.test.ts` | Bundle → Artifacts → Catalog | 79 | 5 fail |
| `discovery-resolution.test.ts` | L3 VirtualProvider → PageRecord | 102 | 2 fail |
| `data-normalization.test.ts` | L4 PageRecord → PageData | 167 | 1 fail |
| `template-rendering.test.tsx` | L5/L6 template + widget sections | 28 | 17 fail |
| `identity-projection.test.ts` | Experience identity projection | 13 | green |
| `experience-projection.test.ts` | Experience projection | 14 | green |
| `narrative-links.test.ts` | Narrative / link integrity | 17 | green |
| `auth-experience-alignment.test.tsx` | Auth experience alignment | 26 | green |
| `auth-experience-stabilization.test.ts` | Auth stabilization | 20 | green |
| `explorer-infrastructure-extraction.test.ts` | Explorer infra boundary | 17 | green |
| `dashboard-registry-contract.test.ts` | Dashboard registry | 5 | green |
| `artifact-consumption-closure.test.ts` | AF-001 guards B-01/B-02/B-03 | 7 | green |
| `page-co-location.test.ts` | 0.7.5.4 page co-location | 3 | green |
| `bundle-nav-self-contained.test.ts` | 0.7.5.4C nav self-containment | 4 | green |

## 3. Authority-unit suites

| Suite | Guards | Tests | Result |
|---|---|---:|---|
| `presentation-authority.test.tsx` | ADR-0013 scope + simple R4/R5 | 39 | green |
| `theme-authority.test.tsx` | ADR-0011 theme | 12 | green |
| `primitive-authority.test.tsx` | ADR-0012 primitive | 21 | green |
| `design-enforcement.test.ts` | ADR-0010 design | 22 | green |
| `design-authority-boundary.test.ts` | Design boundary | 15 | green |
| `theme-authority-boundary.test.ts` | Theme boundary | 10 | green |
| `primitive-authority-boundary.test.ts` | Primitive boundary | 15 | green |
| `ops02b-props-flow.test.ts` | OPS-02B props flow | 3 | green |

## 4. Open failures — root cause and scope

| Suite | Failing | Expected → Actual | Root cause |
|---|---:|---|---|
| template-rendering | 17 | `pageDataMap.get('nexus-*')` undefined | registry id rename (`nexus-home`…`nexus-library` no longer keyed) |
| application-catalog | 5 | shared consumers; core-admin title `OpenFav Admin` | shared metadata / domain-authority drift |
| discovery-resolution | 2 | `open-nexus/library` PROTECTED; correct templates | policy + template drift |
| data-normalization | 1 | `open-nexus/library` PROTECTED | policy drift |
| application-contract | 1 | afterLogin `open-nexus/library` → config `open-nexus/index` | stale assertion |

All 26 target open-nexus / core-admin contracts — stale expectations vs current
config. None touch the Simple bundle.

## 5. Coverage model

```text
L1  ApplicationDefinition structure
L1b Navigation integrity
L2  Navigation ↔ Discovery
L3  Discovery Resolution (VirtualProvider → PageRecord)
L4  Data Normalization (PageRecord → PageData)
L5  Template Rendering
L6  Widget Section contracts

BundleCollector → Catalog / Report / Manifest → artifact-consumption-closure
Authorities Design / Theme / Primitive / Presentation → boundary unit suites
Co-location + Nav self-contained → bundle invariants
```

## 6. What the contracts protect

- L1–L6 pipeline: ApplicationDefinition → PageRegistry → VirtualProvider → PageRecord
  → PageData → Template → Sections; `application-smoke` is the E2E canary.
- Artifact boundary AF-001: type-projection parity and no BundleCollector invoked
  through the navigation path.
- Authority boundaries: Design / Theme / Primitive / Presentation disjoint scopes.
- Bundle invariants: page co-location and navigation self-containment.

## 7. Recommendations from the report

1. Dedicated `0.7.5.5` contract-alignment task to reconcile the 26 stale
   open-nexus/core-admin expectations.
2. CI gate: contracts + authority-unit green before tagging; 26 reds mask regressions.
3. Align the 10 remaining global broken references using the same fix pattern applied
   to the Simple bundle in `0.7.5.4C`.

## Appendix — method

```text
npx vitest run tests/contracts src/test/unit
→ 747 tests / 24 files

baseline probe:
git stash push -u + re-run at b0c9d40
→ identical 26 failures

npx tsc --noEmit
→ 52 pre-existing errors unchanged; 0 in touched files
```

---

*Source captured from the user-provided report on 2026-09-24. Operational impact:
`frontend/backlog/FE-001` updated to make 0.7.5.5 alignment the gate before the 0.8
minimal baseline.*
