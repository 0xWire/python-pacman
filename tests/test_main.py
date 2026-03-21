import sys

import pytest

import main

pytestmark = pytest.mark.unit


def test_parse_args_uses_default_values(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["main.py"])

    args = main.parse_args()

    assert args.tile_size == 28
    assert args.fps == 60


def test_parse_args_reads_custom_values(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["main.py", "--tile-size", "32", "--fps", "75"])

    args = main.parse_args()

    assert args.tile_size == 32
    assert args.fps == 75


def test_main_builds_config_and_runs_app(monkeypatch) -> None:
    created = {}

    class DummyApp:
        def __init__(self, config) -> None:
            created["config"] = config

        def run(self) -> None:
            created["ran"] = True

    monkeypatch.setattr(sys, "argv", ["main.py", "--tile-size", "24", "--fps", "90"])
    monkeypatch.setattr(main, "GameApp", DummyApp)

    main.main()

    assert created["config"].tile_size == 24
    assert created["config"].fps == 90
    assert created["ran"] is True
