# 이미지와 도식 안내

[README로 돌아가기](../README.md)

teum의 공개 화면과 브랜드 자산으로 만든 문서 자료입니다.<br>
스크린샷에는 공개 체험용 샘플만 사용했습니다.

<br>
<br>

## 01. 화면 자료

2026-10-14에 공개 서비스의 Chrome 화면을 캡처했습니다.<br>
고객 계정·고객 저장소·운영 분석 결과를 촬영한 자료가 아닙니다. 화면의 코드는 공개 체험용 합성 예시입니다.

| 파일 | 화면 출처 |
|---|---|
| [rule-review.jpg](../assets/screenshots/rule-review.jpg) | [규칙 결과](https://teum.today/demo/scans/R-042?source=rules) |
| [ai-review.jpg](../assets/screenshots/ai-review.jpg) | [AI 결과](https://teum.today/demo/scans/R-042?source=ai) |
| [coverage.jpg](../assets/screenshots/coverage.jpg) | [부분 완료 범위](https://teum.today/demo/scans/R-047/coverage) |

화면의 샘플 안내를 유지했습니다. 제품이 바뀌면 현재 서비스 화면과 차이가 생길 수 있습니다.

<br>
<br>

## 02. 설명용 SVG

| 파일 | 설명하는 내용 |
|---|---|
| [hero.svg](../assets/diagrams/hero.svg) | 열린 틈 심벌과 서비스 슬로건 |
| [review-flow.svg](../assets/diagrams/review-flow.svg) | 연결 → 점검 → 검토 → 재점검 흐름 |
| [architecture.svg](../assets/diagrams/architecture.svg) | 웹·DB·작업 실행·격리 분석·외부 서비스의 경계 |
| [database.svg](../assets/diagrams/database.svg) | PK·FK 표시·자료형·Crow’s Foot 기호로 표시한 서비스 테이블 15개와 Auth 참조 |
| [sdk-optimization.svg](../assets/diagrams/sdk-optimization.svg) · [세로형](../assets/diagrams/sdk-optimization-mobile.svg) | 첫 4/4 성공본과 최종 두 회차의 요청·토큰·시간·usage 추정 비용 비교 |

순수 SVG와 CSS로 구성했습니다. 스크립트·외부 이미지·외부 폰트 요청은 없습니다.<br>
흐름·아키텍처 도식의 텍스트와 화살표는 정적으로 읽을 수 있습니다.<br>
흐름·아키텍처 도식의 애니메이션은 구성 요소의 연결과 데이터 이동 방향을 보여줍니다.<br>
이 움직임은 실행 시간이나 실제 진행률을 표현하지 않습니다.<br>
아키텍처는 상단 요청·접수 → 하단 세 연결의 동시 왕복 → 결과 저장 → 상단 결과 조회 왕복 순서로 표시합니다.<br>
시작 요청의 접수 응답과 분석 결과 조회를 구분한 표현입니다. 실제 Workflow 실행과 접수 응답은 겹칠 수 있으며, 하단 세 연결의 동시 움직임이 실제 작업의 병렬 실행을 뜻하지는 않습니다.<br>
모션 감소 설정에서는 움직이는 장식을 멈추거나 숨깁니다. 이미지가 작게 보이면 원본 SVG 링크를 열어 확대할 수 있습니다.

ERD는 2026-10-27 실제 PostgreSQL 카탈로그를 읽기 전용으로 조회해 대조했습니다.<br>
서비스의 `public` 테이블 15개와 `auth.users` 참조에 주요 키·자료형을 표시하고, 자기 참조를 포함한 외래키 19개를 연결했습니다.<br>
`PK`는 기본키, `FK`는 외래키, `PK/FK`는 두 역할을 겸하는 컬럼입니다. 여러 컬럼에 `PK`가 표시되면 함께 복합 기본키를 이룹니다. 키 표시는 같은 열에 정렬했습니다.<br>
테이블은 헤더 배경과 옅은 행 구분선으로 묶었습니다. 모든 관계선과 끝 기호는 같은 진한 회색과 두께를 사용하며, 색상으로 관계의 종류나 중요도를 구분하지 않습니다.<br>
관계선 양끝의 Crow’s Foot 기호는 막대가 하나, 원이 선택, 갈래가 여러 개를 뜻합니다. NULL 허용과 기본키·UNIQUE 제약을 대조해 선택 여부와 개수를 표시했습니다.<br>
`scan_runs.baseline_id`의 자기 참조도 선으로 표시했습니다. 일부 외래키 13개, 공통 `workspace_id` 등 일부 복합 외래키 컬럼, 전체 컬럼·private 및 Auth 내부 구조는 생략했습니다.<br>
`uploads`는 현재 GitHub 수집 입력의 보관 기록으로 사용합니다.<br>
실제 사용자·분석 내용·운영 설정은 포함하지 않았습니다. 정적 SVG이므로 DB 구조 변경 시 다시 대조해야 합니다.

SDK 그래프는 고정한 자사 코드 26개 파일·2,277줄의 실행 기록으로 만들었습니다.<br>
각 지표에서 r5를 100으로 놓았으며 파란 막대는 r14/r15의 평균을 나타냅니다.<br>
시간은 기록된 전체 실행 시간이고 비용은 usage 기반 추정치입니다.<br>
표시값은 반올림하며 절감률과 막대 길이는 반올림 전 원값으로 계산했습니다.<br>
가로형과 세로형 SVG는 같은 값을 표시합니다.<br>
막대와 감소율 숫자는 약 3초 안에 최종값에 멈춘 뒤 같은 동작을 8초 주기로 반복합니다.<br>
움직이는 중간값은 관측치가 아닙니다. 모션 감소 설정에서는 최종값만 표시합니다.

<br>

색상은 teum의 흰 바탕, 짙은 글자색, 파란 강조색을 사용했습니다.<br>
[브랜드 심벌](../assets/brand/teum-mark.svg)은 기존 서비스의 ‘열린 틈’ 형상을 재사용했습니다.<br>
문서·이미지 공개가 비공개 애플리케이션 코드나 브랜드에 대한 별도 사용 허락을 뜻하지는 않습니다.
