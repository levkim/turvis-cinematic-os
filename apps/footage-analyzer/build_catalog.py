#!/usr/bin/env python3
"""Build human-reviewable footage catalog files from footage-index.json."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from apps.common.project_config import get_nested, load_project_config  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build footage review catalog")
    parser.add_argument("--project-folder", required=True, help="Project folder containing project.yaml")
    return parser.parse_args()


def resolve_repo_path(value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(str(value)).expanduser()
    return path if path.is_absolute() else REPO_ROOT / path


def format_duration(value: Any) -> str:
    if value is None:
        return "unknown"
    try:
        return f"{float(value):.2f}s"
    except (TypeError, ValueError):
        return str(value)


def format_size(value: Any) -> str:
    try:
        size = float(value)
    except (TypeError, ValueError):
        return "unknown"
    units = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f"{size:.1f} {units[index]}"


def format_resolution(width: Any, height: Any) -> str:
    return f"{width}x{height}" if width and height else "unknown"


def clip_file_uri(footage_root: str | None, clip: dict[str, Any]) -> str:
    asset_path = clip.get("asset_path") or clip.get("filename") or ""
    if not asset_path:
        return ""
    path = Path(str(asset_path)).expanduser()
    if not path.is_absolute() and footage_root:
        path = Path(str(footage_root)).expanduser() / path
    try:
        return path.resolve().as_uri()
    except ValueError:
        return str(path)


def render_markdown(index: dict[str, Any]) -> str:
    project_title = get_nested(index, "project.title", "Untitled Project")
    clips = index.get("clips") or []
    lines = [
        f"# Footage Catalog - {project_title}",
        "",
        f"Footage root: `{index.get('footage_root', 'unknown')}`",
        "",
        "| Clip | Filename | Duration | Resolution | Size | Codec | Review Notes |",
        "|---|---|---:|---|---:|---|---|",
    ]
    for clip in clips:
        lines.append(
            "| "
            f"{clip.get('clip_id', 'TBD')} | "
            f"{str(clip.get('filename', 'TBD')).replace('|', '\\|')} | "
            f"{format_duration(clip.get('duration_seconds'))} | "
            f"{format_resolution(clip.get('width'), clip.get('height'))} | "
            f"{format_size(clip.get('size_bytes'))} | "
            f"{clip.get('codec', 'unknown')} |  |"
        )
    lines.extend([
        "",
        "## Review Guide",
        "",
        "Use this catalog to mark which clips are useful before trusting automated edit decisions.",
        "Suggested tags: hero, drone, person, movement, wide, detail, avoid, needs-cut.",
    ])
    return "\n".join(lines) + "\n"


def render_html(index: dict[str, Any]) -> str:
    project_title = str(get_nested(index, "project.title", "Untitled Project"))
    footage_root = index.get("footage_root")
    cards: list[str] = []
    for clip in index.get("clips") or []:
        clip_id = html.escape(str(clip.get("clip_id", "TBD")))
        filename = html.escape(str(clip.get("filename", "TBD")))
        duration = html.escape(format_duration(clip.get("duration_seconds")))
        resolution = html.escape(format_resolution(clip.get("width"), clip.get("height")))
        size = html.escape(format_size(clip.get("size_bytes")))
        codec = html.escape(str(clip.get("codec", "unknown")))
        src = html.escape(clip_file_uri(footage_root, clip), quote=True)
        cards.append(
            f"""
      <article class="clip-card">
        <video src="{src}" controls preload="metadata"></video>
        <div class="clip-body">
          <div class="clip-id">{clip_id}</div>
          <h2>{filename}</h2>
          <dl>
            <div><dt>Duration</dt><dd>{duration}</dd></div>
            <div><dt>Resolution</dt><dd>{resolution}</dd></div>
            <div><dt>Size</dt><dd>{size}</dd></div>
            <div><dt>Codec</dt><dd>{codec}</dd></div>
          </dl>
          <label>Review note</label>
          <textarea class="review-note" placeholder="hero / drone / person / avoid / narration beat..."></textarea>
        </div>
      </article>"""
        )

    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Footage Catalog - {html.escape(project_title)}</title>
  <style>
    body {{ margin: 0; background: #111; color: #f4f4f4; font-family: Arial, sans-serif; }}
    header {{ position: sticky; top: 0; z-index: 2; background: #181818; border-bottom: 1px solid #333; padding: 18px 24px; }}
    h1 {{ margin: 0 0 6px; font-size: 24px; }}
    header p {{ margin: 0; color: #aaa; font-size: 13px; }}
    main {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 18px; padding: 18px; }}
    .clip-card {{ background: #1b1b1b; border: 1px solid #333; border-radius: 6px; overflow: hidden; }}
    video {{ width: 100%; aspect-ratio: 16 / 9; background: #000; display: block; }}
    .clip-body {{ padding: 14px; }}
    .clip-id {{ color: #7ab7ff; font-size: 13px; font-weight: 700; margin-bottom: 6px; }}
    h2 {{ font-size: 16px; line-height: 1.35; margin: 0 0 12px; word-break: keep-all; }}
    dl {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px 12px; margin: 0 0 12px; }}
    dl div {{ min-width: 0; }}
    dt {{ color: #999; font-size: 11px; text-transform: uppercase; }}
    dd {{ margin: 2px 0 0; font-size: 13px; }}
    label {{ display: block; color: #ddd; font-size: 13px; margin-bottom: 6px; }}
    textarea {{ width: 100%; min-height: 74px; box-sizing: border-box; resize: vertical; background: #101010; color: #fff; border: 1px solid #444; border-radius: 4px; padding: 8px; font: inherit; }}
  </style>
</head>
<body>
  <header>
    <h1>Footage Catalog - {html.escape(project_title)}</h1>
    <p>{len(index.get('clips') or [])} clips / {html.escape(str(footage_root or 'unknown'))}</p>
  </header>
  <main>{''.join(cards)}
  </main>
</body>
</html>
"""


def write_catalog_outputs(index: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "footage-catalog.md").write_text(render_markdown(index), encoding="utf-8")
    (output_dir / "footage-catalog.html").write_text(render_html(index), encoding="utf-8")


def main() -> None:
    args = parse_args()
    config = load_project_config(project_folder=args.project_folder)
    memory_dir = resolve_repo_path(get_nested(config, "paths.memory"))
    if not memory_dir:
        raise ValueError("Missing paths.memory in project.yaml")
    index_path = memory_dir / "footage-index.json"
    if not index_path.exists():
        raise FileNotFoundError(f"Missing footage index: {index_path}")
    index = json.loads(index_path.read_text(encoding="utf-8"))
    write_catalog_outputs(index, memory_dir)
    print(f"Created: {memory_dir / 'footage-catalog.md'}")
    print(f"Created: {memory_dir / 'footage-catalog.html'}")


if __name__ == "__main__":
    main()