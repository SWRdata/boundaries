import datetime

import geopandas as gp
import pandas as pd
import shapely.affinity as affinity
import shapely.geometry as geometry
import shapely.ops as ops

from globals import BKG_URL, NAME_SUBS
from usecases.fetch_unless_cached import fetch_unless_cached
from usecases.make_versatiles import make_versatiles


def get_label_point(x: geometry.Polygon):
    xfact = 0.7
    return affinity.scale(
        ops.polylabel(affinity.scale(x, xfact=xfact, yfact=1), 0.1),
        xfact=1 / xfact,
        yfact=1,
    )


def make_admin_labels(cache_dir: str, output_dir: str, date: datetime.date):

    # 1. Fetch the BKG data we need
    ds = date.strftime("%Y-%m-%d")
    json_path = f"{cache_dir}/admin_labels_{ds}.geojson"
    versatiles_path = f"{output_dir}/admin_labels_{ds}.versatiles"
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

    # 3. Concat + write to JSON
    res = gp.GeoDataFrame(
        pd.concat(
            [
                country_labels,
                laender_labels,
            ]
        )
    )

    res["name"] = res["GEN"]
    res["ars"] = res["ARS"]
    res["id"] = res["OBJID"]

    res["name"] = res["name"].apply(lambda x: NAME_SUBS[x] if x in NAME_SUBS else x)

    res[["id", "ars", "land", "name", "admin_level", "geometry"]].to_crs(
        "wgs84"
    ).to_file(json_path)

    print(f"Wrote to {json_path}")

    # 4. Convert to versatiles
    try:
        make_versatiles(json_path, versatiles_path, date, ["--base-zoom=5"])
    except Exception:
        print(f"Failed to build {versatiles_path}")
        return

    return versatiles_path
