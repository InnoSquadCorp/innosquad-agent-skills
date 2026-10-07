# InnoSquad Agent Skills — library-owned pilot

InnoDI **7.0.0**과 InnoNetwork **6.1.x**(검증 기준 **6.1.0**)를 사용하는 AI 개발 스킬의 로컬 파일럿입니다. Codex와 Claude Code가 각 라이브러리의 스킬 본문을 공유합니다. 플러그인 버전 `0.1.0-alpha.5`는 로컬 식별자입니다.

| Skill | Supported library | Validated baseline | Scope |
| --- | --- | --- | --- |
| [innodi](skills/innodi/SKILL.md) | InnoDI 7.0.0 | 7.0.0 | Container, provider, override, readiness and lifecycle |
| [innonetwork](skills/innonetwork/SKILL.md) | InnoNetwork 6.1.x (stable) | 6.1.0 | JSON and encoded requests, auth, retry, limits and operations |

The InnoDI skill covers version-aware setup, containers, providers, overrides, typed prewarm, async ownership, and 6→7 migration guidance. It includes an exact-release Swift consumer and a reproducible validation helper. Read [validation.md](docs/validation.md) for what has actually been tested.

## Source ownership and distribution

**스킬 원본은 각 라이브러리 저장소에서 관리하고, 이 저장소는 Codex·Claude Code용 플러그인으로 묶어 배포합니다.** 원본 경로는 `InnoSquadCorp/InnoDI`의 `skills/innodi/`와 `InnoSquadCorp/InnoNetwork`의 `skills/innonetwork/`입니다. API 변경에 따른 지침·소비 예제 변경은 해당 라이브러리 PR에서 함께 검토합니다.

This repository owns plugin manifests, marketplace catalogs, and host installation/selection evaluations. Its `skills/` directory contains distribution snapshots; edit the library source, then refresh the snapshot. [sources.lock.json](sources.lock.json) records the source commit and Git tree separately from the supported library release.

The InnoNetwork source is under PR review. InnoDI PR #54 has merged; this Network addition retains the previously validated DI snapshot, whose pin predates that merge. Snapshot collection was performed explicitly and checked for exact equality; automated collection/publication is follow-up work. Read the [ownership and update policy](docs/source-ownership.md) before changing a bundled skill.

## Install and use locally

From this package root, install from the included local marketplace:

```bash
codex plugin marketplace add .
codex plugin add innosquad@innosquad-local
claude plugin marketplace add .
claude plugin install innosquad@innosquad-local --scope user
```

**Codex:** Start a new session and invoke the installed plugin skill as `$innosquad:innodi`, for example:

> $innosquad:innodi 이 프로젝트의 실제 InnoDI 버전을 확인하고, APIClient 주입과 테스트용 override를 구성해줘.

> Use $innosquad:innodi to add an owned async container with explicit readiness and shutdown to this project.

**Claude Code:** Start a new session and invoke `/innosquad:innodi` with the same task. For a development session without persistent installation, `claude --plugin-dir .` is also available.

Historical InnoDI evidence: both user-scope installations were performed on 2026-10-05. Codex CLI 0.160.0 passed eight representative selection/generation cases; the generated consumers passed 29 Swift tests. Claude Code 2.1.285 registered the skill, but AI execution was blocked by an invalid OAuth token. See the [actual host evaluation](docs/host-evaluation.md); installation alone is not behavioral qualification. A public release is not included.

For the newly added Network skill, invoke `$innosquad:innonetwork` in Codex or `/innosquad:innonetwork` in Claude Code. Its alpha.5 patch-support policy check and earlier alpha.3/alpha.4 generation results are recorded separately in [Network host evaluation](docs/host-evaluation-innonetwork.md); the earlier InnoDI results were not rerun.

For standalone use, copy the complete `skills/<library>` directory to `.agents/skills/<library>` (Codex) or `.claude/skills/<library>` (Claude Code); preserve all supporting files and compare an existing destination before replacement. Standalone invocations are `$innodi` / `$innonetwork` or `/innodi` / `/innonetwork`.

## Validate the example

On macOS with Xcode 27 / Swift 6.4 and Python 3:

```bash
python3 skills/innodi/scripts/validate_consumer.py --scratch-path /tmp/innodi-skill-validation
python3 skills/innonetwork/scripts/validate_consumer.py --scratch-path /tmp/innonetwork-skill-validation
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
```

The helper copies the fixture outside the package, resolves remote exact pins, checks the active graph and Git checkouts, and runs Swift tests with strict concurrency and warnings as errors. It retains logs and `evidence.json` under the chosen scratch directory. It requires network access on a cold cache and does not install either AI plugin. The Python helper uses only the standard library.

InnoNetwork support covers stable `>=6.1.0, <6.2.0`. The exact fixture stays on 6.1.0; another patch such as 6.1.1 keeps its resolved version and receives patch-specific source checks and consumer tests. A planned release is not recorded as published or validated.

The InnoNetwork fixture passes 13 tests covering JSON macros, buffered encoding, retry byte reuse, auth preflight, codec failures, request/response budgets, no-content responses, operations and cancellation. It verifies the public 6.1.0 release and all six remote checkout pins, including SwiftSyntax 604. Its source-owned [validation record](https://github.com/InnoSquadCorp/InnoNetwork/blob/4dfd88c2d2c6dd771994cdecc20a3b7e9f4318ac/skills/validation.md) is separate from AI host evidence. No combined DI/Network or companion consumer is qualified.

The original InnoDI bundled test target checks 10 cases covering construction, overrides, prewarm, readiness, retry, reader cancellation, close, preflight failure, and a SwiftUI compile boundary. The host evaluation's 29 generated tests are separate evidence. Migration execution, SwiftUI host/device behavior, and Claude AI behavior remain unverified. The [evaluation cases](evals/innodi.json) retain the broader planned scope.

## Packaging boundary

- Root `plugin.json` is the portable identity; `.codex-plugin/plugin.json` is the Codex compatibility overlay; `.claude-plugin/plugin.json` is the Claude manifest. Identity/version/description must stay in sync.
- All resources needed by each skill are contained in each `skills/<library>` directory; no internal InnoSquad configuration or personal checkout is required.
- No MCP server, hooks, credentials, or automatic project migration is included.
- The pilot has a private review repository at `InnoSquadCorp/innosquad-agent-skills`. The [InnoDI](skills/innodi/THIRD_PARTY_NOTICES.md) and [InnoNetwork](skills/innonetwork/THIRD_PARTY_NOTICES.md) snapshots retain their MIT notices. A license for this repository's other original distribution material, a public marketplace, and publication remain undecided.

Format references: [Codex skills](https://developers.openai.com/codex/skills), [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins), [Claude plugin reference](https://code.claude.com/docs/en/plugins-reference).
