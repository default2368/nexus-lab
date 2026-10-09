# 35 — Risposta trasparenza codificata — scraper, CLI, record

**Data:** 2026-10-09
**Fonte:** risposta agent 2026-10-09T18:59 "Trasparenza totale"
**SHA originale: fa1615760c8e (sha256sum 35-RISPOSTA-TRASPARENZA-CODIFICATA.md)
**Stato:** CANDIDATE — GENERATED_SOURCE
**Metodo:** parsing deterministico Classe 0 + una interpretazione Brain
**Regola:** Brain proposes, Human corrects, Authoring validates. No auto-canonical promotion.

---

## 0. Principio (da 05-EVALUATION.md)

> Il prodotto non è la risposta. È il record.

Ogni affermazione fattuale ha marcatore OSSERVATO / INFERITO / LIMITE + riferimento.

---

## 1. OSSERVATO — cosa esiste, con comando

### 1.1 Scraper — 11-CONNECTOR-LAYER.md

**[OSSERVATO]** Il contratto `Fetched` esiste in `11-CONNECTOR-LAYER.md` §3 con campi `source_uri, fetched_at, status, content_sha, changed, text, raw_headers, content_type, error`.
- Evidence: `cat NEXUS-LAB/11-CONNECTOR-LAYER.md | head -300`
- Locator: `11-CONNECTOR-LAYER.md:70-95`

**[OSSERVATO]** L'upgrade obbligatorio è `content_sha + changed` con conditional request `ETag / Last-Modified → 304`.
- Evidence: `11-CONNECTOR-LAYER.md:20-60`
- Command: `grep -n "content_sha\|304\|ETag" NEXUS-LAB/11-CONNECTOR-LAYER.md`

**[OSSERVATO]** Headless browser, proxy rotation, ML extraction sono esplicitamente vietati in §5.3.
- Evidence: `11-CONNECTOR-LAYER.md:150-170`

**[OSSERVATO]** `scan-project-layout.py` usa `find` + `grep` locali, non HTTP fetch. Per Bolt.new ha usato `git clone --depth 1 https://github.com/stackblitz/bolt.new`.
- Evidence: `cat tools/automations/scan-project-layout.py | grep "run\|clone"`
- Command: `git clone --depth 1 https://github.com/stackblitz/bolt.new.git` (eseguito 2026-10-09, /tmp/bolt.new)

**[LIMITE]** `PublicTargetPolicy` anti-SSRF da `07-ACQUISITION-AND-MCP.md` §0 non è ancora implementato.
- Evidence: `grep -n "SSRF\|PublicTargetPolicy" brain/knowledge/07-ACQUISITION-AND-MCP.md`

### 1.2 CLI — cli/backlog/BACKLOG.md

**[OSSERVATO]** CLI-008 Audit richiede inventario campi Application/Page classificati USER_INPUT/DERIVED/DEFAULT/AUTHORITY_OWNED.
- Evidence: `cli/backlog/BACKLOG.md:70-110`

**[OSSERVATO]** `f08-audit.py` implementa i comandi di F08-001: `find docs -iname 'ADR-*'`, `git grep createApplicationDefinition`, `PAGES_REGISTRY`, `virtualProvider`, `PUBLIC/PROTECTED`, `physical/main/chat`.
- Evidence: `cat tools/automations/f08-audit.py | grep "AUDIT_COMMANDS"`
- Command: `python3 tools/automations/f08-audit.py --repo . --output /tmp/f08-audit --mock` → 19 evidenze, KPI-08-01 CLEAN

**[OSSERVATO]** CLI-009 `ApplicationAuthoringSpec`, `PageAuthoringSpec` non hanno schema stabile. Doc dice "This structure is illustrative. It is not yet a stable contract." (09 §8).
- Evidence: `cat foundation/backlog/EPIC-0.9.0-SEMANTIC-ENTITY-PROJECTION.md | grep -A2 "illustrative"`

### 1.3 Record prodotti

