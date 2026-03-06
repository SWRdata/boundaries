# Boundaries

Geographic boundary data for Germany in the versatiles format.

[![Build and deploy demo](https://github.com/SWRdata/boundaries/actions/workflows/deploy-demo.yaml/badge.svg)](https://github.com/SWRdata/boundaries/actions/workflows/deploy-demo.yaml) [![Deploy pipeline](https://github.com/SWRdata/boundaries/actions/workflows/deploy-pipeline.yaml/badge.svg)](https://github.com/SWRdata/boundaries/actions/workflows/deploy-pipeline.yaml)

## Schema

### Layers

| Layer            | Description                                | Source                                                                                                                                                                                    |
| ---------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `administrative` | Staat, Länder, Kreise, Gemeinden 1:250,000 | [Bundesamt für Kartographie und Geodäsie VG250](https://gdz.bkg.bund.de/index.php/default/digitale-geodaten/verwaltungsgebiete/verwaltungsgebiete-1-250-000-stand-01-01-vg250-01-01.html) |
| `labels`         |                                            | Derived from `administrative`                                                                                                                                                             |

### Fields

| Field   | Description                                                                                                                   |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `id`    | Sequential ID unique to the tileset                                                                                           |
| `ars`   | 12-digit [Amtlicher Regionalschlüssel](https://de.wikipedia.org/wiki/Amtlicher_Gemeindeschl%C3%BCssel#Regionalschl%C3%BCssel) |
| `land`  | Two-digit ID indicating the Bundesland containing the feature or the feature itself                                           |
| `level` | Administrative hierarchy level; lower levels represent larger feautres                                                        |
| `name`  | Normalised feature name                                                                                                       |

## Contributing

### Tile generation

- Be on Mac or Linux because `tippecanoe` is only available on those platforms
- `cd tasks/make_boundaries && uv sync && uv run src/main.py`

### Demo page

- `cd demo && npm i && npm run start`
