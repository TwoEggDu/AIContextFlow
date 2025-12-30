# ADR-001: .project + ADRs are the collaboration contract

## Context
长期协作时，最大的风险不是“AI 不够聪明”，而是“约束不明确导致反复发散/推翻”。
我们需要一个既可人读、又可机器读的协作合同，让 AI 每次接手都能快速进入“正式成员模式”。

## Options
1. 只依赖聊天记录与口头约定
2. 只用 Markdown 文档（人读友好，但机器加载成本高）
3. `.project/`（机器入口）+ `docs/adr/`（人读可审）组合

## Decision
- Chosen: **Option 3**
- Status: **accepted**

## Rationale
- `.project/` 提供稳定入口：ledger/decisions/current_intent
- ADR 记录“为什么”，防止重复争论
- 对多项目可复用、可版本化

## Consequences
- 协作稳定性提升，但需要维护少量元数据文件
