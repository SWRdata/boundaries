import pandas as pd
import geopandas as gp

# This is where we do content-specific processing for each admin layer
# before merging them all into one file


def process_geometry(input_path: str) -> gp.GeoDataFrame:
    fp = "vg250_01-01.utm32s.shape.ebenen/vg250_ebenen_0101"
    output_cols = ["OBJID", "ARS", "NUTS", "GEN", "BEZ", "kind", "geometry"]

    country = gp.read_file(f"zip://{input_path}!{fp}/VG250_STA.shp")
    country["id"] = country["OBJID"]
    country["kind"] = "staat"
    country_processed = country.loc[country["OBJID"] == "DEBKGVG200000CKM"][output_cols]

    # laender = gp.read_file(f"zip://{input_path}!{fp}/VG250_LAN.shp")
    # kreise = gp.read_file(f"zip://{input_path}!{fp}/VG250_KRS.shp")
    # regierungsbezirke = gp.read_file(f"zip://{input_path}!{fp}/VG250_RBZ.shp")
    # gemeinden = gp.read_file(f"zip://{input_path}!{fp}/VG250_GEM.shp")

    return pd.concat([country_processed])
