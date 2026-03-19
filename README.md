# SWR Data Lab Boundaries

Timestamped geographic boundary data for Germany in the versatiles format.

[![Build and deploy demo](https://github.com/SWRdata/boundaries/actions/workflows/deploy-demo.yaml/badge.svg)](https://github.com/SWRdata/boundaries/actions/workflows/deploy-demo.yaml) [![Deploy pipeline](https://github.com/SWRdata/boundaries/actions/workflows/deploy-pipeline.yaml/badge.svg)](https://github.com/SWRdata/boundaries/actions/workflows/deploy-pipeline.yaml)

## Usage

`https://static.datenhub.net/data/boundaries/[TILESET]_[TIMESTAMP].versatiles?{z}/{x}/{y}`

See [demo](https://static.datenhub.net/apps/boundaries/main/index.html) for code samples.

## Tilesets

| Name               | Description                                         | Source                                                                                                                                                                                    |
| ------------------ | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `admin_boundaries` | Staat, Länder, Kreise, Gemeinden 1:250,000          | [Bundesamt für Kartographie und Geodäsie VG250](https://gdz.bkg.bund.de/index.php/default/digitale-geodaten/verwaltungsgebiete/verwaltungsgebiete-1-250-000-stand-01-01-vg250-01-01.html) |
| `admin_labels`     | Label points for all features in `admin_boundaries` | Derived from `admin_boundaries` using [polylabel](https://github.com/mapbox/polylabel) + manual adjustments                                                                               |

### Fields

| Field   | Description                                                                                                                   |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `id`    | Sequential ID unique to the tileset                                                                                           |
| `ars`   | 12-digit [Amtlicher Regionalschlüssel](https://de.wikipedia.org/wiki/Amtlicher_Gemeindeschl%C3%BCssel#Regionalschl%C3%BCssel) |
| `land`  | Two-digit ID indicating the Bundesland containing the feature or the feature itself)                                          |
| `level` | Administrative hierarchy level; lower levels represent larger feautres                                                        |
| `name`  | Normalised feature name                                                                                                       |

## Contributing

### Tile generation

- Be on Mac or Linux because `tippecanoe` is only available on those platforms
- `cd tasks/make_boundaries && uv sync` to install Python dependencies
- `uv run src/main.py` to run the tile generation pipeline
- `versatiles serve -c versatiles.yaml` to start a local tile server

### Demo page

- `cd demo && npm i && npm run start`
