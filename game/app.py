from __future__ import annotations

import itertools

import pygame

from .collision import collides_with_ghost
from .config import GameConfig
from .entities import DOWN, Ghost, GameState, LEFT, Pacman, RIGHT, STOP, UP, Vec2
from .ghost_ai import choose_ghost_direction
from .hud import draw_center_message, draw_hud
from .maze import MazeMap, available_mazes, load_maze
from .movement import can_move, near_tile_center, snap_to_tile_center, step, tile_center, world_to_tile, wrap_position
from .sprites import SpritePack, load_sprite_pack


class GameApp:
    FRIGHTENED_DURATION = 6.0
    FRIGHTENED_GHOST_SPEED_RATIO = 0.75
    READY_DURATION = 1.5

    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.maze_names = available_mazes()
        self.maze_index = 0
        self.maze = load_maze(self.maze_names[self.maze_index])
        self.state = GameState(score=0, lives=3, pellets_left=len(self.maze.pellets) + len(self.maze.power_pellets))

        self.pacman, self.ghosts = self._spawn_entities()
        self.state.ready_timer = self.READY_DURATION
        self.elapsed = 0.0
        self.mouth_timer = 0.0

        self.running = True
        self.font: pygame.font.Font | None = None
        self.sprites: SpritePack | None = None

    def _spawn_entities(self) -> tuple[Pacman, list[Ghost]]:
        pacman_tile = self.maze.pacman_spawn
        pacman = Pacman(
            pos=tile_center(pacman_tile[0], pacman_tile[1], self.config.tile_size),
            direction=STOP,
            desired_direction=STOP,
            speed=self.config.pacman_speed,
        )

        ghost_kinds = ["blinky", "pinky", "inky", "clyde"]
        scatter_targets = {
            "blinky": (self.maze.width - 2, 1),
            "pinky": (1, 1),
            "inky": (self.maze.width - 2, self.maze.height - 2),
            "clyde": (1, self.maze.height - 2),
        }

        ghosts: list[Ghost] = []
        spawn_cycle = itertools.cycle(self.maze.ghost_spawns)
        for kind in ghost_kinds:
            col, row = next(spawn_cycle)
            ghosts.append(
                Ghost(
                    kind=kind,
                    pos=tile_center(col, row, self.config.tile_size),
                    direction=LEFT if kind in {"blinky", "inky"} else RIGHT,
                    speed=self.config.ghost_speed,
                    spawn_tile=(col, row),
                    scatter_target=scatter_targets[kind],
                )
            )

        return pacman, ghosts

    def _reset_positions(self) -> None:
        pacman, ghosts = self._spawn_entities()
        self.pacman = pacman
        self.ghosts = ghosts
        self.state.ready_timer = self.READY_DURATION

    def _restart_level(self) -> None:
        self.maze_index = 0
        self.maze = load_maze(self.maze_names[self.maze_index])
        self.state = GameState(score=0, lives=3, pellets_left=len(self.maze.pellets) + len(self.maze.power_pellets))
        self._reset_positions()
        self.elapsed = 0.0
        self.mouth_timer = 0.0

    def _advance_level(self) -> None:
        self.maze_index = (self.maze_index + 1) % len(self.maze_names)
        self.maze = load_maze(self.maze_names[self.maze_index])
        self.state.level += 1
        self.state.level_complete = False
        self.state.pellets_left = len(self.maze.pellets) + len(self.maze.power_pellets)
        self._reset_positions()
        self.elapsed = 0.0
        self.mouth_timer = 0.0

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

    def _update_pacman(self, dt: float) -> None:
        if near_tile_center(self.pacman.pos, self.config.tile_size):
            self.pacman.pos = snap_to_tile_center(self.pacman.pos, self.config.tile_size)
            if can_move(self.maze, self.pacman.pos, self.pacman.desired_direction, self.config.tile_size):
                self.pacman.direction = self.pacman.desired_direction

        if can_move(self.maze, self.pacman.pos, self.pacman.direction, self.config.tile_size):
            self.pacman.pos = step(self.pacman.pos, self.pacman.direction, self.pacman.speed, dt)
            self.pacman.pos = wrap_position(self.maze, self.pacman.pos, self.config.tile_size)

        col, row = world_to_tile(self.pacman.pos, self.config.tile_size)
        ate_power_pellet = (col, row) in self.maze.power_pellets
        gained = self.maze.eat_pellet(col, row)
        if gained:
            self.state.score += gained
            self.state.pellets_left -= 1
            if ate_power_pellet:
                self.state.frightened_timer = self.FRIGHTENED_DURATION
                self.state.frightened_combo = 0
            if self.state.pellets_left <= 0:
                self.state.level_complete = True
                self._advance_level()

    def _update_ghosts(self, dt: float) -> None:
        scatter_mode = int(self.elapsed / 8.0) % 2 == 1
        frightened = self.state.frightened_timer > 0.0
        blinky = self.ghosts[0]

        for ghost in self.ghosts:
            ghost.speed = self.config.ghost_speed * (self.FRIGHTENED_GHOST_SPEED_RATIO if frightened else 1.0)
            if near_tile_center(ghost.pos, self.config.tile_size):
                ghost.pos = snap_to_tile_center(ghost.pos, self.config.tile_size)
                ghost.direction = choose_ghost_direction(
                    ghost=ghost,
                    pacman=self.pacman,
                    blinky=blinky,
                    maze=self.maze,
                    tile_size=self.config.tile_size,
                    scatter_mode=scatter_mode,
                    frightened=frightened,
                )
            if can_move(self.maze, ghost.pos, ghost.direction, self.config.tile_size):
                ghost.pos = step(ghost.pos, ghost.direction, ghost.speed, dt)
                ghost.pos = wrap_position(self.maze, ghost.pos, self.config.tile_size)

    def _check_collisions(self) -> None:
        radius = self.config.tile_size * self.config.collision_radius_ratio
        for ghost in self.ghosts:
            if collides_with_ghost(self.pacman, ghost, radius):
                if self.state.frightened_timer > 0.0:
                    self.state.score += 200 * (2 ** self.state.frightened_combo)
                    self.state.frightened_combo += 1
                    ghost.pos = tile_center(ghost.spawn_tile[0], ghost.spawn_tile[1], self.config.tile_size)
                    ghost.direction = STOP
                    continue
                self.state.lives -= 1
                if self.state.lives <= 0:
                    self.state.game_over = True
                else:
                    self._reset_positions()
                return

    def _update(self, dt: float) -> None:
        self.elapsed += dt
        self.mouth_timer += dt

        if self.state.ready_timer > 0.0:
            self.state.ready_timer = max(0.0, self.state.ready_timer - dt)
            return

        self.state.frightened_timer = max(0.0, self.state.frightened_timer - dt)
        if self.state.frightened_timer == 0.0:
            self.state.frightened_combo = 0

        self._update_pacman(dt)
        self._update_ghosts(dt)
        self._check_collisions()

    def _draw_maze(self, surface: pygame.Surface) -> None:
        wall_color = (8, 88, 255)
        pellet_color = (248, 222, 121)

        for row, row_data in enumerate(self.maze.layout):
            for col, cell in enumerate(row_data):
                x = col * self.config.tile_size
                y = row * self.config.tile_size
                rect = pygame.Rect(x, y, self.config.tile_size, self.config.tile_size)

                if cell == "#":
                    pygame.draw.rect(surface, wall_color, rect)
                elif (col, row) in self.maze.pellets:
                    pygame.draw.circle(
                        surface,
                        pellet_color,
                        (x + self.config.tile_size // 2, y + self.config.tile_size // 2),
                        max(2, self.config.tile_size // 9),
                    )
                elif (col, row) in self.maze.power_pellets:
                    pygame.draw.circle(
                        surface,
                        pellet_color,
                        (x + self.config.tile_size // 2, y + self.config.tile_size // 2),
                        max(4, self.config.tile_size // 4),
                    )

    def _pacman_angle(self) -> float:
        direction = self.pacman.direction
        if direction == RIGHT:
            return 0.0
        if direction == LEFT:
            return 180.0
        if direction == UP:
            return 90.0
        if direction == DOWN:
            return -90.0
        return 0.0

    def _draw_pacman(self, surface: pygame.Surface) -> None:
        if self.sprites is None:
            return

        frame = self.sprites.pacman_open if int(self.mouth_timer * 12) % 2 == 0 else self.sprites.pacman_closed
        rotated = pygame.transform.rotate(frame, self._pacman_angle())
        rect = rotated.get_rect(center=(int(self.pacman.pos.x), int(self.pacman.pos.y)))
        surface.blit(rotated, rect)

    def _draw_ghosts(self, surface: pygame.Surface) -> None:
        if self.sprites is None:
            return

        for ghost in self.ghosts:
            sprite = self.sprites.ghosts[ghost.kind]
            rect = sprite.get_rect(center=(int(ghost.pos.x), int(ghost.pos.y)))
            surface.blit(sprite, rect)

    def _handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.state.paused = not self.state.paused
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self._restart_level()

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption("PacMan")

        self.font = pygame.font.SysFont("consolas", 24)

        window_size = self.config.window_size(self.maze.width, self.maze.height)
        screen = pygame.display.set_mode(window_size)
        self.sprites = load_sprite_pack(self.config.tile_size)
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                self._handle_event(event)

            dt = clock.tick(self.config.fps) / 1000.0
            self._read_input()
            if not self.state.paused and not self.state.game_over and not self.state.level_complete:
                self._update(dt)

            screen.fill((0, 0, 0))
            self._draw_maze(screen)
            self._draw_pacman(screen)
            self._draw_ghosts(screen)

            if self.font is not None:
                draw_hud(
                    surface=screen,
                    font=self.font,
                    top_y=self.maze.height * self.config.tile_size,
                    score=self.state.score,
                    lives=self.state.lives,
                    level=self.state.level,
                )
                if self.state.paused:
                    draw_center_message(screen, self.font, window_size, "PAUSED")
                elif self.state.game_over:
                    draw_center_message(screen, self.font, window_size, "GAME OVER - PRESS R")
                elif self.state.ready_timer > 0.0:
                    draw_center_message(screen, self.font, window_size, "READY")
                elif self.state.level_complete:
                    draw_center_message(screen, self.font, window_size, "LEVEL COMPLETE - PRESS R")

            pygame.display.flip()

        pygame.quit()
