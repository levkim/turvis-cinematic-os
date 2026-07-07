#!/usr/bin/env python3
"""
TURVIS Project Wizard CLI v0.2

Creates a new video project folder with project.yaml and narration.md.

Local-first. No AI API calls.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

VALID_CATEGORIES = [
    "adventure",
    "ski-travel",
    "trekking",
    "avalanche-safety",
    "wfr",
    "travel-promotion",
    "shorts-reels",
]


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9가-힣]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "untitled-project"


def make_prefix(slug: str) -> str:
    ascii_parts = [p for p in re.split(r"[-_\s]+", slug) if p and p.isascii()]
    if ascii_parts:
        return "-".join(part[:2].upper() for part in ascii_parts[:3])
    return "TV-PR"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a TURVIS video project folder")
    parser.add_argument("--title", required=True, help="Project title")
    parser.add_argument("--id", default=None, help="Project ID / slug. Defaults to slugified title")
    parser.add_argument("--category", default="adventure", choices=VALID_CATEGORIES, help="Video category")
    parser.add_argument("--type", default="video", help="Project type")
    parser.add_argument("--genre", default="auto", help="Video genre. Defaults to category auto selection")
    parser.add_argument("--country", default="unknown", help="Country")
    parser.add_argument("--region", default="unknown", help="Region")
    parser.add_argument("--destination", default="unknown", help="Destination")
    parser.add_argument("--route", default="unknown", help="Route")
    parser.add_argument("--duration", type=int, default=240, help="Target duration in seconds")
    parser.add_argument("--aspect", default="16:9", help="Aspect ratio")
    parser.add_argument("--resolution", default="3840x2160", help="Resolution")
    parser.add_argument("--language", default="ko", help="Language")
    parser.add_argument("--root", default="projects", help="Projects root folder")
    parser.add_argument("--force", action="store_true", help="Overwrite existing project files")
    return parser.parse_args()


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"File already exists: {path}. Use --force to overwrite.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_project_yaml(args: argparse.Namespace, project_id: str, project_dir: Path) -> str:
    prefix = make_prefix(project_id)
    safe_project_id = project_id.replace("/", "-")

    return f"""project:
  id: {safe_project_id}
  title: {args.title}
  type: {args.type}
  status: draft
  category: {args.category}
  genre: {args.genre}
  clip_prefix: {prefix}
  episode: episode-01

output:
  aspect_ratio: "{args.aspect}"
  resolution: "{args.resolution}"
  target_duration_seconds: {args.duration}
  language: {args.language}

style:
  references:
    - cinematic travel film
    - premium educational video
    - high-end adventure edit
  mood:
    - cinematic
    - clear
    - purposeful

locations:
  country: {args.country}
  region: {args.region}
  destination: {args.destination}
  route: {args.route}

paths:
  footage: assets/{safe_project_id}/raw
  keyframes: assets/{safe_project_id}/keyframes
  memory: knowledge/footage/{safe_project_id}
  narration: {project_dir.as_posix()}/narration.md
  director_handoff: {project_dir.as_posix()}/director-handoff.md

rules:
  generate_audio: false
  generate_music: false
  generate_sound_effects: false
  local_first: true
"""


def build_narration_md(title: str) -> str:
    return f"""# Narration — {title}

Paste narration text here.

```text
[00:00-00:20]
Narration segment...
```
"""


def build_readme(title: str, project_id: str, category: str) -> str:
    return f"""# {title}

Project ID: `{project_id}`  
Video Category: `{category}`

## Workflow

Run full pipeline:

```bash
python apps/turvis-studio/turvis.py pipeline --project-folder projects/{project_id} --include-review
```

Preview:

```bash
python apps/turvis-studio/turvis.py preview
```
"""


def main() -> None:
    args = parse_args()
    project_id = args.id or slugify(args.title)
    project_dir = Path(args.root) / project_id

    project_yaml = build_project_yaml(args, project_id, project_dir)
    narration_md = build_narration_md(args.title)
    readme_md = build_readme(args.title, project_id, args.category)

    write_file(project_dir / "project.yaml", project_yaml, args.force)
    write_file(project_dir / "narration.md", narration_md, args.force)
    write_file(project_dir / "README.md", readme_md, args.force)

    print(f"Project created: {project_dir}")
    print(f"Category: {args.category}")
    print(f"Next: edit {project_dir / 'project.yaml'}")


if __name__ == "__main__":
    main()
