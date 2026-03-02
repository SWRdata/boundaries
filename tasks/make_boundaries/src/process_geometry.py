import geopandas as gp
import pandas as pd

# This is where we do content-specific processing for each admin layer
# before merging them all into one file


def process_geometry(input_path: str) -> gp.GeoDataFrame:
    fp = "vg250_01-01.utm32s.shape.ebenen/vg250_ebenen_0101"
    output_cols = ["OBJID", "ARS", "NUTS", "GEN", "BEZ", "id", "kind", "geometry"]

    # Admin 0
    print("Staat... ", end="")
    country = gp.read_file(f"zip://{input_path}!{fp}/VG250_STA.shp")
    country["id"] = country["OBJID"]
    country["kind"] = "staat"
    country_processed = country.loc[country["OBJID"] == "DEBKGVG200000CKM"][output_cols]

    print(f"done ({country_processed.shape[0]} geom)")
    assert country_processed.shape[0] == 1

    # Admin 1
    print("Land... ", end="")
    laender = gp.read_file(f"zip://{input_path}!{fp}/VG250_LAN.shp")
    laender["id"] = laender["OBJID"]
    laender["kind"] = "land"
    laender_processed = laender.loc[laender["GF"] == 4][output_cols]

    print(f"done ({laender_processed.shape[0]} geoms)")
    assert laender_processed.shape[0] == 16

    # Admin 2
    print("Kreis... ", end="")
    kreise = gp.read_file(f"zip://{input_path}!{fp}/VG250_KRS.shp")
    kreise["id"] = kreise["OBJID"]
    kreise["kind"] = "kreis"
    kreise_processed = kreise.loc[kreise["GF"] == 4][output_cols]

    print(f"done ({kreise_processed.shape[0]} geoms)")
    
    # Admin 4
    print("Gemeinde... ", end="")
    gemeinden = gp.read_file(f"zip://{input_path}!{fp}/VG250_GEM.shp")
    gemeinden["id"] = gemeinden["OBJID"]
    gemeinden["kind"] = "gemeinde"
    gemeinden_processed = gemeinden.loc[gemeinden["GF"] == 4][output_cols]
    print(f"done ({gemeinden_processed.shape[0]} geoms)")

    return gp.GeoDataFrame(pd.concat([country_processed, laender_processed, kreise_processed, gemeinden_processed])).to_crs("wgs84")
