from __future__ import annotations

from .entities import Vec2


def tile_center(col: int, row: int, tile_size: int) -> Vec2:
    return Vec2((col + 0.5) * tile_size, (row + 0.5) * tile_size)


def world_to_tile(pos: Vec2, tile_size: int) -> tuple[int, int]:
    return int(pos.x // tile_size), int(pos.y // tile_size)
