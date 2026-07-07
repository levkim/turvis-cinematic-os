"""Adventure DNA matcher for Director Intelligence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DNA_PATH = REPO_ROOT / "knowledge/adventure-dna/adventure-dna-v0.1.json"


def load_adventure_dna(path: Path = DEFAULT_DNA_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    principles = data.get("principles", [])
    return principles if isinstance(principles, list) else []


def score_dna(decision: dict[str, Any], principle: dict[str, Any]) -> int:
    score = 0
    if decision.get("emotion") == principle.get("emotion"):
        score += 3
    if decision.get("visual_intention") in principle.get("camera_preference", []):
        score += 3
    if decision.get("shot_preference") in principle.get("camera_preference", []):
        score += 2
    text = str(decision.get("narration", ""))
    story_use = str(principle.get("story_use", ""))
    name = str(principle.get("name", ""))
    if story_use and story_use in text.lower():
        score += 1
    if "도착" in text and principle.get("story_use") == "arrival":
        score += 2
    if "작은" in text and principle.get("story_use") == "scale":
        score += 2
    if "은하수" in text and principle.get("story_use") == "reflection":
        score += 3
    if "지층" in text or "층" in text:
        if principle.get("story_use") == "texture":
            score += 2
    if "끝" in text or "마지막" in text:
        if principle.get("story_use") == "threshold":
            score += 2
    if name and name.lower() in text.lower():
        score += 1
    return score


def match_adventure_dna(decision: dict[str, Any], principles: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    principles = principles if principles is not None else load_adventure_dna()
    if not principles:
        return None
    ranked = sorted(principles, key=lambda p: score_dna(decision, p), reverse=True)
    best = ranked[0]
    if score_dna(decision, best) <= 0:
        return None
    return best


def apply_adventure_dna(decision: dict[str, Any], principles: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    match = match_adventure_dna(decision, principles)
    if not match:
        decision["adventure_dna"] = None
        return decision

    decision["adventure_dna"] = {
        "id": match.get("id"),
        "name": match.get("name"),
        "story_use": match.get("story_use"),
        "visual_rule": match.get("visual_rule"),
        "subtitle_rule": match.get("subtitle_rule"),
        "silence_rule": match.get("silence_rule"),
        "reasoning": match.get("reasoning"),
    }
    decision["reasoning"] = (
        f"{decision.get('reasoning', '')} Adventure DNA matched: "
        f"{match.get('id')} {match.get('name')} — {match.get('reasoning')}"
    ).strip()
    return decision
