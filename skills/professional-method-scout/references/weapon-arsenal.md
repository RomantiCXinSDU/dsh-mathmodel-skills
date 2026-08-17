# C 题专业方法武器库 v2.0（完整版）

> 核心不是背模型，是练反射：
> 看到数据 → 它有什么特殊性？ → 这种特殊性在统计/运筹里叫什么？ → 有没有专门方法？ → 适用条件？ → 为什么普通模型不够？ → 用了解决题目什么真实问题？

## 1. 总触发表（一看到 → 第一反应）

| 一看到 | 第一反应 |
|---|---|
| 同一对象多次观测 | 混合效应 / GEE |
| 多层结构(学生-班-校) | Hierarchical Model |
| "多久发生" | 生存分析 |
| 未发生到观察结束 | 删失 Censoring |
| 目标 0/1 | Logistic / Binomial GLM |
| 目标是计数 | Poisson / 负二项 |
| 大量 0 | Zero-inflated / Hurdle |
| 目标比例 0~1 | Beta 回归 |
| 等级标签(优/良/差) | Ordinal 回归 |
| 关注 90% 分位/达标线 | 分位数回归 |
| 各成分和=100% | CoDA / CLR / ILR |
| 测量有上下限/检测不到 | Tobit / 删失回归 |
| 输入有误差 | Errors-in-Variables / 蒙特卡洛 |
| 异常点多/重尾 | 稳健回归(Huber/RANSAC) |
| 缺失很多 | 缺失机制判别 + MICE |
| 正负样本严重失衡 | 类权重 / 阈值调优 / PR-AUC |
| 样本很少 | 精确检验 / Bootstrap / 贝叶斯 |
| 变量很多/共线 | 正则化 / PCA / PLS |
| 有时间顺序 | 时间序列 / 状态空间 |
| 规律突然改变 | 变点检测 / 分段回归 |
| 有经纬度/地区 | 空间统计(Moran/SAR/GWR) |
| 地区×多年 | 时空面板 |
| 有关系网络 | 图/网络模型 |
| 网络路径/流量/分配 | 最短路/最大流/匹配 |
| 排队/等待/服务系统 | 排队论 M/M/1、M/M/c |
| 进货量/库存/补货 | 报童模型 / EOQ |
| 多方策略互动 | 博弈论(纳什/演化) |
| 筛选/评价对象 | AHP / TOPSIS / RFM / 评分卡 |
| 异常样本稀少且重要 | 异常检测 IsolationForest / LOF |
| 问"真正影响" | 因果推断(PSM/DID) |
| 非线性但要解释 | GAM / 样条 |
| 人群天然异质 | 潜类 / 混合模型 |
| 潜在综合指标 | 因子分析 / SEM |
| 联合依赖/联合风险 | Copula |
| 极端风险 | EVT / CVaR |
| 每个样本是一条曲线 | 功能数据分析 |
| 物理/传播/扩散机制 | ODE / 差分 / SIR |
| 安排试验/检测方案 | 正交试验 / 响应面 |
| 几十次重复检验 | 多重校正(Bonferroni/FDR) |
| 最终要做策略 | 不确定性优化 |
| 黑盒模型要解释 | SHAP / 置换重要性 |

## 2. 八大类结构 × 方法

### 第一大类：数据存在相关性/层级结构
- 同对象多次观测：LMM、GLMM、GEE、固定/随机效应面板、多层模型、层级贝叶斯、重复测量 ANOVA 【S】
- 明显层级(嵌套)：Random Intercept/Slope、Crossed Random Effects、Nested Model 【A】

### 第二大类：目标变量特殊
- 事件时间：Kaplan-Meier、Log-rank、Cox、AFT、Weibull、区间删失、竞争风险、复发事件、联合模型 【S：KM/Cox；B：其余】
- 0/1：Logistic、Probit、cloglog、Firth Logistic、Bayesian Logistic、GAM Logistic 【S】
- 计数：Poisson → NB(过度离散) → Zero-inflated/Hurdle(大量0)、Poisson 混合模型 【S/A】
- 比例 0~1：Beta 回归、Fractional Logistic、Beta-Binomial、零一膨胀 Beta 【A】
- 等级：Ordinal Logistic、Ordered Probit、累积链接模型、Ordinal 混合模型 【A】
- 达标线/分位：分位数回归、贝叶斯分位数、分位数 GAM、分位数森林 【S】

