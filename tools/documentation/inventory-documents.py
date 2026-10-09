#!/usr/bin/env python3
"""Build a read-only, Git-aware documentation index.

The tool reads a Git repository and writes an inventory to an explicit output
folder outside that repository. It never stages, commits, pushes, or modifies
source files.

Only Python's standard library is required.
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence
from urllib.parse import urlsplit, urlunsplit

SCHEMA_VERSION = "open-nexus.document-index/v1"
OUTPUT_FILES = (
    "INDEX-MANIFEST.json",
    "DOCUMENT-INVENTORY.jsonl",
    "DOCUMENT-INVENTORY.csv",
    "INVENTORY-REPORT.md",
    "COMMAND-LEDGER.md",
)

TASK_ID_RE = re.compile(
    r"\b(?:ADR|PRD|EPIC|BACKLOG|PLAN|PROMPT|SURF|PROV|SEC|OPS|REPO|VIS|ENG|ACQ|DOC-TOOL|F\d{2})"
    r"-[A-Z0-9][A-Z0-9._-]*\b",
    re.IGNORECASE,
)
VERSION_RE = re.compile(r"\bv\d+\.\d+(?:\.\d+)?(?:[-+][A-Za-z0-9.-]+)?\b")
COMMIT_RE = re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{7,40}(?![0-9a-fA-F])")

STATUS_PATTERNS = (
    re.compile(r"^status\s*:\s*(.+?)\s*$", re.IGNORECASE),
    re.compile(r"^\*\*status:\*\*\s*(.+?)\s*$", re.IGNORECASE),
    re.compile(r"^lifecycle state\s*:\s*(.+?)\s*$", re.IGNORECASE),
    re.compile(r"^\*\*lifecycle state:\*\*\s*(.+?)\s*$", re.IGNORECASE),
)

SENSITIVITY_PATTERNS = (
    ("PRIVATE_KEY_BLOCK", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("POSSIBLE_GITHUB_TOKEN", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("POSSIBLE_AWS_ACCESS_KEY", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("POSSIBLE_BEARER_TOKEN", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}\b", re.IGNORECASE)),
    (
        "POSSIBLE_SECRET_ASSIGNMENT",
        re.compile(
            r"\b(?:api[_-]?key|secret|token|password|passwd)\b\s*[:=]\s*[\"']?[^\s\"']{12,}",
            re.IGNORECASE,
        ),
    ),
    ("POSSIBLE_EMAIL", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)),
)


class IndexError(RuntimeError):
    """Expected validation or repository error."""


@dataclass(frozen=True)
class GitResult:
    stdout: str
    stderr: str
    returncode: int


class Git:
    def __init__(self, repository: Path) -> None:
        self.requested_repository = repository.resolve()
        root_result = self.run_raw(
            self.requested_repository,
            ["rev-parse", "--show-toplevel"],
            check=False,
        )
        if root_result.returncode != 0 or not root_result.stdout.strip():
            raise IndexError(f"not a Git worktree: {self.requested_repository}")
        self.root = Path(root_result.stdout.strip()).resolve()

    @staticmethod
    def run_raw(cwd: Path, args: Sequence[str], check: bool = True) -> GitResult:
        completed = subprocess.run(
            ["git", *args],
            cwd=cwd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        result = GitResult(completed.stdout, completed.stderr, completed.returncode)
        if check and completed.returncode != 0:
            safe_command = "git " + " ".join(args[:3])
            raise IndexError(f"{safe_command} failed: {completed.stderr.strip()}")
        return result

    def run(self, args: Sequence[str], check: bool = True) -> GitResult:
        return self.run_raw(self.root, args, check=check)

    def text(self, args: Sequence[str], check: bool = True) -> str:
        return self.run(args, check=check).stdout.strip()

    def ref_commit(self, ref: str) -> str | None:
        result = self.run(["rev-parse", "--verify", f"{ref}^{{commit}}"], check=False)
        return result.stdout.strip() if result.returncode == 0 else None

    def object_at_path(self, ref: str, relative_path: str) -> str | None:
        result = self.run(["rev-parse", "--verify", f"{ref}:{relative_path}"], check=False)
        return result.stdout.strip() if result.returncode == 0 else None

    def content_at_path(self, ref: str, relative_path: str) -> bytes | None:
        completed = subprocess.run(
            ["git", "show", f"{ref}:{relative_path}"],
            cwd=self.root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        return completed.stdout if completed.returncode == 0 else None


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def load_config(path: Path) -> dict[str, Any]:
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise IndexError(f"configuration not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise IndexError(f"invalid JSON configuration: {exc}") from exc

    required = ("schemaVersion", "projectId", "repositoryId", "documentRoots")
    missing = [key for key in required if key not in config]
    if missing:
        raise IndexError("configuration missing: " + ", ".join(missing))
    if config["schemaVersion"] != 1:
        raise IndexError("unsupported configuration schemaVersion")
    if not isinstance(config["documentRoots"], list) or not config["documentRoots"]:
        raise IndexError("documentRoots must be a non-empty array")
    return config


def path_is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def sanitize_remote(remote: str | None) -> str | None:
    if not remote:
        return None
    remote = remote.strip()
    if "://" in remote:
        split = urlsplit(remote)
        host = split.hostname or ""
        port = f":{split.port}" if split.port else ""
        return urlunsplit((split.scheme, host + port, split.path, "", ""))
    # SCP-like SSH URL: git@github.com:owner/repository.git
    if "@" in remote and ":" in remote.split("@", 1)[1]:
        host_and_path = remote.split("@", 1)[1]
        host, path = host_and_path.split(":", 1)
        return f"ssh://{host}/{path}"
    return remote


def configured_remote(git: Git, config: dict[str, Any]) -> tuple[str, str | None]:
    remote_name = str(config.get("remoteName", "origin"))
    result = git.run(["remote", "get-url", remote_name], check=False)
    remote = sanitize_remote(result.stdout.strip() if result.returncode == 0 else None)
    return remote_name, remote


def verify_repository_identity(git: Git, config: dict[str, Any]) -> tuple[str, str | None]:
    remote_name, remote = configured_remote(git, config)
    required_path = config.get("requiredRemotePath")
    if required_path:
        normalized_required = "/" + str(required_path).strip("/")
        normalized_remote = (remote or "").rstrip("/")
        if not normalized_remote.endswith(normalized_required):
            raise IndexError(
                "BLOCKED_WRONG_REPOSITORY: configured remote does not match "
                f"{normalized_required}"
            )
    return remote_name, remote


def should_exclude(relative_path: str, patterns: Sequence[str]) -> bool:
    return any(fnmatch.fnmatch(relative_path, pattern) for pattern in patterns)


def enumerate_documents(git: Git, config: dict[str, Any]) -> list[Path]:
    extensions = {str(value).lower() for value in config.get("extensions", [".md", ".mdx", ".txt"])}
    excludes = list(config.get("excludeGlobs", []))
    max_bytes = int(config.get("maxFileBytes", 2 * 1024 * 1024))
    candidates: set[Path] = set()

    configured_paths = list(config["documentRoots"]) + list(config.get("includeFiles", []))
    for configured_path in configured_paths:
        candidate = (git.root / configured_path)
        if not candidate.exists():
            continue
        if candidate.is_symlink():
            continue
        paths: Iterable[Path]
        if candidate.is_file():
            paths = (candidate,)
        else:
            paths = candidate.rglob("*")
        for path in paths:
            if path.is_symlink() or not path.is_file():
                continue
            resolved = path.resolve()
            if not path_is_within(resolved, git.root):
                continue
            relative = resolved.relative_to(git.root).as_posix()
            if should_exclude(relative, excludes):
                continue
            if resolved.suffix.lower() not in extensions:
                continue
            if resolved.stat().st_size > max_bytes:
                continue
            candidates.add(resolved)

    return sorted(candidates, key=lambda value: value.relative_to(git.root).as_posix())


def parse_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return fallback


def parse_declared_status(text: str) -> str | None:
    in_frontmatter = False
    for index, raw_line in enumerate(text.splitlines()[:120]):
        line = raw_line.strip()
        if index == 0 and line == "---":
            in_frontmatter = True
            continue
        if in_frontmatter and line == "---":
            in_frontmatter = False
            continue
        candidate = line.strip("` ")
        for pattern in STATUS_PATTERNS:
            match = pattern.match(candidate)
            if match:
                return match.group(1).strip().strip("*`") or None
    return None


def classify_document(relative_path: str) -> str:
    name = Path(relative_path).name.upper()
    prefixes = (
        "ADR",
        "PRD",
        "EPIC",
        "BACKLOG",
        "PLAN",
        "PROMPT",
        "REPORT",
        "GUIDE",
        "RUNBOOK",
        "README",
        "AGENTS",
    )
    for prefix in prefixes:
        if name.startswith(prefix):
            return prefix
    lowered = relative_path.lower()
    if "/governance/" in f"/{lowered}":
        return "GOVERNANCE"
    if "/reports/" in f"/{lowered}":
        return "REPORT"
    if "/plans/" in f"/{lowered}":
        return "PLAN"
    return "OTHER"


def extract_references(text: str) -> dict[str, list[str]]:
    return {
        "taskIds": sorted({match.upper() for match in TASK_ID_RE.findall(text)}),
        "versions": sorted(set(VERSION_RE.findall(text))),
        "commitShas": sorted({match.lower() for match in COMMIT_RE.findall(text)}),
    }


def sensitivity_findings(text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for finding_type, pattern in SENSITIVITY_PATTERNS:
            if pattern.search(line):
                findings.append({"type": finding_type, "line": line_number})
    return findings


def file_git_state(git: Git, relative_path: str) -> str:
    status = git.text(["status", "--porcelain=v1", "--untracked-files=all", "--", relative_path], check=False)
    if not status:
        return "CLEAN"
    first = status.splitlines()[0]
    code = first[:2]
    if code == "??":
        return "UNTRACKED"
    if "D" in code:
        return "DELETED"
    if "R" in code:
        return "RENAMED"
    if "A" in code:
        return "ADDED"
    return "MODIFIED"


def git_history(git: Git, relative_path: str) -> dict[str, str | None]:
    result = git.run(
        ["log", "--follow", "--format=%H%x09%aI", "--", relative_path],
        check=False,
    )
    entries: list[tuple[str, str | None]] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 1)
        entries.append((parts[0], parts[1] if len(parts) > 1 else None))
    if not entries:
        return {
            "firstCommit": None,
            "firstCommitTime": None,
            "lastCommit": None,
            "lastCommitTime": None,
        }
    last_commit, last_time = entries[0]
    first_commit, first_time = entries[-1]
    return {
        "firstCommit": first_commit,
        "firstCommitTime": first_time,
        "lastCommit": last_commit,
        "lastCommitTime": last_time,
    }


def build_record(
    git: Git,
    config: dict[str, Any],
    path: Path,
    resolved_baselines: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    relative_path = path.relative_to(git.root).as_posix()
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    tracked = git.run(["ls-files", "--error-unmatch", "--", relative_path], check=False).returncode == 0
    head_blob = git.object_at_path("HEAD", relative_path) if tracked else None
    head_content = git.content_at_path("HEAD", relative_path) if head_blob else None
    history = git_history(git, relative_path) if tracked else git_history(git, relative_path)

    at_refs: list[dict[str, Any]] = []
    for baseline in resolved_baselines:
        ref = baseline["ref"]
        commit = baseline.get("commit")
        blob = git.object_at_path(ref, relative_path) if commit else None
        at_refs.append(
            {
                "ref": ref,
                "commit": commit,
                "present": blob is not None,
                "blobOid": blob,
            }
        )

    findings = sensitivity_findings(text)
    return {
        "schemaVersion": SCHEMA_VERSION,
        "projectId": config["projectId"],
        "repositoryId": config["repositoryId"],
        "path": relative_path,
        "documentKey": path.stem,
        "title": parse_title(text, path.stem),
        "documentType": classify_document(relative_path),
        "declaredStatus": parse_declared_status(text),
        "bytes": len(raw),
        "lineCount": len(text.splitlines()),
        "contentSha256": sha256_bytes(raw),
        "git": {
            "tracked": tracked,
            "worktreeState": file_git_state(git, relative_path),
            "headBlobOid": head_blob,
            "headContentSha256": sha256_bytes(head_content) if head_content is not None else None,
            **history,
            "atRefs": at_refs,
        },
        "references": extract_references(text),
        "sensitivityFindings": findings,
    }


def duplicate_groups(records: Sequence[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for record in records:
        value = record.get(field)
        if value:
            groups[str(value)].append(record["path"])
    return [
        {field: value, "paths": sorted(paths)}
        for value, paths in sorted(groups.items())
        if len(paths) > 1
    ]


def duplicate_task_groups(records: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for record in records:
        for task_id in record["references"]["taskIds"]:
            groups[task_id].append(record["path"])
    return [
        {"taskId": task_id, "paths": sorted(set(paths))}
        for task_id, paths in sorted(groups.items())
        if len(set(paths)) > 1
    ]


def markdown_cell(value: Any) -> str:
    if value is None:
        return "—"
    return str(value).replace("|", "\\|").replace("\n", " ")


def build_report(manifest: dict[str, Any], records: Sequence[dict[str, Any]]) -> str:
    git_info = manifest["git"]
    lines = [
        "# Foundation Documentation Inventory",
        "",
        f"**Schema:** `{SCHEMA_VERSION}`  ",
        f"**Project:** `{manifest['projectId']}`  ",
        f"**Repository:** `{manifest['repositoryId']}`  ",
        f"**Branch:** `{git_info['branch']}`  ",
        f"**HEAD:** `{git_info['head']}`  ",
        f"**Source origin:** `{git_info['sourceCommitOrigin']}`  ",
        f"**Documents:** `{manifest['counts']['documents']}`",
        "",
        "This report is an inventory projection. It does not promote a document to canonical authority.",
        "",
        "## Git references",
        "",
        "| Ref | Commit | Available |",
        "|---|---|---:|",
    ]
    for baseline in git_info["baselineRefs"]:
        lines.append(
            f"| `{markdown_cell(baseline['ref'])}` | `{markdown_cell(baseline.get('commit'))}` | "
            f"{str(bool(baseline.get('available'))).lower()} |"
        )

    lines.extend(
        [
            "",
            "## Documents",
            "",
            "| Path | Type | Declared status | Git state | Last commit | SHA-256 | Findings |",
            "|---|---|---|---|---|---|---:|",
        ]
    )
    for record in records:
        last_commit = record["git"].get("lastCommit")
        lines.append(
            f"| `{markdown_cell(record['path'])}` | {markdown_cell(record['documentType'])} | "
            f"{markdown_cell(record.get('declaredStatus'))} | {record['git']['worktreeState']} | "
            f"`{last_commit[:12] if last_commit else '—'}` | `{record['contentSha256'][:12]}` | "
            f"{len(record['sensitivityFindings'])} |"
        )

    lines.extend(["", "## Review findings", ""])
    findings = manifest["findings"]
    lines.append(f"- Exact duplicate groups: `{len(findings['exactDuplicates'])}`")
    lines.append(f"- Same-name groups: `{len(findings['sameNameCandidates'])}`")
    lines.append(f"- Multi-document task references: `{len(findings['multiDocumentTaskReferences'])}`")
    lines.append(f"- Possible sensitive/PII findings: `{manifest['counts']['sensitivityFindings']}`")
    lines.append(f"- Untracked documents: `{manifest['counts']['untrackedDocuments']}`")
    lines.append(f"- Modified documents: `{manifest['counts']['modifiedDocuments']}`")

    if findings["exactDuplicates"]:
        lines.extend(["", "### Exact duplicates", ""])
        for group in findings["exactDuplicates"]:
            lines.append(f"- `{group['contentSha256']}`: " + ", ".join(f"`{path}`" for path in group["paths"]))
    if findings["sameNameCandidates"]:
        lines.extend(["", "### Same-name candidates", ""])
        for group in findings["sameNameCandidates"]:
            lines.append(f"- `{group['documentKey']}`: " + ", ".join(f"`{path}`" for path in group["paths"]))

    lines.extend(
        [
            "",
            "## Interpretation rule",
            "",
            "```text",
            "Script measures.",
            "Agent proposes.",
            "Owner decides.",
            "Git preserves.",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def build_command_ledger(args: argparse.Namespace, manifest: dict[str, Any]) -> str:
    baselines = ", ".join(item["ref"] for item in manifest["git"]["baselineRefs"]) or "none"
    return "\n".join(
        [
            "# Documentation Inventory Command Ledger",
            "",
            f"**Tool schema:** `{SCHEMA_VERSION}`  ",
            f"**Project:** `{manifest['projectId']}`  ",
            f"**HEAD:** `{manifest['git']['head']}`  ",
            f"**Source origin:** `{manifest['git']['sourceCommitOrigin']}`",
            "",
            "## Invocation",
            "",
            "```text",
            "python3 tools/documentation/inventory-documents.py \\",
            "  --repo <foundation-repository> \\",
            "  --config tools/documentation/projects/foundation.json \\",
            "  --output <external-output-directory>" + (" \\\n  --require-clean" if args.require_clean else ""),
            "```",
            "",
            "## Read operations",
            "",
            "```text",
            "git rev-parse / symbolic-ref / status / remote",
            "git ls-files / log --follow / show / rev-parse <ref>:<path>",
            "filesystem read + SHA-256",
            "```",
            "",
            f"Configured baseline refs: `{baselines}`",
            "",
            "## Write boundary",
            "",
            "The tool wrote only the explicit output directory outside the source repository.",
            "It did not stage, commit, push, mutate source files or access the network.",
            "",
        ]
    )


def atomic_write_text(path: Path, content: str) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    os.replace(temporary, path)


def write_outputs(
    output: Path,
    manifest: dict[str, Any],
    records: Sequence[dict[str, Any]],
    args: argparse.Namespace,
) -> None:
    output.mkdir(parents=True, exist_ok=True)
    atomic_write_text(output / "INDEX-MANIFEST.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    atomic_write_text(
        output / "DOCUMENT-INVENTORY.jsonl",
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
    )

    csv_temporary = output / "DOCUMENT-INVENTORY.csv.tmp"
    with csv_temporary.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "projectId",
            "repositoryId",
            "path",
            "documentKey",
            "title",
            "documentType",
            "declaredStatus",
            "contentSha256",
            "tracked",
            "worktreeState",
            "firstCommit",
            "lastCommit",
            "sensitivityFindingCount",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "projectId": record["projectId"],
                    "repositoryId": record["repositoryId"],
                    "path": record["path"],
                    "documentKey": record["documentKey"],
                    "title": record["title"],
                    "documentType": record["documentType"],
                    "declaredStatus": record.get("declaredStatus"),
                    "contentSha256": record["contentSha256"],
                    "tracked": record["git"]["tracked"],
                    "worktreeState": record["git"]["worktreeState"],
                    "firstCommit": record["git"].get("firstCommit"),
                    "lastCommit": record["git"].get("lastCommit"),
                    "sensitivityFindingCount": len(record["sensitivityFindings"]),
                }
            )
    os.replace(csv_temporary, output / "DOCUMENT-INVENTORY.csv")

    atomic_write_text(output / "INVENTORY-REPORT.md", build_report(manifest, records))
    atomic_write_text(output / "COMMAND-LEDGER.md", build_command_ledger(args, manifest))


def build_manifest(
    git: Git,
    config: dict[str, Any],
    records: Sequence[dict[str, Any]],
    baseline_refs: Sequence[dict[str, Any]],
    remote_name: str,
    remote: str | None,
    config_path: Path,
) -> dict[str, Any]:
    status_lines = git.run(["status", "--porcelain=v1", "--untracked-files=all"], check=False).stdout.splitlines()
    clean = len(status_lines) == 0
    branch = git.text(["symbolic-ref", "--quiet", "--short", "HEAD"], check=False) or "DETACHED"
    head = git.text(["rev-parse", "HEAD"])
    head_time = git.text(["show", "-s", "--format=%cI", "HEAD"])

    exact_duplicates = duplicate_groups(records, "contentSha256")
    same_names = duplicate_groups(records, "documentKey")
    multi_task = duplicate_task_groups(records)
    sensitivity_count = sum(len(record["sensitivityFindings"]) for record in records)
    untracked_count = sum(record["git"]["worktreeState"] == "UNTRACKED" for record in records)
    modified_count = sum(record["git"]["worktreeState"] not in ("CLEAN", "UNTRACKED") for record in records)

    return {
        "schemaVersion": SCHEMA_VERSION,
        "projectId": config["projectId"],
        "repositoryId": config["repositoryId"],
        "authority": "INVENTORY_ONLY",
        "tool": {
            "scriptSha256": sha256_bytes(Path(__file__).resolve().read_bytes()),
            "configSha256": sha256_bytes(config_path.read_bytes()),
        },
        "git": {
            "branch": branch,
            "head": head,
            "headCommitTime": head_time,
            "defaultBranch": config.get("defaultBranch"),
            "remoteName": remote_name,
            "remote": remote,
            "worktreeClean": clean,
            "worktreeEntryCount": len(status_lines),
            "sourceCommitOrigin": "GIT_VERIFIED" if clean else "WORKTREE_UNVERIFIED",
            "baselineRefs": list(baseline_refs),
        },
        "scope": {
            "documentRoots": config["documentRoots"],
            "includeFiles": config.get("includeFiles", []),
            "excludeGlobs": config.get("excludeGlobs", []),
            "extensions": config.get("extensions", [".md", ".mdx", ".txt"]),
        },
        "counts": {
            "documents": len(records),
            "trackedDocuments": sum(bool(record["git"]["tracked"]) for record in records),
            "untrackedDocuments": untracked_count,
            "modifiedDocuments": modified_count,
            "sensitivityFindings": sensitivity_count,
        },
        "findings": {
            "exactDuplicates": exact_duplicates,
            "sameNameCandidates": same_names,
            "multiDocumentTaskReferences": multi_task,
        },
        "outputs": list(OUTPUT_FILES),
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path, help="Foundation Git worktree")
    parser.add_argument("--config", required=True, type=Path, help="Project inventory JSON configuration")
    parser.add_argument("--output", required=True, type=Path, help="Output directory outside the source repository")
    parser.add_argument(
        "--require-clean",
        action="store_true",
        help="Reject a dirty worktree instead of emitting WORKTREE_UNVERIFIED",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        git = Git(args.repo)
        config_path = args.config.resolve()
        config = load_config(config_path)
        remote_name, remote = verify_repository_identity(git, config)
        output = args.output.resolve()
        if path_is_within(output, git.root):
            raise IndexError("output directory must be outside the source repository")

        status = git.run(["status", "--porcelain=v1", "--untracked-files=all"], check=False).stdout
        if args.require_clean and status:
            raise IndexError("BLOCKED_DIRTY_WORKTREE: --require-clean was supplied")

        resolved_baselines: list[dict[str, Any]] = []
        for ref in config.get("baselineRefs", []):
            commit = git.ref_commit(str(ref))
            resolved_baselines.append(
                {"ref": str(ref), "commit": commit, "available": commit is not None}
            )
        if config.get("requireBaselineRefs", False):
            missing_refs = [item["ref"] for item in resolved_baselines if not item["available"]]
            if missing_refs:
                raise IndexError(
                    "BLOCKED_MISSING_BASELINE_REF: " + ", ".join(missing_refs)
                )

        documents = enumerate_documents(git, config)
        records = [build_record(git, config, path, resolved_baselines) for path in documents]
        manifest = build_manifest(
            git,
            config,
            records,
            resolved_baselines,
            remote_name,
            remote,
            config_path,
        )
        write_outputs(output, manifest, records, args)

        print(
            json.dumps(
                {
                    "status": "INDEX_COMPLETE",
                    "projectId": config["projectId"],
                    "head": manifest["git"]["head"],
                    "sourceCommitOrigin": manifest["git"]["sourceCommitOrigin"],
                    "documents": len(records),
                    "outputFiles": list(OUTPUT_FILES),
                },
                sort_keys=True,
            )
        )
        return 0
    except IndexError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: filesystem operation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
