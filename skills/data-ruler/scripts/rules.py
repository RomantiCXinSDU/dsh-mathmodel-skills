# -*- coding: utf-8 -*-
"""data-ruler v3：观察单位约束 + Target绑定Requirement + Group Split + 有效独立样本量 + 空白语义。
用法: python rules.py <data.csv> [--config <cfg.json>]"""
import pandas as pd, numpy as np, os, sys, json
TIME_HINTS = ["week","month","year","date","time","day","period","孕周","胎龄","日期","时间","周期","季度"]
def cfg_get():
    return json.load(open(sys.argv[sys.argv.index("--config")+1], encoding="utf-8")) if "--config" in sys.argv else {}
def looks_like_id(name):
    l = str(name).lower()
    return (l in ("id","pid","subject","name","animal_name") or l.startswith("id") or l.endswith("id")
            or l.endswith("name") or "编号" in str(name) or "序号" in str(name) or "姓名" in str(name) or "代码" in str(name))
def auto_id(df):
    for c in df.columns:
        if looks_like_id(c): return c
    for c in df.select_dtypes("number").columns:
        if df[c].dtype.kind in "iu" and df[c].nunique() >= len(df)*0.9 and df[c].isna().sum() == 0: return c
    return None
def target_is_class(s):
    if s.dtype.kind in "iu" and s.nunique() > 20: return False
    return s.nunique() <= 20

