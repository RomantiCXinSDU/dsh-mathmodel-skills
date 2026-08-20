# md 输出协议（所有 .md 产出统一遵守）

## 统一 YAML frontmatter
\`\`\`yaml
---
type: <data-profile|data-rules|method-candidates|candidates|decision-log|critique-log|model-spec|validation-report|要求追踪|ai-usage-log>
stage: <profiling|ruling|method-scout|exploration|judging|critique|formalization|verification>
owner: <deepseek|kimi|gpt|human>
status: <draft|review|locked|frozen>
upstream:
  - "[[上游文件名]]"
downstream:
  - "[[下游文件名]]"
---
\`\`\`

## 链接约定（Obsidian 兼容）
- 要求链接：[[问题拆解#R1.1]]（覆盖哪些要求）
- 规则链接：[[数据规则#规则 12]]
- 方法链接：[[方法候选#MC-02]]
- 上游/下游放在 YAML frontmatter。

## 各文件 frontmatter 默认值
| 文件 | type | owner |
|---|---|---|
| 数据概况.md | data-profile | deepseek |
| 数据规则.md | data-rules | deepseek |
| 方法候选.md | method-candidates | deepseek |
| 候选A1.md ~ 候选C3.md（每候选一文件） | candidate | deepseek |
| 模型评审.md | model-review | kimi |
| 选模决策.md | decision-log | human |
| 反方记录.md | critique-log | gpt |
| 正式模型.md | model-spec | deepseek |
| 验证报告.md | validation-report | deepseek |
| 要求追踪.md | 要求追踪 | human |
| AI使用台账.md | ai-usage-log | deepseek |

## 空白语义约定
- 数据概况/数据规则中对高空值字段标 RAW_BLANK/SEMANTIC_NORMAL/NOT_APPLICABLE/TRUE_MISSING 四类，禁止默认 true missing。
- 数据概况 §5 必须输出观察单位发现（Composite Key Audit 组合键唯一率链）。
