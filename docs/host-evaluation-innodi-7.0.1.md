# InnoDI 7.0.1 source update — 2026-10-07

Local plugin **0.1.0-alpha.6** now bundles the canonical skill from public
[InnoDI 7.0.1](https://github.com/InnoSquadCorp/InnoDI/releases/tag/7.0.1).
Codex and Claude Code were updated through their native plugin commands.
Codex passed two fresh representative cases; Claude registered both skills but
its AI request again failed with OAuth 401. [Machine-readable evidence](host-evaluation-innodi-7.0.1.json).

## Source, support, and validation are separate

| Field | Value |
| --- | --- |
| Skill source | Released 7.0.1 commit `ce47cf4b207c3b8810b2a7d7d622a2f8ead3ed96` |
| Skill Git tree | `aa58cff138c95a3a5af4949a55a460ca253f0435`, 14 files |
| Supported releases | Stable `>=7.0.0, <7.1.0` |
| Canonical fixture / recorded baseline | 7.0.0, `4783eee7f674f99a337768c107b7a5f640810c2a` |
| Additional tested patch | Public 7.0.1, in an isolated consumer copy |

All DI paths, bytes, and modes match the release source. Both installed runtime
caches match the central DI snapshot. The unchanged 13-file Network snapshot
also matches its existing source pin and both caches. Root/Codex/Claude
identity and catalog metadata match alpha.6. Portable schema, skill structure,
relative links, and Claude plugin validation passed. Claude marketplace
validation passed with its existing optional-description warning.

## Consumer evidence reused from the immediately preceding review

Both runs below were performed on 2026-10-07 with Xcode 27 / Swift 6.4 on macOS
arm64, strict concurrency complete, and warnings as errors. The released skill
was not modified between those runs and this exact snapshot refresh.

- The released helper passed **10 tests** against exact remote InnoDI 7.0.0.
  Its evidence labels the scope `exact_baseline` separately from 7.0.x support.
- An isolated copy of the same fixture passed **10 tests** against exact remote
  InnoDI 7.0.1. Only its manifest and lock were retargeted; source and test bytes
  were unchanged. The actual clean remote InnoDI and SwiftSyntax 604.0.0 checkout
  revisions were verified. Canonical fixture pins and historical records remain intact.

These checks cover the skill fixture, not the complete library suite or all
patch-specific regressions. The original 2026-10-05 report remains historical.

## Fresh installed-host evaluation

Codex CLI 0.160.1 used the configured `gpt-6-astra` model with `xhigh` reasoning.
Each case started a new session with a disposable exact-7.0.1 consumer and the
installed alpha.6 plugin. No previous conversation, intended answers, or grader
criteria were supplied. Session overrides disabled unrelated configured skills,
plugins, MCP servers, and memory. No model or persistent user configuration changed.

| Case | Observation | Independent result |
| --- | --- | --- |
| Korean patch-support question | Automatically reads installed alpha.6 DI skill and support references; distinguishes 7.0.x support, 7.0.0 baseline, and actual 7.0.1; does not recommend downgrading or claim unperformed tests | PASS; no edits, build, or external lookup |
| Korean APIClient / fake override generation | Automatically reads installed alpha.6 DI skill; uses typed container/provider/override APIs and preserves exact 7.0.1 plus DAG plugin | PASS; **2 tests**, no manual changes after generation |

The generation case received exact public release notes and upstream manifest
as local source material. The model was asked not to build; the evaluator ran
the resulting code independently with strict concurrency and warnings as errors.
The actual remote graph, clean checkout SHAs, unchanged manifest/lock, and
source hashes were checked. Prompts are retained in [the evaluation cases](../evals/innodi.json).

Claude Code 2.1.285 updated to alpha.6 and its startup registered
`innosquad:innodi` and `innosquad:innonetwork`. A fresh policy request stopped
before model-token use with **HTTP 401: OAuth access token is invalid**. This is
installation/registration evidence only; Claude selection and generation remain
unqualified until authentication is restored and the cases are rerun.

## Boundaries

This is a local plugin update and Draft PR change, not public plugin publication.
The two Korean cases do not replace a full repeated bilingual matrix, migration
execution, SwiftUI device lifecycle, or combined-library consumer validation.
Prior Network and DI host results are reused as dated history, not reported as
new alpha.6 runs. Raw local evaluation traces are kept outside the plugin repository.
