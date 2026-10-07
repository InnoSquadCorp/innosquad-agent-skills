# InnoRouter installation and AI evaluation — 2026-10-07

Local plugin **0.1.0-alpha.8** adds Router beside unchanged DI, Network and Flow
snapshots. Codex and Claude Code were updated through native plugin commands.
Codex completed four representative cases; the transient-presentation case needed
two diagnostic-driven model repairs. Claude registered all four skills, but its
generation request failed with OAuth 401 before model-token use.
[Machine-readable evidence](host-evaluation-innorouter.json).

## Source, planned support and exact candidate

[InnoRouter PR #66](https://github.com/InnoSquadCorp/InnoRouter/pull/66) merged on 2026-10-07.
The final snapshot pins merge commit `3ed5ea0d6b07c1b282182c6e5468dd3ed962c402`, 14-file tree
`eac03752e4acf3b9329846f2cc6002a05d5a5718`. It exactly matches the evaluated source
`f790079eb7a6465bacf69946eac332e9df4028c3`; runtime/tests/manifest/lock also have no
diff between those commits. The merge was observed during final verification,
not performed by this evaluation.
The separate library baseline is **unreleased main**
`851c63f095e49b700c3a0aa8152a3521a39977e7`, intended for 7.0.0. The 7.0.0 tag lookup
returned 404 at the recorded check. Runtime version/changelog dates do not prove
publication. `version: null` and `baseline_kind: unreleased_main_commit` retain
this distinction in the source support record and central lock.

Planned stable support is `>=7.0.0 <7.1.0`, excluding prereleases. When 7.0.0 ships,
inspect the actual tag/commit and API/manifest changes and run an exact-tag consumer
before qualifying a released baseline. Later patches keep their actual version
and receive patch-specific validation; the declared range is not a tested matrix.

The source helper passed **11 exact remote candidate tests**, with SwiftSyntax
604.0.0, strict concurrency and warnings as errors. It verified manifest/lock,
active graph/workspace, clean checkout SHAs and SwiftSyntax prebuilt. Wrong-SHA
input was rejected before build. The initial fixture authoring errors and passing
rerun remain in the [source validation record](https://github.com/InnoSquadCorp/InnoRouter/blob/f790079eb7a6465bacf69946eac332e9df4028c3/skills/validation.md).

## Source repository gates

At source head `f790079eb7a6465bacf69946eac332e9df4028c3`, the full default
`./scripts/principle-gates.sh` completed successfully. Its root Swift suites ran
**1,393 tests**, with one deliberately captured `withKnownIssue` checking that
`RouterTestStore.finish()` diagnoses pending deferrals. This is an expected
harness test, not a newly discovered library defect.

DocC preview, all three public API baselines, documentation contracts and nine
compiled snippets, example targets, independent macro/feature consumers, generated
scenario consumers, source lint, recursive-link and fail-fast probes passed.
The fail-fast probe intentionally traps when authority is missing; the gate
checked its expected diagnostic. The optional full platform probe was not run.
This local source gate is separate from the exact remote skill fixture, installed
AI evaluation, remote CI and eventual release qualification.

## Fresh installed-host cases

Codex CLI 0.160.1 used fresh ephemeral sessions without a model override; the
user's configuration at the final check was `gpt-6.1-sol` / `xhigh`. Initial
workspaces contained an exact candidate manifest/lock and empty source/test
placeholders. Only the task prompt was supplied, with no prior conversation or
grading criteria. Session overrides disabled unrelated skills/plugins, MCP and
memory; all four Inno skills remained available for routing. Persistent user
configuration was unchanged.

| Case | Observed behavior | Independent result |
| --- | --- | --- |
| Korean navigation/deep link | Implicit Router skill read; macro route, Host/environment actions, allowlisted shared pipeline, exhaustive state/revision events | First pass: 7 tests PASS |
| English typed transient presentation | Explicit Router skill read; Delete/Keep values, caller cancellation, stale callback rejection, encode-only omission | 3 tests PASS after two model repairs |
| English unrelated formatter | No Inno skill read; trims input with Guest fallback | First pass: 2 new tests + 1 retained seed PASS |
| Korean candidate/patch policy | Implicit Router skill read; distinguishes unreleased commit from planned 7.0.x, requires actual tag checks | First pass; no edits/build/external lookup |

The transient case first failed to compile because an `inout AsyncStream.Iterator`
helper lost actor isolation. A fresh session received the unchanged generated
files and compiler diagnostics. Its repair used `next(isolation: #isolation)`;
the next run compiled but failed one overly specific stale-handle assertion.
The pinned implementation rejects that post-cancellation call as
`presentationIdentityMismatch(..., actual: nil)`, before lifetime validation,
whereas the generated assertion expected `expiredPresentation`.

A second fresh repair received only that observed failure and the existing code.
The model checked the source, corrected the expected reason, retained cancellation,
rejection, exhaustive events and revision assertions, and added a post-rejection
state assertion. All three tests then passed. The evaluator never manually edited
generated code. The first failures and both repairs are retained separately; this
is **not first-pass success for all cases**, and does not measure whether the skill
alone improved model efficacy. The source skill itself was unchanged during repairs.

Independent execution checked exact remote pins, active graph/workspace/checkouts,
unchanged manifest/lock and source hashes. Builds used Xcode 27 / Swift 6.4 on macOS
27 arm64, complete strict concurrency and warnings as errors. Final successful
generated coverage is **10 Router tests**, plus **2 new formatter tests** and one
unchanged seed test. Parameterized invocations are not counted as additional test
declarations. [Evaluation prompts and repair diagnostics](../evals/innorouter.json).

Claude Code 2.1.285 installed alpha.8 and startup registered `innosquad:innodi`,
`innosquad:innoflow`, `innosquad:innonetwork`, and `innosquad:innorouter`. Its fresh
generation attempt failed with **HTTP 401: OAuth access token is invalid**, with
zero model tokens. Native registration is confirmed; AI behavior is unverified.

## Packaging and boundaries

Source↔central and central↔both installed runtime caches match by every path, byte
and mode: DI 14, Network 13, Flow 14 and Router 14 files. Root/Codex/Claude identity,
catalog metadata, portable schema, skill structure, local links and Claude manifest
checks passed. Marketplace validation retains the existing optional-description warning.

Earlier DI/Network/Flow host results are dated historical evidence, not alpha.8
reruns. These cases do not cover native UI/scene lifecycle, all migration paths,
feature/split/Inspector integration, alternate toolchains, later patches or a
combined-library runtime consumer. Library remote CI and release qualification
are separate. No merge, tag/Release change, public marketplace publication or
automatic snapshot collection was performed by this evaluation.
