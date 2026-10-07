# 실제 설치·AI 평가 — 2026-10-05

This is the historical alpha.1/alpha.2 report. The current DI source and alpha.6 checks are recorded in [the 7.0.1 update](host-evaluation-innodi-7.0.1.md).

**Codex 대표 8개 사례 통과, 생성 코드 29개 테스트 통과. Claude Code는 설치·스킬 등록까지 확인했고 실제 AI 호출은 OAuth 401 오류로 중단됐다.** 두 도구의 코드 생성 평가가 모두 완료됐다는 의미는 아니다.

## 설치와 평가 환경

| 항목 | 확인 결과 |
|---|---|
| 설치 ID | 두 도구 모두 `innosquad@innosquad-local`, 사용자 범위 설치 |
| 당시 로컬 버전 | `0.1.0-alpha.2` |
| Codex | 앱 포함 CLI 0.160.0, 설정 모델 `gpt-6-astra`, reasoning `xhigh` |
| Claude Code | 2.1.285, 시작 이벤트의 모델 `claude-opus-5-5` |
| 모델에 제공한 자료 | 새 소비 프로젝트와 자연어 요청, 설치된 스킬. 이전 대화와 채점 기준은 제공하지 않음 |
| Codex 스킬 격리 | native `skills/list`에서 활성 스킬이 `innosquad:innodi` 하나임을 확인. 다른 스킬·플러그인·MCP·메모리는 실행 단위 override로 제외 |
| 코드 검증 | 별도 평가자가 Xcode 27 / Swift 6.4에서 strict concurrency 및 warnings-as-errors로 실행 |

소비 프로젝트와 평가 로그·채점 자료는 별도 디렉터리에 뒀다. 설치된 스킬 본문을 읽은 실제 명령, 생성 파일, diff, 전체 빌드 로그, dependency graph, 정확한 release checkout SHA를 보관했다. 생성 AI는 빌드하지 않도록 요청했고, 평가자가 독립 실행했다. 이는 AI가 스스로 보고한 성공과 실제 컴파일·실행을 구분하기 위한 조건이다.

## Codex 대표 사례

본 평가의 콘텐츠 기준은 `0.1.0-alpha.1`이다. 각 사례는 대화 이력이 없는 새 세션에서 1회 실행했다.

| 사례 | 언어·호출 | 실제 선택·결과 | 독립 검증 |
|---|---|---|---|
| 새 APIClient 주입·fake override | 한국어·자동 | 설치 캐시의 스킬과 참조를 읽고 remote exact dependency·DAG plugin·코드 생성 | 6개 테스트 통과 |
| 라이브러리 이름 없는 prewarm 요청 | 영어·자동 | 기존 import/lock을 확인하고 typed prewarm 사용 | 3개 테스트 통과 |
| optional nil와 기본 factory 복원 | 영어·자동 | `set(_:to:)`·`useDefault(_:)`, live 호출 횟수 확인 | 2개 테스트 통과 |
| 한 대기자의 취소와 공유 생성 | 한국어·자동 | 대기 취소와 provider 취소 구분, continuation으로 실행 순서 제어 | parameterized 테스트 1개, 3개 입력 통과 |
| 화면 컨트롤러 준비·실패·재시도·종료 | 한국어·명시 | `$innosquad:innodi` 호출, 실제 owner readiness/close 사용 | 11개 테스트 통과 |
| 대상의 DAG 검증 설정 점검 | 한국어·자동 | target에 plugin 추가, pin 유지, 행동 테스트 생성 | 6개 테스트 통과 |
| SwiftSyntax 버전 충돌 확인 | 한국어·자동 | 교집합 없음 판정, 임의 downgrade/override 없음 | manifest 비교 정확, 파일 변경 없음 |
| 관련 없는 SwiftUI 버튼 간격 | 영어·비선택 | InnoDI 스킬을 읽지 않음 | 요청한 한 줄만 변경, SwiftUI typecheck 통과 |

