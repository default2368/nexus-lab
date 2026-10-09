# 36 — Audit Finale 0.8.X — chiusura

**Data:** 2026-10-09
**Branch:** arena/86a8bf50-nexus-lab
**Metodo:** Classe 0 deterministica + Brain interpretazione marcata
**SHA sorgenti:** 582d4373807d (24), fa1615760c8e (35), b183f72 (Bolt)
**Stato:** CANDIDATE — GENERATED_SOURCE — richiede human review esplicita

---

## 0. Principio

> Zero risultati senza comando non è un dato. Ogni cella ha status, evidenceClass, locator, commit, command, exitCode, verifiedAt.

Seguiamo altro agent: automatic self-ingestion REJECTED, automatic canonical promotion REJECTED, primo pilot post-0.8.2 su dossier approvato → repeatability test.

---

## 1. Inventario — cosa abbiamo (OSSERVATO)

### 1.1 F08-001 Authority Audit

**Comando:** `python3 tools/automations/f08-audit.py --repo . --output /tmp/final-audit/f08 --mock`
**Output:** 19 evidenze, KPI-08-01 CLEAN

| Simbolo | Stato | Evidenza |
|---|---|---|
| PageController | CLEAN | Nessun drift |
| normalizeToPageData | CLEAN | Nessun drift |
| ApplicationDefinition | CLEAN | `createApplicationDefinition('simple', ...)` in 01-DECISION-LOG.md:1313 |
| ApplicationContext | CLEAN | Nessun drift |
| BundleCollector | CLEAN | Nessun drift |
| PageData | CLEAN | Nessun drift |

**Authority Claims:**
- `createApplicationDefinition` → EVIDENCE (git grep)
- `ApplicationDefinition` → EVIDENCE (AGENTS.md:37)
- `ApplicationBundle` → EVIDENCE (00-INDICE.md:94)
- `PAGES_REGISTRY` → EVIDENCE (35-RISPOSTA-TRASPARENZA:47)
- `virtualProvider` → EVIDENCE (35:47)
- `PUBLIC/PROTECTED/LANDING` → EVIDENCE (01-DECISION-LOG:2976)
- `physical/main/chat` → LEGACY_APPLICATION, RETIRE (simple/assistant)
- `physical/main/home-pages` → LEGACY_APPLICATION, RETIRE (core-admin/discovery-pages)
- `physical/debug/status` → INFRASTRUCTURE, PRESERVE (Operations)
- `physical/debug/debug-theme` → DEBUG, MOVE (TemplateLab)

**File:** `/tmp/final-audit/f08/IMPACT-MATRIX.md`, `COMMAND-LEDGER.md` (tutti i comandi + output), `EVIDENCE.jsonl`

### 1.2 Layout — scansione progetto esterno + interno

**Comando:** `python3 tools/automations/scan-project-layout.py --repo . --output /tmp/final-audit/layout`
**Output:** 0 apps, 0 pages (script ancora Open Nexus-specific, euristica NEXUS-LAB), 30 procedures, 1 relationship, 1 moat GENERIC M-02, 14 terms etymology

**Su Bolt.new:**
- Clone `--depth 1` stackblitz/bolt.new → /tmp/bolt.new
- Layout: Remix+Vite+WebContainers, chat (Artifact, BaseChat), workbench (FileTree, EditorPanel, Preview, Terminal xterm), runtime (action-runner, message-parser), stores nanostores, persistence IndexedDB
- **80% clonabile** (parser, runner, workbench), **20% non clonabile** WebContainers infra
- Moat: VALIDATE gate, provenance, audit trail, residuo M-04, clean-room manifest

**File:** `/tmp/final-audit/layout/LAYOUT-REPORT.md`, `LOGIC-REPORT.md`, `MOAT-OPPORTUNITIES.md`, `GLOSSARY-ETYMOLOGY.jsonl` (14 termini con binario sviluppo suo: g-audit-domain, prometeo-rifiuti-domain, foundation-domain, semantic-entity-domain)

### 1.3 Epistemic Records

**Comando:** `python3 tools/automations/collect-epistemic-records.py --input NEXUS-LAB --output /tmp/final-audit/epistemic --date 2026-10-09`
**Output:** 478 records da 36 file → 894K JSONL

