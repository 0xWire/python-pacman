from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pygame


ASSET_DIR = Path(__file__).resolve().parent.parent / "assets" / "sprites"


@dataclass
class SpritePack:
    pacman_open: pygame.Surface
    pacman_closed: pygame.Surface
    ghosts: dict[str, pygame.Surface]


def _load_or_none(path: Path) -> pygame.Surface | None:
    if path.exists():
        return pygame.image.load(path.as_posix()).convert_alpha()
    return None


def load_sprite_pack(tile_size: int) -> SpritePack:
    pacman_open = _load_or_none(ASSET_DIR / "pacman_open.png")
    pacman_closed = _load_or_none(ASSET_DIR / "pacman_closed.png")
    if pacman_open is None or pacman_closed is None:
        raise FileNotFoundError("pacman sprite assets are missing")
    return SpritePack(
        pacman_open=pacman_open,
        pacman_closed=pacman_closed,
        ghosts={},
    )
