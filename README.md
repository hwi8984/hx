# hx — Codex 작업 하네스

코딩 에이전트(OpenAI Codex CLI)와 함께 시간이 정해진 과제를 끝낼 때 쓰는 작업 규칙, 기록 틀, 절차서, 독립 검증자, 점검 도구 모음이다. 과정 도구만 담겨 있고 과제 답이나 도메인 코드, 데이터는 없다. 표준 라이브러리만 쓴다.

## 설치 (Codex가 이 절을 읽고 그대로 한다 — 3분)
전제: 이 저장소는 과제 폴더 **밖** `~/hx`에 받는다. 터미널의 현재 폴더는 **과제 루트**다. Codex는 업데이트하지 않는다. 과제의 기존 파일은 덮지 않는다.

1. 받기는 사용자가 Codex를 켜기 **전에** 터미널에서 직접 친다: `git clone https://github.com/hwi8984/hx ~/hx` — Codex는 과제 폴더 밖에 쓰는 권한이 막혀 있을 수 있다. `~/hx`가 아직 없으면 직접 받지 말고 사용자에게 이 한 줄을 치라고 알린다.
2. 과제 루트에서: `python ~/hx/hx.py init 10:00` (시험 시작 시각 HH:MM. python3이면 `python3`. Windows PowerShell은 `~` 대신 `$HOME/hx`)
   - 루트에 `AGENTS.md PLAN.md WORKLOG.md DECISIONS.md`, `.agents/skills/`(5), `.codex/agents/verifier.toml`, `verify/`, `data/DATA_CARD.md`가 생긴다. 있던 파일은 그대로 둔다. 과제 README가 있으면 맨 아래에 제출 절 틀을 덧붙인다.
   - init이 git 사용자 이름이 없으면 설정하고 `setup` 커밋까지 한다. 과제가 준 데이터 파일은 어디 있든 원본으로 잠근다.
   - 과제가 준 데이터가 `data/raw` 밖에 있으면 옮기지 않는다(원본 보호). 과제 README가 다른 위치를 정했으면 그것을 따른다.
3. 사용자에게 알린다: "Codex를 껐다 켜 주세요(`/exit` → `codex`). 그래야 AGENTS.md가 적용됩니다." 하위 에이전트(verifier)는 기본으로 켜져 있어 따로 켤 것이 없다.
4. (새 세션에서) 사용자가 확인: `/skills`에 5개 → "지금 적용 중인 규칙 3줄 요약해줘" → "verifier 에이전트로 README 첫 줄만 읽어 봐".
   - skills가 안 보여도 AGENTS.md "상태 → 절차" 표가 같은 파일을 읽게 하므로 그대로 진행한다.
   - verifier가 안 뜨면 검증은 두 번째 터미널에서 `cd verify && codex`.
5. 과제 README를 읽고 `.agents/skills/kickoff/SKILL.md` 절차를 시작한다.

수시로 `python ~/hx/hx.py board` · 합의 끝 `python ~/hx/hx.py lock` · 동결 전 `python ~/hx/hx.py check --run`

## 구성
```
AGENTS.md              작업 규칙 (과제 루트로 복사됨)
templates/             PLAN(검증표 R·조건 장부 C) · WORKLOG · DECISIONS · README · DATA_CARD · verify_report 틀
.agents/skills/        절차서 5개 — kickoff(합의) step(구현) change(변경) review(검토) explain(설명)
.codex/agents/         verifier.toml — 독립 검증자 (Codex 하위 에이전트)
verify/                RULES.md(검증자 규칙) · AGENTS.md(두 번째 터미널용 같은 역할)
hx.py                  init · board · lock · check
```

## 흐름
합의(kickoff) → v0(step, 얇게 끝까지) → 확장(step 반복, 변경은 change) → 동결 검토(review, 새 세션) → 서술형 준비(explain).
기록은 에이전트가 쓰고 사람은 읽는다. 상태는 시간이 아니라 조건(R·C·커밋)으로 넘어간다. 검증은 만든 쪽이 아니라 verifier가 다시 센다.

## 라이선스
MIT
