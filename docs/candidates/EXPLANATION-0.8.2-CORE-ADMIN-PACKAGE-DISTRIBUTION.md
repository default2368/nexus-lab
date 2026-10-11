# Spiegazione — Perché per 0.8.2 non implementiamo Distribution Profile framework e affini

**Status:** APPROVED EXPLANATION
**DecisionId:** NX-D-045-D1-EXPLANATION
**Source:** Context 3 + Context 4 + Owner approval + Main Agent
**ConversationRef:**
  conversationId: arena/86a8bf50-nexus-lab
  date: 2026-10-09
  extractor: documentation-agent v0.1.0

---

## Direttiva per Arena — OWNER DECISION RECORDED

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

## Premessa — package vs applicazione

Tutti questi punti riguardano la distribuzione di Core Admin come package autonomo, non il funzionamento di Core Admin dentro il repository Foundation.

La decisione è:

```text
Core Admin continua a esistere e funzionare nel repository
≠
Core Admin viene distribuito come package Foundation 0.8.2
```

Un'analogia:

```text
ApplicationBundle
→ inventario completo del magazzino

Distribution Profile
→ lista di cosa mettere in una certa scatola

Manifest
→ distinta del contenuto effettivamente imballato

Producer
→ prepara la scatola

Validator
→ verifica che scatola e distinta coincidano

Materializer
→ costruisce fisicamente la scatola

Clean-room
→ apre la scatola fuori dal magazzino e verifica che funzioni
```

Per simple sappiamo già quale scatola produrre.
Per Core Admin non abbiamo ancora deciso cosa dovrebbe entrare nella scatola.

Per la 0.8.2 non implementiamo:

```text
Distribution Profile framework;
manifest profile fields;
producer filtering;
validator profile rules;
Core Admin package fixtures;
Core Admin materialization/clean-room;
package version transition Core Admin.
```

---

## 1. Distribution Profile framework

### Cosa sarebbe

Core Admin contiene oggi otto pagine, ma con destinazioni differenti:

```text
core-admin/index
→ produzione / Operations

core-admin/discovery-pages
→ produzione / Operations

core-admin/component-catalog
→ reference gated

test/hello-api
→ development

test/redis-console
→ development

core-admin/pages
→ migration/retirement candidate

core-admin/control-center
→ migration/retirement candidate

core-admin/dashboard
→ legacy retirement candidate
```

Un Distribution Profile framework permetterebbe di dichiarare:

```text
ORDINARY_CONSUMER
→ index + discovery-pages

GATED_REFERENCE
→ index + discovery-pages + component-catalog

DEVELOPMENT
→ ordinary + hello-api + redis-console
```

### Perché non ora

Per farlo bene servirebbe introdurre:

```text
nuovi contratti
profile ID/version
page selection
compatibility
route closure
capability closure
API requirements
test matrix
```

È una nuova capability Distribution, non semplice cleanup.

Dato che Core Admin non verrà distribuito nella 0.8.2, il framework non serve alla release corrente.

```text
non implementato ora
≠
idea respinta

significa
→ deferito fino a quando esiste un package/consumer reale
```

---

## 2. Manifest profile fields

### Cosa sarebbero

Il Distribution Manifest descrive oggi:

```text
applicazione
pagine
template
asset
capability
discovery
provenance
```

Con i profili potremmo aggiungere:

```json
{
  "profileId": "core-admin/ordinary-consumer",
  "profileVersion": "1.0",
  "resolvedPageIds": [
    "core-admin/index",
    "core-admin/discovery-pages"
  ],
  "profileConformant": true,
  "profileFindings": []
}
```

### Perché non ora

Il Manifest è un contratto pubblico/versionato. Aggiungere campi non è una semplice modifica interna.

Bisognerebbe decidere:

```text
nomi
semantica
required/optional
compatibilità con 0.8.1
validator
materializer
Admin read model
client frontend
```