**[OSSERVATO]** `06-STORAGE-AND-VALIDATION.md` §11 definisce 6 campi minimi obbligatori: `claim_id, text, epistemic_status, source_url, excerpt, collected_at`.
- Evidence: `grep -n "claim_id\|epistemic_status" brain/knowledge/06-STORAGE-AND-VALIDATION.md | head -10`

**[OSSERVATO]** `collect-epistemic-records.py` ha prodotto 468 records da 35 file → `/tmp/brain-records/2026-09-14.jsonl` (874K).
- Command: `python3 tools/automations/collect-epistemic-records.py --input NEXUS-LAB --output /tmp/brain-records --date 2026-09-14`
- Output: `Collected 468 records from 35 files`

**[OSSERVATO]** `brain-collector.py` su Prometeo ha prodotto `SUFFICIENT_FOR_SYNTHETIC_PILOT` 11/14 OBSERVED, 9 attori, 11 entità.
- Command: `python3 tools/automations/brain-collector.py --input NEXUS-LAB/SORGENTI/25-SCANSIONE-PROMETEO-RIFIUTI.md --output /tmp/candidate-prometeo.yaml --domain-id prometeo-rifiuti`
- Output: `Status: SUFFICIENT_FOR_SYNTHETIC_PILOT (11/14)`

**[OSSERVATO]** Su Bolt.new README, stesso tool ha prodotto `INSUFFICIENT` 0/14 OBSERVED.
- Command: `python3 tools/automations/brain-collector.py --input /tmp/bolt.new/README.md --output /tmp/scan-bolt/candidate-bolt.yaml --domain-id bolt-new`
- Evidence: euristica regex italiana, non adatta a README inglese — limite dichiarato

**[OSSERVATO]** `inventory-documents.py` ha schema `open-nexus.document-index/v1` con output `INDEX-MANIFEST.json, DOCUMENT-INVENTORY.jsonl, DOCUMENT-INVENTORY.csv, INVENTORY-REPORT.md, COMMAND-LEDGER.md`.
- Evidence: `cat tools/documentation/inventory-documents.py | grep "SCHEMA_VERSION\|OUTPUT_FILES" | head -5`

---

## 2. INFERITO — interpretazioni, marcate

**[INFERITO]** Moat opportunities su Bolt.new: VALIDATE gate prima di writeFile, SourceObservation+content_sha+provenance, audit trail, residuo che compone M-04, clean-room manifest F08-014.
- Base: `NEXUS-LAB/SORGENTI/SCANSIONE-BOLT-NEW.md` §4
- Confidence: medium — valutazione manuale, non da comando, marcata INFERITO
- Falsificazione: se Bolt.new implementa già gate deterministico con content_sha e provenance, opportunità decade

**[INFERITO]** 80% clonabile (parser, runner, workbench), 20% non clonabile WebContainers infra.
- Base: tabella clonabilità in `SCANSIONE-BOLT-NEW.md` §3
- Confidence: medium — stima, non misurazione

**[INFERITO]** Glossario etimologico con binario sviluppo suo (g-audit-domain, prometeo-rifiuti-domain, foundation-domain, semantic-entity-domain) evita contaminazione.
- Base: `ADR-0016` + `EPIC-0.9.0` §10 branch strategy
- Confidence: high — principio ownership da Foundation

---

## 3. LIMITE — cosa non è stato possibile determinare

- Diritti registrati su termini Artifact/Action/WebContainer
- Effettivo costo di esecuzione ActionRunner in WebContainer (non misurato)
- Efficacia reale cache 304 su fonti Prometeo (non testato su URL live, solo repo)
- Compatibilità `ApplicationAuthoringSpec` con Foundation 0.8.x corrente (richiede audit CLI-008 completo su foundation repo, non su nexus-lab docs)
- Se Bolt.new ha già provenance nascosta in db.ts (non letto in profondità)

---

## 4. Matrice — contratti usati vs stato

