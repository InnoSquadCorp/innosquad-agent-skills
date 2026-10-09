# InnoSquad Agent Skills

InnoSquad Swift 라이브러리 6개의 스킬을 Codex와 Claude Code 플러그인으로 제공합니다.
**0.1.0-alpha.12**는 배포 준비 후보이며 공개 배포는 아직 하지 않았습니다.

| Skill | Stable support | Exact consumer baseline |
| --- | --- | --- |
| [innodi](skills/innodi/SKILL.md) | 7.0.x | 7.0.0; source snapshot from 7.0.1 |
| [innonetwork](skills/innonetwork/SKILL.md) | 6.1.x | 6.1.0; source snapshot from 6.1.1 |
| [innoflow](skills/innoflow/SKILL.md) | 6.0.x | 6.0.0; source snapshot from 6.0.2 |
| [innorouter](skills/innorouter/SKILL.md) | 7.0.x | Published 7.0.0 (`33b0da7`) |
| [innonetwork-protobuf](skills/innonetwork-protobuf/SKILL.md) | 6.1.x | Reissued 6.1.1 (`ba6ab8d`) + exact Core 6.1.1; historical fixture retained |
| [innonetwork-stream](skills/innonetwork-stream/SKILL.md) | Planned 6.1.x | Unreleased `bd50e87`, intended for 6.1.1 + exact Core 6.1.1 |

지원 범위는 해당 패치 라인 전체입니다. 6.1.x는 `>=6.1.0 <6.2.0`이며
프리릴리스와 6.2 이상을 포함하지 않습니다. 지원 범위가 모든 패치의 테스트
완료를 뜻하지는 않습니다. 프로젝트의 실제 해결 버전을 유지하고 검증합니다.

## Install

Both marketplaces are named **innosquad**. After this candidate merges into
`main`, developers with repository access can install with:

```bash
codex plugin marketplace add InnoSquadCorp/innosquad-agent-skills --ref main
codex plugin add innosquad@innosquad
claude plugin marketplace add InnoSquadCorp/innosquad-agent-skills
claude plugin install innosquad@innosquad --scope user
```

The repository is currently private and `main` does not yet contain this candidate.
Use the [review-branch instructions](docs/distribution.md) until merge. Git
marketplace distribution is separate from an official plugin-directory listing.
Start a fresh session after installation/update.

In Codex use `$innosquad:innorouter`; in Claude Code use `/innosquad:innorouter`.
Replace the skill name with any entry above. Relevant natural-language requests
can also select a skill automatically:

> 이 프로젝트의 InnoRouter 버전을 확인하고, 제품 상세 화면으로 이동하는 타입 안전한 라우트와 테스트를 작성해줘.

For standalone use, copy a complete `skills/<name>` into `.agents/skills/<name>`
or `.claude/skills/<name>`, preserving notices and resources and comparing an
existing destination before replacing it. Avoid duplicate standalone/plugin installs.

## Source ownership

**스킬 원본은 각 라이브러리 저장소에서 관리하며, 중앙 저장소는 검증한 원본을
플러그인으로 묶습니다.** API 지침이나 예제 수정은 라이브러리 PR에서 먼저 합니다.
중앙 저장소는 매니페스트, 배포, 설치 및 AI 호스트 평가를 담당합니다.

[sources.lock.json](sources.lock.json) separately pins skill source commits/trees
and tested library revisions. Runtime resources are self-contained; no
cross-repository symlinks, MCP servers, hooks, credentials or automatic project
migrations are included. Read [source ownership](docs/source-ownership.md).

Router's published-library baseline update is under [source PR #69](https://github.com/InnoSquadCorp/InnoRouter/pull/69).
The library is released, but that new skill source must merge before plugin
publication. Stream remains an explicitly planned library baseline.

## Validation

```bash
python3 -B scripts/validate_bundle.py
python3 -B -m unittest discover -s tests -v
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
```

The bundle check verifies identity/version agreement, support records, portable
links, source notices and exact Git tree equality including modes. CI runs those
checks and rejection controls; it does not call AI models or run Swift.

Fresh release checks passed 11 Flow, 11 Router and 14 reissued-Protobuf consumer
tests with strict concurrency and warnings as errors. See the
[alpha.12 evidence](docs/release-candidate-alpha.12.md) and
[consumer validation commands](docs/distribution.md#consumer-validation).
Earlier host reports remain dated evidence. Installation alone does not qualify
automatic selection or code generation; actual host results are recorded separately.

## License

Original distribution material is under [MIT](LICENSE). Each bundled skill retains
its library's `THIRD_PARTY_NOTICES.md`, including existing years and attributions.
Library release, source merge, plugin publication and directory approval are
independent states.
