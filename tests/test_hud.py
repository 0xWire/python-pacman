from unittest.mock import Mock, call

import pygame
import pytest

from game.hud import HUD_HINT, draw_center_message, draw_hud

pytestmark = [pytest.mark.unit, pytest.mark.pygame]


def test_draw_hud_renders_score_and_hint_text() -> None:
    surface = Mock()
    font = Mock()
    score_label = Mock()
    hint_label = Mock()
    font.render.side_effect = [score_label, hint_label]

    draw_hud(surface, font, top_y=100, score=420, lives=2, level=1)

    assert font.render.call_args_list == [
        call("Score: 420    Lives: 2    Level: 1", True, (240, 240, 240)),
        call(HUD_HINT, True, (155, 155, 155)),
    ]
    assert surface.blit.call_args_list == [
        call(score_label, (12, 108)),
        call(hint_label, (12, 134)),
    ]


def test_draw_center_message_draws_overlay_and_centered_label(pygame_display) -> None:
    surface = Mock()
    font = Mock()
    label = Mock()
    rect = Mock()
    label.get_rect.return_value = rect
    font.render.return_value = label

    draw_center_message(surface, font, (200, 120), "PAUSED")

    assert font.render.call_args == call("PAUSED", True, (255, 255, 255))
    label.get_rect.assert_called_once_with(center=(100, 60))
    assert surface.blit.call_args_list[1] == call(label, rect)
    assert isinstance(surface.blit.call_args_list[0].args[0], pygame.Surface)
