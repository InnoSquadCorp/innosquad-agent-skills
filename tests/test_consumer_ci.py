"""Offline guard tests; mocked tool results are not Swift consumer evidence."""

import copy
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("consumer_ci", ROOT / "scripts/validate_consumer_ci.py")
ci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci)
SKILLS = json.loads((ROOT / "sources.lock.json").read_text())["skills"]
VERSIONS = {"xcode": "Xcode 27.0\nBuild version 27A266a",
            "swift": "Apple Swift version 6.4 (swiftlang-test)",
            "macos": "27.0.1", "sdk": "27.0"}


def expected(skill):
    support = json.loads((ROOT / "skills" / skill / "references/support.json").read_text())
    return ci.expected_dependencies(support, skill)


def evidence(skill):
    return {
        "status": "passed",
        "dependencies": {name: {"version": pin["version"], "revision": pin["revision"], "clean": True}
                         for name, pin in expected(skill).items()},
        "commands": [{"argv": ["swift", "package", "resolve"], "exit_code": 0},
                     {"argv": ["swift", "test"], "exit_code": 0}],
        "release_identity": dict(ci.PROTOBUF_RELEASE),
    }


class ConsumerCIGuards(unittest.TestCase):
    def test_all_six_keep_exact_pins_and_only_protobuf_uses_release_override(self):
        self.assertEqual(len(SKILLS), 6)
        for skill in SKILLS:
            with self.subTest(skill=skill):
                support_path = ROOT / "skills" / skill / "references/support.json"
                before = support_path.read_bytes()
                pins = expected(skill)
                support = json.loads(before)
                self.assertEqual(pins[skill]["version"], support["version"])
                revision = ci.PROTOBUF_RELEASE["revision"] if skill == "innonetwork-protobuf" else support["revision"]
                self.assertEqual(pins[skill]["revision"], revision)
                self.assertEqual(pins["swift-syntax"]["version"], "604.0.0")
                self.assertEqual(support_path.read_bytes(), before)
                argv = ci.consumer_command(ROOT, skill, Path("/external") / skill)
                self.assertEqual(argv[argv.index("--scratch-path") + 1], "/external/" + skill)
                self.assertEqual("--release-tag" in argv, skill == "innonetwork-protobuf")
        argv = ci.consumer_command(ROOT, "innonetwork-protobuf", Path("/external/protobuf"))
        for flag, key in [("--release-tag", "tag"), ("--expected-adapter-revision", "revision"),
                          ("--expected-tag-object", "tag_object")]:
            self.assertEqual(argv[argv.index(flag) + 1], ci.PROTOBUF_RELEASE[key])

    def test_explicit_toolchain_control_and_mismatches(self):
        ci.check_toolchain("darwin", ci.DEVELOPER_DIR, VERSIONS)
        for host, directory, versions in [
            ("linux", ci.DEVELOPER_DIR, VERSIONS),
            ("darwin", "/Applications/Xcode.app/Contents/Developer", VERSIONS),
            *[("darwin", ci.DEVELOPER_DIR, {**VERSIONS, key: value}) for key, value in [
                ("xcode", "Xcode 26.6"), ("swift", "Apple Swift version 6.3"),
                ("macos", "26.0"), ("sdk", "26.0"), ("swift", "")]],
        ]:
            with self.subTest(host=host, directory=directory, versions=versions):
                with self.assertRaises(ValueError):
                    ci.check_toolchain(host, directory, versions)

    def test_passing_evidence_requires_resolve_tests_and_exact_clean_dependencies(self):
        for skill in SKILLS:
            ci.check_consumer_evidence(evidence(skill), expected(skill), skill)
        for mutation in ["failed", "missing", "extra", "version", "revision", "dirty", "resolve", "test", "timeout", "tag"]:
            with self.subTest(mutation=mutation):
                result = copy.deepcopy(evidence("innonetwork-protobuf"))
                dependency = result["dependencies"]["innonetwork-protobuf"]
                if mutation == "failed":
                    result["status"] = "failed"
                elif mutation == "missing":
                    del result["dependencies"]["swift-syntax"]
                elif mutation == "extra":
                    result["dependencies"]["local-override"] = dependency
                elif mutation in ("version", "revision"):
                    dependency[mutation] = "wrong"
                elif mutation == "dirty":
                    dependency["clean"] = False
                elif mutation in ("resolve", "test"):
                    result["commands"][0 if mutation == "resolve" else 1]["exit_code"] = 1
                elif mutation == "timeout":
                    result["commands"][1]["timed_out"] = True
                else:
                    result["release_identity"]["tag_object"] = "0" * 40
                with self.assertRaises(ValueError):
                    ci.check_consumer_evidence(result, expected("innonetwork-protobuf"), "innonetwork-protobuf")

    def test_missing_xcode_records_failed_evidence_and_never_starts_consumer(self):
        with tempfile.TemporaryDirectory() as temp:
            scratch = Path(temp) / "innodi"
            with patch.object(sys, "platform", "darwin"), \
                    patch.dict(os.environ, {"DEVELOPER_DIR": ci.DEVELOPER_DIR, "INNONETWORK_LOCAL_PATH": ""}), \
                    patch.object(ci.subprocess, "Popen", side_effect=FileNotFoundError("xcodebuild missing")) as launch:
                report = ci.run_consumer(ROOT, "innodi", scratch)
            self.assertEqual(report["status"], "failed")
            self.assertIn("xcodebuild missing", report["error"])
            self.assertEqual(launch.call_count, 1)
            saved = json.loads((scratch / "artifacts/ci-evidence.json").read_text())
            self.assertEqual(saved["status"], "failed")
            self.assertEqual(saved["host_validation"], "not_run")
            self.assertTrue((scratch / "artifacts/support.json").is_file())
            with self.assertRaisesRegex(ValueError, "fresh scratch"):
                ci.run_consumer(ROOT, "innodi", scratch)
        with self.assertRaisesRegex(ValueError, "outside"):
            ci.run_consumer(ROOT, "innodi", ROOT / "build-output")

    def test_helper_failure_preserves_stderr_partial_logs_and_resolved_inputs(self):
        with tempfile.TemporaryDirectory() as temp:
            scratch = Path(temp) / "innoflow"

            def launch(argv, *, stdout, stderr, start_new_session):
                process = MagicMock()
                process.__enter__.return_value = process
                process.__exit__.return_value = False
                if any(Path(arg).name == "validate_consumer.py" for arg in argv):
                    run = scratch / "swiftpm/skill-runs/run-failed"
                    (run / "consumer").mkdir(parents=True)
                    (run / "resolve.log").write_text("partial resolve output")
                    (run / "evidence.json").write_text('{"status": "failed"}')
                    (run / "consumer/Package.resolved").write_text('{"pins": []}')
                    stderr.write("consumer failed\n")
                    process.wait.return_value = 23
                else:
                    key = {"xcodebuild": "xcode", "swift": "swift", "sw_vers": "macos", "xcrun": "sdk"}[argv[0]]
                    stdout.write(VERSIONS[key])
                    process.wait.return_value = 0
                return process

            with patch.object(sys, "platform", "darwin"), \
                    patch.dict(os.environ, {"DEVELOPER_DIR": ci.DEVELOPER_DIR, "INNONETWORK_LOCAL_PATH": ""}), \
                    patch.object(ci.subprocess, "Popen", side_effect=launch):
                report = ci.run_consumer(ROOT, "innoflow", scratch)
            self.assertEqual(report["status"], "failed")
            self.assertEqual(report["commands"][-1]["exit_code"], 23)
            artifacts = scratch / "artifacts"
            self.assertEqual((artifacts / "consumer.stderr.log").read_text(), "consumer failed\n")
            self.assertEqual((artifacts / "run-failed/resolve.log").read_text(), "partial resolve output")
            self.assertTrue((artifacts / "run-failed/Package.resolved").is_file())

    def test_timeout_kills_process_group_and_records_failure(self):
        process = MagicMock()
        process.__enter__.return_value = process
        process.__exit__.return_value = False
        process.pid = 12345
        process.wait.side_effect = [ci.subprocess.TimeoutExpired(["xcodebuild", "-version"], 60), -9]
        with tempfile.TemporaryDirectory() as temp:
            scratch = Path(temp) / "innodi"
            with patch.object(sys, "platform", "darwin"), \
                    patch.dict(os.environ, {"INNONETWORK_LOCAL_PATH": ""}), \
                    patch.object(ci.subprocess, "Popen", return_value=process), \
                    patch.object(ci.os, "killpg") as kill:
                report = ci.run_consumer(ROOT, "innodi", scratch)
            kill.assert_called_once_with(12345, ci.signal.SIGKILL)
            self.assertEqual(report["status"], "failed")
            self.assertTrue(report["commands"][0]["timed_out"])
            self.assertEqual(report["commands"][0]["exit_code"], -9)
            self.assertTrue((scratch / "artifacts/ci-evidence.json").is_file())


if __name__ == "__main__":
    unittest.main()
