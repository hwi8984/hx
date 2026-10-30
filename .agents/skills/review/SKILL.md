---
name: review
description: Use right before freezing, in a freshly started Codex session that has not seen the implementation. Reads verify/report.md and the ledgers, runs the final checks, fixes README, and makes the freeze commit.
---

# review — 동결 검토 (새로 켠 세션에서)

이 세션은 만든 적이 없다는 전제로 **파일만 보고** 검토한다. 코드는 작은 수정만 한다.

## 1. verifier 먼저
`verify/report.md`가 없거나 동결 전 판정이 없으면 사용자에게 "검증해"를 요청해 verifier를 돌린다. report의 FAIL마다: 고칠 수 있으면 작은 수정 + 재검증, 아니면 DECISIONS §3 한계에 적는다.

## 2. 증거 확인 — 검증표 R마다 (새 표를 만들지 않는다)
R 행의 증거 칸에 적힌 커밋·verifier 판정·증거 파일이 실제로 있는지 본다(`git log`, `verify/report.md`, `ls verify/`). 증거 없는 ✅는 ⏳로 되돌린다. verifier ○인데 PASS 없는 ✅도 되돌린다. 구현 위치는 README 구조도와 DECISIONS 카드 "어디"에서 확인하고, 못 찾는 R은 ❌. PLAN 에 추적표를 따로 만들지 않는다(m4 에서 27행 중복이 생겼다).
DECISIONS 카드 점검: 조건 묶음마다 카드가 있나, 카드마다 "담당자 말"과 "어디"가 채워졌나, 본문에 번호 대신 말을 썼나. 빠진 카드는 여기서 채운다(코드는 안 고친다).

## 3. 조건 장부 C 마감
미확정이 남아 있으면 가정으로 바꾸고 결과에 표시가 있는지 확인. "반영" 칸이 빈 C는 코드·configs에서 찾아 채우거나 한계로.

## 4. 새로 실행
README "바로 실행" 명령을 그대로 새로 실행 → out/latest 생성·숫자 일치. 테스트 실행. `HXCMD check --run` 경고 해결(루트 문서 수, 사본, out 폴더, README 제목 9개, 증거 무효, report FAIL).

## 5. 처음 보는 사람 시험
README만 읽고 "무엇을 만들었나 / 어떻게 실행하나 / 어떤 단계로 만들었나"를 말해 본다. 다른 파일을 열어야 답할 수 있으면 README를 고친다. "바꾸려면 여기" 표가 실제 위치인지 확인. "확인 방법"이 명령 2줄 + 성적표 4줄인지, 그 밖의 설명이 붙어 있으면 DECISIONS 로 옮긴다. 담당자가 보는 화면·결과 파일에 R·C·D 번호나 작업 용어가 있으면 말로 고친다(코드 수정 허용 — 문구만). 문구라도 src 를 고쳤으면 `HXCMD check` 의 "증거 무효" 경고가 뜨므로 "검증해"를 한 번 더 요청한다(또는 이 문구 수정을 §1 verifier 요청 전에 먼저 한다).

## 6. 코드 검토
`/review`가 있으면 쓴다. 없으면 `git diff <agree 커밋>..HEAD -- src/`: 요청에 없는 기능, 주석 없는 파일, configs에 있어야 할 숫자가 코드에 박힌 곳.

## 7. 제출 조건 대조
과제 README(또는 안내)의 제출 조건을 항목마다 표로: `조건 | 충족/누락 | 어디(파일·명령)`. 파일 이름, 형식, 실행 명령 한 줄, 요구된 문서가 전부 있는지. 누락이 있으면 그것만 고치고 다시 표를 쓴다.

## 8. 커밋
DECISIONS §3 안 한 것·한계 채움. `freeze: 검토 완료 | verify: R1~Rn 상태, verifier PASS n/m, 테스트 k개`. 이후 코드를 고치지 않는다.
