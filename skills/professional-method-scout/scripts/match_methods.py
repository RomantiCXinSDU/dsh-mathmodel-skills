# -*- coding: utf-8 -*-
"""match_methods.py —— 结构识别 → 方法匹配（professional-method-scout 确定性内核，MC 格式）。"""
import pandas as pd, numpy as np, sys, json, os
TIME_HINTS = ["week","month","year","date","time","day","period","孕周","胎龄","日期","时间","周期","季度"]
SPATIAL_HINTS = ["lon","lat","long","经","纬","坐标","longitude","latitude"]
CENSOR_HINTS = ["检出","下限","上限","threshold","limit","检测限","cutoff"]
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
    data = sys.argv[1]; cfg = cfg_get()
    df = pd.read_csv(data, na_values=["?", "", "NA", "nan"])
    target = cfg.get("target_col"); id_col = cfg.get("id_col") or auto_id(df)
    time_col = cfg.get("time_col") or auto_time(df, target)
    numeric = df.select_dtypes("number").columns.tolist()
    hi = [c for c in numeric if df[c].nunique() > 10 and c != target]
    n = len(df)
    hits = []
    def add(rule, structure, essence, methods, condition, risk):
        hits.append((rule, structure, essence, methods, condition, risk))
    if id_col:
        nrep = int((df.groupby(id_col).size() > 1).sum())
        if nrep > 0:
            add("[[data_rules#规则 12]]", "重复测量", "个体内相关，违反独立性",
                "线性混合效应 LMM / GEE / GAMM", "连续或 0/1 目标 + 同对象多次观测",
                "普通 OLS/逻辑回归忽略组内相关 → 标准误低估（伪重复）")
    if cfg.get("event_hint"):
        add("[[data_rules#规则 2]]", "事件时间（多久达标/首次发生）", "删失 + 时间到事件",
            "生存分析 KM + Cox / AFT + 首达时间反推", "存在观察期结束时仍未发生的删失样本",
            "拿单次测量值当达标时间 → 严重偏差")
    if target and target in df.columns:
        s = df[target]
        if not target_is_class(s):
            if s.min() >= 0 and s.max() <= 1 and s.nunique() > 2:
                add("[[data_rules#规则 8]]", "比例目标 [0,1]", "有界响应 + 方差非齐",
                    "Beta 回归 / Fractional Logistic", "目标为 0~1 比例",
                    "OLS 预测可能越界 [0,1]")
            elif s.dtype.kind in "iu" and s.min() >= 0:
                zr = float((s == 0).mean())
                m = "Poisson → 负二项" + (" → Zero-inflated/Hurdle" if zr > 0.3 else "")
                add("[[data_rules#规则 8]]", "计数目标", "非负整数 + 方差=均值假设" + ("+ 零膨胀" if zr > 0.3 else ""),
                    m, "计数型目标", "OLS 对计数目标失真；零多时普通 Poisson 低估零概率")
            elif cfg.get("quantile_hint"):
                add("[[data_rules#规则 2]]", "达标线/分位关注", "条件分位数而非均值",
                    "分位数回归 / 贝叶斯分位数", "题目关注达标阈值或高分位",
                    "均值回归回答不了'90%对象何时达标'")
            else:
                add("[[data_rules#规则 10]]", "连续目标", "回归任务",
                    "变换回归(Box-Cox) → GLM / GAM / 稳健回归", "连续目标 + 诊断后升级",
                    "不诊断直接 OLS 可能违反正态/线性假设")
        else:
            vc = s.value_counts(dropna=False)
            if len(vc) == 2:
                minority = vc.min() / vc.sum()
                m = "逻辑回归(基线)" + (" + 类权重/SMOTE/阈值调优 + PR-AUC" if minority < 0.1 else "")
                add("[[data_rules#规则 8]]", "二分类" + ("+不平衡" if minority < 0.1 else ""), "判别 + 概率输出",
                    m, "二分类目标" + ("；少数类<10% 须处理不平衡" if minority < 0.1 else ""),
                    "只报准确率(不平衡下无意义)；阈值不调优漏检高代价类")
                if minority < 0.15:
                    add("[[data_rules#规则 8]]", "稀少异常样本", "异常检测视角",
                        "Isolation Forest / LOF（与分类互为印证）", "异常类占比很低时",
                        "纯分类模型对稀少类拟合不足")
            else:
                m = "多项逻辑回归" + ("（等级有序→Ordinal 回归）" if cfg.get("ordinal") else "")
                add("[[data_rules#规则 8]]", "多分类", "多类别判别", m, "多分类目标",
                    "强行编码成数值做回归不合规范")
    miss_cols = [c for c in df.columns if df[c].isna().mean() > 0]
    if miss_cols:
        add("[[data_rules#规则 3]]", "缺失数据", "缺失机制 MCAR/MAR/MNAR",
            "机制判别 → MICE 多重插补 / EM", "缺失比例>0",
            "均值填充忽略缺失机制，可能引入偏倚")
    if n < 100:
        add("[[data_rules#规则 7]]", "小样本", "大样本近似失效",
            "Fisher 精确检验 / 置换检验 / Bootstrap / 贝叶斯", "n<100",
            "依赖渐近分布的方法(卡方/t)误差大")
    if len(hi) > max(10, n // 10):
        add("[[data_rules#规则 7]]", "高维/共线", "维度诅咒 + 多重共线",
            "Ridge/Lasso/ElasticNet + PLS", "特征多且样本相对少",
            "OLS 过拟合、系数不稳定")
    if hi:
        in01 = [c for c in hi if df[c].min() >= 0 and df[c].max() <= 1]
        if len(in01) >= 3:
            rsum = df[in01].sum(axis=1)
            if 0.9 <= rsum.mean() <= 1.1:
                add("[[data_rules#规则 5]]", "成分数据(总和恒定)", "单纯形约束 + 成分内在依赖",
                    "CoDA：CLR/ILR 变换", "成分比例列和≈1",
                    "直接建模成分数据会产生伪相关")
        qt = df[hi].quantile([.25,.75]); iqr = qt.iloc[1] - qt.iloc[0]
        ratio = float((((df[hi] < qt.iloc[0]-1.5*iqr) | (df[hi] > qt.iloc[1]+1.5*iqr)).sum().sum()) / (n*len(hi)))
        if ratio > 0.05:
            add("[[data_rules#规则 4]]", "重尾/离群", "离群点拉偏估计",
                "稳健回归 Huber / RANSAC / Theil-Sen / 分位数回归", "IQR 离群占比>5%",
                "OLS 对离群敏感，系数被拉偏")
    if time_col:
        add("[[data_rules#规则 2]]", "时间序列", "时序相关 + 顺序不可乱",
            "ARIMA/SARIMA + Holt-Winters + 状态空间", "含时间维度 + 顺序切分",
            "随机切 train/test 泄漏未来信息")
    spat = [c for c in df.columns if any(h in str(c).lower() for h in SPATIAL_HINTS)]
    if spat or cfg.get("spatial"):
        add("[[data_rules#规则 13]]", "空间结构", "空间自相关",
            "Moran's I → SAR/SEM/GWR + Kriging", "地理邻近样本",
            "忽略空间自相关，残差非独立")
    cens = [c for c in df.columns if any(h in str(c).lower() for h in CENSOR_HINTS)]
    if cens or cfg.get("censored"):
        add("[[data_rules#规则 3]]", "删失/检出限", "截断分布",
            "Tobit / 删失回归", "测量有上下限",
            "把低于检出限当 0 → 偏差")
    if cfg.get("error_required"):
        add("[[data_rules#规则 3]]", "输入测量误差", "X 有误差 → 系数衰减偏倚",
            "Errors-in-Variables + 蒙特卡洛误差传播", "题目要求分析检测误差影响",
            "忽略 X 误差的 OLS 系数有偏")
    for key, rule_ref, structure, essence, m, cond, risk in [
        ("queue", "[[data_rules#规则 2]]", "排队/服务系统", "随机到达+服务时间", "排队论 M/M/1、M/M/c + Little 定律", "系统存在排队等待结构", "静态均值估计忽略等待时间分布"),
        ("inventory", "[[data_rules#规则 10]]", "库存/补货决策", "需求不确定下成本权衡", "报童模型 / EOQ / 多期库存", "订购量/补货决策", "按点估计进货 → 缺货或积压"),
        ("game", "[[data_rules#规则 18]]", "多方策略互动", "策略相互影响", "博弈论：纳什均衡 / 演化博弈", "多主体决策互相影响", "单方优化忽略对手反应"),
        ("mechanism", "[[data_rules#规则 10]]", "物理/传播机理", "机理方程优于纯数据", "ODE / 差分方程 / SIR 类", "存在明确机理过程", "纯数据模型外推不可靠"),
        ("evaluation", "[[data_rules#规则 10]]", "评价/筛选对象", "多指标综合", "AHP/TOPSIS/RFM/评分卡(按题选)", "筛选/评价类子问", "熵权TOPSIS一把梭缺业务解释"),
    ]:
        if cfg.get(key): add(rule_ref, structure, essence, m, cond, risk)
    L = ["---", "type: method-candidates", "stage: method-scout", "owner: deepseek", "status: draft",
         "upstream:", '  - "[[data_rules]]"', "downstream:", '  - "[[candidates]]"', "---", "",
         "# method_candidates.md —— 专业方法候选（③ professional-method-scout 产出）", ""]
    L.append(f"## 数据：{data}（n={n}）"); L.append("")
    if hits:
        for i, (rule_ref, structure, essence, m, cond, risk) in enumerate(hits, 1):
            L.append(f"## MC-{i:02d}")
            L.append(f"- 触发的数据规则：{rule_ref}")
            L.append(f"- 特殊结构：{structure}")
            L.append(f"- 数学本质：{essence}")
            L.append(f"- 候选专业方法：{m}")
            L.append(f"- 适用条件：{cond}")
            L.append(f"- 普通方法的风险：{risk}")
            L.append("- 文献依据：待检索确认（检索'方法名+问题类型'的适用性文献，禁止搜当届赛题解答）")
            L.append("- 建议进入 Model Explorer：是")
            L.append("")
    else:
        L.append("- 未检出特殊结构：常规线性/逻辑回归基线即可，不强行上专业方法。")
    out = sys.argv[sys.argv.index("--out")+1] if "--out" in sys.argv else "results/method_candidates.md"
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    open(out, "w", encoding="utf-8").write("\n".join(L))
    print(f"OK {out} ({len(hits)} 个 MC)")
if __name__ == "__main__":
    main()
