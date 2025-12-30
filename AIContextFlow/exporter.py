"""
project_passport.exporter

从你现有 export 脚本演进而来：
- 兼容原有 export_config.json 结构
- 启用 limits.max_file_bytes（原脚本里配置存在但未生效）
- 输出 index.txt（人读）+ index.json（机器读）
- 对 read_error / skipped_large 做显式记录
"""

from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
from collections import Counter

FILE_HEADER_TMPL = "\n\n===== FILE: {path} =====\n"


def load_config(path: Path) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sha256_short(path: Path, n: int = 12) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:n]


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


@dataclass
class FileRecord:
    rel: str
    size_bytes: int
    sha12: str
    bundle: Optional[str] = None
    status: str = "ok"  # ok | read_error | skipped_large
    error: Optional[str] = None


def collect_paths(root: Path, cfg: Dict) -> List[Path]:
    include_dirs = [root / d for d in cfg["include"]["dirs"]]
    ex_dirs = set(cfg.get("exclude", {}).get("dirs", []))
    ex_files = set(cfg.get("exclude", {}).get("files", []))
    exts = set(cfg["include"]["extensions"])

    paths: List[Path] = []
    for inc in include_dirs:
        if not inc.exists():
            continue
        for p in inc.rglob("*"):
            if not p.is_file():
                continue
            if p.name in ex_files:
                continue
            if p.suffix not in exts:
                continue
            if any(part in ex_dirs for part in p.parts):
                continue
            paths.append(p)

    return sorted(paths, key=lambda x: str(x.relative_to(root)).lower())


def write_manifest(out_dir: Path, cfg: Dict, records: List[FileRecord]) -> None:
    skipped_large = [r.rel for r in records if r.status == "skipped_large"]
    read_errors = [r.rel for r in records if r.status == "read_error"]

    manifest = {
        "root": str(Path(cfg["root"]).resolve()),
        "file_count": len(records),
        "ok_count": sum(1 for r in records if r.status == "ok"),
        "skipped_large_count": len(skipped_large),
        "read_error_count": len(read_errors),
        "skipped_large": skipped_large,
        "read_errors": read_errors,
        "config": cfg,
    }
    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def export_bundles(
    root: Path,
    out_dir: Path,
    paths: List[Path],
    *,
    max_bytes: int,
    encoding: str,
    max_file_bytes: int,
) -> List[FileRecord]:
    index_lines: List[str] = []
    index_rows: List[FileRecord] = []

    bundle_id = 1
    cur_bytes = 0
    bundle_path = out_dir / f"bundle_{bundle_id:04d}.txt"
    bundle_fp = open(bundle_path, "w", encoding=encoding, newline="\n")

    def new_bundle():
        nonlocal bundle_id, cur_bytes, bundle_fp, bundle_path
        bundle_fp.close()
        bundle_id += 1
        cur_bytes = 0
        bundle_path = out_dir / f"bundle_{bundle_id:04d}.txt"
        bundle_fp = open(bundle_path, "w", encoding=encoding, newline="\n")

    for p in paths:
        rel = p.relative_to(root)
        size_bytes = p.stat().st_size
        sha12 = sha256_short(p)
        rec = FileRecord(rel=str(rel), size_bytes=size_bytes, sha12=sha12)

        if max_file_bytes > 0 and size_bytes > max_file_bytes:
            rec.status = "skipped_large"
            index_rows.append(rec)
            index_lines.append(f"{rec.rel}\t{rec.size_bytes}\t{rec.sha12}\t-\t{rec.status}")
            continue

        header = FILE_HEADER_TMPL.format(path=str(rel))
        try:
            content = p.read_text(encoding=encoding)
        except Exception as e:
            rec.status = "read_error"
            rec.error = str(e)
            content = f"<<FAILED TO READ FILE: {e}>>"

        block = header + content
        block_size = len(block.encode(encoding))

        if cur_bytes > 0 and cur_bytes + block_size > max_bytes:
            new_bundle()

        rec.bundle = f"bundle_{bundle_id:04d}.txt"
        bundle_fp.write(block)
        cur_bytes += block_size

        index_rows.append(rec)
        index_lines.append(f"{rec.rel}\t{rec.size_bytes}\t{rec.sha12}\t{rec.bundle}\t{rec.status}")

    bundle_fp.close()

    (out_dir / "index.txt").write_text("\n".join(index_lines), encoding=encoding)
    (out_dir / "index.json").write_text(json.dumps([r.__dict__ for r in index_rows], ensure_ascii=False, indent=2), encoding="utf-8")
    return index_rows


