from __future__ import annotations

from .entities import DIRECTION_ORDER, Ghost, Pacman, STOP, Vec2
from .maze import MazeMap
from .movement import can_move, squared_distance, world_to_tile


def _reverse(direction: Vec2) -> Vec2:
    return Vec2(-direction.x, -direction.y)


def _is_reverse(candidate: Vec2, current: Vec2) -> bool:
    return candidate.x == -current.x and candidate.y == -current.y


def _ahead_tile(pacman: Pacman, tile_size: int, steps: int) -> tuple[int, int]:
    col, row = world_to_tile(pacman.pos, tile_size)
    return col + int(pacman.direction.x) * steps, row + int(pacman.direction.y) * steps


def _target_tile(
    ghost: Ghost,
    pacman: Pacman,
    blinky: Ghost,
    tile_size: int,
    scatter_mode: bool,
) -> tuple[int, int]:
    pacman_tile = world_to_tile(pacman.pos, tile_size)

    if scatter_mode:
        return ghost.scatter_target

    if ghost.kind == "blinky":
        return pacman_tile

    if ghost.kind == "pinky":
        return _ahead_tile(pacman, tile_size, steps=4)

    if ghost.kind == "inky":
        ahead = _ahead_tile(pacman, tile_size, steps=2)
        blinky_tile = world_to_tile(blinky.pos, tile_size)
        vector_x = ahead[0] - blinky_tile[0]
        vector_y = ahead[1] - blinky_tile[1]
        return ahead[0] + vector_x, ahead[1] + vector_y

    # Clyde: chase when far, retreat to corner when close.
    ghost_tile = world_to_tile(ghost.pos, tile_size)
    if squared_distance(ghost_tile, pacman_tile) > 64:
        return pacman_tile
    return ghost.scatter_target


def choose_ghost_direction(
    ghost: Ghost,
    pacman: Pacman,
    blinky: Ghost,
    maze: MazeMap,
    tile_size: int,
    scatter_mode: bool,
    frightened: bool,
) -> Vec2:
    valid: list[Vec2] = []
    for direction in DIRECTION_ORDER:
        if ghost.direction != STOP and _is_reverse(direction, ghost.direction):
            continue
        if can_move(maze, ghost.pos, direction, tile_size):
            valid.append(direction)

    if not valid:
        reverse = _reverse(ghost.direction)
        if can_move(maze, ghost.pos, reverse, tile_size):
            return reverse
        return STOP

    target = _target_tile(ghost, pacman, blinky, tile_size, scatter_mode)

    def score(direction: Vec2) -> int:
        current_col, current_row = world_to_tile(ghost.pos, tile_size)
        next_col = current_col + int(direction.x)
        next_row = current_row + int(direction.y)
        return squared_distance((next_col, next_row), target)

    if frightened:
        return max(valid, key=score)
    return min(valid, key=score)