관련 있는 자동 요청 6개에서 설치된 스킬을 읽었고, 명시 호출 1개도 작동했다. 비관련 요청 1개에서는 선택하지 않았다. 6개 SwiftPM 소비 프로젝트의 **테스트 총 29개**가 통과했다. 각 프로젝트가 실제 remote InnoDI `7.0.0` / `4783eee7f674f99a337768c107b7a5f640810c2a` checkout을 사용했는지도 확인했다. 생성 코드를 평가자가 수동 수정해서 통과시킨 사례는 없다.

기계 판독 결과는 [host-evaluation-results.json](host-evaluation-results.json)에 있다. 1회씩 수행한 유한한 사례의 결과이며, 일반적인 성공률이나 스킬의 인과적 효과를 증명하지 않는다. 스킬 없는 대조 모델 실험은 수행하지 않았다.

## 평가 도중 구분한 문제

- 기존 CLI 0.142.5는 현재 설정 모델을 지원하지 않아 요청이 실패했다. 전역 실행기를 교체하지 않고 앱에 포함된 0.160.0으로 평가했다.
- CLI 설정 인자의 따옴표 처리와 초기 격리 설정을 바로잡았다. authoring checkout을 검색한 초기 진단 실행은 자동 선택 점수에서 제외했다.
- DAG plugin이 없는 최소 소비 프로젝트도 컴파일됐다. 따라서 “이 fixture가 빌드에 실패한다”는 전제가 틀렸다. 해당 모델 실행 전에 질문을 **필수 검증 설정 점검**으로 정정했다. 이것은 library 결함으로 분류하지 않았다.
- 참고 문서의 `InnoDI-Graph`는 실제 공개 실행 제품명이 아니었다. exact release README·manifest를 확인해 `InnoDI-DependencyGraph --diff before.json after.json --check-contract`로 정정하고 `0.1.0-alpha.2`로 양쪽 설치를 갱신했다. 스킬 본문과 기존 Swift 예제는 변경하지 않았다.

갱신 뒤 새 Codex 세션에서 설치된 alpha.2 참조를 읽고 올바른 실행 제품·diff 명령·종료 코드·스키마를 답하는 추가 점검도 통과했다. 최초 점검 질문은 모든 명령 실행을 금지해 로컬 파일 읽기까지 막았다. 모델은 그 제한을 준수했고, 해당 실행은 채점에서 제외했다. 읽기 전용 `cat`/`sed`를 허용하도록 질문을 명확히 한 새 세션으로 재검증했다.

## Claude Code의 현재 경계

설치 목록, plugin component inventory, 새 세션 시작 이벤트에서 `innosquad:innodi` 등록을 확인했다. 설치 파일도 원본과 일치한다. 그러나 첫 AI 요청이 **HTTP 401: OAuth access token is invalid**로 실패했다. 모델 입력·출력 토큰 사용량은 0이므로 자동 선택이나 코드 생성 성능으로 채점하지 않았다.

`claude auth login`으로 사용자 재로그인이 완료되면 준비된 별도 소비 프로젝트에서 같은 평가를 이어갈 수 있다. 인증값을 읽거나 보고서에 기록하지 않았다.

## 남은 범위

- Claude 실제 선택·코드 생성·소비 빌드 평가.
- 최초 계획의 전체 10종 × 양 언어 × 두 도구 반복 실행. 이번에는 8개 대표 사례를 혼합 언어로 한 번씩 실행했다.
- 6.x→7.0 migration 실행, SwiftUI host/device 동작, 여러 라이브러리의 실제 통합 resolve.
- 공개 배포·CI·라이선스 선택. 비공개 검토 저장소와 로컬 설치를 정식 배포와 구분한다.

## PR 준비 시 재확인

비공개 `InnoSquadCorp/innosquad-agent-skills`에서 이 파일럿을 검토한다. 스킬 형식, JSON/YAML, portable plugin schema, manifest identity/version, 로컬 문서 링크와 평가 합계를 새로 검사해 통과했다. Claude plugin manifest도 통과했으며 marketplace 검사에는 선택 사항인 description 누락 경고 1개가 남는다.

번들 예제 파일의 SHA-256은 [소비 테스트 증거](consumer-evidence.json)와 일치한다. 이 PR 준비 단계에서는 Swift 테스트와 AI 평가를 다시 실행하지 않았으며 위 날짜의 실행 증거를 재사용한다. 스킬 내용과 소비 예제는 평가 이후 그대로 유지했다.
