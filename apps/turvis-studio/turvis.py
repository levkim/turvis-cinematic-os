#!/usr/bin/env python3
"""Unified TURVIS Studio CLI."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERIC_CATEGORIES = [
    "documentary",
    "cinematic",
    "promotion",
    "education",
    "youtube",
    "shorts-reels",
    "corporate",
    "interview",
    "presentation",
    "custom",
]


def run(command: list[str]) -> None:
    print(" ".join(command))
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TURVIS Studio unified CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Check local system readiness")

    create = sub.add_parser("create", help="Create a new video project")
    create.add_argument("--title", required=True)
    create.add_argument("--id", default=None)
    create.add_argument("--category", default="cinematic", choices=GENERIC_CATEGORIES)
    create.add_argument("--type", default="video")
    create.add_argument("--genre", default="auto")
    create.add_argument("--country", default="unknown")
    create.add_argument("--region", default="unknown")
    create.add_argument("--destination", default="unknown")
    create.add_argument("--duration", type=int, default=240)
    create.add_argument("--aspect", default="16:9")

    quickstart = sub.add_parser("quickstart", help="Create project and run full footage pipeline immediately")
    quickstart.add_argument("--title", required=True)
    quickstart.add_argument("--id", required=True)
    quickstart.add_argument("--category", default="cinematic", choices=GENERIC_CATEGORIES)
    quickstart.add_argument("--duration", type=int, default=240)
    quickstart.add_argument("--aspect", default="16:9")
    quickstart.add_argument("--skip-keyframes", action="store_true")

    fast_draft = sub.add_parser("fast-draft", help="Create narration-first storyboard/timeline/Remotion draft without footage analysis")
    fast_draft.add_argument("--project-folder", required=True)
    fast_draft.add_argument("--strict-qc", action="store_true")

    pipeline = sub.add_parser("pipeline", help="Run project pipeline")
    pipeline.add_argument("--project-folder", required=True)
    pipeline.add_argument("--include-review", action="store_true")
    pipeline.add_argument("--exclude-avoid", action="store_true")
    pipeline.add_argument("--min-score", type=int, default=0)
    pipeline.add_argument("--skip-keyframes", action="store_true")
    pipeline.add_argument("--strict-qc", action="store_true")

    preview = sub.add_parser("preview", help="Open Remotion preview")
    preview.add_argument("--install", action="store_true")

    render = sub.add_parser("render", help="Render Remotion output")
    render.add_argument("--install", action="store_true")

    return parser.parse_args()


def create_project_command(args: argparse.Namespace) -> list[str]:
    command = [
        sys.executable,
        "apps/project-wizard/create_project.py",
        "--title",
        args.title,
        "--category",
        args.category,
        "--duration",
        str(args.duration),
        "--aspect",
        args.aspect,
    ]
    if getattr(args, "id", None):
        command.extend(["--id", args.id])
    if getattr(args, "type", None):
        command.extend(["--type", args.type])
    if getattr(args, "genre", None):
        command.extend(["--genre", args.genre])
    if getattr(args, "country", None):
        command.extend(["--country", args.country])
    if getattr(args, "region", None):
        command.extend(["--region", args.region])
    if getattr(args, "destination", None):
        command.extend(["--destination", args.destination])
    return command


def fast_draft_command(project_folder: str, strict_qc: bool = False) -> list[str]:
    command = [
        sys.executable,
        "apps/project-pipeline/run_pipeline.py",
        "--project-folder",
        project_folder,
        "--skip-analyze",
        "--skip-review-queue",
        "--skip-handoff",
        "--skip-director-prep",
    ]
    if strict_qc:
        command.append("--strict-qc")
    return command


def main() -> None:
    args = parse_args()

    if args.command == "doctor":
        run([sys.executable, "apps/system-doctor/doctor.py"])
        return

    if args.command == "create":
        run(create_project_command(args))
        return

    if args.command == "quickstart":
        run(create_project_command(args))
        project_folder = f"projects/{args.id}"
        command = [sys.executable, "apps/project-pipeline/run_pipeline.py", "--project-folder", project_folder, "--include-review"]
        if args.skip_keyframes:
            command.append("--skip-keyframes")
        run(command)
        return

    if args.command == "fast-draft":
        run(fast_draft_command(args.project_folder, args.strict_qc))
        return

    if args.command == "pipeline":
        command = [sys.executable, "apps/project-pipeline/run_pipeline.py", "--project-folder", args.project_folder]
        if args.include_review:
            command.append("--include-review")
        if args.exclude_avoid:
            command.append("--exclude-avoid")
        if args.skip_keyframes:
            command.append("--skip-keyframes")
        if args.strict_qc:
            command.append("--strict-qc")
        if args.min_score:
            command.extend(["--min-score", str(args.min_score)])
        run(command)
        return

    if args.command == "preview":
        command = [sys.executable, "apps/render-runner/render_project.py", "--preview"]
        if args.install:
            command.append("--install")
        run(command)
        return

    if args.command == "render":
        command = [sys.executable, "apps/render-runner/render_project.py", "--render"]
        if args.install:
            command.append("--install")
        run(command)
        return


if __name__ == "__main__":
    main()
