import pytest

from game.entities import DOWN, Ghost, LEFT, Pacman, RIGHT, STOP, UP
from game.ghost_ai import _target_tile, choose_ghost_direction
from game.movement import tile_center

pytestmark = pytest.mark.unit


def make_ghost(
    kind: str,
    col: int,
    row: int,
    tile_size: int,
    scatter_target: tuple[int, int],
    direction=LEFT,
) -> Ghost:
    return Ghost(
        kind=kind,
        pos=tile_center(col, row, tile_size),
        direction=direction,
        speed=90.0,
        spawn_tile=(col, row),
        scatter_target=scatter_target,
    )


@pytest.mark.parametrize("direction", [RIGHT, LEFT, UP, DOWN])
def test_target_tile_uses_scatter_target_when_scatter_mode_is_enabled(
    direction,
    tile_size: int,
) -> None:
    pacman = Pacman(
        pos=tile_center(3, 3, tile_size),
        direction=direction,
        desired_direction=direction,
        speed=100.0,
    )
    ghost = make_ghost("pinky", 1, 1, tile_size, scatter_target=(9, 2))
    blinky = make_ghost("blinky", 2, 1, tile_size, scatter_target=(8, 1))

    assert _target_tile(ghost, pacman, blinky, tile_size, scatter_mode=True) == (9, 2)


def test_blinky_targets_current_pacman_tile(tile_size: int) -> None:
    pacman = Pacman(
        pos=tile_center(4, 2, tile_size),
        direction=RIGHT,
        desired_direction=RIGHT,
        speed=100.0,
    )
    blinky = make_ghost("blinky", 1, 1, tile_size, scatter_target=(8, 1))

    assert _target_tile(blinky, pacman, blinky, tile_size, scatter_mode=False) == (4, 2)


@pytest.mark.parametrize(
    ("direction", "expected"),
    [
        (RIGHT, (7, 4)),
        (LEFT, (-1, 4)),
        (UP, (3, 0)),
        (DOWN, (3, 8)),
    ],
)
def test_pinky_targets_four_tiles_ahead(direction, expected, tile_size: int) -> None:
    pacman = Pacman(
        pos=tile_center(3, 4, tile_size),
        direction=direction,
        desired_direction=direction,
        speed=100.0,
    )
    ghost = make_ghost("pinky", 1, 1, tile_size, scatter_target=(1, 1))
    blinky = make_ghost("blinky", 2, 1, tile_size, scatter_target=(8, 1))

    assert _target_tile(ghost, pacman, blinky, tile_size, scatter_mode=False) == expected


def test_inky_uses_blinky_position_to_project_target(tile_size: int) -> None:
    pacman = Pacman(
        pos=tile_center(5, 4, tile_size),
        direction=UP,
        desired_direction=UP,
        speed=100.0,
    )
    inky = make_ghost("inky", 3, 3, tile_size, scatter_target=(8, 8))
    blinky = make_ghost("blinky", 1, 1, tile_size, scatter_target=(8, 1))

    assert _target_tile(inky, pacman, blinky, tile_size, scatter_mode=False) == (9, 3)


@pytest.mark.parametrize(
    ("ghost_tile", "expected"),
    [
        ((1, 1), (8, 8)),
        ((6, 6), (1, 8)),
    ],
)
def test_clyde_switches_between_chase_and_scatter(
    ghost_tile: tuple[int, int],
    expected: tuple[int, int],
    tile_size: int,
) -> None:
    pacman = Pacman(
        pos=tile_center(8, 8, tile_size),
        direction=LEFT,
        desired_direction=LEFT,
        speed=100.0,
    )
    clyde = make_ghost("clyde", ghost_tile[0], ghost_tile[1], tile_size, scatter_target=(1, 8))
    blinky = make_ghost("blinky", 2, 1, tile_size, scatter_target=(8, 1))

    assert _target_tile(clyde, pacman, blinky, tile_size, scatter_mode=False) == expected


def test_choose_ghost_direction_picks_shortest_path_to_target(sample_maze, tile_size: int) -> None:
    pacman = Pacman(
        pos=tile_center(3, 2, tile_size),
        direction=RIGHT,
        desired_direction=RIGHT,
        speed=100.0,
    )
    ghost = make_ghost("blinky", 2, 2, tile_size, scatter_target=(4, 1), direction=STOP)
    blinky = make_ghost("blinky", 1, 1, tile_size, scatter_target=(4, 1))

    result = choose_ghost_direction(ghost, pacman, blinky, sample_maze, tile_size, False, False)
    assert result == RIGHT


def test_choose_ghost_direction_skips_reverse_when_other_moves_exist(
    sample_maze,
    tile_size: int,
) -> None:
    pacman = Pacman(
        pos=tile_center(1, 2, tile_size),
        direction=LEFT,
        desired_direction=LEFT,
        speed=100.0,
    )
    ghost = make_ghost("blinky", 2, 2, tile_size, scatter_target=(4, 1), direction=RIGHT)
    blinky = make_ghost("blinky", 1, 1, tile_size, scatter_target=(4, 1))

    assert choose_ghost_direction(ghost, pacman, blinky, sample_maze, tile_size, False, False) == UP


def test_choose_ghost_direction_falls_back_to_reverse_when_it_is_the_only_move(
    maze_factory,
    tile_size: int,
) -> None:
    maze = maze_factory(
        layout=[
            "#####",
            "#####",
            "##..#",
            "#####",
            "#####",
        ],
        pacman_spawn=(3, 2),
        ghost_spawns=[(3, 2)],
    )
    pacman = Pacman(
        pos=tile_center(1, 1, tile_size),
        direction=LEFT,
        desired_direction=LEFT,
        speed=100.0,
    )
    ghost = make_ghost("blinky", 3, 2, tile_size, scatter_target=(4, 1), direction=RIGHT)
    blinky = make_ghost("blinky", 1, 1, tile_size, scatter_target=(4, 1))

    assert choose_ghost_direction(ghost, pacman, blinky, maze, tile_size, False, False) == LEFT


def test_choose_ghost_direction_returns_stop_when_no_moves_are_available(
    maze_factory,
    tile_size: int,
) -> None:
    maze = maze_factory(
        layout=[
            "#####",
            "#####",
            "##.##",
            "#####",
            "#####",
        ],
        pacman_spawn=(2, 2),
        ghost_spawns=[(2, 2)],
    )
    pacman = Pacman(
        pos=tile_center(1, 1, tile_size),
        direction=LEFT,
        desired_direction=LEFT,
        speed=100.0,
    )
    ghost = make_ghost("blinky", 2, 2, tile_size, scatter_target=(4, 1), direction=RIGHT)
    blinky = make_ghost("blinky", 1, 1, tile_size, scatter_target=(4, 1))

    assert choose_ghost_direction(ghost, pacman, blinky, maze, tile_size, False, False) == STOP
