# Executive Summary — Infrastruttura per trasformare conoscenza documentata in applicazioni governate

**Open Nexus / Nexus Lab — working names**
**Documento riservato · bozza per confronto · 1 pagina staccabile**
**Data:** 2026-10-09

---

**Problema:** Molte attività professionali dipendono da documenti, procedure, evidenze e decisioni. Le informazioni esistono, ma sono frammentate, difficili da attraversare e ancora più difficili da ricostruire quando qualcuno deve spiegare chi ha deciso cosa, sulla base di quali fonti e secondo quale versione.

**Proposta:** Costruire infrastruttura e strumenti che trasformino fonti documentate in applicazioni di conoscenza navigabili, verificabili e governabili.

```text
navigabile — puoi attraversare fonti, procedure, evidenze con locatori precisi
verificabile — ogni affermazione ha fonte, versione, excerpt, chi ha approvato
governabile — puoi approvare, fare eccezione, review, con receipt e audit trail
```

```text
L'AI interpreta.
Il sistema conserva le fonti.
Il gate verifica i contratti.
La persona decide.
```

**Cosa esiste già:**
- Foundation — ApplicationBundle/PageData, Distribution Manifest, package riproducibile, provenance Git, clean-room
- Brain — acquisizione Markdown con SHA-256, RawEvidenceBlob, SourceObservation, AcquisitionReceipt
- Assistant — Roy Client, /evaluate, diagnostic metadata
- Provato tecnicamente: stessa infrastructure su più experience, package riproducibile, claim/source metadata candidate, repeatability test interno M0 (dossier decomposto → 12 claim → matrice rigenerata 3/4 match)

**Non ancora provato esternamente:** uso reale ripetuto, willingness to pay, tempi adozione, processo commerciale, compliance specifica, valore riconosciuto dal buyer.

**Primo verticale di prova — G.:**
```text
Procedure → scheda operativa → questionario → risposta + evidenza → feedback → classificazione → azione → verifica → approvazione → chiusura
```
Serve a falsificare la piattaforma. Infrastruttura deve restare riutilizzabile e dominio sostituibile. Non è "software per audit", è primo stress test. Successo: G. riconosce o corregge il processo.

**Perché multi-settore:**

| Funzione | Esempi |
|---|---|
| ricostruire operazione | progetto, audit, procedimento |
| collegare evidenze | documenti, versioni, fonti |
| governare decisione | approvazione, eccezione, review |
| produrre dossier | rendicontazione, qualifica, controllo |
| dichiarare gap | informazione mancante o conflitto |

Parte comune: chi ha fatto cosa, su quale base, con quale evidenza, secondo quale versione, chi ha approvato.

**Piano:** WP1 Foundation e contratti, WP2 Brain fonti/record, WP3 Assistant experience, WP4 Pilot G., WP5 secondo dominio indipendente, WP6 governance/sicurezza/deployment, WP7 modello operativo/commerciale.

**Milestone:** M1 Foundation 0.8.2 chiusa, M2 upload Markdown→record→risposta epistemica, M3 dossier sintetico completo, M4 review G., M5 repeatability secondo operatore, M6 secondo dominio, M7 decisione pilot/funding/productization.

**Rischi dichiarati:** complessità, owner bandwidth, assenza utenti, naming/IP, storage/dati, access control, differenza prova tecnica/prodotto, mercato non validato, verticalizzazione eccessiva, governance pesante.

**Domande per confronto:**
- Forma di progetto leggibile?
- Output e milestone formulati correttamente?
- Dipendenze o rischi non dichiarati?
- Parte incomprensibile per ente/partecipata?
- Evidenza per finanziabilità/pilotabilità?
- Separazione infrastruttura/verticale credibile?
- Deliverable concreto da mostrare per primo?
- Programmi/bandi/strumenti pertinenti?

**Tono:** bozza riservata per confronto, working names, nessun dato cliente, nessun segreto, nessuna attribuzione a stakeholder, nessuna pretesa di partnership, nessun impegno richiesto. Critica precisa vale più di introduzione.

---

*Executive summary staccabile — resta sulla scrivania, dispensa permette approfondire con calma*
