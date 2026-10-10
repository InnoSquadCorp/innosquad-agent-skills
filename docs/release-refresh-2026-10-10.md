# Published-library refresh — 2026-10-10 KST

This refresh starts from central `d0b32c0` and preserves the library-owned skill
policy and patch support lines. Public tag identities remain unchanged. It does
not publish plugin 1.0.0. See [source/check snapshot](release-status-1.0.0.json).

## Canonical corrections

| Source | Work completed | Remaining remote gate |
| --- | --- | --- |
| Network #153 | JSON/stderr fix merged at `d5213fb`; exact skill tree unchanged | Merge-commit CI is separate from the passing PR checks |
| Protobuf #9 | Previously merged JSON/stderr fix retained at `06e091d` | No new source change |
| DI #59 | Rebasing observed; pin refreshed to `ae4eef4`; skill tree unchanged, four local regression tests pass | Cancelled duplicate CI recorded; current validation still running |
| Flow #63 | JSON/stderr fix plus post-publication `STABLE_VERSION=6.0.2`, multilingual README and release documentation at `c0d7197` | Fresh required CI and merge |
| Router #70 | Four local validator regression tests pass; skill tree unchanged at `4c2eafa` | Failed visionOS native deferred-scene runtime check rerun; no gate waived |
| Stream #14 | JSON/stderr fix plus published 6.1.1 baseline at `7fa6606` | Fresh required CI and merge |

Flow's public 6.0.2 release body now reports its actual publication and successful
Release Gate run 37826649872. The annotated tag object `60b85f6` and commit
`1176de1` were identical before/after editing the body. The stable-marker source
change is in PR #63 until merge; the immutable tag keeps its candidate metadata.
Release synchronization, four validator-output tests, four timeout tests and the
principle-gates selftest passed locally. The 28-check release preflight was not
rerun locally; its prior release CI is linked as historical publication evidence.

## Stream release consumer

The canonical fixture now requires exact Stream 6.1.1 at `2af03b2`, with exact
Core 6.1.1 at `44e4ca2`. On Xcode 27 / Swift 6.4, macOS 27 arm64, **13 Swift
Testing tests passed**, strict concurrency complete and warnings as errors.
All seven resolved dependencies matched active graph/workspace/prebuilt identity,
clean checkouts and unchanged source/lock hashes before/after tests. The remote
annotated tag `c8b74e3` and peeled commit also matched before/after execution.

Six validator automation tests passed, including warning-bearing JSON success,
nonzero exit, malformed JSON, graph drift, missing/wrong tag and tag movement
rejection. Sanitized evidence lives in the
[owning repository](https://github.com/InnoSquadCorp/InnoNetwork-Stream/blob/7fa66060374b16fba37a1486b1b4cdcdd2d441dd/skills/validation/release-6.1.1-evidence.json).
The earlier unpublished-baseline evidence is retained as dated history.

This is fixture and validator proof. Device playback, FairPlay, background
restoration, full HLS conformance and other patches are not newly qualified.
Native host findings are tracked separately from the consumer suite.

## Fresh host and bundle evidence

Codex CLI 0.162.0-alpha.17.2 received all six skills in an isolated project
`.agents/skills` installation. A natural-language Stream request implicitly read
its skill, support/compatibility/download references and manifest. It identified
published 6.1.1 separately from support range 6.1.x, retained exact Core 6.1.1
and generated the playback URL helper using `receipt.entryPlaylistURL`.

The generated Swift was compiled without manual repair inside a disposable copy
of the exact-release consumer; its 13 unchanged fixture tests passed with graph,
checkout, source-hash and tag checks. This is a representative portable-skill
selection/generation check, not a new full native-plugin host matrix or 13
AI-generated tests. [Sanitized evidence](host-evaluation-stream-release.json).
Existing authentication/model limitations of other hosts are unchanged.

All **28 bundle tests passed**, including portable installation and packaging
controls. Both Claude marketplace/plugin manifests validated. All six snapshots
match their canonical commit trees. `--require-merged` correctly rejects pending
sources; no status was relabeled to bypass that gate.

The subsequent packaging-guidance correction removes leftover planned/preview
claims from the plugin descriptions, chat/API introduction and current Stream
evaluation definition. The introduction now delegates version status to each
selected skill's support record. The alpha.11 prompts are archived unchanged,
and their historical evaluation report links to that archive. Two regression
tests failed against the earlier guidance and passed after correction; the full
suite now has **30 passing tests**. This correction does not change the six skill
trees or claim a new live-model evaluation.

## Protobuf version decision

The user confirmed there were no previous installations and accepts keeping the
reissued 6.1.1 tag (`ba6ab8d`, annotated object `eaea83c`). This refresh neither
moves that tag nor creates 6.1.2. Historical fixture identity and the release-mode
validator remain explicit. Earlier fingerprint conflicts in an environment that
recorded the old tag remain historical findings, not a current install claim.

## Distribution boundary

All six central snapshots must equal their exact canonical Git trees. Four
source records remain `pull_request`; final merged-source packaging must reject
them until actual merge evidence is recorded. Candidate packaging is allowed for
review. The central repository is private, and no plugin tag, release, directory
submission or visibility change is performed.