def generate_summary(root: Path, paths: List[Path], out_dir: Path, *, top_n: int = 5) -> None:
    lines: List[str] = []
    lines.append("Project")
    lines.append(f"- Name: {root.name}")
    lines.append("")

    ext_counter = Counter(p.suffix.lower() for p in paths if p.suffix)
    lines.append("Languages")
    for ext, cnt in ext_counter.most_common():
        lines.append(f"- {ext}: {cnt} files")
    lines.append("")

    entry_candidates = []
    for p in paths:
        name = p.name.lower()
        if name.endswith("_cli.py") or name in ("main.py", "app.py"):
            entry_candidates.append(p.relative_to(root))

    lines.append("Entry Points")
    if entry_candidates:
        for p in entry_candidates:
            lines.append(f"- {p}")
    else:
        lines.append("- (none detected)")
    lines.append("")

    size_rank = sorted(paths, key=lambda p: p.stat().st_size, reverse=True)[:top_n]
    lines.append("Key Modules (by file size)")
    for p in size_rank:
        rel = p.relative_to(root)
        lines.append(f"- {rel} ({p.stat().st_size} bytes)")
    lines.append("")

    (out_dir / "summary.txt").write_text("\n".join(lines), encoding="utf-8")


def generate_tree(root: Path, paths: List[Path], out_dir: Path, *, max_depth: int = 4) -> None:
    rel_paths = [p.relative_to(root) for p in paths]
    tree = {}

    for rel in rel_paths:
        cur = tree
        for part in rel.parts[:-1]:
            cur = cur.setdefault(part + "/", {})
        cur.setdefault(rel.parts[-1], None)

    lines: List[str] = []

    def walk(node, prefix="", depth=0):
        if depth > max_depth:
            return
        items = sorted(node.items(), key=lambda x: x[0])
        for i, (name, child) in enumerate(items):
            last = (i == len(items) - 1)
            branch = "└─ " if last else "├─ "
            lines.append(prefix + branch + name)
            if isinstance(child, dict):
                ext = "   " if last else "│  "
                walk(child, prefix + ext, depth + 1)

    lines.append(f"{root.name}/")
    walk(tree)
    (out_dir / "tree.txt").write_text("\n".join(lines), encoding="utf-8")


def run_export(config_path: Path) -> Path:
    cfg_path = config_path.resolve()
    cfg_dir = cfg_path.parent
    cfg = load_config(cfg_path)

    root = (cfg_dir / cfg["root"]).resolve()
    out_dir = (cfg_dir / cfg["output_dir"]).resolve()
    ensure_dir(out_dir)

    paths = collect_paths(root, cfg)

    max_file_bytes = int(cfg.get("limits", {}).get("max_file_bytes", 0) or 0)
    records = export_bundles(
        root=root,
        out_dir=out_dir,
        paths=paths,
        max_bytes=int(cfg["bundle"]["max_bytes"]),
        encoding=cfg["bundle"].get("encoding", "utf-8"),
        max_file_bytes=max_file_bytes,
    )

    write_manifest(out_dir, cfg, records)

    if cfg.get("output", {}).get("emit_summary", False):
        generate_summary(root, paths, out_dir)
    if cfg.get("output", {}).get("emit_tree", False):
        generate_tree(root, paths, out_dir)

    return out_dir
