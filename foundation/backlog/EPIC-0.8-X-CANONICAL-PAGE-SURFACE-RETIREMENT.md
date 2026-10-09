# EPIC 0.8.x — Canonical Page Surface Convergence and Retirement

```text
Status:                  APPROVED DIRECTION
Mutating authorization:  NOT YET GRANTED
Release:                 Foundation 0.8.2 — Surface Convergence and Hygiene
Predecessor:             Foundation 0.8.1 — Distribution Green Line
Program:                 Foundation Completion / Distribution Readiness
```

---

## 1. Decision

After the Foundation 0.8 authority, Page Contract, policy, compatibility and ESSENTIAL
set audits, page surfaces are converged through evidence-backed keep, migration,
isolation and retirement decisions.

This Epic is not a mass deletion.

```text
Audit
→ classify
→ identify authority
→ preserve valuable behavior
→ migrate application ownership when required
→ retire only the superseded surface
→ verify parity
```

Central rule:

> Every active application page must have one explicit identity, one owning
> ApplicationBundle, one canonical declaration and a demonstrated reason to enter a
> distribution package.

Release sequencing decision:

```text
0.8.1
→ freezes and proves the artifact-centric distribution baseline, including the
  documented legacy/reference noise that remains in the Foundation source tree

0.8.2
→ removes or migrates retired/deprecated source surfaces while preserving the 0.8.1
  distribution contract and upgrade path
```

0.8.2 does not retroactively redefine the 0.8.1 package. It proves that future
codebases can be generated from the clean surface without breaking projects produced
from the 0.8.1 line.

---

## 2. Critical distinction: behavior is not page identity

A legacy or misplaced page can contain behavior that must survive.

```text
legacy page identity
≠
legacy behavior
```

Possible result:

```text
preserve capability/behavior
+
migrate ownership and presentation
+
retire old page ID only after parity
```

No page is deleted because its current application is named `system`, `core-admin`,
`test`, `legacy` or `debug`.

---

## 3. Known owner direction — System Control / API Control

The current System control/API surface is not a deletion candidate.

Reported migration direction:

```text
current System control/API page
→ Operations application
→ Operations V1 replacement
```

The exact technical IDs and routes must be verified in the repository. The program
must not infer a rename from the visible title.

Candidate current source:

```text
sys/system-control
```

Target responsibility:

```text
Operations-owned application experience
```

Long-term target:

```text
Operations V1
```

Required treatment:

```text
classification: REFERENCE or EXPERIMENTAL, according to current evidence
role: OPERATIONS
migration: MIGRATE_TO_OPERATIONS_V1
retirement: old identity only, after functional parity
```

Before retiring the current System page:

```text
□ all API/control functions inventoried
□ behavior owner identified
□ data sources and permissions identified
□ Operations V1 target page exists
□ navigation and route parity verified
□ health/control actions preserved
□ role/access policy preserved or intentionally changed
□ no consumer remains on the old ID
□ redirect/alias decision recorded
□ visual and functional parity evidence produced
```

If the control behavior is reusable beyond Operations, it may become a Foundation
Capability. Operations still owns page identity, routing, navigation and composition.

### 3.1 Ratified Operations target surface

The current technical application ID `core-admin` is accepted as the 0.8 Operations
ApplicationBundle while its identity/naming is reviewed for Operations V1.

```text
core-admin technical ID
→ currently owns and exposes Operations pages
→ compliant with the Bundle Page ownership direction
→ rename/replacement deferred to Operations V1
```

The approved target Operations surface is restricted to four responsibilities:

```text
1. Operations index
   application table / application overview
   current candidate: core-admin/index

2. Operations discovery
   page inventory and page inspection entry
   current candidate: core-admin/discovery-pages

3. Template Lab
   migrate from the System surface into Operations
   current source candidate: sys/template-lab
   target technical ID: to be decided from repository evidence

4. API / System Control
   preserve control behavior and migrate into Operations
   current source candidate: sys/system-control
   target technical ID: to be decided from repository evidence
```