def main():
    data = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "test/data/synthetic_nipr.csv"
    cfg = cfg_get(); df = pd.read_csv(data, na_values=["?", "", "NA", "nan"])
    if len(df) == 0: print("FAIL: 空数据"); sys.exit(1)
    id_col = cfg.get("id_col") or auto_id(df)
    event_col = cfg.get("event_col")
    target = cfg.get("target_col")
    numeric = df.select_dtypes("number").columns.tolist()
    hi = [c for c in numeric if df[c].nunique() > 10 and c != target]
    n = len(df)
    n_obj = int(df[id_col].nunique()) if id_col else n
    L = []; p = L.append
    p("# 数据规则.md —— 数据规则（③ data-ruler 产出）"); p("")
    def rule(no, name, concl, basis, impact):
        p(f"## 规则 {no} {name}"); p(f"- 结论：{concl}"); p(f"- 依据：{basis}"); p(f"- 对建模的影响：{impact}"); p("")
    # 1 观测单位与独立样本（合并层级约束）
    if id_col:
        nrep = int((df.groupby(id_col).size() > 1).sum())
        nrep2 = int((df.groupby([id_col, event_col]).size() > 1).sum()) if event_col else 0
        concl = f"同一 {id_col} 多次观测（{nrep} 个对象有多行）；"
        concl += (f"同一 {id_col}+{event_col} 有多条检测记录（{nrep2} 组）" if nrep2 else "")
        concl += f"；独立样本单位=对象（n_obj={n_obj}），**行数 {n} ≠ 独立样本量 {n_obj}**"
        basis = f"对象数 {n_obj} vs 行数 {n}；第二层重复 {nrep2} 组"
        impact = "重复测量→组内相关、伪重复；须按对象聚合/混合效应；同一事件多条记录须按事件聚合；训练测试须按对象分组划分（Group Split）"
        rule(1, "观测单位与独立样本", concl, basis, impact)
    else:
        rule(1, "观测单位与独立样本", "未检测到对象标识列", "无", "须人工指定 id_col")
    # 2 时间三套
    bio = [c for c in df.columns if ('孕周' in str(c) or '胎龄' in str(c))]
    cal = [c for c in df.columns if ('日期' in str(c) and '次' not in str(c))]
    order = [c for c in df.columns if '次' in str(c) or c == event_col]
    rule(2, "时间结构", f"三套时间分开：生物时间={bio or '无'}；日历时间={cal or '无'}；个体内顺序={order or '无'}",
         "孕周/日期/抽血次数语义不同", "建模分别处理，不得混为一个时间变量")
    # 3 缺失与空白语义
    miss = df.isna().mean(); miss_cols = [c for c in df.columns if miss[c] > 0]
    if miss_cols:
        concl = "有空白字段：" + ", ".join(miss_cols[:5]) + "（空白语义见 data_profiler §8；如'非整倍体空白=无异常'属 SEMANTIC_NORMAL，非 true missing）"
        basis = f"最大空白率 {miss.max():.0%}"
        impact = "须先判空白语义再决定填补/保留；不得默认缺失"
        rule(3, "缺失与空白语义", concl, basis, impact)
    else:
        rule(3, "缺失与空白语义", "无空白", "0%", "无")
    # 4 极端观测候选（非"异常值"）
    tot = 0
    if hi:
        qt = df[hi].quantile([.25,.75]); q1, q3 = qt.iloc[0], qt.iloc[1]; iqr = q3 - q1
        tot = int(((df[hi] < q1-1.5*iqr) | (df[hi] > q3+1.5*iqr)).sum().sum())
    rule(4, "极端观测候选", f"连续列共 {tot} 条 IQR 极端观测候选（非'异常值'；NIPT 中极端值可能是真实生物学信号，如真染色体异常）",
         f"IQR 极端候选 {tot} 条", "不得默认当异常剔除；须结合语义判断是否真实极端/记录错误/有效病例")
    # 5 共线性风险（不绝对）
    strong = []
    if len(hi) > 1:
        corr = df[hi].corr()
        for i in range(len(hi)):
            for j in range(i):
                v = corr.iloc[i,j]
                if abs(v) > 0.8: strong.append(f"{hi[i]}-{hi[j]}={v:.2f}")
    rule(5, "共线性风险", ("强相关候选：" + ", ".join(strong[:6])) if strong else "无 |r|>0.8",
         (f"|r|>0.8 {len(strong)} 对") if strong else "无",
         "仅凭 r 不禁止同时入模；须看 VIF、模型目的、正则化、参数稳定性再决定去留")
    # 6 泄漏 + Group Split
    rule(6, "数据泄漏与 Group Split", f"结果列/未来信息不得作特征；**训练集与测试集必须按 {id_col} 分组划分（Group Split）**",
         f"对象 {n_obj} 个", "同对象跨训练/测试划分会导致数据泄漏，交叉验证须用 Group K-Fold")
    # 7 有效样本量
    rule(7, "有效样本量", f"有效独立样本量 = 对象数 {n_obj}（非行数 {n}）；连续特征 {len(hi)} 个",
         f"对象 {n_obj} vs 行 {n}", "复杂度与推断自由度一律以有效独立样本量为准")
    # 8 目标变量（由 Requirement 指定，不锁死）
    if target and target in df.columns:
        s = df[target]
        if not target_is_class(s):
            rule(8, "目标变量", f"本表响应 {target} 为连续目标（Q1-3 的 Y 浓度）；目标由拆题报告按小问指定，数据规则不锁死",
                 f"{target} 共 {int(s.nunique())} 个取值", "回归口径；各问目标不同，见规则 14")
        else:
            vc = s.value_counts(dropna=False)
            n_cat = len(vc)
            if n_cat <= 1:
                rule(8, "目标变量（STOP）", f"⚠️ 目标 {target} 只有 {n_cat} 个非空类别 → 标签退化，无法分类；停止，交拆题报告确认真实目标（如 Q4 应为'染色体的非整倍体'AB列）",
                     f"类别数 {n_cat}", "禁止继续生成不平衡规则；目标以 problem_spec 为准")
            else:
                # 空白可能是"正常"类
                rule(8, "目标变量", f"目标 {target} 有 {n_cat} 个类别（若空白代表'正常'，须先补为显式类）",
                     f"{dict((k, int(v)) for k, v in vc.head(8).items())}", "目标由拆题按 Requirement 指定")
    else:
        rule(8, "目标变量", "未指定目标列", "无", "由拆题报告按小问指定，勿自行认定")
    # 9 类别不平衡（仅当真有≥2类）
    if target and target in df.columns and target_is_class(df[target]) and df[target].nunique() >= 2:
        s = df[target].fillna("正常")  # 空白按正常处理（SEMANTIC_NORMAL）
        vc = s.value_counts()
        if len(vc) == 2:
            minority = vc.min() / vc.sum()
            rule(9, "类别不平衡", f"二分类（含空白=正常），少数类占比 {minority:.0%}",
                 f"{dict((k, int(v)) for k, v in vc.items())}", "不平衡须类权重/阈值调优，报 AUC/查准查全")
        else:
            minr = vc.min() / vc.sum()
            rule(9, "类别不平衡", f"{len(vc)} 类，最小类占比 {minr:.0%}", f"共 {len(vc)} 类", "多分类注意最小类")
    else:
        rule(9, "类别不平衡", "目标非分类或无类别变异，跳过", "无", "见规则 8")
    # 10 复杂度上限（有效独立样本量）
    nfeat = len(hi)
    ceiling = "低复杂度(可解释优先)" if nfeat > 20 or n_obj < 500 else "中等复杂度可接受"
    rule(10, "复杂度上限", f"有效独立样本量 n_obj={n_obj}, 连续特征 {nfeat} → {ceiling}",
         f"n_obj={n_obj}（非行数 {n}）", "以有效独立样本量判复杂度，先可解释基线")
    # 11 多重比较
    npairs = nfeat * (nfeat - 1) // 2
    rule(11, "多重比较", f"两两比较最多 {npairs} 次，须校正", f"{nfeat} 个连续特征", "Bonferroni/FDR 校正，否则假阳性膨胀")
    # 12 效应量与置信区间
    rule(12, "效应量与置信区间", "报告效应量(Cohen's d/OR/相关系数)与置信区间，不只 p 值", "统计规范", "p 显著≠效应有意义")
    # 13 相关≠因果
    rule(13, "相关≠因果", "相关性不得解释为因果", "相关仅描述关联", "题目问'影响/原因'须因果方法")
    # 14 Target 绑定 Requirement
    rule(14, "Target 绑定 Requirement", "各小问目标不同，由拆题报告指定：Q1-3 响应=Y染色体浓度；Q4 目标=染色体的非整倍体(AB列)；数据规则层不永久锁死任何字段为目标/特征",
         "拆题报告 Q1-Q4 目标与约束要点", "建模时按小问选择响应与特征，同一字段在不同问可作不同角色")
    # 15 三级观测结构待决
    rule(15, "三级观测结构待决", "已发现 [孕妇→抽血事件→检测记录] 三级结构，且同一事件可有多条记录；其性质（技术重复/重测/独立检测）数据无法唯一判定",
         "见 data_profiler §5 组合键唯一率链", "须人工/拆题确认后决定：平均、择优、还是保留多层模型（混合效应）")
    # 16 充分性（骨架，逐 R 由拆题编号填）
    reqs = cfg.get("requirements") or []
    p("## 数据充分性检查（逐 Requirement）"); p("")
    if reqs:
        for r in reqs:
            p(f"### Requirement: {r}"); p("当前数据支持：待填（是/部分/否）"); p("已有变量：待填"); p("缺失信息：待填")
            p("缺口类型：待填（变量/参数/背景知识/验证数据）"); p("是否必须补外部数据：待填"); p("理由：待填"); p("若不补数据：模型如何调整？待填"); p("")
    else:
        p("- （待拆题报告 R 编号注入后逐条填写）")
    p("## 锁死清单（人工确认后不得改动）")
    p("1. 观察单位口径（独立样本=对象；同一事件多条记录的处理方式）"); p("2. 空白语义口径（非整倍体空白=无异常）")
    p("3. 各问目标与 Group Split 口径"); p("4. 缺失/极端值处理方式")
    open("E:/26数模国赛/流程产物/数据规则.md","w",encoding="utf-8").write("\n".join(L))
    print(f"OK 数据规则.md ({data})")
if __name__ == "__main__":
    main()
