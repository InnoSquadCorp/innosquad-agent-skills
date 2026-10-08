# InnoSquad Agent Skills — library-owned pilot

InnoDI **7.0.x**, InnoNetwork **6.1.x**, InnoFlow **6.0.x**, 예정된 InnoRouter **7.0.x**, InnoNetwork-Protobuf **6.1.x**, 예정된 InnoNetwork-Stream **6.1.x**를 사용하는 AI 개발 스킬의 로컬 파일럿입니다. Codex와 Claude Code가 각 라이브러리의 스킬 본문을 공유합니다. 플러그인 버전 `0.1.0-alpha.11`은 로컬 식별자입니다.

| Skill | Supported library | Validated baseline | Scope |
| --- | --- | --- | --- |
| [innodi](skills/innodi/SKILL.md) | InnoDI 7.0.x (stable) | 7.0.0 | Container, provider, override, readiness and lifecycle |
| [innonetwork](skills/innonetwork/SKILL.md) | InnoNetwork 6.1.x (stable) | 6.1.0 | JSON and encoded requests, auth, retry, limits and operations |
| [innoflow](skills/innoflow/SKILL.md) | InnoFlow 6.0.x (stable) | 6.0.0 tag | Reducers, effects, typed output, phases, dispatch lifetime and testing |
| [innorouter](skills/innorouter/SKILL.md) | InnoRouter 7.0.x (planned stable) | Unreleased main `851c63f`, intended for 7.0.0 | Routes, hosts, validated state, links, restoration and presentation lifetime |
| [innonetwork-protobuf](skills/innonetwork-protobuf/SKILL.md) | InnoNetwork-Protobuf 6.1.x (stable) | Adapter 6.1.1 tag + exact Core 6.1.1 | HTTP protobuf macros, directional codec/media, empty responses, limits and Core execution |
| [innonetwork-stream](skills/innonetwork-stream/SKILL.md) | InnoNetwork-Stream 6.1.x (planned stable) | Unreleased main `bd50e87`, intended for 6.1.1 + exact Core 6.1.1 | HLS parsing, VOD/offline, Live/DVR, native playback, audio and metadata |

The InnoDI skill covers version-aware setup, containers, providers, overrides, typed prewarm, async ownership, and 6→7 migration guidance. It includes an exact-release Swift consumer and a reproducible validation helper. Read [validation.md](docs/validation.md) for what has actually been tested.

## Source ownership and distribution

**스킬 원본은 각 라이브러리 저장소에서 관리하고, 이 저장소는 Codex·Claude Code용 플러그인으로 묶어 배포합니다.** 원본 경로는 `InnoSquadCorp/InnoDI`의 `skills/innodi/`, `InnoSquadCorp/InnoNetwork`의 `skills/innonetwork/`, `InnoSquadCorp/InnoFlow`의 `skills/innoflow/`, `InnoSquadCorp/InnoRouter`의 `skills/innorouter/`, `InnoSquadCorp/InnoNetwork-Protobuf`의 `skills/innonetwork-protobuf/`, `InnoSquadCorp/InnoNetwork-Stream`의 `skills/innonetwork-stream/`입니다. API 변경에 따른 지침·소비 예제 변경은 해당 라이브러리 PR에서 함께 검토합니다.

This repository owns plugin manifests, marketplace catalogs, and host installation/selection evaluations. Its `skills/` directory contains distribution snapshots; edit the library source, then refresh the snapshot. [sources.lock.json](sources.lock.json) records the source commit and Git tree separately from the validated library release or explicitly unreleased revision.

The lock records InnoNetwork, InnoFlow and Protobuf review-branch sources. Stream PR #9 merged during this work; its snapshot pins merge commit `81f945f`, with the identical evaluated skill tree. InnoRouter PR #66 is merged; its snapshot pins merge commit `3ed5ea0` with the same validated skill tree. The InnoDI snapshot comes from public release **7.0.1**, source commit `ce47cf4b207c3b8810b2a7d7d622a2f8ead3ed96`; its supported range is stable 7.0.x and its exact bundled fixture remains on 7.0.0. Snapshot collection was performed explicitly and checked for exact equality; automated collection/publication is follow-up work. Read the [ownership and update policy](docs/source-ownership.md) before changing a bundled skill.

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