All other current `core-admin`, `system`, `hub`, recovery and physical-debug surfaces
are excluded from the approved production Operations target unless a parity audit
demonstrates a behavior that must be migrated into one of the four responsibilities
above. `core-admin/component-catalog` is the explicit exception: it remains a gated
REFERENCE/DEVELOPER discovery surface and is not part of the ordinary consumer package.

Candidate dispositions:

| Current surface | Owner direction |
|---|---|
| `core-admin/index` | `KEEP` as current Operations index |
| `core-admin/discovery-pages` | `KEEP` as Operations page/discovery surface |
| `sys/template-lab` | `MIGRATE_TO_APPLICATION` → Operations |
| `sys/system-control` | `MIGRATE_TO_OPERATIONS_V1`; preserve API/control behavior |
| `physical/debug/debug-auth` | `REMOVE_REFERENCE`; retire after consumer check |
| `core-admin/pages` | `RETIRE_OR_ALIAS_REMOVE`, subject to parity with discovery-pages |
| `core-admin/control-center` | `RETIRE_OR_MIGRATE_BEHAVIOR`, subject to API-control parity |
| `core-admin/component-catalog` | `KEEP_REFERENCE_DISCOVERY`; gated developer/reference surface |
| `core-admin/dashboard` | `RETIRE` candidate |
| `test/hello-api` | `LEGACY_REFERENCE_REVIEW`; first template experiment, inspect before retirement |
| `test/redis-console` | `LEGACY_REFERENCE_REVIEW`; Operations/integration template experiment |
| `hub` | `RETIRE` candidate |
| `sys/admin/dashboard` | `RETIRE` candidate |

“Out” means excluded from the Operations target and consumer package. It does not
mean immediate deletion without the mutation gate.

### 3.2 Ratified template consequence for Operations

```text
OperationsApplicationsTemplate
    keep while required by the current Operations index;
    review/rebuild under the Operations V1 approved host model.

TemplateLabTemplate
    keep as the current implementation of the Template Lab reference experience while
    migrating page ownership into Operations. The reusable responsibility is Template
    Discovery / Substitutability; `TemplateLabTemplate` itself is not the capability
    identity and remains replaceable.

SystemDebugTemplate
    do not carry into Operations V1 merely for visual parity;
    preserve API/control behavior and rebuild the target experience on the approved
    Operations host model, then retire the old template.

HelloApiTemplate
    LEGACY_REFERENCE_REVIEW; preserve temporarily as the first template experiment,
    inspect its unique composition/data-flow lessons, then extract or retire.

RedisConsoleTemplate
    LEGACY_REFERENCE_REVIEW; preserve temporarily as an Operations/integration
    template experiment, inspect for API/System Control reuse, then extract or retire.

HubPageTemplate
    exclude from the Operations target; RETIRE with hub after consumer verification.
```

The globally approved template set is still derived from all approved application
pages, not only Operations. This decision narrows the Operations subset; it does not
authorize deleting templates used by Open Nexus, Simple or Auth.

### 3.3 Ratified component-catalog direction

`core-admin/component-catalog` is retained.

Its value is not merely visual demonstration: it exposes component identity, ownership
and consumers and therefore acts as a reference discovery surface for the Open Nexus
domain and design/presentation authorities.

```text
classification     REFERENCE
role               DEVELOPER / DISCOVERY / CONFORMANCE
distribution       GATED — excluded from ordinary consumer packages
current owner      core-admin / Operations reference surface
current page ID    core-admin/component-catalog
current template   KEEP while the page remains active
```

Future direction, explicitly outside the current mutation task:

```text
core-admin/component-catalog
→ promoted discovery route/experience
→ candidate discovery.astro host
→ middleware routing in a separate branch/backlog item
```

No route or middleware change is authorized by this Epic update. Until the future
promotion is implemented and proven, the current page/template remain canonical for
the reference/developer profile.

---

## 4. Dependencies

No mutating convergence begins before:

```text
F08-005  Single Page Authority
F08-006  Explicit IDs and current broken-reference ledger
```

Required inputs:

```text
F08-001 / F08-001B  authority and shadow inventory
F08-002             physical application-page retirement
F08-003             Capability / Bundle Page boundary
F08-004             ratified Application Page Contract
F08-009             ESSENTIAL logical-set evidence
```

