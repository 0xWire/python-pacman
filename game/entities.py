from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


GhostKind = Literal["blinky", "pinky", "inky", "clyde"]


@dataclass
class Vec2:
    x: float
    y: float

    def scaled(self, factor: float) -> "Vec2":
        return Vec2(self.x * factor, self.y * factor)

    def is_zero(self) -> bool:
        return self.x == 0.0 and self.y == 0.0


UP = Vec2(0.0, -1.0)
DOWN = Vec2(0.0, 1.0)
LEFT = Vec2(-1.0, 0.0)
RIGHT = Vec2(1.0, 0.0)
STOP = Vec2(0.0, 0.0)
DIRECTION_ORDER = [UP, LEFT, DOWN, RIGHT]


@dataclass
class Pacman:
    pos: Vec2
    direction: Vec2
    desired_direction: Vec2
    speed: float


@dataclass
class Ghost:
    kind: GhostKind
    pos: Vec2
    direction: Vec2
    speed: float
    scatter_target: tuple[int, int]


@dataclass
class GameState:
    score: int
    lives: int
    pellets_left: int
    level: int = 1
    paused: bool = False
    game_over: bool = False
    level_complete: bool = False
