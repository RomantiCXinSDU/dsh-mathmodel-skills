# dsh-mathmodel-skills

**CUMCM（全国大学生数学建模竞赛）多智能体流水线技能包** —— 9 个 Agent Skills，把"拆题 → 数据 → 侦察 → 发散 → 评审 → 决策 → 形式化 → 求解验证"拆成各司其职的环节技能，适配 Kimi / DeepSeek / GPT / Claude / Codex 等任何兼容 SKILL.md 协议的 Agent。

> 设计理念：**AI 负责发散与审查，人负责拍板。** 选模权、组合权、决策权全部保留给人工关卡；每个环节的产出都是带 YAML frontmatter 和 Obsidian wikilink 的落盘文件，全流程可追溯。

## 功能一览

```
① 拆题(Kimi)      拆题报告.md        把题目看准：R 编号 / 七类数学元素 / 歧义清单
② 数据概况(DSH)   数据概况.md        只写事实的 12 项数据画像
③ 数据规则(DSH)   数据规则.md          18 条数据对建模的限制 + 充分性判断
══ 关卡1（人工锁定）══
④ 方法侦察(DSH)   方法候选.md   数据特殊结构 → 专业方法候选（文献验证）
⑤ 模型发散(DSH)   候选_A1…C3.md     6~9 个候选 × 17 项卡，只发散不选模
   评审(Kimi)     评审报告.md        14 维差异分析 + 换皮检查 + 互补分析（无选模权）
══ 关卡1.5（人工选模/组合/修改）→ 决策日志.md（human-only）══
反方(GPT)        反方记录.md        专攻 MAIN，≤2 轮
⑥ 形式化(DSH)     模型规格.md          12 项唯一正式版，禁重新发散
终审(GPT)        终审报告                题目↔模型 / 假设↔方程 / 变量↔约束 / 小问↔子模型
══ 关卡2（人工核验）→ MODEL FREEZE ══
⑦ 求解验证(DSH)   验证报告.md   求解+自证+敏感性/稳健性/误差 + 校验脚本
```

## 技能清单

| Skill | 角色 | 输入 → 输出 |
|---|---|---|
| `cumcm-problem-spec` | ① 拆题（Kimi） | 赛题全文+附件 → 拆题报告.md |
| `data-profiler` | ② 数据概况（DeepSeek） | 数据附件 → 数据概况.md |
| `data-ruler` | ③ 数据规则（DeepSeek） | 数据概况 → 数据规则.md |
| `professional-method-scout` | ④ 方法侦察（DeepSeek） | 数据特殊结构 → 方法候选.md |
| `model-explorer` | ⑤ 模型发散（DeepSeek） | 拆题报告+数据规则 → candidate_*.md |
| `cumcm-model-review` | 评审（Kimi） | 全部上游 → 评审报告.md |
| `formalizer` | ⑥ 形式化（DeepSeek） | 决策日志+候选方案 → 模型规格.md |
| `solver-verifier` | ⑦ 求解验证（DeepSeek） | 模型规格 → 代码+结果+验证报告.md |
| `cumcm-markdown-protocol` | 全体共用 | YAML/wikilink/R 编号输出协议 |

每个技能自带：`SKILL.md`（纪律与流程）+ `references/`（检查清单、rubric、反模式）+ `templates/`（落盘模板）+ `scripts/`（确定性验收脚本）。

## 安装（终端任选一种）

**方式一：skills CLI（推荐，支持 Claude Code / Codex 等）**
```bash
npx -y skills@latest add RomantiCXinSDU/dsh-mathmodel-skills --skill '*' --agent claude-code codex
```

**方式二：一键脚本**
```bash
# Linux / macOS
curl -fsSL https://raw.githubusercontent.com/RomantiCXinSDU/dsh-mathmodel-skills/main/install.sh | bash
# 自定义目标目录：bash install.sh ~/.claude/skills
```
```powershell
# Windows PowerShell
irm https://raw.githubusercontent.com/RomantiCXinSDU/dsh-mathmodel-skills/main/install.ps1 | iex
```

**方式三：手动**
```bash
git clone --depth 1 https://github.com/RomantiCXinSDU/dsh-mathmodel-skills.git
cp -r dsh-mathmodel-skills/skills/* <你的Agent技能目录>/
# Claude Code: ~/.claude/skills/   Codex: ~/.agents/skills/   Kimi: 受管 skills 目录
```

安装后**新开 Agent 会话**生效。

## 使用

对话中点名触发，例如：
```text
加载 cumcm-problem-spec，拆这道题（附赛题 PDF）
加载 model-explorer，基于 拆题报告 和 数据规则 发散候选模型
加载 cumcm-model-review，评审 候选_A1 到 C3
```

完整流程与关卡约定见 `docs/数模工作章程_SOP.md`；DeepSeek 侧细则见 `docs/DSH技能栈使用手册.md`。

## 合规声明（重要）

本技能包按 **2026 国赛 AI 使用规定** 设计：核心建模与决策由参赛队主导（三个人工关卡写死在流程里），AI 产物须逐项人工审查，AI 使用需记入 `AI使用台账` 并在论文附「AI 工具使用声明」。**赛期使用本包联网功能时，禁止检索当届赛题的思路与解答。**

## 自测

```bash
python test/test_full.py        # 全链路验收
python skills/cumcm-problem-spec/scripts/verify_拆题报告.py <file>
python skills/cumcm-model-review/scripts/verify_评审报告.py <file>
```

## 致谢

评审与拆题环节的部分检查清单吸收自以下公开仓库（MIT）：
[handsomeZR-netizen/mathmodel-skill](https://github.com/handsomeZR-netizen/mathmodel-skill)、
[davila7/claude-code-templates](https://github.com/davila7/claude-code-templates)（peer-review）。

## License

MIT — 自由使用、修改、分发，欢迎 Star / Issue / PR。
