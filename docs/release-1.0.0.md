# 1.0.0 release

[v1.0.0](https://github.com/InnoSquadCorp/innosquad-agent-skills/releases/tag/v1.0.0)
was published on **2026-10-16 at 06:24:46 UTC**. After the content review, this
repository was made public at 06:28:00 UTC. The
[verification record](release-verification-1.0.0.json) records actual remote CI,
tag identity, uploaded/downloaded checksums, publication and anonymous access.

The immutable release source is `0c59bbd03541ff1d808e0d7a0efd2d9189e73ece`,
the actual merge of [PR #1](https://github.com/InnoSquadCorp/innosquad-agent-skills/pull/1).
Its annotated tag object is `ed3c6aab28a83ad23bc5ab5d5cec5af3e949af46`.
Later documentation commits record publication; they do not replace the tag or assets.

## Included scope

- Six library-owned skills, independently pinned by source commit, complete Git
  tree, bytes and executable modes. All six canonical correction PRs were
  rechecked as merged before tagging.
- Router source is published 7.0.1, with its two upstream reference corrections.
  Its original 7.0.0 fixture remains intact; a separate central-owned case verifies
  exact 7.0.1 with retained original/adjusted inputs and tag identity checks.
- Flow retains the canonical 6.0.2 fixture and 6.0.x support. Stream verifies
  published 6.1.1 plus exact Core 6.1.1. Protobuf uses the reviewed reissued 6.1.1
  release mode and preserves its historical fixture identity.
- Codex and Claude native catalogs, portable skills and chat reference files,
  original notices, deterministic archives and SHA-256 checksums.

## Verified gates

| Gate | Completed evidence |
| --- | --- |
| Source corrections | All six actual source PR merge identities and complete skill trees match the lock; Router released source is recorded separately from its 7.0.0 baseline |
| PR, actual merged-main and tag CI | Each passed the bundle and seven exact Swift consumers, 83 Swift tests per run; the tag bundle also passed 50 regression tests |
| Apple toolchain | Xcode 27.0, Apple Swift 6.4, macOS 27.0.1, SDK 27; actual pins, active workspace, clean checkouts and explicit builds checked |
| Package | Tagged CI passed the merged-source gate; its thirteen files were byte-identical to two clean local normal builds; 141 native ZIP members and all six skill trees verified |
| Draft and published assets | Thirteen names/labels/sizes/API digests and fresh downloaded bytes matched; all twelve manifest checksums passed |
| Final install | Fresh authenticated and anonymous tag clones installed all six exact trees into isolated projects; existing project settings preserved |
| Content review | 26 reachable commits, 367 unique blob versions, current PR prose/comments, tag metadata and actual assets including nested ZIPs reviewed; no credentials or nonpublic sensitive material found |
| Public delivery | Repository/release APIs, release page, all thirteen assets and tagged Codex manifest returned anonymously; credential-free Git clone and isolated install passed |

The [dated source snapshot](release-status-1.0.0.json),
[Flow/Router follow-up](flow-router-followup-2026-10-10.md) and
[Router source refresh](router-7.0.1-refresh-2026-10-16.md) remain historical
evidence. The separate verification record contains the final 2026-10-16 recheck.

## Reproduce the published package

Check out `v1.0.0` to reproduce the published inputs. Current main also includes
post-publication documentation. Use a clean worktree and a new output directory:

```bash
python3 -B scripts/validate_bundle.py --require-merged
python3 -B -m unittest discover -s tests -v
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
python3 -B scripts/build_release.py --output artifacts/1.0.0
```

The normal builder requires recorded merged/released sources, stable aligned
versions and clean tracked inputs. Candidate mode remains available with
`--candidate`; dirty candidates are not exact-commit evidence. Existing output
is never overwritten. Archive members retain original bytes/modes and fixed
timestamps; Git metadata, raw traces, credentials, caches and build output are excluded.

**The builder is a packaging gate.** Its immutable `release.json` still records
`remote_checks: not_run` and `publication_performed: false`. These fields describe
the builder, which does not merge, tag, upload, publish or call a model.
Actual remote/publication verification is recorded separately. Read-only CI
preserved the tag package as `package-v1.0.0-38860122764`; it did not publish it.

## Publication and delivery

The release was first published privately after PR/main/tag checks. The tag-CI
package supplied twelve files listed by `SHA256SUMS` plus the manifest itself.
Asset labels preserve original relative paths. Draft, published and anonymous
download checks matched every byte; restore `references/` before checking the
flat downloads as shown in [installation instructions](distribution.md).

The complete content review preceded the public visibility change. Only this
repository's visibility was requested to change; collaborator permissions were
not edited, credentials were not created and no external directory submission
was made. Tag and asset identities were checked again after the change.

## Qualification limits

Consumer resolve/build/test and delivery checks do not promote host-model or
device qualification. Preserve the dates, models and versions in
[host support](host-support.md) and evaluation records. Claude/Gemini/Cursor
authentication limits, Copilot GPT-4.1's failed generation evaluation, Grok's
missing live-model qualification and device/FairPlay/audio/integration boundaries
remain. A Git marketplace does not establish official-directory approval.
