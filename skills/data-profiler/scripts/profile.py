# -*- coding: utf-8 -*-
"""data-profiler v3（Semantic First）：观测层级发现 + 语义表 + 时间三套 + 血缘日志 + 空白语义 + 冲突告警。
用法: python profile.py <data.csv> [--config <cfg.json>]"""
import pandas as pd, numpy as np, os, sys, json, re
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei","Microsoft YaHei"]; plt.rcParams["axes.unicode_minus"] = False

DATE_PAT = re.compile(r'^(\d{4})(\d{2})(\d{2})$')          # YYYYMMDD
DATE_HINTS = ["date", "日期", "时间", "day", "月经", "time"]
ORDER_HINTS = ["次", "number", "第", "event", "order", "序号", "批次", "index"]
ID_HINTS = ["编号", "代码", "id", "code", "name", "号"]        # 对象标识
TIME_BIO_HINTS = ["孕周", "胎龄", "周", "week", "gest"]
SEMANTIC = {}

def cfg_get():
    return json.load(open(sys.argv[sys.argv.index("--config")+1], encoding="utf-8")) if "--config" in sys.argv else {}

def looks_date_series(s):
    # 短整数形如 YYYYMMDD 或日期类型
    if pd.api.types.is_datetime64_any_dtype(s): return True
    num = s.dropna()
    if num.empty: return False
    try:
        nums = num.astype(float)
        sample = nums.head(50)
        return all(19700000 <= v <= 21000000 and abs(v) % 1 < 1e-6 for v in sample) or                all(19700000 <= v <= 21000000 for v in sample)
    except Exception:
        return False

def semantic_of(col, series, cfg, is_id_candidate):
    name = str(col)
    # 1 ID
    if is_id_candidate: return ("ID", "对象标识（数据中可能存在多行对应同一对象）")
    # 2 日期
    if any(h in name for h in DATE_HINTS) and looks_date_series(series): return ("date", "日历日期（YYYYMMDD 或日期类型）")
    if looks_date_series(series) and series.nunique() > 20: return ("date", "日历日期")
    # 名称含"日期/月经"即使未解析成功也按日期语义提醒
    if ('日期' in name or '月经' in name or 'date' in name.lower()): return ("date", "应为日期，需按数据字典确认（勿按数值跑统计）")
    # 3 有序事件/计数（整型、取值域小或有明确顺序语义）
    if pd.api.types.is_integer_dtype(series):
        ss = series.dropna()
        if ss.empty: u = 0
        else:
            u = ss.nunique()
        if "次" in name or "第" in name or u <= 15: return ("ordinal_event", "有序事件序号/计数（第几次，非无序类别）")
        if u <= 30: return ("count", "计数型")
    # 4 生物时间
    if any(h in name for h in TIME_BIO_HINTS): return ("bio_time", "生物过程时间（孕周等）")
    # 5 连续 vs 低基数数值
    if pd.api.types.is_numeric_dtype(series):
        u = series.nunique()
        if u <= 10: return ("categorical_numeric", "数值编码的分类（低基数）")
        return ("continuous", "连续数值")
    # 6 分类/文本
    return ("categorical", "分类/文本")

def composite_uniqueness(df, cols):
    return float(df.drop_duplicates(subset=cols).shape[0]) / len(df)

