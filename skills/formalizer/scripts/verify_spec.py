# -*- coding: utf-8 -*-
"""校验 模型规格.md：12 项齐全 + 对照表；组合模式查 M 链。用法: python verify_spec.py [path] [--decision <file>]"""
import sys, re
def check(path):
    txt = open(path, encoding="utf-8").read()
    sections = ["模型目标","模型假设","符号定义","参数定义","决策变量","状态变量",
                "核心数学关系","目标函数","约束条件","子模型关系","适用范围","模型风险"]
    missing = [s for s in sections if s not in txt]
    if "现实" not in txt or "数学表达" not in txt: missing.append("现实→数学对照表")
    if "--decision" in sys.argv:
        d = open(sys.argv[sys.argv.index("--decision")+1], encoding="utf-8").read()
        m_lines = re.findall(r"^M\d+[：:](.+)$", d, re.M)
        if m_lines:
            if "模型链总览" not in txt: missing.append("模型链总览")
            if "模型链数据流" not in txt: missing.append("模型链数据流")
    return missing
def main():
    path = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "E:/26数模国赛/流程产物/正式模型.md"
    missing = check(path)
    if missing: print("FAIL: 缺", missing); sys.exit(1)
    print("PASS: 12 项 + 对照表齐全" + (" + 模型链" if "--decision" in sys.argv else "")); sys.exit(0)
if __name__ == "__main__":
    main()
