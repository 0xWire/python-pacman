from unittest.mock import Mock

import pygame
import pytest

from game.app import GameApp
from game.config import GameConfig
from game.entities import LEFT, RIGHT, Ghost, GameState, Pacman, STOP
from game.movement import tile_center

pytestmark = pytest.mark.unit


def build_open_maze(maze_factory):
    return maze_factory(
        layout=[
            "#####",
            "#...#",
            "#...#",
            "#...#",
            "#####",
        ],
    )


def test_spawn_entities_creates_pacman_and_four_ghosts(game_config: GameConfig) -> None:
    app = GameApp(game_config)

    pacman, ghosts = app._spawn_entities()

    assert pacman.pos == tile_center(app.maze.pacman_spawn[0], app.maze.pacman_spawn[1], game_config.tile_size)
    assert pacman.direction == STOP
    assert pacman.desired_direction == STOP
    assert [ghost.kind for ghost in ghosts] == ["blinky", "pinky", "inky", "clyde"]
    assert [ghost.direction for ghost in ghosts] == [LEFT, RIGHT, LEFT, RIGHT]


def test_update_pacman_eats_pellet_and_completes_level(game_config: GameConfig, maze_factory) -> None:
    app = GameApp(game_config)
    app.maze = build_open_maze(maze_factory)
    app.maze.pellets = {(2, 2)}
    app.state = GameState(score=0, lives=3, pellets_left=1)
    app.pacman = Pacman(
        pos=tile_center(2, 2, game_config.tile_size),
        direction=STOP,
        desired_direction=STOP,
        speed=game_config.pacman_speed,
    )

    app._update_pacman(0.1)

    assert app.state.score == 10
    assert app.state.pellets_left == 0
    assert app.state.level_complete is True


def test_update_pacman_switches_to_desired_direction_when_path_is_open(
    game_config: GameConfig,
    maze_factory,
) -> None:
    app = GameApp(game_config)
    app.maze = build_open_maze(maze_factory)
    start = tile_center(2, 2, game_config.tile_size)
    app.pacman = Pacman(
        pos=start,
        direction=STOP,
        desired_direction=RIGHT,
        speed=game_config.pacman_speed,
    )

    app._update_pacman(0.1)

    assert app.pacman.direction == RIGHT
    assert app.pacman.pos.x > start.x


def test_read_input_updates_desired_direction(monkeypatch, game_config: GameConfig) -> None:
    class FakeKeys:
        def __getitem__(self, key: int) -> bool:
            return key == pygame.K_LEFT

    app = GameApp(game_config)
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: FakeKeys())

    app._read_input()

    assert app.pacman.desired_direction == LEFT


def test_check_collisions_resets_positions_when_lives_remain(game_config: GameConfig) -> None:
    app = GameApp(game_config)
    app.pacman.pos = tile_center(2, 2, game_config.tile_size)
    app.ghosts = [
        Ghost(
            kind="blinky",
            pos=tile_center(2, 2, game_config.tile_size),
            direction=STOP,
            speed=game_config.ghost_speed,
            scatter_target=(1, 1),
        )
    ]
    app.state = GameState(score=0, lives=2, pellets_left=1)
    app._reset_positions = Mock()

    app._check_collisions()

    assert app.state.lives == 1
    assert app.state.game_over is False
    app._reset_positions.assert_called_once_with()


def test_check_collisions_sets_game_over_on_last_life(game_config: GameConfig) -> None:
    app = GameApp(game_config)
    app.pacman.pos = tile_center(2, 2, game_config.tile_size)
    app.ghosts = [
        Ghost(
            kind="blinky",
            pos=tile_center(2, 2, game_config.tile_size),
            direction=STOP,
            speed=game_config.ghost_speed,
            scatter_target=(1, 1),
        )
    ]
    app.state = GameState(score=0, lives=1, pellets_left=1)
    app._reset_positions = Mock()

    app._check_collisions()

    assert app.state.lives == 0
    assert app.state.game_over is True
    app._reset_positions.assert_not_called()


def test_handle_event_supports_pause_restart_and_quit(game_config: GameConfig) -> None:
    app = GameApp(game_config)
    app._restart_level = Mock()

    app._handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
    assert app.state.paused is True

    app._handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))
    app._restart_level.assert_called_once_with()

    app.running = True
    app._handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
    assert app.running is False

    app.running = True
    app._handle_event(pygame.event.Event(pygame.QUIT))
    assert app.running is False


def test_restart_level_resets_state_and_timers(game_config: GameConfig) -> None:
    app = GameApp(game_config)
    app.state = GameState(score=999, lives=1, pellets_left=0, paused=True, game_over=True)
    app.elapsed = 5.0
    app.mouth_timer = 2.0

    app._restart_level()

    assert app.state.score == 0
    assert app.state.lives == 3
    assert app.state.pellets_left == len(app.maze.pellets) + len(app.maze.power_pellets)
    assert app.state.paused is False
    assert app.state.game_over is False
    assert app.elapsed == 0.0
    assert app.mouth_timer == 0.0
