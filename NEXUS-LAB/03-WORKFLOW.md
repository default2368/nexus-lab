# NEXUS LAB — Workflow di lavoro

Il metodo con cui questo progetto viene portato avanti. Formalizzato il 2026-09-10.

---

## 1. Il loop

```text
┌──────────────────────────────────────────────────────────────┐
│ 1. BRAINSTORM     LMArena / Arena Mode (GPT family)          │
│                   esplorazione, dibattito fra agenti,        │
│                   review di proposte                         │
│                        ↓                                     │
│ 2. SPEC           PRD / Recap / Decision Log                 │
│                   si congela cosa si è deciso                │
│                        ↓                                     │
│ 3. PROMPT         prompt MCP-ready per Roo / Cline /         │
│                   AntiGravity                                │
│                        ↓                                     │
│ 4. EXECUTE        Roo Code (deepseek-v4-pro) → compiti pesanti│
│                   Cline → task semplici                      │
│                   Continue → inline veloce                   │
│                        ↓                                     │
│ 5. VERIFY         codebase-memory-mcp + suite contratti      │
│                   flash per audit, pro per giudizio finale   │
│                        ↓                                     │
│ 6. RECORD         Decision Log + Backlog aggiornati          │
└──────────────────────────────────────────────────────────────┘
```

**Regola d'oro:** gli agenti eseguono **una volta sola** se la spec è buona.
Il costo si sposta tutto sul passo 1–2, che è quasi gratis.

---

## 2. Zona sicura — perché il brainstorming è legittimo

Il boundary Foundation/Execution è il **punto di invarianza del sistema**.
Finché una proposta non lo attraversa, esplorarla costa zero rischio architetturale.

```text
┌─────────────────────────────────────────────────┐
│  ZONA SICURA (X, Experience, CLI, Brain, doc)   │
│                                                 │
│  → brainstorming libero                         │
│  → si può proporre, scartare, ribaltare         │
│  → deepseek-flash basta                      │
│  → nessuna suite di contratti a rischio         │
│                                                 │
│  Tutto il backlog NX-01 → NX-10 sta qui.        │
└────────────────────┬────────────────────────────┘
                     │  BOUNDARY
┌────────────────────▼────────────────────────────┐
│  ZONA VINCOLATA (Foundation / Runtime)          │
│                                                 │
│  PageController · normalizeToPageData           │
│  ApplicationDefinition · ApplicationContext     │
│  BundleCollector · DiscoveryService(V2)         │
│  PageData                                       │
│                                                 │
│  → NON è brainstorming, è Foundation RFC        │
│  → audit MCP obbligatorio prima di proporre     │
│  → deepseek-v4-pro obbligatorio                 │
│  → decisione esplicita nel Decision Log         │
└─────────────────────────────────────────────────┘
```

**Test in una domanda:** *questa proposta richiede di modificare un simbolo della
zona vincolata?*
- No → brainstorming, procedi.
- Sì → fermati, apri una Foundation RFC.

---

## 3. Scelta del modello

| Classe di task | Modello | Dove |
|---|---|---|
| Extraction, inventory, audit, classificazioni | `deepseek-flash` | Roo / Cline |
| Retrieval-heavy, report preliminari, review di PRD | `deepseek-flash` | Roo / Cline |
| Giudizio architetturale, decisioni Foundation/Runtime | `deepseek-v4-pro` | Roo |
| Refactor pericolosi, commit complessi | `deepseek-v4-pro` | Roo |
| Second opinion / gate finale | `deepseek-v4-pro` | LMArena o Roo |
| Autocomplete, chat veloce, inline edit | `flash` o Copilot | Continue |

**Default flash, pro come gate.** 2–3 commit complessi al giorno, major release e
a volte cinque tag: il risparmio è sul volume, non sulla qualità delle decisioni.

---

## 4. Guardrail anti-allucinazione per i prompt MCP-ready

Da inserire sempre nelle review affidate a `flash`:

```text
Questa è una review. NON modificare alcun file, NON creare file. Output = report.

Se un simbolo non esiste nel grafo, scrivi NOT FOUND.
Non inferire, non indovinare percorsi, non citare codice che non hai estratto
con get_code_snippet.

Distinguere rigorosamente:
  FACTS OBSERVED
  HYPOTHESES
  RECOMMENDATIONS

RECOMMENDATION: APPROVED WITH CONDITIONS / REJECTED / DEFER
ACCEPTANCE CONDITIONS:
```

Motivo: `flash` tende a validare troppo facilmente una soluzione già contenuta nel
prompt ("SUPPORTED bias") e a comprimere/inventare. Il vincolo "NOT FOUND" e la
separazione FACTS/HYPOTHESES sono la contromisura.

Sostituire `APPROVED / REJECTED` secco con `APPROVED WITH CONDITIONS` + condizioni
di accettazione: produce output azionabile invece di un verdetto binario.

