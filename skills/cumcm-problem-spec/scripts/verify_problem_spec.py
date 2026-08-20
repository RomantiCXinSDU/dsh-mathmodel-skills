# -*- coding: utf-8 -*-
"""校验 拆题报告.md：YAML 协议 + 必备章节 + R 编号 + 原文出处 + 五类越界机械拦截。
用法: python verify_problem_spec.py [path]
"""
import re
import sys

SECTIONS = ["每问拆解", "数学元素", "要求编号清单", "术语表", "陷阱与歧义", "全局符号表"]
ELEMENTS = ["已知量", "待求量", "响应变量", "待解释变量", "待优化量", "待确定规则", "目标", "约束"]

# 五类越界机械拦截（对应 GPT 评审五条罪状）
METHOD_NAMES = r"(回归|聚类|贝叶斯|马尔可夫|XGBoost|LightGBM|GAM|随机森林|神经网络|深度学习|ARIMA|SVM|支持向量|遗传算法|粒子群|模拟退火|决策树|逻辑斯蒂|LSTM|Transformer|蒙特卡洛|层次分析|TOPSIS|熵权|模糊综合|灰色|微分方程数值|龙格库塔)"
PATTERNS_FORBIDDEN = [
    (re.compile(METHOD_NAMES), "出现具体方法/算法名（拆题阶段禁止任何方法词）"),
    (re.compile(r"(倾向|建议|推荐)"), "出现「倾向/建议/推荐」字样（裁决项只列原文+解读+影响）"),
    (re.compile(r"\d{3,}\s*行|共\s*\d{3,}|缺失\s*\d|缺\s*\d+\s*行|重复\s*\d|出现\s*\d+\s*次|占\s*比"), "疑似数据统计痕迹（行数/缺失/重复/分布是 data-profiler 职责）"),
    (re.compile(r"决策变量|状态变量|参数标定|控制变量"), "出现预设模型结构的术语（决策变量/状态变量等，拆题只用中性角色）"),
    (re.compile(r"(doi|DOI|et al\.|Journal|Proceedings|arXiv|第\s*\d+\s*卷|参考文献.*文献)"), "疑似文献定位内容（拆题阶段禁止检索方法文献，防锚定）"),
]

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
            missing.append(f"数学元素缺中性角色「{e}」")
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
    # 五类越界拦截
    for pat, msg in PATTERNS_FORBIDDEN:
        hits = pat.findall(txt)
        if hits:
            sample = hits if isinstance(hits[0], str) else [h for h in hits]
            missing.append(f"{msg}；命中示例：{list(dict.fromkeys(sample))[:3]}")
    return missing

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "../流程产物/拆题报告.md"
    missing = check(path)
    if missing:
        print(f"FAIL: {len(missing)} 处缺失/违规")
        [print("  " + m) for m in missing]
        sys.exit(1)
    print("PASS: 协议、章节、八类中性角色、R 编号、出处标注在位；无方法名/倾向/统计/预设术语/文献痕迹")
    sys.exit(0)

if __name__ == "__main__":
    main()
