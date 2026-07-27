# SWRData/Boundaries

Ready-to-use, timestamped boundary data for Germany.

[![deploy demo](https://github.com/SWRdata/boundaries/actions/workflows/deploy-demo.yaml/badge.svg)](https://github.com/SWRdata/boundaries/actions/workflows/deploy-demo.yaml) [![deploy pipeline](https://github.com/SWRdata/boundaries/actions/workflows/deploy-pipeline.yaml/badge.svg)](https://github.com/SWRdata/boundaries/actions/workflows/deploy-pipeline.yaml) [![ty](https://github.com/SWRdata/boundaries/actions/workflows/ty.yaml/badge.svg)](https://github.com/SWRdata/boundaries/actions/workflows/ty.yaml)

## Usage

The latest `admin_boundaries` tileset is available here:

<!-- BEGIN LATEST_URL -->
```
https://static.datenhub.net/data/boundaries/admin_boundaries_2025-01-01.versatiles?{z}/{x}/{y}
```
<!-- END LATEST_URL -->

See [demo](https://static.datenhub.net/apps/boundaries/main/index.html) for code samples. Note these tilesets may require [manual attribution](https://maplibre.org/maplibre-gl-js/docs/API/interfaces/Source/#attribution).

### Tilesets

| Name               | Description                                         | Source                                                                                                                                                | License                                                                                           |
| ------------------ | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `admin_boundaries` | Staat, Länder, Kreise, Gemeinden 1:250,000          | [BKG VG250](https://gdz.bkg.bund.de/index.php/default/digitale-geodaten/verwaltungsgebiete/verwaltungsgebiete-1-250-000-stand-01-01-vg250-01-01.html) | [DNN 2.0](https://sgx.geodatenzentrum.de/web_public/gdz/lizenz/deu/nutzungsbedingungen_vg250.pdf) |
| `admin_labels`     | Label points for all features in `admin_boundaries` | [BKG VG250](https://gdz.bkg.bund.de/index.php/default/digitale-geodaten/verwaltungsgebiete/verwaltungsgebiete-1-250-000-stand-01-01-vg250-01-01.html) | [DNN 2.0](https://sgx.geodatenzentrum.de/web_public/gdz/lizenz/deu/nutzungsbedingungen_vg250.pdf) |

### Timestamps

<!-- BEGIN TIMESTAMPS -->
`2024-01-01`, `2025-01-01`
<!-- END TIMESTAMPS -->

### Fields

| Field   | Description                                                                                                                                                                                    |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`    | Sequential ID unique to the tileset                                                                                                                                                            |
| `ars`   | 12-digit [Amtlicher Regionalschlüssel](https://de.wikipedia.org/wiki/Amtlicher_Gemeindeschl%C3%BCssel#Regionalschl%C3%BCssel)                                                                  |
| `name`  | Normalised feature name                                                                                                                                                                        |
| `land`  | Two-digit ID indicating the Bundesland containing the feature or the feature itself                                                                                                            |
| `level` | Administrative hierarchy level; lower levels represent larger features (follows [OSM levels](https://wiki.openstreetmap.org/wiki/File:Administrative_Gliederung_Deutschlands_admin_level.png)) |


## Prior work

- [Polylabel](https://github.com/mapbox/polylabel)
