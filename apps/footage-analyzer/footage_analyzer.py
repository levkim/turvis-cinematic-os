#!/usr/bin/env python3
"""
TURVIS Footage Analyzer CLI v0.2

Local-first footage scanner for Adventure Memory Engine.

This tool does not call any AI API.
It creates initial Markdown and JSON memory records and extracts keyframes for later AI/human review.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Optional

VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm"}
KEYFRAME_RATIOS = [0.05, 0.25, 0.50, 0.75, 0.95]


@dataclass
class VideoMetadata:
    duration_seconds: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    codec: Optional[str] = None


@dataclass
class KeyframeSet:
    folder: str
    frames: list[str]


@dataclass
class ClipMemory:
    clip_id: str
    original_filename: str
    asset_path: str
    project: dict[str, Any]
    location: dict[str, Any]
    camera: dict[str, Any]
    visual_context: dict[str, Any]
    emotion_tags: list[str]
    story_tags: list[str]
    best_usage: list[str]
    scores: dict[str, int]
    flags: dict[str, bool]
    technical_metadata: dict[str, Any]
    keyframes: dict[str, Any]
    director_notes: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TURVIS Footage Analyzer CLI")
    parser.add_argument("--input", required=True, help="Input folder containing video files")
    parser.add_argument("--project", required=True, help="Project slug, e.g. mangystau")
    parser.add_argument("--episode", required=True, help="Episode slug, e.g. day3")
    parser.add_argument("--prefix", required=True, help="Clip ID prefix, e.g. MG-D3")
    parser.add_argument("--output", required=True, help="Output folder for memory files")
    parser.add_argument("--country", default="unknown", help="Country name")
    parser.add_argument("--region", default="unknown", help="Region name")
    parser.add_argument("--destination", default="unknown", help="Destination or route name")
    parser.add_argument("--keyframes", default=None, help="Output folder for extracted keyframes")
    parser.add_argument("--skip-keyframes", action="store_true", help="Skip keyframe extraction")
    return parser.parse_args()


def find_video_files(input_dir: Path) -> list[Path]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Input folder does not exist: {input_dir}")

    files = [p for p in input_dir.rglob("*") if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS]
    return sorted(files)


def run_ffprobe(video_path: Path) -> VideoMetadata:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,codec_name,r_frame_rate:format=duration",
        "-of",
        "json",
        str(video_path),
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        return VideoMetadata()

    stream = (data.get("streams") or [{}])[0]
    fmt = data.get("format") or {}

    fps = None
    rate = stream.get("r_frame_rate")
    if rate and "/" in rate:
        numerator, denominator = rate.split("/", 1)
        try:
            fps = float(numerator) / float(denominator)
        except (ValueError, ZeroDivisionError):
            fps = None

    duration = None
    try:
        duration = float(fmt.get("duration")) if fmt.get("duration") else None
    except ValueError:
        duration = None

    return VideoMetadata(
        duration_seconds=duration,
        width=stream.get("width"),
        height=stream.get("height"),
        fps=fps,
        codec=stream.get("codec_name"),
    )


def extract_keyframes(video_path: Path, clip_id: str, metadata: VideoMetadata, keyframes_root: Path) -> KeyframeSet:
    clip_keyframe_dir = keyframes_root / clip_id
    clip_keyframe_dir.mkdir(parents=True, exist_ok=True)

    frames: list[str] = []
    duration = metadata.duration_seconds

    if not duration or duration <= 0:
        return KeyframeSet(folder=str(clip_keyframe_dir), frames=[])

    for ratio in KEYFRAME_RATIOS:
        timestamp = max(0.0, duration * ratio)
        label = int(ratio * 100)
        frame_path = clip_keyframe_dir / f"{clip_id}_{label:02d}.jpg"

        command = [
            "ffmpeg",
            "-y",
            "-ss",
            f"{timestamp:.3f}",
            "-i",
            str(video_path),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(frame_path),
        ]

        try:
            subprocess.run(command, capture_output=True, text=True, check=True)
            frames.append(str(frame_path))
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    return KeyframeSet(folder=str(clip_keyframe_dir), frames=frames)


def make_clip_id(prefix: str, index: int) -> str:
    return f"{prefix}-{index:04d}"


def create_initial_memory(
    clip_id: str,
    file_path: Path,
    input_dir: Path,
    project: str,
    episode: str,
    country: str,
    region: str,
    destination: str,
    metadata: VideoMetadata,
    keyframes: KeyframeSet,
) -> ClipMemory:
    relative_asset_path = file_path.relative_to(input_dir).as_posix()

    return ClipMemory(
        clip_id=clip_id,
        original_filename=file_path.name,
        asset_path=relative_asset_path,
        project={
            "series": project,
            "episode": episode,
            "destination": destination,
            "country": country,
            "region": region,
        },
        location={
            "name": "unknown",
            "sub_location": "unknown",
        },
        camera={
            "type": "unknown",
            "shot_type": "unknown",
            "movement": "unknown",
            "altitude": "unknown",
            "lens_feel": "unknown",
            "stability": "unknown",
        },
        visual_context={
            "time_of_day": "unknown",
            "weather": "unknown",
            "light_quality": "unknown",
            "landscape_type": "unknown",
            "human_presence": False,
            "vehicle_presence": False,
        },
        emotion_tags=["needs-analysis"],
        story_tags=["needs-analysis"],
        best_usage=["needs-analysis"],
        scores={
            "composition": 0,
            "light": 0,
            "movement": 0,
            "stability": 0,
            "emotion": 0,
            "story_relevance": 0,
            "overall": 0,
        },
        flags={
            "hero_shot": False,
            "avoid": False,
            "needs_review": True,
        },
        technical_metadata=asdict(metadata),
        keyframes=asdict(keyframes),
        director_notes="Initial local scan only. Requires AI or human visual review using extracted keyframes.",
    )


def write_json(memory: ClipMemory, output_path: Path) -> None:
    output_path.write_text(json.dumps(asdict(memory), ensure_ascii=False, indent=2), encoding="utf-8")


def write_markdown(memory: ClipMemory, output_path: Path) -> None:
    tech = memory.technical_metadata
    keyframes = memory.keyframes
    keyframe_lines = "\n".join([f"- `{frame}`" for frame in keyframes.get("frames", [])]) or "- No keyframes extracted"

    content = f"""# {memory.clip_id}

