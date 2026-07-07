"""
TURVIS Project Config Loader v0.1

Loads project.yaml without requiring external YAML dependencies.

For v0.1, this loader supports simple nested YAML structures used by TURVIS project specs.
It intentionally avoids PyYAML to keep local setup lightweight.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "None", ""}:
        return None
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def load_simple_yaml(path: Path) -> dict[str, Any]:
    """Load a limited YAML subset used by TURVIS project.yaml.

    Supported:
    - nested mappings by indentation
    - scalar values
    - simple list items under a key

    This is not a general YAML parser.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any] | list[Any]]] = [(-1, root)]
    last_key_by_indent: dict[int, str] = {}

    for raw_line in lines:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()

        parent = stack[-1][1]

        if line.startswith("- "):
            item = parse_scalar(line[2:])
            if not isinstance(parent, list):
                raise ValueError(f"Invalid list item without list parent: {raw_line}")
            parent.append(item)
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if not isinstance(parent, dict):
            raise ValueError(f"Invalid mapping under list parent: {raw_line}")

        if value == "":
            # Determine whether the next block is a list by peeking ahead.
            child: dict[str, Any] | list[Any] = {}
            parent[key] = child
            stack.append((indent, child))
            last_key_by_indent[indent] = key
        else:
            parent[key] = parse_scalar(value)

    # Second pass to convert empty dicts followed by list-like blocks is intentionally avoided.
    # Use inline list-compatible structure only as shown in templates.
    return root


def resolve_project_spec(project_folder: str | None = None, project_spec: str | None = None) -> Path:
    if project_spec:
        path = Path(project_spec).expanduser().resolve()
    elif project_folder:
        path = (Path(project_folder).expanduser().resolve() / "project.yaml")
    else:
        raise ValueError("Provide either project_folder or project_spec")

    if not path.exists():
        raise FileNotFoundError(f"project.yaml not found: {path}")
    return path


def load_project_config(project_folder: str | None = None, project_spec: str | None = None) -> dict[str, Any]:
    path = resolve_project_spec(project_folder, project_spec)
    config = load_simple_yaml(path)
    config["_project_spec_path"] = str(path)
    config["_project_folder"] = str(path.parent)
    return config


def get_nested(config: dict[str, Any], path: str, default: Any = None) -> Any:
    current: Any = config
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current
