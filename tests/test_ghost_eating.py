import pytest

from game.app import GameApp
from game.config import GameConfig
from game.entities import GameState, Ghost, STOP
from game.movement import tile_center

pytestmark = pytest.mark.unit


def collide_pacman_with(ghost: Ghost, app: GameApp) -> None:
    ghost.pos = app.pacman.pos


@pytest.mark.parametrize(
    ("combo_before", "expected_award"),
    [
        (0, 200),
        (1, 400),
        (2, 800),
        (3, 1600),
    ],
)
def test_eating_frightened_ghost_awards_doubling_combo(
    game_config: GameConfig,
    combo_before: int,
    expected_award: int,
) -> None:
    app = GameApp(game_config)
    app.state = GameState(
        score=0,
        lives=3,
        pellets_left=10,
        frightened_timer=4.0,
        frightened_combo=combo_before,
    )
    app.pacman.pos = tile_center(5, 5, game_config.tile_size)
    collide_pacman_with(app.ghosts[0], app)
    app.ghosts = app.ghosts[:1]

    app._check_collisions()

    assert app.state.score == expected_award
    assert app.state.frightened_combo == combo_before + 1
    assert app.state.lives == 3


def test_eaten_ghost_respawns_at_spawn_tile(game_config: GameConfig) -> None:
    app = GameApp(game_config)
    app.state = GameState(
        score=0,
        lives=3,
        pellets_left=10,
        frightened_timer=4.0,
    )
    app.pacman.pos = tile_center(5, 5, game_config.tile_size)
    ghost = app.ghosts[0]
    ghost.spawn_tile = (8, 9)
    collide_pacman_with(ghost, app)
    app.ghosts = [ghost]

    app._check_collisions()

    assert ghost.pos == tile_center(8, 9, game_config.tile_size)
    assert ghost.direction == STOP


def test_collision_without_frightened_costs_a_life(game_config: GameConfig) -> None:
    app = GameApp(game_config)
    app.state = GameState(score=0, lives=3, pellets_left=10, frightened_timer=0.0)
    app.pacman.pos = tile_center(5, 5, game_config.tile_size)
    app.ghosts = [
        Ghost(
            kind="blinky",
            pos=app.pacman.pos,
            direction=STOP,
            speed=90.0,
            spawn_tile=(1, 1),
            scatter_target=(1, 1),
        ),
    ]

    app._check_collisions()

    assert app.state.lives == 2
    assert app.state.score == 0
