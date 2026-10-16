# 1.0.0 preparation

Manifests and the Claude marketplace declare 1.0.0 so the package can be
reviewed and validated as a unit. Actual publication is recorded in the
[private v1.0.0 Release](https://github.com/InnoSquadCorp/innosquad-agent-skills/releases/tag/v1.0.0)
and separate verification evidence. Packaging tools do not create tags, publish
a GitHub Release, change visibility or submit to directories.

## What is included

- Six independently versioned library skill snapshots. Stream now validates
  published 6.1.1 with a fresh representative Codex portable-skill evaluation.
  Flow now uses its canonical published 6.0.2 fixture and updated diagnostics;
  its supported range remains 6.0.x. Router's source now comes from published
  7.0.1, with only two upstream reference corrections and its 7.0.0 fixture retained.
- Codex and Claude native manifests/catalogs; portable installation for Gemini,
  Cursor, Copilot, Grok and common Agent Skills directories.
- Gemini 0.24.0 setup guidance and accurate host qualification levels. Copilot's
  GPT-4.1 evaluation is recorded as failed, not silently promoted to supported.
- Deterministic native plugin ZIP, per-library Markdown/native skill reference
  pack, immutable skill-source records and SHA-256 checksums.
- Stream supports stable 6.1.x and validates published 6.1.1 at `2af03b2`,
  including remote tag checks and 13 passing exact-release consumer tests.

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

Current upstream status was read on **2026-10-11 KST**; see
[the recorded snapshot](release-status-1.0.0.json) and
[Flow/Router follow-up](flow-router-followup-2026-10-10.md). Router's released
source was refreshed on 2026-10-16; see the [7.0.1 record](router-7.0.1-refresh-2026-10-16.md).
Recheck at the final commit.

| Condition | Current preparation state | Completion evidence |
| --- | --- | --- |
| Canonical source corrections | All six correction PRs merged; Router subsequently advanced to released source `482587b` | Actual merged/released pins and all six canonical directories verified by paths, blob bytes and executable modes; `--require-merged` passes |
| Bundle integrity | Version 1.0.0; Flow, Stream and Router refreshed from canonical sources | Bundle tests and source-tree equality on final commit; Router source release recorded separately from its unchanged 7.0.0 baseline |
| Central Swift consumers | Six original exact consumers plus isolated Router 7.0.1 on Xcode 27.0 / Swift 6.4 / macOS 27; Protobuf uses its reviewed reissued release mode | All seven jobs pass at the final commit; [toolchain, resolved pins, original/adjusted inputs and failure artifacts](consumer-ci.md) retained separately from bundle/mock tests |
| Central PR / CI | PR #1 remains the preparation vehicle; the Flow/Router follow-up updates its source pins without publishing | Final commit pushed, remote SHA equality, required checks passed, reviewed merge |
| Host claims | Evidence and limitations documented | Preserve dates/models/versions; only promote a blocked or failed host after a successful new evaluation |
| Stream | Published 6.1.1 `2af03b2`; 13 exact-release consumer tests passed | Canonical PR #14 passed its checks and merged at `7fb61ac`; merge-tree equality verified separately from release-consumer proof |
| Protobuf | Reissued 6.1.1 tag `ba6ab8d`, tag object `eaea83c…`; historical fixture retained | User confirmed no previous installs and accepts keeping 6.1.1; preserve release-mode checks and historical fixture identity |
| Audience | Central repository is private | Confirm access for the intended audience; a public launch requires the corresponding explicit visibility/publication action |
| Final install | Candidate can be installed from an extracted package/local catalog | Clean install from the immutable final commit/tag, all six trees equal to the lock, no stale duplicate plugin entries |
| Publication | Requires the initial private v1.0.0 tag/Release after all gates pass | Tag points to the reviewed merged commit; uploaded checksums match; fresh remote installation verified |

Authentication-blocked Claude/Gemini/Cursor runs and Copilot's failed GPT-4.1 run
are limitations, not tests to mark green because files copied successfully.
The earlier dated native-host evidence remains separate. Grok live model behavior
and official-directory approval are not part of the confirmed 1.0.0 claims.

## Build the final package after source verification

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

## Initial private release procedure

Keep the existing private repository and audience. Complete current-head CI,
remove Draft from PR #1, and use a normal allowed merge with the reviewed head
SHA as the lease. Never use an administrative/protection bypass. Verify the
actual merged commit and its main-branch CI separately.

Build the final package from that clean merged commit. Create the initial
annotated `v1.0.0` tag at exactly that commit only after confirming the tag does
not already exist. Push only that tag, verify its remote tag object and peeled
commit, and wait for **tag-triggered CI**, including all seven consumers and the
merged-source packaging gate. The workflow retains the tagged package as a
`package-v1.0.0-<run-id>` artifact; it does not publish it.

Use the verified tagged package as the release payload. Its twelve files listed
in `SHA256SUMS`, plus `SHA256SUMS` itself, become thirteen Release assets. Asset
filenames are unique; retain each original relative path as the asset label.
When downloading the flat Release assets, reconstruct `references/` from those
manifest paths before verifying every checksum. Do not rewrite the builder's
`release.json`: `remote_checks: not_run` and `publication_performed: false`
describe the builder. Record actual remote CI, tag and publication verification
separately.

Create a draft Release with `--verify-tag`, upload the complete payload, download
it again and check inventory, bytes and checksums. Publish only after this
verification, then verify the published Release metadata, fresh downloads,
immutable tag and private visibility again. Record publication evidence in
`docs/release-verification-1.0.0.json` and update the current README, installation
instructions and release notes after publication. Do not alter access or submit
to public directories.

## Release handoff

Use `v1.0.0` only for the reviewed merged commit after the conditions above are
satisfied. The draft [release notes](release-notes-1.0.0.md) describe the supported
scope and limitations. The plugin ZIP and reference pack have different purposes;
include their checksums and provenance with any uploaded assets.

A tag or GitHub release is not an official marketplace-directory listing. A
private release is not public availability. Update this document, the README and
installation instructions with the actual tag URL and publication evidence after
those actions complete. Preserve the evaluation history.
