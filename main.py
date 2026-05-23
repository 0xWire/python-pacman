import argparse

from game.app import GameApp
from game.config import GameConfig
from game.maze import available_mazes

DEFAULT_TILE_SIZE = 28
DEFAULT_FPS = 60
DEFAULT_LIVES = 3


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PacMan with four attacking ghosts")
    parser.add_argument(
        "--tile-size", type=int, default=DEFAULT_TILE_SIZE, help="Tile size in pixels"
    )
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS, help="Target frames per second")
    parser.add_argument(
        "--maze", choices=available_mazes(), default="classic", help="Starting maze layout"
    )
    parser.add_argument("--lives", type=int, default=DEFAULT_LIVES, help="Starting lives")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = GameConfig(
        tile_size=args.tile_size,
        fps=args.fps,
        start_maze=args.maze,
        starting_lives=max(1, args.lives),
    )
    GameApp(config).run()


if __name__ == "__main__":
    main()
