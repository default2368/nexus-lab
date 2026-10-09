from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "inventory-documents.py"
CONFIG = Path(__file__).resolve().parents[1] / "projects" / "foundation.json"


def run(command: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"command failed ({result.returncode}): {' '.join(command)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


class InventoryDocumentsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repository = self.root / "foundation"
        self.repository.mkdir()
        run(["git", "init", "-b", "master"], self.repository)
        run(["git", "config", "user.name", "Synthetic Test"], self.repository)
        run(["git", "config", "user.email", "synthetic@example.invalid"], self.repository)
        run(["git", "remote", "add", "origin", "https://token@example.invalid/default2368/open-nexus-foundation.git"], self.repository)

        (self.repository / "docs" / "plans" / "folder with spaces").mkdir(parents=True)
        (self.repository / "README.md").write_text("# Foundation\n\n**Status:** ACTIVE\n", encoding="utf-8")
        (self.repository / "docs" / "plans" / "SURF-082-005.md").write_text(
            "# SURF-082-005 — Registry convergence\n\n**Status:** PLANNED\n\nBaseline v0.8.1.\n",
            encoding="utf-8",
        )
        run(["git", "add", "--", "README.md", "docs/plans/SURF-082-005.md"], self.repository)
        run(["git", "commit", "-m", "docs: baseline"], self.repository)
        run(["git", "tag", "-a", "v0.8.1", "-m", "baseline"], self.repository)

        (self.repository / "docs" / "plans" / "folder with spaces" / "SEC-082-001.md").write_text(
            "# SEC-082-001 — Debug gate\n\nStatus: READY\n\nReference SURF-082-005.\n",
            encoding="utf-8",
        )
        run(["git", "add", "--", "docs/plans/folder with spaces/SEC-082-001.md"], self.repository)
        run(["git", "commit", "-m", "docs: add security plan"], self.repository)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def invoke(self, output: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        return run(
            [
                sys.executable,
                str(SCRIPT),
                "--repo",
                str(self.repository),
                "--config",
                str(CONFIG),
                "--output",
                str(output),
                *extra,
            ],
            self.root,
            check=False,
        )

    def load_jsonl(self, output: Path) -> list[dict]:
        return [json.loads(line) for line in (output / "DOCUMENT-INVENTORY.jsonl").read_text(encoding="utf-8").splitlines()]

    def test_clean_foundation_index_is_git_verified_and_baseline_linked(self) -> None:
        output = self.root / "spool"
        result = self.invoke(output, "--require-clean")
        self.assertEqual(result.returncode, 0, result.stderr)

        summary = json.loads(result.stdout)
        self.assertEqual(summary["status"], "INDEX_COMPLETE")
        self.assertEqual(summary["sourceCommitOrigin"], "GIT_VERIFIED")

        manifest = json.loads((output / "INDEX-MANIFEST.json").read_text(encoding="utf-8"))
        self.assertTrue(manifest["git"]["worktreeClean"])
        self.assertEqual(manifest["git"]["branch"], "master")
        self.assertEqual(manifest["git"]["baselineRefs"][0]["ref"], "v0.8.1")
        self.assertTrue(manifest["git"]["baselineRefs"][0]["available"])
        self.assertNotIn("token@", manifest["git"]["remote"])
        self.assertRegex(manifest["tool"]["scriptSha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(manifest["tool"]["configSha256"], r"^[0-9a-f]{64}$")

        records = {record["path"]: record for record in self.load_jsonl(output)}
        self.assertEqual(set(records), {
            "README.md",
            "docs/plans/SURF-082-005.md",
            "docs/plans/folder with spaces/SEC-082-001.md",
        })
        surf = records["docs/plans/SURF-082-005.md"]
        security = records["docs/plans/folder with spaces/SEC-082-001.md"]
        self.assertEqual(surf["declaredStatus"], "PLANNED")
        self.assertIn("SURF-082-005", surf["references"]["taskIds"])
        self.assertTrue(surf["git"]["atRefs"][0]["present"])
        self.assertFalse(security["git"]["atRefs"][0]["present"])
        self.assertIsNotNone(surf["git"]["firstCommit"])
        self.assertIsNotNone(surf["git"]["lastCommit"])

        for expected in (
            "INDEX-MANIFEST.json",
            "DOCUMENT-INVENTORY.jsonl",
            "DOCUMENT-INVENTORY.csv",
            "INVENTORY-REPORT.md",
            "COMMAND-LEDGER.md",
        ):
            self.assertTrue((output / expected).is_file(), expected)

    def test_dirty_inventory_is_unverified_and_require_clean_rejects(self) -> None:
        target = self.repository / "docs" / "plans" / "SURF-082-005.md"
        target.write_text(target.read_text(encoding="utf-8") + "\nUncommitted note.\n", encoding="utf-8")

        diagnostic_output = self.root / "diagnostic"
        diagnostic = self.invoke(diagnostic_output)
        self.assertEqual(diagnostic.returncode, 0, diagnostic.stderr)
        manifest = json.loads((diagnostic_output / "INDEX-MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["git"]["sourceCommitOrigin"], "WORKTREE_UNVERIFIED")
        records = {record["path"]: record for record in self.load_jsonl(diagnostic_output)}
        self.assertEqual(records["docs/plans/SURF-082-005.md"]["git"]["worktreeState"], "MODIFIED")

        rejected_output = self.root / "rejected"
        rejected = self.invoke(rejected_output, "--require-clean")
        self.assertEqual(rejected.returncode, 2)
        self.assertIn("BLOCKED_DIRTY_WORKTREE", rejected.stderr)
        self.assertFalse(rejected_output.exists())

    def test_output_inside_source_repository_is_rejected(self) -> None:
        output = self.repository / "docs" / "generated-index"
        result = self.invoke(output)
        self.assertEqual(result.returncode, 2)
        self.assertIn("outside the source repository", result.stderr)
        self.assertFalse(output.exists())

    def test_sensitivity_findings_do_not_emit_secret_value(self) -> None:
        secret_value = "example-secret-value-1234567890"
        sensitive = self.repository / "docs" / "plans" / "sensitive.md"
        sensitive.write_text(
            f"# Synthetic sensitivity test\n\napi_key={secret_value}\n",
            encoding="utf-8",
        )
        run(["git", "add", "--", "docs/plans/sensitive.md"], self.repository)
        run(["git", "commit", "-m", "test: add synthetic sensitivity fixture"], self.repository)

        output = self.root / "sensitivity"
        result = self.invoke(output, "--require-clean")
        self.assertEqual(result.returncode, 0, result.stderr)
        combined_output = "\n".join(
            path.read_text(encoding="utf-8")
            for path in output.iterdir()
            if path.is_file()
        )
        self.assertNotIn(secret_value, combined_output)
        records = {record["path"]: record for record in self.load_jsonl(output)}
        findings = records["docs/plans/sensitive.md"]["sensitivityFindings"]
        self.assertTrue(any(item["type"] == "POSSIBLE_SECRET_ASSIGNMENT" for item in findings))

    def test_wrong_repository_remote_is_rejected(self) -> None:
        run(["git", "remote", "set-url", "origin", "git@github.com:someone/another-project.git"], self.repository)
        output = self.root / "wrong-repository"
        result = self.invoke(output)
        self.assertEqual(result.returncode, 2)
        self.assertIn("BLOCKED_WRONG_REPOSITORY", result.stderr)
        self.assertFalse(output.exists())

    def test_required_baseline_ref_is_fail_closed(self) -> None:
        run(["git", "tag", "-d", "v0.8.1"], self.repository)
        output = self.root / "missing-baseline"
        result = self.invoke(output)
        self.assertEqual(result.returncode, 2)
        self.assertIn("BLOCKED_MISSING_BASELINE_REF", result.stderr)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
