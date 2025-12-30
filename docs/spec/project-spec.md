# Project Passport 规范（v0.1）

这个仓库的目标：把“AI 协作”从临时对话升级为可复用、可版本化的工程能力。

## 三层协作记忆
- `.project/ledger.json`：长期事实与协作风格（项目宪法）
- `.project/decisions.json` + `docs/adr/`：决策与理由（ADR）
- `.project/current_intent.json`：本次协作约束（临时宪法）

## Context Pack
Context Pack 是一组小而稳定的文件集合，用于给 AI 快速注入工程上下文（避免全仓库噪声）。

建议最小包含：
- `manifest.json` / `index.json` / `summary.txt` / `tree.txt`
- 相关源码（bundle_*.txt）
- `.project/*`
- 与任务相关的 accepted ADR
