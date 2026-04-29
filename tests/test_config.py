import pytest

from game.config import GameConfig

pytestmark = pytest.mark.unit


def test_window_size_uses_tile_size_and_hud_height(game_config: GameConfig) -> None:
    assert game_config.window_size(5, 7) == (100, 188)
