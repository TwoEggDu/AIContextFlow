# ADR-001: .project + ADRs act as the collaboration contract

## Context
长期协作时，最大的风险不是“忘记”，而是“约束不明确导致反复发散/推翻”。
需要一个既可人读、又可机器读的“协作合同”，在每次协作时快速注入上下文。

## Options
1. 只依赖聊天记录与口头约定
2. 只用 Markdown 文档
3. `.project/`（机器入口）+ `docs/adr/`（人读可审）组合

## Decision
- Chosen: **Option 3**
- Status: **accepted**

## Rationale
- `.project/` 提供稳定、可程序化加载的入口（ledger/decisions/current_intent）
- `docs/adr/` 记录“为什么”，防止重复争论

## Consequences
- 协作稳定性提升，但需要维护少量元数据