Related owners and required evidence:

```text
F08-010  Asset Locality
F08-011  Template Resolution — STATIC model, three-surface authority fracture
F08-011A Application-aware Template Asset Resolution
F08-012  Self-contained ApplicationBundle
```

F08-011 is a direct input to this Epic: page convergence changes the active template
consumer set and therefore the set of templates that may be retained, rebuilt,
isolated or retired.

---

## 5. Target architecture

```text
ApplicationDefinition
    owns routing and navigation intent

ApplicationBundle
    owns application composition and page membership

Canonical PageDefinition
    owns stable page identity and presentation requirements

Foundation Capability
    may own reusable behavior without application identity

Derived Registry / Provider Artifacts
    are generated or composed from canonical declarations

Infrastructure Routes
    remain on an explicit allowlist and are not application pages

Test / Recovery Experiences
    are isolated from consumer packages
```

Candidate source direction, subject to F08-005:

```text
src/applications/<application>/pages/
    canonical application-page declarations

src/pages/
    infrastructure route hosts and explicitly allowlisted framework entry points

registry / virtual provider
    derived projection or compatibility adapter, never a second write authority
```

---

## 6. Non-goals

```text
mass delete
repository-wide rename
PageController changes
DiscoveryService changes without Foundation RFC
PageData changes
ApplicationDefinition changes
new generic page abstraction
0.9 Semantic Entity integration
general UI redesign unrelated to migrated behavior
asset migration
inventing a new universal template architecture
rewriting Git history
copying legacy codebases into the documentation repository
```

---

## 7. Classification model

Each surface receives values on independent axes.

### Lifecycle classification

```text
ESSENTIAL
REFERENCE
EXPERIMENTAL
LEGACY
BROKEN
```

### Operational role

```text
USER
SHARED
OPERATIONS
ADMIN
DEBUG
TEST
BUILD_TIME
INFRASTRUCTURE
```

### Distribution disposition

```text
INCLUDE
EXCLUDE
GATED
INTERNAL_ONLY
DEV_ONLY
REVIEW_REQUIRED
```

### Convergence disposition

```text
KEEP
MOVE_TO_BUNDLE
DERIVE_FROM_AUTHORITY
ALLOWLIST_INFRASTRUCTURE
DEV_ONLY
LEGACY_ADAPTER
FIX_REFERENCE
REMOVE_REFERENCE
MIGRATE_TO_APPLICATION
MIGRATE_TO_OPERATIONS_V1
PRESERVE_BEHAVIOR_REPLACE_PAGE
MOVE_COMPONENT_TO_DOMAIN
MOVE_COMPONENT_TO_DEVTOOLS
MOVE_COMPONENT_TO_LEGACY_COMPAT
RETIRE
REVIEW_REQUIRED
```

Example:

```yaml
id: sys/system-control
role: OPERATIONS
distribution: REVIEW_REQUIRED
convergence: MIGRATE_TO_OPERATIONS_V1
retireCurrentIdentityOnlyAfterParity: true
```

---

## 8. Retirement and migration ledger

For every Page ID or related source record:

| Field | Meaning |
|---|---|
| Page ID | Current canonical or legacy identity |
| Source path | Declaration or shim |
| Owner bundle | Exactly one owner or `NONE` |
| Behavior owner | Domain/application/capability owner |
| Runtime reachable | Yes / No / Unknown |
| Build reachable | Yes / No / Unknown |
| Navigation refs | Count and source |
| Package/export refs | Count and source |
| Replacement | Successor when observed |
| Lifecycle | ESSENTIAL / REFERENCE / EXPERIMENTAL / LEGACY / BROKEN |
| Role | USER / OPERATIONS / TEST / INFRASTRUCTURE / etc. |
| Distribution | INCLUDE / EXCLUDE / GATED / etc. |
| Convergence | KEEP / MIGRATE / RETIRE / etc. |
| Parity requirement | Functional behavior to preserve |
| Evidence | Commands and file:line references |
| Owner decision | Required before mutation |

---

## 9. Mutation gate

A page or shim may be retired only when:

