import subprocess


def make_versatiles(input_path: str, output_path: str, year: int):
    mbtiles_path = output_path.replace(".versatiles", ".mbtiles")
    mbtiles_path_tmp = mbtiles_path.replace("boundaries_", "tmp-boundaries_")

    subprocess.run(
        [
            "tippecanoe",
            "--no-progress-indicator",
            "--name",
            "SWR Data Lab Boundaries",
            f"--description=Geographic boundary data for Germany as of {year}-01-01",
            f"--attribution=© BKG ({year}) dl-de/by-2-0",
            "--layer",
            "administrative",
            "--low-detail=10",  # Lower than default for better aesthetics at low zooms
            "--minimum-zoom=0",
            "--maximum-zoom=8",
            "--generate-ids",
            "--extend-zooms-if-still-dropping",
            "--coalesce-densest-as-needed",
            "--force",
            "-o",
            mbtiles_path,
            input_path,
        ]
    ).check_returncode()

    # Unclear to me why this fixes overzoom but it does
    subprocess.run(["tile-join", "-f", "-o", mbtiles_path_tmp, mbtiles_path])

    subprocess.run(
        [
            "versatiles",
            "convert",
            "--quiet",
            "--compress=brotli",
            mbtiles_path_tmp,
            output_path,
        ]
    ).check_returncode()

    subprocess.run(["rm", mbtiles_path]).check_returncode()
    subprocess.run(["rm", mbtiles_path_tmp]).check_returncode()
