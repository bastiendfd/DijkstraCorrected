# Dijkstra Corrected

A small **educational** Python implementation of Dijkstra's shortest-path algorithm. It exposes a dependency-free library API and a JSON-file command-line interface. It is a portfolio/demo project, **not production routing software**: it has no service interface, performance guarantees, operational support, or security review.

## Requirements and installation

- Python 3.10+
- No runtime dependencies for the library or CLI

```bash
python -m pip install .
```

For development tests:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

The retained original notebook uses NumPy, SciPy, and Jupyter. Install those only if you want to run it:

```bash
python -m pip install -e ".[notebook]"
```

## Library usage

The graph is an adjacency map. Add reverse edges yourself when the graph is undirected.

```python
from dijkstra_corrected import shortest_path

graph = {
    "A": {"B": 4, "C": 1},
    "B": {"A": 4, "C": 2, "D": 1},
    "C": {"A": 1, "B": 2, "D": 5},
    "D": {"B": 1, "C": 5},
}

result = shortest_path(graph, "A", "D")
# PathResult(distance=4, path=("A", "C", "B", "D"))
```

`shortest_path` returns `None` when the target cannot be reached. It raises `ValueError` for negative or non-numeric edge weights, because Dijkstra's algorithm does not support them. Source, target, and neighbor nodes must appear as top-level graph keys.

## CLI usage

Save a JSON adjacency map, for example `graph.json`:

```json
{
  "A": {"B": 2, "C": 5},
  "B": {"C": 1},
  "C": {}
}
```

Then run either command:

```bash
python -m dijkstra_corrected --graph graph.json --source A --target C
# {"distance": 3, "path": ["A", "B", "C"]}

dijkstra-corrected --graph graph.json --source A --target C
```

The CLI prints `null` when no route exists, emits input errors on stderr, and exits non-zero for invalid graph files or invalid node/weight data.

## Algorithm notes

Dijkstra's algorithm requires non-negative edge weights. With a binary heap, the implementation runs in `O((V + E) log V)` time for a graph with vertices `V` and edges `E`. Equal-cost paths are valid alternatives; avoid depending on a particular tie-breaking order.

## Notebook

`dijkstras.ipynb` is retained as the original exploratory city-network notebook. The package and tests are the maintained interface; the notebook is illustrative and not used by CI.

## Development

```bash
python -m pytest -q
python -m build
```

See [SECURITY.md](SECURITY.md) for responsible disclosure guidance.
