import pytest

from game.sprites import load_sprite_pack

pytestmark = [pytest.mark.unit, pytest.mark.pygame]


def test_load_sprite_pack_loads_and_scales_assets(pygame_display) -> None:
    pack = load_sprite_pack(28)

    assert pack.pacman_open.get_size() == (26, 26)
    assert pack.pacman_closed.get_size() == (26, 26)
    assert set(pack.ghosts) == {"blinky", "pinky", "inky", "clyde"}
    assert all(sprite.get_size() == (26, 26) for sprite in pack.ghosts.values())


def test_load_sprite_pack_falls_back_when_assets_are_missing(pygame_display, monkeypatch) -> None:
    monkeypatch.setattr("game.sprites._load_or_none", lambda path: None)

    pack = load_sprite_pack(20)

    assert pack.pacman_open.get_size() == (20, 20)
    assert pack.pacman_closed.get_size() == (20, 20)
    assert all(sprite.get_size() == (20, 20) for sprite in pack.ghosts.values())
