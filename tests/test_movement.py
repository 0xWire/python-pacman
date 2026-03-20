import pytest

from game.entities import LEFT, RIGHT, STOP, UP, Vec2
from game.movement import (
    can_move,
    near_tile_center,
    squared_distance,
    step,
    tile_center,
    world_distance,
    world_to_tile,
)

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("col", "row", "tile_size", "expected"),
    [
        (0, 0, 20, Vec2(10.0, 10.0)),
        (2, 3, 16, Vec2(40.0, 56.0)),
    ],
)
def test_tile_center_returns_middle_of_tile(
    col: int,
    row: int,
    tile_size: int,
    expected: Vec2,
) -> None:
    assert tile_center(col, row, tile_size) == expected


@pytest.mark.parametrize(
    ("position", "tile_size", "expected"),
    [
        (Vec2(0.0, 0.0), 20, (0, 0)),
        (Vec2(39.9, 40.0), 20, (1, 2)),
        (Vec2(59.9, 79.9), 20, (2, 3)),
    ],
)
def test_world_to_tile_uses_floor_division(
    position: Vec2,
    tile_size: int,
    expected: tuple[int, int],
) -> None:
    assert world_to_tile(position, tile_size) == expected


@pytest.mark.parametrize(
    ("position", "tolerance", "expected"),
    [
        (Vec2(50.0, 50.0), 2.5, True),
        (Vec2(52.4, 49.0), 2.5, True),
        (Vec2(53.0, 50.0), 2.5, False),
    ],
)
def test_near_tile_center_respects_tolerance(
    position: Vec2,
    tolerance: float,
    expected: bool,
) -> None:
    assert near_tile_center(position, 20, tolerance=tolerance) is expected


def test_can_move_allows_idle_direction(sample_maze) -> None:
    pos = tile_center(2, 2, 20)

    assert can_move(sample_maze, pos, STOP, 20) is True


@pytest.mark.parametrize(
    ("position", "direction", "expected"),
    [
        (tile_center(2, 2, 20), RIGHT, True),
        (tile_center(1, 1, 20), LEFT, False),
        (tile_center(1, 1, 20), UP, False),
    ],
)
def test_can_move_checks_walls_ahead(position: Vec2, direction: Vec2, expected: bool, sample_maze) -> None:
    assert can_move(sample_maze, position, direction, 20) is expected


@pytest.mark.parametrize(
    ("direction", "speed", "dt", "expected"),
    [
        (RIGHT, 100.0, 0.1, Vec2(20.0, 10.0)),
        (LEFT, 50.0, 0.2, Vec2(0.0, 10.0)),
    ],
)
def test_step_moves_position_by_speed_and_delta_time(
    direction: Vec2,
    speed: float,
    dt: float,
    expected: Vec2,
) -> None:
    start = Vec2(10.0, 10.0)

    assert step(start, direction, speed, dt) == expected


@pytest.mark.parametrize(
    ("point_a", "point_b", "expected"),
    [
        ((0, 0), (3, 4), 25),
        ((2, 2), (2, 2), 0),
    ],
)
def test_squared_distance_returns_cartesian_distance_squared(
    point_a: tuple[int, int],
    point_b: tuple[int, int],
    expected: int,
) -> None:
    assert squared_distance(point_a, point_b) == expected


def test_world_distance_returns_euclidean_distance() -> None:
    assert world_distance(Vec2(0.0, 0.0), Vec2(3.0, 4.0)) == pytest.approx(5.0)
