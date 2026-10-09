# Riferimenti — risoluzione delle citazioni del Brain

**Scopo:** `brain/knowledge/*.md` cita ID del corpus strategico. Il corpus non entra
nel repo (D-014), quindi la risoluzione sta qui — fuori, dove sta il corpus.

**Regola:** ogni regola del Brain è autosufficiente. Questo file serve a contestarla,
non a capirla.

**Ultima verifica:** 2026-09-17 · 8 riferimenti distinti nei file `05-EVALUATION.md` e
`06-STORAGE-AND-VALIDATION.md`, tutti risolti.

---

## Citati in `05-EVALUATION.md`

| ID | Dove | Cosa dice | Perché è citato |
|---|---|---|---|
| **AF-001** | `05-AF001-VERDETTO.md` | `Runtime → BundleCollector` nel request path: **chiuso** su `feature/catalog-registry-authority` via `APPLICATION_TYPE_PROJECTION` | A1 — ipotesi affermata come prerequisito commerciale e falsificata dai file |
| **D-027** | `01-DECISION-LOG.md` | "Formalizzare la posizione non è formalizzare la proprietà" — **FALSIFICATO**: la projection è materializzazione dichiarata, documentata e coperta da test di parità | A1 — quarta ipotesi di drift smentita dall'evidenza |
| **D-040** | `01-DECISION-LOG.md` | Metodo Sonda: separazione percorso-piattaforma / applicazione-sonda, **sei gate di promozione** nel core | R6.1–R6.6 — la regola del due e i cinque test |
| **NX-30** | `02-BACKLOG-NX.md` | Scelta del verticale. **Ricalibrato tre volte**: da "P0 strategico" a "ha un criterio" (D-047) a "candidata forte" (D-053) a "in attesa di NX-91" | A4 — chiuso tre volte, tre volte prematuro |
| **NX-57** | `02-BACKLOG-NX.md` | Test di ripetibilità: analisi su oggetto nuovo usando **solo** il metodo scritto, senza operatore. **P0** | R5.5 — e prerequisito per estrarre l'ontologia |
| **Q-005** | `01-DECISION-LOG.md` + `06-PROMPT-Q005.md` | `applicationType` dichiarato o inferito? **Risposta:** dichiarato nel Bundle (`src/applications/*/package.ts`), non in `ApplicationDefinition` | R3.2, R3.3 — il grep sui nomi invece che sui valori |

| **D-009** | `01-DECISION-LOG.md` | Embeddings: interfaccia subito, provider mai per ora; testo source authority, embedding proiezione | `06-STORAGE-AND-VALIDATION.md` § 2.2 — storage/proiezioni derivate |

## Non citati ma collegati

| ID | Dove | Collegamento |
|---|---|---|
| D-014 | `01-DECISION-LOG.md` | strategia fuori dal repo → perché questo file non viaggia col Brain |
| D-037 | `01-DECISION-LOG.md` | `observed ≠ inferred` e le tre separazioni → § 1 marcatori |
| D-087 | `01-DECISION-LOG.md` | ambiguità del destinatario comparsa in entrambe le simulazioni → A3 |
| D-088 | `01-DECISION-LOG.md` | limite strutturale delle simulazioni → R5.5 |
| D-092 | `01-DECISION-LOG.md` | perché `05-EVALUATION` è trascrizione e non progettazione |

---

## Come si mantiene

```text
1. ogni nuovo file in brain/knowledge/ che cita un ID → aggiungere la riga qui
2. a ogni chiusura di sessione: rieseguire il controllo ID citati / ID risolti
3. se un ID citato non è risolvibile → o la regola perde la provenienza,
   o il riferimento va corretto. Mai lasciare un ID che non punta a niente.
```

Controllo eseguibile:

```bash
grep -oE '\b(NX-[0-9]+[ab]?|D-[0-9]+|C-[0-9]+|Q-[0-9]+|AF-[0-9]+)\b' \
  brain/knowledge/*.md | sort -u
```

---

*Questo file sta nel workspace strategico, non nel repo del Brain.*
