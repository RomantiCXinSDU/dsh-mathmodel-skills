# -*- coding: utf-8 -*-
"""校验 data_rules.md：规则 1-18 齐全 + 充分性节 + 依据非空 + ≥12 条有数字。"""
import sys, re
txt = open("results/data_rules.md", encoding="utf-8").read()
missing = [i for i in range(1, 19) if f"## 规则 {i} " not in txt]
if "数据充分性检查" not in txt: missing.append("充分性节")
basis = []
for i in range(1, 19):
    start = txt.find(f"## 规则 {i} ")
    if start < 0: basis.append(""); continue
    end = txt.find(f"## 规则 {i+1} ", start + 1)
    seg = txt[start:end if end > 0 else len(txt)]
    m = re.search(r"- 依据：([^\n]*)", seg)
    basis.append(m.group(1).strip() if m else "")
empty = [i + 1 for i, b in enumerate(basis) if not b]
digits = sum(1 for b in basis if re.search(r"\d", b))
if missing: print("FAIL: 缺", missing); sys.exit(1)
if empty: print("FAIL: 依据为空", empty); sys.exit(1)
if digits < 12: print(f"FAIL: 数字依据仅 {digits}/18（需≥12）"); sys.exit(1)
print(f"PASS: 18 条规则 + 充分性节齐全，{digits}/18 有数字依据"); sys.exit(0)
