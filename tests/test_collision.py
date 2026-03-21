import pytest

from game.collision import collides_with_ghost
from game.entities import Ghost, Pacman, STOP, Vec2

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("ghost_pos", "radius", "expected"),
    [
        (Vec2(13.0, 14.0), 5.0, True),
        (Vec2(14.0, 14.0), 5.0, False),
        (Vec2(10.0, 10.0), 0.0, True),
    ],
)
def test_collides_with_ghost_respects_distance_threshold(
    ghost_pos: Vec2,
    radius: float,
    expected: bool,
) -> None:
    pacman = Pacman(pos=Vec2(10.0, 10.0), direction=STOP, desired_direction=STOP, speed=100.0)
    ghost = Ghost(
        kind="blinky",
        pos=ghost_pos,
        direction=STOP,
        speed=90.0,
        scatter_target=(0, 0),
    )

    assert collides_with_ghost(pacman, ghost, radius) is expected
