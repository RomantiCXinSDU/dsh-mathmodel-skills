---
name: data-profiler
description: 数据概况与观测层级发现（Semantic First）。读任意 CSV/XLSX，先识别"一行到底是什么、行间层级关系"（对象→事件→记录组合键审计），再做 12 项数据事实画像（含字段语义表/时间三套/血缘日志/Blank≠Missing/冲突告警）。只描述事实，禁止推荐模型、禁止自行认定 target。当用户要求做数据概况、EDA、读数据、看数据质量时使用。
---

# data-profiler — 数据概况手（DeepSeek）

## 核心目标（Semantic First）
> **先搞清"一行代表什么、行与行之间是什么关系"，再谈任何统计。** 不是把 Excel 描述清楚，而是看穿观测单位与层级。

## 铁律
1. **Semantic First**：先确认字段语义 → 再定变量类型 → 最后才做统计。禁止用 Python dtype 顶替语义。
2. **Observation Unit Discovery**：一行=对象？事件？还是记录？出现"同一对象+同一事件+多行"，必须继续向下一层检查，不得停在第一层就说"多次采血"。
3. **Composite Key Audit**：自动试组合键（如 ID → ID+事件 → ID+事件+时间 → ID+事件+时间+日期），报告在哪一层才接近唯一，识别多维层级。
4. **Blank ≠ Missing**：高空值字段分类报告 RAW_BLANK / SEMANTIC_NORMAL / NOT_APPLICABLE / TRUE_MISSING，禁止把 cell blank 直接当 true missing。
5. **Contradiction Alarm**：某字段疑似分类 target 却只有 1 个类别 → STOP，标记语义冲突，交给 problem_spec / data-ruler，禁止自行认定 target。
6. 只描述事实，不选模型、不预测、不下建模结论；不擅自删除/填补。

## 输出（固定节，写入 数据概况.md）
1. 数据表/文件说明  2. 行代表什么（观测单位）  3. 列语义表  4. 样本量与层级
5. 观察单位发现（组合键审计结果）  6. 血缘日志（RAW→DROP→DERIVED）  7. 数据类型（物理/语义）
8. 缺失与空白语义  9. 重复与多层观测  10. 时间结构（生物/日历/个体内，三套分开）
11. 分布与相关（语义化）  12. 冲突告警与待确认

## 确定性内核
- `scripts/profile.py <data.csv> --config <cfg.json>`：自动跑组合键审计、语义推断、血缘、空白语义、冲突告警，生成 12 节画像；
- `scripts/verify_profile.py`：验收 12 节 + 层级发现 + 无 target 误判。

## 合规红线（2026 国赛，详见 references/2026-compliance.md）
- 核心建模与分析由参赛队主导，AI 产物须逐项人工审查核实后方可采纳
- 赛期禁止搜当届赛题实时解答；引用公开资料须列参考文献
- 本环节产出仅作草稿，最终须人工核验；AI 使用记入 ai_usage_log.md