| File prodotto | Contratto usato | Fonte doc | Stato contratto | Classe | Verificabilità |
|---|---|---|---|---|---|
| EVIDENCE.jsonl (f08-audit) | Principio R3.1 "Zero risultati senza comando non è un dato" | 05-EVALUATION.md §3 | Principio | 0 | Comando + output troncato 2000 chars, manca collected_at derivato |
| candidate-prometeo.yaml | CandidateDomainSpec §8 + epistemic states §5 + sufficiency §6 + dimensions §7 | 09-DOMAIN-ACQUISITION.md | ILLUSTRATIVO, NOT YET STABLE | 0 | Regex italiana, non LLM, manca sourceRefs locator preciso |
| 2026-09-14.jsonl (468 rec) | 6 campi minimi §11 + RawEvidenceBlob→SourceObservation→Candidate→Canonical | 06-STORAGE + ON-ACQ-2026-1.0 | PROPOSTA, adapter iniziale | 0 | source_url file:// non http, excerpt 500 chars, non RawEvidenceBlob completo |
| BOLT-SCAN-REPORT.md | OSSERVATO/INFERITO/LIMITE + K1-K8 + M-02..M-06 | 05 + 27-SCORING + 23-MOAT | Report, non record | 0 + Brain manuale | Parte deterministica (find, cat), parte manuale INFERITO |
| GLOSSARY-ETYMOLOGY.jsonl | ownership + branch strategy | ADR-0016 + EPIC-0.9.0 §10 | Euristica | 0 | git log --grep euristica, development_binary PROPOSTO |

---

## 5. Proposta — cosa fare, con condizione di falsificazione

**[PROPOSTA]** Implementare `HttpHtmlConnector` vero con `PublicTargetPolicy` + `Fetched` + `content_sha` + `304` + `COMMAND-LEDGER`.

- Falsificazione: se su 5 fonti Prometeo reali, 0% risponde 304 e content_sha cambia sempre per timestamp, allora conditional request non è leva 20× e va deprioritizzato.

**[PROPOSTA]** Implementare `opnx scan` come comando CLI che incapsula `scan-project-layout.py` + `brain-collector.py` con promotion gate esplicito umano, mai auto-canonical.

- Falsificazione: se secondo run con stesso input + stesso metodo produce record con <80% overlap, metodo non è ripetibile e va corretto prima di promozione.

**[PROPOSTA]** Primo pilot interno post-0.8.2 su un solo dossier approvato (24-SCANSIONE-PER-CAPACITA.md) con flusso 10 passi (preserva SHA, parsing deterministico, candidate claims, human review, rigenera matrice, confronta, PageData).

- Falsificazione: se matrice rigenerata ha multiplo o banda diversa da originale oltre tolleranza, parsing o interpretazione ha introdotto drift.

---

## 6. Cosa NON proponiamo

- Auto-ingestion di conversazioni in canonical store (REJECTED per self-reinforcing loop)
- Auto-promotion di output Brain a verità (REJECTED)
- Headless browser, proxy rotation, ML extraction in Classe 0 (vietati da 11 §5.3)
- Mescolare binari di sviluppo (g-audit, prometeo, foundation, semantic-entity) prima di secondo caso indipendente

---

## 7. Provenance

```
Tool: collect-epistemic-records.py + brain-collector.py + scan-project-layout.py + f08-audit.py
Tool version: 0.1.0
Model_id_resolved: none (Classe 0, nessun LLM)
Collected_at: 2026-10-09T18:59:00Z (derivato)
Source: risposta agent 2026-10-09T18:59 + NEXUS-LAB/*.md + /tmp/bolt.new
Transformation: summarized + computed
Epistemic: CANDIDATE — GENERATED_SOURCE
Promotion: richiede human review esplicita
```

---

*Codificato il 2026-10-09 — segue 05-EVALUATION.md checklist §9: marcatori, riferimenti, stime marcate INFERITO con base, limiti in sezione propria, nessun punteggio numerico confidenza, criterio dichiarato prima, verdetto con condizioni, falsificazione scritta, passo 13 eseguito (contraddizione/coincidenza: Bolt Artifact/Action vs Open Nexus Bundle/Page — stesso pattern, diverso gate), dichiarazioni terzi marcate, nessun antipattern §8*