Non cambiamo un contratto stabile per descrivere un package che abbiamo deciso di non rilasciare.

---

## 3. Producer filtering

### Cosa sarebbe

Oggi il producer fa concettualmente:

```text
prendi ApplicationBundle core-admin
→ prendi tutte le pagine app=core-admin
→ produci manifest
```

Il filtering farebbe:

```text
prendi ApplicationBundle core-admin
→ applica profile ORDINARY_CONSUMER
→ includi soltanto index + discovery-pages
→ ricalcola template/assets/capabilities
→ produci manifest
```

### Perché non ora

Il producer dovrebbe ricevere un profilo approvato e deterministico.

Se aggiungessimo semplicemente:

```text
--include-page index
--exclude-page redis-console
```

creeremmo una seconda authority manuale e fragile.

La selezione deve avere:

```text
owner
versione
schema
test
compatibility behavior
```

Senza package Core Admin, nessun filtering è necessario.

Per simple, l'ApplicationBundle già coincide col package target dimostrato.

---

## 4. Validator profile rules

### Cosa sarebbero

Il validator dovrebbe verificare:

```text
manifest profile = ordinary
pagine attese:
- core-admin/index
- core-admin/discovery-pages
pagine extra:
→ reject
pagina mancante:
→ reject
template non richiesto:
→ reject
profile hash errato:
→ reject
```

Inoltre:

```text
clean Git provenance
→ necessario
profile conformance
→ necessario
owner release approval
→ separato
```

### Perché non ora

Non esiste ancora un profilo normativo. Il validator non può verificare una regola che non è stata definita e versionata.

Non vogliamo codificare le disposizioni provvisorie del backlog come se fossero già un public contract.

Il validator corrente continua a verificare i contratti 0.8 esistenti.

---

## 5. Core Admin package fixtures

### Cosa sarebbero

File di esempio/test come:

```text
core-admin-ordinary.valid.json
core-admin-gated-reference.valid.json
core-admin-development.valid.json
core-admin-profile-mismatch.invalid.json
```

Servirebbero a dimostrare:

```text
quali pagine entrano
quali template
quali asset
quali capability
quali failure
```

### Perché non ora

Le fixture sarebbero la codificazione del contratto profile.

Se non abbiamo ratificato e implementato quel contratto, creare fixture significherebbe congelare prematuramente decisioni ancora aperte.

Inoltre non esiste un package Core Admin 0.8.2 da validare.

---

## 6. Core Admin materialization / clean-room

### Cosa sarebbe

```text
Core Admin bundle
→ producer
→ manifest
→ materializer
→ filesystem package
→ clean-room
→ prova che il package funziona senza repository
```

È stato prodotto un artifact diagnostico con tutte le otto pagine, ma:

```text
Git provenance      corretta
Page IDs            corretti
Package profile     non approvato
```

Quindi non era release evidence.

### Perché non ora

Se facessimo materialization/clean-room su tutte le otto pagine potremmo provare:

```text
la scatola è tecnicamente auto-consistente
```

Ma non:

```text
è la scatola giusta da distribuire
```

Contiene:

```text
pagine legacy
test pages
Catalog gated
superfici in migrazione
```

Sarebbe una prova tecnica del package sbagliato.

Per la release 0.8.2 faremo materialization e clean-room sul package simple, che è il release target approvato.

---

## 7. Package version transition Core Admin

### Cosa sarebbe

Se esistesse un package Core Admin precedente, dovremmo decidere:

```text
core-admin-app 0.8.0
→ core-admin-app 0.8.2?
quali pagine rimosse?
quali ID cambiati?
quali alias?
quale upgrade path?
breaking o patch?
```

Inoltre oggi esistono versioni differenti:

```text
root Foundation version
→ 0.8.1
producer generated package version
→ hardcoded 0.8.0
Foundation release
→ derivata dal root package
```

È già un contratto da riconciliare.

### Perché non ora

Non abbiamo evidenza di un package Core Admin 0.8.1 pubblicato e supportato.

