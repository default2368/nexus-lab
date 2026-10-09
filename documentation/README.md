# Workspace Documentation

Questa directory raccoglie gli artefatti documentali che prima erano dispersi nella
root del workspace.

Non è il repository canonico `nexus-lab-documentation`: è la workspace di review,
lettura e ratifica usata da questa conversazione.

```text
workspace documentation
→ review e approvazione
→ publication packet
→ repository documentale Git
```

---

## Struttura

### `governance/`

Regole e sorgenti di governance usate per preparare il repository documentale.

```text
INTAKE-AND-QUARANTINE.md
MAINTENANCE-WORKFLOW.md
```

### `prompts/`

Prompt operativi riutilizzabili per sessioni Arena e publisher Git.

```text
PROMPT-BOOTSTRAP-NEXUS-LAB-DOCUMENTATION.md
PUBLISHER-PROMPT.md
PROMPT-GENERIC-MAINTENANCE.md
```

Sono inoltre presenti prompt task-specifici derivati dallo stesso workflow; restano
strumenti operativi, non authority architetturali.

### `publication-packets/`

Manifest di pubblicazione candidati o approvati.

```text
PUBLICATION-PACKET-ON-ACQ-2026-1.0.yaml
```

Il packet corrente resta soggetto al proprio campo `approval.status`.

### `guides/`

Guide leggibili e artefatti esplicativi.

```text
GUIDA-DUMMIES-VIS-001-G-AUDIT.md
```

### `stakeholders/a/`

Documenti preparati per A. Conservano la distinzione fra registro analitico e
narrativo.

```text
NOTA-PER-A.md
ALLEGATO-NARRATIVO-PER-A.md
```

Questi file non sono automaticamente autorizzati alla pubblicazione nel repository
centrale.

### `research/benchmarks/`

Dossier competitivi e benchmark congelati.

```text
TRUSTABLE-vs-OPENNEXUS.md
TOOLJET-benchmark.md
```

---

## File lasciati intenzionalmente nella root

```text
.clinerules
AGENTS.md
```

Devono restare nella root perché governano il comportamento degli agenti e del
workspace.

---

## Regola di pubblicazione

Spostare un file in questa directory non lo rende canonico.

La pubblicazione nel repository Git richiede:

```text
documento approvato
+
publication packet approvato
+
source SHA-256
+
publisher prompt
+
diff owner-reviewed
```
