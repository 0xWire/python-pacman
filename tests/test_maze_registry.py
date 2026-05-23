import pytest

from game.maze import MAZE_LAYOUTS, available_mazes

pytestmark = pytest.mark.unit


def test_available_mazes_returns_tuple() -> None:
    assert isinstance(available_mazes(), tuple)


def test_available_mazes_includes_known_layouts() -> None:
    names = available_mazes()

    assert "classic" in names
    assert "loops" in names


def test_available_mazes_matches_registry_keys() -> None:
    assert set(available_mazes()) == set(MAZE_LAYOUTS.keys())


def test_available_mazes_is_stable_across_calls() -> None:
    assert available_mazes() == available_mazes()


def test_available_mazes_reflects_new_registry_entry(monkeypatch) -> None:
    extended = dict(MAZE_LAYOUTS)
    extended["temp"] = ["###", "#.#", "###"]
    monkeypatch.setattr("game.maze.MAZE_LAYOUTS", extended)

    assert "temp" in available_mazes()
