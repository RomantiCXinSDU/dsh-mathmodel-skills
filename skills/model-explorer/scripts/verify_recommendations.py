# -*- coding: utf-8 -*-
"""校验 recommendations.md：三派齐全、候选总数 6-9、无越权推荐。"""
import sys, re
txt = open(sys.argv[1] if len(sys.argv) > 1 else "results/recommendations.md", encoding="utf-8").read()
issues = []
for s in ["A 统计/概率派", "B 机理/优化派", "C 数据驱动/混合派"]:
    if s not in txt: issues.append("缺派别 " + s)
n_cand = len(re.findall(r"^- ([ABC]\d):", txt, re.M))
if not (6 <= n_cand <= 9): issues.append(f"候选数 {n_cand} 不在 6-9")
for b in ["MAIN","BACKUP","最终推荐","首选"]:
    if b in txt: issues.append("越权语「" + b + "」")
if "数据事实" not in txt: issues.append("缺数据事实")
if issues: print("FAIL:", issues); sys.exit(1)
print(f"PASS: 三派齐全，{n_cand} 个候选，无越权"); sys.exit(0)
