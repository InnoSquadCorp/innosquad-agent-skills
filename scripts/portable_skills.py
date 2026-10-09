#!/usr/bin/env python3
"""Install unchanged Agent Skills or export self-contained chat reference packs."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile
import zipfile

from validate_bundle import tree_id, validate


ROOT = Path(__file__).resolve().parents[1]
HOST_PATHS = {
    "agents": ".agents/skills", "codex": ".agents/skills",
    "claude": ".claude/skills", "grok": ".grok/skills",
    "gemini": ".gemini/skills", "cursor": ".cursor/skills",
    "copilot": ".github/skills",
}
CHAT_GUIDANCE = """Use only the library references relevant to the user's task.
First establish the project's actual resolved library version and revision.
Keep its dependency choices; a bundled exact baseline is not a downgrade target.
Support ranges do not prove every patch was tested. Stream remains a planned baseline.
The file sections below preserve the original library-owned instructions and resources.
Relative paths inside a file refer to other named sections of the same skill.
In a chat or text-only API, scripts and examples are reference text, not executed tools.
Ask for relevant manifest, lockfile and source context if unavailable. Never claim
to have inspected a repository, run Swift tests, or validated a device without evidence.
The user's requested scope governs adoption, dependency changes and external actions.
"""


def selection(root, names=None):
    validate(root)
    lock = json.loads((root / "sources.lock.json").read_text())["skills"]
    chosen = sorted(set(names or lock))
    unknown = set(chosen) - set(lock)
    if unknown:
        raise ValueError("Unknown skills: " + ", ".join(sorted(unknown)))
    return {name: lock[name] for name in chosen}


def catalog(root, pins):
    version = json.loads((root / "plugin.json").read_text())["version"]
    entries = []
    for name, pin in pins.items():
        text = (root / pin["path"] / "SKILL.md").read_text()
        entries.append({"name": name, "description": re.search(r"^description: (.+)$", text, re.M)[1],
                        "context_file": name + ".md", "source": pin})
    return {"schema_version": 1, "plugin_version": version, "skills": entries}


def context_markdown(root, name, pin):
    """Keep original files verbatim inside labeled fences, including all notices."""
    version = json.loads((root / "plugin.json").read_text())["version"]
    lines = [f"# {name} — InnoSquad {version}", "", CHAT_GUIDANCE,
             f"Source: {pin['repository']} at `{pin['revision']}`",
             f"Skill Git tree: `{pin['git_tree']}`", "",
             "Declared support and exact validation identity:",
             "```json", json.dumps(pin["library"], indent=2), "```", ""]
    skill = root / pin["path"]
    files = sorted((p for p in skill.rglob("*") if p.is_file()),
                   key=lambda p: (p.name != "SKILL.md", p.relative_to(skill).as_posix()))
    for path in files:
        data = path.read_text(encoding="utf-8")
        fence = "`" * max(4, max((len(x) + 1 for x in re.findall(r"`+", data)), default=0))
        lines.extend([f"## File: {name}/{path.relative_to(skill).as_posix()}", "", fence,
                      data.rstrip("\n"), fence, ""])
    return "\n".join(lines)


def safe_destination(project, relative):
    destination = project / relative
    for item in (destination, *destination.parents):
        if item == project:
            break
        if item.is_symlink():
            raise ValueError(f"Refusing a symlink destination: {item}")
    return destination


def install(root, pins, project, host, dry_run=False):
    project = project.expanduser().resolve(strict=True)
    if not project.is_dir():
        raise ValueError("Project must be an existing directory")
    base = safe_destination(project, HOST_PATHS[host])
    plan = []
    for name, pin in pins.items():
        target = safe_destination(project, HOST_PATHS[host] + "/" + name)
        if target.exists():
            if not target.is_dir() or tree_id(target) != pin["git_tree"]:
                raise ValueError(f"Existing skill differs; preserve it and choose another destination: {target}")
            status = "unchanged"
        else:
            status = "install"
        plan.append({"skill": name, "destination": str(target), "status": status,
                     "git_tree": pin["git_tree"]})
    if dry_run:
        return {"dry_run": True, "host": host, "skills": plan}
    base.mkdir(parents=True, exist_ok=True)
    # Prepare every copy before publishing any; existing different skills are never replaced.
    with tempfile.TemporaryDirectory(prefix=".innosquad-stage-", dir=base) as scratch:
        staged = Path(scratch)
        for item in plan:
            if item["status"] == "install":
                name = item["skill"]
                shutil.copytree(root / pins[name]["path"], staged / name)
                if tree_id(staged / name) != pins[name]["git_tree"]:
                    raise ValueError(f"Copy changed source identity: {name}")
        for item in plan:
            if item["status"] == "install":
                target = Path(item["destination"])
                if target.exists() or target.is_symlink():
                    raise ValueError(f"Destination changed during install: {target}")
                (staged / item["skill"]).rename(target)
                item["status"] = "installed"
    return {"dry_run": False, "host": host, "skills": plan}


def export_pack(root, pins, output):
    output = output.expanduser().absolute()
    if output.exists() or output.is_symlink():
        raise ValueError("Export directory must not exist; use a new path to preserve earlier exports")
    # Do not accidentally contaminate the immutable source snapshots.
    if output.resolve().is_relative_to((root / "skills").resolve()):
        raise ValueError("Export outside the source skills directory")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".innosquad-export-", dir=output.parent) as scratch:
        staged = Path(scratch) / "pack"
        staged.mkdir()
        index = catalog(root, pins)
        (staged / "catalog.json").write_text(json.dumps(index, indent=2) + "\n")
        for name, pin in pins.items():
            (staged / (name + ".md")).write_text(context_markdown(root, name, pin))
        rows = [f"- `{e['context_file']}` — {e['description']}" for e in index["skills"]]
        (staged / "START_HERE.md").write_text(
            "# InnoSquad chat reference pack\n\n" + CHAT_GUIDANCE +
            "\nAttach or paste the relevant .md file into Grok, ChatGPT, Gemini or another text-capable assistant. "
            "Do not assume the chat can unpack a ZIP or access your local repository. "
            "If an upload is unavailable or too large, paste the relevant labeled file sections, "
            "keeping SKILL.md, support.json and their notices. "
            "Ask the assistant to confirm the baseline it read before generating code.\n\n" +
            "\n".join(rows) + "\n\nExample request:\n\n"
            "> 첨부한 스킬을 적용하고 실제 Package.resolved 버전에 맞춰 구현해줘. "
            "실행하지 않은 테스트는 실행했다고 말하지 말아줘.\n\n"
            "`innosquad-skills.zip` contains unchanged native skill directories, not a web-chat plugin.\n")
        with zipfile.ZipFile(staged / "innosquad-skills.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
            members = [("LICENSE", (root / "LICENSE").read_bytes(), 0o100644),
                       ("sources.lock.json", (json.dumps({"schema_version": 1, "skills": pins}, indent=2) + "\n").encode(), 0o100644)]
            for pin in pins.values():
                for path in sorted((root / pin["path"]).rglob("*")):
                    if path.is_file():
                        mode = 0o100755 if path.stat().st_mode & stat.S_IXUSR else 0o100644
                        members.append((path.relative_to(root).as_posix(), path.read_bytes(), mode))
            for name, data, mode in sorted(members):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = mode << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, data)
        checksums = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(staged.iterdir())}
        (staged / "sha256.json").write_text(json.dumps(checksums, indent=2) + "\n")
        staged.rename(output)
    return {"output": str(output), "skills": list(pins), "sha256": checksums}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    local = sub.add_parser("install", help="Copy original skills into a project; never overwrite different content")
    local.add_argument("--host", choices=HOST_PATHS, required=True)
    local.add_argument("--project", type=Path, required=True)
    local.add_argument("--dry-run", action="store_true")
    pack = sub.add_parser("export", help="Write Markdown references and a portable skill ZIP")
    pack.add_argument("--output", type=Path, required=True)
    for command in (local, pack):
        command.add_argument("--skill", action="append", help="Repeat to select skills; default: all six")
    args = parser.parse_args()
    try:
        pins = selection(ROOT, args.skill)
        result = (install(ROOT, pins, args.project, args.host, args.dry_run) if args.command == "install"
                  else export_pack(ROOT, pins, args.output))
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f"Portable skills: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
