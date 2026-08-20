# -*- coding: utf-8 -*-
"""校验 数据规则.md：规则 1-15 + Group Split + 有效独立样本 + 充分性节。"""
import sys
txt = open("E:/26数模国赛/流程产物/数据规则.md", encoding="utf-8").read()
missing = [i for i in range(1, 16) if f"## 规则 {i} " not in txt]
if "Group Split" not in txt: missing.append("Group Split")
if "有效独立样本" not in txt: missing.append("有效独立样本")
if "数据充分性检查" not in txt: missing.append("充分性节")
if "Target 绑定" not in txt: missing.append("Target绑定Requirement")
if missing: print("FAIL:", missing); sys.exit(1)
print("PASS: 规则 1-15 + Group Split + 有效独立样本 + Target绑定 + 充分性节"); sys.exit(0)
