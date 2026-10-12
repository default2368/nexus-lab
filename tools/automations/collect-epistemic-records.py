#!/usr/bin/env python3
"""
NX-56 — NEXUS-LAB/*.md → brain/records/*.jsonl
Trasforma i 34 documenti di brainstorming in epistemic records validati per 06-STORAGE-AND-VALIDATION.md

Ogni record ha i 6 campi minimi obbligatori:
claim_id, text, epistemic_status, source_url, excerpt, collected_at

Usage:
  python3 tools/automations/collect-epistemic-records.py --input NEXUS-LAB --output brain/records/nexus-lab/ --date 2026-09-14
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from datetime import datetime, timezone

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def extract_claims_from_md(md_path: Path):
    text = md_path.read_text(encoding="utf-8", errors="replace")
    claims = []
    # Estrai blocchi con OSSERVATO / INFERITO / LIMITE o con tabelle
    # Semplice: ogni heading + paragrafo successivo è un claim candidato
    lines = text.splitlines()
    current_heading = md_path.stem
    buffer = []
    for line in lines:
        if line.startswith("#"):
            if buffer:
                para = "\n".join(buffer).strip()
                if len(para) > 40 and len(para) < 2000:
                    # Determina epistemic status da parole chiave
                    lower = para.lower()
                    if any(k in lower for k in ["verificato", "evidenza", "comando", "file", "misurato", "osservato"]):
                        status = "OBSERVED"
                    elif any(k in lower for k in ["ipotesi", "probabile", "sembra", "inferito", "stimato"]):
                        status = "INFERRED"
                    elif any(k in lower for k in ["non è stato possibile", "limite", "manca", "sconosciuto"]):
                        status = "LIMIT"
                    else:
                        status = "INFERRED"
                    claims.append({
                        "heading": current_heading,
                        "text": para[:2000],
                        "status": status,
                        "excerpt": para[:500],
                    })
                buffer = []
            current_heading = line.lstrip("# ").strip()[:80]
        else:
            if line.strip() and not line.strip().startswith("```"):
                buffer.append(line.strip())
    return claims

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True, help="NEXUS-LAB dir")
    parser.add_argument("--output", type=Path, required=True, help="output dir for jsonl")
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()

    input_dir = args.input.resolve()
    output_dir = args.output.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    all_records = []
    for md_file in sorted(input_dir.glob("*.md")):
        if md_file.name.startswith("00-INDICE"):
            continue
        claims = extract_claims_from_md(md_file)
        for idx, claim in enumerate(claims[:20]):  # max 20 per file per non esplodere
            record = {
                "claim_id": f"{md_file.stem.upper()}-{idx:03d}",
                "text": claim["text"],
                "epistemic_status": claim["status"],
                "source_url": f"file://{md_file.relative_to(input_dir.parent)}",
                "source_locator": f"{md_file.name}:{claim['heading']}",
                "excerpt": claim["excerpt"],
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "collection_action": "markdown_extraction",
                "tool_id": "collect-epistemic-records.py",
                "tool_version": "0.1.0",
                "content_sha": sha256(claim["text"]),
                "excerpt_sha": sha256(claim["excerpt"]),
                "quantity_type": "none",
                "declared_by": "us",
                "transformation": "summarized",
                "as_of": args.date,
                "as_of_note": f"extracted from {md_file.name}",
            }
            all_records.append(record)

    # Write JSONL per date
    out_file = output_dir / f"{args.date}.jsonl"
    with out_file.open("w", encoding="utf-8") as f:
        for rec in all_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # Also write manifest
    manifest = {
        "schemaVersion": "open-nexus.claim-record/v0.1",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceDir": str(input_dir),
        "records": len(all_records),
        "outputFile": str(out_file),
        "filesProcessed": len(list(input_dir.glob("*.md"))),
        "rule": "text is source authority, embedding is projection, record is source of truth",
    }
    (output_dir / f"{args.date}-MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Collected {len(all_records)} records from {len(list(input_dir.glob('*.md')))} files → {out_file}")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