```text
□ source and behavior authority identified
□ replacement identified or non-necessity demonstrated
□ production consumers = 0
□ build/package consumers = 0, or migrated
□ navigation references = 0, or resolved
□ bundle references = 0, or resolved
□ route aliases explicitly decided
□ tests classified as CURRENT or LEGACY
□ useful current coverage preserved
□ functionality parity verified for migrations
□ source history recoverable from Git/tag
□ owner decision recorded
```

A filename containing `legacy`, `old`, `copy`, `system`, `test` or `debug` is a signal,
not authorization to delete.

---

## 10. Broken-reference closure

For every finding record:

```text
source application/page
source field
target ID
target existence
target bundle ownership
route existence
failure reason
owner decision
```

Allowed outcomes:

```text
FIX_REFERENCE
REMOVE_REFERENCE
MOVE_TARGET_TO_BUNDLE
DECLARE_INFRASTRUCTURE_ROUTE
MIGRATE_TARGET_TO_APPLICATION
LEGACY_ALIAS_WITH_EXPIRY
RETIRE_SOURCE
```

Target:

```text
broken navigation references = 0
```

No broken reference is fixed through a silent fallback or invented alias.

---

## 11. Infrastructure routes

Physical framework routes may remain when they are infrastructure rather than
application content.

Candidate categories:

```text
/build catch-all host
API routes
auth callbacks
health endpoints
framework shells
```

Each allowlisted route declares owner, purpose, consumer, distribution requirement and
security policy.

Target:

```text
unmanaged physical application/content pages = 0
```

Not:

```text
physical route files = 0
```

---

## 12. Test, recovery and operations surfaces

Examples such as:

```text
test/hello-api
test/redis-console
sys/template-lab
sys/system-control
```

must be classified individually.

Possible results:

```text
DEV_ONLY bundle
REFERENCE package
test fixture
Operations migration
Foundation Capability + Operations page
retirement
```

They must not enter consumer distributions accidentally.

### 12.1 Component retirement strategy

Do not move every unwanted component into one generic `src/react/legacy/` directory.
That would hide debt without retiring it and could keep legacy components inside the
compile/package graph.

For every component of a page being migrated or retired, classify:

```text
KEEP_SHARED
    consumed by another approved page/capability; move only if current ownership is wrong

MOVE_TO_DOMAIN
    useful behavior/component belongs to an approved application or capability

MOVE_TO_DEVTOOLS
    diagnostic/reference component remains useful but must be excluded from consumer packages

MOVE_TO_LEGACY_COMPAT
    still required by a bounded compatibility adapter with owner, target and expiry

DELETE
    zero active consumers, no approved compatibility need; Git preserves history

REVIEW_REQUIRED
    consumer or ownership evidence incomplete
```

`src/react/legacy/` is allowed only for still-consumed compatibility implementations.
It must have:

```text
owner
replacement
declared consumers
expiry/removal condition
no export from the main React barrel
no new imports policy
consumer-package exclusion test
```

Preferred retirement for zero-consumer components is deletion from the active tree,
not relocation to `legacy/`.

Page retirement is atomic across:

```text
page declaration
navigation/route reference
template binding
component imports
assets
registry/provider entry
compatibility alias or redirect
```

Useful subcomponents are migrated before the old page/template is removed.

---

## 13. Registry and provider shims

F08-005 and the 0.7.5.4 co-location work already resolved the write authority:

```text
src/applications/<app>/pages
→ canonical PageDefinition source
```

The remaining `src/config/discovery/page-registry/pages/*` files are compatibility
re-exports, not a second PageDefinition authority. The residual problem is the consumer
path and duplicated composition:

```text
virtualProvider
→ imports registry/shim names
→ manually recomposes the application maps
```

Target:

```text
canonical application page maps
→ one derived PAGES_REGISTRY composition
→ virtualProvider consumes PAGES_REGISTRY
→ bundle/catalog/manifest projections
```

After consumer parity is proven:

```text
re-export-only page-registry/pages shims
→ retire
```

Backups and historical source snapshots remain a separate inventory/retirement task.
No new manual double registration may be introduced.

---

## 14. Template convergence derived from page convergence

Page convergence and template convergence are coupled.

```text
target canonical page set
→ declared template consumer set
→ approved host/model set
→ template disposition
→ scoped route imports and mapping
```

