#!/usr/bin/env python3
"""
TURVIS Project Pipeline CLI v0.8

Runs a local-first project pipeline:
validate -> analyze -> review queue -> director handoff -> director prep -> director intelligence -> storyboard -> timeline draft -> remotion bridge -> remotion sync -> qc

Local-first. No API calls.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
REPO_ROOT = CURRENT_FILE.parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run TURVIS local project pipeline")
    parser.add_argument("--project-folder", required=True, help="Project folder containing project.yaml")
    parser.add_argument("--skip-validate", action="store_true", help="Skip project validation")
    parser.add_argument("--skip-analyze", action="store_true", help="Skip footage analysis")
    parser.add_argument("--skip-review-queue", action="store_true", help="Skip review queue generation")
    parser.add_argument("--skip-handoff", action="store_true", help="Skip Director handoff generation")
    parser.add_argument("--skip-director-prep", action="store_true", help="Skip Director prep package generation")
    parser.add_argument("--skip-director-intelligence", action="store_true", help="Skip Director Intelligence decision generation")
    parser.add_argument("--skip-storyboard", action="store_true", help="Skip story beat/storyboard draft generation")
    parser.add_argument("--skip-timeline", action="store_true", help="Skip timeline draft generation")
    parser.add_argument("--skip-remotion-bridge", action="store_true", help="Skip Remotion timeline conversion")
    parser.add_argument("--skip-remotion-sync", action="store_true", help="Skip syncing Remotion timeline into app data")
    parser.add_argument("--skip-qc", action="store_true", help="Skip project QC report generation")
    parser.add_argument("--strict-qc", action="store_true", help="Fail pipeline when QC warnings exist")
    parser.add_argument("--skip-keyframes", action="store_true", help="Skip keyframe extraction during analysis")
    parser.add_argument("--include-review", action="store_true", help="Include needs_review clips in Director handoff")
    parser.add_argument("--exclude-avoid", action="store_true", help="Exclude avoid clips in Director handoff")
    parser.add_argument("--min-score", type=int, default=0, help="Minimum score for Director handoff")
    return parser.parse_args()


def run_step(name: str, command: list[str]) -> None:
    print(f"\n=== {name} ===")
    print(" ".join(command))
    subprocess.run(command, check=True, cwd=REPO_ROOT)


def main() -> None:
    args = parse_args()
    project_folder = args.project_folder

    if not args.skip_validate:
        run_step("Validate Project", [sys.executable, "apps/common/validate_project.py", "--project-folder", project_folder])

    if not args.skip_analyze:
        command = [sys.executable, "apps/footage-analyzer/analyze_project.py", "--project-folder", project_folder]
        if args.skip_keyframes:
            command.append("--skip-keyframes")
        run_step("Analyze Footage", command)

    if not args.skip_review_queue:
        from apps.common.project_config import get_nested, load_project_config
        config = load_project_config(project_folder=project_folder)
        memory = get_nested(config, "paths.memory")
        if not memory:
            raise ValueError("Missing paths.memory in project.yaml")
        run_step("Generate Review Queue", [sys.executable, "apps/footage-analyzer/review_queue.py", "--memory", str(memory)])

    if not args.skip_handoff:
        command = [sys.executable, "apps/footage-analyzer/handoff_project.py", "--project-folder", project_folder, "--min-score", str(args.min_score)]
        if args.include_review:
            command.append("--include-review")
        if args.exclude_avoid:
            command.append("--exclude-avoid")
        run_step("Create Director Handoff", command)

    if not args.skip_director_prep:
        run_step("Prepare Director Package", [sys.executable, "apps/director-prep/prepare_director.py", "--project-folder", project_folder])

    if not args.skip_director_intelligence:
        run_step("Analyze Director Intelligence", [sys.executable, "apps/director-intelligence/analyze_narration.py", "--project-folder", project_folder])

    if not args.skip_storyboard:
        run_step("Create Storyboard Draft", [sys.executable, "apps/director-engine/create_storyboard.py", "--project-folder", project_folder])

    if not args.skip_timeline:
        run_step("Build Timeline Draft", [sys.executable, "apps/timeline-builder/build_timeline.py", "--project-folder", project_folder])

    if not args.skip_remotion_bridge:
        run_step("Build Remotion Timeline", [sys.executable, "apps/remotion-bridge/build_remotion_timeline.py", "--project-folder", project_folder])

    if not args.skip_remotion_sync:
        run_step("Sync Remotion App Data", [sys.executable, "apps/remotion-sync/sync_timeline.py", "--project-folder", project_folder])

    if not args.skip_qc:
        command = [sys.executable, "apps/qc-engine/qc_project.py", "--project-folder", project_folder]
        if args.strict_qc:
            command.append("--strict")
        run_step("Run QC", command)

    print("\nPipeline complete.")


if __name__ == "__main__":
    main()
