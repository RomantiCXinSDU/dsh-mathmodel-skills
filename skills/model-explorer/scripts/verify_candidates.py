# -*- coding: utf-8 -*-
"""校验 candidates.md：6-9 个候选、每候选 17 点齐全 + Baseline 对照、无越权推荐语。"""
import sys, re
txt = open(sys.argv[1] if len(sys.argv) > 1 else "results/candidates.md", encoding="utf-8").read()
cands = re.findall(r"^## ([ABC]\d)", txt, re.M)
banned = ["MAIN","BACKUP","最终推荐","推荐 A","推荐B","推荐C","首选方案","综合来看"]
issues = []
if not (6 <= len(cands) <= 9): issues.append(f"候选数 {len(cands)} 不在 6-9")
for c in cands:
    start = txt.find("## " + c)
    if start < 0: issues.append(c + " 缺标题"); continue
    nxt = re.search(r"^## ", txt[start+3:], re.M)
    seg = txt[start:(start+3+nxt.start())] if nxt else txt[start:]
    for n in range(1, 18):
        if f"\n{n}. " not in seg and not seg.startswith(f"{n}. "): issues.append(c + f" 缺第{n}点")
    if "Baseline 对照" not in seg: issues.append(c + " 缺 Baseline 对照")
for b in banned:
    if b in txt: issues.append("越权推荐语「" + b + "」")
if issues: print("FAIL:", issues[:10]); sys.exit(1)
print(f"PASS: {len(cands)} 个候选（6-9），17 项 + Baseline 齐全，无越权"); sys.exit(0)
