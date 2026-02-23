from __future__ import annotations

import pygame

from .config import GameConfig
from .entities import DOWN, LEFT, Pacman, RIGHT, STOP, UP
from .hud import draw_hud
from .maze import MazeMap, load_default_maze
from .movement import can_move, near_tile_center, step, tile_center, world_to_tile


class GameApp:
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.maze: MazeMap = load_default_maze()
        self.score = 0
        self.lives = 3
        self.running = True
        self.font: pygame.font.Font | None = None
        self.pacman = Pacman(
            pos=tile_center(self.maze.pacman_spawn[0], self.maze.pacman_spawn[1], self.config.tile_size),
            direction=STOP,
            desired_direction=STOP,
            speed=self.config.pacman_speed,
        )

    def _read_input(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pacman.desired_direction = LEFT
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pacman.desired_direction = RIGHT
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.pacman.desired_direction = UP
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.pacman.desired_direction = DOWN

    def _update(self, dt: float) -> None:
        if near_tile_center(self.pacman.pos, self.config.tile_size):
            if can_move(self.maze, self.pacman.pos, self.pacman.desired_direction, self.config.tile_size):
                self.pacman.direction = self.pacman.desired_direction

        if can_move(self.maze, self.pacman.pos, self.pacman.direction, self.config.tile_size):
            self.pacman.pos = step(self.pacman.pos, self.pacman.direction, self.pacman.speed, dt)

        col, row = world_to_tile(self.pacman.pos, self.config.tile_size)
        gained = self.maze.eat_pellet(col, row)
        if gained:
            self.score += gained

    def _draw_maze(self, surface: pygame.Surface) -> None:
        for row, row_data in enumerate(self.maze.layout):
            for col, cell in enumerate(row_data):
                x = col * self.config.tile_size
                y = row * self.config.tile_size
                rect = pygame.Rect(x, y, self.config.tile_size, self.config.tile_size)
                if cell == "#":
                    pygame.draw.rect(surface, (8, 88, 255), rect)
                elif (col, row) in self.maze.pellets:
                    pygame.draw.circle(
                        surface,
                        (248, 222, 121),
                        (x + self.config.tile_size // 2, y + self.config.tile_size // 2),
                        max(2, self.config.tile_size // 9),
                    )

    def _draw_pacman(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(
            surface,
            (255, 220, 0),
            (int(self.pacman.pos.x), int(self.pacman.pos.y)),
            max(8, self.config.tile_size // 2 - 2),
        )

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption("PacMan")
        self.font = pygame.font.SysFont("consolas", 24)

        window_size = self.config.window_size(self.maze.width, self.maze.height)
        screen = pygame.display.set_mode(window_size)
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            dt = clock.tick(self.config.fps) / 1000.0
            self._read_input()
            self._update(dt)

            screen.fill((0, 0, 0))
            self._draw_maze(screen)
            self._draw_pacman(screen)
            if self.font is not None:
                draw_hud(screen, self.font, self.maze.height * self.config.tile_size, self.score, self.lives)
            pygame.display.flip()

        pygame.quit()