Removing or migrating a page may remove the last valid consumer of its template. The
system must not preserve unused templates merely because they remain listed in a gate,
switch or manager map.

Conversely, retiring a page does not automatically authorize deleting its template:
the template may be an approved host, a reusable capability surface or a consumer of
another active page.

### 14.1 F08-011 evidence incorporated

The current resolution model is STATIC and split across three surfaces:

```text
PageMeta.template
→ declaration

SUPPORTED_ROUTE_TEMPLATES
→ permission gate

/build route switch + static imports
→ effective name-to-component mapping

template-manager
→ auxiliary divergent map with silent VirtualPageTemplate fallback
```

Observed F08-011 findings include:

```text
G-13  gate/switch/manager divergence and alias mismatch
G-22  inert validation caused by non-null fallback
4      materialized templates with zero page declarations
2      declared alias names with zero page declarations and no homonymous component
```

These findings are not corrected by this Epic document. They become inputs to the
page/template target simulation and F08-012 implementation.

### 14.2 Read-only retirement simulation

Before page or template mutation, construct the target page set produced by F08-005
and F08-006 decisions.

For every current template calculate:

| Field | Meaning |
|---|---|
| Current page consumers | All current PageMeta declarations |
| Target page consumers | Consumers remaining after page migration/retirement |
| Gate entry | Present / absent |
| Route-switch branch | Component or alias target |
| Static import | Actual imported component |
| Manager-map entry | Component or fallback behavior |
| Approved host/model | Yes / No / Unknown |
| Behavior to preserve | Experience/capability responsibility |
| Target disposition | Keep / rebuild / isolate / retire / review |

The simulation changes no source file. It answers:

```text
If the approved page plan were applied, which templates would still have a valid
consumer or approved platform responsibility?
```

### 14.3 Template dispositions

```text
KEEP_APPROVED_HOST
KEEP_ACTIVE_TEMPLATE
REBUILD_ON_APPROVED_MODEL
MIGRATE_CONSUMER_THEN_RETIRE
DEV_ONLY
REMOVE_ALIAS
REMOVE_ORPHAN_DECLARATION
RETIRE_WITH_PAGE
REVIEW_REQUIRED
```

`REBUILD_ON_APPROVED_MODEL` means the experience remains useful but the existing
legacy template implementation is not carried into the target architecture. The
replacement follows the ratified Presentation/Experience host model; it does not
invent a fourth template authority.

### 14.4 Known candidate groups and owner dispositions

Global audit candidates, still subject to the target simulation:

```text
ORPHAN candidates from the STATIC application-page census
  WelcomePage
  SettingsTemplate
  OpenNexusHomeTemplate

AI / GENERATED-PAGE templates — NOT ORPHAN
  WowPageTemplate / WowLandingTemplate naming must be reconciled against source
  AiPageTemplate compatibility alias must be traced through the generated-page provider

DECLARED/ALIAS candidates
  DashboardTemplate      → PageInspector

OTHER LEGACY / REFERENCE candidates
  WebPageTemplateLegacy
  DocumentationTemplate
```

Owner correction:

> The Wow template is consumed by AI-generated pages. A zero count in static
> `src/applications/**` PageMeta declarations does not prove zero runtime/generated
> consumers.

Therefore `WowPageTemplate`, `WowLandingTemplate` and `AiPageTemplate` may not be
retired or pruned until the exact symbol/alias chain and generated PageRecord contract
have been verified.

Operations-specific owner direction:

```text
OperationsApplicationsTemplate
  KEEP_ACTIVE_TEMPLATE for the current Operations index;
  REVIEW/REBUILD for Operations V1.

TemplateLabTemplate
  KEEP_ACTIVE_TEMPLATE;
  migrate its page consumer from System to Operations.

SystemDebugTemplate
  REBUILD_ON_APPROVED_MODEL for the API/System Control migration;
  retire after Operations parity.

HelloApiTemplate
  LEGACY_REFERENCE_REVIEW; first template experiment, inspect before retirement.

RedisConsoleTemplate
  LEGACY_REFERENCE_REVIEW; inspect for Operations/API-Control lessons before retirement.

HubPageTemplate
  RETIRE_WITH_PAGE after hub consumer verification.
```

