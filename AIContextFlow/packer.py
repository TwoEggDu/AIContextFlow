"""
project_passport.packer

补齐为“可直接投喂”的 Context Pack：
- 生成 PROMPT.md
- 可选复制目标项目 .project/ 与 accepted ADR
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List


PROMPT_TMPL = """# Context Pack Prompt (paste into ChatGPT/Copilot Chat)

You are collaborating on a long-term software project.

## Hard rules
- Treat status=accepted ADRs referenced by `.project/decisions.json` as hard constraints.
- Prefer explicit behavior over implicit guesses.
- Do not change public APIs unless explicitly requested.

## Inputs provided in this pack
- `manifest.json`, `index.json`, `summary.txt`, `tree.txt`
- `bundle_*.txt` (if present)
- `.project/*` (if included)

## Current task
{task}

## Do NOT do
{do_not_do}
"""

def write_prompt(out_dir: Path, *, task: str, do_not_do: List[str]) -> Path:
    text = PROMPT_TMPL.format(
        task=(task or "(fill in task)").strip(),
        do_not_do="\n".join(f"- {x}" for x in (do_not_do or ["(none)"]))
    )
    p = out_dir / "PROMPT.md"
    p.write_text(text, encoding="utf-8")
    return p


def _read_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def copy_governance(project_root: Path, out_dir: Path, *, include_adrs: bool = True) -> None:
    src_project = project_root / ".project"
    if src_project.exists():
        dst = out_dir / ".project"
        dst.mkdir(parents=True, exist_ok=True)
        for f in src_project.glob("*"):
            if f.is_file():
                (dst / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")

    if include_adrs:
        dec = src_project / "decisions.json"
        if dec.exists():
            d = _read_json(dec)
            accepted = [a for a in d.get("adrs", []) if a.get("status") == "accepted"]
            if accepted:
                dst_adr = out_dir / "docs" / "adr"
                dst_adr.mkdir(parents=True, exist_ok=True)
                for a in accepted:
                    rel_path = a.get("path", "")
                    src = project_root / rel_path
                    if src.exists() and src.is_file():
                        (dst_adr / src.name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
