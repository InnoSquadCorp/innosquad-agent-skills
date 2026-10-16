# Protobuf installation and AI evaluation — 2026-10-08

The local plugin adds `innonetwork-protobuf` beside the four unchanged Inno
skills. Fresh Codex sessions passed four representative selection/policy cases;
generated code passed **11 Protobuf tests + 2 Core JSON tests** independently.
Claude registered all five skills, but OAuth 401 blocked generation before model
token use. [Machine-readable evidence](host-evaluation-innonetwork-protobuf.json).

## Source and exact dependency pair

[Protobuf PR #7](https://github.com/InnoSquadCorp/InnoNetwork-Protobuf/pull/7)
owns the 13-file runtime skill. The final source is
`10721888976bea9d619cb66f2d2a57fd932a41f1`, tree
`2f0958d5095a396b4c77ef191cd1938110dd2ad7`. The source remains under review;
it is not included in the existing adapter tag.

Remote main and annotated adapter **6.1.1** both pointed to
`5e5f8316c94358235c3997e70e5e97aadc11df3a` when work began. The tag object is
`e37446078ad3e3e87e565ca2f1ce539ed75bb39e`. No adapter GitHub Release page was
found at check; its tag identity was verified separately. Core **6.1.1** is
published at `44e4ca28c50c03f817231a077c0f3bdfdbc859c8`, and the adapter manifest
requires exactly that version. Original checkout `d4336c3` was preserved.

Stable adapter support is `>=6.1.0 <6.2.0`, excluding prereleases. No 6.1.0 adapter
tag was found. The range does not invent earlier versions, qualify future patches
or permit arbitrary Core 6.1.x combinations. Another adapter patch keeps its
actual version, with manifest/API/tag and consumer checks for that pair.

## Consumer and source validation

The source-owned remote-tag fixture passed **14 tests**, with all eight remote
pins, active graph/workspace and clean checkout identities verified. It uses
SwiftProtobuf 1.38.1 and SwiftSyntax 604.0.0. Complete strict concurrency and
warnings as errors were enabled on macOS arm64, Xcode 27 / Swift 6.4. A wrong
baseline was rejected before resolution/build.

Source static contracts, 68 runtime + 2 macro tests, DocSmoke and the preferred
and compatibility-product consumers passed. Their source/sample dependency
integrity checks are separate from the fixture: the sample intentionally uses
the changed local adapter plus remote Core. Production runtime, manifest and
tests were unchanged. See the [source validation record](https://github.com/InnoSquadCorp/InnoNetwork-Protobuf/blob/10721888976bea9d619cb66f2d2a57fd932a41f1/skills/validation.md).

## Fresh native host evaluation

The actual Codex executable was the desktop-bundled CLI **0.162.0-alpha.2**, not
the older PATH CLI. Sessions were ephemeral and received only the task prompt
and an empty consumer with exact manifest/lock. No grading criteria, prior
conversation or intended answers were provided. User model settings were retained
without an override (`gpt-6.1-sol` / `xhigh` at check). Session-only overrides
disabled unrelated plugins, personal/system skills, MCP and memory; all five Inno
skills remained available. Persistent configuration was not edited for evaluation.

| Case | Observed selection and behavior | Independent result |
| --- | --- | --- |
| Korean HTTP protobuf endpoints | Implicitly read Core Network and Protobuf skills; generated macro POST/GET/DELETE, wire tests and no-content rejection | 6 tests PASS |
| English explicit directional codec | Read Protobuf skill; legacy request/standard response, bounded retry, once-per-invocation encoding, exact request/response quotas and media rejection | 5 tests PASS |
| English Core JSON endpoint | Read only Core Network skill; generated JSON `@APIDefinition`, no Protobuf skill read | 2 tests PASS |
| Korean patch policy | Read Protobuf skill, checked immutable upstream manifest, rejected Core-only 6.1.2 upgrade and explained future pair validation | PASS; no project changes/build |

The evaluator compiled the completed generation without manually editing Swift
code. All three generated consumers passed on the first independent run; no
separate evaluator repair sessions were needed. Their manifests/locks and source
hashes were preserved, and exact remote dependency graph/checkouts were checked.
Parameterized invocations are not counted as additional test declarations.
Prompts and acceptance criteria are in [the evaluation cases](../evals/innonetwork-protobuf.json).

Claude Code **2.1.285** used a fresh native installed session with hooks disabled
and an empty MCP configuration for that invocation. Startup registered all five
Inno skills, including `innosquad:innonetwork-protobuf`. The generation request
failed with **HTTP 401: OAuth access token is invalid**, with zero input/output
model tokens. Installation/registration is confirmed; actual Claude selection
and generation remain unverified. No credentials or login settings were changed.

## Final packaging and evidence reuse

Behavioral runs used **alpha.9**, source `00a70aa0b81b23ee40acf1031891318ad0d0f07e`.
The final **alpha.10** retains the shared validator's original 2025 copyright and
Router provenance alongside the Protobuf 2026 MIT notice. Only
`THIRD_PARTY_NOTICES.md` differs between evaluated and final skill trees;
instructions, metadata, references, validator code and consumer assets are
identical. The behavioral evidence is reused on that explicit basis, not
reported as a second set of alpha.10 AI runs.

Native Codex and Claude commands installed alpha.10. Final source↔central↔both
runtime caches match by every path, byte and mode: DI 14, Network 13, Flow 14,
Router 14 and Protobuf 13 files. Root/Codex/Claude identity and version metadata,
catalog, portable schema, skill structure and links passed. The existing optional
marketplace-description warning remains. Earlier plugin caches are retained.

These cases do not constitute a repeated bilingual matrix or a no-plugin efficacy
comparison. Earlier results for the four unchanged skills remain dated evidence,
not alpha.10 reruns. The work does not qualify later patches, all migrations,
macro-free consumers, alternate toolchains/platforms, live sockets/services,
device behavior or the complete library release/TSAN matrix. Remote CI, source
merge, tag/Release publication and public plugin distribution are separate.
No merge, tag/Release change or public marketplace publication was performed.
