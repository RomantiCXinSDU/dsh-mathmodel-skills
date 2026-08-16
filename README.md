# dsh-mathmodel-skills

**面向全国大学生数学建模竞赛（CUMCM）C 题的 6 个 DeepSeek Harness (DSH) Agent Skills**——从"数据概况 → 数据规则 → 结构识别与专业方法匹配 → 模型发散 → 形式化 → 求解验证"的全流程武器库，内嵌 2026 国赛合规约束与确定性校验脚本。

> Six Agent Skills for the DSH (DeepSeek Harness) covering the full CUMCM Problem-C workflow: data profiling, data rules, structure-to-method matching (a 45-class professional method arsenal), model exploration, formalization, and solve-and-verify — with deterministic verifiers and 2026 CUMCM compliance built in.

---

## ✨ 特性

- **6 个 skill，一条流水线**：数据概况 → 数据规则 → 结构识别/方法匹配 → 三派发散 → 正式建模 → 求解验证；
- **专业方法武器库 v2.0**：45+ 类专业方法（生存分析/混合效应/分位数回归/CoDA/排队论/报童模型/异常检测/因果推断……），按"结构信号 → 方法 → 评委解释句"检索；
- **确定性机制**：每个 skill 带可运行脚本 + 校验器（10 项画像校验、10 条规则校验、3派×14点校验、12项规格校验、数字溯源/符号一致/可复现/合规审计、返工上限与冻结状态机）；
- **机器管正确、人管判断**：论文数字必须有来源、符号必须与代码一致、程序必须可复现；
- **2026 国赛合规内嵌**：AI 工具使用声明、附录源程序要求、联网边界（可查资料/用 AI，禁止抄当届实时解答、禁止与队外讨论）逐条写入每个 skill；
- **零依赖门槛**：skill 本体是 Markdown + Python 标准库/pandas，Python ≥ 3.10。

## 🗺️ 工作流

```text
题目 + 数据附件
   │
   ├─① 拆题（交给 Kimi/其他模型）→ problem_spec.md
   │
   ├─② data-profiler        → data_profile.md（10 项数据画像 + 图）
   ├─③ data-ruler           → data_rules.md（10 条数据规则，人工锁死）
   ├─④ data-pattern-to-method → method_matches.md（结构识别 → 专业方法匹配，带评委解释句）
   ├─⑤ model-explorer       → candidates.md（统计/机理/数据三派，每方案 14 点）
   ├─⑥ formalizer           → model_spec.md（12 项正式数学模型）
   └─⑦ solver-verifier      → 代码 + 自证 + 敏感性/误差/对比 + validation_report.md
                     【3 个人工关卡：锁规则 / 定主方案 / 终审冻结】
```

## 📦 安装（终端命令，任选其一）

### 方式 1：DSH 一键安装（Windows PowerShell）

```powershell
irm https://raw.githubusercontent.com/RomantiCXinSDU/dsh-mathmodel-skills/main/install.ps1 | iex
```

或手动：

```powershell
git clone https://github.com/RomantiCXinSDU/dsh-mathmodel-skills.git "$env:USERPROFILE\.dsh\skills"
```

### 方式 2：DSH 一键安装（Linux / macOS）

```bash
curl -fsSL https://raw.githubusercontent.com/RomantiCXinSDU/dsh-mathmodel-skills/main/install.sh | bash
```

或手动：

```bash
git clone https://github.com/RomantiCXinSDU/dsh-mathmodel-skills.git ~/.dsh/skills
```

### 方式 3：Claude Code / Codex 等 Agent Skills 工具

```bash
npx -y skills@latest add RomantiCXinSDU/dsh-mathmodel-skills --skill '*' --agent claude-code codex
```

### 方式 4：手动下载（任何环境）

```bash
git clone https://github.com/RomantiCXinSDU/dsh-mathmodel-skills.git
# 把 skills/ 下 6 个目录复制到你的 agent 的 skills 目录即可
```

> 安装后重启/新开会话，skill 即被自动发现；之后说"做数据概况""结构识别"等触发词即自动加载。

## 🚀 用法（赛时标准流程，直接照喊）

| 顺序 | 触发词 | Skill | 产出 |
|---|---|---|---|
| 1 | "做数据概况 / EDA / 读数据" | data-profiler | data_profile.md + 分布图 |
| 2 | "定数据规则 / 清洗口径" | data-ruler | data_rules.md（人工锁死）|
| 3 | "结构识别 / 该用什么专业方法" | data-pattern-to-method | method_matches.md（带评委解释句）|
| 4 | "发散模型 / 三派候选" | model-explorer | candidates.md |
| 5 | "正式建模 / 写数学模型" | formalizer | model_spec.md |
| 6 | "求解 / 验证 / 敏感性 / 误差分析" | solver-verifier | 代码 + 结果 + validation_report.md |

**一句口诀**：概况 → 规则 → 结构匹配 → 发散 → 形式化 → 求解验证；三个关卡人点头；数字全部有来源。

## 🧪 测试

每个 skill 自带校验器，可对任意 CSV 自测：

```bash
cd <skill>/scripts
python profile.py 你的数据.csv --config 你的配置.json   # data-profiler
python verify_profile.py                                 # 验收 10 项画像
python match_methods.py 你的数据.csv --config 你的配置.json  # 结构识别→方法匹配
```

配置 JSON 示例（指定目标列/ID列/题目语义信号）：

```json
{ "target_col": "AB异常", "id_col": "ID", "event_hint": true, "error_required": true }
```

支持的语义信号：event_hint（事件时间）、error_required（误差影响）、quantile_hint（达标线）、queue（排队）、inventory（库存）、game（博弈）、mechanism（机理）、evaluation（评价）、ordinal（有序分类）、spatial（空间）、censored（删失）。

## 📐 2026 国赛合规（已内嵌进每个 skill）

- 核心建模与分析由参赛队主导，AI 参与内容逐项人工审查核实；
- 论文参考文献前设「AI 工具使用声明」，用 AI 附《AI工具使用详情.pdf》；
- 附录含全部可运行源程序，程序须可复现；
- 联网边界：✅ 可联网查资料/用 AI；❌ 禁止抄当届赛题实时解答、禁止与队外讨论赛题。

## 🗂️ 目录结构

```text
skills/
├── data-profiler/          # SKILL.md + scripts(profile/verify) + references + templates
├── data-ruler/             # SKILL.md + scripts(rules/verify) + references + templates
├── data-pattern-to-method/ # SKILL.md + scripts(match_methods/verify) + 武器库 v2.0
├── model-explorer/         # SKILL.md + scripts(recommend/verify×2) + 60+方法目录
├── formalizer/             # SKILL.md + scripts(spec_scaffold/verify) + 12项模板
└── solver-verifier/        # SKILL.md + scripts(校验×4+状态机) + 求解/敏感性 SOP
docs/                       # 使用手册、工作章程
install.sh / install.ps1    # 一键安装
LICENSE                     # MIT
```

## ⚠️ 说明

- 本技能包是**辅助工具**，不替代参赛队主导；模型选择与结论由队伍人工核验负责；
- 每个 skill 的确定性脚本不依赖任何大模型 API，可用纯 Python 独立运行验证；
- 武器库方法条目为"结构识别 → 方法匹配"参考，实际使用须结合当年赛题与数据。

## 📄 License

[MIT](LICENSE)