#!/usr/bin/env python3
"""Run one unchanged library-owned consumer on the qualified Apple CI host."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys

from validate_bundle import require, validate


ROOT = Path(__file__).resolve().parents[1]
DEVELOPER_DIR = "/Applications/Xcode_27.0.app/Contents/Developer"
PROTOBUF_RELEASE = {
    "tag": "6.1.1",
    "revision": "ba6ab8d6112d51efa69d92ac6739464bfc775aed",
    "tag_object": "eaea83c7f95f931b6e963c49ae10c7ef5f869438",
}


def expected_dependencies(support, skill):
    expected = support.get("resolved_dependencies") or {
        "innodi": support, "swift-syntax": support["swift_syntax"]
    }
    expected = {name: {key: pin[key] for key in ("repository", "version", "revision")}
                for name, pin in expected.items()}
    if skill == "innonetwork-protobuf":
        expected[skill]["revision"] = PROTOBUF_RELEASE["revision"]
    return expected


def consumer_command(root, skill, scratch):
    argv = [sys.executable, "-B", str(root / "skills" / skill / "scripts/validate_consumer.py"),
            "--scratch-path", str(scratch)]
    if skill == "innonetwork-protobuf":
        argv += ["--release-tag", PROTOBUF_RELEASE["tag"],
                 "--expected-adapter-revision", PROTOBUF_RELEASE["revision"],
                 "--expected-tag-object", PROTOBUF_RELEASE["tag_object"]]
    return argv


def check_toolchain(host, developer_dir, versions):
    require(host == "darwin", "Consumer CI requires macOS")
    require(developer_dir == DEVELOPER_DIR, "Select the explicit Xcode 27.0 DEVELOPER_DIR")
    require(re.search(r"^Xcode 27\.0$", versions["xcode"], re.M),
            "Consumer CI requires Xcode 27.0")
    require(re.search(r"Apple Swift version 6\.4(?:[.\s]|$)", versions["swift"]),
            "Consumer CI requires Apple Swift 6.4")
    require(re.match(r"27(?:\.|$)", versions["macos"]), "Consumer CI requires macOS 27")
    require(re.match(r"27(?:\.|$)", versions["sdk"]), "Consumer CI requires the macOS 27 SDK")


def check_consumer_evidence(evidence, expected, skill):
    require(evidence["status"] == "passed", "Library consumer did not pass")
    require(set(evidence["dependencies"]) == set(expected), "Consumer dependency inventory changed")
    for identity, baseline in expected.items():
        actual = evidence["dependencies"][identity]
        require(actual.get("clean") is True and all(actual.get(k) == baseline[k]
                for k in ("version", "revision")), f"Consumer identity mismatch: {identity}")
    for operation in ("resolve", "test"):
        require(any(entry["argv"][:2] == ["swift", "package" if operation == "resolve" else "test"]
                    and (operation != "resolve" or entry["argv"][-1] == "resolve")
                    and entry.get("exit_code") == 0 and not entry.get("timed_out")
                    for entry in evidence["commands"]), f"Missing successful Swift {operation}")
    if skill == "innonetwork-protobuf":
        require(evidence.get("release_identity") == PROTOBUF_RELEASE,
                "Protobuf release identity was not verified")


def collect_artifacts(scratch, artifacts):
    """Keep failure logs and exact inputs without uploading caches/checkouts."""
    for run in sorted((scratch / "skill-runs").glob("run-*")):
        destination = artifacts / run.name
        destination.mkdir(exist_ok=True)
        for path in run.iterdir():
            if path.is_file() and path.suffix in {".json", ".log"}:
                shutil.copy2(path, destination / path.name)
        for name in ("Package.swift", "Package.resolved"):
            path = run / "consumer" / name
            if path.is_file():
                shutil.copy2(path, destination / name)
    state = scratch / "workspace-state.json"
    if state.is_file():
        shutil.copy2(state, artifacts / state.name)


def run_consumer(root, skill, scratch):
    root, scratch = root.resolve(), scratch.resolve()
    require(not scratch.is_relative_to(root), "Scratch must be outside the repository")
    require(not scratch.exists(), "Use a fresh scratch directory for each consumer")
    artifacts = scratch / "artifacts"
    artifacts.mkdir(parents=True)
    swiftpm = scratch / "swiftpm"
    report = {"status": "failed", "skill": skill, "started_at": datetime.now(timezone.utc).isoformat(),
              "commands": [], "host_validation": "not_run", "publication_performed": False,
              "runner": {key: os.environ.get(key) for key in
                         ("RUNNER_OS", "RUNNER_ARCH", "ImageOS", "ImageVersion", "GITHUB_SHA", "GITHUB_RUN_ID")}}

    def command(label, argv, timeout=3600):
        log, diagnostics = artifacts / (label + ".log"), artifacts / (label + ".stderr.log")
        entry = {"argv": [str(a) for a in argv], "log": str(log), "stderr_log": str(diagnostics),
                 "timeout_seconds": timeout}
        report["commands"].append(entry)
        with log.open("w") as output, diagnostics.open("w") as error:
            with subprocess.Popen(entry["argv"], stdout=output, stderr=error, start_new_session=True) as process:
                try:
                    entry["exit_code"] = process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    entry.update(exit_code=process.wait(), timed_out=True)
        require(entry.get("timed_out") is not True, f"{label} timed out; see {diagnostics}")
        require(entry["exit_code"] == 0, f"{label} failed ({entry['exit_code']}); see {diagnostics}")
        return log.read_text().strip()

    try:
        validate(root, require_merged=True)
        lock = json.loads((root / "sources.lock.json").read_text())
        require(skill in lock["skills"], "Unknown skill")
        report["source_pin"] = lock["skills"][skill]
        support_path = root / "skills" / skill / "references/support.json"
        shutil.copy2(support_path, artifacts / "support.json")
        shutil.copy2(root / "sources.lock.json", artifacts / "sources.lock.json")
        expected = expected_dependencies(json.loads(support_path.read_text()), skill)
        report["expected_dependencies"] = expected
        require(sys.platform == "darwin", "Consumer CI requires macOS")
        require(not os.environ.get("INNONETWORK_LOCAL_PATH"), "Unset INNONETWORK_LOCAL_PATH")
        versions = report["toolchain"] = {}
        for name, argv in [("xcode", ["xcodebuild", "-version"]), ("swift", ["swift", "--version"]),
                           ("macos", ["sw_vers", "-productVersion"]),
                           ("sdk", ["xcrun", "--sdk", "macosx", "--show-sdk-version"])]:
            versions[name] = command(name, argv, timeout=60)
        check_toolchain(sys.platform, os.environ.get("DEVELOPER_DIR"), versions)
        output = command("consumer", consumer_command(root, skill, swiftpm))
        result = json.loads(output)
        require(result["status"] == "passed", "Library consumer reported failure")
        evidence_path = Path(result["evidence"]).resolve()
        require(evidence_path.is_relative_to(swiftpm / "skill-runs"),
                "Consumer evidence escaped the scratch directory")
        evidence = json.loads(evidence_path.read_text())
        check_consumer_evidence(evidence, expected, skill)
        package = evidence_path.parent / "consumer"
        # swift test already compiles; also keep an explicit build result.
        command("swift-build", ["swift", "build", "--package-path", package,
                               "--scratch-path", swiftpm, "--jobs", "2",
                               "-Xswiftc", "-strict-concurrency=complete", "-Xswiftc", "-warnings-as-errors"])
        pins = {p["identity"]: p for p in json.loads((package / "Package.resolved").read_text())["pins"]}
        require(set(pins) == set(expected), "Final dependency inventory changed")
        workspace = json.loads((swiftpm / "workspace-state.json").read_text())["object"]
        dependencies = {d["packageRef"]["identity"]: d for d in workspace["dependencies"]}
        require(set(dependencies) == set(expected), "Final workspace inventory changed")
        for identity, baseline in expected.items():
            pin = pins[identity]
            require(pin["kind"] == "remoteSourceControl" and pin["location"] == baseline["repository"]
                    and pin["state"] == {k: baseline[k] for k in ("version", "revision")},
                    f"Final pin changed: {identity}")
            checkout = (swiftpm / "checkouts" / dependencies[identity]["subpath"]).resolve()
            require(checkout.is_relative_to(swiftpm / "checkouts"), "Checkout escaped scratch")
            require(command(identity + "-final-head", ["git", "-C", checkout, "rev-parse", "HEAD"], 60)
                    == baseline["revision"], f"Final checkout changed: {identity}")
            require(not command(identity + "-final-status", ["git", "-C", checkout, "status", "--porcelain",
                                                           "--untracked-files=all"], 60),
                    f"Final checkout is dirty: {identity}")
        for relative, digest in evidence["source_sha256"].items():
            if relative != "Package.resolved":
                require(hashlib.sha256((package / relative).read_bytes()).hexdigest() == digest,
                        f"Consumer source changed: {relative}")
        tests = (evidence_path.parent / "swift-test.log").read_text()
        summaries = re.findall(r"Test run with (\d+) tests? in (\d+) suites? passed", tests)
        require(summaries and sum(int(n) for n, _ in summaries) > 0, "No passing Swift tests recorded")
        report.update(status="passed", dependencies=evidence["dependencies"],
                      tests=sum(int(n) for n, _ in summaries))
        validate(root, require_merged=True)
    except (OSError, ValueError, KeyError, TypeError) as error:
        report.update(status="failed", error=str(error))
    finally:
        collect_artifacts(swiftpm, artifacts)
        report["finished_at"] = datetime.now(timezone.utc).isoformat()
        (artifacts / "ci-evidence.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", required=True)
    parser.add_argument("--scratch-path", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = run_consumer(ROOT, args.skill, args.scratch_path)
        print(json.dumps(report, indent=2))
        return 0 if report["status"] == "passed" else 1
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
