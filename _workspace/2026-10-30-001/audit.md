# 틈 공개 문서 정합성 검토 — 2026-10-30

공개 문서 6개, SVG 9개, 샘플 이미지 3개를 비공개 구현·실험 기록과 대조했습니다. 큰 성과 수치를 잘못 옮긴 사례는 찾지 못했지만, 공개 문서의 검증 시점과 현재 기능 설명이 뒤처져 있었습니다. 공개 문서 6개와 ERD의 설명·메타데이터 1개를 로컬에서 수정했습니다.

공개 문서의 SDK 수치는 원본 15회와 일치했습니다. AI의 과거 평가, 현재 서비스 실행 경로, 서비스에 연결하지 않은 실험 후보는 서로 다른 근거이므로 그 경계를 명시했습니다. 이 검토는 현재 배포의 품질을 새로 인증한 작업이 아닙니다.

## 대조 범위와 기준

- 공개 기준: `DOMADO-PROJECT/teum`, 작업 전 `main` = `d30b563d562c978e3eccc3d29d61b1f8230ad09e`.
- 비공개 기준: `DO-MADO/teum`, 로컬 HEAD = `d9f6b76f2ca16c90bde842330ee8797cb4407aed`, 조회한 원격 `main` = `e70596a27a61bf70ed335cef43d8e53def3ce2aa`. 커밋은 다르지만 파일 트리는 같고, 비공개 작업 트리는 변경하지 않았습니다.
- 로컬 GitHub 문서 폴더의 관련 연구·모델 기록도 검색했으며, 틈에 대한 근거는 비공개 틈 저장소의 문서·verification JSON·원본 실행 파일에서 확인했습니다. 다른 프로젝트의 성과를 틈의 성과로 가져오지 않았습니다.
- DB는 연결된 틈 Supabase 프로젝트의 카탈로그만 SELECT로 조회했습니다. 테이블·컬럼·제약조건만 대조했고 사용자 데이터 조회나 변경, 마이그레이션 실행은 하지 않았습니다.
- `domado-world`는 이번 조사의 계기이며, 해당 저장소 자체는 이번 수정 범위에 포함하지 않았습니다.

## 발견한 차이와 반영 내용

| 항목 | 기존 공개 설명의 문제 | 대조 결과와 수정 |
|---|---|---|
| 검증 시점 | 기본 검증 기록이 10-13에서 멈춰 후속 검증이 빠짐 | 10-19~21 자체 분석·AI 기록을 추가하고, 문서 대조일과 실제 실행일을 구분 |
| 전환 모델 평가 | Sol 후속 평가가 아직 남은 것으로 읽힘 | 10-16 합성 25사례, 10-21 위험·대조 4쌍의 기록을 반영 |
| 현재 AI 경로 | 과거 계획→조사→반증 흐름과 현재 실행본의 차이가 드러나지 않음 | 현재 코드의 조사 대화와 후보가 있을 때의 독립 반증 대화를 설명; 과거 품질 판정의 승계 금지 |
| AI 통합 성공 범위 | AI 완료와 전체 점검 완료·모든 다운로드 검증을 혼동할 여지 | 수정 전·후 후보 1/0, AI 완료·전체 partial, 수정본 JSON·인증 HTML 미검증을 명시 |
| 자체 코드 분석 | 구현된 후속 분석과 한도 설명이 부족 | 제한된 TS SQL·셸·객체 소유권·서버 데이터 전달 분석과 64파일/1 MiB/256 KiB 한도를 추가 |
| 캐시 | 이전 결과 재사용이 분석 생략 전체로 읽힐 수 있음 | 권한·입력 준비 유지, OSV 새 조회, AI 문맥의 비밀정보 재검사를 설명 |
| DB 도식 | public 테이블 전체가 15개인 것으로 읽힘 | 실제 16개 중 15개를 표시, 과거 website_targets 생략을 명시; 관계선은 맞아 유지 |
| 작업 공간 역할 | workspace_members만 보면 팀·다중 역할 기능으로 오해할 여지 | 현재 owner만 지원하며 팀 초대·다중 권한 기능이 아님을 명시 |
| SDK 실험 범위 | r14/r15의 ‘최종’이 이후 모든 실험까지 뜻하는 것으로 읽힘 | r1~r15 구간의 마지막임을 명시; r16/r17 미채택·r18 미완료는 합계 밖의 후속 기록으로 추가 |
| 문장·문단 줄바꿈 | 종결 뒤 누락과 여러 문장 한 줄 배치 | 누락이 있는 줄 121개 → 0개; 문장 <br>, 큰 문단 <br><br>로 정리 |

