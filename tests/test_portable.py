import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError, URLError
import zipfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import portable_skills as portable
import grok_request as grok


class PortableSkillsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name)
        self.pins = portable.selection(ROOT)

    def tearDown(self):
        self.tmp.cleanup()

    def test_each_host_gets_all_original_files_modes_and_notices(self):
        for host, relative in portable.HOST_PATHS.items():
            with self.subTest(host=host):
                project = self.project / host
                project.mkdir()
                result = portable.install(ROOT, self.pins, project, host)
                self.assertEqual(len(result["skills"]), 6)
                for name, pin in self.pins.items():
                    target = project / relative / name
                    self.assertEqual(portable.tree_id(target), pin["git_tree"])
                    self.assertTrue((target / "THIRD_PARTY_NOTICES.md").is_file())
                again = portable.install(ROOT, self.pins, project, host)
                self.assertTrue(all(p["status"] == "unchanged" for p in again["skills"]))

    def test_dry_run_does_not_create_directories(self):
        portable.install(ROOT, self.pins, self.project, "grok", dry_run=True)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_host_setup_guidance_does_not_overwrite_project_settings(self):
        settings = self.project / ".gemini/settings.json"
        settings.parent.mkdir()
        settings.write_text('{"experimental":{"skills":false},"userSetting":"preserve"}\n')
        original = settings.read_bytes()
        preview = portable.install(ROOT, self.pins, self.project, "gemini", dry_run=True)
        installed = portable.install(ROOT, self.pins, self.project, "gemini")
        self.assertEqual(preview["host_guidance"], installed["host_guidance"])
        self.assertTrue(installed["host_guidance"])
        self.assertEqual(settings.read_bytes(), original)
        self.assertTrue(portable.install(ROOT, self.pins, self.project, "copilot")["host_guidance"])

    def test_conflict_preflight_preserves_existing_and_other_skills(self):
        target = self.project / ".grok/skills/innorouter"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("user-owned instructions")
        with self.assertRaisesRegex(ValueError, "Existing skill differs"):
            portable.install(ROOT, self.pins, self.project, "grok")
        self.assertEqual((target / "SKILL.md").read_text(), "user-owned instructions")
        self.assertEqual([p.name for p in target.parent.iterdir()], ["innorouter"])

    def test_symlink_destination_cannot_redirect_install(self):
        outside = self.project / "outside"
        outside.mkdir()
        (self.project / ".grok").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            portable.install(ROOT, self.pins, self.project, "grok")
        self.assertEqual(list(outside.iterdir()), [])

    def test_unknown_skill_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown skills"):
            portable.selection(ROOT, ["../private"])

    def test_export_is_complete_deterministic_and_preserves_existing_output(self):
        first, second = self.project / "one", self.project / "two"
        a = portable.export_pack(ROOT, self.pins, first)
        b = portable.export_pack(ROOT, self.pins, second)
        self.assertEqual(a["sha256"], b["sha256"])
        index = json.loads((first / "catalog.json").read_text())
        self.assertEqual({s["name"] for s in index["skills"]}, set(self.pins))
        with zipfile.ZipFile(first / "innosquad-skills.zip") as archive:
            for name, pin in self.pins.items():
                context = (first / (name + ".md")).read_text()
                self.assertIn(pin["revision"], context)
                for source in (ROOT / pin["path"]).rglob("*"):
                    if not source.is_file():
                        continue
                    member = source.relative_to(ROOT).as_posix()
                    self.assertEqual(archive.read(member), source.read_bytes())
                    self.assertEqual((archive.getinfo(member).external_attr >> 16) & 0o100,
                                     source.stat().st_mode & 0o100)
                    self.assertIn(source.read_text().rstrip("\n"), context)
            self.assertEqual(archive.read("LICENSE"), (ROOT / "LICENSE").read_bytes())
        for filename, checksum in a["sha256"].items():
            self.assertEqual(hashlib.sha256((first / filename).read_bytes()).hexdigest(), checksum)
        with self.assertRaisesRegex(ValueError, "must not exist"):
            portable.export_pack(ROOT, self.pins, first)

    def test_export_selection_does_not_include_unselected_skills(self):
        pins = portable.selection(ROOT, ["innodi"])
        target = self.project / "pack"
        portable.export_pack(ROOT, pins, target)
        self.assertFalse((target / "innorouter.md").exists())
        with zipfile.ZipFile(target / "innosquad-skills.zip") as archive:
            self.assertFalse(any(n.startswith("skills/innorouter/") for n in archive.namelist()))


