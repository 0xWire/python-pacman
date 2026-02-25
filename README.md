# PacMan Python

PacMan on Python + pygame. Branch `dev` is prepared for PR into `main`.

## Features
- Maze with pellets and power pellets
- PacMan movement (arrows / WASD)
- 4 ghosts with attacking behavior (Blinky, Pinky, Inky, Clyde)
- Score, lives, pause, game over, level complete
- PacMan and ghost sprite icons loaded from `assets/sprites`

## Run
```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
python main.py --tile-size 28 --fps 60
```

## CLI options
- `--tile-size`: tile size in pixels (default `28`)
- `--fps`: target frame rate (default `60`)

## Controls
- `Arrows` or `WASD`: move
- `P`: pause/resume
- `R`: restart level
- `ESC`: quit
