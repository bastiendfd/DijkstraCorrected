"""Command-line interface for calculating a path from a JSON graph."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from . import shortest_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Calculate a shortest path with Dijkstra's algorithm.")
    parser.add_argument("--graph", type=Path, required=True, help="Path to a JSON adjacency-map graph.")
    parser.add_argument("--source", required=True, help="Start node identifier.")
    parser.add_argument("--target", required=True, help="Destination node identifier.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        graph = json.loads(args.graph.read_text(encoding="utf-8"))
        if not isinstance(graph, dict):
            raise TypeError("graph JSON must be an object mapping nodes to neighbor objects")
        result = shortest_path(graph, args.source, args.target)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        parser.error(str(error))

    payload = None if result is None else {"distance": result.distance, "path": list(result.path)}
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    main()
