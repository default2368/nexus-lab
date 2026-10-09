# Frontend Backlog

**Ultimo aggiornamento:** 2026-09-20
**Percorso attuale:** chiusura 0.7.0.4 → preparazione 0.8

---

## NOW

Massimo tre voci. Queste sono le sole attività frontend da considerare “in corso”.

### FE-001 · Derivare la baseline ESSENTIAL dal tag green

```text
Release    0.8
Stato      READY
Priorità   P0
Blocca     CLI-001 baseline minimal
Base       foundation-baseline-green @ a2183f5
Fonte      Contracts Report 0.7.5.4C + 0.7.5.5 alignment
```

**Stato acquisito**

```text
747/747 contract + authority test verdi
public TypeScript surface = 0 errori
tag foundation-baseline-green
10 broken refs classificati in 2 root cause
```

Il Contract Alignment è chiuso come FE-014. Restano la classificazione delle pagine
e la derivazione del set distribuibile.

**Prossima azione**

Classificare pagine e capability:

```text
ESSENTIAL       necessario a runtime, starter e contract validation
REFERENCE       dimostra una capability
EXPERIMENTAL    laboratorio / debug
LEGACY          conservato soltanto nel tag
BROKEN          riferimento realmente invalido
```

**Definition of Done**

```text
□ tutte le pagine classificate
□ elenco ESSENTIAL per ogni applicazione
□ i 10 broken refs hanno owner e destinazione 0.8
□ minimal-template.manifest generabile dalla allowlist ESSENTIAL
□ nessuna copia da delete-list
□ baseline minimal valida, builda e serve una landing
□ Shared Auth inclusa soltanto se confermata dai consumer dei routing contracts
```

---

### FE-014 · 0.7.5.5 Contract Alignment

```text
Release    0.7.5.5
Stato      DONE
Priorità   —
Commit     a2183f5
Tag        foundation-baseline-green
Fonte      CONTRACT-ALIGNMENT-REPORT-0.7.5.5.md
```

```text
✓ 26 → 0 contract failure
✓ 747/747 contract + authority test
✓ 26 fix, 0 regressioni full-suite
✓ 10 broken refs classificati
✓ public TypeScript surface: 0 errori
✓ nessun protected file toccato
✓ DEC-001 Operations title
✓ DEC-002 post-auth open-nexus/index
```

---

### FE-002 · Completare Asset Resolution

```text
Release    0.7.0.4
Stato      READY
Priorità   P0
Blocca     chiusura Ownership Consolidation / Presentation rollout
Fonte      review Presentation Authority
```

**Problema osservato**

Esistono due fonti fisiche per gli asset Open Nexus:

```text
public/images/applications/open-nexus/
src/applications/open-nexus/assets/
```

Asset Ownership è attivata; Asset Resolution non è migrata.

**Prossima azione**

Produrre inventario `asset → import/consumer → authority`, scegliere la fonte
canonica e migrare **una sola classe di asset** come prova.

**Definition of Done**

```text
□ una sola source of truth fisica per ogni asset migrato
□ nessuna copia manuale fra public/ e src/applications/
□ resolver o build step coperto da test
□ logo/favicon/hero della prova risolti dalla Presentation Authority
□ comportamento runtime invariato
□ piano residuo per le altre applicazioni, senza migrazione massiva nello stesso PR
```

---

### FE-003 · Allineare il brand visibile a “Open Nexus”

```text
Release    0.7.0.4
Stato      READY
Priorità   P1
Fonte      D-082 + screenshot 2026-09-20
```

**Problema osservato**

Nella UI pubblica compaiono ancora:

```text
OpenNexus
About OpenNexus
```

Convenzione decisa:

```text
prosa / brand visibile   Open Nexus
identificatori tecnici   open-nexus
```

**Prossima azione**

Individuare la source authority del display name e verificare se tutte le superfici
lo derivano oppure mantengono stringhe locali.

**Definition of Done**

```text
□ navbar, hero, title, tabella Applications e document title mostrano “Open Nexus”
□ percorsi, registry ID e directory restano `open-nexus`
□ nessun replace indiscriminato sugli identificatori
□ un test impedisce la ricomparsa di `OpenNexus` nelle superfici visibili
```

---

## NEXT — 0.8

Non iniziare finché almeno due voci NOW non sono `DONE`.

### FE-004 · Formalizzare Presentation Profile vs Experience Profile

```text
Release    0.8
Stato      READY
Priorità   P1
Fonte      screenshot Open Nexus / Operations, D-005, Presentation Authority
```

**Problema**

La 0.8 deve consentire layout differenti senza scegliere renderer tramite `appId` e
senza permettere a ogni applicazione di inventare un proprio sistema visivo.

**Decisione da implementare**

```text
Presentation Profile   livello applicazione: chrome, densità, larghezza,
                       navbar/header variant, asset, branding
Experience Profile     livello pagina: landing, library, dashboard,
                       explorer, documentation, workflow
```

Profili iniziali massimi:

```text
knowledge    Open Nexus
workspace    Operations
focused      Authentication
```

**Prossima azione**

Scrivere un ADR breve con schema del manifest e una matrice
`profile → proprietà consentite/non consentite`.

**Definition of Done**

```text
□ nessun `if (appId === ...)` per scegliere il renderer
□ Page semantics continua a selezionare il renderer
□ Presentation Authority possiede il chrome, non PageData
□ tre profili sufficienti per Open Nexus, Operations e Authentication
□ una quarta variante richiede una prova che le prime tre non bastano
```

---

