import datetime

import geopandas as gp
import pandas as pd
import shapely.affinity as affinity
import shapely.ops as ops

from globals import BKG_URL, NAME_SUBS
from usecases.fetch_unless_cached import fetch_unless_cached
from usecases.make_versatiles import make_versatiles


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
    # 2.1 Admin 4
    print("Land... ", end="")
    xfact = 1.5
    laender = gp.read_file(f"zip://{cache_path}!{fp}/VG250_LAN.shp")
    laender["admin_level"] = 4
    laender["kind"] = "Land"
    laender["land"] = laender["SN_L"]
    laender_labels = laender.loc[laender["GF"] == 4]
    assert laender_labels.shape[0] == 16

    laender_labels["geometry"] = laender_labels.geometry.apply(
        lambda x: affinity.scale(
            ops.polylabel(affinity.scale(x, xfact, yfact=1), 0.1),
            xfact=1 / xfact,
            yfact=1,
        )
    )
    print(f"done ({laender_labels.shape[0]} geoms)")

    # 3. Concat + write to JSON
    res = gp.GeoDataFrame(
        pd.concat(
            [
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
        make_versatiles(json_path, versatiles_path, date)
    except Exception:
        print(f"Failed to build {versatiles_path}")
        return
