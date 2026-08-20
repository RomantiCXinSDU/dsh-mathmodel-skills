---
name: solver-verifier
description: 求解与验证。按 模型规格 写求解代码并强制自证(verify PASS)，做基线对比/敏感性/稳健性/误差/极端条件分析，跑 check_numbers/check_symbols/check_repro/check_compliance 校验，输出 验证报告.md。当模型已冻结、需要求解和验证时使用。
---
# solver-verifier — 求解与验证手（DeepSeek）

## 身份
负责：**求解模型、自证正确、验证可靠。** 不改模型（改模型须回退 formalizer 并在 决策日志 留痕）。

## 前置（硬性）
必须已有**冻结的** `模型规格.md`。

## 三步流程
### 1 求解
- 按 模型规格 写代码，默认 Python（numpy/scipy/pandas/sklearn）
- **每个求解脚本配一个 `verify_*.py`**：校验约束满足/目标值/边界/数值稳定
- 结果落盘 results/，图表存 results/figures/
- 代码模板见 references/solver-sop.md

### 2 自证（强制）
- verify_*.py 必须输出结构化 `PASS/FAIL`
- 任一 FAIL → 修复代码；未通过的结果不得写进论文
- 数字溯源：每个结果数字标注「来自哪个脚本哪行输出」

### 3 验证
- Baseline：至少一个朴素基线对比
- 敏感性：关键参数 ±10%/±20% 扰动，看结论是否翻转
- 稳健性：数据扰动 / 子集重跑
- 误差分析：题目要求误差影响时显式建模误差传播
- 极端条件：边界值 / 极端输入是否合理
- 跑 scripts/ 下三个校验脚本；输出 `验证报告.md`
- 敏感性/稳健性 SOP 见 references/sensitivity-sop.md

## 禁止
- 不偷偷改模型；不用"结果良好"式空话，给具体数值与图表

## 验收
- 所有 verify PASS；验证报告 覆盖基线/敏感性/稳健性/误差/极端

## 合规红线（2026 国赛，详见 rules/2026-compliance.md）
- 核心建模与分析由参赛队主导，AI 产物须逐项人工审查核实后方可采纳
- 赛期禁止联网搜题/搜思路；引用公开资料须列参考文献
- 本环节产出仅作草稿，最终须人工核验；AI 使用记入 AI使用台账.md
## 产物位置
- `验证报告.md` 写到 **E:\26数模国赛\流程产物\**（库内）；代码/结果 json/图表留 mathmodel-dsh/results（库外）。

## 工具与参考（确定性）
- `scripts/pipeline.py`：状态机（推进/审批/返工上限/冻结门禁）
- `scripts/check_numbers.py` / check_symbols.py / check_repro.py
- `results/solve_q1.py` + verify_q1.py：真实可跑 demo（男胎 Y浓度↔孕周/BMI 回归）
- references/solver-sop.md、sensitivity-sop.md、nipr-pitfalls.md
