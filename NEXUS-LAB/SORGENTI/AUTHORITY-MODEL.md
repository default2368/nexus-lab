# OpenNexus Authority Model

**Provenienza:** documento prodotto in altra sessione, ricevuto il 2026-09-17.
Salvato verbatim. Analisi e difetti riscontrati in chat il 2026-09-17;
il documento precedente di riferimento era `14-AUTHORITY-ARCHITECTURE.md`.

**Collocazione proposta dall'autore:** appendice di architettura della serie 0.7.x.

---

Questo sì che merita un documento. Non come roadmap, ma come mappa delle
responsabilità del sistema.

Lo userei quasi come appendice di architettura della serie 0.7.x.

## OpenNexus Authority Model

### Executive Summary

L'architettura OpenNexus è organizzata per ownership.

Ogni authority possiede un dominio preciso e non può duplicare responsabilità
appartenenti ad altre authority.

Principio guida:

```text
Una responsabilità
↓
Una authority
↓
Una source of truth
```

### Flusso delle Authority

```text
Application Authority
        ↓
Content Authority
        ↓
Domain Authority
        ↓
Design Authority
        ↓
Theme Authority
        ↓
Primitive Authority
        ↓
Presentation Authority
```

### 1. Application Authority

**Ownership:** Application Identity · Application Definition · Routing · Navigation ·
Contracts

**Source of Truth:** `src/config/applications/*`

**Possiede:** Chi è l'applicazione · Qual è il suo percorso · Quale landing utilizza ·
Quali pagine appartengono all'app

**Non possiede:** Design · Theme · Assets · Branding · UI

### 2. Content Authority

**Ownership:** Pages · Discovery · Registry · Policies

**Source of Truth:** `src/config/discovery/page-registry/*`

**Possiede:** Contenuto · Metadati pagina · Esperienze

**Non possiede:** Design · Application Identity · Theme

### 3. Domain Authority

**Ownership:** Classification · Health · Visibility · Projection · Indexes

**Source of Truth:** `src/core/domain-authority/*`

**Possiede:** Governance

**Risponde a:** Cosa rappresenta questo dominio?

**Non possiede:** UI · Branding · Theme

### 4. Design Authority

**Ownership:** Visual Meaning · Semantic Tokens · Typography · Spacing · Radius ·
Elevation

**Source of Truth:** `src/core/design-authority/*`

**Possiede:** primary · secondary · success · warning · danger · background · card ·
border

**Risponde a:** Che significato ha questo colore?

**Non possiede:** Tema · Logo · Brand · Componenti

### 5. Theme Authority

**Ownership:** Theme State

**Source of Truth:** `ThemeInjector`

**Possiede:** light · dark · system

**Risponde a:** Quale proiezione attiva utilizzo?

**Non possiede:** Colori · Token · Branding

### 6. Primitive Authority

**Ownership:** Building Blocks UI

**Source of Truth:** `src/core/ui-primitives/*`

**Possiede:** Badge · StatusBadge · EmptyState · MetaLine · IconButton

**Risponde a:** Come viene rappresentato un concetto UI?

**Consuma:** Design Authority · Theme Authority

**Non possiede:** Brand · Logo · Application Identity

### 7. Presentation Authority

**Ownership:** Identity · Branding · Chrome · Assets

**Source of Truth:** `src/core/presentation-authority/*`

**Possiede:** Logo · Favicon · Application Branding · Navbar Variants ·
TemplateHeader Variants · Presentation Assets

**Risponde a:** Come si presenta questa applicazione?

**Non possiede:** Tokens · Theme · Spacing · Colors · UI primitives ·
Navigation data · Chrome

Nel contesto OpenNexus:

```text
Chrome = cornice dell'applicazione

Comprende:      Navbar · TemplateHeader · OpenNexusHead · Layout placement
Non comprende:  Badge · Buttons · Cards · Input
```

### Ownership degli Asset

**Foundation Assets**

Possiede: `/favicon.svg` · shared illustrations · platform assets
Owner: Foundation

**Application Assets**

Possiede: logo · hero images · application illustrations · application branding
Owner: Application

Posizione target: `src/applications/<app>/assets/*`

### Flusso di Rendering

Dal concetto alla UI.

```text
Application Authority
        ↓  definisce l'app
Presentation Authority
        ↓  definisce identità e branding
Design Authority
        ↓  fornisce il significato visuale
Theme Authority
        ↓  proietta light/dark
Primitive Authority
        ↓  costruisce componenti
Templates / Pages
        ↓  rendering finale
```

### Stato della piattaforma (0.7.x)

**Completato**

```text
✅ Application Authority
✅ Content Authority
✅ Domain Authority
✅ Design Authority
✅ Theme Authority
✅ Primitive Authority
✅ Presentation Authority (pilota)
```

### Osservazione Architetturale

La serie 0.6.x era principalmente: stabilizzazione.

La serie 0.7.x è stata principalmente: formalizzazione delle ownership.

L'evoluzione più significativa non è stata l'introduzione di nuove funzionalità, ma
la capacità del sistema di rispondere in modo univoco alla domanda:

> **Chi possiede questa responsabilità?**

Per ogni area principale della piattaforma.

Questa è probabilmente la milestone architetturale più importante raggiunta da
OpenNexus Foundation fino ad oggi.
