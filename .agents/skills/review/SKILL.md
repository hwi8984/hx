---
name: review
description: Use right before freezing, in a freshly started Codex session that has not seen the implementation. Reads verify/report.md and the ledgers, runs the final checks, fixes README, and makes the freeze commit.
---

# review — 동결 검토 (새로 켠 세션에서)

이 세션은 만든 적이 없다는 전제로 **파일만 보고** 검토한다. 코드는 작은 수정만 한다.

## 1. verifier 먼저
`verify/report.md`가 없거나 동결 전 판정이 없으면 사용자에게 "검증해"를 요청해 verifier를 돌린다. report의 FAIL마다: 고칠 수 있으면 작은 수정 + 재검증, 아니면 DECISIONS §3 한계에 적는다.

## 2. 추적표 — 검증표 R마다
R → 구현 위치(파일·함수·상자 번호) → 증거 → 상태. 증거 없는 ✅는 ⏳로 되돌린다. verifier ○인데 PASS 없는 ✅도 되돌린다. 구현 위치를 못 찾는 R은 ❌.

## 3. 조건 장부 C 마감
미확정이 남아 있으면 가정으로 바꾸고 결과에 표시가 있는지 확인. "반영" 칸이 빈 C는 코드·configs에서 찾아 채우거나 한계로.

## 4. 새로 실행
README "바로 실행" 명령을 그대로 새로 실행 → out/latest 생성·숫자 일치. 테스트 실행. `HXCMD check --run` 경고 해결(루트 문서 수, 사본, out 폴더, README 제목 9개, 증거 무효, report FAIL).

## 5. 처음 보는 사람 시험
README만 읽고 "무엇을 만들었나 / 어떻게 실행하나 / 어떤 단계로 만들었나"를 말해 본다. 다른 파일을 열어야 답할 수 있으면 README를 고친다. "바꾸려면 여기" 표가 실제 위치인지 확인.

## 6. 코드 검토
`/review`가 있으면 쓴다. 없으면 `git diff <agree 커밋>..HEAD -- src/`: 요청에 없는 기능, 주석 없는 파일, configs에 있어야 할 숫자가 코드에 박힌 곳.

## 7. 제출 조건 대조
과제 README(또는 안내)의 제출 조건을 항목마다 표로: `조건 | 충족/누락 | 어디(파일·명령)`. 파일 이름, 형식, 실행 명령 한 줄, 요구된 문서가 전부 있는지. 누락이 있으면 그것만 고치고 다시 표를 쓴다.

## 8. 커밋
DECISIONS §3 안 한 것·한계 채움. `freeze: 검토 완료 | verify: R1~Rn 상태, verifier PASS n/m, 테스트 k개`. 이후 코드를 고치지 않는다.
