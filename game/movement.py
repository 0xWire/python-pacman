from __future__ import annotations

import math

from .entities import Vec2
from .maze import MazeMap


def _is_idle_direction(direction: Vec2) -> bool:
    return direction.x == 0 and direction.y == 0


def tile_center(col: int, row: int, tile_size: int) -> Vec2:
    return Vec2((col + 0.5) * tile_size, (row + 0.5) * tile_size)


def world_to_tile(pos: Vec2, tile_size: int) -> tuple[int, int]:
    return int(pos.x // tile_size), int(pos.y // tile_size)


def near_tile_center(pos: Vec2, tile_size: int, tolerance: float = 2.5) -> bool:
    col, row = world_to_tile(pos, tile_size)
    center = tile_center(col, row, tile_size)
    return abs(pos.x - center.x) <= tolerance and abs(pos.y - center.y) <= tolerance


def can_move(maze: MazeMap, pos: Vec2, direction: Vec2, tile_size: int) -> bool:
    if _is_idle_direction(direction):
        return True
    probe = tile_size * 0.52
    target_x = pos.x + direction.x * probe
    target_y = pos.y + direction.y * probe
    col = int(target_x // tile_size)
    row = int(target_y // tile_size)
    return not maze.is_wall(col, row)


def step(pos: Vec2, direction: Vec2, speed: float, dt: float) -> Vec2:
    return Vec2(pos.x + direction.x * speed * dt, pos.y + direction.y * speed * dt)


def squared_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def world_distance(a: Vec2, b: Vec2) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)
