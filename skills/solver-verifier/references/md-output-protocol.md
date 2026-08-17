# md 输出协议（所有 .md 产出统一遵守）

## 统一 YAML frontmatter
\`\`\`yaml
---
type: <data-profile|data-rules|method-candidates|candidates|decision-log|critique-log|model-spec|validation-report|traceability|ai-usage-log>
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
- 要求链接：[[problem_spec#R1.1]]（覆盖哪些要求）
- 规则链接：[[data_rules#规则 12]]
- 方法链接：[[method_candidates#MC-02]]
- 上游/下游放在 YAML frontmatter。

## 各文件 frontmatter 默认值
| 文件 | type | owner |
|---|---|---|
| data_profile.md | data-profile | deepseek |
| data_rules.md | data-rules | deepseek |
| method_candidates.md | method-candidates | deepseek |
| candidates.md | candidates | deepseek |
| decision_log.md | decision-log | human |
| critique_log.md | critique-log | gpt |
| model_spec.md | model-spec | deepseek |
| validation_report.md | validation-report | deepseek |
| traceability.md | traceability | human |
| ai_usage_log.md | ai-usage-log | deepseek |
