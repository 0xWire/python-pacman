import pytest

from game.app import GameApp
from game.config import GameConfig
from game.entities import GameState, Pacman, STOP
from game.movement import tile_center

pytestmark = [pytest.mark.unit, pytest.mark.levels]


def test_advance_level_loads_next_maze_and_bumps_counter(
    game_config: GameConfig,
) -> None:
    app = GameApp(game_config)
    starting_name = app.maze.name
    starting_level = app.state.level

    app._advance_level()

    assert app.state.level == starting_level + 1
    assert app.maze.name != starting_name
    assert app.maze.name in app.maze_names
    assert app.state.pellets_left == len(app.maze.pellets) + len(app.maze.power_pellets)


def test_advance_level_cycles_back_to_first_maze(game_config: GameConfig) -> None:
    app = GameApp(game_config)
    total = len(app.maze_names)
    first_name = app.maze.name

    for _ in range(total):
        app._advance_level()

    assert app.maze.name == first_name
    assert app.state.level == 1 + total


def test_advance_level_resets_positions_and_ready_timer(
    game_config: GameConfig,
) -> None:
    app = GameApp(game_config)
    app.state.ready_timer = 0.0
    app.elapsed = 9.9
    app.mouth_timer = 7.7

    app._advance_level()

    assert app.state.ready_timer == pytest.approx(GameApp.READY_DURATION)
    assert app.elapsed == 0.0
    assert app.mouth_timer == 0.0


def test_eating_last_pellet_triggers_advance(
    game_config: GameConfig,
    maze_factory,
) -> None:
    app = GameApp(game_config)
    app.maze = maze_factory(
        layout=[
            "#####",
            "#...#",
            "#...#",
            "#...#",
            "#####",
        ],
        pellets={(2, 2)},
    )
    app.state = GameState(score=0, lives=3, pellets_left=1)
    app.pacman = Pacman(
        pos=tile_center(2, 2, game_config.tile_size),
        direction=STOP,
        desired_direction=STOP,
        speed=game_config.pacman_speed,
    )
    starting_level = app.state.level

    app._update_pacman(0.0)

    assert app.state.level == starting_level + 1
    assert app.state.pellets_left == len(app.maze.pellets) + len(app.maze.power_pellets)
