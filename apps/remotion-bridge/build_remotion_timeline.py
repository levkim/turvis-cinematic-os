#!/usr/bin/env python3
"""Convert timeline-draft.json into timeline.remotion.json."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote

REPO_ROOT = Path(__file__).resolve().parents[2]
FOOTAGE_SERVER_URL = "http://127.0.0.1:37678"
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


def resolve_repo_path(value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(str(value)).expanduser()
    return path if path.is_absolute() else REPO_ROOT / path


def parse_shot_list_clip_ids(shot_list_path: Path) -> list[str]:
    if not shot_list_path.exists():
        return []

    clip_ids: list[str] = []
    for line in shot_list_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or stripped.startswith("|---") or "Candidate Clip" in stripped:
            continue
        parts = [part.strip() for part in stripped.split("|")]
        if len(parts) >= 5 and parts[1].isdigit():
            clip_id = parts[3]
            if clip_id and clip_id != "TBD":
                clip_ids.append(clip_id)
    return clip_ids


def load_footage_index(config: dict[str, Any]) -> dict[str, Any]:
    memory_dir = resolve_repo_path(get_nested(config, "paths.memory"))
    if not memory_dir:
        return {}

    index_path = memory_dir / "footage-index.json"
    if not index_path.exists():
        return {}
    return json.loads(index_path.read_text(encoding="utf-8"))


def load_footage_candidates(config: dict[str, Any], footage_index: dict[str, Any]) -> list[dict[str, Any]]:
    memory_dir = resolve_repo_path(get_nested(config, "paths.memory"))
    clips = footage_index.get("clips") or []
    if not memory_dir:
        return clips

    by_id = {clip.get("clip_id"): clip for clip in clips}
    ordered_ids = parse_shot_list_clip_ids(memory_dir / "shot-list.md")
    ordered = [by_id[clip_id] for clip_id in ordered_ids if clip_id in by_id]
    return ordered or clips


def static_mount_name(config: dict[str, Any]) -> str:
    return str(get_nested(config, "project.id", "current-project"))


def clip_to_video_source(candidate: dict[str, Any], config: dict[str, Any]) -> str | None:
    asset_path = candidate.get("asset_path") or candidate.get("filename")
    if not asset_path:
        return None

    normalized = str(asset_path).replace("\\", "/").lstrip("/")
    encoded = quote(normalized, safe="/-_.()")
    return f"{FOOTAGE_SERVER_URL}/{encoded}"


def build_remotion_timeline(config: dict[str, Any], draft: dict) -> dict:
    fps = int(draft.get("output", {}).get("fps", 30))
    resolution = get_nested(config, "output.resolution", "1920x1080")
    width, height = parse_resolution(resolution)
    footage_index = load_footage_index(config)
    candidates = load_footage_candidates(config, footage_index)

    clips = []
    for index, item in enumerate(draft.get("clips", [])):
        start = seconds_to_frames(item.get("start_seconds", 0), fps)
        duration = seconds_to_frames(item.get("duration_seconds", 1), fps)
        candidate = candidates[index % len(candidates)] if candidates else None
        video_src = clip_to_video_source(candidate, config) if candidate else None
        clips.append({
            "id": item.get("id"),
            "type": "video" if video_src else "video-placeholder",
            "startFrame": start,
            "durationInFrames": duration,
            "beat": item.get("beat"),
            "src": video_src or item.get("footage", "TBD"),
            "sourceClipId": candidate.get("clip_id") if candidate else None,
            "sourceFilename": candidate.get("filename") if candidate else None,
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