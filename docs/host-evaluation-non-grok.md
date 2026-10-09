# Non-Grok host evaluation — 2026-10-10

Evaluated distribution: **0.1.0-alpha.14**, commit
`2a5b4fed66ba4750c89df09f9fd8e0d8878f31cf`. The 1.0.0 preparation keeps these exact
six skill trees. These are reused behavioral results for that unchanged content,
not new 1.0.0 model runs. See [machine-readable evidence](host-evaluation-non-grok.json).

Five hosts received all six skill directories. **30/30** copies matched the
original file inventory, bytes and executable modes. Seven portable-packaging
tests passed. Installation was confined to isolated projects.

| Host | Observation | Qualification |
| --- | --- | --- |
| Codex desktop CLI 0.162.0-alpha.17.2 | Implicit DI request read SKILL.md, manifest/lock, implementation reference and example/test files | Generated DI 2 tests and unrelated Swift Testing 2 tests passed |
| Claude Code 2.1.286 | alpha.14 inline plugin registered six namespaced skills | OAuth session expired before model output; no new generation result |
| Gemini CLI 0.24.0 | All six Enabled after project `experimental.skills=true` | Request stopped at OAuth sign-in; no model output |
| Cursor Agent 2026.01.02-80e4d9b | Project files and installed `.cursor/skills` loader verified | Actual request required authentication; runtime discovery and generation unverified |
| Copilot CLI 1.0.11, GPT-4.1 | All six listed; explicit `skill innodi` loaded instructions/references | Implicit selection failed; both DI generated answers failed compilation |

## Behavioral method and controls

The positive task named the **library**, not the skill: implement synchronous
APIClient injection, fake override and a test proving the live factory is bypassed.
The scaffold used exact InnoDI **7.0.0**, revision
`4783eee7f674f99a337768c107b7a5f640810c2a`, and SwiftSyntax **604.0.0**, revision
`050f1a346fbbac0ca2cfb15a95274f7bd1cf0ccf`. Manifests and lockfiles stayed unchanged.
The independent validator checked actual dependency graph paths and checkout SHAs;
checkouts were clean. Generated source was saved without manual repair.

Hosts could read local references but not edit files, build, call network tools or
delegate. Codex used read-only shell commands for file access. SwiftPM compilation
and tests ran afterward under the fixture's Swift 6 manifest. The resulting
`swift test --jobs 2 --no-parallel --force-resolved-versions` check was not a full
autonomous build-and-repair loop. The older alpha.12 strict-warning evaluations
are recorded separately; their compiler flags are not attributed to this run.

Codex selected DI, used macro-generated wiring and passed normal-construction and
override/factory-bypass tests. It read no Inno files for the unrelated slug task,
whose two Swift Testing cases passed. The probe used project alpha.14 skills while
unrelated/global plugins were excluded per invocation. It did not replace the
installed alpha.12 native plugin cache.

Copilot GPT-4.1 made no tool call in the implicit positive task, generated
`Container` and a nongeneric `Provider`, and failed compilation. It also selected
XCTest despite the Swift Testing request. The explicit control successfully loaded
`innodi` and its implementation/example/test references but put a `@DIContainer`
inside a test function, which the macro rejected. Its unrelated task read no Inno
skill, passed two XCTest cases, and again missed the requested testing framework.
This distinguishes loading support from model selection/code accuracy.

Copilot's listed Haiku 4.5 was rejected by the API as unsupported; a GPT-5.2 request
was unavailable. The earlier default GPT-5 mini probe was also rejected. These are
model-availability results, not skill failures. No global model selection changed.
Two unrelated user-global skills exceeded Copilot's description length limit;
all six Inno entries were enabled.

## Environment boundaries

- Gemini 0.24.0's installed settings schema defaults `experimental.skills` to false;
  its command registration checks that flag. The project-only setting enabled
  discovery. The installer must not overwrite user settings to do so.
- Claude's successful auth-status report did not establish a working API session.
  Its actual request failed authentication with no token usage. Both standalone
  project entries and inline-plugin entries were present for its catalog probe;
  no generation claim is made for that duplicate environment.
- Cursor's actual request failed authentication despite its status command's login
  indication. Static loader compatibility is the limit of this evidence.
- Initial Codex/Claude harness configuration mistakes were corrected before the
  reported probes. A stale Swift scratch directory referenced a missing checkout;
  the reported builds used a valid cache and independently verified graph/pins.
- Raw prompts, responses and build logs remain outside the repository. This summary
  includes hashes and bounded diagnostics, without credentials or OAuth URLs.

This is a representative DI smoke evaluation, not every host × library × patch
combination. Web attachment acceptance, live services, devices and fresh behavior
of the authentication-blocked hosts remain unverified. Older successful Claude
runs remain useful dated evidence for unchanged guidance; see
[alpha.12](release-candidate-alpha.12.md).
