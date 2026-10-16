"""Central-owned Router patch verification; never edit the vendored baseline."""

import hashlib
import json
import shutil
import stat

from validate_bundle import require, tree_id


CASE = "router-7.0.1"
RELEASE = {
    "repository": "https://github.com/InnoSquadCorp/InnoRouter.git",
    "tag": "7.0.1",
    "version": "7.0.1",
    "revision": "482587bcac8347857fd521ff38f169c010f48b83",
    "source_tree": "645baccc66df3d8e7989787e875f7063939b6444",
}
BASELINE = {"version": "7.0.0", "revision": "33b0da7639105cfa8e6f5acffa3badb91b5e0254"}
INPUTS = {"references/support.json", "assets/consumer/Package.swift",
          "assets/consumer/Package.resolved"}


def file_records(directory):
    return {path.relative_to(directory).as_posix(): {
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "executable": bool(path.stat().st_mode & stat.S_IXUSR),
    } for path in sorted(directory.rglob("*")) if path.is_file()}


def check_tag(output):
    rows = [line.split() for line in output.splitlines()]
    require(len(rows) == 1 and len(rows[0]) == 2,
            "Router 7.0.1 must retain its reviewed lightweight tag")
    refs = {name: revision for revision, name in rows}
    require(refs == {"refs/tags/" + RELEASE["tag"]: RELEASE["revision"]},
            "Router 7.0.1 tag differs from the reviewed immutable release")
    return refs


def check_unchanged(source, qualified, provenance):
    require(file_records(source) == provenance["original"],
            "Original Router skill changed during isolated verification")
    require(file_records(qualified) == provenance["adjusted"],
            "Qualified Router inputs changed during verification")


def prepare(source, qualified, artifacts):
    require(tree_id(source) == RELEASE["source_tree"], "Router source tree differs from reviewed release")
    original = file_records(source)
    support = json.loads((source / "references/support.json").read_text())
    require({key: support[key] for key in BASELINE} == BASELINE,
            "Preserve the upstream-owned Router 7.0.0 baseline")
    require(support["repository"] == RELEASE["repository"] and support["tag"] == BASELINE["version"],
            "Unexpected Router baseline identity")
    shutil.copytree(source, qualified)
    support.update(version=RELEASE["version"], revision=RELEASE["revision"], tag=RELEASE["tag"],
                   release_url=RELEASE["repository"].removesuffix(".git") + "/releases/tag/" + RELEASE["tag"],
                   checked_on="2026-10-16", baseline_kind="central_isolated_release_tag",
                   scope="Central-owned isolated Router 7.0.1 verification; original 7.0.0 inputs are retained separately.")
    support["resolved_dependencies"]["innorouter"].update(
        version=RELEASE["version"], revision=RELEASE["revision"])
    (qualified / "references/support.json").write_text(json.dumps(support, indent=2) + "\n")
    manifest = qualified / "assets/consumer/Package.swift"
    text = manifest.read_text()
    require(text.count('exact: "7.0.0"') == 1, "Unexpected Router manifest baseline")
    manifest.write_text(text.replace('exact: "7.0.0"', 'exact: "7.0.1"')
                       .replace("Published 7.0.0;", "Central-only published 7.0.1;"))
    lock_path = qualified / "assets/consumer/Package.resolved"
    lock = json.loads(lock_path.read_text())
    router, = [pin for pin in lock["pins"] if pin["identity"] == "innorouter"]
    require(router["kind"] == "remoteSourceControl" and router["location"] == RELEASE["repository"]
            and router["state"] == BASELINE, "Unexpected original Router lock pin")
    router["state"] = {key: RELEASE[key] for key in BASELINE}
    lock_path.write_text(json.dumps(lock, indent=2) + "\n")
    adjusted = file_records(qualified)
    require(set(original) == set(adjusted), "Isolated Router file inventory changed")
    require({name for name in original if original[name] != adjusted[name]} == INPUTS,
            "Only temporary Router Package/support inputs may change")
    provenance = {"owner": "central", "case": CASE, "release": RELEASE,
                  "original_baseline": BASELINE, "changed_inputs": sorted(INPUTS),
                  "original": original, "adjusted": adjusted}
    for label, directory in [("original-inputs", source), ("adjusted-inputs", qualified)]:
        for name in sorted(INPUTS):
            target = artifacts / label / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(directory / name, target)
    (artifacts / "router-release-inputs.json").write_text(json.dumps(provenance, indent=2) + "\n")
    check_unchanged(source, qualified, provenance)
    return provenance
