---
name: explain
description: Use after the freeze commit and before submission. Writes DECISIONS.md section 0 (question-to-file map, storyline, top decisions, numbers, expected essay answers) in complete spoken Korean sentences, copied from the existing decision cards, so the user can answer the follow-up essay questions after reading it once.
---

# explain — 서술형 준비 (2~3분 안에 쓴다)

근거는 `DECISIONS.md` §1 카드, `README.md`(구조도·성적표·바꾸려면 여기), `data/DATA_CARD.md`, `WORKLOG.md`, `PLAN.md`(R·C·단계), `verify/report.md` 사람용 5줄, `git log`만. 지어내지 않는다. 새 계산·새 가정을 더하지 않는다.
**소리 내어 읽을 수 있는 완전한 문장**으로. 키워드 나열·화살표·가운뎃점 나열 금지. **본문에 R·C·D 번호를 쓰지 않고 말로 쓴다.** 번호는 문단 끝 괄호에 한 번만. 숫자 앞뒤 띄어쓰기. 2쪽 이내.

## DECISIONS.md §0에 쓴다 (템플릿 순서대로)
### 문항 → 볼 곳 표
템플릿의 표는 고치지 않는다. 괄호 속 항목(예: 휴일)이 이 과제에 없으면 그 낱말 뒤에만 "(해당 없음)"을 붙인다.

### 줄거리 — 국면 4~6개, 한 줄씩
"담당자와 기준을 합의했고, 가장 작은 버전으로 숫자를 낸 뒤, …, 마지막에 검증자가 다른 방법으로 다시 세어 확인했다."

### 결정 다섯 가지 — 결과 숫자에 가장 크게 영향 준 것부터
각각 세 문장: 무엇을 어떻게 정했다 / 담당자가 "…"라고 했기 때문이다(원문) / 다른 선택은 …였고 안 쓴 이유는 …. **§1 카드의 "담당자 말·한 줄 답·왜·다른 선택"을 옮겨 쓴다.**

### 기억할 숫자 5개 · 가정으로 둔 것과 그 영향 · AI 가 틀렸던 것과 고친 것 · 안 한 것 · 한계 · verifier 가 본 것
숫자는 README 성적표와 report 사람용 5줄에서 가져온다(테스트 수, PASS 수, 재계산 차이, 잡은 오류, 원본 수). AI 교정은 §2 표를 문장으로.

### 예상 서술형 답 초안 6유형 (각 3~4문장: 결론 → 근거 → 약점 → 파급 → 다음 검증)
1. 전체를 어떤 단계로 나눴고 왜 (→ README 구조도 상자 이름과 step 마다 넣은 조건)
2. 기준 정의: 기간 시작·끝, 시간대, 주말·휴일 (→ 카드 "담당자 말"·"한 줄 답"의 문장과 숫자)
3. 데이터 이상 처리와 틀리면 어떤 수치가 왜곡되나 (→ DATA_CARD 함정 표의 개수·예시, 카드 "틀리면")
4. 전제 오류 문항("○○한다고 가정하고…" 실제로 안 한 설계) → 사실을 바로잡고 가정에도 답한다 (→ "안 한 것", 카드 "다른 선택")
5. 변경 요청이 오면 어느 파일·함수를 고치나 (→ 카드 "어디", README "바꾸려면 여기" — 파일 이름, 함수 이름, configs 키 이름을 그대로 적는다)
6. 검증 방법과 결과, AI에게 맡긴 것과 직접 판단·고친 것 (→ report 사람용 5줄, README 성적표, §2)

## README 마무리
"왜 이렇게 했나"·"안 한 것·한계"를 §0과 같은 내용으로. "확인 방법" 성적표 4줄이 최종 값인지 확인.

## 커밋 → 사용자에게
`explain: 서술형 준비 | verify: §0 작성` 커밋(국면 커밋이라 허용).
"DECISIONS.md §0을 위에서 아래로 한 번 읽으세요(5분). 서술형 중에는 맨 위 표대로 그 파일의 그 절만 여세요. 처음 보는 내용이 있으면 그 줄을 알려 주세요." 그다음 제출.
