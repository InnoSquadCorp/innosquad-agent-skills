#!/usr/bin/env python3
"""Check the distributable snapshot without installing a host or resolving Swift."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
from urllib.parse import unquote


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git_object(kind, content):
    return hashlib.sha1(f"{kind} {len(content)}\0".encode() + content).digest()


def tree_id(directory):
    """Reproduce Git's tree identity, including paths and executable bits."""
    entries = []
    for path in directory.iterdir():
        require(not path.is_symlink(), f"Symlink is not portable: {path}")
        require(path.name not in {".git", ".build", ".swiftpm", "__pycache__", ".DS_Store"},
                f"Generated/private artifact in skill: {path}")
        if path.is_dir():
            mode, digest, key = "40000", bytes.fromhex(tree_id(path)), path.name + "/"
        else:
            require(path.is_file(), f"Unsupported file type: {path}")
            mode = "100755" if path.stat().st_mode & stat.S_IXUSR else "100644"
            digest, key = git_object("blob", path.read_bytes()), path.name
        entries.append((key.encode(), mode.encode() + b" " + path.name.encode() + b"\0" + digest))
    return git_object("tree", b"".join(value for _, value in sorted(entries))).hex()


def codex_skills_path(root, value, inventory):
    """Bind Codex discovery to the same portable skill inventory we package."""
    require(isinstance(value, str) and bool(value.strip()),
            "Codex skills path must be a nonempty string")
    require(value == value.strip() and "\\" not in value and "\0" not in value,
            "Codex skills path must be portable")
    relative = PurePosixPath(value)
    require(not relative.is_absolute() and not re.match(r"^[A-Za-z]:", value),
            "Codex skills path must be relative")
    require(".." not in relative.parts, "Codex skills path must not escape the plugin")
    path = root
    for part in relative.parts:
        path = path / part
        require(not path.is_symlink(), "Codex skills path must not contain a symlink")
    require(path.is_dir(), "Codex skills path must name an existing directory")
    require(path.resolve() == (root / "skills").resolve(),
            "Codex skills path must select the shared skills directory")
    require(set(inventory) == {p.name for p in path.iterdir() if p.is_dir()}
            and all(p.is_dir() and not p.is_symlink() for p in path.iterdir()),
            "Codex skill inventory mismatch")
    return path


def validate(root, require_merged=False):
    def read(path):
        return json.loads((root / path).read_text())

    manifests = [read(p) for p in ["plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json"]]
    manifest = manifests[0]
    for key in ["name", "version", "description", "author", "license", "repository"]:
        require(all(m.get(key) == manifest[key] for m in manifests), f"Manifest mismatch: {key}")
    require(re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", manifest["version"]), "Invalid plugin version")
    require(manifest["license"] == "MIT" and (root / "LICENSE").read_text().startswith("MIT License\n"),
            "Missing distribution license")
    catalogs = [read(".agents/plugins/marketplace.json"), read(".claude-plugin/marketplace.json")]
    require(all(c["name"] == "innosquad" for c in catalogs), "Marketplace identity mismatch")
    require(all(len(c["plugins"]) == 1 and c["plugins"][0]["name"] == manifest["name"] for c in catalogs),
            "Marketplace plugin inventory mismatch")
    require(catalogs[0]["plugins"][0]["source"] == {"source": "local", "path": "./"}, "Codex source must stay inside fetched repo")
    require(catalogs[1]["plugins"][0]["source"] == "./", "Claude source must stay inside fetched repo")
    for key in ["version", "description"]:
        require(catalogs[1]["plugins"][0][key] == manifest[key], f"Claude marketplace mismatch: {key}")
    lock = read("sources.lock.json")["skills"]
    codex_skills_path(root, manifests[1].get("skills"), lock)
    for name, pin in lock.items():
        require(pin["path"] == "skills/" + name, f"Unexpected source path: {name}")
        skill = root / pin["path"]
        require(tree_id(skill) == pin["git_tree"], f"Snapshot differs from source tree: {name}")
        require(re.fullmatch(r"[0-9a-f]{40}", pin["revision"]), f"Source is not immutable: {name}")
        require(pin["source_status"] in {"released", "merged", "pull_request"}, f"Unknown source status: {name}")
        if require_merged:
            require(pin["source_status"] in {"released", "merged"}, f"Source still awaits merge: {name}")
        support = read(pin["path"] + "/references/support.json")
        # DI's earlier source schema expresses stable patches through its range/channel.
        if "supported_version_range" in support and support.get("supported_release_channel") == "stable":
            line = re.fullmatch(r">=(\d+)\.(\d+)\.0 <(\d+)\.(\d+)\.0", support["supported_version_range"])
            require(line and line[1] == line[3] and int(line[4]) == int(line[2]) + 1,
                    f"Unsupported legacy patch range: {name}")
            support.setdefault("supported_release_line", f"{line[1]}.{line[2]}.x")
            support.setdefault("include_prereleases", False)
        for key, value in pin["library"].items():
            field = "supported_version_range" if key == "supported_range" and "supported_version_range" in support else key
            require(support.get(field) == value, f"Support mismatch: {name}.{key}")
        if "core_requirement" in pin:
            for key, value in pin["core_requirement"].items():
                require(support["core_requirement"].get(key) == value, f"Core requirement mismatch: {name}.{key}")
        require((skill / "THIRD_PARTY_NOTICES.md").is_file(), f"Missing source notice: {name}")
        text = (skill / "SKILL.md").read_text()
        require(text.startswith("---\n") and re.search(r"^name: " + re.escape(name) + r"$", text, re.M),
                f"Invalid skill name: {name}")
        require(re.search(r"^description: .+", text, re.M), f"Missing discovery description: {name}")
        for page in skill.rglob("*.md"):
            for link in re.findall(r"\]\(([^)]+)\)", page.read_text()):
                if link.startswith(("https:", "http:", "#")):
                    continue
                target = (page.parent / unquote(link.split("#")[0])).resolve()
                require(target.is_relative_to(skill.resolve()) and target.exists(), f"Broken/nonportable skill link: {page}: {link}")
    return {"status": "passed", "version": manifest["version"], "skills": len(lock),
            "source_tree_equality": True, "require_merged": require_merged}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--require-merged", action="store_true",
                        help="Reject review-branch inputs; remote status and release checks remain separate")
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.root.resolve(), args.require_merged), indent=2))
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f"Bundle validation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
