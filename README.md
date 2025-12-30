# AIContextFlow

AIContextFlow 是一个“协作基础设施仓库”：

- 为其他项目提供 `.project/` 规范（ledger / decisions / current_intent + schemas）
- 提供 ADR 模板与索引方式（accepted = 硬约束）
- 生成 Context Pack：把你本地的代码/文档/决策打包成 AI 可稳定消费的最小上下文
- 为未来 MCP 扩展预留空间（但 v0.1 尽量 stdlib-only）

> 目标：让 AI 从“外包”升级为“正式成员”——行为可预测、遵循约束、可持续接手。

## 目录一眼看懂

- `.project/`：本仓库的长期事实、决策索引、本次意图（以及 schemas）
- `docs/adr/`：本仓库自己的 ADR（并在 `.project/decisions.json` 里索引）
- `ai_context_flow/templates/project/`：给其他项目注入的模板（.project + ADR template）
- `ai_context_flow/exporter.py`：导出 Context Pack（bundle/index/manifest/summary/tree）
- `ai_context_flow/packer.py`：生成 `PROMPT.md` + 可选复制 `.project` 与 accepted ADR
- `configs/export_config.json`：导出配置示例

## 安装/运行（零依赖）

直接在仓库根目录：

```bash
python -m ai_context_flow.cli -h
```

如果你愿意安装成命令（可选）：

```bash
pip install -e .
aiflow -h
```

## 常用工作流

### 1) 把一个项目“纳入规范”（生成 .project + ADR 模板）

```bash
python -m ai_context_flow.cli init-project --project-root .
```

### 2) 导出 Context Pack（bundles + index + manifest + summary/tree）

在目标项目里准备 `export_config.json`（可参考本仓库 `configs/export_config.json`），然后：

```bash
python -m ai_context_flow.cli export --config export_config.json
```

### 3) 生成 PROMPT（可粘贴给 ChatGPT/Copilot Chat）

```bash
python -m ai_context_flow.cli pack --project-root . --out ./_export   --task "实现 svn_ops.update() 的结构化返回"   --do-not-do "不引入新依赖"   --copy-governance
```

`_export/` 里会出现 `PROMPT.md`，你直接复制内容到对话开头即可。

## 输出格式（稳定）

见 ADR：`docs/adr/ADR-002-context-pack-format.md`
