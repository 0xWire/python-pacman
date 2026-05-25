import pytest

from game.entities import LEFT, RIGHT, Vec2
from game.movement import can_move, wrap_position

pytestmark = pytest.mark.unit


@pytest.fixture
def tunnel_maze(maze_factory):
    return maze_factory(
        layout=[
            "#####",
            "#...#",
            ".....",
            "#...#",
            "#####",
        ],
    )


@pytest.mark.parametrize(
    ("position", "expected_x"),
    [
        (Vec2(-30.0, 40.0), 90.0),
        (Vec2(105.0, 40.0), -10.0),
        (Vec2(50.0, 40.0), 50.0),
    ],
)
def test_wrap_position_wraps_horizontally(
    tunnel_maze,
    position: Vec2,
    expected_x: float,
) -> None:
    result = wrap_position(tunnel_maze, position, tile_size=20)

    assert result.x == pytest.approx(expected_x)
    assert result.y == pytest.approx(position.y)


@pytest.mark.parametrize(
    ("y_offset",),
    [
        (-50.0,),
        (200.0,),
    ],
)
def test_wrap_position_does_not_wrap_vertically(
    tunnel_maze,
    y_offset: float,
) -> None:
    result = wrap_position(tunnel_maze, Vec2(50.0, y_offset), tile_size=20)

    assert result.y == pytest.approx(y_offset)


def test_can_move_through_tunnel_edges(tunnel_maze) -> None:
    left_edge = Vec2(10.0, 50.0)
    right_edge = Vec2(90.0, 50.0)

    assert can_move(tunnel_maze, left_edge, LEFT, 20) is True
    assert can_move(tunnel_maze, right_edge, RIGHT, 20) is True


def test_tunnel_blocked_when_no_opening(maze_factory) -> None:
    sealed = maze_factory(
        layout=[
            "#####",
            "#...#",
            "#...#",
            "#...#",
            "#####",
        ],
    )

    assert can_move(sealed, Vec2(50.0, 50.0), LEFT, 20) is True
    assert can_move(sealed, Vec2(10.0, 50.0), LEFT, 20) is False
    assert can_move(sealed, Vec2(50.0, 50.0), RIGHT, 20) is True
    assert can_move(sealed, Vec2(90.0, 50.0), RIGHT, 20) is False
