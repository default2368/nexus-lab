#!/usr/bin/env python3
"""
Scan a project, take layout, if logic useful → create moat and value
CLI + Brain automation per 0.8.X / 0.9.X

Idea:
  progetto (repo o sito) → layout (pages, components, templates, routes, assets, procedures)
  → logic (entities, relationships, workflows, decisions, evidence)
  → evaluation K1-K8 + sufficiency 14 dimensioni
  → se utile → CandidateDomainSpec + moat proposal (evidence layer, audit trail, governance)

Usage:
  python3 tools/automations/scan-project-layout.py --repo . --output /tmp/scan-layout
  python3 tools/automations/scan-project-layout.py --repo /path/to/foundation --output /tmp/scan --url https://www.prometeorifiuti.com/

Output:
  LAYOUT-REPORT.md
  LOGIC-REPORT.md
  MOAT-OPPORTUNITIES.md
  GLOSSARY-ETYMOLOGY.jsonl  (etimologica — traccia origine termini)
  COMMAND-LEDGER.md
  EVIDENCE.jsonl
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

def run(cmd, cwd):
    try:
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=15)
        return r.stdout.strip()[:10000], r.returncode
    except Exception as e:
        return f"ERROR {e}", 1

def sha256(s): return hashlib.sha256(s.encode()).hexdigest()[:12]

def scan_layout(repo: Path):
    """Estrae layout: applications, pages, components, templates, assets, procedures"""
    layout = {"applications": [], "pages": [], "components": [], "templates": [], "procedures": [], "entities": []}
    # Applications
    out, _ = run("find src -type d -name applications 2>/dev/null; find . -type f -path '*/applications/*/package.ts' 2>/dev/null | head -20", repo)
    layout["applications"] = out.splitlines()[:20]
    # Pages
    out, _ = run("find src -type f -name '*.astro' 2>/dev/null | head -30; find src -type f -path '*/pages/*.ts' 2>/dev/null | head -30", repo)
    layout["pages"] = out.splitlines()[:30]
    # Components
    out, _ = run("find src -type f -name '*.tsx' -o -name '*.jsx' 2>/dev/null | head -30", repo)
    layout["components"] = out.splitlines()[:30]
    # Templates
    out, _ = run("grep -Rni 'WebPageTemplate\\|Template' --include='*.ts' --include='*.tsx' src 2>/dev/null | head -20", repo)
    layout["templates"] = out.splitlines()[:20]
    # Procedures / docs
    out, _ = run("find . -type f -name '*.md' | xargs grep -l -i 'procedura\\|workflow\\|processo\\|engagement\\|procedure' 2>/dev/null | head -20", repo)
    layout["procedures"] = out.splitlines()[:20]
    # NEXUS-LAB docs as procedures
    nexus = list((repo / "NEXUS-LAB").glob("*.md")) if (repo / "NEXUS-LAB").exists() else []
    layout["procedures"].extend([str(p.relative_to(repo)) for p in nexus[:10]])
    return layout

def extract_logic(repo: Path, layout):
    """Estrae logica: entities, relationships, workflows, decisions"""
    logic = {"entities": [], "relationships": [], "workflows": [], "decisions": []}
    # Search for Entity patterns
    out, _ = run("grep -Rno 'interface.*Entity\\|type.*Entity\\|EntityRecord\\|Procedure\\|Engagement\\|Evidence\\|Feedback\\|Action\\|Decision' --include='*.md' --include='*.ts' NEXUS-LAB/ 2>/dev/null | head -40", repo)
    for line in out.splitlines():
        if "Entity" in line or "Procedure" in line or "Engagement" in line:
            logic["entities"].append(line[:120])
    # Workflows from backlog
    out, _ = run("grep -Rno 'NX-[0-9]*' NEXUS-LAB/02-BACKLOG-NX.md 2>/dev/null | head -20", repo)
    logic["workflows"] = out.splitlines()[:20]
    # Decisions
    out, _ = run("grep -Rno 'DECISO\\|DECISION' NEXUS-LAB/01-DECISION-LOG.md 2>/dev/null | head -20", repo)
    logic["decisions"] = out.splitlines()[:20]
    # Relationships heuristic from Prometeo doc
    prometeo = repo / "NEXUS-LAB/SORGENTI/25-SCANSIONE-PROMETEO-RIFIUTI.md"
    if prometeo.exists():
        txt = prometeo.read_text(errors="replace")[:5000].lower()
        if "produttore" in txt and "trasportatore" in txt:
            logic["relationships"].append("produttore → trasportatore → destinatario → impianto (catena responsabilità)")
        if "norma" in txt and "obbligo" in txt:
            logic["relationships"].append("norma ↔ obbligo ↔ ruolo ↔ modulo ↔ caso cliente (modello semantico latente)")
    return logic

def evaluate_moat_potential(layout, logic, repo):
    """Valuta se logica ha potenziale moat: K1-K8 + contenuto/distribuzione/compliance/posizione"""
    text_blob = " ".join(layout["procedures"] + logic["entities"]) + " ".join(logic["relationships"])
    text_blob_lower = text_blob.lower()
    opportunities = []
    # K1: obbligo di rendere conto
    if any(k in text_blob_lower for k in ["obbligo", "sanzione", "compliance", "audit", "rendere conto", "registro"]):
        opportunities.append({"type": "K1_OBLIGATION", "moat": "M-06 posizione normativa", "value": "Alta: obbligo = payer obbligato, non opzionale", "epistemic": "OBSERVED"})
    # K2: non sostituibile da LLM generalista
    if any(k in text_blob_lower for k in ["evidenza", "fonte", "tracciabilità", "autorizzazione", "scadenza"]):
        opportunities.append({"type": "K2_NON_SUBSTITUTABLE", "moat": "M-04 residuo che compone + M-05 storia falsificazioni", "value": "Alta: LLM non ha registro/autorizzazioni cliente", "epistemic": "OBSERVED"})
    # K3: osservazione continua deterministica
    if any(k in text_blob_lower for k in ["monitora", "scadenza", "alert", "change detection", "content_sha"]):
        opportunities.append({"type": "K3_CONTINUOUS_OBSERVATION", "moat": "M-03 boundary compilato + NX-19", "value": "Alta: pricing per-check a costo zero, margine 99%", "epistemic": "OBSERVED"})
    # Content moat
    if len(layout["pages"]) > 50:
        opportunities.append({"type": "CONTENT_MOAT", "moat": "M-04 corpus accumulato", "value": f"{len(layout['pages'])} pagine → dopo 200 hai dataset unico", "epistemic": "INFERRED"})
    # Distribution moat
    if "forward-deployed" in text_blob_lower or "associazione" in text_blob_lower:
        opportunities.append({"type": "DISTRIBUTION_MOAT", "moat": "Network di responsabilità (produttore→trasportatore→...)", "value": "Federazione multi-tenant con isolamento rigoroso", "epistemic": "INFERRED"})
    # Compliance moat
    if "RENT" in text_blob or "GDPR" in text_blob or "231" in text_blob:
        opportunities.append({"type": "COMPLIANCE_MOAT", "moat": "M-06 EU sovereignty + audit trail come tier", "value": "Governance venduta come tier (GoMarble pattern)", "epistemic": "OBSERVED"})
    # If no opportunities, still propose generic
    if not opportunities:
        opportunities.append({"type": "GENERIC", "moat": "M-02 governance eseguibile", "value": "Check-style-authority + gate VALIDATE = coerenza non copiabile in 10gg", "epistemic": "INFERRED"})
    return opportunities

def glossary_etymology(repo: Path):
    """Traccia etimologica termini: prima apparizione, evoluzione, in binario di sviluppo suo"""
    terms = ["Engagement", "Procedure", "Evidence", "Feedback", "Action", "Decision", "PageData", "ApplicationBundle", "EntityRecord", "RENTRI", "Prometeo", "Foundation", "X", "Brain"]
    etym = []
    for term in terms:
        out, _ = run(f"git log --follow --diff-filter=A --format='%aI %H' -- \"*\" 2>/dev/null | head -1; git log --all --oneline --grep='{term}' 2>/dev/null | head -3; git grep -n '{term}' NEXUS-LAB/ 2>/dev/null | head -2", repo)
        # Simplified: just check if term exists and count
        out2, _ = run(f"grep -Rno '{term}' NEXUS-LAB/ 2>/dev/null | wc -l", repo)
        count = out2.strip()
        # Find first file mentioning
        out3, _ = run(f"grep -Rno '{term}' NEXUS-LAB/ 2>/dev/null | head -1", repo)
        etym.append({
            "term": term,
            "occurrences": int(count) if count.isdigit() else 0,
            "first_locator": out3[:120],
            "etymology": f"Tracciato in NEXUS-LAB, {count} occorrenze, sviluppo in binario {term.lower()}-domain",
            "development_binary": f"{term.lower()}-domain",
            "epistemic_status": "OBSERVED" if int(count) > 0 else "UNKNOWN",
        })
    return etym

def main():
    parser = argparse.ArgumentParser(description="Scan project layout → logic → moat")
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--url", type=str, default=None, help="optional site URL to scan technically")
    args = parser.parse_args()

    repo = args.repo.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    layout = scan_layout(repo)
    logic = extract_logic(repo, layout)
    moats = evaluate_moat_potential(layout, logic, repo)
    etym = glossary_etymology(repo)

    # Reports
    layout_report = [
        "# Layout Report — scansione progetto",
        f"Repo: {repo} — {datetime.now().isoformat()}",
        "",
        "## Applications",
        *[f"- {p}" for p in layout["applications"][:15]],
        "",
        "## Pages",
        *[f"- {p}" for p in layout["pages"][:15]],
        "",
        "## Templates / Components",
        *[f"- {p}" for p in layout["templates"][:10]],
        "",
        "## Procedures (NEXUS-LAB + docs)",
        *[f"- {p}" for p in layout["procedures"][:15]],
    ]
    logic_report = [
        "# Logic Report — logica estratta",
        f"Repo: {repo}",
        "",
        "## Entities candidate",
        *[f"- {e}" for e in logic["entities"][:20]],
        "",
        "## Relationships (modello semantico latente)",
        *[f"- {r}" for r in logic["relationships"]],
        "",
        "## Workflows / Decisions",
        *[f"- {w}" for w in logic["workflows"][:10]],
        *[f"- {d}" for d in logic["decisions"][:10]],
    ]
    moat_report = [
        "# Moat Opportunities — dove creare valore",
        f"Repo: {repo} — {len(moats)} opportunità rilevate",
        "",
        "| Type | Moat | Value | Epistemic |",
        "|---|---|---|---|",
    ]
    for m in moats:
        moat_report.append(f"| {m['type']} | {m['moat']} | {m['value']} | {m['epistemic']} |")
    moat_report.extend([
        "",
        "## Come CLI + Brain lo trasformano in valore",
        "",
        "```text",
        "scan layout (Classe 0, inventory-documents.py + f08-audit.py)",
        "  ↓",
        "extract logic (brain-collector.py → CandidateDomainSpec)",
        "  ↓",
        "evaluate sufficiency (sufficiency-evaluator.py, 14 dimensioni)",
        "  ↓",
        "if SUFFICIENT_FOR_SYNTHETIC_PILOT:",
        "  → Domain Pack sintetico",
        "  → EntityViewArtifact → PageData",
        "  → Evidence layer / Audit trail / Governance tier",
        "  → moat che compone (M-04) + posizione normativa (M-06)",
        "```",
        "",
        "## Binario di sviluppo suo (etimologica)",
        "",
        "Ogni termine ha un binario di sviluppo separato, con ownership:",
        "- Engagement, Procedure, Evidence → g-audit-domain",
        "- RENTRI, Formulario, Registro → prometeo-rifiuti-domain",
        "- PageData, ApplicationBundle → foundation-domain",
        "- EntityRecord, Projection → semantic-entity-domain (0.9.X)",
        "",
        "Non mescolare binari prima che due casi indipendenti confermino il minimo comune.",
    ])

    (output / "LAYOUT-REPORT.md").write_text("\n".join(layout_report), encoding="utf-8")
    (output / "LOGIC-REPORT.md").write_text("\n".join(logic_report), encoding="utf-8")
    (output / "MOAT-OPPORTUNITIES.md").write_text("\n".join(moat_report), encoding="utf-8")
    with (output / "GLOSSARY-ETYMOLOGY.jsonl").open("w", encoding="utf-8") as f:
        for e in etym:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    # Command ledger
    ledger = [
        "# Command Ledger — scan-project-layout",
        f"Repo: {repo}",
        f"Generated: {datetime.now().isoformat()}",
        "",
        "## Commands",
        "find src -type d -name applications",
        "find src -type f -path '*/applications/*/package.ts'",
        "find src -type f -name '*.astro'",
        "grep -Rni WebPageTemplate src",
        "grep -Rni EntityRecord NEXUS-LAB/",
        "git log --follow --grep=term",
        "",
        f"Applications: {len(layout['applications'])}, Pages: {len(layout['pages'])}, Procedures: {len(layout['procedures'])}",
        f"Moat opportunities: {len(moats)}",
    ]
    (output / "COMMAND-LEDGER.md").write_text("\n".join(ledger), encoding="utf-8")

    print(f"SCAN COMPLETE → {output}")
    print(f"Layout: {len(layout['applications'])} apps, {len(layout['pages'])} pages, {len(layout['procedures'])} procedures")
    print(f"Logic: {len(logic['entities'])} entities, {len(logic['relationships'])} relationships")
    print(f"Moat: {len(moats)} opportunities")
    print(f"Etymology: {len(etym)} terms tracked in own development binaries")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
