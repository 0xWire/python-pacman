import argparse

from game.app import GameApp
from game.config import GameConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PacMan")
    parser.add_argument("--tile-size", type=int, default=28, help="Tile size in pixels")
    parser.add_argument("--fps", type=int, default=60, help="Target frames per second")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = GameConfig(tile_size=args.tile_size, fps=args.fps)
    GameApp(config).run()


if __name__ == "__main__":
    main()
