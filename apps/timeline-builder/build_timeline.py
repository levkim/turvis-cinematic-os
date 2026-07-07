#!/usr/bin/env python3
"""Build timeline-draft.md and timeline-draft.json from storyboard.md."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from apps.common.project_config import get_nested, load_project_config  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a timeline draft from storyboard.md")
    parser.add_argument("--project-folder", required=True, help="Project folder containing project.yaml")
    return parser.parse_args()


def extract_beats(storyboard_text: str) -> list[dict]:
    sections = re.split(r"\n##\s+", storyboard_text)
    beats = []
    for section in sections[1:]:
        lines = section.strip().splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:])
        purpose = extract_field(body, "Purpose")
        narration = extract_field(body, "Narration Anchor")
        preferred = extract_field(body, "Preferred Footage")
        subtitle = extract_field(body, "Subtitle Treatment")
        transition = extract_field(body, "Transition")
        beats.append({
            "title": title,
            "purpose": purpose or "TBD",
            "narration": narration or "TBD",
            "preferred_footage": preferred or "TBD",
            "subtitle_treatment": subtitle or "Premium broadcast-style subtitle",
            "transition": transition or "documentary cut",
        })
    return beats


def extract_field(text: str, label: str) -> str:
    pattern = rf"\*\*{re.escape(label)}:\*\*\s*(.*)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""


def build_timeline(config: dict, beats: list[dict]) -> dict:
    total = int(get_nested(config, "output.target_duration_seconds", 240) or 240)
    fps = 30
    count = max(1, len(beats))
    base_duration = max(4, total // count)

    clips = []
    cursor = 0
    for idx, beat in enumerate(beats, start=1):
        duration = base_duration if idx < count else max(4, total - cursor)
        clips.append({
            "id": f"beat-{idx:02d}",
            "beat": beat["title"],
            "start_seconds": cursor,
            "duration_seconds": duration,
            "end_seconds": cursor + duration,
            "narration": beat["narration"],
            "footage": beat["preferred_footage"],
            "subtitle": beat["narration"],
            "subtitle_treatment": beat["subtitle_treatment"],
            "transition": beat["transition"],
            "status": "draft",
        })
        cursor += duration

    return {
        "project": {
            "id": get_nested(config, "project.id", "unknown"),
            "title": get_nested(config, "project.title", "Untitled Project"),
        },
        "output": {
            "fps": fps,
            "duration_seconds": cursor,
            "duration_frames": cursor * fps,
            "aspect_ratio": get_nested(config, "output.aspect_ratio", "16:9"),
            "resolution": get_nested(config, "output.resolution", "3840x2160"),
        },
        "clips": clips,
    }


def build_markdown(timeline: dict) -> str:
    content = f"# Timeline Draft — {timeline['project']['title']}\n\n"
    content += f"Duration: {timeline['output']['duration_seconds']}s  \n"
    content += f"Frames: {timeline['output']['duration_frames']}  \n\n"
    content += "| # | Beat | Start | Duration | Footage | Subtitle | Transition |\n"
    content += "|---:|---|---:|---:|---|---|---|\n"
    for idx, clip in enumerate(timeline["clips"], start=1):
        content += f"| {idx} | {clip['beat']} | {clip['start_seconds']}s | {clip['duration_seconds']}s | {clip['footage']} | {clip['subtitle']} | {clip['transition']} |\n"
    content += "\n## Notes\n\nThis is a draft timeline. Replace footage placeholders after Director review.\n"
    return content


def main() -> None:
    args = parse_args()
    project_folder = Path(args.project_folder).expanduser().resolve()
    config = load_project_config(project_folder=str(project_folder))
    storyboard_path = project_folder / "storyboard.md"
    if not storyboard_path.exists():
        raise FileNotFoundError(f"Missing storyboard: {storyboard_path}")

    beats = extract_beats(storyboard_path.read_text(encoding="utf-8"))
    timeline = build_timeline(config, beats)

    (project_folder / "timeline-draft.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    (project_folder / "timeline-draft.md").write_text(build_markdown(timeline), encoding="utf-8")

    print(f"Created: {project_folder / 'timeline-draft.json'}")
    print(f"Created: {project_folder / 'timeline-draft.md'}")


if __name__ == "__main__":
    main()
