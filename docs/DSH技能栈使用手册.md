# DSH 数模技能栈使用手册（赛时直接照抄）

> 6 个 skill 已全局挂载（C:\Users\Lenovo\.dsh\skills\），任何会话自动识别，说出触发词即用。
> 源工程在 E:\26数模国赛\mathmodel-dsh（迭代修改后记得同步挂载）。

## 一、技能栈总览（按比赛流程顺序）

| 顺序 | Skill | 一句话触发 | 产出 |
|---|---|---|---|
| 0 | （拆题=Kimi 的活） | 你另有安排 | problem_spec.md |
| 1 | data-profiler | "做数据概况 / EDA / 读数据" | data_profile.md + 图 |
| 2 | data-ruler | "定数据规则 / 清洗口径 / 数据能用什么模型" | data_rules.md（人工锁死） |
| 3 | data-pattern-to-method | "结构识别 / 该用什么方法 / 有没有更专业的" | method_matches.md（带评委句） |
| 4 | model-explorer | "发散模型 / 三派候选 / 推荐模型" | candidates.md |
| 5 | formalizer | "正式建模 / 写数学模型 / model_spec" | model_spec.md |
| 6 | solver-verifier | "求解 / 验证 / 敏感性分析 / 误差分析" | 代码+结果+validation_report.md |

## 二、赛时标准喊法（直接复制）

```
1. "加载 data-profiler 对附件数据做数据概况"
2. "加载 data-ruler 定数据规则"
3. 【人工关卡1：确认并锁死 data_rules】
4. "加载 data-pattern-to-method 识别这道题的数据结构该用什么专业方法"
5. "加载 model-explorer 按三派发散候选模型"
6. 【人工关卡1.5：确认主方案】
7. "加载 formalizer 把主方案写成正式数学模型"
8. "加载 solver-verifier 求解并做敏感性/误差/对比验证"
9. 【人工关卡2：逐项核验 → 冻结】
```

## 三、一句口诀
**"概况 → 规则 → 结构匹配 → 发散 → 形式化 → 求解验证，三个关卡人点头，数字全部有来源。"**

## 四、校验脚本（solver-verifier 自动跑）
- check_numbers.py：数字溯源（论文数字必须有 [src:...]）
- check_symbols.py：符号与代码变量一致
- check_repro.py：可复现
- check_compliance.py：合规（AI 声明/无身份信息/附录源程序）
- pipeline.py：状态机（返工上限 2 / 冻结门禁）

## 五、维护注意
- 我迭代 skill 后会把 E:\26数模国赛\mathmodel-dsh\skills\ 重新复制到 C:\Users\Lenovo\.dsh\skills\；
- 联网边界：✅ 可联网查资料/用 AI；❌ 禁止搜当届赛题实时解答、禁止与队外讨论赛题。