def main():
    data = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "test/data/synthetic_nipr.csv"
    cfg = cfg_get(); df = pd.read_csv(data, na_values=["?", "", "NA", "nan"])
    if len(df) == 0: print("FAIL: 空数据"); sys.exit(1)
    id_col = cfg.get("id_col")
    event_col = cfg.get("event_col")
    target = cfg.get("target_col")
    # 自动候选 ID：名字带编号/代码且重复度高
    if not id_col:
        for c in df.columns:
            if any(h in str(c) for h in ID_HINTS) and df[c].nunique() <= len(df):
                id_col = c; break
    numeric = df.select_dtypes("number").columns.tolist()
    os.makedirs("results/figures", exist_ok=True)
    L = []; p = L.append
    p("---"); p("type: data-profile"); p("stage: 数据概况"); p("owner: deepseek"); p("status: draft")
    p("upstream:"); p('  - "原始数据"'); p("downstream:"); p('  - "[[数据规则]]"'); p("---"); p("")
    p("# 数据概况.md —— 数据概况与观测层级（② data-profiler 产出）"); p("")
    # 1 文件说明
    p("## 1. 数据表/文件说明"); p(f"- 数据文件：{data}"); p(f"- 原始行列：{len(df)} 行 × {df.shape[1]} 列（含派生列前见血缘日志）"); p("")
    # 2 行代表什么（观测单位）
    p("## 2. 行代表什么（观测单位）")
    p(f"- 原始一行是一条原始记录。对象标识候选：{id_col or '未自动识别'}。")
    if id_col:
        n_obj = int(df[id_col].nunique())
        p(f"- 独立对象数：{n_obj}；行数 {len(df)} ≠ 独立对象数 → 存在多层结构（见 §5 观察单位）。")
    p("")
    # 3 列语义表
    p("## 3. 列语义表（Semantic First）"); p("| 列 | 物理类型 | 语义类型 | 说明 |"); p("|---|---|---|---|")
    for c in df.columns:
        is_id = (c == id_col)
        sem, desc = semantic_of(c, df[c], cfg, is_id)
        phys = "数值" if pd.api.types.is_numeric_dtype(df[c]) else "文本/日期"
        p(f"| {c} | {phys} | {sem} | {desc} |")
    p("")
    # 4 样本量与层级概述
    p("## 4. 样本量与层级概述")
    if id_col:
        grp = df.groupby(id_col).size()
        p(f"- 独立对象数：{int(len(grp))}")
        p(f"- 对象重复分布：1次 {int((grp==1).sum())} 个，2次 {int((grp==2).sum())} 个，≥3次 {int((grp>=3).sum())} 个")
        p(f"- 行数 {len(df)} vs 对象数 {len(grp)}（差异就是第一层重复）")
    else:
        p("- 未识别明确对象标识列。")
    p("")
    # 5 观察单位发现（组合键审计）
    p("## 5. 观察单位发现（Composite Key Audit / Observation Unit Discovery）")
    keys = [ [id_col], [id_col, event_col] ] if id_col and event_col else ([ [id_col] ] if id_col else [])
    if id_col:
        keys.append([id_col, event_col] if event_col else [id_col])
        # 再自动加时间/数值候选
        for c in df.columns:
            if c != id_col and c != event_col and df[c].nunique() > 1:
                if len(keys[-1]) < 3: keys[-1] = keys[-1] + [c]
        uniqs = []
        for k in ([id_col] if id_col else []):
            pass
        # 重组：逐级组合
        # 组合键仅选有层级/时间语义的字段：ID → 事件 → 生物时间 → 日历时间
        chain = [id_col]
        cands = []
        if event_col: cands.append(event_col)
        for c in df.columns:
            if any(h in str(c) for h in TIME_BIO_HINTS) and c not in chain and c not in cands:
                cands.append(c); break
        for c in df.columns:
            if ('日期' in str(c) or 'date' in str(c).lower()) and "次" not in str(c) and c not in chain and c not in cands:
                cands.append(c); break
        # 其余高基数连续字段补足
        for c in df.columns:
            if c in chain or c in cands or c == id_col or c == event_col: continue
            if pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique() > 10 and len(chain) + len(cands) < 6:
                cands.append(c)
        chain = chain + cands
        print("  组合键链:", chain)
        prev = 1.0
        p("| 组合键层 | 当前唯一率 | 相比上层下降 |"); p("|---|---|---|")
        for depth in range(1, len(chain)+1):
            k = chain[:depth]
            u = composite_uniqueness(df, k)
            tag = " ← 接近唯一" if u >= 0.995 else ""
            down = f"{prev-u:.3f}" if prev else "-"
            p(f"| {'+'.join(k)} | {u:.3f}{tag} | {down} |")
            prev = u
        p("- 结论：若唯一率随层级显著上升，说明存在 [对象 → 事件 → 记录] 的多层观测结构，需在 data-ruler 中按最高唯一层定义观察单位")
    else:
        p("- 无法做组合键审计（无明确对象标识）。")
    p("")
    # 6 血缘日志
    p("## 6. 血缘日志（Schema Transformation Log）")
    p(f"- RAW：原始 {len(df)} 行 × {df.shape[1]} 列")
    dropped = cfg.get("dropped_columns") or []
    if dropped:
        p(f"- DROP：去除 {len(dropped)} 列（{', '.join(dropped)}，原因待确认）→ 分析表列数 {df.shape[1]-len(dropped)}")
    added = cfg.get("derived_columns") or []
    if added:
        p(f"- DERIVED：新增 {len(added)} 列（{', '.join(added)}）")
    p("- 说明：血缘日志应尽量由上游预处理记录；本 skill 以显式 DROP/DERIVED 为准。")
    p("")
    # 7 类型（物理/语义）已并入 §3，此处补充
    p("## 7. 数据类型说明")
    p("- 物理类型（Python dtype）仅反映存储，**语义类型才是统计依据**（见 §3 语义表）。")
    p("")
    # 8 缺失与空白语义
    p("## 8. 缺失与空白语义（Blank ≠ Missing）")
    miss = df.isna().mean()
    any_m = False
    for c in df.columns:
        if miss[c] > 0:
            sem = "待确认"
            p(f"- {c}：原始空白率 {miss[c]:.1%}（语义：{sem}；可能是 NOT_APPLICABLE/SEMANTIC_NORMAL/TRUE_MISSING，需按数据字典确认，勿直接当 true missing）")
            any_m = True
    if not any_m: p("- 无原始空白。")
    p("")
    # 9 重复与多层观测
    p("## 9. 重复与多层观测")
    p(f"- 完全重复行：{int(df.duplicated().sum())}")
    if id_col:
        grp = df.groupby(id_col).size()
        p(f"- {id_col} 出现多行的对象：{int((grp>1).sum())} 个（第一层重复）")
        if event_col:
            grp2 = df.groupby([id_col, event_col]).size()
            p(f"- {id_col}+{event_col} 出现多行的组：{int((grp2>1).sum())} 个（第二层重复 → 同一抽血事件多条检测记录）")
    p("")
    # 10 时间三套
    p("## 10. 时间结构（三套分开）")
    bio = [c for c in df.columns if any(h in str(c) for h in TIME_BIO_HINTS)]
    cal = [c for c in df.columns if any(h in str(c) for h in DATE_HINTS) and ('日期' in str(c) or 'date' in str(c).lower())]
    order = [c for c in df.columns if '次' in str(c) or '第' in str(c) or c == event_col]
    p(f"- 生物时间（孕周等）：{bio or '无'}")
    p(f"- 日历时间（检测日期等）：{cal or '无'}")
    p(f"- 个体内顺序（第几次/事件序号）：{order or '无'}")
    p("- 三套时间不要混成一个变量。")
    p("")
    # 11 分布与相关
    p("## 11. 分布与相关（语义化）")
    cont = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique() > 10]
    p("### IQR 极端观测候选（并非'异常值'，是否异常由 data-ruler 判断）")
    p("| 列 | IQR 极端候选条数 |"); p("|---|---|")
    shown = 0
    for c in cont:
        if c in (id_col or []): continue
        q1, q3 = df[c].quantile([.25,.75]); iqr = q3-q1
        n = int(((df[c] < q1-1.5*iqr) | (df[c] > q3+1.5*iqr)).sum())
        if n > 0: p(f"| {c} | {n} |"); shown += 1
    if shown == 0: p("| (无) | 0 |")
    p("### 相关性（|r|>0.7，仅供参考）")
    if cont and len(cont) > 1:
        corr = df[cont].corr(method="spearman")
        for i in range(len(cont)):
            for j in range(i):
                v = corr.iloc[i,j]
                if abs(v) > 0.7: p(f"- {cont[i]} × {cont[j]}（Spearman r={v:.2f}）")
    p("")
    # 12 冲突告警
    p("## 12. 冲突告警（Contradiction Alarm）")
    n_alert = 0
    if target and target in df.columns:
        vc = df[target].value_counts(dropna=False)
        if len(vc.dropna()) <= 1:
            p(f"- ⚠️ 疑似 target「{target}」只有 {len(vc.dropna())} 个非空类别，无法作为分类目标 → STOP，交给 problem_spec/data-ruler 确认，禁止自行认定。")
            n_alert += 1
    if cfg.get("blank_semantic_pending"):
        p(f"- ⚠️ {len(cfg['blank_semantic_pending'])} 个高空白字段语义待按数据字典确认（勿当 true missing）。")
    if n_alert == 0: p("- 未触发冲突告警（target 语义以拆题报告为准）。")
    p("")
    p("## 待确认清单"); p("- 字段空白语义（尤其染色体非整倍体、胎儿是否健康）；- 观察单位最终定义（见 §5）。")
    open("E:/26数模国赛/流程产物/数据概况.md","w",encoding="utf-8").write("\n".join(L))
    print(f"OK 数据概况.md ({data})")
if __name__ == "__main__":
    main()