from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    tile_size: int = 28
    fps: int = 60
    hud_height: int = 68
    pacman_speed: float = 125.0
    ghost_speed: float = 108.0
    collision_radius_ratio: float = 0.42

    def window_size(self, maze_width: int, maze_height: int) -> tuple[int, int]:
        return maze_width * self.tile_size, maze_height * self.tile_size + self.hud_height
