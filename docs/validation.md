# InnoDI pilot validation — 2026-10-05

This records the initial creation pass. The later user-requested installation and AI evaluation are recorded in [host-evaluation.md](host-evaluation.md): both tools installed, Codex representative cases passed, Claude AI execution blocked by OAuth 401. Historical “not performed” statements below describe the initial pass.

Local skill creation is complete for this first slice. This is not a public release or a claim of completed Codex/Claude behavioral qualification.

## Baseline and fresh evidence

The consumer resolved public InnoDI **7.0.0**, revision `4783eee7f674f99a337768c107b7a5f640810c2a`, and SwiftSyntax **604.0.0**, revision `050f1a346fbbac0ca2cfb15a95274f7bd1cf0ccf`. The active SwiftPM graph used remote checkout directories at those revisions; both checkouts were clean. No path dependency was substituted.

Environment: macOS 27 arm64, Xcode 27.0 (27A266a), Apple Swift 6.4 (`swiftlang-6.4.0.34.1`). The last positive helper run completed at **2026-10-05 11:15:17 UTC**. Its [persisted evidence](consumer-evidence.json) records source hashes, toolchain, dependency revisions, and results. Source hashes let a later edit be distinguished from this validated example.

| Check | Result |
|---|---|
| Skill creator `quick_validate.py` | PASS |
| `agents/openai.yaml` structure and automatic invocation setting | PASS, metadata only |
| Portable `plugin.json` against published 1.0.0 JSON schema | PASS |
| Root / Codex / Claude identity, version, description, author consistency | PASS |
| Claude Code 2.1.285 `claude plugin validate .` | PASS without warnings |
| Codex compatibility manifest's skill path | Resolves to the shared `skills/` directory; runtime load untested |
| Consumer helper, isolated copied fixture, exact remote graph and SHA checks | PASS |
| Swift test with strict concurrency and warnings as errors | PASS, 10 tests in 1 suite |
| Wrong expected InnoDI revision in a disposable skill copy | Correctly rejected before tests; failed evidence recorded |

The first compile exposed a test-fixture type-inference issue: a throwing read embedded only in `#expect` did not infer the closure's throwing effect. Assigning the result with `try await` before the expectation corrected the fixture. No library source was changed. The full corrected suite then passed directly and again through the reusable validation script.

## Consumer behavior covered

1. Typed constructor wiring and fake value override.
2. Empty/selective prewarm and shared cache across container copies.
3. Explicit optional nil bypassing live construction, followed by `useDefault` restoring it.
4. Owned readiness, idempotent close, and rejected async reads after close.
5. Preparation failure and one explicit successful retry.
6. A cancelled reader leaving shared construction available to another reader.
7. `withPrepared` closing before an escaped view is used.
8. Owned value override avoiding the live async factory.
9. Throwing override preflight preventing live work.
10. SwiftUI explicit imports and injected value boundary compiling.

These tests use deterministic factory counters and actor continuations, with a suite time limit; they do not call an external service.

## Remaining host and release work

- Actual installation, automatic/explicit skill selection, supporting-file loading, and generated-code behavior in fresh Codex and Claude Code sessions. The [10 bilingual cases](../evals/innodi.json) are prepared, not run.
- Actual 6→7 migration execution, SwiftUI host/environment behavior on Simulator/device, advanced hierarchy/assisted/multibinding scenarios, and other toolchains/platforms.
- Combined Inno library dependency graphs; the documented SwiftSyntax conflicts are fixed-manifest comparisons.
- Marketplace/catalog, install/update/remove trials, CI, public license choice, Git repository/remote creation, and publication.

The existing InnoDI source checkout and internal skill configuration were not modified. The broader plan was updated separately to make DI the first pilot. No global skill/plugin installation, commit, or push was performed.
