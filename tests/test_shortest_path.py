import pytest

from dijkstra_corrected import shortest_path


def test_shortest_path_returns_known_route_and_total_distance():
    graph = {
        "A": {"B": 4, "C": 1},
        "B": {"A": 4, "C": 2, "D": 1},
        "C": {"A": 1, "B": 2, "D": 5},
        "D": {"B": 1, "C": 5},
    }

    result = shortest_path(graph, "A", "D")

    assert result.path == ("A", "C", "B", "D")
    assert result.distance == 4


def test_shortest_path_returns_none_when_target_is_disconnected():
    graph = {
        "A": {"B": 3},
        "B": {"A": 3},
        "C": {},
    }

    assert shortest_path(graph, "A", "C") is None


def test_shortest_path_rejects_negative_weight_in_unvisited_adjacency_map():
    graph = {
        "A": {"B": 1},
        "B": {},
        "C": {"D": -1},
        "D": {},
    }

    with pytest.raises(ValueError, match="invalid weight"):
        shortest_path(graph, "A", "B")


def test_shortest_path_rejects_non_mapping_adjacency_value():
    graph = {"A": {}, "B": []}

    with pytest.raises(TypeError, match="adjacency.*mapping"):
        shortest_path(graph, "A", "A")


@pytest.mark.parametrize("weight", [float("inf"), float("nan")])
def test_shortest_path_rejects_non_finite_weight(weight):
    graph = {"A": {"B": 1}, "B": {}, "C": {"D": weight}, "D": {}}

    with pytest.raises(ValueError, match="invalid weight"):
        shortest_path(graph, "A", "B")
