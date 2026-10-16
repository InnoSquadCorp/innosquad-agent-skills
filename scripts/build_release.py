#!/usr/bin/env python3
"""Build deterministic plugin and reference archives without publishing anything."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import zipfile

from portable_skills import export_pack, selection
from validate_bundle import validate


ROOT = Path(__file__).resolve().parents[1]
FILES = ["plugin.json", "LICENSE", "README.md", "CHANGELOG.md", "sources.lock.json",
         ".codex-plugin/plugin.json", ".claude-plugin/plugin.json",
         ".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json"]
DIRECTORIES = ["skills", "scripts", "docs", "evals"]


def git_state(root):
    def git(*args):
        return subprocess.run(["git", "-C", str(root), *args], text=True,
                              capture_output=True, timeout=10, check=True).stdout.strip()
    try:
        if Path(git("rev-parse", "--show-toplevel")).resolve() != root.resolve():
            return {"commit": None, "dirty": None}
        return {"commit": git("rev-parse", "HEAD"),
                "dirty": bool(git("status", "--porcelain", "--untracked-files=normal"))}
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {"commit": None, "dirty": None}


def build(root, output, candidate=False):
    root = root.resolve()
    validated = validate(root, require_merged=not candidate)
    version = validated["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Release packaging requires a stable version in the manifests")
    source = git_state(root)
    if not candidate and (source["commit"] is None or source["dirty"] is not False):
        raise ValueError("Release packaging requires a clean committed worktree")
    output = output.expanduser().absolute()
    if output.exists() or output.is_symlink():
        raise ValueError("Output must not exist; preserve previous packages")
    for name in [*DIRECTORIES, ".codex-plugin", ".claude-plugin", ".agents", ".git"]:
        if output.resolve().is_relative_to(root / name):
            raise ValueError("Output must be outside distribution inputs")
    members = [root / name for name in FILES]
    for name in DIRECTORIES:
        directory = root / name
        if directory.is_symlink():
            raise ValueError(f"Distribution input is a symlink: {directory}")
        for path in sorted(directory.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Distribution input is a symlink: {path}")
            if path.is_file() and (name == "skills" or path.suffix in {".md", ".json", ".py"}):
                members.append(path)
    for path in members:
        if path.is_symlink() or not path.is_file() or any(p.is_symlink() for p in path.parents if p != root):
            raise ValueError(f"Missing or nonportable distribution input: {path}")
    if not candidate:
        tracked = set(subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                                     text=True, capture_output=True, timeout=10, check=True).stdout.split("\0"))
        if any(path.relative_to(root).as_posix() not in tracked for path in members):
            raise ValueError("Release inputs must be tracked; ignored/untracked files cannot be packaged")
    label = f"innosquad-{version}" + ("-candidate" if candidate else "")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".innosquad-release-", dir=output.parent) as temp:
        staged = Path(temp) / "package"
        staged.mkdir()
        archive_path = staged / f"{label}.zip"
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(members):
                info = zipfile.ZipInfo("innosquad/" + path.relative_to(root).as_posix(), (1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                mode = 0o100755 if path.stat().st_mode & stat.S_IXUSR else 0o100644
                info.external_attr = mode << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())
        export_pack(root, selection(root), staged / "references")
        metadata = {"schema_version": 1, "version": version,
                    "package_kind": "candidate" if candidate else "merged_source_package",
                    "source": source, "require_merged": not candidate,
                    "remote_checks": "not_run", "publication_performed": False,
                    "plugin_archive": archive_path.name,
                    "sources": json.loads((root / "sources.lock.json").read_text())["skills"]}
        (staged / "release.json").write_text(json.dumps(metadata, indent=2) + "\n")
        sums = {p.relative_to(staged).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(staged.rglob("*")) if p.is_file()}
        (staged / "SHA256SUMS").write_text("".join(f"{digest}  {name}\n" for name, digest in sums.items()))
        if not candidate and git_state(root) != source:
            raise ValueError("Worktree changed while building the release package")
        staged.rename(output)
    return {"output": str(output), "version": version, "package_kind": metadata["package_kind"],
            "plugin_archive": str(output / archive_path.name), "source": source,
            "publication_performed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--candidate", action="store_true",
                        help="Allow review-branch sources; label artifacts as unpublished candidates")
    args = parser.parse_args()
    try:
        print(json.dumps(build(ROOT, args.output, args.candidate), indent=2))
        return 0
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(f"Release packaging failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
