# -*- coding: utf-8 -*-
"""pipeline.py —— 确定性状态机：阶段推进 + 返工上限(默认2) + 冻结门禁。
用法:
  python pipeline.py init|status|advance <stage>|approve <stage>|rework <stage>|freeze
"""
import json, sys, os
STAGES = ["理解问题", "模型发散", "模型筛选", "反方攻击", "正式建模", "终审", "冻结"]
MAX_REWORK = 2
PATH = "results/pipeline.json"
def fresh():
    return {"stages": {s: {"status": "pending", "rework": 0} for s in STAGES},
            "frozen": False, "current": STAGES[0]}
def load():
    return json.load(open(PATH, encoding="utf-8")) if os.path.exists(PATH) else fresh()
def save(st): json.dump(st, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
def show(st):
    print("current:", st["current"], "| frozen:", st["frozen"])
    for s, v in st["stages"].items():
        print(f"  {s}: {v['status']} (rework {v['rework']})")
def main():
    args = sys.argv[1:]
    if not args or args[0] == "init":
        save(fresh()); print("init done"); return
    st = load()
    cmd = args[0]
    if cmd == "status": show(st); return
    if cmd == "freeze":
        if all(v["status"] == "approved" for s, v in st["stages"].items() if s != "冻结"):
            st["frozen"] = True; st["stages"]["冻结"]["status"] = "approved"; save(st); print("FROZEN"); sys.exit(0)
        print("FAIL: 尚有阶段未 approved，不可冻结"); sys.exit(1)
    stage = args[1] if len(args) > 1 else st["current"]
    if stage not in st["stages"]:
        print(f"未知阶段 {stage}"); sys.exit(2)
    v = st["stages"][stage]
    if cmd == "advance":
        v["status"] = "pending_review"; save(st); print(f"{stage} → pending_review")
    elif cmd == "approve":
        if v["status"] != "pending_review": print(f"FAIL: {stage} 未处于待审"); sys.exit(1)
        v["status"] = "approved"
        idx = STAGES.index(stage)
        if idx + 1 < len(STAGES) - 1:
            st["current"] = STAGES[idx+1]; st["stages"][st["current"]]["status"] = "in_progress"
        save(st); print(f"{stage} approved → {st['current']}")
    elif cmd == "rework":
        v["rework"] += 1
        if v["rework"] > MAX_REWORK:
            v["status"] = "blocked"; save(st); print(f"FAIL: {stage} 返工超过 {MAX_REWORK} 次，blocked（应启用备选方案）"); sys.exit(1)
        v["status"] = "in_progress"; save(st); print(f"{stage} rework #{v['rework']}")
    else:
        print("未知命令"); sys.exit(2)
if __name__ == "__main__":
    main()
