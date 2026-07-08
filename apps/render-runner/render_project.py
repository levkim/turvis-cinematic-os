#!/usr/bin/env python3
"""Run Remotion preview or render for the current synced TURVIS timeline."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REMOTION_DIR = REPO_ROOT / "remotion"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run TURVIS Remotion preview or render")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preview", action="store_true", help="Open Remotion Studio preview")
    mode.add_argument("--render", action="store_true", help="Render final MP4")
    parser.add_argument("--install", action="store_true", help="Run npm install before preview/render")
    return parser.parse_args()


def npm_executable(os_name: str | None = None) -> str:
    platform_name = os.name if os_name is None else os_name
    return "npm.cmd" if platform_name == "nt" else "npm"


def run(command: list[str]) -> None:
    print(" ".join(command))
    subprocess.run(command, cwd=REMOTION_DIR, check=True)


def main() -> None:
    args = parse_args()
    if not REMOTION_DIR.exists():
        raise FileNotFoundError(f"Remotion folder not found: {REMOTION_DIR}")

    npm = npm_executable()

    if args.install:
        run([npm, "install"])

    if args.preview:
        run([npm, "run", "start"])
    elif args.render:
        run([npm, "run", "render"])


if __name__ == "__main__":
    main()