This list is an audit and planning input, not a direct delete list. Templates used by
other approved applications remain governed by their own active consumers.

Owner-reported consumer correction:

```text
VirtualPageTemplate
→ hosts/injects the current AI Pages panel and context
→ deprecated but maintained
→ MIGRATE_CONSUMER_THEN_RETIRE
```

Therefore `VirtualPageTemplate` is not an orphan and cannot be retired until the AI
Pages panel/context are migrated to an approved host with package and visual parity.
This work is tracked separately as `SURF-082-001` and does not block provenance or
other low-risk 0.8.2 cleanups.

### 14.5 Generated/AI page consumer correction

The F08-011 static census counted explicit declarations under application source maps.
It did not establish the complete consumer set for templates selected by generated or
provider-supplied PageRecords.

The target simulation must classify template consumers as:

```text
STATIC_APPLICATION_PAGE
DYNAMIC_PROVIDER_PAGE
GENERATED_PAGE_ARTIFACT
COMPATIBILITY_ALIAS
TEST_OR_FIXTURE
ROUTE_ONLY_DECLARATION
```

Required reconciliation commands/evidence in the Foundation repository:

```text
search exact symbols:
  WowPageTemplate
  WowLandingTemplate
  AiPageTemplate

trace:
  generated-page authoring output
  Redis/provider PageRecord.template values
  fixtures and seeds
  alias normalization
  route-host branch
  template-manager result
  package capability requirements
```

Required decisions:

```text
canonical template key for AI-generated pages
legacy alias policy and expiry
whether AI-page capability is included, gated or excluded per package
which component and assets must accompany that capability
fail-closed behavior for an unknown generated template key
```

Distribution rule:

```text
AI/generated-page capability included
→ canonical Wow template + declared assets + explicit aliases included

AI/generated-page capability excluded
→ template may be omitted from that package, but not declared globally orphaned
```

No static-source census may authorize template retirement without checking generated
PageRecord consumers.

### 14.6 Runtime template-catalog dependency

Template Lab is a reference/conformance experience for template substitutability:

```text
inject application/presentation context
→ enumerate an approved template catalog
→ select a template implementation
→ vary layout/presentation
→ preserve the governing contracts
```

Its current `TemplateLabTemplate` implementation introduces a set-valued runtime
dependency:

```text
getAllTemplates()
→ user selection
→ getComponent(target)
```

The runtime lookup is intentional; an undeclared/global lookup is not. This dependency
cannot be represented as one static `templateRef`. If Template Lab is included, the
package must declare a finite package-scoped template catalog.

```text
resolutionMode: RUNTIME_TEMPLATE_CATALOG
allowedTemplates: [...]
```

The runtime may enumerate only that catalog. Selection outside it must fail closed.
`VirtualPageTemplate` fallback may not hide a missing component.

Candidate classification:

```text
capability/responsibility  Template Discovery / Substitutability
page owner                 Operations
page/experience role       REFERENCE / CONFORMANCE
current implementation     TemplateLabTemplate
resolution mode            RUNTIME_TEMPLATE_CATALOG
package disposition        GATED
```

The globally available repository registry is not a valid distribution dependency.
Operations may intentionally package a broad approved catalog; a minimal consumer may
exclude Template Lab entirely.

The manifest must also distinguish:

```text
rendering.kind: TEMPLATE
rendering.kind: PHYSICAL
```

`PHYSICAL` is a rendering sentinel/category, not a `templateRef`. A physical route is
valid only when its packaged route artifact and infrastructure allowlist entry are
explicit.

Producer paths that emit `template: undefined` remain a separate fail-open finding.
Packaging must reject incomplete rendering metadata even before those producers are
refactored.

### 14.7 Operations V1 consequence

The System/API control migration must not drag `SystemDebugTemplate` or another legacy
host into Operations V1 merely to preserve visual parity.

```text
preserve control behavior
→ model it through approved capability/experience contracts
→ render it through the approved Operations V1 presentation model
→ retire the old page/template pair after functional parity
```

