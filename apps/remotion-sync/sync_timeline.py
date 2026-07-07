#!/usr/bin/env python3
"""Sync project timeline.remotion.json into remotion/src/data/turvis.timeline.ts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync project Remotion timeline into Remotion app data")
    parser.add_argument("--project-folder", required=True, help="Project folder containing timeline.remotion.json")
    parser.add_argument("--output", default="remotion/src/data/turvis.timeline.ts", help="Output TypeScript data file")
    return parser.parse_args()


def ts_stringify(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def main() -> None:
    args = parse_args()
    project_folder = Path(args.project_folder).expanduser().resolve()
    source_path = project_folder / "timeline.remotion.json"
    if not source_path.exists():
        raise FileNotFoundError(f"Missing Remotion timeline: {source_path}")

    data = json.loads(source_path.read_text(encoding="utf-8"))
    output_path = (REPO_ROOT / args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = "import type { TurvisRemotionTimeline } from '../types';\n\n"
    content += "export const turvisTimeline: TurvisRemotionTimeline = "
    content += ts_stringify(data)
    content += ";\n"

    output_path.write_text(content, encoding="utf-8")
    print(f"Synced timeline: {source_path} -> {output_path}")


if __name__ == "__main__":
    main()
