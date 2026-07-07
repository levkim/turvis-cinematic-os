#!/usr/bin/env python3
"""Create story beat and storyboard draft files from Director Decisions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from apps.common.project_config import get_nested, load_project_config  # noqa: E402

FALLBACK_BEATS = [
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


def read_narration(config: dict[str, Any]) -> list[str]:
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


def load_decisions(project_folder: Path) -> list[dict[str, Any]]:
    path = project_folder / "director-decisions.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    decisions = data.get("decisions", [])
    return decisions if isinstance(decisions, list) else []


def decision_to_beat_name(decision: dict[str, Any], index: int) -> str:
    visual = decision.get("visual_intention", "")
    emotion = decision.get("emotion", "")
    if "night" in visual:
        return "cosmic"
    if "texture" in visual:
        return "texture"
    if "reveal" in visual:
        return "discovery"
    if "human" in visual:
        return "scale"
    if emotion == "awe":
        return "arrival"
    if emotion == "isolation":
        return "threshold"
    return f"beat-{index:02d}"


def footage_need_for(decision: dict[str, Any]) -> str:
    shot = decision.get("shot_preference", "establishing-wide")
    if shot == "drone-wide":
        return "Wide drone landscape / hero establishing shot"
    if shot == "drone-reveal":
        return "Slow drone reveal or forward push"
    if shot == "detail-texture":
        return "Geological texture detail / layered land close-up"
    if shot == "human-scale":
        return "Human or camp scale shot against vast landscape"
    if shot == "night-sky":
        return "Night sky / Milky Way / cosmic landscape"
    return "Cinematic support footage from handoff"


def transition_for(decision: dict[str, Any]) -> str:
    silence = decision.get("silence_need")
    rhythm = decision.get("rhythm")
    if silence == "high":
        return "slow fade or dip-to-black"
    if rhythm == "slow-hold":
        return "long restrained cut"
    return "documentary cut"


def build_story_beats(config: dict[str, Any], narration_lines: list[str], decisions: list[dict[str, Any]]) -> str:
    title = get_nested(config, "project.title", "Untitled Project")
    content = f"# Story Beat Draft — {title}\n\n"
    content += "Generated with Director Intelligence.\n\n"
    content += "| # | Beat | Narration Anchor | Emotion | Rhythm | Footage Need | Reasoning |\n"
    content += "|---:|---|---|---|---|---|---|\n"

    if decisions:
        for idx, decision in enumerate(decisions, start=1):
            beat = decision_to_beat_name(decision, idx)
            content += (
                f"| {idx} | {beat} | {decision.get('narration', 'TBD')} | "
                f"{decision.get('emotion', 'TBD')} | {decision.get('rhythm', 'TBD')} | "
                f"{footage_need_for(decision)} | {decision.get('reasoning', 'TBD')} |\n"
            )
    else:
        for idx, (beat, purpose) in enumerate(FALLBACK_BEATS, start=1):
            anchor = narration_lines[idx - 1] if idx - 1 < len(narration_lines) else "TBD"
            content += f"| {idx} | {beat} | {anchor} | TBD | TBD | Candidate from handoff | {purpose} |\n"

    content += "\n## Notes\n\nThis draft uses Director Decisions when available. Refine before final timeline generation.\n"
    return content


def build_storyboard(config: dict[str, Any], narration_lines: list[str], decisions: list[dict[str, Any]]) -> str:
    title = get_nested(config, "project.title", "Untitled Project")
    content = f"# Storyboard Draft — {title}\n\n"
    content += "Generated with Director Intelligence.\n\n"

    if decisions:
        for idx, decision in enumerate(decisions, start=1):
            beat = decision_to_beat_name(decision, idx)
            content += f"## {idx}. {beat.title()}\n\n"
            content += f"**Narration Anchor:** {decision.get('narration', 'TBD')}  \n"
            content += f"**Primary Emotion:** {decision.get('emotion', 'TBD')}  \n"
            content += f"**Rhythm:** {decision.get('rhythm', 'TBD')}  \n"
            content += f"**Preferred Footage:** {footage_need_for(decision)}  \n"
            content += f"**Camera Language:** {decision.get('shot_preference', 'TBD')}  \n"
            content += f"**Silence Need:** {decision.get('silence_need', 'TBD')}  \n"
            content += f"**Subtitle Treatment:** {decision.get('subtitle_strategy', 'premium-documentary')}  \n"
            content += f"**Transition:** {transition_for(decision)}  \n"
            content += f"**Director Reasoning:** {decision.get('reasoning', 'TBD')}  \n"
            content += "**QC Question:** Does this beat justify its emotional and visual weight?\n\n---\n\n"
    else:
        for idx, (beat, purpose) in enumerate(FALLBACK_BEATS, start=1):
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
    decisions = load_decisions(project_folder)

    (project_folder / "story-beats.md").write_text(build_story_beats(config, narration_lines, decisions), encoding="utf-8")
    (project_folder / "storyboard.md").write_text(build_storyboard(config, narration_lines, decisions), encoding="utf-8")

    print(f"Created: {project_folder / 'story-beats.md'}")
    print(f"Created: {project_folder / 'storyboard.md'}")


if __name__ == "__main__":
    main()
