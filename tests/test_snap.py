import pytest

from game.entities import Vec2
from game.movement import snap_to_tile_center, tile_center

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("offset_x", "offset_y"),
    [
        (0.0, 0.0),
        (1.5, -1.0),
        (-2.4, 2.0),
    ],
)
def test_snap_pulls_close_positions_to_center(offset_x: float, offset_y: float) -> None:
    tile_size = 20
    center = tile_center(2, 3, tile_size)
    pos = Vec2(center.x + offset_x, center.y + offset_y)

    result = snap_to_tile_center(pos, tile_size)

    assert result == center


@pytest.mark.parametrize(
    ("offset_x", "offset_y"),
    [
        (5.0, 0.0),
        (0.0, -6.0),
        (3.0, 3.0),
    ],
)
def test_snap_leaves_distant_positions_unchanged(offset_x: float, offset_y: float) -> None:
    tile_size = 20
    center = tile_center(2, 3, tile_size)
    pos = Vec2(center.x + offset_x, center.y + offset_y)

    result = snap_to_tile_center(pos, tile_size)

    assert result is pos


def test_snap_respects_custom_tolerance() -> None:
    tile_size = 20
    center = tile_center(1, 1, tile_size)
    pos = Vec2(center.x + 4.0, center.y)

    assert snap_to_tile_center(pos, tile_size, tolerance=5.0) == center
    assert snap_to_tile_center(pos, tile_size, tolerance=2.0) is pos


def test_snap_is_idempotent_at_center() -> None:
    tile_size = 28
    center = tile_center(4, 4, tile_size)

    first = snap_to_tile_center(center, tile_size)
    second = snap_to_tile_center(first, tile_size)

    assert first == center
    assert second == center
