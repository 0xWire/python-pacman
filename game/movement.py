from __future__ import annotations

from .entities import Vec2
from .maze import MazeMap


def tile_center(col: int, row: int, tile_size: int) -> Vec2:
    return Vec2((col + 0.5) * tile_size, (row + 0.5) * tile_size)


def world_to_tile(pos: Vec2, tile_size: int) -> tuple[int, int]:
    return int(pos.x // tile_size), int(pos.y // tile_size)


def near_tile_center(pos: Vec2, tile_size: int, tolerance: float = 2.5) -> bool:
    col, row = world_to_tile(pos, tile_size)
    center = tile_center(col, row, tile_size)
    return abs(pos.x - center.x) <= tolerance and abs(pos.y - center.y) <= tolerance


def can_move(maze: MazeMap, pos: Vec2, direction: Vec2, tile_size: int) -> bool:
    if direction.x == 0 and direction.y == 0:
        return True
    probe = tile_size * 0.52
    target_x = pos.x + direction.x * probe
    target_y = pos.y + direction.y * probe
    col = int(target_x // tile_size)
    row = int(target_y // tile_size)
    return not maze.is_wall(col, row)
