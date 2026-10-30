---
name: explain
description: Use after the freeze commit and before submission. Writes DECISIONS.md section 0 (storyline, step table, top decisions, expected essay answers) in complete spoken Korean sentences so the user can answer the follow-up essay questions without the workspace.
---

# explain — 서술형 준비 (2~3분 안에 쓴다)

근거는 `WORKLOG.md`, `DECISIONS.md`, `PLAN.md`(R·C), `verify/report.md`, `git log`만. 지어내지 않는다.
**소리 내어 읽을 수 있는 완전한 문장**으로(B 단계표만 표 허용). 키워드 나열·화살표·가운뎃점 나열 금지. 2쪽 이내.

## DECISIONS.md §0에 쓴다
### A. 줄거리 — 국면 4~6개, 한 줄씩
"담당자와 기준을 합의했고, 가장 작은 버전으로 숫자를 낸 뒤, …, 마지막에 검증자가 다른 방법으로 다시 세어 확인했다."

### B. 단계표 — 모든 step 한 줄씩
`단계 | 구현 | 판단(D) | 변경(전→후, 계기) | 검증(방법→결과)`. 한 줄에 "무엇을 했다 → 왜 → 어떻게 확인했다 → 틀리면 무엇이 망가지나".

### C. 결정 Top 5 — 결과 숫자에 가장 크게 영향 준 것부터
질문 → 한 줄 답 → 이유(발언·데이터) → 다른 선택 → 참조 C.

### D. 핵심 숫자 3~5개 · 가정으로 둔 C와 그 영향 · AI가 틀렸던 것과 고친 것 · 안 한 것 · 한계 · verifier가 본 것

### E. 예상 서술형 6유형 답 초안 (각 3~4문장: 결론 → 근거(파일·함수·수치) → 약점 → 파급 → 다음 검증)
1. 전체를 어떤 단계로 나눴고 왜 (→ README 구조도)
2. 기준 정의: 기간 시작·끝, 시간대, 주말·휴일 (→ 장부 C)
3. 데이터 이상 처리와 틀리면 어떤 수치가 왜곡되나 (→ C의 "영향" 칸)
4. 전제 오류 문항("○○한다고 가정하고…" 실제로 안 한 설계) → 사실을 바로잡고 가정에도 답한다
5. 변경 요청이 오면 어느 파일·함수를 고치나 (→ README "바꾸려면 여기")
6. 검증 방법과 결과, AI에게 맡긴 것과 직접 판단·고친 것 (→ report.md, AI 교정 기록)

## README 마무리
"왜 이렇게 했나"·"안 한 것·한계"를 §0과 같은 내용으로.

## 커밋 → 사용자에게
`explain: 서술형 준비 | verify: §0 A~E 작성` 커밋(국면 커밋이라 허용).
"§0을 위에서 아래로 소리 내어 한 번 읽으세요(5분). 처음 보는 내용이 있으면 그 줄을 알려 주세요." 그다음 제출.
