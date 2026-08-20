# -*- coding: utf-8 -*
"""spec_scaffold.py —— 模型规格 骨架生成器。支持单模型 12 项；决策日志 含 M1/M2/M3 时生成组合模型链。
用法: python spec_scaffold.py --model <名> [--data <csv> --config <cfg> --decision <决策日志.md> --out <path>]"""
import sys, json, pandas as pd, re
def arg(k, d=None):
    return sys.argv[sys.argv.index(k)+1] if k in sys.argv else d
TEMPLATES = {
  "线性回归": {"eq": "y_i = b_0 + sum_k(b_k * x_ik) + e_i,  e_i ~ N(0, s^2)",
    "symbols": {"y_i": "第 i 个样本的目标值", "x_ik": "第 i 个样本的第 k 个特征", "b_k": "第 k 个特征的系数", "e_i": "随机误差项"},
    "loss": "最小二乘：min sum_i (y_i - y_hat_i)^2",
    "assumptions": ["目标与特征线性相关", "误差独立同分布", "无异方差", "无严重多重共线"]},
  "逻辑回归": {"eq": "logit(p_i) = ln(p_i / (1 - p_i)) = b_0 + sum_k(b_k * x_ik)",
    "symbols": {"p_i": "第 i 个样本为正类的概率", "x_ik": "第 i 个样本的第 k 个特征", "b_k": "第 k 个特征的系数"},
    "loss": "极大似然(交叉熵)：min -sum_i [y_i ln(p_i) + (1 - y_i) ln(1 - p_i)]",
    "assumptions": ["logit 尺度上线性可分", "样本相互独立", "无严重多重共线", "类别不平衡时须加权/调阈值"]},
  "分位数回归": {"eq": "Q_tau(y_i | x_i) = b_0(tau) + sum_k(b_k(tau) * x_ik)",
    "symbols": {"Q_tau": "tau 分位数", "x_ik": "特征", "b_k(tau)": "tau 分位下系数"},
    "loss": "min sum_i rho_tau(y_i - Q_tau(y_i | x_i))",
    "assumptions": ["关注条件分位数而非均值", "不同分位系数可不同", "样本独立"]},
  "决策树": {"eq": "递归划分：按 Gini/信息增益选最优分裂特征与阈值，叶节点输出多数类/均值",
    "symbols": {"T": "决策树", "Gini": "不纯度指标", "depth": "树深(剪枝超参)"},
    "loss": "Gini 不纯度 / 信息增益最大化",
    "assumptions": ["非线性关系可刻画", "可解释", "易过拟合，须剪枝"]},
  "随机森林": {"eq": "集成 B 棵自助采样树，分类取多数投票，回归取平均",
    "symbols": {"B": "树的数量", "m": "每次分裂随机特征数"},
    "loss": "Bagging + 特征随机化",
    "assumptions": ["非线性、交互可自动捕捉", "稳健", "可解释性弱于单棵树"]},
}
def main():
    model = arg("--model", "线性回归")
    decision = arg("--decision")
    data = arg("--data"); cfgpath = arg("--config")
    cfg = json.load(open(cfgpath, encoding="utf-8")) if cfgpath else {}
    target = cfg.get("target_col", "y")
    feats = []
    if data:
        df = pd.read_csv(data, na_values=["?", "", "NA", "nan"])
        feats = [c for c in df.columns if c != target and df[c].nunique() > 1][:8]
    L = ["---", "type: model-spec", "stage: formalization", "owner: deepseek", "status: draft",
         "upstream:", '  - "[[决策日志]]"', "downstream:", '  - "[[验证报告]]"', "---", "",
         "# 模型规格.md —— 正式模型（formalizer 产出）", ""]
    m_lines = []
    if decision:
        try:
            dtext = open(decision, encoding="utf-8").read()
            m_lines = re.findall(r"^M\d+[：:](.+)$", dtext, re.M)
        except Exception:
            pass
    if m_lines:
        L.append("## 模型链总览（来源：决策日志，唯一决策）")
        for i, ml in enumerate(m_lines, 1):
            L.append(f"- M{i}：{ml.strip()}")
        L.append("")
        for i, ml in enumerate(m_lines, 1):
            L.append(f"## M{i}（组件 {i}）")
            L.append(f"- 构成（人工决定）：{ml.strip()}")
            L.append("- 定义：待填（严格按上行的构成形式化，禁止增删模型）")
            L.append("- 输出：" + ("模型链最终输出" if i == len(m_lines) else f"供 M{i+1} 使用的输出"))
            L.append("- 使用上游输出：" + ("无（模型链起点）" if i == 1 else f"M{i-1} 的输出"))
            L.append("")
        L.append("## 模型链数据流")
        for i in range(len(m_lines)):
            if i < len(m_lines) - 1:
                L.append(f"- M{i+1} 输出 → M{i+2} 输入")
            else:
                L.append(f"- M{i+1} 输出 → 最终结果")
        L.append("")
        L.append("## 12 项规格（每个 M 组件分别补全）")
        L.append("1 模型目标 / 2 模型假设 / 3 符号定义 / 4 参数定义 / 5 决策变量 / 6 状态变量 / 7 核心数学关系 / 8 目标函数 / 9 约束条件 / 10 子模型关系 / 11 适用范围 / 12 模型风险（每个 M 组件分别补全）")
        L.append("")
        L.append("## 现实→数学对照表")
        L.append("| 现实条件(题目原文) | R | 数学表达 | 符号 |"); L.append("|---|---|---|---|")
        L.append("| 待填 | R? | 待填 | 待填 |")
    else:
        tpl = TEMPLATES.get(model) or {"eq": "待定", "symbols": {"y": "目标变量", "x": "特征向量"}, "loss": "待定", "assumptions": ["待定"]}
        L.append("## 1. 模型目标")
        L.append(f"- 用「{model}」对目标 {target} 建模（对应 R 编号：待填）。"); L.append("")
        L.append("## 2. 模型假设"); L.append("| # | 假设 | 现实依据 | 若违背的后果 |"); L.append("|---|---|---|---|")
        for i, a in enumerate(tpl["assumptions"], 1): L.append(f"| {i} | {a} | 待填 | 待填 |")
        L.append("")
        L.append("## 3. 符号定义"); L.append("| 符号 | 含义 | 单位/取值 |"); L.append("|---|---|---|")
        for sym, desc in tpl["symbols"].items(): L.append(f"| $" + sym + "$ | {desc} | 待填 |")
        L.append("")
        L.append("## 4. 参数定义"); L.append("| 参数 | 含义 | 来源 |"); L.append("|---|---|---|")
        L.append("| 模型参数 | 由数据估计 | 数据拟合 |"); L.append("")
        L.append("## 5. 决策变量"); L.append("| 变量 | 含义 |"); L.append("|---|---|"); L.append("| (本题无决策变量 / 待填) | |"); L.append("")
        L.append("## 6. 状态变量"); L.append("| 变量 | 含义 |"); L.append("|---|---|"); L.append("| (待填) | |"); L.append("")
        L.append("## 7. 核心数学关系"); L.append("$$ " + tpl["eq"] + " $$")
        if feats: L.append(f"- 可选特征：{', '.join(feats)}")
        L.append("")
        L.append("## 8. 目标函数"); L.append("- " + tpl["loss"]); L.append("")
        L.append("## 9. 约束条件"); L.append("| # | 约束 | 对应现实条件 | R |"); L.append("|---|---|---|---|"); L.append("| 1 | 待填 | 待填 | 待填 |"); L.append("")
        L.append("## 10. 子模型关系"); L.append("- 待填（多子模型时描述数据流）"); L.append("")
        L.append("## 11. 适用范围"); L.append("- 待填"); L.append("")
        L.append("## 12. 模型风险"); L.append("- 待填"); L.append("")
        L.append("## 现实→数学对照表"); L.append("| 现实条件(题目原文) | R | 数学表达 | 符号 |"); L.append("|---|---|---|---|"); L.append("| 待填 | R? | 待填 | 待填 |")
    out = arg("--out", "E:/26数模国赛/流程产物/正式模型.md")
    open(out, "w", encoding="utf-8").write("\n".join(L))
    print(f"OK {out} (" + ("组合链" if m_lines else "单模型") + "模式)")
if __name__ == "__main__":
    main()