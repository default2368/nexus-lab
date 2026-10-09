#!/usr/bin/env python3
"""
DA-02 Sufficiency Evaluator — valuta se una sorgente è sufficiente per modellare un dominio
Segue 09-DOMAIN-ACQUISITION-AND-CANDIDATE-MODELING.md §6-7

Dimensioni valutate (14):
Purpose, Actors, Objects, Workflow, States, Decisions, Evidence, Relationships, Operations, Access, Exceptions, Examples, Provenance, Sensitivity

Livelli:
INSUFFICIENT / SUFFICIENT_FOR_GLOSSARY / SUFFICIENT_FOR_CANDIDATE_MODEL / SUFFICIENT_FOR_SYNTHETIC_PILOT / SUFFICIENT_FOR_IMPLEMENTATION_REVIEW

Usage:
  python3 tools/automations/sufficiency-evaluator.py --input uploads/03-opennexus-verticale-rifiuti.txt --output /tmp/suff.json
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from datetime import datetime

DIMENSIONS = {
    "Purpose": {"keywords": ["scopo", "obiettivo", "produce", "risultato", "serve a"], "question": "What result does the activity produce?"},
    "Actors": {"keywords": ["attore", "ruolo", "responsabilità", "chi", "produttore", "trasportatore"], "question": "Who participates and with what responsibility?"},
    "Objects": {"keywords": ["registro", "formulario", "documento", "oggetto", "entità", "MUD", "RENTRI"], "question": "What is created, received, modified or preserved?"},
    "Workflow": {"keywords": ["workflow", "processo", "fase", "step", "inizio", "chiusura", "flusso"], "question": "What starts the activity and what closes it?"},
    "States": {"keywords": ["stato", "lifecycle", "attivo", "chiuso", "scadenza", "validità"], "question": "Which lifecycle states do the main objects traverse?"},
    "Decisions": {"keywords": ["decisione", "approvazione", "chi decide", "approva", "firma"], "question": "Who decides, when and on the basis of what evidence?"},
    "Evidence": {"keywords": ["evidenza", "fonte", "prova", "citazione", "allegato"], "question": "Which documents or facts support actions and decisions?"},
    "Relationships": {"keywords": ["relazione", "collega", "rete", "→", "verso", "produttore.*trasportatore"], "question": "What is related to what, and why?"},
    "Operations": {"keywords": ["crea", "modifica", "archivia", "operazione", "comando", "azione"], "question": "What may be created, changed, linked, archived or approved?"},
    "Access": {"keywords": ["accesso", "visibilità", "tenant", "permesso", "ruolo", "privacy"], "question": "Who may see or modify each class of information?"},
    "Exceptions": {"keywords": ["eccezione", "errore", "anomalia", "mancante", "incompleto"], "question": "What happens when the normal path fails?"},
    "Examples": {"keywords": ["esempio", "caso", "testimonianza", "scenario", "cliente"], "question": "Is at least one complete synthetic or sanitized case available?"},
    "Provenance": {"keywords": ["fonte", "data", "versione", "tracciabilità", "storico"], "question": "Can each material statement be traced to a source?"},
    "Sensitivity": {"keywords": ["privacy", "riservato", "sensibile", "GDPR", "confidenziale"], "question": "Does the source contain personal, confidential or regulated data?"},
}

def evaluate(text: str):
    text_lower = text.lower()
    results = {}
    for dim, meta in DIMENSIONS.items():
        hits = []
        for kw in meta["keywords"]:
            if re.search(kw, text_lower):
                hits.append(kw)
        if len(hits) >= 3:
            status = "OBSERVED"
            confidence = "high"
        elif len(hits) >= 1:
            status = "INFERRED"
            confidence = "medium"
        else:
            status = "UNKNOWN"
            confidence = "low"
        results[dim] = {
            "status": status,
            "hits": hits[:5],
            "question": meta["question"],
            "confidence": confidence,
            "epistemicStatus": status,
        }
    observed = sum(1 for r in results.values() if r["status"] == "OBSERVED")
    inferred = sum(1 for r in results.values() if r["status"] == "INFERRED")
    if observed >= 10:
        level = "SUFFICIENT_FOR_SYNTHETIC_PILOT"
    elif observed >= 7:
        level = "SUFFICIENT_FOR_CANDIDATE_MODEL"
    elif observed >= 4:
        level = "SUFFICIENT_FOR_GLOSSARY"
    else:
        level = "INSUFFICIENT"

    # What is missing to unlock next level
    missing_for_next = []
    for dim, r in results.items():
        if r["status"] == "UNKNOWN":
            missing_for_next.append(f"{dim}: {r['question']}")

    return {
        "level": level,
        "observed": observed,
        "inferred": inferred,
        "unknown": 14 - observed - inferred,
        "dimensions": results,
        "missing_for_next_level": missing_for_next[:5],
        "evaluatedAt": datetime.now().isoformat(),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8", errors="replace")
    result = evaluate(text)
    result["source"] = str(args.input)
    result["sourceChars"] = len(text)

    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Sufficiency: {result['level']} — {result['observed']}/14 OBSERVED, {result['inferred']} INFERRED, {result['unknown']} UNKNOWN")
    if result["missing_for_next_level"]:
        print("Missing for next level:")
        for m in result["missing_for_next_level"]:
            print(f"  - {m}")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
