import argparse

from game.app import GameApp
from game.config import GameConfig

DEFAULT_TILE_SIZE = 28
DEFAULT_FPS = 60


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PacMan with four attacking ghosts")
    parser.add_argument(
        "--tile-size",
        type=int,
        default=DEFAULT_TILE_SIZE,
        help="Tile size in pixels",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=DEFAULT_FPS,
        help="Target frames per second",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = GameConfig(tile_size=args.tile_size, fps=args.fps)
    GameApp(config).run()


if __name__ == "__main__":
    main()