기존 숫자를 수정해야 할 근거는 발견하지 못했습니다. 아래에서 ‘일치’는 지정한 소스·기록과 문서가 일치한다는 뜻이며, 모든 고객 저장소에서 같은 결과가 나온다는 뜻은 아닙니다.

## 주요 주장과 근거

| 공개 내용 | 대조 근거 | 판정 |
|---|---|---|
| GitHub 중심 입력·초기 이용 제한 | [docs/SCOPE.md](/Users/domado/Documents/GitHub/teum/docs/SCOPE.md), [docs/DB_SCHEMA.md](/Users/domado/Documents/GitHub/teum/docs/DB_SCHEMA.md) | 일치; 직접 점검 이용 조건을 보충 |
| 공개 샘플·R-042/R-047·브라우저 내 검토 상태 | [apps/web/features/demo/fixtures.ts](/Users/domado/Documents/GitHub/teum/apps/web/features/demo/fixtures.ts), [apps/web/features/demo/state.ts](/Users/domado/Documents/GitHub/teum/apps/web/features/demo/state.ts), [apps/web/features/demo/session.ts](/Users/domado/Documents/GitHub/teum/apps/web/features/demo/session.ts) | 일치; 실제 분석과 구별 유지 |
| 수집과 분석 Workflow 분리 | [apps/web/workflows/scan.ts](/Users/domado/Documents/GitHub/teum/apps/web/workflows/scan.ts), [apps/web/workflows/runtime.ts](/Users/domado/Documents/GitHub/teum/apps/web/workflows/runtime.ts) | 일치 |
| 규칙·의존성 → OSV → 자체 분석 → 저장 → Sandbox 정지 → AI → 정리 | [apps/web/workflows/runtime.ts](/Users/domado/Documents/GitHub/teum/apps/web/workflows/runtime.ts:111) | 설명 보완 |
| GitHub 최대 8·OSV 최대 4 병렬 요청 | [apps/web/server/github/archive.ts](/Users/domado/Documents/GitHub/teum/apps/web/server/github/archive.ts), [apps/web/server/services/dependencies.ts](/Users/domado/Documents/GitHub/teum/apps/web/server/services/dependencies.ts) | 일치; 단계 내 병렬임을 유지 |
| Sandbox 격리·고객 코드 미실행 | [apps/web/workflows/runtime.ts](/Users/domado/Documents/GitHub/teum/apps/web/workflows/runtime.ts), [docs/SECURITY_DATA.md](/Users/domado/Documents/GitHub/teum/docs/SECURITY_DATA.md) | 코드·실행 기록과 일치 |
| 캐시 검증·OSV 새 조회·AI 비밀정보 재검사 | [apps/web/workflows/runtime.ts](/Users/domado/Documents/GitHub/teum/apps/web/workflows/runtime.ts), [apps/web/workflows/local-analysis.ts](/Users/domado/Documents/GitHub/teum/apps/web/workflows/local-analysis.ts) | 설명 추가 |
| 제한된 자체 분석과 미지원 범위 | [apps/web/server/services/native-analysis.ts](/Users/domado/Documents/GitHub/teum/apps/web/server/services/native-analysis.ts), [docs/NON_AI_SERVICE_STATUS.md](/Users/domado/Documents/GitHub/teum/docs/NON_AI_SERVICE_STATUS.md) | 누락된 기능·한도 보충 |
| 서버 → Client 데이터 전달은 사실 기록 | [docs/SERVER_COMPONENT_DATA_FLOW.md](/Users/domado/Documents/GitHub/teum/docs/SERVER_COMPONENT_DATA_FLOW.md) | 취약점 판정과 구별 |
| 최초 분석·재점검의 캐시와 준비 VM | [docs/SERVER_COMPONENT_DATA_FLOW_PRODUCTION.md](/Users/domado/Documents/GitHub/teum/docs/SERVER_COMPONENT_DATA_FLOW_PRODUCTION.md) | 당시 2회 기록과 일치 |
| 현재 조사·독립 반증의 두 대화 | [apps/web/server/services/repository-review.ts](/Users/domado/Documents/GitHub/teum/apps/web/server/services/repository-review.ts:65) | 현재 코드에 맞춰 수정 |
| 실제 제공한 파일·줄로 인용 복원·검증 | [apps/web/server/services/repository-review.ts](/Users/domado/Documents/GitHub/teum/apps/web/server/services/repository-review.ts:259) | 일치; 추론 정확도와 구별 |
| Sol 합성 25사례와 10-21 평가 | [docs/AI_EVAL.md](/Users/domado/Documents/GitHub/teum/docs/AI_EVAL.md:723), [docs/verification/ai-first-evaluation-r4-20261021.json](/Users/domado/Documents/GitHub/teum/docs/verification/ai-first-evaluation-r4-20261021.json) | 누락 이력 보완; 일반 정확도 아님 |
| 수정 전·후 2회 AI 통합·partial·다운로드 한계 | [docs/verification/ai-first-production-e2e-20261021.json](/Users/domado/Documents/GitHub/teum/docs/verification/ai-first-production-e2e-20261021.json), [docs/AI_EVAL.md](/Users/domado/Documents/GitHub/teum/docs/AI_EVAL.md:587) | 검증 범위를 구체화 |
| 후속 후보 3표본 보고서 1/3·핵심 조사 0/3 | [docs/verification/read-budget-new-real-20261022.json](/Users/domado/Documents/GitHub/teum/docs/verification/read-budget-new-real-20261022.json), [docs/verification/review-effective-budget-20261022.json](/Users/domado/Documents/GitHub/teum/docs/verification/review-effective-budget-20261022.json) | 채택 보류 후보의 결과; 현재 서비스 성적으로 합산하지 않음 |
| 재점검 비교 조건·판단 보류 | [packages/analysis/compare.ts](/Users/domado/Documents/GitHub/teum/packages/analysis/compare.ts) | 일치 |
| 비밀정보의 프로젝트별 식별과 줄 이동 | [docs/verification/security-comparison-20261016.json](/Users/domado/Documents/GitHub/teum/docs/verification/security-comparison-20261016.json) | 기록과 일치; 파일 이동까지 일반화하지 않음 |
| 정지 → 객체 부재 확인 → 종료 → 예약 반환 | [apps/web/workflows/runtime.ts](/Users/domado/Documents/GitHub/teum/apps/web/workflows/runtime.ts:279) | 일치; 물리 삭제 감사와 구별 |
| SDK r1~r15 표·실패 상태·누계 | [docs/verification/sdk-r1-r15-summary-20261024.json](/Users/domado/Documents/GitHub/teum/docs/verification/sdk-r1-r15-summary-20261024.json) 및 이 JSON이 가리키는 원본 result.json 15개 | 원본 해시·usage·시간·비용 대조 통과 |
| SDK 품질·요청 감소·시간 회귀 | 같은 집계의 quality 원본 13개 및 비교 값 | 품질 기록 해시·수치 재계산 일치 |
| r16/r17 미채택·r18 미완료·r14/r15 생성 유지 | [docs/verification/sdk-explicit-review-live-20261024.json](/Users/domado/Documents/GitHub/teum/docs/verification/sdk-explicit-review-live-20261024.json), [docs/verification/sdk-verbosity-live-20261024.json](/Users/domado/Documents/GitHub/teum/docs/verification/sdk-verbosity-live-20261024.json), [docs/verification/sdk-readable-live-20261024.json](/Users/domado/Documents/GitHub/teum/docs/verification/sdk-readable-live-20261024.json), [docs/verification/sdk-readable-final-validation-20261024.json](/Users/domado/Documents/GitHub/teum/docs/verification/sdk-readable-final-validation-20261024.json) | 후속 범위 보충 |
| public 16테이블·표시 15·관계선 19 | [읽기 전용 카탈로그](/Users/domado/Documents/GitHub/teum_public/_workspace/2026-10-30-001/schema-catalog.json), [ERD](/Users/domado/Documents/GitHub/teum_public/assets/diagrams/database.svg) | 컬럼 자료형·PK/FK·선택성·카디널리티 일치 |
| 라이브러리 버전 11개·고정 엔진 | [apps/web/package.json](/Users/domado/Documents/GitHub/teum/apps/web/package.json), [기술 표](/Users/domado/Documents/GitHub/teum_public/docs/ENGINEERING.md:115) | 저장소 고정값과 일치 |
| 9개 SVG·3개 JPG | [자산 설명](/Users/domado/Documents/GitHub/teum_public/docs/ASSETS.md)와 실제 파일 | 구조·수치·샘플 표기 확인; 고객 데이터로 표시하지 않음 |