### FE-005 · Presentation rollout su una seconda applicazione

```text
Release    0.8
Stato      BLOCKED
Priorità   P1
Blocco     FE-002, FE-004
Fonte      regola del due
```

**Prossima azione dopo lo sblocco**

Applicare il modello di Presentation Authority a Operations senza duplicare token,
primitive o chrome locale.

**Definition of Done**

```text
□ Open Nexus e Operations consumano lo stesso contratto di Presentation
□ identità differenti, Design/Theme/Primitive condivise
□ test negativi impediscono a Presentation di possedere token/theme/navigation data
□ nessuna regressione visuale sulle due superfici
```

---

### FE-006 · Verifica responsive e tastiera sulle due superfici di riferimento

```text
Release    0.8
Stato      READY
Priorità   P2
Fonte      screenshot desktop 2026-09-20
```

**Perimetro**

```text
Open Nexus landing
Operations Applications dashboard
```

**Definition of Done**

```text
□ viewport mobile, tablet e desktop
□ navigazione completa da tastiera
□ focus visibile
□ tabella Operations degrada senza perdita di significato
□ contrasto e stato non affidati soltanto al colore
□ screenshot/regression evidence conservata
```

---

### FE-011 · Admin 0.8 composto manualmente: Applications → Pages → Details

```text
Release    0.8
Stato      BLOCKED
Priorità   P1
Blocco     FE-001, FE-004
Fonte      modello Application Catalog + pilot di componibilità
```

**Scopo**

Costruire Admin manualmente, usando soltanto componenti e sotto-componenti già
inventariati o promossi nelle Authority. Non costruire un visual builder e non
competere sul numero di widget.

**Gerarchia iniziale**

```text
Applications
  → Application Detail
      → Pages
          → Page Detail
```

**Definition of Done**

```text
□ Applications legge l'Application Catalog, non una lista locale
□ Application Detail proietta identità, stato, entry point, presentation e health
□ Pages legge la relazione dell'applicazione, non duplica il registry
□ Page Detail mostra source authority, policy, template, relazioni e stato
□ nessun nuovo componente entra in Primitive Authority senza secondo consumer
□ nessun `if (appId === ...)` per comporre le viste
□ il pilot documenta quali composizioni sono davvero riutilizzabili
```

---

### FE-012 · Cambio template governato dal Page Detail

```text
Release    0.8
Stato      BLOCKED
Priorità   P1
Blocco     FE-011
Fonte      PageData.template + invariante D-005
```

**Scopo**

Consentire al Page Detail di proporre o applicare un template compatibile senza
spostare logica nel kernel.

**Flusso**

```text
PageRecord
  → template candidate
  → compatibility validation
  → preview
  → approvazione
  → nuova definizione / build artifact
  → Runtime esegue
```

**Definition of Done**

```text
□ il Runtime non sceglie e non modifica template
□ Page semantics continua a selezionare il renderer
□ il cambio avviene nell'Authoring/Experience layer
□ template key risolta tramite registry, mai tramite appId
□ preview prima della persistenza
□ validazione di compatibilità e rollback
□ un futuro prompt può PROPORRE la modifica, mai applicarla nel request path
```

---

### FE-013 · Estrarre il modello Entity → Projection → Experience soltanto dal pilot

```text
Release    post-0.8 pilot
Stato      PARKED
Priorità   P2
Blocco     FE-011, FE-012
Fonte      regola del due
```

**Guardrail**

Non progettare subito una `GenericEntityPage`. Prima osservare almeno due entità
reali — `Application` e `Page` — e soltanto dopo estrarre ciò che condividono.

```text
Entity             dato di dominio
Projection         vista read-only dell'entità
Experience/Page    superficie che rende la projection
```

Una `PageRecord` può essere visualizzata dentro una Page Experience: è un meta-livello,
non un riferimento circolare, purché la projection contenga riferimenti per ID e non
incorpori ricorsivamente il rendering di sé stessa.

**Definition of Done**

```text
□ due entità reali confermano lo stesso contratto
□ relazioni tramite ID, lazy e con profondità limitata
□ nessun kernel branch per entity kind
□ entity-specific adapter/registry resta nel layer Experience
□ Infrastructure reusable; Domain replaceable
```

---

## LATER

### FE-007 · Design Enforcement migration

```text
Stato      PARKED
Priorità   P2
Fonte      baseline 554 violazioni / 33 superfici evolutive
```

Procedere con Boy-Scout rule, non con una migrazione massiva. Ogni file migrato
attiva il gate per-file e non può ricrescere.

### FE-008 · Machine-enforced expiry delle eccezioni

```text
Stato      PARKED
Priorità   P2
Fonte      NX-46
```

Aggiungere `expires` al dato `EXCEPTIONS` e far fallire CI quando una scadenza è
superata senza formalizzazione.

### FE-009 · Restringere `legacy-frozen:pages`

```text
Stato      PARKED
Priorità   P2
Fonte      NX-47
```

Lo scope a prefisso `src/pages/build/` comprende il punto d’ingresso di Execution e
qualunque file futuro. Restringere ai file effettivamente congelati.

### FE-010 · Onboarding della knowledge experience

```text
Stato      PARKED
Priorità   P2
Fonte      NX-70, benchmark Trustable
```

La curva di apprendimento è l’unica frizione di mercato importante senza risposta
architetturale. Non progettare tutorial prima che esista una prima istanza esterna.

---

## DONE

Una riga per voce chiusa. Il dettaglio rimane nei commit e negli ADR.

```text
— nessuna voce ancora chiusa in questo backlog operativo —
```
