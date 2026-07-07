#!/usr/bin/env python3
"""
TURVIS Footage Search CLI v0.1

Searches Adventure Memory JSON files using local keyword/tag/score matching.

Local-first. No AI API calls.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search TURVIS Adventure Memory footage records")
    parser.add_argument("--memory", required=True, help="Folder containing footage memory JSON files")
    parser.add_argument("--query", default="", help="Free text query")
    parser.add_argument("--emotion", action="append", default=[], help="Emotion tag filter. Can be repeated")
    parser.add_argument("--story", action="append", default=[], help="Story tag filter. Can be repeated")
    parser.add_argument("--shot", action="append", default=[], help="Shot type filter. Can be repeated")
    parser.add_argument("--location", default="", help="Location text filter")
    parser.add_argument("--hero-only", action="store_true", help="Only return hero shots")
    parser.add_argument("--exclude-avoid", action="store_true", help="Exclude clips marked avoid")
    parser.add_argument("--min-score", type=int, default=0, help="Minimum overall score")
    parser.add_argument("--limit", type=int, default=10, help="Maximum results")
    parser.add_argument("--output", default=None, help="Optional markdown output path")
    return parser.parse_args()


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


def normalize(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return " ".join(normalize(v) for v in value)
    if isinstance(value, dict):
        return " ".join(normalize(v) for v in value.values())
    return str(value).lower()


def text_blob(record: dict[str, Any]) -> str:
    fields = [
        record.get("clip_id"),
        record.get("original_filename"),
        record.get("asset_path"),
        record.get("project"),
        record.get("location"),
        record.get("camera"),
        record.get("visual_context"),
        record.get("emotion_tags"),
        record.get("story_tags"),
        record.get("best_usage"),
        record.get("director_notes"),
    ]
    return normalize(fields)


def record_matches(record: dict[str, Any], args: argparse.Namespace) -> bool:
    flags = record.get("flags") or {}
    scores = record.get("scores") or {}
    camera = record.get("camera") or {}

    if args.exclude_avoid and flags.get("avoid", False):
        return False

    if args.hero_only and not flags.get("hero_shot", False):
        return False

    if int(scores.get("overall") or 0) < args.min_score:
        return False

    emotion_tags = {str(t).lower() for t in record.get("emotion_tags", [])}
    story_tags = {str(t).lower() for t in record.get("story_tags", [])}
    shot_type = str(camera.get("shot_type", "")).lower()
    location_text = normalize(record.get("location"))
    blob = text_blob(record)

    for emotion in args.emotion:
        if emotion.lower() not in emotion_tags:
            return False

    for story in args.story:
        if story.lower() not in story_tags:
            return False

    for shot in args.shot:
        if shot.lower() not in shot_type:
            return False

    if args.location and args.location.lower() not in location_text:
        return False

    if args.query:
        terms = [t.strip().lower() for t in args.query.split() if t.strip()]
        if not all(term in blob for term in terms):
            return False

    return True


def rank_score(record: dict[str, Any], args: argparse.Namespace) -> int:
    scores = record.get("scores") or {}
    flags = record.get("flags") or {}
    base = int(scores.get("overall") or 0)
    if flags.get("hero_shot"):
        base += 15
    if flags.get("needs_review"):
        base -= 5
    if flags.get("avoid"):
        base -= 50
    return base


def format_result(record: dict[str, Any], index: int, args: argparse.Namespace) -> str:
    scores = record.get("scores") or {}
    flags = record.get("flags") or {}
    camera = record.get("camera") or {}
    location = record.get("location") or {}
    keyframes = record.get("keyframes") or {}

    return f"""## {index}. {record.get('clip_id', 'unknown')}

**Filename:** `{record.get('original_filename', 'unknown')}`  
**Asset Path:** `{record.get('asset_path', 'unknown')}`  
**Location:** {location.get('name', 'unknown')} / {location.get('sub_location', 'unknown')}  
**Shot Type:** {camera.get('shot_type', 'unknown')}  
**Movement:** {camera.get('movement', 'unknown')}  
**Emotion Tags:** {', '.join(record.get('emotion_tags', []))}  
**Story Tags:** {', '.join(record.get('story_tags', []))}  
**Best Usage:** {', '.join(record.get('best_usage', []))}  
**Overall Score:** {scores.get('overall', 0)}  
**Hero Shot:** {flags.get('hero_shot', False)}  
**Needs Review:** {flags.get('needs_review', True)}  
**JSON:** `{record.get('_json_path', '')}`  
**Keyframes:** `{keyframes.get('folder', '')}`

**Director Notes:**  
{record.get('director_notes', '')}

---
"""


def build_output(results: list[dict[str, Any]], args: argparse.Namespace) -> str:
    header = f"""# TURVIS Footage Search Results

## Query

```text
query: {args.query}
emotion: {args.emotion}
story: {args.story}
shot: {args.shot}
location: {args.location}
hero_only: {args.hero_only}
min_score: {args.min_score}
```

## Results

"""
    if not results:
        return header + "No matching clips found.\n"

    body = ""
    for index, record in enumerate(results, start=1):
        body += format_result(record, index, args)
    return header + body


def main() -> None:
    args = parse_args()
    memory_dir = Path(args.memory).expanduser().resolve()
    if not memory_dir.exists():
        raise FileNotFoundError(f"Memory folder does not exist: {memory_dir}")

    records = load_records(memory_dir)
    matches = [record for record in records if record_matches(record, args)]
    matches.sort(key=lambda r: rank_score(r, args), reverse=True)
    results = matches[: args.limit]

    output = build_output(results, args)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.write_text(output, encoding="utf-8")
        print(f"Search results written to: {output_path}")
    else:
        print(output)


if __name__ == "__main__":
    main()