## 숫자 재계산

- 15회 요청 합계 **250회**, 수신 토큰 **14,182,881개**, usage 추정 비용 **$14.7371835 → $14.7372**.
- r4의 **$6.23304**는 미확정 예약이며 실제 청구액·수신 usage 비용 합계에 넣지 않음.
- r5 대비 r14/r15 평균: 요청 **92.6%**, 입력 **91.2%**, 출력 **31.0%**, 총토큰 **88.0%**, 전체 시간 **32.2%**, usage 추정 비용 **32.7% 감소**.
- 직전 성공본 r11/r12 평균 대비 전체 시간은 **5.3% 증가**. 요청을 줄였다는 사실만으로 계속 빨라졌다고 주장하지 않음.
- 원 실행 상태 기준 보고서 완료 **11/15**, 실패 **4/15**. 완료하면서 핵심 4/4인 회차는 **8회**. 실패 원문을 나중에 복구한 점수를 실행 성공으로 바꾸지 않음.
- ERD: 외래키 총 **32개** 중 **19개 표시·13개 생략**, 표시 관계 중 식별 **5개·비식별 14개**. 관계선 자체는 수정할 이유가 없었음.

## 줄바꿈·윤문

README 38줄, SDK 18줄, ASSETS 28줄, DEMO 6줄, ENGINEERING 20줄, VALIDATION 11줄에서 종결 뒤 줄바꿈 누락을 확인했습니다. 숫자는 문장 수가 아닌 누락이 있는 원문 줄 수입니다. 모든 본문·목록·표의 한국어 종결 뒤에 <br>를 적용하고, 큰 절과 큰 문단에는 두 번 적용했습니다. 제목·코드·URL·이미지 대체 텍스트는 검사 대상에서 제외했습니다. 세 번 이상 연속되는 <br>는 없습니다.

