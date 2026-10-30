---
name: change
description: Use when the stakeholder changes a requirement or condition, or sends a new file into data/incoming after agreement. Adds new R and C rows (never deletes), marks old rows 변경됨, and proposes the next step.
---

# change — 조건 변경·새 파일

## 1. 장부에 적는다 (지우지 않는다)
- 바뀐 조건: 조건 장부에 **새 C 행**(출처 발언 시각, 상태 확인됨). 옛 C 행 상태를 "변경됨"으로.
- 바뀐 요구: 검증표에 **새 R 행**. 옛 R 행 상태를 "변경됨"으로.
- 새 파일: `data/incoming/`에 두고 고치지 않는다. DATA_CARD에 그 파일 절(행·열·기간·함정 10종·예시 2행) 추가. 숫자에 영향 주는 차이는 C 행.

## 2. 영향 3줄 보고
어느 R이 바뀌나 / 어느 구조도 상자·파일·configs 키가 바뀌나 / 이미 낸 숫자 중 무엇이 달라지나.

## 3. 다음 단계 제안
바뀐 R을 다루는 step 계획 3줄(+C)을 내고 승인을 기다린다. 변경 자체로는 커밋하지 않는다. 구현 step 커밋에 포함.
변경 뒤 첫 step이 끝나면 "검증해"를 권한다(verifier가 새 C 반영을 본다).

## 4. 해석이 갈리면
결과 숫자 두 가지를 보여 주고 예/아니오로 묻는 DM 문안을 사용자에게 준다. 답이 없으면 가정 C로 계산하고 표시한다.
