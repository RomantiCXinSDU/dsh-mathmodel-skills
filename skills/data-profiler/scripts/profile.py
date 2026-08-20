# -*- coding: utf-8 -*-
"""data-profiler 确定性实现：任意 CSV → data_profile.md（固定 12 项）。"""
import pandas as pd, numpy as np, os, sys, json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei","Microsoft YaHei"]; plt.rcParams["axes.unicode_minus"] = False
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
    categorical = [c for c in df.columns if c not in numeric]
    cat_eff = categorical + low
    os.makedirs("results/figures", exist_ok=True)
    L = []; p = L.append
    p("---"); p("type: data-profile"); p("stage: profiling"); p("owner: deepseek"); p("status: draft")
    p("upstream:"); p('  - "原始数据"')
    p("downstream:"); p('  - "[[data_rules]]"')
    p("---"); p("")
    p("# data_profile.md —— 数据概况（② data-profiler 产出）"); p("")
    p("## 1. 数据表/文件说明"); p(f"- 数据文件：{data}"); p(f"- 行列规模：{len(df)} 行 × {df.shape[1]} 列"); p("")
    p("## 2. 行代表什么"); p("- 一行代表一条观测记录" + (f"；{id_col} 为对象标识（同一对象可能多行，见 §7）" if id_col else "；未检测到对象标识列") + "。"); p("")
    p("## 3. 列代表什么"); p("| 列名 | 含义(待确认则标注) | 类型 | 取值域 |"); p("|---|---|---|---|")
    for c in df.columns:
        if c in hi: p(f"| {c} | 待确认 | 数值(连续) | {df[c].min():.3g} ~ {df[c].max():.3g} |")
        elif c in low: p(f"| {c} | 待确认 | 分类(数值编码) | {','.join(map(str, df[c].dropna().unique()[:8]))} |")
        else: p(f"| {c} | 待确认 | 分类 | {','.join(map(str, df[c].dropna().unique()[:6]))} |")
    p(""); p("## 4. 样本量"); p(f"- 总行数 n={len(df)}" + (f"；独立对象数 {df[id_col].nunique()}" if id_col else "") + "。"); p("- 注意：行数 ≠ 独立样本量（重复观测时以对象数为准，详见 data_rules）。"); p("")
    p("## 5. 数据类型"); p(f"- 连续数值 {len(hi)} 个；数值编码分类 {len(low)} 个；分类/文本 {len(categorical)} 个。"); p("")
    p("## 6. 缺失值"); miss = df.isna().mean(); p("| 列 | 缺失率 |"); p("|---|---|")
    any_m = False
    for c in df.columns:
        if miss[c] > 0: p(f"| {c} | {miss[c]:.1%} |"); any_m = True
    if not any_m: p("| (无缺失) | 0% |")
    p(""); p("## 7. 重复记录/重复测量"); p(f"- 完全重复行：{int(df.duplicated().sum())}")
    if id_col: p(f"- {id_col} 中多次出现的对象数：{int((df.groupby(id_col).size() > 1).sum())}")
    p(""); p("## 8. 时间结构"); p(("- " + time_col + " 为时间/顺序维度（自动检测）" if time_col else "- 未检测到时间列（--config time_col 可指定）") + "。"); p("")
    p("## 9. 层级结构"); p(("- 检测到对象标识 " + id_col + "，可能存在对象-观测两级结构" if id_col else "- 未检测到层级/嵌套结构（若存在须 --config id_col 指定）") + "。"); p("")
    p("## 10. 异常值"); p("| 列 | IQR 离群条数 |"); p("|---|---|")
    for c in hi:
        q1, q3 = df[c].quantile([.25,.75]); iqr = q3 - q1
        n = int(((df[c] < q1-1.5*iqr) | (df[c] > q3+1.5*iqr)).sum())
        if n > 0: p(f"| {c} | {n} |")
    p(""); p("## 11. 分布特征"); p("| 列 | 偏度 | 图 |"); p("|---|---|---|")
    top = sorted(hi, key=lambda c: df[c].nunique(), reverse=True)[:3]
    for c in top:
        if df[c].notna().sum() > 0:
            sk = float(df[c].dropna().skew()); df[c].dropna().hist(bins=30); plt.title(f"{c} n={int(df[c].notna().sum())}")
            plt.savefig(f"results/figures/data_{c}.png"); plt.clf(); p(f"| {c} | {sk:.2f} | data_{c}.png |")
    p(""); p("## 12. 变量之间的初步关系"); corr = df[hi].corr() if hi else pd.DataFrame(); p("### 相关性(|r|>0.8)")
    p("| 变量对 | Pearson |"); p("|---|---|")
    for i in range(len(corr.columns)):
        for j in range(i):
            v = corr.iloc[i,j]
            if abs(v) > 0.8: p(f"| {corr.columns[i]} × {corr.columns[j]} | {v:.2f} |")
    p("### 类别分布")
    for c in cat_eff:
        if df[c].nunique() <= 15:
            vc = df[c].value_counts(dropna=False)
            p(f"- {c}：" + "，".join(f"{k}={v}" for k, v in vc.items()))
    p(""); p("## 事实清单（仅陈述，不下结论）")
    p("- 缺失列：" + (", ".join(c for c in df.columns if miss[c] > 0) or "无"))
    open("E:/26数模国赛/流程产物/data_profile.md","w",encoding="utf-8").write("\n".join(L))
    print(f"OK data_profile.md ({data})")
if __name__ == "__main__":
    main()
