#!/usr/bin/env python3
"""Build a Director Decision Graph from director-decisions.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Director Decision Graph")
    parser.add_argument("--project-folder", required=True, help="Project folder containing director-decisions.json")
    return parser.parse_args()


def node(node_id: str, node_type: str, label: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"id": node_id, "type": node_type, "label": label, "data": data or {}}


def edge(source: str, target: str, relation: str, reason: str = "") -> dict[str, str]:
    return {"source": source, "target": target, "relation": relation, "reason": reason}


def build_graph(decisions: list[dict[str, Any]]) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []

    for decision in decisions:
        decision_id = decision.get("id", "decision")
        narration_id = f"{decision_id}:narration"
        emotion_id = f"{decision_id}:emotion"
        visual_id = f"{decision_id}:visual"
        shot_id = f"{decision_id}:shot"
        subtitle_id = f"{decision_id}:subtitle"
        silence_id = f"{decision_id}:silence"
        rhythm_id = f"{decision_id}:rhythm"
        decision_node_id = f"{decision_id}:decision"

        nodes.extend([
            node(narration_id, "narration", decision.get("narration", "")),
            node(emotion_id, "emotion", decision.get("emotion", "unknown")),
            node(visual_id, "visual_intention", decision.get("visual_intention", "unknown")),
            node(shot_id, "shot_preference", decision.get("shot_preference", "unknown")),
            node(subtitle_id, "subtitle_strategy", decision.get("subtitle_strategy", "unknown")),
            node(silence_id, "silence_need", decision.get("silence_need", "unknown")),
            node(rhythm_id, "rhythm", decision.get("rhythm", "unknown")),
            node(decision_node_id, "director_decision", decision_id, {"reasoning": decision.get("reasoning", "")}),
        ])

        edges.extend([
            edge(narration_id, emotion_id, "suggests", "Narration keywords imply emotion."),
            edge(narration_id, visual_id, "suggests", "Narration imagery implies visual intention."),
            edge(emotion_id, rhythm_id, "shapes", "Emotion changes pacing."),
            edge(visual_id, shot_id, "requires", "Visual intention implies shot preference."),
            edge(emotion_id, silence_id, "controls", "Emotion controls silence level."),
            edge(rhythm_id, subtitle_id, "shapes", "Rhythm shapes subtitle timing."),
            edge(shot_id, decision_node_id, "feeds", "Shot is one component of final decision."),
            edge(subtitle_id, decision_node_id, "feeds", "Subtitle strategy is one component of final decision."),
            edge(silence_id, decision_node_id, "feeds", "Silence is one component of final decision."),
        ])

        dna = decision.get("adventure_dna")
        if dna:
            dna_id = f"{decision_id}:adventure_dna"
            nodes.append(node(dna_id, "adventure_dna", f"{dna.get('id')} — {dna.get('name')}", dna))
            edges.extend([
                edge(emotion_id, dna_id, "matches", "Emotion and visual intention match Adventure DNA."),
                edge(dna_id, shot_id, "influences", dna.get("visual_rule", "")),
                edge(dna_id, subtitle_id, "influences", dna.get("subtitle_rule", "")),
                edge(dna_id, silence_id, "influences", dna.get("silence_rule", "")),
                edge(dna_id, decision_node_id, "justifies", dna.get("reasoning", "")),
            ])

    return {
        "schema": "turvis.director.decision_graph.v0.1",
        "nodes": nodes,
        "edges": edges,
    }


def build_markdown(graph: dict[str, Any]) -> str:
    content = "# Director Decision Graph\n\n"
    content += f"Nodes: {len(graph.get('nodes', []))}  \n"
    content += f"Edges: {len(graph.get('edges', []))}  \n\n"
    content += "## Edges\n\n"
    content += "| Source | Relation | Target | Reason |\n"
    content += "|---|---|---|---|\n"
    for item in graph.get("edges", []):
        content += f"| {item['source']} | {item['relation']} | {item['target']} | {item.get('reason', '')} |\n"
    return content


def main() -> None:
    args = parse_args()
    project_folder = Path(args.project_folder).expanduser().resolve()
    decisions_path = project_folder / "director-decisions.json"
    if not decisions_path.exists():
        raise FileNotFoundError(f"Missing director decisions: {decisions_path}")

    data = json.loads(decisions_path.read_text(encoding="utf-8"))
    decisions = data.get("decisions", [])
    graph = build_graph(decisions)

    (project_folder / "director-decision-graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    (project_folder / "director-decision-graph.md").write_text(build_markdown(graph), encoding="utf-8")

    print(f"Created: {project_folder / 'director-decision-graph.json'}")
    print(f"Created: {project_folder / 'director-decision-graph.md'}")


if __name__ == "__main__":
    main()