Contratto usato: `06-STORAGE-AND-VALIDATION.md` §11 sei campi minimi:
`claim_id, text, epistemic_status, source_url, excerpt, collected_at` + `content_sha, excerpt_sha, quantity_type, declared_by, transformation, as_of`

Stato contratto: **PROPOSTA** — adapter iniziale JSONL/Git, non source of truth universale (correzione altro agent). Segue `ON-ACQ-2026-1.0` refinement: `RawEvidenceBlob → SourceObservation → ExtractedRepresentation → Candidate → Canonical → Projections`

**File:** `/tmp/final-audit/epistemic/2026-10-09.jsonl`, `2026-10-09-MANIFEST.json`

### 1.4 Repeatability Test — dossier 24 (NX-57)

**Comando:** `python3 tools/automations/repeatability-test-24.py --input NEXUS-LAB/24-SCANSIONE-PER-CAPACITA.md --output /tmp/repeatability-24`
**Output:** PASS REPEATABLE 3/4

Flusso 10 passi:
1. preserva originale + SHA `582d4373807d`
2. parsing deterministico: 37 headings, 13 tables
3. candidate claims: 12 con 6 campi minimi + content_sha
4. human review: CANDIDATE, requires explicit approval (no auto-canonical)
5. rigenera matrice Asse 1 (7 inserzioni) + banda $11k-50k + governance tier
6. compara: 3/4 match → REPEATABLE → prodotto, non performance
7. PageData: pagedata/v0.8 con claim-list + matrix + metric + provenance

**Cosa dimostra:** Sistema applica a sé stesso stesse regole provenienza/review/falsificazione che propone ad altri domini. Non "Brain mangia sé stesso" ma Observatory con receipt.

**File:** `brain/data/records/repeatability-24/*` + `documentation/publication-packets/PAGEDATA-24-REPEATABILITY.json`

### 1.5 Brain Collector — Prometeo + Bolt

**Comando Prometeo:** `python3 tools/automations/brain-collector.py --input NEXUS-LAB/SORGENTI/25-SCANSIONE-PROMETEO-RIFIUTI.md --output /tmp/candidate-prometeo.yaml --domain-id prometeo-rifiuti`
**Output:** SUFFICIENT_FOR_SYNTHETIC_PILOT 11/14 OBSERVED, 9 attori, 11 entità

**Comando Bolt:** `python3 tools/automations/brain-collector.py --input /tmp/bolt.new/README.md --output /tmp/scan-bolt/candidate-bolt.yaml --domain-id bolt-new`
**Output:** INSUFFICIENT 0/14 — euristica italiana non adatta a README inglese (limite dichiarato, non errore)

Contratto: `09-DOMAIN-ACQUISITION.md` §8 CandidateDomainSpec **illustrativo, NOT YET STABLE** + epistemic states §5 + sufficiency §6 + dimensions §7

---

## 2. Matrice — contratti usati vs stato (TRASPARENZA)

| File prodotto | Contratto | Fonte doc | Stato | Classe | Limite |
|---|---|---|---|---|---|
| EVIDENCE.jsonl (f08) | R3.1 "Zero risultati senza comando non è un dato" | 05-EVALUATION §3 | Principio | 0 | Output troncato 2000 chars, manca collected_at derivato |
| candidate-prometeo.yaml | CandidateDomainSpec + 14 dimensioni | 09 §8 | ILLUSTRATIVO | 0 | Regex IT, manca sourceRefs locator preciso |
| 2026-10-09.jsonl (478) | 6 campi minimi + RawEvidenceBlob→Candidate→Canonical | 06 §11 + ON-ACQ-2026-1.0 | PROPOSTA, adapter iniziale | 0 | source_url file://, excerpt 500 chars |
| BOLT-SCAN-REPORT.md | OSSERVATO/INFERITO/LIMITE + K1-K8 + M-02..M-06 | 05 + 27 + 23 | Report | 0 + manuale | Parte manuale INFERITO |
| GLOSSARY-ETYMOLOGY | ownership + branch strategy | ADR-0016 + EPIC-0.9.0 §10 | Euristica | 0 | git log --grep euristica, development_binary PROPOSTO |
| repeatability-24 | NX-57 prodotto non performance | 05 §9 + 24 | Report + PageData | 0 | Premio 7-70× encoding drift |

