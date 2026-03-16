import os
from datetime import date

import geopandas as gp
import pandas as pd
import requests

from globals import BKG_URL
from usecases.make_versatiles import make_versatiles

name_subs = {
    "Freiburg im Breisgau": "Freiburg",
    "Dillingen a.d.Donau": "Dillingen an der Donau",
    "Mühldorf a.Inn": "Mühldorf am Inn",
}


# This is where we do content-specific processing for each admin layer
# before merging them all into one JSON file which we convert to versatiles
# See: https://wiki.openstreetmap.org/wiki/File:Administrative_Gliederung_Deutschlands_admin_level.png
def make_admin(cache_dir: str, output_dir: str, date: date):

    # 1. Fetch the BKG data we need
    ds = date.strftime("%Y-%m-%d")

    file_name = "vg250_01-01.utm32s.shape.ebenen.zip"
    cache_path = f"{cache_dir}/{ds}_{file_name}"
    json_path = f"{cache_dir}/admin_boundaries_{ds}.geojson"
    versatiles_path = f"{output_dir}/admin_boundaries_{ds}.versatiles"

    fp = "vg250_01-01.utm32s.shape.ebenen/vg250_ebenen_0101"

    if os.path.exists(cache_path):
        print(f"Found cached data at {cache_path}")
    else:
        print("Cache miss, fetching BKG data... ")
        r = requests.get(f"{BKG_URL}/{date.year}/{file_name}")
        with open(cache_path, "wb") as f:
            f.write(r.content)
        print(f"wrote to {cache_path}")

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
    country["kind"] = "Land"
    laender["land"] = laender["SN_L"]
    laender_processed = laender.loc[laender["GF"] == 4]
    assert laender_processed.shape[0] == 16
    print(f"done ({laender_processed.shape[0]} geoms)")

    # 2.3 Admin 6
    print("Kreis... ", end="")
    kreise = gp.read_file(f"zip://{cache_path}!{fp}/VG250_KRS.shp")
    kreise["admin_level"] = 6
    country["kind"] = "Kreis"
    kreise["land"] = kreise["SN_L"]
    kreise_processed = kreise.loc[kreise["GF"] == 4]
    print(f"done ({kreise_processed.shape[0]} geoms)")

    # 2.4 Admin 8
    print("Gemeinde... ", end="")
    gemeinden = gp.read_file(f"zip://{cache_path}!{fp}/VG250_GEM.shp")
    gemeinden["admin_level"] = 8
    country["kind"] = "Gemeinde"
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

    res["name"] = res["name"].apply(lambda x: name_subs[x] if x in name_subs else x)

    res[["id", "ars", "land", "name", "admin_level", "geometry"]].to_crs(
        "wgs84"
    ).to_file(json_path)

    print(f"Wrote to {json_path}")

    try:
        make_versatiles(json_path, versatiles_path, date)
    except Exception:
        print(f"Failed to build {versatiles_path}")
        return

    return versatiles_path
