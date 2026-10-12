# Scheda di progetto — Open Nexus / Nexus Lab

**Denominazioni provvisorie — Bozza riservata · ottobre 2026 — 2 pagine**

---

## Obiettivo

Costruire infrastruttura e strumenti per trasformare conoscenza documentata in dossier e applicazioni navigabili, verificabili e governabili, mantenendo esplicite fonti, versioni, verifiche e decisioni.

## Beneficiari candidati

- Professionisti che devono ricostruire attività e decisioni (audit, controllo, qualifica)
- Team che gestiscono procedure con evidenze e approvazioni
- Organizzazioni che devono rendere conto di decisioni con fonti

Non: prospect da qualificare, investitore per pitch, contatto da attivare. Prima di tutto confronto progettuale.

## Output

- Piattaforma stabile con contratti e artefatti distribuibili verificabili
- Dossier sintetico con claim, evidenze, fonte, gap, azione, approvazione, receipt
- Interfaccia per navigare dossier e ispezionare evidenze
- Pilot G. corretto da professionista di dominio
- Secondo caso applicativo per testare riusabilità infrastruttura

## Work package

```text
WP1  consolidare piattaforma e contratti
  obiettivo: chiudere base tecnica stabile e verificabile
  output: piattaforma stabile, artefatti distribuibili, provenienza e controlli
  stato: in corso
  dipendenza: PR #14 debug gate
  gate: piattaforma stabile

WP2  acquisire e strutturare le fonti
  obiettivo: trasformare documenti in record con fonte e versione
  output: acquisizione documenti, record e relazioni
  stato: in sviluppo
  dipendenza: WP1
  gate: documento → record con fonte

WP3  costruire dossier ed esperienza utente
  obiettivo: rendere dossier navigabile e verificabile
  output: interfaccia per ispezionare risultati, evidenze, gap
  stato: in sviluppo
  dipendenza: WP2
  gate: dossier sintetico ENG-001

WP4  eseguire e correggere il pilot G.
  obiettivo: verificare modello con professionista di dominio
  output: dossier corretto, feedback strutturato
  stato: North Star
  dipendenza: WP2+WP3
  gate: G. riconosce o corregge il processo

WP5  verificare secondo dominio e sostenibilità
  obiettivo: testare se infrastruttura resta comune cambiando dominio
  output: secondo caso (A. operation/evidence reconstruction), analisi sostenibilità
  stato: da avviare dopo M4
  dipendenza: WP4
  gate: ripetibilità con secondo operatore + decisione sviluppo/pilot/finanziamento
```

## Milestone

```text
M1  piattaforma stabile
M2  documento → record
M3  dossier sintetico
M4  review G.
M5  ripetibilità con secondo operatore
M6  secondo dominio
M7  decisione di sviluppo / pilot / finanziamento
```

## Dipendenze e rischi

- complessità e dipendenza dal promotore
- dati e controllo degli accessi
- assenza utenti e mercato non validato
- eccesso di governance
- denominazione e naming

## Criteri di successo

- G. riconosce o corregge il processo (non dice che UI è bella)
- Dossier sintetico con fonte, versione, gap, approvazione
- Ripetibilità: secondo operatore che non ha visto originale riproduce dossier
- Infrastruttura resta comune mentre dominio cambia (Infrastructure reusable, Domain replaceable)

## Ipotesi da falsificare

```text
H1 buyer values traceability over generic generation
H2 governance supports higher price tier
H3 same infrastructure supports second domain
H4 dossier reduces reconstruction/review time
H5 non-technical expert can correct model

F1 G. does not recognize workflow
F2 source/claim links not useful during review
F3 dossier production costs more than manual reconstruction
F4 second domain requires kernel changes
F5 buyer will not allocate budget for governance
F6 another operator cannot reproduce dossier
```

---

*Bozza riservata · denominazioni provvisorie · nessun impegno richiesto*
