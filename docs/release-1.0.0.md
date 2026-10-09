# 1.0.0 preparation

**Unreleased candidate.** Manifests and the Claude marketplace declare 1.0.0 so
that the proposed package can be reviewed and validated as a unit. No 1.0.0 tag,
GitHub Release, repository visibility change or directory submission is performed
by the packaging tools.

## What is included

- Six unchanged, independently versioned library skill snapshots from alpha.14.
- Codex and Claude native manifests/catalogs; portable installation for Gemini,
  Cursor, Copilot, Grok and common Agent Skills directories.
- Gemini 0.24.0 setup guidance and accurate host qualification levels. Copilot's
  GPT-4.1 evaluation is recorded as failed, not silently promoted to supported.
- Deterministic native plugin ZIP, per-library Markdown/native skill reference
  pack, immutable skill-source records and SHA-256 checksums.
- Stream is explicitly **preview**, based on an unreleased commit intended for
  6.1.1. Package version 1.0.0 does not make Stream 6.1.1 a published library.

## Local preparation

```bash
python3 -B scripts/validate_bundle.py
python3 -B -m unittest discover -s tests -v
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
python3 -B scripts/build_release.py --candidate --output artifacts/1.0.0-candidate
```

The output contains `innosquad-1.0.0-candidate.zip`, `references/`, `release.json`
and `SHA256SUMS`. Extract the ZIP and validate its `innosquad/` folder as well.
The archive contains manifests, catalogs, original skill files/modes, distributable
scripts, notices and documentation. It excludes repository-private traces, Git
metadata, tests, temporary build output and arbitrary untracked root files.
Archive entries have fixed timestamps. Existing output is never overwritten.

`release.json` records the inspected source commit and whether the worktree was
dirty. Candidate mode can package a worktree for review; a dirty candidate must
not be presented as exact-commit evidence. Rebuild from the clean reviewed commit
for the final handoff. `SHA256SUMS` covers every output except the checksum list
itself. No packaging mode calls a remote model, merges, tags, uploads or publishes.

## Publication conditions

Current upstream status was read on **2026-10-10 KST**; see
[the recorded snapshot](release-status-1.0.0.json). Recheck at the final commit.

| Condition | Current preparation state | Completion evidence |
| --- | --- | --- |
| Canonical source corrections | DI #59, Network #153, Flow #63, Router #70, Stream #14 are open Draft PRs with CI still pending; Protobuf #9 is merged | Owning-library merge/required checks and full skill-tree comparison; update lock to the actual merged revision |
| Bundle integrity | Version 1.0.0; six source trees unchanged | Bundle tests and source-tree equality on final commit |
| Central PR / CI | PR #1 is the preparation vehicle | Final commit pushed, remote SHA equality, required checks passed, reviewed merge |
| Host claims | Evidence and limitations documented | Preserve dates/models/versions; only promote a blocked or failed host after a successful new evaluation |
| Stream | No 6.1.1 tag found | Keep preview labeling; to advertise stable Stream 6.1.1, verify the actual tag and rerun its exact-release consumer in the owning repository first |
| Protobuf | Reissued 6.1.1 tag `ba6ab8d`, tag object `eaea83c…`; historical fixture retained | Use release-mode validator; do not relabel the revoked fixture as the current release |
| Audience | Central repository is private | Confirm access for the intended audience; a public launch requires the corresponding explicit visibility/publication action |
| Final install | Candidate can be installed from an extracted package/local catalog | Clean install from the immutable final commit/tag, all six trees equal to the lock, no stale duplicate plugin entries |
| Publication | No v1.0.0 tag/release yet | Tag points to the reviewed merged commit; uploaded checksums match; fresh remote installation verified |

Authentication-blocked Claude/Gemini/Cursor runs and Copilot's failed GPT-4.1 run
are limitations, not tests to mark green because files copied successfully.
The earlier dated native-host evidence remains separate. Grok live model behavior
and official-directory approval are not part of the confirmed 1.0.0 claims.

## Build the final package after source merges

After verifying the source PRs and refreshing exact merge pins/tree identities,
commit the final package changes and use a clean worktree:

```bash
python3 -B scripts/validate_bundle.py --require-merged
python3 -B scripts/build_release.py --output artifacts/1.0.0
```

The normal builder rejects a review-branch source, a non-stable manifest version,
a dirty/uncommitted worktree or an existing output destination. It produces
`innosquad-1.0.0.zip` with `package_kind: merged_source_package`.
**This is a packaging gate, not a live merge/CI/publication verifier.** Both modes
record `remote_checks: not_run` and `publication_performed: false`. Check upstream
states and final remote CI separately; never edit a status merely to bypass the gate.

CI builds a candidate on ordinary changes and applies the merged-source/clean-tree
packaging gate on version tags, including tag-to-manifest version agreement.
CI has read-only permissions and never creates a GitHub release.

## Release handoff

Use `v1.0.0` only for the reviewed merged commit after the conditions above are
satisfied. The draft [release notes](release-notes-1.0.0.md) describe the supported
scope and limitations. The plugin ZIP and reference pack have different purposes;
include their checksums and provenance with any uploaded assets.

A tag or GitHub release is not an official marketplace-directory listing. A
private release is not public availability. Update this document, the README and
installation instructions with the actual tag URL and publication evidence after
those actions complete. Preserve the evaluation history.
