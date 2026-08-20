# -*- coding: utf-8 -*-
"""校验 拆题报告.md：YAML 协议 + 必备章节 + R 编号 + 原文出处。用法: python verify_拆题报告.py [path]"""
import re
import sys

SECTIONS = ["每问拆解", "数学元素", "要求编号清单", "术语表", "陷阱与歧义", "全局变量表"]
ELEMENTS = ["已知量", "未知量", "决策变量", "状态变量", "参数", "目标", "约束"]

def check(path):
    txt = open(path, encoding="utf-8").read()
    missing = []
    # cumcm-markdown-protocol：YAML 六字段 + owner
    for f in ["type:", "stage:", "owner:", "status:", "upstream:", "downstream:"]:
        if f not in txt:
            missing.append(f"YAML 缺字段「{f}」")
    if "owner: kimi" not in txt:
        missing.append("YAML owner 应为 kimi")
    for s in SECTIONS:
        if s not in txt:
            missing.append(f"缺章节「{s}」")
    for e in ELEMENTS:
        if e not in txt:
            missing.append(f"数学元素缺「{e}」")
    if re.search(r"\|\s*\|\s*\|", txt) or "第_页" in txt:
        missing.append("存在空白表格行或占位符（如 第_页），疑似未填写")
    rs = set(re.findall(r"R\d+\.\d+", txt))
    if not rs:
        missing.append("无 R 编号（形如 R1.1）")
    else:
        m = re.search(r"要求编号清单(.*?)(\n## |\Z)", txt, re.S)
        defined = set(re.findall(r"R\d+\.\d+", m.group(1))) if m else set()
        undefined = rs - defined
        if undefined:
            missing.append(f"R 编号未在清单中定义：{sorted(undefined)}")
    if "出处" not in txt and "页" not in txt and "原文" not in txt:
        missing.append("未见原文出处标注（页码/段落），不满足可追溯")
    # 越权检查：拆题阶段不得出现具体模型推荐
    if re.search(r"(应该|建议|推荐)(使用|采用|用).{0,12}(XGBoost|GAM|GA|遗传算法|随机森林|神经网络|ARIMA|SVM)", txt):
        missing.append("疑似越权推荐具体模型（拆题阶段禁止）")
    return missing

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "../流程产物/拆题报告.md"
    missing = check(path)
    if missing:
        print(f"FAIL: {len(missing)} 处缺失/违规"); [print("  " + m) for m in missing]; sys.exit(1)
    print("PASS: 协议、章节、七类元素、R 编号、出处标注在位，无越权推荐"); sys.exit(0)

if __name__ == "__main__":
    main()
