# Consumer graph-output correction — alpha.14

The six consumer helpers now parse dependency-graph JSON from stdout and retain
SwiftPM warnings separately in a `*.stderr.log` file recorded by `stderr_log`.
The correction follows the already-merged Protobuf implementation. Malformed,
empty or noisy stdout and nonzero exits still fail validation. Swift test output
continues to combine stdout/stderr, preserving test-summary parsing. Flow keeps
its process-group timeout and reaping behavior.

Only `scripts/validate_consumer.py` changes inside each distributed skill. Skill
instructions, discovery metadata, API fixtures, support ranges and dependency
pins are unchanged. Source regression tests and maintainer documentation remain
in the owning repositories.

## Source pins

Five fixes are review-branch sources pending merge; Protobuf uses merged PR #9.
See `sources.lock.json` for immutable commit/tree identities and PR links.
`--require-merged` deliberately rejects this candidate while those five PRs are
open. A skill-source correction does not upgrade the validated library release.

| Skill | Source commit | Source state | PR |
| --- | --- | --- | --- |
| innodi | `e3af97115a67` | pull_request | [#59](https://github.com/InnoSquadCorp/InnoDI/pull/59) |
| innonetwork | `600467d957f4` | pull_request | [#153](https://github.com/InnoSquadCorp/InnoNetwork/pull/153) |
| innoflow | `4de23f95ef02` | pull_request | [#63](https://github.com/InnoSquadCorp/InnoFlow/pull/63) |
| innorouter | `4c2eafa4361b` | pull_request | [#70](https://github.com/InnoSquadCorp/InnoRouter/pull/70) |
| innonetwork-protobuf | `06e091d79f93` | merged | [#9](https://github.com/InnoSquadCorp/InnoNetwork-Protobuf/pull/9) |
| innonetwork-stream | `0fd0601be142` | pull_request | [#14](https://github.com/InnoSquadCorp/InnoNetwork-Stream/pull/14) |

## Fresh checks

- Central Python suite: 23 tests passed. Four new cross-skill regression tests
  execute 36 validator scenarios with real child-process output streams and
  simulated Swift/Git results; no compiler or network is used by these tests.
- All six pre-fix snapshots pass the clean JSON control and fail the stderr
  warning case. Updated snapshots pass both; malformed/empty/noisy stdout and
  nonzero-exit controls still reject the run before Swift tests.
- Five source suites pass their four output-regression tests. Existing Flow
  timeout/process cleanup tests (4) and Protobuf validation tests (11) pass.
- Real exact-dependency consumers passed **72 Swift tests**: DI 10, Network 13,
  Flow 11, Router 11, reissued Protobuf 14, planned Stream 13. All used strict
  concurrency and warnings as errors, with dependency provenance verified.
- Network root `swift test --jobs 2 --no-parallel` exited 0 (2,050 tests across
  eight passing summaries). Its docs/API contract checker passed.
- Native Claude manifest and marketplace validation passed.
- Bundle byte/path/mode equality passed against the pinned library skill trees.

Real Swift consumer results are recorded in
[consumer-output-validation-alpha.14.json](consumer-output-validation-alpha.14.json).
The initial DI run found a stale external cache whose referenced checkout files
were missing; a separate cache and a fresh scratch run passed. That initial
resolve failure is retained as environment evidence, not attributed to JSON
handling. Controlled stderr-warning coverage is in the subprocess regression
suite; successful live graph commands need not emit a warning.

## Reused evidence and remaining conditions

Previous alpha.12/alpha.13 host-selection and generated-code reports remain dated
evidence for unchanged instructions. No new AI model runs or global plugin-cache
updates are claimed. alpha.14 portable exports include the updated validators.

Merge the five owning-library PRs, record their merge commits and compare trees
before using `--require-merged` as a publication gate. Router's earlier merge
performance CI issue is separate; this fix does not address it. Stream's 6.1.1
baseline remains planned. Central merge, repository visibility, tags/releases and
official-directory submission are not performed by this correction.
