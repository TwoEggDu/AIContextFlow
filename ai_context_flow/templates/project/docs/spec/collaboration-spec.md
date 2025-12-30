# 项目协作规范（由 AIContextFlow 注入）

建议在项目 README 或 docs/spec 中引用以下约束：

- `.project/ledger.json`：长期事实与协作风格（项目宪法）
- `.project/decisions.json` + `docs/adr/`：架构/流程决策（ADR）
- `.project/current_intent.json`：本次协作约束（临时宪法）

原则：**accepted ADR 是硬约束**，除非本次 intent 明确要推翻并新增 superseding ADR。
