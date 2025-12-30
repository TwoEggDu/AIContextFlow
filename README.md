# project-passport

把“AI 协作”从临时对话升级为可复用、可版本化的工程能力。

**核心能力：**
- 为其他项目提供 `.project/` 规范（ledger / decisions / current_intent + schemas）
- ADR 模板与索引（docs/adr + .project/decisions.json）
- Context Pack 生成：把本地代码/文档打包成 AI 可快速消费的最小上下文

## Quickstart

### 1) 把一个项目“纳入协作规范”
```bash
python -m project_passport.cli init-project --project-root .
```

### 2) 导出 Context Pack
```bash
python -m project_passport.cli export --config export_config.json
```

### 3) 生成 PROMPT 并复制 governance（可选）
```bash
python -m project_passport.cli pack --project-root . --out ./_export --task "..." --do-not-do "..." --copy-governance
```

ai-context-flow/
├─ ai_context_flow/
│  ├─ exporter.py
│  ├─ packer.py
│  ├─ validator.py
│  ├─ cli.py
│  └─ __init__.py
├─ .project/
│  ├─ ledger.json
│  ├─ decisions.json
│  └─ current_intent.json
├─ docs/
│  ├─ adr/
│  │  └─ ADR-001-context-as-contract.md
│  └─ spec/
│     └─ flow-design.md
├─ configs/
│  └─ export_config.json
└─ README.md