Visual identity may change. Functional behavior, authority, policy and evidence must
be preserved or explicitly superseded.

### 14.8 Atomic template retirement gate

A template or alias may be retired only when:

```text
□ static target page consumer count = 0, or every static consumer migrated
□ dynamic/generated/provider consumer count = 0, or every consumer migrated
□ compatibility aliases have an owner, target and expiry
□ it is not an approved shared host/contract
□ reusable behavior has an explicit owner and replacement
□ gate entry disposition decided
□ route-switch branch disposition decided
□ static import disposition decided
□ manager-map entry disposition decided
□ silent fallback does not mask removal
□ build and representative routes pass without the template
□ no consumer package requires it
□ owner decision recorded
```

For a retired template, gate, switch, import and manager entries are removed or derived
in the same bounded change. Partial removal must not create another drift surface.

---

## 15. Historical snapshots

Tracked codebase copies are handled separately by:

```text
REPO-LEGACY-001 — Tracked Snapshot and Backup Retirement
```

Before removal:

```text
□ path/hash inventory
□ unique-content analysis
□ remote commit/tag verified
□ secret and PII scan
□ approved unique documentation extracted separately
□ retirement record created
```

The central documentation repository stores source ID, tag/version, commit SHA and
approved notes. It does not store full legacy codebases.

---

## 16. Delivery plan

No mega-delete.

### Phase 0 — Target Page and Template Disposition Simulation

Read-only. Apply the ratified page plan to the current census and calculate the target
page consumers, template consumers, alias dispositions and approved-host set.

This phase is the first implementation-planning step of F08-012 after F08-005 closes.
It produces no source change.

### PR 1 — Empty and re-export registry shims

Only after F08-005.

### PR 2 — Broken and out-of-bundle references

Resolve ownership and navigation parity.

### PR 3 — Test/recovery isolation

Move or mark `DEV_ONLY`; preserve useful diagnostics.

### PR 4 — Operations migration preparation

Inventory System/API control behavior and define Operations V1 parity requirements.
No retirement before the target exists.

### PR 5 — Page and Template Convergence

For one bounded migration group:

```text
migrate or retire page consumers
→ rebuild useful experience on the approved host model when required
→ update target template consumers
→ remove obsolete gate/switch/import/manager entries atomically
```

No legacy template is carried into a target application solely for visual parity.

### PR 6 — Legacy page/template retirement

Only surfaces with replacement or proven non-use and a ratified template disposition.

### PR 7 — Tracked backup/version snapshots

Separate repository-hygiene PR under REPO-LEGACY-001.

---

## 17. Verification per PR

```text
□ exact file allowlist
□ replacement/parity evidence
□ targeted tests
□ TypeScript error-set comparison
□ full-suite failure-set comparison
□ build
□ representative route matrix
□ package/export diff
□ ApplicationBundle report
□ registry duplicate/collision report
□ broken-reference report
□ target page/template consumer matrix
□ template gate/switch/import/manager parity report
□ orphan and alias disposition report
□ silent template fallback path count
□ protected-kernel diff = 0, unless approved Foundation RFC
□ command ledger
```

Tests are classified and useful current behavior is migrated; tests are not deleted
merely because a legacy surface is removed.

---

## 18. Completion criteria

```text
□ unmanaged physical application/content pages = 0
□ manual duplicate page registrations = 0
□ canonical pages without explicit ID = 0
□ canonical pages without exactly one owner bundle = 0
□ broken navigation references = 0
□ out-of-bundle canonical pages = 0
□ legacy aliases without owner/expiry = 0
□ test/recovery pages in consumer package = 0
□ production Operations target contains only the four ratified responsibility groups
□ component-catalog exists only as the explicitly gated reference/developer surface
□ deprecated core-admin/system/hub/debug surfaces have explicit dispositions
□ Operations V1 migration ledger complete
□ System/API control behavior preserved or explicitly superseded
□ Template Lab is owned by Operations or its approved successor
□ active registry maps with duplicate write authority = 0
□ active orphan template declarations without approved role = 0
□ templates classified orphan without dynamic/generated consumer audit = 0
□ declared-only template aliases without owner/disposition = 0
□ AI/generated-page canonical template key and compatibility aliases are explicit
□ runtime template lookups outside a package-scoped declared catalog = 0
□ PHYSICAL rendering represented as a distinct kind, not a templateRef = 100%
□ producer outputs with undefined rendering metadata accepted by packaging = 0
□ template validation paths hidden by silent fallback = 0
□ active page/template pairs outside approved host model = 0
□ package static template imports outside target allowlist = 0
□ tracked backup codebase snapshots = 0
□ new 0.8.2 generated codebases contain retired/deprecated surfaces = 0
□ 0.8.1 → 0.8.2 compatibility findings are deterministic and actionable
□ supported 0.8.1 aliases/routes have migration or expiry behavior
□ clean-room package contains only allowlisted surfaces
```

