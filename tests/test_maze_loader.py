import pytest

from game import maze as maze_module
from game.maze import load_maze

pytestmark = [pytest.mark.unit, pytest.mark.levels]


def test_load_maze_rejects_unknown_name() -> None:
    with pytest.raises(ValueError, match="Unknown maze"):
        load_maze("does-not-exist")


@pytest.mark.parametrize(
    ("bad_layout", "match"),
    [
        ([], "at least one row"),
        ([""], "empty rows"),
        (["####", "###"], "rectangular"),
        (["####", "##"], "rectangular"),
    ],
)
def test_load_maze_rejects_invalid_layout(monkeypatch, bad_layout, match) -> None:
    monkeypatch.setitem(maze_module.MAZE_LAYOUTS, "broken", bad_layout)

    with pytest.raises(ValueError, match=match):
        load_maze("broken")


def test_load_maze_attaches_name_to_result() -> None:
    maze = load_maze("classic")

    assert maze.name == "classic"


def test_load_maze_loops_layout_collects_pellets_and_spawns() -> None:
    maze = load_maze("loops")

    assert maze.name == "loops"
    assert maze.pacman_spawn == (13, 16)
    assert len(maze.ghost_spawns) == 4
    assert len(maze.pellets) > 0
    assert len(maze.power_pellets) >= 2
