# -*- coding: utf-8 -*-
"""data-ruler 确定性实现：任意 CSV → 数据规则.md（规则 1-18 + 充分性骨架）。"""
import pandas as pd, numpy as np, os, sys, json
TIME_HINTS = ["week","month","year","date","time","day","period","孕周","胎龄","日期","时间","周期","季度"]
def cfg_get():
    return json.load(open(sys.argv[sys.argv.index("--config")+1], encoding="utf-8")) if "--config" in sys.argv else {}
def looks_like_id(name):
    l = str(name).lower()
    return (l in ("id","pid","subject","name","animal_name") or l.startswith("id") or l.endswith("id")
            or l.endswith("name") or "编号" in str(name) or "序号" in str(name) or "姓名" in str(name))
def auto_id(df):
    for c in df.columns:
        if looks_like_id(c): return c
    for c in df.select_dtypes("number").columns:
        if df[c].dtype.kind in "iu" and df[c].nunique() >= len(df)*0.9 and df[c].isna().sum() == 0: return c
    for c in df.select_dtypes("object").columns:
        if df[c].nunique() >= len(df)*0.9 and df[c].isna().sum() == 0: return c
    return None
def auto_time(df, target):
    for c in df.select_dtypes("number").columns:
        if c == target: continue
        if any(h in str(c).lower() for h in TIME_HINTS): return c
    return None
def target_is_class(s):
    if s.dtype.kind in "iu" and s.nunique() > 20: return False
    return s.nunique() <= 20

