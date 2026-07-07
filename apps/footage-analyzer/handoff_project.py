#!/usr/bin/env python3
"""
TURVIS Handoff Project CLI v0.1

Project-folder based wrapper for Director Handoff.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
REPO_ROOT = CURRENT_FILE.parents[2]
sys.path.insert(0, str(REPO_ROOT))

from apps.common.project_config import get_nested, load_project_config  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create Director handoff using project.yaml")
    parser.add_argument("--project-folder", required=True, help="Project folder containing project.yaml")
    parser.add_argument("--min-score", type=int, default=0, help="Minimum overall score")
    parser.add_argument("--exclude-avoid", action="store_true", help="Exclude clips marked avoid")
    parser.add_argument("--include-review", action="store_true", help="Include clips still marked needs_review")
    return parser.parse_args()


def require_value(value: str | None, label: str) -> str:
    if not value:
        raise ValueError(f"Missing required project.yaml value: {label}")
    return value


def main() -> None:
    args = parse_args()
    config = load_project_config(project_folder=args.project_folder)

    title = get_nested(config, "project.title", get_nested(config, "project.id", "Untitled Project"))
    memory = require_value(get_nested(config, "paths.memory"), "paths.memory")
    output = get_nested(config, "paths.director_handoff")

    command = [
        sys.executable,
        str(CURRENT_FILE.parent / "director_handoff.py"),
        "--memory",
        memory,
        "--project",
        title,
        "--min-score",
        str(args.min_score),
    ]

    if output:
        command.extend(["--output", output])
    if args.exclude_avoid:
        command.append("--exclude-avoid")
    if args.include_review:
        command.append("--include-review")

    print("Running Director Handoff from project.yaml")
    print(" ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
