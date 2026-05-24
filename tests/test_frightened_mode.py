import pytest

from game.app import GameApp
from game.config import GameConfig
from game.entities import GameState, Pacman, STOP
from game.movement import tile_center

pytestmark = pytest.mark.unit


def open_maze(maze_factory, power_at=(2, 2)):
    return maze_factory(
        layout=[
            "#####",
            "#...#",
            "#...#",
            "#...#",
            "#####",
        ],
        power_pellets={power_at},
    )


def test_power_pellet_activates_frightened_timer(
    game_config: GameConfig,
    maze_factory,
) -> None:
    app = GameApp(game_config)
    app.maze = open_maze(maze_factory)
    app.state = GameState(score=0, lives=3, pellets_left=5)
    app.pacman = Pacman(
        pos=tile_center(2, 2, game_config.tile_size),
        direction=STOP,
        desired_direction=STOP,
        speed=game_config.pacman_speed,
    )

    expected = game_config.frightened_duration_for_level(app.state.level)

    app._update_pacman(0.0)

    assert app.state.frightened_timer == pytest.approx(expected)
    assert app.state.score == 50


def test_frightened_timer_decays_with_dt(game_config: GameConfig) -> None:
    app = GameApp(game_config)
    app.state.frightened_timer = 2.0
    app.state.ready_timer = 0.0

    app._update(0.5)

    assert app.state.frightened_timer == pytest.approx(1.5)


def test_frightened_timer_clamps_at_zero_and_resets_combo(
    game_config: GameConfig,
) -> None:
    app = GameApp(game_config)
    app.state.frightened_timer = 0.1
    app.state.frightened_combo = 3
    app.state.ready_timer = 0.0

    app._update(0.5)

    assert app.state.frightened_timer == 0.0
    assert app.state.frightened_combo == 0


def test_frightened_mode_slows_ghosts(game_config: GameConfig) -> None:
    app = GameApp(game_config)
    app.state.frightened_timer = 5.0
    app.state.ready_timer = 0.0
    base_ghost_speed = game_config.ghost_speed_for_level(app.state.level)

    app._update_ghosts(0.016)

    expected = base_ghost_speed * GameApp.FRIGHTENED_GHOST_SPEED_RATIO
    for ghost in app.ghosts:
        assert ghost.speed == pytest.approx(expected)


def test_normal_mode_keeps_full_ghost_speed(game_config: GameConfig) -> None:
    app = GameApp(game_config)
    app.state.frightened_timer = 0.0
    app.state.ready_timer = 0.0
    base_ghost_speed = game_config.ghost_speed_for_level(app.state.level)

    app._update_ghosts(0.016)

    for ghost in app.ghosts:
        assert ghost.speed == pytest.approx(base_ghost_speed)
