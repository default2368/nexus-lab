#!/usr/bin/env python3
"""
F08-001 Audit delle authority e impatto ADR
Classe 0, deterministico, nessun LLM.
Produce Impact Matrix come report 0.8, non come overview normativa.

Usage:
  python3 tools/automations/f08-audit.py --repo /path/to/foundation --output /tmp/f08-audit
  python3 tools/automations/f08-audit.py --repo . --output /tmp/f08-audit --mock  (usa questo repo se foundation non presente)

Output:
  IMPACT-MATRIX.md
  COMMAND-LEDGER.md
  EVIDENCE.jsonl
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

PROTECTED_KERNEL = [
    "PageController",
    "normalizeToPageData",
    "ApplicationDefinition",
    "ApplicationContext",
    "BundleCollector",
    "DiscoveryService",
    "DiscoveryServiceV2",
    "PageData",
]

AUDIT_COMMANDS = [
    ("ADR files", "find docs -type f -iname 'ADR-*' 2>/dev/null | sort"),
    ("createApplicationDefinition", "git grep -n \"createApplicationDefinition\" 2>/dev/null | head -20"),
    ("ApplicationDefinition", "git grep -n \"ApplicationDefinition\" 2>/dev/null | head -30"),
    ("ApplicationBundle", "git grep -n \"ApplicationBundle\" 2>/dev/null | head -30"),
    ("PageMeta", "git grep -n \"PageMeta\" 2>/dev/null | head -20"),
    ("WebPageTemplate", "git grep -n \"WebPageTemplate\" 2>/dev/null | head -20"),
    ("PAGES_REGISTRY", "git grep -n \"PAGES_REGISTRY\" 2>/dev/null | head -20"),
    ("virtualProvider", "git grep -n \"virtualProvider\\|virtual-provider\" 2>/dev/null | head -20"),
    ("access policies", "git grep -n \"PUBLIC\\|PROTECTED\\|LANDING\\|HIDDEN\" 2>/dev/null | head -30"),
    ("physical pages", "git grep -n \"physical/main/chat\\|physical/main/home-pages\" 2>/dev/null | head -20"),
    ("assistant/discovery", "git grep -n \"simple/assistant\\|core-admin/discovery-pages\" 2>/dev/null | head -20"),
]

def run_cmd(cmd: str, cwd: Path) -> tuple[str, int]:
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()[:8000], result.returncode
    except Exception as e:
        return f"ERROR: {e}", 1

def main():
    parser = argparse.ArgumentParser(description="F08-001 Audit")
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mock", action="store_true", help="mock mode if foundation repo not present")
    args = parser.parse_args()

    repo = args.repo.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    ledger = [f"# F08-001 Command Ledger", f"Generated: {datetime.now().isoformat()}", f"Repo: {repo}", "", "## Commands executed", ""]
    evidences = []
    matrix_lines = [
        "# F08-001 Impact Matrix — Authority Audit",
        f"Generated: {datetime.now().isoformat()}",
        f"Repo: {repo}",
        "",
        "## Protected Kernel Check",
        "",
        "| Symbol | Found | Risk |",
        "|---|---|---|",
    ]

    # Check protected kernel modifications via git diff
    for sym in PROTECTED_KERNEL:
        cmd = f"git diff HEAD -- \"*{sym}*\" 2>/dev/null | head -20"
        out, code = run_cmd(cmd, repo)
        found = "MODIFIED" if out else "CLEAN"
        risk = "BLOCKER" if out else "OK"
        matrix_lines.append(f"| {sym} | {found} | {risk} |")
        evidences.append({"symbol": sym, "cmd": cmd, "output": out[:2000], "status": found})
        ledger.append(f"```bash\n{cmd}\n```\nOutput: {len(out)} chars\n")

    matrix_lines.extend(["", "## Authority Claims Verification", "", "| Claim | Command | Evidence | Status |", "|---|---|---|---|"])

    for label, cmd in AUDIT_COMMANDS:
        out, code = run_cmd(cmd, repo)
        status = "EVIDENCE" if out else "NOT_FOUND"
        # Truncate for table
        ev_short = out.splitlines()[0][:80] if out else "—"
        matrix_lines.append(f"| {label} | `{cmd[:40]}...` | {ev_short} | {status} |")
        evidences.append({"label": label, "cmd": cmd, "output": out[:5000], "status": status})
        ledger.append(f"### {label}\n```bash\n{cmd}\n```\n```\n{out[:3000]}\n```\n")

    # Physical routes classification
    matrix_lines.extend(["", "## Physical Routes Classification", "", "| Route | Classification | Owner | Action |", "|---|---|---|---|"])
    physical_checks = [
        ("physical/main/chat", "LEGACY_APPLICATION", "simple/assistant", "RETIRE"),
        ("physical/main/home-pages", "LEGACY_APPLICATION", "core-admin/discovery-pages", "RETIRE"),
        ("physical/debug/status", "INFRASTRUCTURE", "Operations", "PRESERVE"),
        ("physical/debug/debug-theme", "DEBUG", "TemplateLab", "MOVE"),
        ("physical/debug/debug-auth", "DEBUG", "Auth", "RETIRE"),
    ]
    for route, cls, owner, action in physical_checks:
        matrix_lines.append(f"| {route} | {cls} | {owner} | {action} |")

    # Write outputs
    (output / "IMPACT-MATRIX.md").write_text("\n".join(matrix_lines), encoding="utf-8")
    (output / "COMMAND-LEDGER.md").write_text("\n".join(ledger), encoding="utf-8")
    with (output / "EVIDENCE.jsonl").open("w", encoding="utf-8") as f:
        for ev in evidences:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")

    print(json.dumps({"status": "AUDIT_COMPLETE", "output": str(output), "evidences": len(evidences)}, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
