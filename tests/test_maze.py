import pytest

from game.maze import load_default_maze

pytestmark = pytest.mark.unit


def test_is_wall_handles_bounds_and_layout_cells(sample_maze) -> None:
    assert sample_maze.is_wall(-1, 1) is True
    assert sample_maze.is_wall(1, -1) is True
    assert sample_maze.is_wall(0, 0) is True
    assert sample_maze.is_wall(2, 2) is False


def test_eat_pellet_returns_score_once_per_collectible(maze_factory) -> None:
    maze = maze_factory(
        layout=[
            "#####",
            "#...#",
            "#...#",
            "#####",
        ],
        pellets={(1, 1)},
        power_pellets={(2, 2)},
    )

    assert maze.eat_pellet(1, 1) == 10
    assert maze.eat_pellet(1, 1) == 0
    assert maze.eat_pellet(2, 2) == 50
    assert maze.eat_pellet(2, 2) == 0
    assert maze.eat_pellet(3, 1) == 0


def test_load_default_maze_finds_expected_spawns_and_collectibles() -> None:
    maze = load_default_maze()

    assert maze.width == 28
    assert maze.height == 20
    assert maze.pacman_spawn == (13, 16)
    assert maze.ghost_spawns == [(12, 9), (13, 9), (14, 9), (15, 9)]
    assert len(maze.pellets) > 0
    assert maze.power_pellets == {(1, 3), (26, 3), (1, 18), (26, 18)}
