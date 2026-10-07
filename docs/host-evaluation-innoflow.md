# InnoFlow installation and AI evaluation — 2026-10-07

Local plugin **0.1.0-alpha.7** adds InnoFlow beside the unchanged DI and Network
snapshots. Codex and Claude Code were updated through their native plugin
commands. Codex passed four representative cases. Claude registered all three
skills, but its AI request stopped with OAuth 401 before model-token use.
[Machine-readable evidence](host-evaluation-innoflow.json).

## Source and support

The canonical source is [InnoFlow PR #57](https://github.com/InnoSquadCorp/InnoFlow/pull/57),
commit `9dee939ea4e4b0d84609351e046bfc70dfc9d95e`, 14-file skill tree
`51eab5f99de25af4574e6b9d54a01191da90b866`. The source remains under review.
The separate library baseline is exact tag **6.0.0** at
`188c2732d26350cf01afadade3dac89a2b73b68f`; no corresponding GitHub Release page
was found at the recorded check. The new skill source is not inside that existing tag.

Support covers stable `>=6.0.0, <6.1.0`. Later patches keep their resolved version
and receive actual source/manifest/consumer checks. Neither this range nor an
exact baseline test implies every patch was tested.

The source helper passed **11 tests** against remote InnoFlow 6.0.0 and
SwiftSyntax 604.0.0. It verifies manifest/lock, active graph/workspace, clean
checkout revisions, and any SwiftSyntax prebuilt. A wrong expected release SHA
was rejected before build in a disposable copy. The source's dated
[validation record](https://github.com/InnoSquadCorp/InnoFlow/blob/9dee939ea4e4b0d84609351e046bfc70dfc9d95e/skills/validation.md)
retains the initial fixture error and corrected passing run; framework code was unchanged.

## Fresh installed-host cases

Codex CLI 0.160.1 used the configured `gpt-6-astra` / `xhigh` settings. Each case
started with a separate temporary consumer, exact manifest/lock, empty source/test
placeholders, and installed alpha.7. Only the natural-language task was given;
no prior conversation, expected answer, or grading criteria was supplied.
Session overrides disabled unrelated configured skills/plugins, MCP and memory.
All three Inno skills remained available to evaluate routing. Persistent user
configuration and model choice were not changed.

| Case | Selection and behavior | Independent validation |
| --- | --- | --- |
| Korean async loading | Implicit Flow skill read; three-generic macro reducer, PhaseMap, dependency closure, exhaustive success/failure/retry | 3 tests PASS |
| English dispatch lifetime/output | Explicit Flow skill read; one cancelled dispatch preserves a sibling; synchronous output capture, manual clock | 4 tests PASS |
| English unrelated formatter | No Inno skill read; trims display name with Guest fallback | 3 new tests + 1 retained placeholder PASS |
| Korean future-patch policy | Implicit Flow skill read; separates 6.0.x support from 6.0.0 tests and does not claim 6.0.1 exists or passed | PASS; no edits, build, or external lookup |

The evaluator built/tested generated consumers without manual changes. Exact
remote pins, graph/workspace/checkouts, source hashes, and unchanged manifest/lock
were checked. All builds used Xcode 27 / Swift 6.4 with strict concurrency complete
and warnings as errors. There are **7 generated Flow behavior tests**, plus
**3 new unrelated formatter tests**; the original placeholder is not counted as
a generated test. Prompts and expected observations are in [evals/innoflow.json](../evals/innoflow.json).

Claude Code 2.1.285 installed alpha.7 and startup listed `innosquad:innodi`,
`innosquad:innonetwork`, and `innosquad:innoflow`. The fresh generation attempt
failed with **HTTP 401: OAuth access token is invalid**. No Claude behavioral
success is claimed; authentication must be restored before repeating the cases.

## Packaging and remaining boundaries

The Flow snapshot matches its source by every path, byte, and mode. Both installed
runtime caches match all three central snapshots (DI 14 / Network 13 / Flow 14
files). Root/Codex/Claude identity and catalog versions match alpha.7. Portable
schema, skill structure, local links, and Claude plugin validation passed;
marketplace validation retains the existing optional-description warning.

The two new Flow generation cases do not establish the full repeated bilingual
matrix, a no-plugin efficacy baseline, device lifecycle, migration execution,
optional-child ownership, scheduler/Inspector behavior, other toolchains, later
patches, or combined-library runtime integration. Existing DI/Network host results
remain dated historical evidence, not new alpha.7 runs. Library remote CI and
its CI-only release preflight are separate gates. No merge, tag/Release change,
public marketplace publication, or automatic snapshot collection was performed.
