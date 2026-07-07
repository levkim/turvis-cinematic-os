#!/usr/bin/env python3
"""
TURVIS Analyze Project CLI v0.1

Project-folder based wrapper for Footage Analyzer.

This keeps the engine universal:
- App reads project.yaml
- Project data stays in project folder
- No project-specific command required
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
    parser = argparse.ArgumentParser(description="Analyze footage using project.yaml")
    parser.add_argument("--project-folder", required=True, help="Project folder containing project.yaml")
    parser.add_argument("--prefix", default=None, help="Optional clip ID prefix override")
    parser.add_argument("--skip-keyframes", action="store_true", help="Skip keyframe extraction")
    return parser.parse_args()


def require_value(value: str | None, label: str) -> str:
    if not value:
        raise ValueError(f"Missing required project.yaml value: {label}")
    return value


def main() -> None:
    args = parse_args()
    config = load_project_config(project_folder=args.project_folder)

    project_id = require_value(get_nested(config, "project.id"), "project.id")
    title = get_nested(config, "project.title", project_id)
    country = get_nested(config, "locations.country", "unknown")
    region = get_nested(config, "locations.region", "unknown")
    destination = get_nested(config, "locations.destination", "unknown")

    footage = require_value(get_nested(config, "paths.footage"), "paths.footage")
    keyframes = get_nested(config, "paths.keyframes")
    memory = require_value(get_nested(config, "paths.memory"), "paths.memory")

    prefix = args.prefix or project_id.upper().replace("-", "_")

    command = [
        sys.executable,
        str(CURRENT_FILE.parent / "footage_analyzer.py"),
        "--input",
        footage,
        "--project",
        project_id,
        "--episode",
        title,
        "--prefix",
        prefix,
        "--country",
        country,
        "--region",
        region,
        "--destination",
        destination,
        "--output",
        memory,
    ]

    if keyframes:
        command.extend(["--keyframes", keyframes])
    if args.skip_keyframes:
        command.append("--skip-keyframes")

    print("Running Footage Analyzer from project.yaml")
    print(" ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
