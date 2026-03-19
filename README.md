# SWR Data Lab Boundaries

Ready-to-use, timestamped boundary data for Germany in the versatiles format.

[![deploy demo](https://github.com/SWRdata/boundaries/actions/workflows/deploy-demo.yaml/badge.svg)](https://github.com/SWRdata/boundaries/actions/workflows/deploy-demo.yaml) [![deploy pipeline](https://github.com/SWRdata/boundaries/actions/workflows/deploy-pipeline.yaml/badge.svg)](https://github.com/SWRdata/boundaries/actions/workflows/deploy-pipeline.yaml) [![ty](https://github.com/SWRdata/boundaries/actions/workflows/ty.yaml/badge.svg)](https://github.com/SWRdata/boundaries/actions/workflows/ty.yaml)

## Usage

```
https://static.datenhub.net/data/boundaries/[TILESET]_[TIMESTAMP].versatiles?{z}/{x}/{y}
```

See [demo](https://static.datenhub.net/apps/boundaries/main/index.html) for code samples. Note these tilesets require [manual attribution](https://maplibre.org/maplibre-gl-js/docs/API/interfaces/Source/#attribution).

### Tilesets

| Name               | Description                                         | Source                                                                                                                                                | License                                                                                           |
| ------------------ | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `admin_boundaries` | Staat, Länder, Kreise, Gemeinden 1:250,000          | [BKG VG250](https://gdz.bkg.bund.de/index.php/default/digitale-geodaten/verwaltungsgebiete/verwaltungsgebiete-1-250-000-stand-01-01-vg250-01-01.html) | [DNN 2.0](https://sgx.geodatenzentrum.de/web_public/gdz/lizenz/deu/nutzungsbedingungen_vg250.pdf) |
| `admin_labels`     | Label points for all features in `admin_boundaries` | [BKG VG250](https://gdz.bkg.bund.de/index.php/default/digitale-geodaten/verwaltungsgebiete/verwaltungsgebiete-1-250-000-stand-01-01-vg250-01-01.html)                                                                                                                       | [DNN 2.0](https://sgx.geodatenzentrum.de/web_public/gdz/lizenz/deu/nutzungsbedingungen_vg250.pdf) |
### Timestamps

`2025-01-01`, `2024-01-01`

### Fields

| Field   | Description                                                                                                                   |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `id`    | Sequential ID unique to the tileset                                                                                           |
| `ars`   | 12-digit [Amtlicher Regionalschlüssel](https://de.wikipedia.org/wiki/Amtlicher_Gemeindeschl%C3%BCssel#Regionalschl%C3%BCssel) |
| `name`  | Normalised feature name                                                                                                       |
| `land`  | Two-digit ID indicating the Bundesland containing the feature or the feature itself                                           |
| `level` | Administrative hierarchy level; lower levels represent larger features                                                        |

## Contributing

### Tile generation

- Install [`uv`](https://github.com/astral-sh/uv), [`versatiles`](https://github.com/versatiles-org/versatiles-rs) and [`tippecanoe`](https://github.com/felt/tippecanoe) (Mac/Linux only)
- `cd tasks/make_boundaries`
- `uv sync` to install Python dependencies
- `uv run src/main.py` to run the tile generation pipeline
- `versatiles serve -c versatiles.yaml` to start a local tile server

### Demo page

- `cd demo && npm i && npm run start`

## Prior work

- [Polylabel](https://github.com/mapbox/polylabel)
