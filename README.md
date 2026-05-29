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
. .venv/bin/activate
pip install -r requirements.txt
python main.py --tile-size 28 --fps 60 --maze classic --lives 3
```

PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

## CLI options
- `--tile-size`: tile size in pixels (default `28`)
- `--fps`: target frame rate (default `60`)
- `--maze`: starting maze (`classic` or `loops`)
- `--lives`: starting lives (default `3`)

## Controls
- `Arrows` or `WASD`: move
- `P`: pause/resume
- `R`: restart level
- `ESC`: quit

## Quality Checks
```bash
make test
make lint
make report
make ci
```

- `make test`: runs the full pytest suite
- `make lint`: runs `flake8` for the project
- `make report`: generates HTML reports in `reports/pytest/` and `reports/flake8/`
- `make ci`: runs linting, tests, and report generation in one command

## Test markers
- `pytest -m unit`: pure unit tests for gameplay logic with no pygame dependencies
- `pytest -m pygame`: tests that require pygame initialization or surfaces
- `pytest -m levels`: tests that exercise multi-level progression and maze cycling

## GitHub Actions
- Workflow file: `.github/workflows/ci.yml`
- Triggers: every `push` and `pull_request`
- Artifacts: uploaded HTML reports from `reports/` — open `reports/pytest/report.html` for the test
  run and `reports/flake8/index.html` for the lint report after downloading the `ci-reports`
  artifact from the Actions run summary
