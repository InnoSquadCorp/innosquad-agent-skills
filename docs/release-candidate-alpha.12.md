# alpha.12 validation — 2026-10-09

This candidate refreshes Flow/Protobuf released snapshots, qualifies Router 7.0.0
through source PR #69, uses the `innosquad` marketplace identity and licenses
original distribution material under MIT.

Fresh consumer tests: Flow 11, Router 11 and reissued Protobuf 14 passed with
complete strict concurrency and warnings as errors, with exact remote graph
verification. Router wrong-SHA and missing-version controls rejected before Swift.

See [consumer identities and results](consumer-release-validation-alpha.12.json).
Bundle validation and six controls passed. Claude catalog/manifest validation
passed without warnings. GitHub's bundle jobs passed on candidate commit
`626a3024fa6318e14e1ea437a55ed9208a94bbe8`.

## Installed-host evaluation

Native Codex and Claude installation succeeded under `innosquad@innosquad` from
that exact Git revision. Codex fetched the Git marketplace; Claude used a separate
GitHub clone as its local marketplace. All six installed skill trees matched the
central lock and owning source trees. The old `innosquad-local` identity was
disabled. Claude authentication worked throughout the fresh evaluation.

Claude Code 2.1.286 (`claude-opus-5-5`) selected the expected skill without explicit
skill invocation in each library case. An independent validator compiled the
final generated sources without editing them and verified unchanged manifest/lock,
source hashes and the actual remote dependency graph before and after testing.
All tests used complete strict concurrency and warnings as errors.

| Task | Selected skill | Independent tests |
| --- | --- | ---: |
| DI factory and fake override | innodi | 3 |
| Anonymous JSON GET/POST | innonetwork | 2 |
| PhaseMap loading/failure/retry | innoflow | 5 |
| Typed SwiftUI navigation and deep links | innorouter | 4 |
| Reissued Protobuf POST/GET/empty DELETE | innonetwork-protobuf | 6 |
| Unrelated string formatter | None; no Inno skill file read | 4 |

The 24 tests passed. Protobuf's first compile failed because generated tests nested
Swift Testing `#require` expressions. Claude corrected this in the same session
and reran successfully; no evaluator repair or follow-up prompt was supplied.
Some compound read/git commands and a supplemental Router build exceeded the
harness permissions. The independent validator completed the final graph and
strict build checks. These denials were not authentication failures.

Codex 0.162.0-alpha.2 independently selected the installed Router and Protobuf
skills for two read-only policy tasks. It distinguished support ranges from tested
versions, recognized Router's published 7.0.0 and Protobuf's revoked versus
reissued 6.1.1 identities, and kept the adapter's exact Core 6.1.1 constraint.
Both workspaces remained unchanged. External lookups were unavailable in those
isolated sessions; the answers explicitly reported that limitation and did not
claim fresh test execution. These were policy checks, not new generation runs.

The [sanitized prompts](../evals/release-candidate-alpha.12.json) and
[host evidence](host-evaluation-alpha.12.json) include exact pins, selected skills
and generated-source hashes. Raw traces remain outside the repository.

The earlier alpha.11 Stream run after Claude reauthentication is reused evidence:
implicit selection and generated consumer passed 5 independent strict tests,
including 13 parameterized invalid settings. It did not exercise live media.
Earlier Codex reports remain dated evidence for unchanged instructions.

One task per library is a smoke evaluation. Mock HTTP, host compilation and
deep-link parser/store tests do not validate live servers, HLS media, device URL
delivery or every patch in a supported line.

## Publication boundary

Router source [PR #69](https://github.com/InnoSquadCorp/InnoRouter/pull/69) remains
open at `aa6f9ddb41ffb290a506dc33068eb8afc3b63cdc`; some source CI jobs remain
queued or running. The central release gate `--require-merged` intentionally
rejects that source until its actual merge tree and CI are verified and the lock
is refreshed. The central repository is private and this candidate remains on
PR #1, outside `main`. Public publication and directory listing have not occurred.
