from unittest.mock import Mock

import pytest

from game.app import GameApp
from game.config import GameConfig

pytestmark = pytest.mark.unit


def test_new_app_starts_with_ready_timer(game_config: GameConfig) -> None:
    app = GameApp(game_config)

    assert app.state.ready_timer == pytest.approx(GameApp.READY_DURATION)


def test_update_skips_entity_updates_during_ready(game_config: GameConfig) -> None:
    app = GameApp(game_config)
    app.state.ready_timer = 1.0
    app._update_pacman = Mock()
    app._update_ghosts = Mock()
    app._check_collisions = Mock()

    app._update(0.1)

    assert app.state.ready_timer == pytest.approx(0.9)
    app._update_pacman.assert_not_called()
    app._update_ghosts.assert_not_called()
    app._check_collisions.assert_not_called()


def test_update_runs_entities_after_ready_expires(game_config: GameConfig) -> None:
    app = GameApp(game_config)
    app.state.ready_timer = 0.0
    app._update_pacman = Mock()
    app._update_ghosts = Mock()
    app._check_collisions = Mock()

    app._update(0.1)

    app._update_pacman.assert_called_once_with(0.1)
    app._update_ghosts.assert_called_once_with(0.1)
    app._check_collisions.assert_called_once_with()


def test_ready_timer_clamps_at_zero(game_config: GameConfig) -> None:
    app = GameApp(game_config)
    app.state.ready_timer = 0.05

    app._update(1.0)

    assert app.state.ready_timer == 0.0


def test_reset_positions_restores_ready_timer(game_config: GameConfig) -> None:
    app = GameApp(game_config)
    app.state.ready_timer = 0.0

    app._reset_positions()

    assert app.state.ready_timer == pytest.approx(GameApp.READY_DURATION)
