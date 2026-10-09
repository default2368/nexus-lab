#!/usr/bin/env python3
"""
Brain Collector of Procedures — trasforma procedure documentate in Candidate Domain Definition
Segue 09-DOMAIN-ACQUISITION-AND-CANDIDATE-MODELING.md

Epistemic states: OBSERVED / INFERRED / PROPOSED / UNKNOWN / CONFLICTING
Sufficiency: INSUFFICIENT / SUFFICIENT_FOR_GLOSSARY / SUFFICIENT_FOR_CANDIDATE_MODEL / SUFFICIENT_FOR_SYNTHETIC_PILOT / SUFFICIENT_FOR_IMPLEMENTATION_REVIEW

Usage:
  python3 tools/automations/brain-collector.py --input NEXUS-LAB/SORGENTI/25-SCANSIONE-PROMETEO-RIFIUTI.md --output /tmp/candidate-prometeo.yaml
  python3 tools/automations/brain-collector.py --input uploads/03-opennexus-verticale-rifiuti.txt --output /tmp/candidate.yaml --domain-id g-audit

Output: CandidateDomainSpec YAML (illustrative structure, non ancora stable contract per 09)
"""
from __future__ import annotations
import argparse
import re
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import Counter

# Simple heuristics, Classe 0, nessun LLM

ACTOR_PATTERNS = [
    r"\b(produttore|trasportatore|destinatario|intermediario|consulente|associazione|cliente|auditor|approver|responsabile|titolare|operatore|autista)\b",
    r"\b(CTO|CEO|manager|CFO|broker|avvocato|funzionario)\b",
]
ENTITY_PATTERNS = [
    r"\b(registro|formulario|MUD|RENTRI|autorizzazione|giacenza|contratto|preventivo|DDT|rapportino|fattura|magazzino|EER|CER|Engagement|ProcedureVersion|WorkItem|Questionnaire|Evidence|Feedback|Action|Decision|Approval|Deliverable)\b",
]
COMMAND_PATTERNS = [
    r"\b(crea|genera|compila|verifica|approva|chiudi|archivia|invia|conferma|pianifica|controlla|monitora)\b",
]

SUFFICIENCY_DIMENSIONS = [
    "Purpose", "Actors", "Objects", "Workflow", "States", "Decisions",
    "Evidence", "Relationships", "Operations", "Access", "Exceptions",
    "Examples", "Provenance", "Sensitivity"
]

def extract_terms(text: str, patterns: list[str]) -> list[str]:
    terms = []
    for pat in patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            terms.append(m.group(0).lower())
    return sorted(set(terms))

def evaluate_sufficiency(text: str) -> dict:
    # Very simple heuristic: check presence of dimension keywords
    scores = {}
    text_lower = text.lower()
    for dim in SUFFICIENCY_DIMENSIONS:
        keywords = {
            "Purpose": ["scopo", "obiettivo", "produce", "risultato"],
            "Actors": ["attore", "ruolo", "responsabilità", "chi"],
            "Objects": ["registro", "formulario", "documento", "oggetto", "entità"],
            "Workflow": ["workflow", "processo", "fase", "step", "inizio", "chiusura"],
            "States": ["stato", "lifecycle", "attivo", "chiuso", "scadenza"],
            "Decisions": ["decisione", "approvazione", "chi decide", "approva"],
            "Evidence": ["evidenza", "fonte", "prova", "documento", "citazione"],
            "Relationships": ["relazione", "collega", "→", "verso", "rete"],
            "Operations": ["crea", "modifica", "archivia", "operazione"],
            "Access": ["accesso", "visibilità", "tenant", "permesso"],
            "Exceptions": ["eccezione", "errore", "anomalia", "mancante"],
            "Examples": ["esempio", "caso", "testimonianza", "scenario"],
            "Provenance": ["fonte", "data", "versione", "tracciabilità"],
            "Sensitivity": ["privacy", "riservato", "sensibile", "GDPR"],
        }.get(dim, [dim.lower()])
        count = sum(1 for k in keywords if k in text_lower)
        scores[dim] = "OBSERVED" if count >= 2 else ("INFERRED" if count == 1 else "UNKNOWN")

    observed = sum(1 for v in scores.values() if v == "OBSERVED")
    if observed >= 10:
        level = "SUFFICIENT_FOR_SYNTHETIC_PILOT"
    elif observed >= 7:
        level = "SUFFICIENT_FOR_CANDIDATE_MODEL"
    elif observed >= 4:
        level = "SUFFICIENT_FOR_GLOSSARY"
    else:
        level = "INSUFFICIENT"
    return {"level": level, "dimensions": scores, "observed_count": observed}