---

## 19. Relationship with packaging

Source retirement and package allowlisting are complementary but independent.

```text
source convergence
→ reduces active-tree ambiguity

ESSENTIAL page allowlist
+
target template disposition
+
scoped registry and static imports
→ prevents accidental distribution
```

Page retirement narrows the target template set. Template convergence removes stale
resolution surfaces. F08-012 then materializes the approved page/template closure as a
self-contained package.

A legacy source or template remaining temporarily in the source tree must still be
excluded from consumer packages. A clean source tree does not replace package
validation.

---

## 20. Compatibility monitoring: 0.8.1 → 0.8.2

Surface cleanup can affect codebases, templates and projects produced from or modeled
on the 0.8.1 source tree. Compatibility must therefore be measured, not assumed.

### 20.1 Frozen 0.8.1 reference

Before 0.8.2 mutation preserve:

```text
v0.8.1 release commit and annotated tag
0.8.1 Distribution Manifest
0.8.1 package filesystem inventory
0.8.1 package/reproducibility hashes
0.8.1 canonical/legacy page surface inventory
0.8.1 template and alias inventory
one generated minimal consumer fixture
one Operations/reference fixture
```

These are comparison fixtures, not active source copies.

### 20.2 Generation invariant

The CLI and authoring flow must consume Foundation Release artifacts and Distribution
Contracts, not clone source internals from 0.8.1.

```text
Foundation 0.8.1 source noise
≠
consumer project content
```

If a generated project contains retired pages/templates merely because they existed in
the 0.8.1 repository, that is a generation defect.

### 20.3 Upgrade matrix

For each 0.8.2 retirement/migration verify:

| Concern | 0.8.1 project/package | 0.8.2 target | Required compatibility |
|---|---|---|---|
| Page ID | existing reference | migrated/retired | alias, migration or explicit rejection |
| Route | existing URL | target URL | redirect/expiry decision |
| Template key | legacy/current | approved host | alias or rebuild rule |
| Asset slot | current binding | resolved binding | manifest-compatible mapping |
| Capability ID/version | current contract | 0.8.2 contract | compatibility gate |
| Application identity | current bundle | current/Operations V1 | lifecycle decision |

### 20.4 Required tests

```text
□ 0.8.1 minimal project validates under its pinned 0.8.1 release
□ 0.8.1 project upgrade to 0.8.2 returns deterministic findings
□ supported aliases migrate to canonical IDs/templates
□ expired/unsupported aliases fail with actionable diagnostics
□ 0.8.2 new project generation contains no retired/deprecated surface
□ 0.8.2 package remains self-contained
□ 0.8.1 source snapshots are not copied into generated projects
□ CLI compatibility matrix records supported Foundation release ranges
□ package/public contract changes are classified before release
```

### 20.5 Release classification

A cleanup may ship as `0.8.2` only if removed surfaces are already noncanonical,
retired, dev-only or protected by explicit compatibility behavior.

If 0.8.2 removes a supported public route/contract without migration, the change must
be reclassified rather than hidden behind a patch version.

---

## 21. Final result

At completion, every active page must answer:

```text
Who owns it?
Where is it declared?
Why does it enter this package?
Which approved host/template renders it?
If migrated, which behavior was preserved and where?
If its former page disappeared, why does its former template still exist?
```

The target is not historical erasure. The target is one understandable, testable and
distributable current Foundation surface, with history preserved by Git and governed
records rather than active duplicate code.
