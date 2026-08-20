# -*- coding: utf-8 -*-
"""校验 data_profile.md：固定 12 项齐全 + 文中引用的图存在。"""
import os, sys, re
txt = open("E:/26数模国赛/流程产物/data_profile.md", encoding="utf-8").read()
need = ["1. 数据表/文件说明","2. 行代表什么","3. 列代表什么","4. 样本量","5. 数据类型",
        "6. 缺失值","7. 重复记录/重复测量","8. 时间结构","9. 层级结构","10. 异常值",
        "11. 分布特征","12. 变量之间的初步关系"]
missing = [h for h in need if h not in txt]
figs = re.findall(r"data_\S+\.png", txt)
missing_figs = [f for f in figs if not os.path.exists("results/figures/" + f)]
if missing or missing_figs:
    print("FAIL: 缺项", missing, "缺图", missing_figs); sys.exit(1)
print(f"PASS: 12 项齐全 + {len(figs)} 图齐全"); sys.exit(0)