### 第三大类：数据特殊约束
- 成分和=100%：CoDA、CLR/ALR/ILR、Aitchison 距离、Dirichlet 回归、成分 PCA 【S】
- 截断/删失：Tobit、删失回归、截断回归、区间删失、检出限模型 【A】
- 输入测量误差：EIV、Deming 回归、TLS、SIMEX、贝叶斯测量误差、蒙特卡洛传播、Delta 方法 【S】
- 大量异常/重尾：Huber、RANSAC、Theil-Sen、LAD、分位数回归、稳健协方差、Student-t 误差 【S】

### 第四大类：数据质量与样本规模
- 缺失多：MCAR/MAR/MNAR 判别 → 完整案例分析/多重插补/MICE/KNN插补/EM/IPW；模式混合模型、选择模型 【S：机制+MICE；B：其余】
- 类别极不平衡：类权重/代价敏感/Focal Loss(模型层)、过采样/SMOTE 系/欠采样(数据层)、阈值调优(决策层)、PR-AUC/ROC/Balanced Acc/MCC(评价) 【S】
- 异常样本稀少且重要：Isolation Forest、LOF、One-Class SVM —— 异常检测视角，不是纯分类 【A】★NIPT 问题4 备选
- 小样本：Fisher 精确、精确二项、置换检验、Bootstrap、贝叶斯、收缩估计、Firth、LOOCV/嵌套 CV 【A】
- 高维/共线：Ridge/Lasso/ElasticNet/GroupLasso(正则)、PCA/SparsePCA/PLS/因子/ICA(降维)、稳定性选择/RFE/互信息/Boruta(选特征) 【S】

### 第五大类：时间、空间、网络结构
- 时间序列：AR/MA/ARMA/ARIMA/SARIMA、指数平滑/Holt/Holt-Winters、VAR/VECM、状态空间/Kalman、ARCH/GARCH、GAM/GP/TBATS 【S】
- 规律突变：变点检测、分段回归、CUSUM、PELT、贝叶斯变点、HMM 【A】
- 空间：Moran's I/Geary's C/LISA、SAR/SEM/SDM、GWR/MGWR、Kriging、Getis-Ord Gi* 【S】
- 时空：时空回归、空间面板、动态空间模型、时空高斯过程 【B】
- 网络关系(科学视角)：中心性(度/介数/特征向量)、PageRank、Louvain/Leiden、谱聚类、网络 SIR、ERGM、随机块模型 【A】
- 图论经典(运筹视角)：最短路、最小生成树、最大流/最小割、匹配、选址、网络设计 【A】

### 第六大类：关系不是简单"相关"
- 问"真正影响"：PSM、IPW、DID、RDD、工具变量、合成控制、双重稳健、因果森林、DAG、SCM 【A】
- 非线性但要解释：GAM、样条回归、LOESS、限制立方样条、分段回归 【S】
- 人群天然异质：GMM、潜类分析、潜剖面、混合回归、专家混合、HMM、模型聚类 【A】
- 潜在综合指标：探索性/验证性因子、SEM、PLS-SEM、IRT、潜变量模型 —— 比"熵权TOPSIS一把梭"更规范 【A】
- 联合依赖：交互模型、Copula/Vine Copula、多元回归/多元GLM、贝叶斯网络 【A】
- 极端值：EVT、GEV、GPD、POT、VaR/CVaR、尾部依赖、极端分位数回归 【B】
- 样本是曲线：功能PCA、功能回归、功能聚类、基展开、B样条/小波、功能ANOVA 【B】
- 物理/传播/扩散机制：ODE/PDE、差分方程、SIR 类、系统动力学、元胞自动机 【B】(2015 C 月上柳梢头=天文几何机理)
- 多方策略互动：纳什均衡、演化博弈、拍卖/匹配理论 【A】(2019 C 司机决策可加博弈视角)

### 第七大类：运筹与决策（C 题高频，别只学规划）
- 确定性优化：LP、MILP(大M/0-1逻辑)、NLP、动态规划、网络优化 【S】
- 多目标：加权和、ε-约束、帕累托前沿、NSGA-II 【S】
- 不确定性优化：随机规划、鲁棒优化、机会约束、分布鲁棒、情景优化、CVaR 优化、Min-Max Regret 【S】
- 排队论：M/M/1、M/M/c、M/G/1、Little 定律、排队优化 —— 2019 C 国奖核心 【S】★补
- 库存理论：报童模型(Newsvendor)、EOQ、(s,S) 策略、多期动态库存 —— 2023 C 补货本质 【S】★补
- 序贯决策：马尔可夫决策过程 MDP、动态规划、强化学习入门 【A】★补

