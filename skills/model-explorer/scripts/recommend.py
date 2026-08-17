# -*- coding: utf-8 -*-
"""recommend.py —— 数据驱动候选空间种子（每派 2-3 个，共 6-9，带角色定位）。"""
import pandas as pd, numpy as np, sys, json, os
def cfg_get():
    return json.load(open(sys.argv[sys.argv.index("--config")+1], encoding="utf-8")) if "--config" in sys.argv else {}
def target_is_class(s):
    if s.dtype.kind in "iu" and s.nunique() > 20: return False
    return s.nunique() <= 20
def main():
    data = sys.argv[1]; cfg = cfg_get(); target = cfg.get("target_col")
    df = pd.read_csv(data, na_values=["?", "", "NA", "nan"])
    s = df[target]; is_class = target_is_class(s); n = len(df)
    miss = int(df.isna().sum().sum())
    hi = [c for c in df.select_dtypes("number").columns if df[c].nunique() > 10 and c != target]
    A = []; B = []; C = []
    if not is_class:
        A = [("A1","线性回归（基线层）","可解释基线：最小二乘 + 显著性"),
             ("A2","分位数回归（达标线层）","关注达标分位点而非均值"),
             ("A3","混合效应模型（结构层）","刻画重复观测的组内相关（若规则12命中）")]
        B = [("B1","机理方程（若物理关系可写）","机理层"),
             ("B2","鲁棒/随机优化（决策层）","不确定性下的最优决策")]
        C = [("C1","GAM/样条（非线性层）","可解释的非线性"),
             ("C2","随机森林（混合层）","稳健非线性 + 特征重要性")]
    elif len(s.value_counts()) == 2:
        imbalance = s.value_counts().min() / s.value_counts().sum() < 0.1
        A = [("A1","逻辑回归（基线层）","可解释概率输出"),
             ("A2","Firth/贝叶斯逻辑（小样本层）","n 小或不平衡时更稳"),
             ("A3","GLMM（结构层）","重复观测 + 二分类")]
        B = [("B1","阈值/评分规则（决策层）","误判代价最小化调阈值"),
             ("B2","评分卡 WOE/IV（业务层）","业务可解释分箱")]
        C = [("C1","决策树（可解释层）","非线性 + 可解释"),
             ("C2","随机森林/XGBoost（精度层）","稳健基线" + ("；配合类权重/SMOTE" if imbalance else "")),
             ("C3","异常检测 IsolationForest（稀少类层）","异常样本稀少时互补视角")]
    else:
        A = [("A1","多项逻辑回归（基线层）","多分类基线"),
             ("A2","Ordinal 回归（等级层）","若类别有序更规范")]
        B = [("B1","层次规则/评分卡（业务层）","分步决策可解释"),
             ("B2","组合赋权评价（评价层）","多指标综合")]
        C = [("C1","决策树（可解释层）","非线性 + 可解释"),
             ("C2","随机森林（精度层）","稳健基线"),
             ("C3","KNN/混合模型（备选层）","局部结构/混合")]
    notes = []
    if n < 500: notes.append(f"n={n} 小样本 → 基线优先")
    if miss > 0: notes.append(f"缺失 {miss} 个 → 先定填补策略")
    L = ["---", "type: candidates", "stage: exploration", "owner: deepseek", "status: draft",
         "upstream:", '  - "[[data_rules]]"', '  - "[[method_candidates]]"', "downstream:", '  - "[[decision_log]]"', "---", "",
         "# recommendations.md —— 候选模型空间（数据驱动种子）", ""]
    L.append(f"## 数据事实（{data}）")
    L.append(f"- 目标 {target} 为{'分类' if is_class else '回归'}型；n={n}")
    for x in notes: L.append("- " + x)
    L.append(""); L.append("## 候选模型空间（每派 2-3 个，共 6-9 个）")
    for school, items in [("A 统计/概率派", A), ("B 机理/优化派", B), ("C 数据驱动/混合派", C)]:
        L.append(f"### {school}")
        for code, name, role in items:
            L.append(f"- {code}: {name} —— 角色：{role}")
    L.append(""); L.append("## 使用纪律")
    L.append("- 本文件是候选空间的种子；完整 17 项 Model Card 由发散手补全；")
    L.append("- 禁止从中直接确定主方案、备选方案或最终唯一推荐（选模是人工职责）。")
    out = sys.argv[sys.argv.index("--out")+1] if "--out" in sys.argv else "results/recommendations.md"
    open(out, "w", encoding="utf-8").write("\n".join(L))
    print(f"OK {out} ({len(A)}A/{len(B)}B/{len(C)}C)")
if __name__ == "__main__":
    main()
