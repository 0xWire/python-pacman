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
