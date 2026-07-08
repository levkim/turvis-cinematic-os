#!/usr/bin/env python3
"""Convert timeline-draft.json into timeline.remotion.json."""

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
    parser = argparse.ArgumentParser(description="Build Remotion-ready timeline JSON")
    parser.add_argument("--project-folder", required=True, help="Project folder containing project.yaml")
    return parser.parse_args()


def seconds_to_frames(seconds: int | float, fps: int) -> int:
    return int(round(float(seconds) * fps))


def parse_resolution(resolution: str | None) -> tuple[int, int]:
    if not resolution:
        return 1920, 1080
    match = re.match(r"^\s*(\d+)\s*x\s*(\d+)\s*$", str(resolution), re.IGNORECASE)
    if not match:
        return 1920, 1080
    return int(match.group(1)), int(match.group(2))


def build_remotion_timeline(config: dict, draft: dict) -> dict:
    fps = int(draft.get("output", {}).get("fps", 30))
    resolution = get_nested(config, "output.resolution", "1920x1080")
    width, height = parse_resolution(resolution)
    clips = []

    for item in draft.get("clips", []):
        start = seconds_to_frames(item.get("start_seconds", 0), fps)
        duration = seconds_to_frames(item.get("duration_seconds", 1), fps)
        clips.append({
            "id": item.get("id"),
            "type": "video-placeholder",
            "startFrame": start,
            "durationInFrames": duration,
            "beat": item.get("beat"),
            "src": item.get("footage", "TBD"),
            "subtitle": item.get("subtitle", ""),
            "subtitleStyle": item.get("subtitle_treatment", "premium-documentary"),
            "transition": item.get("transition", "cut"),
            "status": item.get("status", "draft"),
        })

    return {
        "schema": "turvis.remotion.timeline.v0.1",
        "project": draft.get("project", {}),
        "composition": {
            "fps": fps,
            "durationInFrames": sum(c["durationInFrames"] for c in clips),
            "aspectRatio": get_nested(config, "output.aspect_ratio", "16:9"),
            "resolution": resolution,
            "language": get_nested(config, "output.language", "ko"),
            "width": width,
            "height": height,
        },
        "audio": {
            "generateNarration": bool(get_nested(config, "rules.generate_audio", False)),
            "generateMusic": bool(get_nested(config, "rules.generate_music", False)),
            "generateSoundEffects": bool(get_nested(config, "rules.generate_sound_effects", False)),
        },
        "clips": clips,
    }


def main() -> None:
    args = parse_args()
    project_folder = Path(args.project_folder).expanduser().resolve()
    config = load_project_config(project_folder=str(project_folder))
    draft_path = project_folder / "timeline-draft.json"
    if not draft_path.exists():
        raise FileNotFoundError(f"Missing timeline draft: {draft_path}")

    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    remotion_timeline = build_remotion_timeline(config, draft)
    output_path = project_folder / "timeline.remotion.json"
    output_path.write_text(json.dumps(remotion_timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Created: {output_path}")


if __name__ == "__main__":
    main()