class GrokRequestTests(unittest.TestCase):
    def setUp(self):
        self.body = grok.payload(ROOT, ["innodi"], "account-selected-model", "Show a fake override")

    def test_payload_contains_selected_context_without_tools_or_key(self):
        self.assertEqual(self.body["model"], "account-selected-model")
        self.assertFalse(self.body["store"])
        self.assertNotIn("tools", self.body)
        self.assertNotIn("Authorization", self.body)
        self.assertIn("## File: innodi/SKILL.md", self.body["input"][0]["content"])
        self.assertNotIn("## File: innorouter/", self.body["input"][0]["content"])
        self.assertEqual(self.body["input"][1]["content"], "Show a fake override")

    def test_dry_run_works_without_key_or_network(self):
        with tempfile.TemporaryDirectory() as directory:
            prompt = Path(directory) / "prompt.txt"
            prompt.write_text("Explain an override")
            with patch.object(sys, "argv", ["grok_request.py", "--skill", "innodi", "--model", "chosen",
                                            "--prompt-file", str(prompt), "--dry-run"]), \
                    patch.dict("os.environ", {}, clear=True), patch.object(grok, "send") as send, \
                    patch("sys.stdout", new_callable=io.StringIO) as stdout:
                self.assertEqual(grok.main(), 0)
                self.assertEqual(json.loads(stdout.getvalue())["model"], "chosen")
                send.assert_not_called()

    def test_missing_key_or_invalid_timeout_never_opens_network(self):
        with patch.object(grok, "build_opener") as opener:
            with self.assertRaisesRegex(ValueError, "XAI_API_KEY"):
                grok.send(self.body, None)
            for key in ["private-key\n", "private key", "비밀키"]:
                with self.assertRaises(ValueError) as failure:
                    grok.send(self.body, key)
                self.assertNotIn(key, str(failure.exception))
            for timeout in [0, -1, 3601, float("inf"), float("nan")]:
                with self.assertRaises(ValueError):
                    grok.send(self.body, "test-key", timeout)
            opener.assert_not_called()

    def test_real_request_shape_and_response_parser(self):
        response = {"id": "example", "model": "account-selected-model", "status": "completed",
                    "output": [{"type": "reasoning", "summary": []},
                               {"type": "message", "content": [{"type": "output_text", "text": "First"},
                                                                {"type": "output_text", "text": "Second"}]}]}
        opener = MagicMock()
        opener.open.return_value.__enter__.return_value.read.return_value = json.dumps(response).encode()
        with patch.object(grok, "build_opener", return_value=opener):
            result = grok.send(self.body, "test-key", timeout=9)
        self.assertEqual(result["text"], "First\nSecond")
        request = opener.open.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.x.ai/v1/responses")
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.get_header("Authorization"), "Bearer test-key")
        self.assertEqual(json.loads(request.data), self.body)
        self.assertEqual(opener.open.call_args.kwargs["timeout"], 9)

    def test_errors_are_not_retried_or_echoed(self):
        for error in [HTTPError(grok.ENDPOINT, 401, "private body", {}, None),
                      HTTPError(grok.ENDPOINT, 429, "private body", {}, None),
                      URLError("private body"), TimeoutError("private body")]:
            opener = MagicMock()
            opener.open.side_effect = error
            with patch.object(grok, "build_opener", return_value=opener):
                with self.assertRaises(RuntimeError) as failure:
                    grok.send(self.body, "test-key")
            self.assertNotIn("private body", str(failure.exception))
            self.assertEqual(opener.open.call_count, 1)
        self.assertIsNone(grok.NoRedirect().redirect_request(None, None, 302, "", {}, "https://elsewhere.invalid"))

    def test_incomplete_malformed_empty_and_oversized_responses_rejected(self):
        cases = [b"not json", b"[]", b'{"status":"incomplete"}',
                 b'{"status":"completed","output":[]}', b"x" * (grok.MAX_RESPONSE_BYTES + 1)]
        for data in cases:
            opener = MagicMock()
            opener.open.return_value.__enter__.return_value.read.return_value = data
            with patch.object(grok, "build_opener", return_value=opener):
                with self.assertRaises(RuntimeError):
                    grok.send(self.body, "test-key")


if __name__ == "__main__":
    unittest.main()
