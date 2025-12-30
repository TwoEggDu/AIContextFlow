"""
project_passport.validator

v0.1 轻校验：不引入第三方 jsonschema。
后续可加 optional dependency 做严格 JSON Schema 校验。
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Tuple, List


def _load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def validate_ledger(p: Path) -> Tuple[bool, List[str]]:
    d = _load(p)
    errs = []
    if "schema_version" not in d:
        errs.append("missing schema_version")
    proj = d.get("project")
    if not isinstance(proj, dict) or "name" not in proj or "intent" not in proj:
        errs.append("project.name & project.intent required")
    collab = d.get("collaboration")
    if not isinstance(collab, dict) or "style" not in collab:
        errs.append("collaboration.style required")
    return (len(errs) == 0, errs)


def validate_decisions(p: Path) -> Tuple[bool, List[str]]:
    d = _load(p)
    errs = []
    if "schema_version" not in d:
        errs.append("missing schema_version")
    if "adrs" not in d or not isinstance(d["adrs"], list):
        errs.append("adrs[] required")
    return (len(errs) == 0, errs)


def validate_intent(p: Path) -> Tuple[bool, List[str]]:
    d = _load(p)
    errs = []
    if "schema_version" not in d:
        errs.append("missing schema_version")
    goal = d.get("goal")
    if not isinstance(goal, dict) or "summary" not in goal:
        errs.append("goal.summary required")
    return (len(errs) == 0, errs)
