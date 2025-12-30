"""
ai_context_flow.filters

集中管理 include/exclude 规则，避免 exporter 里逻辑膨胀。
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set


@dataclass(frozen=True)
class FilterRules:
    include_dirs: List[Path]
    include_exts: Set[str]
    exclude_dirs: Set[str]
    exclude_files: Set[str]


def build_rules(root: Path, cfg: Dict) -> FilterRules:
    include_dirs = [root / d for d in cfg["include"]["dirs"]]
    include_exts = set(cfg["include"]["extensions"])
    exclude_dirs = set(cfg.get("exclude", {}).get("dirs", []))
    exclude_files = set(cfg.get("exclude", {}).get("files", []))
    return FilterRules(
        include_dirs=include_dirs,
        include_exts=include_exts,
        exclude_dirs=exclude_dirs,
        exclude_files=exclude_files,
    )


def is_excluded(path: Path, rules: FilterRules) -> bool:
    if path.name in rules.exclude_files:
        return True
    # 任一路径段命中则排除（包含 .git/.svn 等）
    if any(part in rules.exclude_dirs for part in path.parts):
        return True
    return False