### Regola aggiunta il 2026-09-12 (dopo tre errori di affermazione)

> **Ogni affermazione su cosa esiste nel codebase deve citare il comando che l'ha
> prodotta. Zero risultati senza comando non è un dato.**

E due corollari sulla ricerca negativa:

```text
· Una ricerca per NOME non prova l'assenza di un CONCETTO.
  Cerca i valori, o leggi il type. Solo la lettura del type prova l'assenza.
· Un grep che restituisce zero richiede un sanity check sul path
  (esiste? contiene file?). Altrimenti il falso negativo è indistinguibile
  dal vero negativo.
```

Valgono per gli agenti **e** per chi scrive i prompt. Nella sessione 2026-09-12
l'assistente ha violato entrambe tre volte: vedi `01-DECISION-LOG.md`, nota di
processo.

### Regola aggiunta il 2026-09-13 — giudicare le proposte

> Quando si giudica una proposta che arriva da un'altra sessione, chiedere
> **cosa si vende** prima di chiedere **cosa si costruisce**.
> La seconda domanda è più facile, e per questo produce risposte sbagliate.

Motivo: una proposta incollata ha già una FORMA. Nella sessione 2026-09-13 la forma
era "implementazione di un agente"; l'intento era "capacità di Open Nexus da vendere".
Giudicare la forma invece dell'intento ha prodotto un verdetto corretto sulla forma
e sbagliato sulla proposta. Vedi `20-CAPABILITA-ANALISI-MERCATO.md` § 1 e § 10.

---

## 5. Sequenza MCP obbligatoria

```text
index_status        → sempre per primo; se l'indice non è sincronizzato, fermarsi
search_graph        → trovare simboli/route (preferire a search_code)
trace_path          → caller/callee, fan-in/fan-out, dipendenze
get_code_snippet    → solo l'implementazione del simbolo target
query_graph /
get_architecture    → layer strutturali, quando serve la visione d'insieme
```

**Mai:** leggere directory intere, grep su tutto il codebase, aprire file da 500 righe
per vederne una funzione. È budget bruciato.

Per il working tree locale (status/diff/log/commit) usare **git MCP locale**, non
GitHub remote MCP: quest'ultimo parla con GitHub.com (issue/PR), non con le modifiche
non committate.

---

## 6. Convergenza — il loop È il prodotto

Il loop del § 1 oggi è **manuale**: vive nelle chat, nei prompt copiati a mano,
nei PRD incollati.

NX-02 (Workflow Contract) è esattamente la sua productizzazione:

```text
OGGI (manuale)                          NX-02 (prodotto)
─────────────────────────────────────────────────────────────
brainstorm in chat                  →   (resta umano, ed è giusto)
PRD scritto a mano                  →   workflow.md nel bundle
prompt MCP-ready copiato in Roo     →   step con prompt embedded
Roo esegue                          →   runner esegue uno step alla volta
verifica a mano / suite contratti   →   gate: nexus validate
decisioni nella testa               →   Decision Log + stato step persistente
```

**Conseguenza strategica:** l'utente sta già eseguendo a mano il workflow che deve
costruire. Questo significa che NX-02 non è speculazione — è **strumentazione di una
pratica già validata**, con l'utente come primo utente. È il modo migliore di
progettare un contratto: estrarlo da qualcosa che funziona già.

Ed è anche il gate che manca a Trustable (nessuna validazione dell'artefatto) e a
Instruqt (`check-host` chiuso sui lab). Vedi `02-BACKLOG-NX.md` NX-03.

---

## 7. Persistenza fra sessioni

Il problema: le chat si perdono, i contesti si compattano, le decisioni evaporano.

La soluzione è che **il workspace è la memoria**, non la chat:

```text
NEXUS-LAB/00-INDICE.md          → mappa + contesto permanente
NEXUS-LAB/01-DECISION-LOG.md    → cosa è deciso, cosa è aperto, cosa è scartato
NEXUS-LAB/02-BACKLOG-NX.md      → cosa c'è da fare
NEXUS-LAB/03-WORKFLOW.md        → come si lavora (questo file)
../documentation/research/benchmarks/TRUSTABLE-vs-OPENNEXUS.md       → dossier competitivo congelato
uploads/NEXUS-recap-ufficiale.pdf → autorità congelata
.clinerules / AGENTS.md         → invarianti per gli agenti
```

**Protocollo di inizio sessione:** leggere `00-INDICE.md` → `01-DECISION-LOG.md`
(sezione APERTO) → `02-BACKLOG-NX.md`. Tre file, contesto ricostruito.

**Protocollo di fine sessione:** aggiornare `01-DECISION-LOG.md` con le decisioni
prese, spostare gli stati nel backlog, aggiornare "Stato corrente" in `00-INDICE.md`.

---

*Ultimo aggiornamento: 2026-09-10*
