from __future__ import annotations

from .entities import Ghost, Pacman
from .movement import world_distance


def collides_with_ghost(pacman: Pacman, ghost: Ghost, radius: float) -> bool:
    return world_distance(pacman.pos, ghost.pos) <= radius
