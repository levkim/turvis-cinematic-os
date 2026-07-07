#!/usr/bin/env python3
"""
TURVIS Project Validator v0.1

Validates project.yaml before running engines.

Local-first. No AI API calls.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from apps.common.project_config import get_nested, load_project_config  # noqa: E402

REQUIRED_FIELDS = [
    "project.id",
    "project.title",
    "project.type",
    "paths.footage",
    "paths.keyframes",
    "paths.memory",
    "paths.narration",
    "paths.director_handoff",
]

RECOMMENDED_FIELDS = [
    "project.clip_prefix",
    "project.episode",
    "output.aspect_ratio",
    "output.resolution",
    "output.target_duration_seconds",
    "output.language",
    "locations.country",
    "locations.region",
    "locations.destination",
    "rules.local_first",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate TURVIS project.yaml")
    parser.add_argument("--project-folder", default=None, help="Project folder containing project.yaml")
    parser.add_argument("--project-spec", default=None, help="Path to project.yaml")
    parser.add_argument("--strict-paths", action="store_true", help="Fail if configured paths do not exist")
    return parser.parse_args()


def check_fields(config: dict[str, Any], fields: list[str]) -> list[str]:
    missing: list[str] = []
    for field in fields:
        value = get_nested(config, field)
        if value in {None, ""}:
            missing.append(field)
    return missing


def check_paths(config: dict[str, Any], strict: bool) -> list[str]:
    warnings: list[str] = []
    path_fields = [
        "paths.footage",
        "paths.keyframes",
        "paths.memory",
        "paths.narration",
    ]
    for field in path_fields:
        value = get_nested(config, field)
        if not value:
            continue
        path = Path(str(value)).expanduser()
        if not path.exists():
            label = f"{field}: {path} does not exist"
            warnings.append(label)
            if strict:
                raise FileNotFoundError(label)
    return warnings


def main() -> None:
    args = parse_args()
    config = load_project_config(project_folder=args.project_folder, project_spec=args.project_spec)

    missing_required = check_fields(config, REQUIRED_FIELDS)
    missing_recommended = check_fields(config, RECOMMENDED_FIELDS)

    if missing_required:
        print("Project validation failed. Missing required fields:")
        for field in missing_required:
            print(f"- {field}")
        raise SystemExit(1)

    path_warnings = check_paths(config, strict=args.strict_paths)

    print("Project validation passed.")
    print(f"Project: {get_nested(config, 'project.title', 'Untitled Project')}")
    print(f"Spec: {config.get('_project_spec_path')}")

    if missing_recommended:
        print("\nRecommended fields missing:")
        for field in missing_recommended:
            print(f"- {field}")

    if path_warnings:
        print("\nPath warnings:")
        for warning in path_warnings:
            print(f"- {warning}")


if __name__ == "__main__":
    main()
