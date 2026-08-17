# -*- coding: utf-8 -*-
"""校验 model_review.md：14 维 + 定性矩阵 + 换皮/互补 + 无越权措辞。用法: python verify_model_review.py [path]"""
import re
import sys

DIMS = ["Requirement 覆盖", "题目本质", "数据结构匹配", "假设", "结构性错误",
        "Baseline", "可解释", "可验证", "数据需求", "计算复杂度",
        "最大失败风险", "失效边界", "互补", "高级但没必要"]
SECTIONS = ["换皮检查", "比较矩阵", "互补关系", "风险与适用条件", "留给人工关卡"]
# 越权措辞（选模权在人工，model_review.md 中禁止出现）
FORBIDDEN = [
    (r"MAIN\s*[=＝:：]", "出现 MAIN 指定"),
    (r"BACKUP\s*[=＝:：]", "出现 BACKUP 指定"),
    (r"最终建议采用", "出现最终采用结论"),
    (r"(推荐|建议)(选择|采用|使用)方案", "出现推荐选型结论"),
    (r"总分\s*[:：=＝]", "出现总分"),
    (r"综合得分|加权总分|排名第[一二三四五六\d]", "出现打分排名"),
]

def check(path):
    txt = open(path, encoding="utf-8").read()
    missing = []
    for f in ["type:", "stage:", "owner:", "status:", "upstream:", "downstream:"]:
        if f not in txt:
            missing.append(f"YAML 缺字段「{f}」")
    if "owner: kimi" not in txt:
        missing.append("YAML owner 应为 kimi")
    for s in SECTIONS:
        if s not in txt:
            missing.append(f"缺章节「{s}」")
    for d in DIMS:
        if d not in txt:
            missing.append(f"14 维缺「{d}」")
    if "证据" not in txt and "出处" not in txt and "[[problem_spec" not in txt:
        missing.append("矩阵未见证据标注（证据/出处/wikilink）")
    if re.search(r"\|\s*\|\s*\|", txt):
        missing.append("比较矩阵存在空白单元格，疑似未填写")
    if "高" not in txt or "中" not in txt or "低" not in txt:
        missing.append("比较矩阵未见 高/中/低 定性分级")
    for pat, msg in FORBIDDEN:
        if re.search(pat, txt):
            missing.append(f"越权措辞：{msg}")
    return missing

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "results/model_review.md"
    missing = check(path)
    if missing:
        print(f"FAIL: {len(missing)} 处缺失/违规"); [print("  " + m) for m in missing]; sys.exit(1)
    print("PASS: 协议、14 维、定性矩阵、换皮/互补在位，无越权措辞"); sys.exit(0)

if __name__ == "__main__":
    main()
