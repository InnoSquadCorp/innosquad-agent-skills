# Stream installation and AI evaluation — 2026-10-09

Alpha.11 adds the sixth library-owned skill, `innonetwork-stream`. Both native
hosts installed and registered the plugin. Codex passed four representative
selection/policy cases; final generated code passed **25 tests** independently.
Claude registered all six Inno skills, but OAuth 401 blocked generation before
model use. [Machine-readable evidence](host-evaluation-innonetwork-stream.json).

## Source and supported baseline

[Stream PR #9](https://github.com/InnoSquadCorp/InnoNetwork-Stream/pull/9) was
created for this work and merged remotely during evaluation, at
2026-10-08T15:50:33Z (2026-10-09 KST). The central snapshot pins merge commit
`81f945f751090aed7c696e4c453816e01df5dd93`, tree
`e0265a81762cd94656c16f53b466faa93c3b1e36`. Its 13 runtime files exactly match
evaluated source `bc8b79ea7a96adc4185493115536fcedebbc23b6` by paths, bytes and
modes. No instruction, metadata, code or fixture changed on merge.

The independently validated API baseline is captured main
`bd50e877644ded1b739f66bdd8fb604908606e4b`, intended for **6.1.1**, with Core
**exact 6.1.1**, `44e4ca28c50c03f817231a077c0f3bdfdbc859c8`. Stream had no
6.1.1 tag or GitHub Release at the initial and post-merge checks. `version: null`
and `unreleased_main_commit` preserve the distinction. Planned stable support is
`>=6.1.0 <6.2.0`, excluding prereleases. Verify the eventual tag and differences,
then run an exact-tag consumer before release qualification. Another Stream
patch needs its own manifest/API/consumer checks; arbitrary Core upgrades are
not permitted by this range.

The source-owned fixture passed **13 tests**, all seven exact remote pins,
active graph/workspace/prebuilt and clean checkout verification, strict Swift 6
concurrency and warnings-as-errors on Xcode 27 / Swift 6.4, macOS 27 arm64.
Wrong revision and local Core override controls failed before Swift commands.
Draft release-state and CI workflow lint passed; repository swift-format passed
329 files. See [source validation](https://github.com/InnoSquadCorp/InnoNetwork-Stream/blob/bc8b79ea7a96adc4185493115536fcedebbc23b6/skills/validation.md).
Original Stream checkouts and their existing generated/uncommitted work were
preserved; authoring occurred in a separate worktree.

## Native host cases

Desktop-bundled Codex CLI **0.162.0-alpha.2** used fresh ephemeral sessions,
without a model override (configured `gpt-6.1-sol` / `xhigh`). Session-only
configuration disabled unrelated tools/plugins, memory and personal/system
skills; all six Inno skills remained available. The model received only each
prompt and an empty exact-manifest/lock consumer, not grading criteria, prior
conversation or intended answers. [Prompts and acceptance](../evals/archive/innonetwork-stream-alpha.11.json).

| Case | Observed behavior | Independent final result |
| --- | --- | --- |
| Korean offline media | Implicitly read Stream; macro limits, selected audio/subtitles, task/handle ownership, concurrency and rejection tests | 10 tests PASS |
| English Live/DVR/native | Explicitly read Stream; dynamic equivalents, supplied transport/client, terminal DVR functions, MainActor playback and ENDLIST | 8 tests PASS |
| English generic AsyncStream | Did not read Stream skill; ordinary bounded in-memory sequence utility | 7 tests PASS |
| Korean version/platform policy | Read Stream; planned patch range vs unreleased baseline, exact Core dependency and decoded-audio gates | PASS; no project changes |

The generic AsyncStream session passed seven tests in a temporary dependency-free
package after its full-graph attempt was blocked by sandbox cache/fetch access.
The evaluator then passed all seven unchanged tests with the actual pinned full
graph; the standalone result is not substituted for this dependency evidence.

Generated outputs were compiled without evaluator edits. Validation checked the
manifest/lock, source hashes and exact graph/checkouts before/after tests.
Parameterized inputs are not counted as additional test declarations. No
separate evaluator repair sessions were supplied.

The offline run required model self-correction within its session. Its initial
mock playlist included unsupported DISCONTINUITY; a copied evaluator diagnostic
also reproduced that backend rejection without modifying the model workspace.
The model switched the success fixture to supported input and added an explicit
unsupported-input control. Its initial whole-receipt equality was corrected to
persisted fields when reopening a package.

The Codex sandbox returned zero from the important-usage capacity query while
an unsandboxed control returned positive capacity. The model retained the
production default required-capacity policy and parameterized a **test-only**
workflow with capacity checking disabled. The generated suite therefore validates
mocked transfer/ownership behavior separately from capacity admission; the source
fixture tests transfers with its default policy in the normal validation host.
Final generated output passed independently, including concurrency and cancellation.
Earlier failures are retained in local traces and are not presented as an initial
one-shot pass.

Claude Code **2.1.285** used a fresh native installed session with hooks disabled
and empty MCP configuration for that invocation. Startup registered all six
Inno skills, including `innosquad:innonetwork-stream`. **HTTP 401: OAuth access
token is invalid** occurred before model use, with zero input/output tokens.
Installation/registration is confirmed; actual Claude selection and generation
remain unverified. No login or credential settings were changed.

## Packaging and boundaries

All six source snapshots match their pinned Git trees and both installed runtime
caches: DI 14, Network 13, Flow 14, Router 14, Protobuf 13 and Stream 13 files.
Root/Codex/Claude identities and versions, catalog, portable schema, structure
and relative runtime links passed. Claude retains the existing optional
marketplace-description warning. Earlier caches are preserved.

The five earlier runtime snapshots and pins remain unchanged. Their historical
behavioral reports are not alpha.11 reruns. This is a representative fresh set,
not a repeated full bilingual matrix or no-plugin efficacy comparison. No actual
DVR recording/player launch, device/FairPlay/background restoration, audio delivery,
full release matrix, alternate toolchain/platform or future patch is qualified.
Source PR merge was observed independently; remote CI and eventual tag/Release
qualification remain distinct. This work did not execute a merge, tag creation,
public Release or public marketplace publication.

At the final check, the [merge-commit CI run](https://github.com/InnoSquadCorp/InnoNetwork-Stream/actions/runs/37804053326) for `81f945f` was queued. Local consumer results do not establish a completed remote CI run.
