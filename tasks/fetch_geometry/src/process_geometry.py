import geopandas as gp


def process_geometry(input_path: str, output_path: str):
    laender = gp.read_file(
        f"zip://{input_path}!vg250_01-01.utm32s.shape.ebenen/vg250_ebenen_0101/VG250_LAN.shp"
    )
    print(laender)
    return
