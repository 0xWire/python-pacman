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


def test_parse_args_defaults_maze_and_lives(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["main.py"])

    args = main.parse_args()

    assert args.maze == "classic"
    assert args.lives == 3


def test_parse_args_reads_maze_and_lives(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["main.py", "--maze", "loops", "--lives", "5"])

    args = main.parse_args()

    assert args.maze == "loops"
    assert args.lives == 5


def test_parse_args_rejects_unknown_maze(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["main.py", "--maze", "swamp"])

    with pytest.raises(SystemExit):
        main.parse_args()


def test_main_passes_maze_and_lives_into_config(monkeypatch) -> None:
    seen = {}

    class DummyApp:
        def __init__(self, config) -> None:
            seen["config"] = config

        def run(self) -> None:
            seen["ran"] = True

    monkeypatch.setattr(sys, "argv", ["main.py", "--maze", "loops", "--lives", "7"])
    monkeypatch.setattr(main, "GameApp", DummyApp)

    main.main()

    assert seen["config"].start_maze == "loops"
    assert seen["config"].starting_lives == 7
    assert seen["ran"] is True


def test_main_clamps_lives_to_minimum_one(monkeypatch) -> None:
    seen = {}

    class DummyApp:
        def __init__(self, config) -> None:
            seen["config"] = config

        def run(self) -> None:
            pass

    monkeypatch.setattr(sys, "argv", ["main.py", "--lives", "0"])
    monkeypatch.setattr(main, "GameApp", DummyApp)

    main.main()

    assert seen["config"].starting_lives == 1
