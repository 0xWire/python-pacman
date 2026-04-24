from __future__ import annotations

from dataclasses import dataclass


CLASSIC_LAYOUT = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.#####.##.#####.######",
    "#....#................#....#",
    "####.#.##.##GGGG##.##.#.####",
    "#....#.##.##....##.##.#....#",
    "####.#.##.########.##.#.####",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#...##................##...#",
    "###.##.##.########.##.##.###",
    "#......##....P.....##......#",
    "#.##########.##.##########.#",
    "#o........................o#",
    "############################",
]

MAZE_LAYOUTS = {
    "classic": CLASSIC_LAYOUT,
    "loops": [
        "############################",
        "#............##............#",
        "#.####.#####.##.#####.####.#",
        "#o####.#####.##.#####.####o#",
        "#..........................#",
        "#.####.##.########.##.####.#",
        "#......##....##....##......#",
        "######.#####.##.#####.######",
        "#............##............#",
        "####.#.##.##GGGG##.##.#.####",
        "#....#.##.##....##.##.#....#",
        "####.#.##.########.##.#.####",
        "#............##............#",
        "#.####.#####.##.#####.####.#",
        "#o..##................##..o#",
        "###.##.##.########.##.##.###",
        "#......##....P.....##......#",
        "#.##########.##.##########.#",
        "#..........................#",
        "############################",
    ],
}

FALLBACK_GHOST_SPAWNS = [(12, 9), (13, 9), (14, 9), (15, 9)]


@dataclass
class MazeMap:
    name: str
    layout: list[str]
    pacman_spawn: tuple[int, int]
    ghost_spawns: list[tuple[int, int]]
    pellets: set[tuple[int, int]]
    power_pellets: set[tuple[int, int]]

    @property
    def width(self) -> int:
        return len(self.layout[0])

    @property
    def height(self) -> int:
        return len(self.layout)

    def is_wall(self, col: int, row: int) -> bool:
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return True
        return self.layout[row][col] == "#"

    def eat_pellet(self, col: int, row: int) -> int:
        key = (col, row)
        if key in self.pellets:
            self.pellets.remove(key)
            return 10
        if key in self.power_pellets:
            self.power_pellets.remove(key)
            return 50
        return 0


def _validate_layout(name: str, layout: list[str]) -> None:
    if not layout:
        raise ValueError(f"Maze '{name}' must contain at least one row")

    width = len(layout[0])
    if width == 0:
        raise ValueError(f"Maze '{name}' cannot have empty rows")

    for row in layout:
        if len(row) != width:
            raise ValueError(f"Maze '{name}' must be rectangular")


def load_maze(name: str) -> MazeMap:
    if name not in MAZE_LAYOUTS:
        raise ValueError(f"Unknown maze '{name}'")

    layout = MAZE_LAYOUTS[name]
    _validate_layout(name, layout)
    pacman_spawn = (14, 16)
    ghost_spawns: list[tuple[int, int]] = []
    pellets: set[tuple[int, int]] = set()
    power_pellets: set[tuple[int, int]] = set()

    for row, row_value in enumerate(layout):
        for col, cell in enumerate(row_value):
            if cell == "P":
                pacman_spawn = (col, row)
            elif cell == "G":
                ghost_spawns.append((col, row))
            elif cell == ".":
                pellets.add((col, row))
            elif cell == "o":
                power_pellets.add((col, row))

    if len(ghost_spawns) < 4:
        for tile in FALLBACK_GHOST_SPAWNS:
            if tile not in ghost_spawns:
                ghost_spawns.append(tile)
            if len(ghost_spawns) == 4:
                break

    return MazeMap(
        name=name,
        layout=layout,
        pacman_spawn=pacman_spawn,
        ghost_spawns=ghost_spawns[:4],
        pellets=pellets,
        power_pellets=power_pellets,
    )


def load_default_maze() -> MazeMap:
    return load_maze("classic")


def available_mazes() -> tuple[str, ...]:
    return tuple(MAZE_LAYOUTS)
