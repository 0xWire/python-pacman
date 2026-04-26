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

    def ghost_speed_for_level(self, level: int) -> float:
        return self.ghost_speed + min(18.0, (level - 1) * 4.0)

    def pacman_speed_for_level(self, level: int) -> float:
        return self.pacman_speed + min(10.0, (level - 1) * 2.0)

    def frightened_duration_for_level(self, level: int) -> float:
        return max(3.0, 6.0 - (level - 1) * 0.35)