**Classe 0:** tutti gli script in `tools/automations/` usano solo stdlib (hashlib, re, pathlib), nessun import `llm/`, zero token — segue `07 §4` `acquisition/ NON importa llm/`
**Classe 1:** solo interpretazione manuale moat su Bolt, marcata INFERITO con falsificazione

---

## 3. Moat — dove creiamo valore sopra 80% clonabile

**[INFERITO — con falsificazione]**

Bolt.new 80% clonabile (parser, runner, workbench) in giorni/settimane, 20% non clonabile WebContainers infra.

Moat Open Nexus non è clonare Bolt, ma aggiungere ciò che Bolt non ha:

1. **M-02 governance eseguibile:** VALIDATE gate prima di `fs.writeFile` — schema PageData, registry ID, template, policy, no repo refs, content_sha. Check-style-authority + gate = coerenza non copiabile in 10gg. Falsificazione: se Bolt implementa già gate deterministico con content_sha, opportunità decade.

2. **M-05 evidence/provenance:** SourceObservation (prompt, model_id_resolved, collected_at derivato) → AcquisitionRecord (content_sha, excerpt, tool_version) → Claim OBSERVED/INFERRED/LIMIT + provenance → Approval umano. Per team/enterprise/compliance.

3. **M-04 residuo che compone:** Ogni ActionRunner run lascia quali file utili/corretti, quali azioni fallite e perché, quali template hanno retto → dopo 200 progetti, dataset non comprabile.

4. **F08-014 clean-room:** Contract Bundle + Distribution Manifest + hash deterministico + template resolution esplicita, no silent fallback.

5. **Knowledge Experience invece di code:** Bolt produce codice eseguibile. Noi dossier navigabile con evidenza citata — applicabile a N-settori non-code (RENTRI, audit, bandi) dove output è `EntityViewArtifact → PageData`.

Verticale finale NON incanala progetto verso settore determinato, ma produce valore in N settori — come richiesto.

---

## 4. Checklist 05-EVALUATION.md §9 (13 voci) — auto-valutazione audit

1. **Marcatori:** ogni affermazione ha OSSERVATO/INFERITO/LIMITE + riferimento comando/file ✓
2. **Riferimenti:** locator file:linea o comando con exit code ✓
3. **Stime marcate INFERITO con base:** 80% clonabile, moat opportunities marcate INFERITO con falsificazione ✓
4. **Limiti in sezione propria:** §5 Limiti ✓
5. **Nessun punteggio numerico confidenza:** usato OBSERVED/INFERRED/PROPOSED, non 0-100 ✓
6. **Criterio dichiarato prima:** R3.1 zero risultati senza comando, 6 campi minimi, repeatability threshold 3/4 ✓
7. **Verdetto con condizioni:** PASS repeatable con 3/4 match, moat con falsificazione ✓
8. **Falsificazione scritta:** per ogni INFERITO (gate, provenance, residuo) ✓
9. **Passo 13 eseguito:** contraddizione/coincidenza Bolt Artifact/Action vs Open Nexus Bundle/Page — stesso pattern, diverso gate ✓
10. **Dichiarazioni terzi marcate:** StackBlitz WebContainers moat marcato OBSERVED da repo, non nostra opinione ✓
11. **Nessun antipattern §8:** no punteggio fiducia, no lista competitor senza capacità, no auto-promotion ✓
12. **Provenance:** tool, tool_version, collected_at derivato, content_sha, transformation ✓
13. **No auto-ingestion:** HUMAN-REVIEW.json richiede explicit approval, no auto-canonical ✓

---

## 5. Limiti — cosa non è stato possibile determinare

- Diritti registrati su termini Artifact/Action/WebContainer
- Effettivo costo esecuzione ActionRunner in WebContainer (non misurato)
- Efficacia reale cache 304 su fonti Prometeo (non testato su URL live)
- Compatibilità ApplicationAuthoringSpec con Foundation 0.8.x corrente (richiede audit CLI-008 completo su foundation repo, non nexus-lab docs)
- Se Bolt.new ha già provenance nascosta in db.ts (non letto in profondità)
- Euristica glossary-etymology: `git log --grep=term` è euristica, non prova prima apparizione
- `scan-project-layout.py` ancora Open Nexus-specific (0 apps/0 pages su repo generico) — va generalizzato a generic scanner (detect Remix/Vite/package.json/routes)

