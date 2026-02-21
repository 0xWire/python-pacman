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


def _fallback_pacman(size: int, open_mouth: bool) -> pygame.Surface:
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = (size // 2, size // 2)
    radius = size // 2 - 1
    pygame.draw.circle(surface, (255, 220, 0), center, radius)
    if open_mouth:
        mouth = [center, (size - 2, size // 4), (size - 2, size - size // 4)]
        pygame.draw.polygon(surface, (0, 0, 0), mouth)
    pygame.draw.circle(surface, (0, 0, 0), (size // 2 + size // 6, size // 3), max(1, size // 14))
    return surface


def _fallback_ghost(size: int, color: tuple[int, int, int]) -> pygame.Surface:
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    body_rect = pygame.Rect(2, size // 3, size - 4, size - size // 3 - 2)
    pygame.draw.rect(surface, color, body_rect)
    pygame.draw.circle(surface, color, (size // 3, size // 3), size // 4)
    pygame.draw.circle(surface, color, (size - size // 3, size // 3), size // 4)

    eye_r = max(2, size // 8)
    pupil_r = max(1, size // 14)
    left_eye = (size // 3, size // 2)
    right_eye = (size - size // 3, size // 2)
    pygame.draw.circle(surface, (255, 255, 255), left_eye, eye_r)
    pygame.draw.circle(surface, (255, 255, 255), right_eye, eye_r)
    pygame.draw.circle(surface, (20, 70, 255), (left_eye[0], left_eye[1] + 1), pupil_r)
    pygame.draw.circle(surface, (20, 70, 255), (right_eye[0], right_eye[1] + 1), pupil_r)
    return surface


def _fit(sprite: pygame.Surface, size: int) -> pygame.Surface:
    return pygame.transform.smoothscale(sprite, (size, size))


def load_sprite_pack(tile_size: int) -> SpritePack:
    desired = max(20, tile_size - 2)

    pacman_open = _load_or_none(ASSET_DIR / "pacman_open.png")
    pacman_closed = _load_or_none(ASSET_DIR / "pacman_closed.png")
    if pacman_open is None:
        pacman_open = _fallback_pacman(desired, open_mouth=True)
    if pacman_closed is None:
        pacman_closed = _fallback_pacman(desired, open_mouth=False)

    ghost_colors = {
        "blinky": (230, 70, 70),
        "pinky": (255, 140, 200),
        "inky": (90, 240, 255),
        "clyde": (255, 170, 70),    }

    ghosts: dict[str, pygame.Surface] = {}
    for name in ["blinky", "pinky", "inky", "clyde"]:
        sprite = _load_or_none(ASSET_DIR / f"ghost_{name}.png")
        if sprite is None:
            sprite = _fallback_ghost(desired, ghost_colors[name])
        ghosts[name] = _fit(sprite, desired)

    return SpritePack(
        pacman_open=_fit(pacman_open, desired),
        pacman_closed=_fit(pacman_closed, desired),
        ghosts=ghosts,
    )