E abbiamo deciso:

```text
nessun Core Admin package nella 0.8.2
```

Quindi non esiste una transizione da dichiarare in questa release.

La versione verrà decisa quando verrà costruito il nuovo Operations package/experience.

---

## Cosa continuiamo a fare su Core Admin

L'esclusione dal package non significa abbandono.

Continuiamo a:

```text
mantenere il source runtime
correggere identity authority
chiudere security finding (diagnostic API policy)
inventariare backup/snapshot disposition
mantenere navigazione e route compatibility
preparare migrazione Operations sull'host approvato
riusare primitive e contratti disponibili
migrare comportamento utile
ritirare Core Admin soltanto dopo parity gates:

□ Operations index ha un successor
□ Discovery/pages ha un successor
□ Template Lab ownership è migrata o esplicitamente differita
□ API/System Control behavior è migrato o superseded
□ Component Catalog ha il proprio host gated/reference
□ navigazione e route compatibility sono decise
□ consumer source/build/package = 0
□ full-suite e package parity sono provate
□ eventuali alias hanno owner e scadenza
```

È coerente con:

> Infrastructure must be reusable; Domain must be replaceable.

La ricostruzione probabilmente sarà più semplice del refactor incrementale perché:

```text
le primitive esistono
i contratti sono più chiari
il read model Distribution esiste
sappiamo cosa non trascinare
SystemDebugTemplate e le legacy page non devono essere preservate per identità visiva
```

Ma resta una direzione da dimostrare, non una stima ancora verificata.

---

## Provenance

