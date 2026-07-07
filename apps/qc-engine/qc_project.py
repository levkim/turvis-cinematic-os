#!/usr/bin/env python3
"""Validate TURVIS project outputs before Remotion preview/render."""

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

FULL_REQUIRED_PROJECT_FILES = [
    "project.yaml",
    "narration.md",
    "director-prep.md",
    "story-beats.md",
    "storyboard.md",
    "timeline-draft.json",
    "timeline.remotion.json",
]

FAST_DRAFT_REQUIRED_PROJECT_FILES = [
    "project.yaml",
    "narration.md",
    "director-decisions.md",
    "director-decisions.json",
    "story-beats.md",
    "storyboard.md",
    "timeline-draft.json",
    "timeline.remotion.json",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run TURVIS project QC")
    parser.add_argument("--project-folder", required=True, help="Project folder containing project.yaml")
    parser.add_argument("--strict", action="store_true", help="Exit with error if warnings exist")
    parser.add_argument("--fast-draft", action="store_true", help="Use narration-first fast draft required files")
    return parser.parse_args()


def add_result(results: list[dict[str, str]], level: str, item: str, message: str) -> None:
    results.append({"level": level, "item": item, "message": message})


def validate_required_files(project_folder: Path, results: list[dict[str, str]], fast_draft: bool) -> None:
    required_files = FAST_DRAFT_REQUIRED_PROJECT_FILES if fast_draft else FULL_REQUIRED_PROJECT_FILES
    for filename in required_files:
        path = project_folder / filename
        if path.exists():
            add_result(results, "PASS", filename, "File exists")
        else:
            add_result(results, "FAIL", filename, "Missing required project output")


def load_json(path: Path, results: list[dict[str, str]]) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        add_result(results, "FAIL", path.name, "JSON file missing")
    except json.JSONDecodeError as exc:
        add_result(results, "FAIL", path.name, f"Invalid JSON: {exc}")
    return None


def validate_remotion_timeline(project_folder: Path, config: dict[str, Any], results: list[dict[str, str]], fast_draft: bool) -> None:
    path = project_folder / "timeline.remotion.json"
    data = load_json(path, results)
    if data is None:
        return

    if data.get("schema") == "turvis.remotion.timeline.v0.1":
        add_result(results, "PASS", "schema", "Remotion timeline schema is valid")
    else:
        add_result(results, "FAIL", "schema", "Unexpected or missing Remotion timeline schema")

    composition = data.get("composition") or {}
    clips = data.get("clips") or []

    required_composition = ["fps", "durationInFrames", "aspectRatio", "resolution", "language"]
    for field in required_composition:
        if field in composition:
            add_result(results, "PASS", f"composition.{field}", "Present")
        else:
            add_result(results, "FAIL", f"composition.{field}", "Missing")

    if not clips:
        add_result(results, "WARN", "clips", "No clips in Remotion timeline")
        return

    last_end = 0
    for idx, clip in enumerate(clips, start=1):
        clip_id = clip.get("id", f"clip-{idx}")
        start = int(clip.get("startFrame", 0) or 0)
        duration = int(clip.get("durationInFrames", 0) or 0)
        end = start + duration

        if duration <= 0:
            add_result(results, "FAIL", clip_id, "durationInFrames must be positive")
        if start < last_end:
            add_result(results, "WARN", clip_id, "Clip overlaps previous clip")
        if not clip.get("subtitle"):
            add_result(results, "WARN", clip_id, "Subtitle is empty")
        if clip.get("src") in {None, "", "TBD"}:
            level = "PASS" if fast_draft else "WARN"
            message = "Placeholder footage accepted in fast draft" if fast_draft else "Footage source is placeholder"
            add_result(results, level, clip_id, message)
        last_end = max(last_end, end)

    declared_duration = int(composition.get("durationInFrames", 0) or 0)
    actual_duration = sum(int(c.get("durationInFrames", 0) or 0) for c in clips)
    if declared_duration == actual_duration:
        add_result(results, "PASS", "duration", "Composition duration matches clip sum")
    else:
        add_result(results, "WARN", "duration", f"Declared {declared_duration}, clip sum {actual_duration}")

    if get_nested(config, "rules.generate_audio", False):
        add_result(results, "WARN", "audio", "generate_audio is true; current workflow expects separate audio editing")
    else:
        add_result(results, "PASS", "audio", "Audio generation disabled as expected")


def build_report(project_folder: Path, results: list[dict[str, str]], fast_draft: bool) -> str:
    passes = sum(1 for r in results if r["level"] == "PASS")
    warnings = sum(1 for r in results if r["level"] == "WARN")
    fails = sum(1 for r in results if r["level"] == "FAIL")

    mode = "Fast Draft" if fast_draft else "Full Pipeline"
    content = "# TURVIS QC Report\n\n"
    content += f"Mode: **{mode}**  \n"
    content += f"Project Folder: `{project_folder}`\n\n"
    content += "## Summary\n\n"
    content += f"- PASS: {passes}\n"
    content += f"- WARN: {warnings}\n"
    content += f"- FAIL: {fails}\n\n"
    content += "## Results\n\n"
    content += "| Level | Item | Message |\n"
    content += "|---|---|---|\n"
    for result in results:
        content += f"| {result['level']} | {result['item']} | {result['message']} |\n"
    content += "\n## Decision\n\n"
    if fails:
        content += "QC status: **FAILED**. Fix failed items before render.\n"
    elif warnings:
        content += "QC status: **PASSED WITH WARNINGS**. Review warnings before final render.\n"
    else:
        content += "QC status: **PASSED**. Ready for Remotion preview/render.\n"
    return content


def main() -> None:
    args = parse_args()
    project_folder = Path(args.project_folder).expanduser().resolve()
    config = load_project_config(project_folder=str(project_folder))
    results: list[dict[str, str]] = []

    validate_required_files(project_folder, results, args.fast_draft)
    validate_remotion_timeline(project_folder, config, results, args.fast_draft)

    report = build_report(project_folder, results, args.fast_draft)
    output_path = project_folder / "qc-report.md"
    output_path.write_text(report, encoding="utf-8")
    print(f"QC report created: {output_path}")

    has_fail = any(r["level"] == "FAIL" for r in results)
    has_warn = any(r["level"] == "WARN" for r in results)
    if has_fail or (args.strict and has_warn):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
