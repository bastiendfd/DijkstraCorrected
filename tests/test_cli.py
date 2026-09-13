import json
import subprocess
import sys


def test_cli_reads_graph_file_and_prints_shortest_path(tmp_path):
    graph_file = tmp_path / "graph.json"
    graph_file.write_text(
        json.dumps({"A": {"B": 2, "C": 5}, "B": {"C": 1}, "C": {}}),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "dijkstra_corrected",
            "--graph",
            str(graph_file),
            "--source",
            "A",
            "--target",
            "C",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert json.loads(completed.stdout) == {"distance": 3, "path": ["A", "B", "C"]}


def test_cli_reports_malformed_adjacency_as_a_concise_error(tmp_path):
    graph_file = tmp_path / "graph.json"
    graph_file.write_text(
        json.dumps({"A": {"B": 1}, "B": [], "C": {}}),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "dijkstra_corrected",
            "--graph",
            str(graph_file),
            "--source",
            "A",
            "--target",
            "C",
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    assert completed.returncode != 0
    assert "error: adjacency for node 'B' must be a mapping" in completed.stderr
    assert "Traceback" not in completed.stderr
