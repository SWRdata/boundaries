# Contributing

- Install [`uv`](https://github.com/astral-sh/uv), [`versatiles`](https://github.com/versatiles-org/versatiles-rs) and [`tippecanoe`](https://github.com/felt/tippecanoe) (Mac/Linux only)
- Clone this repository
- `uv sync` to install Python dependencies

## Data pipeline

- `cd tasks/make_boundaries`
- `uv run src/main.py` to run the tile generation pipeline
- `versatiles serve -c versatiles.yaml` to start a local tile server

## Demo

- `cd demo && npm i && npm run start`
