#!/usr/bin/env python3
"""Unified TURVIS Studio CLI."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def run(command: list[str]) -> None:
    print(" ".join(command))
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TURVIS Studio unified CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Check local system readiness")

    create = sub.add_parser("create", help="Create a new project")
    create.add_argument("--title", required=True)
    create.add_argument("--id", default=None)
    create.add_argument("--type", default="documentary")
    create.add_argument("--country", default="unknown")
    create.add_argument("--region", default="unknown")
    create.add_argument("--destination", default="unknown")
    create.add_argument("--duration", type=int, default=240)
    create.add_argument("--aspect", default="16:9")

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


def main() -> None:
    args = parse_args()

    if args.command == "doctor":
        run([sys.executable, "apps/system-doctor/doctor.py"])
        return

    if args.command == "create":
        command = [
            sys.executable,
            "apps/project-wizard/create_project.py",
            "--title",
            args.title,
            "--type",
            args.type,
            "--country",
            args.country,
            "--region",
            args.region,
            "--destination",
            args.destination,
            "--duration",
            str(args.duration),
            "--aspect",
            args.aspect,
        ]
        if args.id:
            command.extend(["--id", args.id])
        run(command)
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
