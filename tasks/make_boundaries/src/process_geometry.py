import geopandas as gp
import pandas as pd

# This is where we do content-specific processing for each admin layer
# before merging them all into one file
# See: https://wiki.openstreetmap.org/wiki/File:Administrative_Gliederung_Deutschlands_admin_level.png


def process_geometry(input_path: str) -> gp.GeoDataFrame:
    fp = "vg250_01-01.utm32s.shape.ebenen/vg250_ebenen_0101"
    output_cols = ["ARS", "GEN", "id", "admin", "land", "geometry"]

    # Admin 2
    print("Staat... ", end="")
    country = gp.read_file(f"zip://{input_path}!{fp}/VG250_STA.shp")
    country["id"] = country["OBJID"]
    country["admin"] = 2
    country_processed = country.loc[country["OBJID"] == "DEBKGVG200000CKM"]
    assert country_processed.shape[0] == 1
    print(f"done ({country_processed.shape[0]} geom)")

    # Admin 4
    print("Land... ", end="")
    laender = gp.read_file(f"zip://{input_path}!{fp}/VG250_LAN.shp")
    laender["id"] = laender["OBJID"]
    laender["admin"] = 4
    laender_processed = laender.loc[laender["GF"] == 4]
    assert laender_processed.shape[0] == 16
    print(f"done ({laender_processed.shape[0]} geoms)")

    # Admin 6
    print("Kreis... ", end="")
    kreise = gp.read_file(f"zip://{input_path}!{fp}/VG250_KRS.shp")
    kreise["id"] = kreise["OBJID"]
    kreise["admin"] = 6
    kreise["land"] = kreise["SN_L"]
    kreise_processed = kreise.loc[kreise["GF"] == 4]
    print(f"done ({kreise_processed.shape[0]} geoms)")

    # Admin 8
    print("Gemeinde... ", end="")
    gemeinden = gp.read_file(f"zip://{input_path}!{fp}/VG250_GEM.shp")
    gemeinden["id"] = gemeinden["OBJID"]
    gemeinden["admin"] = 8
    gemeinden["land"] = gemeinden["SN_L"]
    gemeinden_processed = gemeinden.loc[gemeinden["GF"] == 4]
    print(f"done ({gemeinden_processed.shape[0]} geoms)")

    return gp.GeoDataFrame(
        pd.concat(
            [
                country_processed,
                laender_processed,
                kreise_processed,
                gemeinden_processed,
            ]
        )
    )[output_cols].to_crs("wgs84")
