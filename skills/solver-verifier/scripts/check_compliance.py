# -*- coding: utf-8 -*-
"""check_compliance.py —— 合规审计：AI声明、无身份信息、附录源程序说明。
用法: python check_compliance.py <paper.md>"""
import sys
txt = open(sys.argv[1], encoding="utf-8").read()
issues = []
if "AI 工具使用声明" not in txt: issues.append("缺「AI 工具使用声明」")
for bad in ["学校", "姓名", "学号", "指导教师", "赛区"]:
    if bad in txt: issues.append(f"疑似身份信息「{bad}」")
if "附录" not in txt and "源程序" not in txt: issues.append("缺附录源程序说明")
if issues:
    print("FAIL:", issues); sys.exit(1)
print("PASS: 合规审计通过"); sys.exit(0)
