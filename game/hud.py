from __future__ import annotations

import pygame

HUD_TEXT_COLOR = (240, 240, 240)
HUD_HINT_COLOR = (155, 155, 155)
HUD_HINT = "Arrows/WASD move   P pause   R restart   ESC quit"


def draw_hud(
    surface: pygame.Surface,
    font: pygame.font.Font,
    top_y: int,
    score: int,
    lives: int,
    level: int,
) -> None:
    text = f"Score: {score}    Lives: {lives}    Level: {level}"
    surface.blit(font.render(text, True, HUD_TEXT_COLOR), (12, top_y + 8))
    surface.blit(font.render(HUD_HINT, True, HUD_HINT_COLOR), (12, top_y + 34))


def draw_center_message(
    surface: pygame.Surface,
    font: pygame.font.Font,
    window_size: tuple[int, int],
    text: str,
) -> None:
    overlay = pygame.Surface(window_size, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))
    label = font.render(text, True, (255, 255, 255))
    rect = label.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    surface.blit(label, rect)
