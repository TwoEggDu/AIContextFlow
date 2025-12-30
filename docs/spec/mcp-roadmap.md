# MCP 方向（占位）

当前 AIContextFlow 提供“类 MCP 的最小闭环”：
- 结构化上下文（.project）
- 决策记录（ADR）
- 上下文打包（Context Pack）

后续如果接入 MCP（或自研 Server）：
- 建议以插件方式扩展（如 `ai_context_flow/plugins/`）
- 核心 exporter/packer 的输出格式保持 ADR-002 兼容
