# InnoSquad Agent Skills

InnoSquad Swift 라이브러리 6개의 스킬을 Codex·Claude Code 플러그인과
다른 AI 도구용 공통 스킬로 제공합니다. **1.0.0 배포 준비 버전**이며,
아직 1.0.0 태그·GitHub Release·공개 배포는 만들지 않았습니다.

| Skill | Support | Exact consumer baseline |
| --- | --- | --- |
| [innodi](skills/innodi/SKILL.md) | 7.0.x | 7.0.0 |
| [innonetwork](skills/innonetwork/SKILL.md) | 6.1.x | 6.1.0 |
| [innoflow](skills/innoflow/SKILL.md) | 6.0.x | 6.0.0 |
| [innorouter](skills/innorouter/SKILL.md) | 7.0.x | Published 7.0.0 (`33b0da7`) |
| [innonetwork-protobuf](skills/innonetwork-protobuf/SKILL.md) | 6.1.x | Reissued 6.1.1 (`ba6ab8d`) + exact Core 6.1.1; historical fixture retained |
| [innonetwork-stream](skills/innonetwork-stream/SKILL.md) | **Preview: planned 6.1.x** | Unreleased `bd50e87`, intended for 6.1.1 + exact Core 6.1.1 |

지원 범위는 해당 패치 라인 전체입니다. 예를 들어 6.1.x는 `>=6.1.0 <6.2.0`이며
프리릴리스와 6.2 이상은 포함하지 않습니다. 모든 패치를 테스트했다는 뜻은 아닙니다.
프로젝트의 실제 해결 버전을 유지하고 해당 소비자를 검증합니다. Stream은 정식
6.1.1 검증 완료 항목이 아닌 preview로 포함됩니다.

## AI 도구별 검증 수준

| 도구 | 제공 방식 | 확인된 수준 |
| --- | --- | --- |
| Codex | 네이티브 플러그인 / `.agents/skills` | 기존 플러그인 평가 + 최근 대표 DI 자동 선택·생성 테스트 통과 |
| Claude Code | 네이티브 플러그인 / `.claude/skills` | 기존 생성 평가 통과. 최근 alpha.14 인식 확인, OAuth 만료로 새 생성 평가 중단 |
| Gemini CLI | `.gemini/skills` | 0.24.0은 `experimental.skills=true` 필요. 6개 인식 확인, 생성 미검증 |
| Cursor Agent | `.cursor/skills` | 설치·로더 확인. 인증 문제로 실제 선택·생성 미검증 |
| GitHub Copilot | `.github/skills` | 6개 인식·명시 로딩 확인. **GPT-4.1 자동 선택·생성 평가 미통과** |
| Grok CLI / 웹·앱 / API | 네이티브 폴더 / Markdown / API 도구 | 형식·로컬 검사만 완료, 실제 모델 동작 미검증 |
| ChatGPT·Gemini 웹 등 | Markdown 첨부·붙여넣기 | 참고 자료 전달. 웹용 네이티브 플러그인 제공을 의미하지 않음 |

스킬 인식, 자동 선택, 생성 코드 컴파일, 공개 배포는 별도로 검증합니다.
[호스트별 설정·제한](docs/host-support.md)과 [최근 평가](docs/host-evaluation-non-grok.md)에
버전, 대조군, 인증·모델 제한을 기록했습니다. 1.0.0 후보의 스킬 원본은 평가한
alpha.14와 동일하며, 이전 검증을 새 실행 결과로 표시하지 않습니다.

## Install

저장소는 현재 private이며 후보는 PR #1에 있습니다. 먼저
[검토 브랜치 설치](docs/distribution.md#review-the-candidate)를 사용하세요.
마켓플레이스는 두 도구 모두 `innosquad`, 플러그인 ID는 `innosquad@innosquad`입니다.
정식 태그 설치는 **v1.0.0 게시 후** [배포 안내](docs/distribution.md)를 따릅니다.

설치 후 새 세션에서 Codex는 `$innosquad:innorouter`, Claude Code는
`/innosquad:innorouter`로 명시 호출할 수 있습니다. 관련 자연어 요청에 따른
자동 선택은 호스트와 모델의 영향을 받습니다.

```bash
python3 scripts/portable_skills.py install --host gemini --project /path/to/app
python3 scripts/portable_skills.py install --host copilot --project /path/to/app
python3 scripts/portable_skills.py export --output artifacts/portable-1.0.0-candidate
```

`--host`는 `codex`, `claude`, `gemini`, `cursor`, `copilot`, `grok`, `agents`를
지원합니다. 기존 파일이 다르면 덮어쓰지 않습니다. 설정·인증은 변경하지 않으며,
Gemini와 Copilot의 설치 결과에 필요한 설정과 검증 한계를 안내합니다.
네이티브 플러그인과 같은 스킬의 독립 설치를 중복으로 활성화하지 마세요.

내보낸 ZIP은 네이티브 스킬 폴더이고, 라이브러리별 Markdown은 채팅용 참고 자료입니다.
Grok API 도구는 `scripts/grok_request.py`; `--dry-run`으로 요청을 먼저 확인합니다.
자세한 사용법은 [호스트 안내](docs/host-support.md)를 참조하세요.

## Source ownership

**스킬 원본은 각 라이브러리 저장소가 관리하고, 중앙 저장소는 검증한 원본을 묶습니다.**
[sources.lock.json](sources.lock.json)은 원본 커밋·트리와 라이브러리 검증 기준을
따로 고정합니다. API 지침·예제 수정은 원본 PR에서 먼저 합니다.
[원본 관리 정책](docs/source-ownership.md)을 참조하세요.

검증 스크립트의 stdout/stderr 혼합 오류는 6개 스냅샷 모두 수정되어 있습니다.
[alpha.14 수정 보고서](docs/consumer-output-fix-alpha.14.md)의 원본 PR 5개는
아직 병합 대기 중이며 Protobuf 수정은 병합됐습니다. **정식 패키지 생성은
미병합 원본이 있으면 실패합니다.**

## Validate and prepare 1.0.0

```bash
python3 -B scripts/validate_bundle.py
python3 -B -m unittest discover -s tests -v
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
python3 -B scripts/build_release.py --candidate --output artifacts/1.0.0-candidate
```

후보 패키지는 플러그인 ZIP, 채팅 참고 자료, 출처 정보, SHA-256 목록을 포함합니다.
이 명령은 배포하지 않습니다. 병합·CI·공개 설정 등 남은 조건과 정식 패키지 생성
절차는 [1.0.0 준비 문서](docs/release-1.0.0.md)에 정리했습니다.
변경 내역은 [CHANGELOG](CHANGELOG.md)를 참조하세요.

## License

중앙 배포물은 [MIT](LICENSE)입니다. 각 스킬의 `THIRD_PARTY_NOTICES.md`와
기존 저작권 표기를 보존합니다. Git 마켓플레이스 배포와 공식 디렉터리 등록은
서로 별도입니다.