## Clip Identity

**Clip ID:** {memory.clip_id}  
**Original Filename:** {memory.original_filename}  
**Asset Path:** `{memory.asset_path}`  
**Analyst:** Footage Analyzer CLI v0.2

---

## Project Context

**Series:** {memory.project.get('series')}  
**Episode:** {memory.project.get('episode')}  
**Country:** {memory.project.get('country')}  
**Region:** {memory.project.get('region')}  
**Destination:** {memory.project.get('destination')}  
**Location:** unknown  
**Sub-location:** unknown  

---

## Technical Metadata

| Field | Value |
|---|---|
| Duration | {tech.get('duration_seconds')} seconds |
| Resolution | {tech.get('width')}x{tech.get('height')} |
| FPS | {tech.get('fps')} |
| Codec | {tech.get('codec')} |

---

## Keyframes

**Folder:** `{keyframes.get('folder')}`

{keyframe_lines}

---

## Visual Description

```text
Needs visual analysis using keyframes.
```

---

## Camera Analysis

**Camera Type:** unknown  
**Shot Type:** unknown  
**Movement:** unknown  
**Altitude:** unknown  
**Lens Feel:** unknown  
**Stability:** unknown  

---

## Emotion Tags

- needs-analysis

---

## Story Tags

- needs-analysis

---

## Best Usage

- needs-analysis

---

## Scores

| Category | Score |
|---|---:|
| Composition | 0 |
| Light | 0 |
| Movement | 0 |
| Stability | 0 |
| Emotion | 0 |
| Story Relevance | 0 |
| Overall | 0 |

---

## Flags

**Hero Shot:** no  
**Avoid:** no  
**Needs Review:** yes  

---

## Director Notes

Initial local scan only. Requires AI or human visual review using extracted keyframes.
"""
    output_path.write_text(content, encoding="utf-8")


def write_batch_summary(memories: list[ClipMemory], output_dir: Path) -> None:
    total = len(memories)
    needs_review = sum(1 for m in memories if m.flags.get("needs_review"))
    keyframe_count = sum(len(m.keyframes.get("frames", [])) for m in memories)

    content = f"""# Footage Batch Summary

## Summary

| Category | Count |
|---|---:|
| Total clips analyzed | {total} |
| Keyframes extracted | {keyframe_count} |
| Hero shots | 0 |
| Strong support shots | 0 |
| Needs review | {needs_review} |
| Avoid | 0 |

---

## Notes

This batch was generated by Footage Analyzer CLI v0.2.

The files were scanned locally, technical metadata was extracted where possible, and keyframes were generated for review.
Visual interpretation still requires AI-assisted or human review.

---

## Clips

"""
    for memory in memories:
        frames = len(memory.keyframes.get("frames", []))
        content += f"- `{memory.clip_id}` — {memory.original_filename} — keyframes: {frames}\n"

    (output_dir / "batch-summary.md").write_text(content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    keyframes_root = (
        Path(args.keyframes).expanduser().resolve()
        if args.keyframes
        else output_dir / "keyframes"
    )
    if not args.skip_keyframes:
        keyframes_root.mkdir(parents=True, exist_ok=True)

    video_files = find_video_files(input_dir)
    if not video_files:
        print(f"No video files found in {input_dir}")
        return

    memories: list[ClipMemory] = []

    for index, video_path in enumerate(video_files, start=1):
        clip_id = make_clip_id(args.prefix, index)
        metadata = run_ffprobe(video_path)
        keyframes = (
            KeyframeSet(folder="", frames=[])
            if args.skip_keyframes
            else extract_keyframes(video_path, clip_id, metadata, keyframes_root)
        )
        memory = create_initial_memory(
            clip_id=clip_id,
            file_path=video_path,
            input_dir=input_dir,
            project=args.project,
            episode=args.episode,
            country=args.country,
            region=args.region,
            destination=args.destination,
            metadata=metadata,
            keyframes=keyframes,
        )

        write_markdown(memory, output_dir / f"{clip_id}.md")
        write_json(memory, output_dir / f"{clip_id}.json")
        memories.append(memory)
        print(f"Created memory: {clip_id} — {video_path.name} — keyframes: {len(keyframes.frames)}")

    write_batch_summary(memories, output_dir)
    print(f"\nDone. Created {len(memories)} clip memories in {output_dir}")


if __name__ == "__main__":
    main()