Historical InnoDI evidence: both user-scope installations were performed on 2026-10-05. Codex CLI 0.160.0 passed eight representative selection/generation cases; the generated consumers passed 29 Swift tests. Claude Code 2.1.285 registered the skill, but AI execution was blocked by an invalid OAuth token. See the [actual host evaluation](docs/host-evaluation.md); installation alone is not behavioral qualification. A public plugin release is not included.

The [DI 7.0.1 snapshot update](docs/host-evaluation-innodi-7.0.1.md) records alpha.6 installation, current policy/generation checks, and separate 7.0.1 consumer evidence. The original 7.0.0 fixture pin and historical reports are preserved.

For the Network skill, invoke `$innosquad:innonetwork` in Codex or `/innosquad:innonetwork` in Claude Code. Its alpha.5 patch-support policy check and earlier alpha.3/alpha.4 generation results are recorded separately in [Network host evaluation](docs/host-evaluation-innonetwork.md); those results remain historical evidence for the unchanged snapshot in alpha.8.

For Flow, invoke `$innosquad:innoflow` in Codex or `/innosquad:innoflow` in Claude Code. Its [host evaluation](docs/host-evaluation-innoflow.md) records alpha.7 installation and representative selection/generation checks. The 6.0.0 tag was verified separately from a GitHub Release page, which was not found at the recorded check.

For Router, invoke `$innosquad:innorouter` in Codex or `/innosquad:innorouter` in Claude Code. The [Router host evaluation](docs/host-evaluation-innorouter.md) records alpha.8 installation and fresh evaluation results. Its 7.0.0 baseline is an unreleased main commit, not a published tag.

For Protobuf, invoke `$innosquad:innonetwork-protobuf` in Codex or `/innosquad:innonetwork-protobuf` in Claude Code. Its [host evaluation](docs/host-evaluation-innonetwork-protobuf.md) records alpha.9 representative cases and the alpha.10 attribution-only packaging update. The adapter 6.1.1 tag requires exact Core 6.1.1; the support line does not permit an arbitrary Core patch. The existing four runtime snapshots are unchanged.

For Stream, invoke `$innosquad:innonetwork-stream` in Codex or `/innosquad:innonetwork-stream` in Claude Code. Its [host evaluation](docs/host-evaluation-innonetwork-stream.md) records alpha.11 installation and fresh representative cases. Planned stable `>=6.1.0 <6.2.0` is separate from the exact unreleased `bd50e87` baseline; Core remains exact 6.1.1. All five earlier runtime snapshots and pins remain unchanged.

For standalone use, copy the complete `skills/<library>` directory to `.agents/skills/<library>` (Codex) or `.claude/skills/<library>` (Claude Code); preserve all supporting files and compare an existing destination before replacement. Standalone invocations are `$innodi`, `$innonetwork`, `$innoflow`, `$innorouter`, `$innonetwork-protobuf`, `$innonetwork-stream` or `/innodi`, `/innonetwork`, `/innoflow`, `/innorouter`, `/innonetwork-protobuf`, `/innonetwork-stream`.

## Validate the example

On macOS with Xcode 27 / Swift 6.4 and Python 3:

```bash
python3 skills/innodi/scripts/validate_consumer.py --scratch-path /tmp/innodi-skill-validation
python3 skills/innonetwork/scripts/validate_consumer.py --scratch-path /tmp/innonetwork-skill-validation
python3 skills/innoflow/scripts/validate_consumer.py --scratch-path /tmp/innoflow-skill-validation
python3 skills/innorouter/scripts/validate_consumer.py --scratch-path /tmp/innorouter-skill-validation
python3 skills/innonetwork-protobuf/scripts/validate_consumer.py --scratch-path /tmp/protobuf-skill-validation
python3 skills/innonetwork-stream/scripts/validate_consumer.py --scratch-path /tmp/stream-skill-validation
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
```

The helper copies the fixture outside the package, resolves remote exact pins, checks the active graph and Git checkouts, and runs Swift tests with strict concurrency and warnings as errors. It retains logs and `evidence.json` under the chosen scratch directory. It requires network access on a cold cache and does not install either AI plugin. The Python helper uses only the standard library.

