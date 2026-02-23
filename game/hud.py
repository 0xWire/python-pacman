from __future__ import annotations

import pygame


def draw_hud(
    surface: pygame.Surface,
    font: pygame.font.Font,
    top_y: int,
    score: int,
    lives: int,
) -> None:
    text = f"Score: {score}    Lives: {lives}"
    surface.blit(font.render(text, True, (240, 240, 240)), (12, top_y + 10))
