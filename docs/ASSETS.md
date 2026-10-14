# 이미지와 도식 안내

[README로 돌아가기](../README.md)

공개 서비스의 화면과 기존 브랜드를 바탕으로 만든 포트폴리오 자료입니다.<br>
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

순수 SVG와 CSS로 구성했습니다. 스크립트·외부 이미지·외부 폰트 요청은 없습니다.<br>
텍스트와 화살표는 정적으로 읽을 수 있고, 애니메이션은 연결 순서를 강조합니다. 실행 시간이나 실제 진행률을 표현하지 않습니다.<br>
모션 감소 설정에서는 움직이는 장식을 멈추거나 숨깁니다. 이미지가 작게 보이면 원본 SVG 링크를 열어 확대할 수 있습니다.

<br>

색상은 teum의 흰 바탕, 짙은 글자색, 파란 강조색을 사용했습니다.<br>
[브랜드 심벌](../assets/brand/teum-mark.svg)은 기존 서비스의 ‘열린 틈’ 형상을 재사용했습니다.<br>
문서·이미지 공개가 비공개 애플리케이션 코드나 브랜드에 대한 별도 사용 허락을 뜻하지는 않습니다.
