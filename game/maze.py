from __future__ import annotations

from dataclasses import dataclass


DEFAULT_LAYOUT = [
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


@dataclass
class MazeMap:
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


def load_default_maze() -> MazeMap:
    pacman_spawn = (14, 16)
    ghost_spawns: list[tuple[int, int]] = []
    pellets: set[tuple[int, int]] = set()
    power_pellets: set[tuple[int, int]] = set()

    for row, row_value in enumerate(DEFAULT_LAYOUT):
        for col, cell in enumerate(row_value):
            if cell == "P":
                pacman_spawn = (col, row)
            elif cell == "G":
                ghost_spawns.append((col, row))
            elif cell == ".":
                pellets.add((col, row))
            elif cell == "o":
                power_pellets.add((col, row))

    return MazeMap(
        layout=DEFAULT_LAYOUT,
        pacman_spawn=pacman_spawn,
        ghost_spawns=ghost_spawns[:4],
        pellets=pellets,
        power_pellets=power_pellets,
    )
