#!/usr/bin/env python3
"""Create story beat and storyboard draft files from a TURVIS project folder."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from apps.common.project_config import get_nested, load_project_config  # noqa: E402

BEATS = [
    ("opening", "Establish the world and emotional promise."),
    ("threshold", "Show departure from the ordinary world."),
    ("journey", "Carry movement through space."),
    ("discovery", "Reveal the first major visual subject."),
    ("texture", "Let the landscape explain itself."),
    ("scale", "Show human smallness against place."),
    ("arrival", "Reach the emotional center of the project."),
    ("reflection", "Create silence, pause, and meaning."),
    ("ending", "Leave the viewer with a final emotional image."),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create story beat and storyboard drafts")
    parser.add_argument("--project-folder", required=True, help="Project folder containing project.yaml")
    return parser.parse_args()


def read_narration(config: dict) -> list[str]:
    path_value = get_nested(config, "paths.narration")
    if not path_value:
        return []
    path = Path(str(path_value)).expanduser()
    if not path.exists():
        return []
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        clean = line.strip()
        if clean and not clean.startswith("#") and not clean.startswith("```"):
            lines.append(clean)
    return lines[:24]


def build_story_beats(config: dict, narration_lines: list[str]) -> str:
    title = get_nested(config, "project.title", "Untitled Project")
    content = f"# Story Beat Draft — {title}\n\n"
    content += "| # | Beat | Purpose | Narration Anchor | Footage Need | Emotion |\n"
    content += "|---:|---|---|---|---|---|\n"
    for idx, (beat, purpose) in enumerate(BEATS, start=1):
        anchor = narration_lines[idx - 1] if idx - 1 < len(narration_lines) else "TBD"
        content += f"| {idx} | {beat} | {purpose} | {anchor} | Candidate from handoff | TBD |\n"
    content += "\n## Notes\n\nThis is a structural draft. Refine before timeline generation.\n"
    return content


def build_storyboard(config: dict, narration_lines: list[str]) -> str:
    title = get_nested(config, "project.title", "Untitled Project")
    content = f"# Storyboard Draft — {title}\n\n"
    for idx, (beat, purpose) in enumerate(BEATS, start=1):
        anchor = narration_lines[idx - 1] if idx - 1 < len(narration_lines) else "TBD"
        content += f"## {idx}. {beat.title()}\n\n"
        content += f"**Purpose:** {purpose}  \n"
        content += f"**Narration Anchor:** {anchor}  \n"
        content += "**Preferred Footage:** TBD from director-handoff.md  \n"
        content += "**Subtitle Treatment:** Premium broadcast-style lower subtitle  \n"
        content += "**Transition:** restrained documentary transition  \n\n---\n\n"
    return content


def main() -> None:
    args = parse_args()
    project_folder = Path(args.project_folder).expanduser().resolve()
    config = load_project_config(project_folder=str(project_folder))
    narration_lines = read_narration(config)

    (project_folder / "story-beats.md").write_text(build_story_beats(config, narration_lines), encoding="utf-8")
    (project_folder / "storyboard.md").write_text(build_storyboard(config, narration_lines), encoding="utf-8")

    print(f"Created: {project_folder / 'story-beats.md'}")
    print(f"Created: {project_folder / 'storyboard.md'}")


if __name__ == "__main__":
    main()
