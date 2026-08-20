# -*- coding: utf-8 -*-
"""校验 数据概况.md：12 节齐全 + 观察单位发现 + 无 target 误判 + 血缘日志。"""
import sys, re
txt = open("E:/26数模国赛/流程产物/数据概况.md", encoding="utf-8").read()
need = ["1. 数据表/文件说明","2. 行代表什么","3. 列语义表","4. 样本量与层级","5. 观察单位发现",
        "6. 血缘日志","7. 数据类型说明","8. 缺失与空白语义","9. 重复与多层观测","10. 时间结构",
        "11. 分布与相关","12. 冲突告警"]
missing = [h for h in need if h not in txt]
# 观察单位发现必须有组合键审计结果
if "组合键" not in txt: missing.append("组合键审计")
# 冲突告警必须有 target 语义或待确认说明（不得直接宣布 target）
if "冲突告警" in txt and ("STOP" not in txt) and "待确认" not in txt: missing.append("冲突告警无 STOP 或待确认")
if missing: print("FAIL:", missing); sys.exit(1)
print("PASS: 12 节齐全 + 观察单位发现 + 冲突告警语义正确"); sys.exit(0)