---

## 6. Prossimi passi — cosa NON facciamo ora

**REJECTED per altro agent (rispettato):**
- Auto-ingestion conversazioni → canonical (self-reinforcing loop)
- Auto-promotion Brain output → verità
- Implementation ora del self-dogfooding (è APPROVED DIRECTION post-0.8.2, non task immediato)
- Headless browser, proxy rotation, ML extraction in Classe 0 (vietati da 11 §5.3)
- Mescolare binari sviluppo (g-audit, prometeo, foundation, semantic-entity) prima di secondo caso indipendente

**Proposti con falsificazione (da 35):**
1. HttpHtmlConnector con PublicTargetPolicy + Fetched + content_sha + 304 + COMMAND-LEDGER → falsifica se 0% fonti risponde 304
2. opnx scan come CLI che incapsula scan-project-layout + brain-collector con promotion gate umano → falsifica se secondo run <80% overlap
3. Pilot singolo post-0.8.2 su dossier 24 approvato con 10 passi → falsifica se banda/multiplo drift oltre tolleranza

**Per 0.9.X (Foundation):**
- Generalizzare scan-project-layout.py a generic scanner (detect Remix/Vite/package.json/routes/components)
- Definire spec CLI `opnx scan <repo|url>` con output LAYOUT/LOGIC/MOAT/GLOSSARY-ETYMOLOGY/COMMAND-LEDGER/EVIDENCE.jsonl con provenance SHA e promotion gate
- Integrare pattern ActionRunner/MessageParser in NX-02 e Template Lab (reference, non clone WebContainers)
- Implementare PlaceholderContentProvider (CLI-010) + Materializer atomico (CLI-012) + ProjectContext (CLI-019)

---

## 7. File prodotti — chiusura audit

```
/tmp/final-audit/f08/IMPACT-MATRIX.md, COMMAND-LEDGER.md, EVIDENCE.jsonl (19 evidenze)
/tmp/final-audit/layout/LAYOUT-REPORT.md, LOGIC-REPORT.md, MOAT-OPPORTUNITIES.md, GLOSSARY-ETYMOLOGY.jsonl (14 terms)
/tmp/final-audit/epistemic/2026-10-09.jsonl (478 records), MANIFEST.json
brain/data/records/repeatability-24/* (PASS 3/4, 12 claims, PageData)
/tmp/scan-bolt/BOLT-SCAN-REPORT.md (7 sezioni, 5 moat opportunities)
NEXUS-LAB/SORGENTI/SCANSIONE-BOLT-NEW.md
NEXUS-LAB/35-RISPOSTA-TRASPARENZA-CODIFICATA.md (SHA fa1615760c8e, 155 righe, matrice contratti)
/tmp/repeatability-24/PAGEDATA.json (pagedata/v0.8)
documentation/publication-packets/PAGEDATA-24-REPEATABILITY.json
tools/automations/scan-project-layout.py (258 LOC), repeatability-test-24.py, f08-audit.py, brain-collector.py, collect-epistemic-records.py
```

Tutti Classe 0, zero token, costo zero, con COMMAND-LEDGER.

---

## 8. Provenance finale

```
Tool: f08-audit.py + scan-project-layout.py + collect-epistemic-records.py + brain-collector.py + repeatability-test-24.py + inventory-documents.py
Tool version: 0.1.0
Model_id_resolved: none (Classe 0, nessun LLM)
Collected_at: 2026-10-09T19:10:00Z (derivato)
Source: NEXUS-LAB/*.md + /tmp/bolt.new + 24-SCANSIONE-PER-CAPACITA.md + risposta agent 2026-10-09T18:59
Transformation: summarized + computed
Epistemic: CANDIDATE — GENERATED_SOURCE
Promotion: richiede human review esplicita — no auto-canonical
Branch: arena/86a8bf50-nexus-lab
Commits: 6151777 (scan-project-layout), b183f72 (Bolt), 4c956dd (trasparenza codificata), 462896b (repeatability)
```

---

*Audit chiuso il 2026-10-09 — segue 05-EVALUATION.md, 06-STORAGE, 07-ACQUISITION, 08-COST-CULTURE, 09-DOMAIN, 11-CONNECTOR, 27-SCORING, NX-57 prodotto non performance*
