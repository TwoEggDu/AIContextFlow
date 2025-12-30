# ADR-002: Context Pack export format (manifest/index/bundles/summary/tree)

## Context
AI 需要“足够的上下文”，但全仓库导入会产生噪声和漂移。
我们需要一个小而稳定的导出格式，既能人读，也能被脚本/未来 MCP 消费。

## Decision
- Chosen: 输出以下文件集合
- Status: **accepted**

## Format
- `manifest.json`: 导出摘要与配置回显
- `index.txt`: 人读索引（tsv）
- `index.json`: 机器读索引（结构化）
- `bundle_*.txt`: 代码/文档拼接包（用于粘贴/上传）
- `summary.txt`: 可选：工程概览
- `tree.txt`: 可选：目录树
- `PROMPT.md`: 可选：可直接粘贴给 ChatGPT/Copilot Chat 的提示词

## Consequences
- 导出可预测、稳定；后续新增字段只能“追加”，不能破坏兼容
