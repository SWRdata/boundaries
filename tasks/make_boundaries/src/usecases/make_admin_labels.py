import datetime
import os
from typing import Dict

import geopandas as gp
import pandas as pd
import shapely.affinity as affinity
import shapely.geometry as geometry
import shapely.ops as ops

from globals import BKG_URL, NAME_SUBS
from usecases.fetch_unless_cached import fetch_unless_cached
from usecases.make_versatiles import make_versatiles

label_subs: Dict[str, geometry.Point] = {}


def get_label_point(x: geometry.Polygon | geometry.MultiPolygon):
    xfact = 0.7
    geom = (
        max(x.geoms, key=lambda x: x.area)
        if isinstance(x, geometry.MultiPolygon)
        else x
    )

    return affinity.scale(
        ops.polylabel(affinity.scale(geom, xfact=xfact, yfact=1), 0.1),
        xfact=1 / xfact,
        yfact=1,
    )


def make_admin_labels(
    cache_dir: str, output_dir: str, date: datetime.date
) -> list[str]:

    # 1. Fetch the BKG data we need
    ds = date.strftime("%Y-%m-%d")

    json_path = os.path.join(cache_dir, f"admin_labels_{ds}.geojson")
    versatiles_path = os.path.join(output_dir, f"admin_labels_{ds}.versatiles")
    tilejson_path = versatiles_path.replace(".versatiles", ".json")

    fp = "vg250_01-01.utm32s.shape.ebenen/vg250_ebenen_0101"

    zip_name = "vg250_01-01.utm32s.shape.ebenen.zip"
    cache_path = f"{cache_dir}/{ds}_{zip_name}"

    fetch_unless_cached(f"{BKG_URL}/{date.year}/{zip_name}", cache_path)

    # 2. Extract + wrangle shapes
    # 2.1 Admin 2
    print("Staat... ", end="")
    country = gp.read_file(f"zip://{cache_path}!{fp}/VG250_STA.shp")
    country_labels = country.loc[country["OBJID"] == "DEBKGVG200000CKM"]
    assert country_labels.shape[0] == 1
    country_labels["admin_level"] = 2
    country_labels["kind"] = "Staat"
    country_labels["geometry"] = country_labels.geometry.apply(lambda x: x.centroid)
    print(f"done ({country_labels.shape[0]} geom)")

    # 2.2 Admin 4
    print("Land... ", end="")
    laender = gp.read_file(f"zip://{cache_path}!{fp}/VG250_LAN.shp")
    laender_labels = laender.loc[laender["GF"] == 4]
    assert laender_labels.shape[0] == 16
    laender_labels["admin_level"] = 4
    laender_labels["kind"] = "Land"
    laender_labels["land"] = laender["SN_L"]
    laender_labels["geometry"] = laender_labels.geometry.apply(get_label_point)
    print(f"done ({laender_labels.shape[0]} geoms)")

    # 2.3 Admin 6
    print("Kreis... ", end="")
    kreise = gp.read_file(f"zip://{cache_path}!{fp}/VG250_KRS.shp")
    kreise_labels = kreise.loc[kreise["GF"] == 4]
    kreise_labels["admin_level"] = 6
    kreise_labels["kind"] = "Kreis"
    kreise_labels["land"] = kreise_labels["SN_L"]
    kreise_labels["geometry"] = kreise_labels.geometry.apply(get_label_point)
    print(f"done ({kreise_labels.shape[0]} geoms)")

    # 2.4 Admin 8
    print("Gemeinde... ", end="")
    gemeinden = gp.read_file(f"zip://{cache_path}!{fp}/VG250_GEM.shp")
    gemeinden_labels = gemeinden.loc[gemeinden["GF"] == 4]
    gemeinden_labels["admin_level"] = 8
    gemeinden_labels["kind"] = "Gemeinde"
    gemeinden_labels["land"] = gemeinden["SN_L"]
    gemeinden_labels["geometry"] = gemeinden_labels.geometry.apply(get_label_point)
    print(f"done ({gemeinden_labels.shape[0]} geoms)")

    # 3. Concat
    res = gp.GeoDataFrame(
        pd.concat([country_labels, laender_labels, kreise_labels, gemeinden_labels])
    )

    res["name"] = res["GEN"]
    res["ars"] = res["ARS"]
    res["id"] = res["OBJID"]

    # 4. Apply manual substitutions
    res["name"] = res["name"].apply(lambda x: NAME_SUBS[x] if x in NAME_SUBS else x)

    label_subs = gp.read_file("./label_substitutions.geojson")
    print(f"Applying {label_subs.shape[0]} manual subsititutions... ", end="")

    label_position_subs = (
        label_subs.to_crs(res.crs or "EPSG:25832")
        .set_index("ars")
        .to_dict(orient="index")
    )

    res["geometry"] = res.apply(
        lambda x: (
            label_position_subs[x["ars"]]["geometry"]
            if x["ars"] in label_position_subs
            else x["geometry"]
        ),
        axis=1,
    )
    print("done")

    res[["id", "ars", "land", "name", "admin_level", "geometry"]].to_crs(
        "wgs84"
    ).reset_index().to_file(json_path)

    print(f"Wrote to {json_path}")

    # 4. Convert to versatiles
    try:
        make_versatiles(
            json_path, versatiles_path, tilejson_path, date, ["--base-zoom=5"]
        )
    except Exception:
        print(f"Failed to build {versatiles_path}")
        return []

    return [versatiles_path]