InnoDI support covers stable `>=7.0.0, <7.1.0`. Its released skill source is 7.0.1; its exact fixture stays on 7.0.0. A separate copy of that fixture passed 10 tests against actual public 7.0.1. This is patch-specific evidence, not a claim that every 7.0.x patch or every consumer is tested.

InnoNetwork support covers stable `>=6.1.0, <6.2.0`. The exact fixture stays on 6.1.0; another patch such as 6.1.1 keeps its resolved version and receives patch-specific source checks and consumer tests. A planned release is not recorded as published or validated.

The InnoNetwork fixture passes 13 tests covering JSON macros, buffered encoding, retry byte reuse, auth preflight, codec failures, request/response budgets, no-content responses, operations and cancellation. It verifies the public 6.1.0 release and all six remote checkout pins, including SwiftSyntax 604. Its source-owned [validation record](https://github.com/InnoSquadCorp/InnoNetwork/blob/4dfd88c2d2c6dd771994cdecc20a3b7e9f4318ac/skills/validation.md) is separate from AI host evidence. No combined DI/Network or companion consumer is qualified.

InnoFlow support covers stable `>=6.0.0, <6.1.0`. Its exact tagged 6.0.0 consumer passed 11 tests covering macro authoring, binding, phase success/failure/retry, typed output, child composition, manual time, dispatch cancellation and FlowScope ownership. SwiftSyntax 604 and the exact remote graph were verified. The [source validation record](https://github.com/InnoSquadCorp/InnoFlow/blob/9dee939ea4e4b0d84609351e046bfc70dfc9d95e/skills/validation.md) remains separate from AI host results and CI-only release preflight.

InnoRouter planned support covers stable `>=7.0.0, <7.1.0`. The fixture pins main `851c63f095e49b700c3a0aa8152a3521a39977e7`, intended for 7.0.0, and passed 11 exact remote consumer tests. `version: null` means no released version was qualified. Verify the actual tag, differences and exact tagged consumer when 7.0.0 ships; later patches receive their own checks. See the [source validation record](https://github.com/InnoSquadCorp/InnoRouter/blob/3ed5ea0d6b07c1b282182c6e5468dd3ed962c402/skills/validation.md).

InnoNetwork-Protobuf supports stable `>=6.1.0 <6.2.0`. Its exact adapter/Core 6.1.1 consumer passed 14 strict Swift tests and verified eight remote pins. Only the 6.1.1 adapter tag exists in the observed 6.1.x line; no adapter GitHub Release page was found at check. Later patches require their own manifest/API and consumer checks. The source skill in [PR #7](https://github.com/InnoSquadCorp/InnoNetwork-Protobuf/pull/7) is not part of the existing 6.1.1 tag.

The original InnoDI bundled test target checks 10 cases covering construction, overrides, prewarm, readiness, retry, reader cancellation, close, preflight failure, and a SwiftUI compile boundary. The host evaluation's 29 generated tests are separate evidence. Migration execution, SwiftUI host/device behavior, and Claude AI behavior remain unverified. The [evaluation cases](evals/innodi.json) retain the broader planned scope.

## Packaging boundary

- Root `plugin.json` is the portable identity; `.codex-plugin/plugin.json` is the Codex compatibility overlay; `.claude-plugin/plugin.json` is the Claude manifest. Identity/version/description must stay in sync.
- All resources needed by each skill are contained in each `skills/<library>` directory; no internal InnoSquad configuration or personal checkout is required.
- No MCP server, hooks, credentials, or automatic project migration is included.
- The pilot has a private review repository at `InnoSquadCorp/innosquad-agent-skills`. The [InnoDI](skills/innodi/THIRD_PARTY_NOTICES.md), [InnoNetwork](skills/innonetwork/THIRD_PARTY_NOTICES.md), [InnoFlow](skills/innoflow/THIRD_PARTY_NOTICES.md), [InnoRouter](skills/innorouter/THIRD_PARTY_NOTICES.md), [Protobuf](skills/innonetwork-protobuf/THIRD_PARTY_NOTICES.md), and [Stream](skills/innonetwork-stream/THIRD_PARTY_NOTICES.md) snapshots retain their MIT notices. A license for this repository's other original distribution material, a public marketplace, and publication remain undecided.

Format references: [Codex skills](https://developers.openai.com/codex/skills), [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins), [Claude plugin reference](https://code.claude.com/docs/en/plugins-reference).
