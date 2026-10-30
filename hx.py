#!/usr/bin/env python3
"""hx.py — 하네스 도구 하나. init(설치) · board(현황판) · lock(장부 잠금) · check(제출 전 점검).
표준 라이브러리만 쓴다. 과제 루트에서 `python ~/hx/hx.py <명령>` 으로 실행한다."""
import hashlib, json, re, shutil, subprocess, sys
from datetime import datetime
from pathlib import Path
try:  # 출력이 파이프로 잘려도 조용히 끝나게 (리눅스/맥). 윈도우엔 SIGPIPE가 없어 건너뜀
    import signal; signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except Exception:
    pass

HX = Path(__file__).resolve().parent          # 하네스 저장소(~/hx)
CWD = Path.cwd()                              # 과제 루트
STATE = CWD / ".hx"                           # 도구 상태(해시·잠금). 제출물 아님
ROOT_DOCS = ["README.md", "AGENTS.md", "PLAN.md", "WORKLOG.md", "DECISIONS.md"]
README_HEADS = ["한 줄 요약", "바로 실행", "결과 미리보기", "구조도", "이렇게 만들었다", "왜 이렇게 했나", "확인 방법", "안 한 것", "파일 지도"]


def sh(cmd, timeout=120):
    """셸 명령을 돌리고 (종료코드, 출력)을 돌려준다. 실패해도 예외를 내지 않는다."""
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
        return p.returncode, (p.stdout + p.stderr).strip()
    except Exception as e:
        return 99, str(e)