```
Context 3: Direttiva per Arena OWNER DECISION RECORDED Foundation 0.8.2 release package target simple Core Admin package CORE_ADMIN_PACKAGE_OUT_OF_0_8_2_RELEASE_SCOPE Do not implement Core Admin Distribution Profile in 0.8.2 Do not modify manifest schema producer validator materializer Admin read model frontend profile behavior Do not delete or retire core-admin ApplicationBundle/source application in 0.8.2 Future direction rebuild approved Operations experience using existing primitives/contracts migrate useful behavior then retire current core-admin identity only after consumer and parity gates diagnostic eight-page Core Admin package remains PROFILE_UNAPPROVED not release evidence F08-006 Phase A explicit IDs remain approved as current source-authority hygiene
Context 3 explanation: Per 0.8.2 non implementiamo Distribution Profile framework manifest profile fields producer filtering validator profile rules Core Admin package fixtures Core Admin materialization/clean-room package version transition Core Admin — Tutti questi punti riguardano distribuzione Core Admin come package autonomo non funzionamento dentro repository — Decisione Core Admin continua esistere funzionare ≠ viene distribuito come package 0.8.2 — Analogia ApplicationBundle inventario completo magazzino Distribution Profile lista cosa mettere in certa scatola Manifest distinta contenuto effettivamente imballato Producer prepara scatola Validator verifica scatola e distinta coincidano Materializer costruisce fisicamente scatola Clean-room apre scatola fuori magazzino verifica funzioni — Per simple sappiamo già quale scatola produrre Per Core Admin non abbiamo ancora deciso cosa dovrebbe entrare nella scatola — 1 Distribution Profile framework Cosa sarebbe Core Admin otto pagine destinazioni differenti index→produzione Operations discovery-pages→produzione Operations component-catalog→reference gated hello-api→development redis-console→development pages→migration/retirement control-center→migration/retirement dashboard→legacy retirement — Un Distribution Profile framework permetterebbe dichiarare ORDINARY_CONSUMER→index+discovery-pages GATED_REFERENCE→index+discovery-pages+component-catalog DEVELOPMENT→ordinary+hello-api+redis-console — Perché non ora introdurre nuovi contratti profile ID/version page selection compatibility route closure capability closure API requirements test matrix — nuova capability Distribution non semplice cleanup Dato Core Admin non verrà distribuito in 0.8.2 framework non serve release corrente non implementato ora ≠ idea respinta significa deferito fino a quando esiste package/consumer reale
Context 4: 2 Manifest profile fields Cosa sarebbero Manifest descrive applicazione pagine template asset capability discovery provenance Con profili aggiungere profileId profileVersion resolvedPageIds profileConformant profileFindings — Perché non ora Manifest contratto pubblico/versionato Aggiungere campi non semplice modifica interna Bisognerebbe decidere nomi semantica required/optional compatibilità con 0.8.1 validator materializer Admin read model client frontend Non cambiamo contratto stabile per descrivere package che abbiamo deciso non rilasciare — 3 Producer filtering Cosa sarebbe oggi producer prendi ApplicationBundle core-admin prendi tutte pagine app=core-admin produci manifest Filtering prendi ApplicationBundle applica profile ORDINARY_CONSUMER includi soltanto index+discovery-pages ricalcola template/assets/capabilities produci manifest — Perché non ora producer dovrebbe ricevere profilo approvato deterministico Se aggiungessimo --include-page index --exclude-page redis-console creeremmo seconda authority manuale fragile Selezione deve avere owner versione schema test compatibility behavior Senza package Core Admin nessun filtering necessario Per simple ApplicationBundle già coincide col package target dimostrato — 4 Validator profile rules Cosa sarebbero validator verificare manifest profile=ordinary pagine attese core-admin/index discovery-pages pagine extra reject pagina mancante reject template non richiesto reject profile hash errato reject Inoltre clean Git provenance necessario profile conformance necessario owner release approval separato — Perché non ora Non esiste ancora profilo normativo validator non può verificare regola non definita versionata Non vogliamo codificare disposizioni provvisorie backlog come se fossero già public contract validator corrente continua verificare contratti 0.8 esistenti — 5 Core Admin package fixtures Cosa sarebbero file esempio/test core-admin-ordinary.valid.json gated-reference valid development valid profile-mismatch invalid Servirebbero dimostrare quali pagine entrano quali template quali asset quali capability quali failure — Perché non ora fixture sarebbero codificazione contratto profile Se non abbiamo ratificato implementato contratto creare fixture significherebbe congelare prematuramente decisioni ancora aperte Inoltre non esiste package Core Admin 0.8.2 da validare — 6 Core Admin materialization/clean-room Cosa sarebbe Core Admin bundle→producer→manifest→materializer→filesystem package→clean-room→prova package funziona senza repository È stato prodotto artifact diagnostico con tutte otto pagine ma Git provenance corretta Page IDs corretti Package profile non approvato Quindi non era release evidence — Perché non ora Se facessimo materialization/clean-room su tutte otto pagine potremmo provare scatola tecnicamente auto-consistente Ma non è scatola giusta da distribuire Contiene pagine legacy test pages Catalog gated superfici migrazione Sarebbe prova tecnica package sbagliato Per release 0.8.2 faremo materialization clean-room su package simple che è release target approvato — 7 Package version transition Core Admin Cosa sarebbe Se esistesse package Core Admin precedente dovremmo decidere core-admin-app 0.8.0→0.8.2 quali pagine rimosse quali ID cambiati quali alias quale upgrade path breaking o patch Inoltre oggi esistono versioni differenti root Foundation 0.8.1 producer generated package version hardcoded 0.8.0 Foundation release derivata root package È già contratto da riconciliare — Perché non ora Non abbiamo evidenza package Core Admin 0.8.1 pubblicato supportato E abbiamo deciso nessun Core Admin package in 0.8.2 Quindi non esiste transizione da dichiarare in questa release Versione verrà decisa quando verrà costruito nuovo Operations package/experience — Cosa continuiamo a fare su Core Admin Esclusione dal package non significa abbandono Continuiamo mantenere source runtime correggere identity authority chiudere security finding...
Status: APPROVED EXPLANATION
Extractor: documentation-agent v0.1.0
```
