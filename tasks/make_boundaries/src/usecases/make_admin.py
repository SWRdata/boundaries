import os
from datetime import date

import geopandas as gp
import pandas as pd

from globals import BKG_URL, NAME_SUBS
from usecases.fetch_unless_cached import fetch_unless_cached
from usecases.make_versatiles import make_versatiles


# This is where we do content-specific processing for each admin layer
# before merging them all into one JSON file which we convert to versatiles
# See: https://wiki.openstreetmap.org/wiki/File:Administrative_Gliederung_Deutschlands_admin_level.png
def make_admin(cache_dir: str, output_dir: str, date: date):

    # 1. Fetch the BKG data we need
    ds = date.strftime("%Y-%m-%d")
    json_path = os.path.join(cache_dir, f"admin_boundaries_{ds}.geojson")
    versatiles_path = os.path.join(output_dir, f"admin_boundaries_{ds}.versatiles")
    tilejson_path = versatiles_path.replace(".versatiles", ".json")

    fp = "vg250_01-01.utm32s.shape.ebenen/vg250_ebenen_0101"

    zip_name = "vg250_01-01.utm32s.shape.ebenen.zip"
    cache_path = f"{cache_dir}/{ds}_{zip_name}"

    fetch_unless_cached(f"{BKG_URL}/{date.year}/{zip_name}", cache_path)

    # 2. Extract + wrangle shapes
    # 2.1 Admin 2
    print("Staat... ", end="")
    country = gp.read_file(f"zip://{cache_path}!{fp}/VG250_STA.shp")
    country["admin_level"] = 2
    country["kind"] = "Staat"
    country_processed = country.loc[country["OBJID"] == "DEBKGVG200000CKM"]
    assert country_processed.shape[0] == 1
    print(f"done ({country_processed.shape[0]} geom)")

    # 2.2  Admin 4
    print("Land... ", end="")
    laender = gp.read_file(f"zip://{cache_path}!{fp}/VG250_LAN.shp")
    laender["admin_level"] = 4
    laender["kind"] = "Land"
    laender["land"] = laender["SN_L"]
    laender_processed = laender.loc[laender["GF"] == 4]
    assert laender_processed.shape[0] == 16
    print(f"done ({laender_processed.shape[0]} geoms)")

    # 2.3 Admin 6
    print("Kreis... ", end="")
    kreise = gp.read_file(f"zip://{cache_path}!{fp}/VG250_KRS.shp")
    kreise["admin_level"] = 6
    kreise["kind"] = "Kreis"
    kreise["land"] = kreise["SN_L"]
    kreise_processed = kreise.loc[kreise["GF"] == 4]
    print(f"done ({kreise_processed.shape[0]} geoms)")

    # 2.4 Admin 8
    print("Gemeinde... ", end="")
    gemeinden = gp.read_file(f"zip://{cache_path}!{fp}/VG250_GEM.shp")
    gemeinden["admin_level"] = 8
    gemeinden["kind"] = "Gemeinde"
    gemeinden["land"] = gemeinden["SN_L"]
    gemeinden_processed = gemeinden.loc[gemeinden["GF"] == 4]
    print(f"done ({gemeinden_processed.shape[0]} geoms)")

    res = gp.GeoDataFrame(
        pd.concat(
            [
                country_processed,
                laender_processed,
                kreise_processed,
                gemeinden_processed,
            ]
        )
    )

    res["name"] = res["GEN"]
    res["ars"] = res["ARS"]
    res["id"] = res["OBJID"]

    res["name"] = res["name"].apply(lambda x: NAME_SUBS[x] if x in NAME_SUBS else x)

    output_cols = ["id", "ars", "land", "name", "admin_level", "geometry"]
    res[output_cols].to_crs("wgs84").to_file(json_path)
    laender_processed.to_crs("wgs84").simplify(0.01).to_file(
        f"{cache_dir}/admin_boundaries_laender_{ds}.geojson"
    )

    print(f"Wrote to {json_path}")

    try:
        make_versatiles(json_path, versatiles_path, tilejson_path, date)
    except Exception:
        print(f"Failed to build {versatiles_path}")
        return

    return [versatiles_path]
