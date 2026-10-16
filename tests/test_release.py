import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_release as release
from validate_bundle import tree_id, validate


class ReleasePackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        for name in ["plugin.json", "LICENSE", "README.md", "CHANGELOG.md", "sources.lock.json",
                     ".codex-plugin", ".claude-plugin", ".agents", "skills", "scripts", "docs", "evals"]:
            source = ROOT / name
            if source.is_dir():
                shutil.copytree(source, self.root / name, ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copy2(source, self.root / name)

    def tearDown(self):
        self.temp.cleanup()

    def commit_merged_fixture(self):
        lock = self.root / "sources.lock.json"
        data = json.loads(lock.read_text())
        for pin in data["skills"].values():
            pin["source_status"] = "merged"
        lock.write_text(json.dumps(data))
        for args in [["init", "-q"], ["add", "."],
                     ["-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                      "commit", "-qm", "Fixture"]]:
            subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)

    def test_candidate_round_trip_preserves_complete_skills_modes_and_checksums(self):
        # Resources without a recognized extension must survive native packaging.
        extra = self.root / "skills/innodi/assets/sample.data"
        extra.write_bytes(b"additional text resource\n")
        lock = self.root / "sources.lock.json"
        data = json.loads(lock.read_text())
        data["skills"]["innodi"]["git_tree"] = tree_id(extra.parents[1])
        lock.write_text(json.dumps(data))
        (self.root / "private-trace.json").write_text("must not ship")
        first, second = self.base / "first", self.base / "second"
        a = release.build(self.root, first, candidate=True)
        b = release.build(self.root, second, candidate=True)
        self.assertEqual(Path(a["plugin_archive"]).read_bytes(), Path(b["plugin_archive"]).read_bytes())
        self.assertIn("-candidate.zip", a["plugin_archive"])
        self.assertFalse(a["publication_performed"])
        extracted = self.base / "extracted"
        with zipfile.ZipFile(a["plugin_archive"]) as archive:
            self.assertNotIn("innosquad/private-trace.json", archive.namelist())
            archive.extractall(extracted)
            for info in archive.infolist():
                (extracted / info.filename).chmod((info.external_attr >> 16) & 0o777)
        self.assertEqual(validate(extracted / "innosquad")["skills"], 6)
        for line in (first / "SHA256SUMS").read_text().splitlines():
            checksum, name = line.split("  ", 1)
            self.assertEqual(hashlib.sha256((first / name).read_bytes()).hexdigest(), checksum)
        with self.assertRaisesRegex(ValueError, "must not exist"):
            release.build(self.root, first, candidate=True)

    def test_release_rejects_review_source_before_creating_output(self):
        lock = self.root / "sources.lock.json"
        data = json.loads(lock.read_text())
        data["skills"]["innodi"]["source_status"] = "pull_request"
        lock.write_text(json.dumps(data))
        output = self.base / "blocked"
        with self.assertRaisesRegex(ValueError, "awaits merge"):
            release.build(self.root, output)
        self.assertFalse(output.exists())

    def test_merged_package_records_commit_without_claiming_remote_checks_or_publication(self):
        self.commit_merged_fixture()
        output = self.base / "release"
        result = release.build(self.root, output)
        record = json.loads((output / "release.json").read_text())
        self.assertEqual(record["package_kind"], "merged_source_package")
        self.assertEqual(len(record["source"]["commit"]), 40)
        self.assertFalse(record["source"]["dirty"])
        self.assertEqual(record["remote_checks"], "not_run")
        self.assertFalse(record["publication_performed"])
        self.assertNotIn("-candidate", result["plugin_archive"])
        (self.root / ".git/info/exclude").write_text("docs/private-evaluation.md\n")
        (self.root / "docs/private-evaluation.md").write_text("Ignored local evaluation")
        with self.assertRaisesRegex(ValueError, "must be tracked"):
            release.build(self.root, self.base / "ignored")
        (self.root / "README.md").write_text("Uncommitted release change")
        with self.assertRaisesRegex(ValueError, "clean committed"):
            release.build(self.root, self.base / "dirty")

    def test_generated_output_cannot_contaminate_distribution_inputs(self):
        with self.assertRaisesRegex(ValueError, "outside distribution inputs"):
            release.build(self.root, self.root / "skills/new-package", candidate=True)
        (self.root / "docs/external.md").symlink_to(self.root / "README.md")
        with self.assertRaisesRegex(ValueError, "symlink"):
            release.build(self.root, self.base / "symlink", candidate=True)


if __name__ == "__main__":
    unittest.main()
