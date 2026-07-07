#!/usr/bin/env python3
"""Build timeline-draft.md and timeline-draft.json from storyboard.md."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from apps.common.project_config import get_nested, load_project_config  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a timeline draft from storyboard.md")
    parser.add_argument("--project-folder", required=True, help="Project folder containing project.yaml")
    return parser.parse_args()


def extract_beats(storyboard_text: str) -> list[dict[str, Any]]:
    sections = re.split(r"\n##\s+", storyboard_text)
    beats: list[dict[str, Any]] = []
    for section in sections[1:]:
        lines = section.strip().splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:])
        beats.append({
            "title": title,
            "purpose": extract_field(body, "Purpose") or "TBD",
            "narration": extract_field(body, "Narration Anchor") or "TBD",
            "preferred_footage": extract_field(body, "Preferred Footage") or "TBD",
            "subtitle_treatment": extract_field(body, "Subtitle Treatment") or "Premium broadcast-style subtitle",
            "transition": extract_field(body, "Transition") or "documentary cut",
            "emotion": extract_field(body, "Primary Emotion") or "neutral-cinematic",
            "rhythm": extract_field(body, "Rhythm") or "measured",
            "silence_need": extract_field(body, "Silence Need") or "low",
            "camera_language": extract_field(body, "Camera Language") or "TBD",
            "director_reasoning": extract_field(body, "Director Reasoning") or "TBD",
        })
    return beats


def extract_field(text: str, label: str) -> str:
    pattern = rf"\*\*{re.escape(label)}:\*\*\s*(.*)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""


def weight_for_beat(beat: dict[str, Any]) -> float:
    weight = 1.0
    emotion = str(beat.get("emotion", "")).lower()
    rhythm = str(beat.get("rhythm", "")).lower()
    silence = str(beat.get("silence_need", "")).lower()

    if emotion in {"awe", "isolation", "memory"}:
        weight += 0.35
    if emotion in {"tension", "discovery"}:
        weight += 0.15
    if rhythm == "slow-hold":
        weight += 0.35
    elif rhythm == "flowing":
        weight -= 0.15
    if silence == "high":
        weight += 0.25
    elif silence == "medium":
        weight += 0.10

    return max(0.5, weight)


def allocate_durations(total_seconds: int, beats: list[dict[str, Any]]) -> list[int]:
    if not beats:
        return []

    weights = [weight_for_beat(beat) for beat in beats]
    total_weight = sum(weights)
    raw = [max(4, int(round(total_seconds * weight / total_weight))) for weight in weights]

    diff = total_seconds - sum(raw)
    index = 0
    while diff != 0 and raw:
        pos = index % len(raw)
        if diff > 0:
            raw[pos] += 1
            diff -= 1
        elif raw[pos] > 4:
            raw[pos] -= 1
            diff += 1
        index += 1
        if index > 10000:
            break
    return raw


def build_timeline(config: dict[str, Any], beats: list[dict[str, Any]]) -> dict[str, Any]:
    total = int(get_nested(config, "output.target_duration_seconds", 240) or 240)
    fps = 30
    durations = allocate_durations(total, beats)

    clips = []
    cursor = 0
    for idx, beat in enumerate(beats, start=1):
        duration = durations[idx - 1] if idx - 1 < len(durations) else 4
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
            "emotion": beat.get("emotion"),
            "rhythm": beat.get("rhythm"),
            "silence_need": beat.get("silence_need"),
            "camera_language": beat.get("camera_language"),
            "director_reasoning": beat.get("director_reasoning"),
            "timing_reasoning": f"Duration allocated from emotion={beat.get('emotion')}, rhythm={beat.get('rhythm')}, silence={beat.get('silence_need')}.",
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


def build_markdown(timeline: dict[str, Any]) -> str:
    content = f"# Timeline Draft — {timeline['project']['title']}\n\n"
    content += f"Duration: {timeline['output']['duration_seconds']}s  \n"
    content += f"Frames: {timeline['output']['duration_frames']}  \n\n"
    content += "| # | Beat | Start | Duration | Emotion | Rhythm | Silence | Footage | Transition |\n"
    content += "|---:|---|---:|---:|---|---|---|---|---|\n"
    for idx, clip in enumerate(timeline["clips"], start=1):
        content += (
            f"| {idx} | {clip['beat']} | {clip['start_seconds']}s | {clip['duration_seconds']}s | "
            f"{clip.get('emotion')} | {clip.get('rhythm')} | {clip.get('silence_need')} | "
            f"{clip['footage']} | {clip['transition']} |\n"
        )
    content += "\n## Timing Reasoning\n\n"
    for clip in timeline["clips"]:
        content += f"- **{clip['id']}**: {clip['timing_reasoning']}\n"
    content += "\n## Notes\n\nThis timeline uses Director Intelligence fields when available. Replace footage placeholders after Director review.\n"
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
