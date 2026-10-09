# Operations V1 — Candidate Backlog

**Status:** PARKED — post Foundation 0.8.2 surface convergence  
**Purpose:** preserve owner directions that must not leak into the current cleanup implementation.

---

## OPS-V1-001 · Promote Component Catalog to Discovery Experience

```text
Status      PARKED
Priority    P1 when Operations V1 opens
Depends     0.8.2 page/template convergence
Owner       Operations
```

### Owner direction

`core-admin/component-catalog` is retained as a valuable reference/developer surface.
It is not a disposable demo page.

Observed/candidate value:

```text
component identity
component consumers
presentation/design authority visibility
Open Nexus domain discovery
conformance and developer inspection
```

### Candidate target

```text
current core-admin/component-catalog
↓
Discovery reference experience
↓
candidate discovery.astro host/route
↓
middleware routing
```

The exact route, host and middleware contract require a separate branch and evidence
task. No route or middleware modification is authorized by this backlog entry.

### Boundary

```text
Component Discovery capability/responsibility
    owns discovery/inspection behavior

Operations / Open Nexus reference page
    owns identity, route, navigation and policy

Current component-catalog template
    remains the implementation until a replacement is proven
```

### Non-goals

```text
retire component-catalog during 0.8.2 cleanup
merge it into Template Lab without parity evidence
expose it in ordinary consumer packages by default
introduce middleware changes in the surface-retirement PR
rename the current route before compatibility analysis
```

### Required future evidence

```text
□ current component consumers and data sources inventoried
□ distinction from Template Lab demonstrated
□ target application ownership ratified
□ discovery.astro host contract defined
□ middleware route behavior and security defined
□ old route compatibility/expiry decided
□ package profile includes/excludes the reference experience explicitly
□ clean-room and navigation tests
□ no repository scan during Execution
```

### Success criterion

> A developer/reference user can discover which components exist, who consumes them
> and which authority owns them through a governed Discovery experience, without the
> page becoming a generic consumer dependency.
