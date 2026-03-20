from __future__ import annotations

import os
import sys
from pathlib import Path

import pygame
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from game.config import GameConfig
from game.entities import Ghost, Pacman, STOP
from game.maze import MazeMap
from game.movement import tile_center


@pytest.fixture
def game_config() -> GameConfig:
    return GameConfig(
        tile_size=20,
        fps=30,
        hud_height=48,
        pacman_speed=100.0,
        ghost_speed=90.0,
        collision_radius_ratio=0.5,
    )


@pytest.fixture
def tile_size(game_config: GameConfig) -> int:
    return game_config.tile_size


@pytest.fixture
def maze_factory():
    def build_maze(
        layout: list[str],
        pacman_spawn: tuple[int, int] = (2, 2),
        ghost_spawns: list[tuple[int, int]] | None = None,
        pellets: set[tuple[int, int]] | None = None,
        power_pellets: set[tuple[int, int]] | None = None,
    ) -> MazeMap:
        return MazeMap(
            layout=layout,
            pacman_spawn=pacman_spawn,
            ghost_spawns=ghost_spawns or [(1, 1), (3, 1), (1, 3), (3, 3)],
            pellets=pellets or set(),
            power_pellets=power_pellets or set(),
        )

    return build_maze


@pytest.fixture
def sample_maze(maze_factory) -> MazeMap:
    return maze_factory(
        layout=[
            "#####",
            "#...#",
            "#...#",
            "#...#",
            "#####",
        ],
    )


@pytest.fixture
def pacman(tile_size: int) -> Pacman:
    return Pacman(
        pos=tile_center(2, 2, tile_size),
        direction=STOP,
        desired_direction=STOP,
        speed=100.0,
    )


@pytest.fixture
def ghost(tile_size: int) -> Ghost:
    return Ghost(
        kind="blinky",
        pos=tile_center(1, 1, tile_size),
        direction=STOP,
        speed=90.0,
        scatter_target=(3, 1),
    )


@pytest.fixture
def blinky(tile_size: int) -> Ghost:
    return Ghost(
        kind="blinky",
        pos=tile_center(1, 1, tile_size),
        direction=STOP,
        speed=90.0,
        scatter_target=(3, 1),
    )


@pytest.fixture
def pygame_display():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        yield
    finally:
        pygame.display.quit()
        pygame.quit()
