from __future__ import annotations

from .entities import Ghost, Pacman


def collides_with_ghost(pacman: Pacman, ghost: Ghost, radius: float) -> bool:
    dx = pacman.pos.x - ghost.pos.x
    dy = pacman.pos.y - ghost.pos.y
    return dx * dx + dy * dy <= radius * radius