def read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def file_hash(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


DATA_EXT = {".csv", ".tsv", ".xlsx", ".xls", ".json", ".jsonl", ".parquet", ".txt", ".xml", ".db", ".sqlite"}
SKIP_DIRS = {".git", ".hx", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".practice", "out", "verify", "src", "tests", "configs", ".agents", ".codex"}

def raw_hashes():
    """원본 데이터 해시: data/ 아래 전부(DATA_CARD 제외) + 그 밖의 폴더에 있는 데이터 확장자 파일. 원본 불변 확인용.
    경로는 항상 / 로 적는다(Windows에서 잠근 해시를 리눅스에서 비교해도 맞게)."""
    out = {}
    for f in sorted(CWD.rglob("*")):
        if not f.is_file() or any(p in SKIP_DIRS for p in f.relative_to(CWD).parts[:-1]): continue
        rel = f.relative_to(CWD)
        if rel.parts and rel.parts[0] == "data":
            if f.name != "DATA_CARD.md": out[rel.as_posix()] = file_hash(f)
        elif f.suffix.lower() in DATA_EXT and f.name not in ("requirements.txt",):
            out[rel.as_posix()] = file_hash(f)
    return out


def rows(text, pattern):
    """마크다운 표에서 첫 칸이 패턴에 맞는 행들을 칸 목록으로."""
    out = []
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and re.match(pattern, cells[0]):
                out.append(cells)
    return out


def hxcmd():
    """이 환경에서 hx.py를 부르는 실제 명령 (python 이름 + 절대 경로). 문서의 HXCMD 자리에 넣는다."""
    py = "python3" if Path(sys.executable).name.startswith("python3") else "python"
    return f"{py} {HX / 'hx.py'}"


def write_sub(src, dst):
    """틀 파일을 복사하며 HXCMD를 실제 명령으로 바꾼다."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(read(src).replace("HXCMD", hxcmd()), encoding="utf-8")


def copy_if_absent(src, dst, made, kept, label=None):
    """없을 때만 복사한다. 있던 파일은 덮지 않는다."""
    label = label or dst.name
    if dst.exists():
        kept.append(label); return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst)
        for f in dst.rglob("*.md"): f.write_text(read(f).replace("HXCMD", hxcmd()), encoding="utf-8")
    else: write_sub(src, dst)
    made.append(label)


# ---------------- init ----------------
def cmd_init(args):
    """하네스 파일을 과제 루트에 복사한다. 있는 파일은 덮지 않는다."""
    if HX == CWD:
        print("멈춤: 지금 폴더가 하네스 저장소 자체입니다. 과제 루트로 이동한 뒤 실행하세요."); sys.exit(1)
    if CWD in HX.parents:
        print(f"멈춤: 하네스가 과제 폴더 안({HX})에 받아졌습니다. 밖으로 옮기세요: mv {HX} ~/hx  → 그 뒤 과제 루트에서 python ~/hx/hx.py init"); sys.exit(1)
    start = args[0] if args else datetime.now().strftime("%H:%M")
    made, kept = [], []
    copy_if_absent(HX / "AGENTS.md", CWD / "AGENTS.md", made, kept)
    rd = CWD / "README.md"
    if rd.exists():
        if "## 바로 실행" not in read(rd):
            rd.write_text(read(rd).rstrip("\n") + "\n\n---\n\n" + read(HX / "templates" / "README.md"), encoding="utf-8"); made.append("README.md(제출 절 덧붙임)")
        else: kept.append("README.md")
    else:
        write_sub(HX / "templates" / "README.md", rd); made.append("README.md")
    for name in ["PLAN.md", "WORKLOG.md", "DECISIONS.md"]:
        dst = CWD / name
        if dst.exists(): kept.append(name); continue
        dst.write_text(read(HX / "templates" / name).replace("__START__", start).replace("HXCMD", hxcmd()), encoding="utf-8"); made.append(name)
    copy_if_absent(HX / ".agents" / "skills", CWD / ".agents" / "skills", made, kept, ".agents/skills(5)")
    copy_if_absent(HX / ".codex" / "agents" / "verifier.toml", CWD / ".codex" / "agents" / "verifier.toml", made, kept, ".codex/agents/verifier.toml")
    copy_if_absent(HX / "verify" / "RULES.md", CWD / "verify" / "RULES.md", made, kept, "verify/RULES.md")
    copy_if_absent(HX / "verify" / "AGENTS.md", CWD / "verify" / "AGENTS.md", made, kept, "verify/AGENTS.md")
    copy_if_absent(HX / "templates" / "verify_report.md", CWD / "verify" / "report.md", made, kept, "verify/report.md")
    copy_if_absent(HX / "templates" / "DATA_CARD.md", CWD / "data" / "DATA_CARD.md", made, kept, "data/DATA_CARD.md")
    for d in ["src", "tests", "configs", "data/raw", "data/incoming", "out/latest"]:
        (CWD / d).mkdir(parents=True, exist_ok=True)
    STATE.mkdir(exist_ok=True)
    (STATE / "start.json").write_text(json.dumps({"start": start, "date": datetime.now().strftime("%Y-%m-%d")}), encoding="utf-8")
    (STATE / "raw_hashes.json").write_text(json.dumps(raw_hashes(), indent=1), encoding="utf-8")
    gi = CWD / ".gitignore"; g = read(gi)
    if ".hx/" not in g:
        # verify/ 는 보고서·검증자 규칙·own_*.py 만 커밋한다. 스크린샷·응답 JSON·브라우저 프로필 같은 산출물은 제외 (m4: 59개 파일이 커밋됨)
        g += ("" if not g or g.endswith("\n") else "\n") + ".hx/\n__pycache__/\n.pytest_cache/\n.venv/\ntests/.browser*/\n"
        g += "verify/*\n!verify/report.md\n!verify/RULES.md\n!verify/AGENTS.md\n!verify/own_*.py\n!verify/own_*.cjs\n"
        gi.write_text(g, encoding="utf-8")
    if not (CWD / ".git").exists(): sh("git init -q")
    if sh("git config user.name")[1].strip() == "": sh('git config user.name "codex" && git config user.email "codex@local"')
    sh("git add -A"); code, out = sh('git commit -q -m "setup: 하네스 설치 | verify: 루트 문서, 원본 해시 저장"')
    print(f"만듦: {', '.join(made) or '없음'}")
    print("setup 커밋: " + ("완료" if code == 0 else "실패 → " + out.splitlines()[-1][:80] if out else "실패"))
    if kept: print(f"있어서 둠: {', '.join(kept)}")
    print(f"시작 {start} · 원본 데이터 {len(raw_hashes())}개 해시 저장")
    print("다음: Codex 껐다 켜기(/exit → codex) → /status(Agents.md 줄·한도) → /skills → '규칙 3줄 요약' → 'verifier로 README 첫 줄 읽어 봐' → 과제 README 읽고 합의")


# ---------------- board ----------------
def elapsed_min():
    s = json.loads(read(STATE / "start.json") or "{}")
    if not s: return None
    t0 = datetime.strptime(s["date"] + " " + s["start"], "%Y-%m-%d %H:%M")
    return max(0, int((datetime.now() - t0).total_seconds() // 60))


def state_from_git():
    """git log의 마지막 국면 커밋으로 상태를 읽는다."""
    _, log = sh("git log --oneline -50")
    for line in log.splitlines():
        m = re.match(r"\w+\s+(freeze|step\d+|agree|setup)\b", line)
        if m:
            k = m.group(1)
            return {"setup": "설치됨", "agree": "합의됨"}.get(k, "동결됨" if k == "freeze" else ("v0 됨" if k == "step1" else "요구 채우는 중"))
    return "시작 전"


def cmd_board(_):
    """터미널 현황판을 보여 주고 PLAN 현황판을 갱신한다."""
    m = elapsed_min()
    plan = read(CWD / "PLAN.md")
    R = rows(plan, r"^R\d+"); C = rows(plan, r"^C\d+")
    st = {k: sum(1 for r in R if len(r) > 5 and k in r[5]) for k in ["✅", "⏳", "⬜", "❌", "변경됨"]}
    cst = {k: sum(1 for c in C if len(c) > 3 and k in c[3]) for k in ["미확정", "확인됨", "가정", "변경됨", "무시함"]}
    cards = [l.strip("# ").strip() for l in read(CWD / "DECISIONS.md").splitlines() if re.match(r"^### D\d+", l)]
    wl = [l for l in read(CWD / "WORKLOG.md").splitlines() if l.startswith("## ") and "형식" not in l][-3:]
    _, log = sh("git log --oneline -3")
    state = state_from_git()
    nxt = re.search(r"- 다음: (.*)", plan)
    rep = read(CWD / "verify" / "report.md").splitlines()[:1]
    print("=" * 64)
    print(f"경과 {m if m is not None else '?'}/180분 · 상태 {state} · 다음: {nxt.group(1).strip() if nxt else '-'}")
    print(f"검증표 R{len(R)}: ✅{st['✅']} ⏳{st['⏳']} ⬜{st['⬜']} ❌{st['❌']} 변경됨{st['변경됨']}   조건 C{len(C)}: 미확정{cst['미확정']} 확인됨{cst['확인됨']} 가정{cst['가정']}")
    print(f"결정 카드 {len(cards)}개: " + (" / ".join(c[:26] for c in cards) if cards else "없음"))
    print("verifier: " + (rep[0][:90] if rep else "없음"))
    print("커밋:\n  " + log.replace("\n", "\n  "))
    print("WORKLOG:\n  " + ("\n  ".join(wl) if wl else "없음"))
    print("=" * 64)
    fill_worklog_commits()
    if plan and m is not None:
        new = re.sub(r"- 시작: (.+?) · 경과: .+?분 · 상태: .*", lambda mm: f"- 시작: {mm.group(1)} · 경과: {m}/180분 · 상태: {state}", plan, count=1)
        new = re.sub(r"- 막힌 것: (.*?) · 결정 카드: \d+개", lambda mm: f"- 막힌 것: {mm.group(1)} · 결정 카드: {len(cards)}개", new, count=1)
        if new != plan: (CWD / "PLAN.md").write_text(new, encoding="utf-8")


def fill_worklog_commits():
    """WORKLOG 블록(## stepN · 시각) 아래 꼬리표 `(D번호 · )`의 빈 커밋 자리를 git log에서 채운다."""
    w = CWD / "WORKLOG.md"; txt = read(w)
    if not txt: return
    _, log = sh("git log --oneline -80")
    hashes = {}
    for line in log.splitlines():
        mm = re.match(r"(\w+)\s+(setup|agree|freeze|explain|verify|step\d+)\b", line)
        if mm and mm.group(2) not in hashes: hashes[mm.group(2)] = mm.group(1)
    out, changed, cur = [], False, None
    for line in txt.splitlines():
        mm = re.match(r"^## (setup|agree|freeze|explain|verify|step\d+)\b", line)
        if mm: cur = mm.group(1)
        tail = re.match(r"^\((.*?)·\s*\)\s*$", line.strip())
        if tail and cur in hashes:
            line = f"({tail.group(1).strip()} · {hashes[cur]})"; changed = True
        out.append(line)
    if changed: w.write_text("\n".join(out) + "\n", encoding="utf-8")


# ---------------- lock ----------------
def cmd_lock(_):
    """합의 시점의 R·C 행을 잠근다. 이후 행이 사라지면 check가 경고한다."""
    plan = read(CWD / "PLAN.md")
    R = [r[0] for r in rows(plan, r"^R\d+")]; C = [c[0] for c in rows(plan, r"^C\d+")]
    STATE.mkdir(exist_ok=True)
    (STATE / "rows.json").write_text(json.dumps({"R": R, "C": C}), encoding="utf-8")
    (STATE / "raw_hashes.json").write_text(json.dumps(raw_hashes(), indent=1), encoding="utf-8")
    print(f"잠금: {R} · {C} · data/raw {len(raw_hashes())}개 해시")
    if len(R) < 3: print("경고: R이 3개 미만 — 합의가 덜 됐을 수 있음")
    und = [c[0] for c in rows(plan, r"^C\d+") if len(c) > 3 and "미확정" in c[3]]
    if und: print("경고: 미확정 C가 남음 → 가정으로 돌리고 넘어갈 것: " + ", ".join(und))


# ---------------- check ----------------
def cmd_check(args):
    """제출 전 점검. 종료코드 0 통과 / 1 문제 / 2 검사한 게 0건."""
    run = "--run" in args
    bad, warn, zero = [], [], False
    # 1 원본 불변 — 잠근 뒤 바뀌거나 사라진 파일만 문제. 새로 생긴 파일(담당자 추가 파일)은 경고 (m4: CVD 접수 뒤 check 가 실패했던 원인)
    saved = json.loads(read(STATE / "raw_hashes.json") or "{}"); now = raw_hashes()
    if saved:
        changed = [k for k in saved if k in now and saved[k] != now[k]]
        gone = [k for k in saved if k not in now]
        new = [k for k in now if k not in saved]
        if changed: bad.append("원본 데이터가 바뀜: " + ", ".join(changed))
        if gone: bad.append("잠근 원본이 사라짐: " + ", ".join(gone))
        if new: warn.append(f"잠근 뒤 새로 생긴 데이터 파일 {len(new)}개 (담당자 추가 파일이면 정상, DATA_CARD 에 절이 있나): " + ", ".join(new[:5]))
    # 2 테스트 — pytest 가 있으면 pytest, 없으면 표준 unittest 로 (시험 리눅스에 pytest 보장 없음)
    tdir = CWD / "tests"
    if tdir.exists() and (any(tdir.rglob("test*.py")) or any(tdir.rglob("*_test.py"))):
        _, out = sh(f"{sys.executable} -m pytest -q tests", timeout=300)
        runner = "pytest"
        if "No module named pytest" in out:
            runner = "unittest"
            _, out = sh(f"{sys.executable} -m unittest discover -s tests -p '*test*.py'", timeout=300)
        if runner == "pytest":
            mm = re.search(r"(\d+) passed", out); sk = re.search(r"(\d+) skipped", out); fa = re.search(r"(\d+) failed", out)
            passed = int(mm.group(1)) if mm else 0; failed = int(fa.group(1)) if fa else 0; skipped = int(sk.group(1)) if sk else 0
        else:
            mm = re.search(r"Ran (\d+) tests?", out); fa = re.search(r"failures=(\d+)", out); er = re.search(r"errors=(\d+)", out); sk = re.search(r"skipped=(\d+)", out)
            ran = int(mm.group(1)) if mm else 0; failed = (int(fa.group(1)) if fa else 0) + (int(er.group(1)) if er else 0); skipped = int(sk.group(1)) if sk else 0
            passed = max(0, ran - failed - skipped)
        if failed: bad.append(f"테스트 실패 {failed}개 ({runner})")
        if passed == 0: zero = True; bad.append("통과한 테스트 0개 (검사한 게 없음)")
        else: print(f"테스트 통과 {passed}개 ({runner})" + (f", skip {skipped}" if skipped else ""))
    else:
        zero = True; bad.append("tests/ 에 테스트가 없음 (검사한 게 없음)")
    # 3 결과물
    latest = CWD / "out" / "latest"
    files = [f for f in latest.rglob("*") if f.is_file()] if latest.exists() else []
    if not files: bad.append("out/latest 가 비어 있음")
    else:
        txt = "\n".join(read(f) for f in files if f.suffix in (".txt", ".md", ".csv", ".json"))
        if txt and len(re.findall(r"\d", txt)) < 5: bad.append("결과 텍스트에 숫자가 거의 없음 (전부 보류?)")
        if txt.count("보류") >= 3: warn.append(f"결과에 '보류'가 {txt.count('보류')}번")
    out_dirs = [d for d in (CWD / "out").iterdir() if d.is_dir()] if (CWD / "out").exists() else []
    extra_out = [d.name for d in out_dirs if d.name not in ("latest", "archive")]
    if extra_out: warn.append("out/ 에 latest·archive 밖의 폴더: " + ", ".join(extra_out))
    # 4 정리
    extra = [p.name for p in CWD.glob("*.md") if p.name not in ROOT_DOCS]
    if extra: warn.append("루트에 정해진 5개 밖의 md: " + ", ".join(extra))
    hashes = {}
    for f in CWD.rglob("*"):
        rel = f.relative_to(CWD).parts
        if f.is_file() and not any(x in rel for x in (".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".hx", ".practice")) \
           and rel[0] not in ("data", "verify") and not (len(rel) > 1 and rel[0] == "out" and rel[1] == "archive") and f.stat().st_size > 200:  # verify/ 증거 파일은 사본이어도 정상
            hashes.setdefault(file_hash(f), []).append(str(f.relative_to(CWD)))
    dups = [v for v in hashes.values() if len(v) > 1]
    if dups: warn.append("같은 내용 파일(사본): " + "; ".join(" = ".join(v) for v in dups[:5]))
    # 5 README
    rd = read(CWD / "README.md")
    miss = [h for h in README_HEADS if h not in rd]
    if miss: bad.append("README 제목 빠짐: " + ", ".join(miss))
    if "(결과물 이름 — 담당자의 말로)" in rd or "(누구를 위해 무엇을, 2줄)" in rd or "```\n(명령 한 줄)" in rd: bad.append("README 틀의 괄호 자리가 남아 있음")  # 틀 전용 문구만 (과제 README 본문과 충돌 방지)
    if run:
        sec = rd.split("## 바로 실행", 1)[1].split("\n## ", 1)[0] if "## 바로 실행" in rd else ""
        m = re.search(r"```[^\n]*\n(.+?)```", sec, re.S)
        if not m: warn.append("README '바로 실행'에 코드 펜스(```)로 적힌 명령이 없어 실행 확인을 못 함")
        else:
            cmd = m.group(1).strip().splitlines()[0]
            if cmd.startswith("("): pass  # 틀의 자리 표시 — 위에서 이미 '괄호 자리' 문제로 잡힘
            elif re.search(r"0\.0\.0\.0|PORT|runserver|flask run|uvicorn|serve|http\.server|npm (start|run dev)", cmd):
                warn.append(f"README 실행 명령이 서버라 자동 확인 안 함(직접 미리보기로 확인): {cmd}")
            else:
                code, out = sh(cmd, timeout=120)
                if code != 0: bad.append(f"README 실행 명령 실패(code {code}): {cmd}")
                else: print(f"README 실행 명령 성공: {cmd}")
    # 6 장부
    plan = read(CWD / "PLAN.md"); dc = read(CWD / "DECISIONS.md")
    if "○○" in dc: warn.append("DECISIONS 에 채우지 않은 ○○ 자리")
    if dc.count("### D") == 0: warn.append("결정 카드가 0개")
    R = rows(plan, r"^R\d+"); C = rows(plan, r"^C\d+")
    locked = json.loads(read(STATE / "rows.json") or "{}")
    gone = [i for i in locked.get("R", []) if i not in [r[0] for r in R]] + [i for i in locked.get("C", []) if i not in [c[0] for c in C]]
    if gone: bad.append("잠근 장부 행이 사라짐: " + ", ".join(gone))
    # verifier report
    rep = read(CWD / "verify" / "report.md")
    rep_pass = {r[0] for r in rows(rep, r"^R\d+") if len(r) > 1 and "PASS" in r[1]}
    rep_fail = [r[0] for r in rows(rep, r"^R\d+") if len(r) > 1 and "FAIL" in r[1]]
    if rep_fail: bad.append("verifier FAIL: " + ", ".join(rep_fail))
    if "아직 검증 전" in rep: warn.append("verifier가 한 번도 돌지 않음 (report.md 틀 그대로)")
    for r in R:
        if len(r) > 6 and "✅" in r[5]:
            if not r[6].strip(): bad.append(f"{r[0]} ✅인데 증거 칸이 빔")
            if r[4].strip() in ("○", "◯", "O", "o", "필요") and r[0] not in rep_pass: bad.append(f"{r[0]} verifier 필요(○)인데 report PASS 없음")
            h = re.search(r"\b(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b", r[6])
            if h:
                code, diff = sh(f"git diff --name-only {h.group(0)} -- src")  # 커밋 이후 + 아직 커밋 안 한 수정까지
                if code == 0 and diff.strip(): warn.append(f"{r[0]} 증거 커밋 {h.group(0)} 이후 src 가 바뀜 → 증거 무효, 다시 확인")
    nd = [r[0] for r in R if len(r) > 5 and any(k in r[5] for k in ("⬜", "⏳", "❌"))]
    if nd: warn.append("확인 안 된 요구: " + ", ".join(nd) + " (한계에 적었나?)")
    und = [c[0] for c in C if len(c) > 3 and "미확정" in c[3]]
    if und: bad.append("미확정 C가 남음 (가정으로 돌릴 것): " + ", ".join(und))
    norf = [c[0] for c in C if len(c) > 5 and c[3].startswith(("확인됨", "가정")) and not c[5].strip()]
    if norf: warn.append("반영 칸이 빈 C: " + ", ".join(norf))
    noimp = [c[0] for c in C if len(c) > 4 and not c[4].strip()]
    if noimp: warn.append("'영향 받는 숫자'가 빈 C: " + ", ".join(noimp))
    _, stt = sh("git status --porcelain")
    if stt.strip(): warn.append(f"커밋 안 된 변경 {len(stt.strip().splitlines())}개")
    for b in bad: print("문제 :", b)
    for w in warn: print("경고 :", w)
    if not bad and not warn: print("통과: 문제·경고 없음")
    rc = 2 if zero else (1 if bad else 0)
    print(f"종료코드 {rc}  (0 통과 / 1 문제 / 2 검사한 게 0건)")
    sys.exit(rc)


if __name__ == "__main__":
    cmds = {"init": cmd_init, "board": cmd_board, "lock": cmd_lock, "check": cmd_check}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print("사용법: python ~/hx/hx.py init [HH:MM] | board | lock | check [--run]"); sys.exit(1)
    cmds[sys.argv[1]](sys.argv[2:])