### 第八大类：评价与赋权（C 题高频中的高频）
- 经典评价：AHP、TOPSIS、熵权法、模糊综合评价、灰色关联、秩和比 RSR 【S】★补
- 业务评价：RFM(2018 会员画像国奖)、客户价值金字塔 【S】★补
- 评分卡：WOE/IV 分箱、逻辑回归评分卡、KS/AUC 验证 —— 信贷/风险类题目首选 【A】★补
- 效率评价：DEA、SBM、Malmquist 【A】★补
- 组合赋权：主观(AHP)+客观(熵权/CRITIC) 组合，而非单边赋权 【A】★补

### 横切武器（挂在任何题型上）
- Bootstrap：小样本/置信区间/稳定性 【S】
- 蒙特卡洛：误差传播/情景模拟/风险分析 【S】
- 贝叶斯：小样本/先验/层级/复杂概率模型；MCMC、BMA 【A】
- 概率校准：Platt/Isotonic/Temperature、校准曲线、Brier —— 输出"概率80%"要真有概率意义 【A】
- 模型平均：BMA、集成、Stacking —— 不为了集成而集成 【A】
- 多重检验校正：Bonferroni/FDR —— 几十次检验必做 【A】★补
- 效应量：不只报 p 值(Cohen's d/OR/相关系数) 【A】★补
- 试验设计：正交试验、响应面 RSM —— "如何安排检测/试验"子问 【B】★补
- 呈现武器：双标图(2022国一)、龙卷风图(敏感性)、SHAP/置换重要性(黑盒解释)、校准曲线 【S】★补

## 3. 三级弹药库（按时间分配）

### S 级：C 题队伍必须熟练（18 类，赛前死磕）
混合效应/GEE · GLM · GAM/样条 · 生存分析 · 分位数回归 · CoDA · 缺失机制+MICE · 稳健回归 · 不平衡+阈值 · Bootstrap · 蒙特卡洛误差传播 · 时间序列/状态空间 · 空间统计 · 正则化/PLS · 随机/鲁棒优化 · 排队论 · 报童/库存 · 评价赋权家族(AHP/TOPSIS/RFM)

### A 级：冲国奖应该认识（12 类，知道触发信号+能调）
零膨胀 · Tobit/删失 · 层级贝叶斯 · 因果推断 · 变点检测 · 潜类/混合模型 · SEM · 概率校准 · Copula · Beta 回归 · 异常检测(IsolationForest/LOF) · 博弈论 · 评分卡(WOE/IV) · 多重校正+效应量 · 图论经典 · MDP

### B 级：遇到了再调出来（不推公式）
EVT · 功能数据 · 时空面板 · 竞争风险 · 联合纵向-生存 · 高斯过程 · Dirichlet 回归 · Firth Logistic · Vine Copula · 分布鲁棒优化 · 机理动力学(ODE/SIR/元胞自动机) · 试验设计(正交/RSM)

## 4. 历年真题映射表（考纲）
| 年份 | C 题 | 对应武器 |
|---|---|---|
| 2015 | 月上柳梢头 | 机理/天文几何(B级机理) |
| 2016 | 电池放电预测 | 回归+曲线拟合 |
| 2017 | 颜色与浓度 | 线性回归(简单正确) |
| 2018 | 会员画像 | RFM+聚类(评价家族) |
| 2019 | 机场出租车 | 排队论+成本收益决策★ |
| 2020 | 信贷决策 | 分类+不平衡+评分卡 |
| 2021 | 原材料订购 | 评价指标+优化+噪声模拟 |
| 2022 | 玻璃成分 | CoDA+分类+多重校正+双标图 |
| 2023 | 蔬菜定价补货 | 时间序列+报童/补货决策★ |
| 2024 | 农作物种植 | MILP+启发式 |
| 2025 | NIPT 时点与异常 | 生存/首达+分位数+误差传播+异常检测/不平衡分类 |

## 5. NIPT 2025 四问武器映射
| 问题 | 题型 | 首选专业武器 |
|---|---|---|
| 问题1 相关+关系模型 | 推断+回归 | Spearman/Pearson 按数据选 → 变换回归 + 显著性 + 多重校正 |
| 问题2 分组+最佳时点 | 生存+决策 | 首达时间反推 + 生存分析 + 业务分组 + 风险最小化目标 |
| 问题3 多因素+误差+达标比例 | 回归+误差 | 分位数回归 + 误差传播/蒙特卡洛 + CDF 达标比例 |
| 问题4 女胎异常判定 | 分类/异常检测 | 横评分类器 → 可解释最优 + 不平衡三件套 + AUC；备选异常检测视角(IsolationForest/LOF) |

## 6. 条目模板（写进 data-pattern-to-method skill 用）
每类方法一条目，禁止写百科式介绍，必须含：
【触发信号】【数学本质】【适用】【优先比较】【不能机械使用】【建模亮点】【评委解释句】【验证】
