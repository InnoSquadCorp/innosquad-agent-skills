"""Offline isolation/identity guards; actual Swift evidence comes from CI."""

import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import router_release_case as case

spec = importlib.util.spec_from_file_location("router_release_ci", ROOT / "scripts/validate_consumer_ci.py")
ci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci)
SOURCE = ROOT / "skills/innorouter"


class RouterReleaseCaseTests(unittest.TestCase):
    def test_preparation_preserves_baseline_examples_validator_and_all_other_bytes(self):
        original = case.file_records(SOURCE)
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            qualified, artifacts = directory / "qualified", directory / "artifacts"
            artifacts.mkdir()
            proof = case.prepare(SOURCE, qualified, artifacts)
            self.assertEqual(case.file_records(SOURCE), original)
            self.assertEqual(set(proof["changed_inputs"]), case.INPUTS)
            for name in original.keys() - case.INPUTS:
                self.assertEqual((SOURCE / name).read_bytes(), (qualified / name).read_bytes(), name)
            support = json.loads((qualified / "references/support.json").read_text())
            self.assertEqual(support["version"], "7.0.1")
            self.assertEqual(support["revision"], case.RELEASE["revision"])
            self.assertEqual(support["resolved_dependencies"]["innorouter"]["revision"], case.RELEASE["revision"])
            self.assertIn('exact: "7.0.1"', (qualified / "assets/consumer/Package.swift").read_text())
            original_pins = json.loads((SOURCE / "assets/consumer/Package.resolved").read_text())["pins"]
            adjusted_pins = json.loads((qualified / "assets/consumer/Package.resolved").read_text())["pins"]
            for before, after in zip(original_pins, adjusted_pins, strict=True):
                if before["identity"] == "innorouter":
                    self.assertEqual(before["state"], case.BASELINE)
                    self.assertEqual(after["state"], {k: case.RELEASE[k] for k in case.BASELINE})
                else:
                    self.assertEqual(before, after)
            for label in ("original-inputs", "adjusted-inputs"):
                self.assertTrue(all((artifacts / label / name).is_file() for name in case.INPUTS))
            self.assertEqual(json.loads((artifacts / "router-release-inputs.json").read_text()), proof)
            case.check_unchanged(SOURCE, qualified, proof)
            path = next((qualified / "assets/consumer/Sources").rglob("*.swift"))
            path.write_text(path.read_text() + "\n// Unreviewed change\n")
            with self.assertRaisesRegex(ValueError, "Qualified Router inputs changed"):
                case.check_unchanged(SOURCE, qualified, proof)

    def test_tag_requires_the_reviewed_lightweight_identity(self):
        ref = "refs/tags/7.0.1"
        output = case.RELEASE["revision"] + "\t" + ref + "\n"
        self.assertEqual(case.check_tag(output), {ref: case.RELEASE["revision"]})
        for wrong in ("", "not a ref", "0" * 40 + "\t" + ref,
                      case.RELEASE["revision"] + "\trefs/tags/7.0.0",
                      output + case.RELEASE["revision"] + "\t" + ref + "^{}\n"):
            with self.subTest(output=wrong):
                with self.assertRaises(ValueError):
                    case.check_tag(wrong)

    def test_isolated_case_rejects_another_skill_before_launching_tools(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(ci.subprocess, "Popen") as launch:
            report = ci.run_consumer(ROOT, "innodi", Path(temp) / "scratch", case.CASE)
            self.assertEqual(report["status"], "failed")
            self.assertIn("Unsupported consumer case", report["error"])
            launch.assert_not_called()

    def test_release_evidence_cannot_use_the_historical_tag_identity(self):
        support = json.loads((SOURCE / "references/support.json").read_text())
        support["resolved_dependencies"]["innorouter"].update(
            {k: case.RELEASE[k] for k in case.BASELINE})
        expected = ci.expected_dependencies(support, "innorouter")
        evidence = {
            "status": "passed",
            "dependencies": {name: {"clean": True, **{k: pin[k] for k in case.BASELINE}}
                             for name, pin in expected.items()},
            "commands": [{"argv": ["swift", "package", "resolve"], "exit_code": 0},
                         {"argv": ["swift", "test"], "exit_code": 0}],
            "release_identity": {"tag": "7.0.1", "revision": case.RELEASE["revision"]},
        }
        ci.check_consumer_evidence(evidence, expected, "innorouter", case.CASE)
        for key, value in [("tag", "7.0.0"), ("revision", case.BASELINE["revision"])]:
            wrong = copy.deepcopy(evidence)
            wrong["release_identity"][key] = value
            with self.assertRaisesRegex(ValueError, "Isolated Router release identity"):
                ci.check_consumer_evidence(wrong, expected, "innorouter", case.CASE)


if __name__ == "__main__":
    unittest.main()