def main():
    data = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "test/data/synthetic_nipr.csv"
    cfg = cfg_get(); df = pd.read_csv(data, na_values=["?", "", "NA", "nan"])
    if len(df) == 0: print("FAIL: 空数据"); sys.exit(1)
    id_col = cfg.get("id_col") or auto_id(df)
    time_col = cfg.get("time_col") or auto_time(df, cfg.get("target_col"))
    target = cfg.get("target_col")
    numeric = df.select_dtypes("number").columns.tolist()
    hi = [c for c in numeric if df[c].nunique() > 10]
    low = [c for c in numeric if df[c].nunique() <= 10]
    n = len(df)
    n_obj = int(df[id_col].nunique()) if id_col else n
    L = []; p = L.append
    p("---"); p("type: data-rules"); p("stage: ruling"); p("owner: deepseek"); p("status: draft")
    p("upstream:"); p('  - "[[数据概况]]"')
    p("downstream:"); p('  - "[[方法候选]]"')
    p("---"); p("")
    p("# 数据规则.md —— 数据规则（③ data-ruler 产出）"); p("")
    def rule(no, name, concl, basis, impact):
        p(f"## 规则 {no} {name}"); p(f"- 结论：{concl}"); p(f"- 依据：{basis}"); p(f"- 对建模的影响：{impact}"); p("")
    # A. 1-10
    if id_col:
        nrep = int((df.groupby(id_col).size() > 1).sum())
        rule(1, "样本独立性", (f"同一 {id_col} 多条记录，观测不独立" if nrep else f"{id_col} 唯一，观测独立"),
             f"{nrep} 个 {id_col} 有 ≥2 条记录", "若重复须先聚合或加随机效应")
    else:
        rule(1, "样本独立性", "未检测到对象标识列", "无", "若存在分组须人工指定 id_col")
    rule(2, "时间顺序", (time_col + " 为时间/顺序维度（自动检测）" if time_col else "未检测到时间列"),
         (f"{time_col} 范围 {df[time_col].min():.0f}~{df[time_col].max():.0f}" if time_col and df[time_col].notna().any() else "未指定"),
         "保留顺序 / 可用首达时间建模")
    miss = df.isna().mean(); miss_cols = [c for c in df.columns if miss[c] > 0]
    rule(3, "缺失处理", ("有缺失列：" + ", ".join(miss_cols[:4]) if miss_cols else "无缺失"),
         (f"最大缺失率 {miss.max():.0%}" if miss_cols else "0%"), "缺失处理须锁定")
    tot_out = 0
    if hi:
        qt = df[hi].quantile([.25,.75]); q1, q3 = qt.iloc[0], qt.iloc[1]; iqr = q3 - q1
        tot_out = int(((df[hi] < q1-1.5*iqr) | (df[hi] > q3+1.5*iqr)).sum().sum())
    rule(4, "异常值", f"连续列共 {tot_out} 条 IQR 离群（低基数/二值列已跳过）", f"IQR 离群 {tot_out} 条", "判断真异常 vs 真实极端值")
    strong = []
    if len(hi) > 1:
        corr = df[hi].corr()
        for i in range(len(corr.columns)):
            for j in range(i):
                v = corr.iloc[i,j]
                if abs(v) > 0.8: strong.append(f"{corr.columns[i]}-{corr.columns[j]}={v:.2f}")
    rule(5, "共线性", ("强相关对：" + ", ".join(strong)) if strong else "无强共线(|r|>0.8)",
         ("|r|>0.8 " + str(len(strong)) + " 对") if strong else "无", "共线变量不同时入回归")
    if target and target in df.columns:
        vc6 = df[target].value_counts(dropna=False)
        rule(6, "数据泄漏", target + " 是结果标签，不能当输入特征",
             (f"{target} 取值 {dict((k, int(v)) for k, v in vc6.items())}" if len(vc6) <= 15 else f"{target} 共 {len(vc6)} 个取值(连续)"),
             "建模剔除结果列")
    else:
        rule(6, "数据泄漏", "未指定目标列", "未指定", "指定 target_col 后判断")
    rule(7, "样本量", f"n={n}，连续特征 {len(hi)} 个，数值编码分类 {len(low)} 个",
         f"n={n}", "决定可接受的模型复杂度")
    if target and target in df.columns:
        s = df[target]
        if target_is_class(s):
            vc = s.value_counts(dropna=False)
            if len(vc) == 2:
                minority = vc.min() / vc.sum()
                rule(8, "类别不平衡", f"二分类，少数类占比 {minority:.0%}",
                     f"{dict((k, int(v)) for k, v in vc.items())}", "不平衡须类权重/SMOTE/调阈值，报 AUC")
            else:
                minr = vc.min() / vc.sum()
                verdict = "高度不平衡" if minr < 0.1 else "较均衡"
                rule(8, "类别不平衡", f"{len(vc)} 类，最小类占比 {minr:.0%}（{verdict}）",
                     f"共 {len(vc)} 类", "多分类注意最小类占比")
        else:
            rule(8, "目标类型", f"{target} 为连续/回归目标，不做类别平衡分析",
                 f"{target} 共 {int(s.nunique())} 个取值", "改做分布与离群分析")
    else:
        rule(8, "类别不平衡", "未指定目标列", "无", "指定 target_col 后评估")
    const_cols = [c for c in df.columns if df[c].nunique(dropna=True) <= 1]
    rule(9, "变量可用性", ("近常数列：" + ", ".join(const_cols)) if const_cols else "无近常数列",
         (str(len(const_cols)) + " 列") if const_cols else "0 列", "近常数列剔除")
    nfeat = len(hi)
    ceiling = "低复杂度(可解释模型优先)" if nfeat > 20 or n < 500 else "中等复杂度可接受"
    rule(10, "复杂度上限", f"n={n}, 连续特征 {nfeat} → {ceiling}", f"n={n}", "先可解释基线")
    # B. 11-18 nature-statistics
    rule(11, "独立样本单位", f"独立样本单位={n_obj} 个对象，**行数 {n} ≠ 独立样本量 {n_obj}**",
         f"行数 {n} vs 对象数 {n_obj}", "一切推断以对象数为有效样本量，不得用行数")
    nrep = int((df.groupby(id_col).size() > 1).sum()) if id_col else 0
    rule(12, "重复测量", ("存在 repeated measures" if nrep else "无重复测量"),
         f"{nrep} 个对象有 ≥2 条记录", "须聚合或混合效应/组内相关结构")
    rule(13, "嵌套结构", ("对象-观测两级嵌套" if id_col else "未检测到嵌套结构"),
         (f"对象标识 {id_col}" if id_col else "无"), "多级数据需多水平模型")
    rule(14, "伪重复", ("存在伪重复风险" if nrep else "无伪重复风险"),
         f"重复测量对象 {nrep} 个", "把重复测量当独立样本会低估标准误（伪重复），必须修正")
    rule(15, "组内相关", ("存在组内相关，应估计 ICC" if nrep else "无组内相关问题"),
         f"重复测量对象 {nrep} 个", "组内相关>0 时 OLS 无效，用混合效应")
    npairs = nfeat * (nfeat - 1) // 2
    rule(16, "多重比较", f"两两比较最多 {npairs} 次，须校正",
         f"{nfeat} 个连续特征", "用 Bonferroni/FDR 校正，否则假阳性膨胀")
    rule(17, "效应量与置信区间", "报告效应量(Cohen's d / OR / 相关系数)与置信区间，不只 p 值",
         "统计检验的规范要求", "p 值显著≠效应有意义，须报告效应量与 CI")
    rule(18, "相关≠因果", "相关性不得解释为因果",
         "相关分析仅描述关联", "题目问'影响/原因'时须因果方法（见 方法候选）")
    # C. 充分性骨架
    reqs = cfg.get("requirements") or []
    p("## 数据充分性检查（逐 Requirement）"); p("")
    if reqs:
        for r in reqs:
            p(f"### Requirement: {r}"); p("当前数据支持：待人工确认（是/部分/否）")
            p("已有变量：待填"); p("缺失信息：待填"); p("缺口类型：待填（变量/参数/背景知识/验证数据）")
            p("是否必须补外部数据：待确认（是/否/可选）"); p("理由：待填"); p("若不补数据：模型应该如何调整？待填"); p("")
    else:
        p("- （待拆题结果 拆题报告 提供 Requirement 清单后，逐条填写充分性）")
    p("## 锁死清单（人工确认后不得改动）"); p("1. 缺失处理方式"); p("2. 离群处理方式"); p("3. 目标列与评价指标"); p("4. 独立样本单位口径")
    open("E:/26数模国赛/流程产物/数据规则.md","w",encoding="utf-8").write("\n".join(L))
    print(f"OK 数据规则.md ({data})")
if __name__ == "__main__":
    main()
