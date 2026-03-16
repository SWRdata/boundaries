import geopandas as gp
import pandas as pd


def make_admin(input_path: str, year: int):

    # This is where we do content-specific processing for each admin layer before merging them all into one file
    # See: https://wiki.openstreetmap.org/wiki/File:Administrative_Gliederung_Deutschlands_admin_level.png

    name_subs = {
        "Freiburg im Breisgau": "Freiburg",
        "Dillingen a.d.Donau": "Dillingen an der Donau",
        "Mühldorf a.Inn": "Mühldorf am Inn",
    }

    fp = "vg250_01-01.utm32s.shape.ebenen/vg250_ebenen_0101"
    output_cols = ["id", "ars", "land", "name", "admin_level", "geometry"]

    # Admin 2
    print("Staat... ", end="")
    country = gp.read_file(f"zip://{input_path}!{fp}/VG250_STA.shp")
    country["admin_level"] = 2
    country["kind"] = "Staat"
    country_processed = country.loc[country["OBJID"] == "DEBKGVG200000CKM"]
    assert country_processed.shape[0] == 1
    print(f"done ({country_processed.shape[0]} geom)")

    # Admin 4
    print("Land... ", end="")
    laender = gp.read_file(f"zip://{input_path}!{fp}/VG250_LAN.shp")
    laender["admin_level"] = 4
    country["kind"] = "Land"
    laender["land"] = laender["SN_L"]
    laender_processed = laender.loc[laender["GF"] == 4]
    assert laender_processed.shape[0] == 16
    print(f"done ({laender_processed.shape[0]} geoms)")

    # Admin 6
    print("Kreis... ", end="")
    kreise = gp.read_file(f"zip://{input_path}!{fp}/VG250_KRS.shp")
    kreise["admin_level"] = 6
    country["kind"] = "Kreis"
    kreise["land"] = kreise["SN_L"]
    kreise_processed = kreise.loc[kreise["GF"] == 4]
    print(f"done ({kreise_processed.shape[0]} geoms)")

    # Admin 8
    print("Gemeinde... ", end="")
    gemeinden = gp.read_file(f"zip://{input_path}!{fp}/VG250_GEM.shp")
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

    return res[output_cols].to_crs("wgs84")
