"""Reusable Dijkstra shortest-path implementation for non-negative graphs."""

from __future__ import annotations

from collections.abc import Hashable, Mapping
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from math import inf, isfinite
from numbers import Real
from typing import TypeAlias

Node: TypeAlias = Hashable
Graph: TypeAlias = Mapping[Node, Mapping[Node, Real]]


@dataclass(frozen=True)
class PathResult:
    """The total distance and ordered nodes for a reachable shortest path."""

    distance: Real
    path: tuple[Node, ...]


def shortest_path(graph: Graph, source: Node, target: Node) -> PathResult | None:
    """Return the shortest path from *source* to *target*, or ``None`` if unreachable.

    ``graph`` maps each node to its outgoing neighbors and non-negative edge
    weights. The graph may be directed or undirected, as represented by its
    supplied edges. A negative edge weight raises ``ValueError`` because
    Dijkstra's algorithm is not valid for such graphs.
    """
    _validate_graph(graph)
    if source not in graph:
        raise KeyError(f"source node {source!r} is not in the graph")
    if target not in graph:
        raise KeyError(f"target node {target!r} is not in the graph")

    distances: dict[Node, Real] = {source: 0}
    predecessors: dict[Node, Node] = {}
    sequence = count()
    queue: list[tuple[Real, int, Node]] = [(0, next(sequence), source)]

    while queue:
        current_distance, _, current = heappop(queue)
        if current_distance != distances[current]:
            continue
        if current == target:
            return PathResult(current_distance, _reconstruct_path(predecessors, source, target))

        for neighbor, weight in graph[current].items():
            candidate_distance = current_distance + weight
            if candidate_distance < distances.get(neighbor, inf):
                distances[neighbor] = candidate_distance
                predecessors[neighbor] = current
                heappush(queue, (candidate_distance, next(sequence), neighbor))

    return None


def _validate_graph(graph: Graph) -> None:
    if not isinstance(graph, Mapping):
        raise TypeError("graph must be an adjacency mapping")

    for current, neighbors in graph.items():
        if not isinstance(neighbors, Mapping):
            raise TypeError(f"adjacency for node {current!r} must be a mapping")
        for neighbor, weight in neighbors.items():
            if not isinstance(weight, Real) or isinstance(weight, bool) or not isfinite(weight) or weight < 0:
                raise ValueError(f"edge {current!r} -> {neighbor!r} has an invalid weight: {weight!r}")
            if neighbor not in graph:
                raise KeyError(f"neighbor node {neighbor!r} is not in the graph")


def _reconstruct_path(predecessors: Mapping[Node, Node], source: Node, target: Node) -> tuple[Node, ...]:
    path = [target]
    while path[-1] != source:
        path.append(predecessors[path[-1]])
    path.reverse()
    return tuple(path)


__all__ = ["Graph", "Node", "PathResult", "shortest_path"]
