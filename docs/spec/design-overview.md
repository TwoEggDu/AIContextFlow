# AIContextFlow 设计概览

AIContextFlow 做三件事：
1) **规范化**：为每个项目提供 `.project/`（ledger/decisions/current_intent）与 schema
2) **决策化**：用 ADR 把“为什么这样做”钉住（accepted = 硬约束）
3) **上下文化**：把项目的“当前可用上下文”导出为 Context Pack，让 AI 稳定接手

> Flow 的含义：上下文在 “代码/文档 ⇄ Pack ⇄ 对话 ⇄ 决策 ⇄ 回写” 之间流动。
