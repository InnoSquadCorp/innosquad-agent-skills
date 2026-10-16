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

    def set_codex_skills(self, value):
        path = self.root / ".codex-plugin/plugin.json"
        data = json.loads(path.read_text())
        data["skills"] = value
        path.write_text(json.dumps(data))

    def test_missing_codex_skills_path_is_rejected(self):
        path = self.root / ".codex-plugin/plugin.json"
        data = json.loads(path.read_text())
        del data["skills"]
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "Codex skills path"):
            bundle.validate(self.root)

    def test_invalid_codex_skills_path_values_are_rejected(self):
        for value in [None, False, 1, [], ["./skills/"], {}, "", " ", "\t"]:
            with self.subTest(value=value):
                self.set_codex_skills(value)
                with self.assertRaisesRegex(ValueError, "Codex skills path"):
                    bundle.validate(self.root)

    def test_absolute_escaping_and_nonportable_codex_paths_are_rejected(self):
        for value in [str(self.root / "skills"), "/skills", "../skills",
                      "./skills/../skills", "C:/skills", r"skills\innodi",
                      "./skills/\0", " ./skills/"]:
            with self.subTest(value=value):
                self.set_codex_skills(value)
                with self.assertRaisesRegex(ValueError, "Codex skills path"):
                    bundle.validate(self.root)

    def test_nonexistent_file_and_wrong_inventory_paths_are_rejected(self):
        (self.root / "empty").mkdir()
        shutil.copytree(self.root / "skills/innodi", self.root / "partial/innodi")
        for value in ["./missing/", "./LICENSE", ".", "./empty/", "./partial/"]:
            with self.subTest(value=value):
                self.set_codex_skills(value)
                with self.assertRaisesRegex(ValueError, "Codex skills path"):
                    bundle.validate(self.root)

    def test_codex_path_symlinks_inside_and_outside_plugin_are_rejected(self):
        for name, target in [("inside", self.root / "skills"), ("outside", ROOT / "skills")]:
            (self.root / name).symlink_to(target, target_is_directory=True)
            for value in [f"./{name}/", f"./{name}/innodi"]:
                with self.subTest(value=value):
                    self.set_codex_skills(value)
                    with self.assertRaisesRegex(ValueError, "Codex skills path.*symlink"):
                        bundle.validate(self.root)

    def test_shared_skills_directory_cannot_be_a_symlink(self):
        (self.root / "skills").rename(self.root / "original-skills")
        (self.root / "skills").symlink_to(self.root / "original-skills", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Codex skills path.*symlink"):
            bundle.validate(self.root)

    def test_codex_inventory_drift_is_rejected(self):
        shutil.rmtree(self.root / "skills/innodi")
        with self.assertRaisesRegex(ValueError, "Codex skill inventory mismatch"):
            bundle.validate(self.root)

    def test_portable_codex_path_spellings_select_the_shared_inventory(self):
        for value in ["./skills/", "skills", "skills/"]:
            with self.subTest(value=value):
                self.set_codex_skills(value)
                self.assertEqual(bundle.validate(self.root)["skills"], 6)

    def test_snapshot_control(self):
        self.assertEqual(bundle.validate(self.root)["skills"], 6)

    def test_released_router_source_keeps_its_upstream_baseline_and_provenance(self):
        lock = json.loads((self.root / "sources.lock.json").read_text())["skills"]["innorouter"]
        support = json.loads((self.root / "skills/innorouter/references/support.json").read_text())
        self.assertEqual(lock["source_status"], "released")
        self.assertEqual(lock["source_release"]["revision"], lock["revision"])
        self.assertEqual(lock["source_release"]["tag"], "7.0.1")
        self.assertEqual(lock["library"]["version"], support["version"])
        self.assertEqual(support["version"], "7.0.0")
        self.assertEqual(support["swift_syntax_requirement"], ">=603.0.2 <605.0.0")
        self.assertEqual(lock["previous_source"]["source_status"], "merged")

    def test_released_source_provenance_must_match_the_source_pin(self):
        path = self.root / "sources.lock.json"
        original = json.loads(path.read_text())
        for mutation in ("missing", "type", "revision", "url"):
            with self.subTest(mutation=mutation):
                data = json.loads(json.dumps(original))
                pin = data["skills"]["innorouter"]
                if mutation == "missing":
                    del pin["source_release"]
                elif mutation == "type":
                    pin["source_release"] = []
                else:
                    pin["source_release"][mutation] = "wrong"
                path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, "Released source provenance mismatch"):
                    bundle.validate(self.root)

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
