#!/usr/bin/env python3
"""
TURVIS Director Handoff CLI v0.2

Builds a Director-ready handoff package from Adventure Memory JSON files.

Local-first. No AI API calls.

Architecture rule:
Applications never know projects. Projects are data.
Prefer --project-folder or --project-spec over hard-coded project arguments.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from apps.common.project_config import get_nested, load_project_config  # noqa: E402

DEFAULT_STORY_BUCKETS = [
    "opening",
    "establishing",
    "threshold",
    "journey",
    "preparation",
    "discovery",
    "texture",
    "scale",
    "arrival",
    "camp",
    "reflection",
    "ending",
]


@dataclass
class HandoffSettings:
    memory_dir: Path
    output_path: Path
    project_title: str
    min_score: int
    exclude_avoid: bool
    include_review: bool
    per_bucket: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a TURVIS Director handoff package")

    parser.add_argument("--project-folder", default=None, help="Project folder containing project.yaml")
    parser.add_argument("--project-spec", default=None, help="Path to project.yaml")

    # Backward-compatible direct inputs.
    parser.add_argument("--memory", default=None, help="Folder containing footage memory JSON files")
    parser.add_argument("--project", default=None, help="Project name for the handoff")
    parser.add_argument("--output", default=None, help="Output markdown path")
    parser.add_argument("--min-score", type=int, default=0, help="Minimum overall score")
    parser.add_argument("--exclude-avoid", action="store_true", help="Exclude clips marked avoid")
    parser.add_argument("--include-review", action="store_true", help="Include clips still marked needs_review")
    parser.add_argument("--per-bucket", type=int, default=5, help="Maximum clips per story bucket")
    return parser.parse_args()


def resolve_settings(args: argparse.Namespace) -> HandoffSettings:
    config: dict[str, Any] = {}
    if args.project_folder or args.project_spec:
        config = load_project_config(args.project_folder, args.project_spec)

    memory_value = args.memory or get_nested(config, "paths.memory")
    if not memory_value:
        raise ValueError("Missing memory folder. Provide --memory or paths.memory in project.yaml")

    output_value = args.output or get_nested(config, "paths.director_handoff")
    memory_dir = Path(str(memory_value)).expanduser().resolve()
    output_path = Path(str(output_value)).expanduser().resolve() if output_value else memory_dir / "director-handoff.md"

    project_title = args.project or get_nested(config, "project.title", get_nested(config, "project.id", "Untitled Project"))

    return HandoffSettings(
        memory_dir=memory_dir,
        output_path=output_path,
        project_title=str(project_title),
        min_score=args.min_score,
        exclude_avoid=args.exclude_avoid,
        include_review=args.include_review,
        per_bucket=args.per_bucket,
    )


def load_records(memory_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(memory_dir.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            record["_json_path"] = str(path)
            records.append(record)
        except json.JSONDecodeError:
            continue
    return records


def is_eligible(record: dict[str, Any], settings: HandoffSettings) -> bool:
    scores = record.get("scores") or {}
    flags = record.get("flags") or {}

    if settings.exclude_avoid and flags.get("avoid", False):
        return False

    if not settings.include_review and flags.get("needs_review", False):
        return False

    if int(scores.get("overall") or 0) < settings.min_score:
        return False

    return True


def rank_record(record: dict[str, Any]) -> int:
    scores = record.get("scores") or {}
    flags = record.get("flags") or {}
    score = int(scores.get("overall") or 0)

    if flags.get("hero_shot"):
        score += 20
    if flags.get("needs_review"):
        score -= 10
    if flags.get("avoid"):
        score -= 100

    return score


def bucket_records(records: list[dict[str, Any]], settings: HandoffSettings) -> dict[str, list[dict[str, Any]]]:
    buckets: dict[str, list[dict[str, Any]]] = {bucket: [] for bucket in DEFAULT_STORY_BUCKETS}

    for record in records:
        if not is_eligible(record, settings):
            continue
        story_tags = [str(tag).lower() for tag in record.get("story_tags", [])]
        best_usage = [str(tag).lower() for tag in record.get("best_usage", [])]
        combined = set(story_tags + best_usage)

        for bucket in DEFAULT_STORY_BUCKETS:
            if bucket in combined:
                buckets[bucket].append(record)

    for bucket in buckets:
        buckets[bucket].sort(key=rank_record, reverse=True)
        buckets[bucket] = buckets[bucket][: settings.per_bucket]

    return buckets


def format_clip(record: dict[str, Any]) -> str:
    flags = record.get("flags") or {}
    scores = record.get("scores") or {}
    camera = record.get("camera") or {}
    location = record.get("location") or {}
    keyframes = record.get("keyframes") or {}

    return f"""- **{record.get('clip_id', 'unknown')}** — `{record.get('original_filename', 'unknown')}`
  - Asset: `{record.get('asset_path', 'unknown')}`
  - Location: {location.get('name', 'unknown')} / {location.get('sub_location', 'unknown')}
  - Shot: {camera.get('shot_type', 'unknown')} / {camera.get('movement', 'unknown')}
  - Emotion: {', '.join(record.get('emotion_tags', []))}
  - Story: {', '.join(record.get('story_tags', []))}
  - Best usage: {', '.join(record.get('best_usage', []))}
  - Score: {scores.get('overall', 0)} | Hero: {flags.get('hero_shot', False)} | Needs review: {flags.get('needs_review', False)}
  - Keyframes: `{keyframes.get('folder', '')}`
  - Notes: {record.get('director_notes', '')}