GitHub Markdown 렌더링 결과를 로컬에서 열어 데스크톱 README, 390px 폭 README, 긴 자산 설명의 표·문단 간격을 확인했습니다. 전체 브라우저·실기기 접근성 시험은 아닙니다.

[최종 윤문본](/Users/domado/Documents/GitHub/teum_public/_workspace/2026-10-30-001/final.md) · [문체 변경 집계](/Users/domado/Documents/GitHub/teum_public/_workspace/2026-10-30-001/style-metrics.json) · [적용한 문체 수정](/Users/domado/Documents/GitHub/teum_public/_workspace/2026-10-30-001/style-edits.json)

- 사실 정정과 줄바꿈을 끝낸 본문 기준 **32,868자 → 32,868자**, 순수 문체 수정 **1문장**, 참고 변경률 **0.0274%**.
- D-2 중요성 강조 **1→0**, A-7 직역 **0→0**, A-8 이중 피동 **0→0**, H-1 문단 접속사 밀집 **0→0**. 기술 문서의 표·격식체·지원 범위 설명은 유지했고, 사용자 요청대로 쉼표는 허용했습니다.
- “응답 완료와 품질 기준 통과의 구별이 중요합니다.” → “응답 완료가 품질 기준 통과를 뜻하지는 않습니다.”
- 자체검증 **5/6**, 등급 **B**. 설치된 [humanize-korean 스킬](/Users/domado/.codex/skills/humanize-korean/SKILL.md)의 quick-rules는 “확정 판정은 … verify_change_rate.py — 자가 산출값은 참고용”이라고 규정하지만, 설치 경로에 해당 검증기가 없어 공식 변경률은 확정하지 않았습니다. 참고 계산을 공식 통과로 처리하지 않았으며, 변경률 목표를 맞추기 위한 추가 윤문도 하지 않았습니다.
- 스킬 안내에 따라 정밀 검증은 Claude Code의 정밀 모드(3콜)를 권장합니다. 의미·고유명사·수치·날짜·코드·링크 보존과 격식체 유지 등 나머지 항목은 확인했습니다.

## 실행·검사 결과

