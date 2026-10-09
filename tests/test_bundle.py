import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("bundle", ROOT / "scripts/validate_bundle.py")
bundle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bundle)


class DistributionChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for name in ["plugin.json", "LICENSE", "sources.lock.json", ".codex-plugin", ".claude-plugin", ".agents", "skills"]:
            source = ROOT / name
            if source.is_dir():
                shutil.copytree(source, self.root / name)
            else:
                shutil.copy2(source, self.root / name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_snapshot_control(self):
        self.assertEqual(bundle.validate(self.root)["skills"], 6)

    def test_instruction_tampering_is_rejected(self):
        p = self.root / "skills/innodi/SKILL.md"
        p.write_text(p.read_text() + "\nUnreviewed instruction.\n")
        with self.assertRaisesRegex(ValueError, "Snapshot differs"):
            bundle.validate(self.root)

    def test_executable_mode_change_is_rejected(self):
        p = self.root / "skills/innodi/scripts/validate_consumer.py"
        p.chmod(p.stat().st_mode ^ 0o100)
        with self.assertRaisesRegex(ValueError, "Snapshot differs"):
            bundle.validate(self.root)

    def test_version_drift_is_rejected(self):
        p = self.root / ".claude-plugin/plugin.json"
        data = json.loads(p.read_text())
        data["version"] = "0.0.0"
        p.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "Manifest mismatch: version"):
            bundle.validate(self.root)

    def test_external_symlink_is_rejected(self):
        (self.root / "skills/innodi/external").symlink_to(ROOT / "LICENSE")
        with self.assertRaisesRegex(ValueError, "Symlink"):
            bundle.validate(self.root)

    def test_release_check_rejects_unmerged_source(self):
        p = self.root / "sources.lock.json"
        data = json.loads(p.read_text())
        data["skills"]["innodi"]["source_status"] = "pull_request"
        p.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "awaits merge"):
            bundle.validate(self.root, require_merged=True)


if __name__ == "__main__":
    unittest.main()
