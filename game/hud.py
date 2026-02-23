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
    hint = "Arrows/WASD move   P pause   R restart   ESC quit"
    surface.blit(font.render(text, True, (240, 240, 240)), (12, top_y + 8))
    surface.blit(font.render(hint, True, (155, 155, 155)), (12, top_y + 34))