def build_candidate(text: str, domain_id: str, source_path: str) -> dict:
    actors = extract_terms(text, ACTOR_PATTERNS)
    entities = extract_terms(text, ENTITY_PATTERNS)
    commands = extract_terms(text, COMMAND_PATTERNS)
    suff = evaluate_sufficiency(text)

    # Extract glossary from markdown headings
    glossary = []
    for line in text.splitlines():
        m = re.match(r"^#{1,3}\s+(.+)", line)
        if m:
            title = m.group(1).strip()
            if len(title) < 60 and len(title) > 3:
                glossary.append(title)

    # Build candidate relationships heuristically
    relationships = []
    if "produttore" in actors and "trasportatore" in actors:
        relationships.append({"source": "produttore", "relation": "consegna_a", "target": "trasportatore", "epistemicStatus": "OBSERVED"})
    if "trasportatore" in actors and "destinatario" in actors:
        relationships.append({"source": "trasportatore", "relation": "consegna_a", "target": "destinatario", "epistemicStatus": "OBSERVED"})
    if "engagement" in text.lower() and "evidence" in text.lower():
        relationships.append({"source": "Engagement", "relation": "hasEvidence", "target": "Evidence", "epistemicStatus": "OBSERVED"})

    # Gaps = UNKNOWN dimensions
    gaps = [f"{dim}: evidenza insufficiente per modellare {dim.lower()}" for dim, st in suff["dimensions"].items() if st == "UNKNOWN"]
    # Assumptions = INFERRED
    assumptions = [f"{dim}: interpretazione plausibile ma non canonica" for dim, st in suff["dimensions"].items() if st == "INFERRED"]

    candidate = {
        "schemaVersion": "candidate-domain/v0.1",
        "generatedAt": datetime.now().isoformat(),
        "sourceRef": source_path,
        "status": suff["level"],
        "domain": {"id": domain_id, "title": domain_id.replace("-", " ").title()},
        "actors": [{"id": a, "epistemicStatus": "OBSERVED"} for a in actors[:15]],
        "candidateEntities": [{"id": e, "epistemicStatus": "OBSERVED"} for e in entities[:20]],
        "candidateRelationships": relationships,
        "candidateCommands": [{"id": c, "epistemicStatus": "INFERRED"} for c in commands[:10]],
        "glossary": glossary[:20],
        "assumptions": [{"statement": s, "epistemicStatus": "INFERRED", "confidence": "medium"} for s in assumptions[:8]],
        "gaps": gaps[:8],
        "conflicts": [],
        "sufficiency": suff,
        "sources": [{"sourceId": Path(source_path).name, "sections": ["workflow", "responsibilities", "evidence"]}],
        "nextActions": [
            "Verificare K4: censimento incumbent (cosa fanno, cosa non fanno, cosa costano)",
            "Colloquio con esperto di dominio sulle 13 domande (bisogni e payer, non pitch)",
            "Produrre un caso sintetico completo con stati attraversati e approvazioni",
        ],
        "provenance": {
            "collector": "brain-collector.py v0.1",
            "method": "deterministic heuristics, Classe 0, nessun LLM",
            "epistemicRule": "Brain interprets and proposes. Human corrects meaning. Authoring validates.",
        }
    }
    return candidate

def to_yaml(data: dict, indent=0) -> str:
    # Minimal YAML serializer without external deps
    lines = []
    pad = "  " * indent
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{pad}{k}:")
                lines.append(to_yaml(v, indent+1))
            else:
                # escape
                val = json.dumps(v, ensure_ascii=False) if isinstance(v, str) and ("\n" in v or ":" in v) else (str(v) if not isinstance(v, str) else v)
                if isinstance(v, str) and len(v) > 80:
                    lines.append(f"{pad}{k}: |")
                    for l in v.splitlines():
                        lines.append(f"{pad}  {l}")
                else:
                    lines.append(f"{pad}{k}: {val}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}-")
                lines.append(to_yaml(item, indent+1))
            else:
                lines.append(f"{pad}- {item}")
    else:
        lines.append(f"{pad}{data}")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Brain Collector of Procedures")
    parser.add_argument("--input", type=Path, required=True, help="input procedure doc")
    parser.add_argument("--output", type=Path, required=True, help="output candidate YAML")
    parser.add_argument("--domain-id", type=str, default="prometeo-rifiuti", help="domain id")
    parser.add_argument("--json", action="store_true", help="also output JSON")
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8", errors="replace")
    candidate = build_candidate(text, args.domain_id, str(args.input))

    # Write YAML (simple)
    yaml_content = f"""# Candidate Domain Definition — {args.domain_id}
# Generated: {candidate['generatedAt']}
# Source: {args.input}
# Status: {candidate['status']}
# Rule: Brain proposes, Human corrects, Authoring validates

status: {candidate['status']}
domain:
  id: {candidate['domain']['id']}
  title: {candidate['domain']['title']}

actors:
"""
    for a in candidate["actors"]:
        yaml_content += f"  - id: {a['id']}\n    epistemicStatus: {a['epistemicStatus']}\n"
    yaml_content += "\ncandidateEntities:\n"
    for e in candidate["candidateEntities"]:
        yaml_content += f"  - id: {e['id']}\n    epistemicStatus: {e['epistemicStatus']}\n"
    yaml_content += "\ncandidateRelationships:\n"
    for r in candidate["candidateRelationships"]:
        yaml_content += f"  - source: {r['source']}\n    relation: {r['relation']}\n    target: {r['target']}\n    epistemicStatus: {r['epistemicStatus']}\n"
    yaml_content += f"\nsufficiency:\n  level: {candidate['sufficiency']['level']}\n  observed_count: {candidate['sufficiency']['observed_count']}\n  dimensions:\n"
    for dim, st in candidate["sufficiency"]["dimensions"].items():
        yaml_content += f"    {dim}: {st}\n"
    yaml_content += "\ngaps:\n"
    for g in candidate["gaps"]:
        yaml_content += f"  - {g}\n"
    yaml_content += "\nassumptions:\n"
    for a in candidate["assumptions"]:
        yaml_content += f"  - statement: {a['statement']}\n    epistemicStatus: {a['epistemicStatus']}\n"
    yaml_content += "\nnextActions:\n"
    for na in candidate["nextActions"]:
        yaml_content += f"  - {na}\n"

    args.output.write_text(yaml_content, encoding="utf-8")
    if args.json:
        Path(str(args.output)+".json").write_text(json.dumps(candidate, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"CANDIDATE_DOMAIN generated: {args.output}")
    print(f"Status: {candidate['status']} ({candidate['sufficiency']['observed_count']}/14 dimensions OBSERVED)")
    print(f"Actors: {len(candidate['actors'])}, Entities: {len(candidate['candidateEntities'])}, Relationships: {len(candidate['candidateRelationships'])}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
