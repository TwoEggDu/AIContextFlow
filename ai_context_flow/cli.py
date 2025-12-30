"""
AIContextFlow CLI (`aiflow`)

Commands:
- init-project: 将 `.project/` + `docs/adr/ADR-000-template.md` 注入到目标项目
- export:       按 export_config.json 导出 Context Pack（bundles/index/summary/tree）
- pack:         生成 PROMPT.md，并可选复制 `.project` + accepted ADR

Examples:
  aiflow init-project --project-root .
  aiflow export --config export_config.json
  aiflow pack --project-root . --out ./_export --task "..." --do-not-do "..." --copy-governance
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from .exporter import run_export
from .packer import copy_governance, write_prompt


def _copytree(src: Path, dst: Path, *, force: bool) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for p in src.rglob("*"):
        rel = p.relative_to(src)
        out = dst / rel
        if p.is_dir():
            out.mkdir(parents=True, exist_ok=True)
            continue

        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists() and not force:
            continue
        out.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")


def cmd_init_project(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).resolve()
    tpl = Path(__file__).resolve().parent / "templates" / "project"
    _copytree(tpl / ".project", project_root / ".project", force=args.force)
    _copytree(tpl / "docs" / "adr", project_root / "docs" / "adr", force=args.force)
    _copytree(tpl / "docs" / "spec", project_root / "docs" / "spec", force=args.force)
    print(f"[init-project] wrote .project/ + docs/adr/ + docs/spec/ into: {project_root}")


def cmd_export(args: argparse.Namespace) -> None:
    out_dir = run_export(Path(args.config))
    print(f"[export] done: {out_dir}")


def cmd_pack(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).resolve()
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    do_not_do: List[str] = args.do_not_do or []
    write_prompt(out_dir, task=args.task or "", do_not_do=do_not_do)

    if args.copy_governance:
        copy_governance(project_root, out_dir, include_adrs=not args.no_adrs)

    print(f"[pack] done: {out_dir}")


def main():
    ap = argparse.ArgumentParser("aiflow")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p0 = sub.add_parser("init-project", help="init .project/ + ADR template into a target project")
    p0.add_argument("--project-root", required=True)
    p0.add_argument("--force", action="store_true", help="overwrite existing files")
    p0.set_defaults(func=cmd_init_project)

    p1 = sub.add_parser("export", help="export a project into bundles/index/summary/tree")
    p1.add_argument("--config", required=True, help="export_config.json path")
    p1.set_defaults(func=cmd_export)

    p2 = sub.add_parser("pack", help="write PROMPT.md and optionally copy .project + accepted ADRs")
    p2.add_argument("--project-root", required=True)
    p2.add_argument("--out", required=True)
    p2.add_argument("--task", default="")
    p2.add_argument("--do-not-do", dest="do_not_do", action="append", default=[], help="repeatable")
    p2.add_argument("--copy-governance", action="store_true")
    p2.add_argument("--no-adrs", action="store_true")
    p2.set_defaults(func=cmd_pack)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