```sh
cd /Users/domado/Documents/GitHub/teum_public
python3 _workspace/2026-10-30-001/verify_audit.py
git diff --check
git -C /Users/domado/Documents/GitHub/teum diff --quiet HEAD FETCH_HEAD
git -C /Users/domado/Documents/GitHub/teum status --porcelain
```

[자동 대조 결과](/Users/domado/Documents/GitHub/teum_public/_workspace/2026-10-30-001/verification.json) · [외부 링크 응답 기록](/Users/domado/Documents/GitHub/teum_public/_workspace/2026-10-30-001/link-checks.json)

| 검사 | 결과 |
|---|---|
| 문장 줄바꿈·큰 절 간격·중복 줄바꿈 | 6문서 통과, 종결 줄바꿈 누락 0 |
| 상대 링크·이미지 | 56개 참조 존재 확인 |
| 외부 URL | 서로 다른 12개 모두 리다이렉트 후 HTTP 200 |
| SDK 원본 | 15개 SHA256·요청·usage·시간·비용 통과 |
| SDK 품질 원본 | 제공된 13개 SHA256 일치 |
| 공개 수치표 | 토큰·요청 60셀, 시간·비용 30셀 일치 |
| 성과 비교 | 12개 변화율 재계산·공개 값 대조 통과 |
| SVG | 9개 XML 파싱·중복 ID·외부 리소스·실행 요소 검사 통과 |
| SDK SVG | 가로·세로 합계 8개 지표 일치 |
| DB 도식 | 19개 관계·표시 컬럼의 자료형·키·선택성 통과 |
| 라이브러리 | 공개 버전 11개 일치 |
| Git | diff 공백 오류 없음, 비공개 파일 트리 원격 일치·작업 트리 변경 없음 |

## 변경 파일과 남은 확인

- [README.md](/Users/domado/Documents/GitHub/teum_public/README.md): 현재 지원 범위·검증 시점·DB 설명과 줄바꿈.
- [docs/ENGINEERING.md](/Users/domado/Documents/GitHub/teum_public/docs/ENGINEERING.md): 실행 순서·캐시·자체 분석·현재 AI 경로와 줄바꿈.
- [docs/VALIDATION.md](/Users/domado/Documents/GitHub/teum_public/docs/VALIDATION.md): 후속 평가·부분 완료·미검증 항목과 현재 실행본의 경계.
- [docs/AI_SDK_R1_R15.md](/Users/domado/Documents/GitHub/teum_public/docs/AI_SDK_R1_R15.md): 15회 집계 범위·후속 후보 설명과 1문장 윤문.
- [docs/ASSETS.md](/Users/domado/Documents/GitHub/teum_public/docs/ASSETS.md): ERD 총수·생략 범위·긴 문단 분리.
- [docs/DEMO.md](/Users/domado/Documents/GitHub/teum_public/docs/DEMO.md): 기존 의미를 유지한 문장·문단 줄바꿈.
- [assets/diagrams/database.svg](/Users/domado/Documents/GitHub/teum_public/assets/diagrams/database.svg): 대조일·전체 테이블 수·생략 테이블 메타데이터. 화면 배치는 유지.

비공개 [docs/REPOSITORY_REVIEW.md](/Users/domado/Documents/GitHub/teum/docs/REPOSITORY_REVIEW.md:44)에도 과거 3단계 흐름이 현재처럼 남아 있습니다. 공개 설명은 실제 코드에 맞췄으며, 비공개 문서의 날짜·현재 구현 설명 갱신은 별도 후속 작업입니다.

이번에는 문서·정적 자산만 수정했으므로 앱 빌드·제품 테스트 전체·새 Sandbox 실행·유료 모델 평가를 반복하지 않았습니다. 기존 검증 기록이 뒷받침하는 범위를 적었으며, 최신 운영 배포·모든 장애·독립 고객 저장소 품질은 새로 검증하지 않았습니다. 샘플 JPG의 캡처일·Chrome 출처는 기존 기록을 유지했으며 이미지 자체로 촬영 메타데이터를 새로 입증하지 않았습니다.

커밋·push·배포는 하지 않았습니다. `_workspace`는 비공개 소스 경로와 카탈로그를 포함하는 로컬 검토 자료이므로 공개 커밋 대상에서 제외해야 합니다. 공개 반영 후보는 위 7개 파일입니다.
