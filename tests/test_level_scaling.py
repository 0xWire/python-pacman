import pytest

from game.config import GameConfig

pytestmark = pytest.mark.unit


@pytest.fixture
def base_config() -> GameConfig:
    return GameConfig(pacman_speed=100.0, ghost_speed=90.0)


@pytest.mark.parametrize(
    ("level", "expected"),
    [
        (1, 90.0),
        (2, 94.0),
        (5, 106.0),
        (10, 108.0),
        (100, 108.0),
    ],
)
def test_ghost_speed_grows_and_caps(
    base_config: GameConfig,
    level: int,
    expected: float,
) -> None:
    assert base_config.ghost_speed_for_level(level) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("level", "expected"),
    [
        (1, 100.0),
        (2, 102.0),
        (5, 108.0),
        (10, 110.0),
        (100, 110.0),
    ],
)
def test_pacman_speed_grows_and_caps(
    base_config: GameConfig,
    level: int,
    expected: float,
) -> None:
    assert base_config.pacman_speed_for_level(level) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("level", "expected"),
    [
        (1, 6.0),
        (2, 5.65),
        (5, 4.6),
        (10, 3.0),
        (50, 3.0),
    ],
)
def test_frightened_window_shrinks_and_caps(
    base_config: GameConfig,
    level: int,
    expected: float,
) -> None:
    assert base_config.frightened_duration_for_level(level) == pytest.approx(expected)


def test_speeds_grow_monotonically(base_config: GameConfig) -> None:
    prior_ghost = base_config.ghost_speed_for_level(1)
    prior_pacman = base_config.pacman_speed_for_level(1)
    for level in range(2, 11):
        current_ghost = base_config.ghost_speed_for_level(level)
        current_pacman = base_config.pacman_speed_for_level(level)
        assert current_ghost >= prior_ghost
        assert current_pacman >= prior_pacman
        prior_ghost, prior_pacman = current_ghost, current_pacman


def test_frightened_window_decreases_monotonically(base_config: GameConfig) -> None:
    prior = base_config.frightened_duration_for_level(1)
    for level in range(2, 12):
        current = base_config.frightened_duration_for_level(level)
        assert current <= prior
        prior = current
