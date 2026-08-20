---
name: cumcm-markdown-protocol
description: CUMCM 多智能体流水线的 Markdown/Obsidian 输出协议。所有流程产物（拆题报告、数据概况、数据规则、方法候选、candidate_*、评审报告、决策日志 等 .md）落盘时必须遵守的统一 YAML frontmatter 与 wikilink 链路规范，保证 Obsidian 中可追溯"题目要求→候选模型→评审→人工决策"。当在数模流水线中创建或修改任何流程 .md 文件时使用。
---

# cumcm-markdown-protocol — 输出链路协议（全 Agent 共用）

## 定位
不增加任何科研知识。只负责一件事：**所有流程 .md 落盘时自动把 Obsidian 链路搭好。**

## 统一 YAML（每个流程文件必带）
```yaml
---
type:           # 产物类型，如 problem-spec / data-profile / data-rules / method-候选方案 / candidate / model-review / decision-log
stage:          # 阶段，如 problem-analysis / data-profiling / model-exploration / model-review
owner:          # 产出者：kimi / deepseek / gpt / human
status:         # draft / review / frozen
upstream:       # 本文件读了谁（wikilink 列表，无则 []）
downstream:     # 谁会读本文件（wikilink 列表，无则 []）
---
```

## 示例
Problem Analyst 的 拆题报告.md：
```yaml
---
type: problem-spec
stage: problem-analysis
owner: kimi
status: review
upstream: []
downstream:
  - "[[数据概况]]"
  - "[[数据规则]]"
---
```
Model Reviewer 的 评审报告.md：
```yaml
---
type: model-review
stage: model-review
owner: kimi
status: review
upstream:
  - "[[拆题报告]]"
  - "[[数据规则]]"
  - "[[方法候选]]"
  - "[[候选_A1]]"
downstream:
  - "[[决策日志]]"
---
```

## Requirement 级链接
小问要求编号 R1.1、R2.2 全流水线保持稳定、不得重编。引用粒度到 R 级：
```markdown
- [[拆题报告#R1.1]]
- [[拆题报告#R2.2]]
```

## 铁律：决策日志.md 是 human-only
```yaml
owner: human
```
任何 AI（含 Kimi）：**可读、可引用；不得创建、不得修改、不得覆盖**。淘汰/选择/组合/修改/MAIN/BACKUP 只能由人写进去。

## 验收
落盘前自查：YAML 六字段齐全；owner 正确；up/downstream 用 wikilink；引用了 R 编号的地方用 `[[拆题报告#Rn.n]]` 格式。
