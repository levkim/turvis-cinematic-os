#!/usr/bin/env python3
"""Check local TURVIS Studio development environment."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

CHECK_PATHS = [
    "apps/turvis-studio/turvis.py",
    "apps/project-pipeline/run_pipeline.py",
    "apps/footage-analyzer/footage_analyzer.py",
    "apps/remotion-sync/sync_timeline.py",
    "apps/qc-engine/qc_project.py",
    "remotion/package.json",
    "remotion/src/Root.tsx",
]


def run_version(command: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        output = (result.stdout or result.stderr).strip().splitlines()
        return result.returncode == 0, output[0] if output else "installed"
    except FileNotFoundError:
        return False, "not found"


def print_check(ok: bool, name: str, detail: str) -> None:
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {name}: {detail}")


def main() -> None:
    print("TURVIS System Doctor")
    print(f"Repository: {REPO_ROOT}\n")

    py_ok = sys.version_info >= (3, 10)
    print_check(py_ok, "Python", sys.version.split()[0])

    for name, command in [
        ("FFmpeg", ["ffmpeg", "-version"]),
        ("FFprobe", ["ffprobe", "-version"]),
        ("Node", ["node", "--version"]),
        ("npm", ["npm", "--version"]),
    ]:
        ok, detail = run_version(command)
        print_check(ok, name, detail)

    print("")
    for rel in CHECK_PATHS:
        path = REPO_ROOT / rel
        print_check(path.exists(), rel, "exists" if path.exists() else "missing")

    print("")
    if shutil.which("ffmpeg") is None:
        print("Install FFmpeg before footage analysis/keyframe extraction.")
    if shutil.which("node") is None or shutil.which("npm") is None:
        print("Install Node.js before Remotion preview/render.")


if __name__ == "__main__":
    main()