"""


def build_handoff(project: str, records: list[dict[str, Any]], buckets: dict[str, list[dict[str, Any]]], settings: HandoffSettings) -> str:
    eligible_count = sum(1 for record in records if is_eligible(record, settings))
    hero_count = sum(1 for record in records if (record.get("flags") or {}).get("hero_shot"))
    review_count = sum(1 for record in records if (record.get("flags") or {}).get("needs_review"))

    content = f"""# Director Handoff — {project}

Generated by `apps/footage-analyzer/director_handoff.py`.

## Summary

| Category | Count |
|---|---:|
| Total memory records | {len(records)} |
| Eligible records | {eligible_count} |
| Hero shots | {hero_count} |
| Needs review | {review_count} |

## Director Instructions

Use this handoff as the footage candidate pool.

Do not treat this as a final edit.
Use it to build the story beat table, storyboard, and timeline.

Priority order:

1. Emotion
2. Story relevance
3. Landscape power
4. Shot quality
5. Pacing
6. Technical stability

---

"""

    for bucket, bucket_records_list in buckets.items():
        content += f"## {bucket.title()} Candidates\n\n"
        if not bucket_records_list:
            content += "No candidates found.\n\n---\n\n"
            continue
        for record in bucket_records_list:
            content += format_clip(record) + "\n"
        content += "---\n\n"

    content += """## Next Step

The Documentary Director should now:

1. Read the project brief.
2. Read this handoff.
3. Create a story beat table.
4. Select the strongest candidate clips for each beat.
5. Build a storyboard.
6. Convert the storyboard into a Remotion timeline.
"""

    return content


def main() -> None:
    args = parse_args()
    settings = resolve_settings(args)

    if not settings.memory_dir.exists():
        raise FileNotFoundError(f"Memory folder does not exist: {settings.memory_dir}")

    settings.output_path.parent.mkdir(parents=True, exist_ok=True)
    records = load_records(settings.memory_dir)
    buckets = bucket_records(records, settings)
    output = build_handoff(settings.project_title, records, buckets, settings)
    settings.output_path.write_text(output, encoding="utf-8")
    print(f"Director handoff created: {settings.output_path}")


if __name__ == "__main__":
    main()
