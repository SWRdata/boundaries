import subprocess


def make_versatiles(input_path: str, output_path: str, year: int):
    mbtiles_path = output_path.replace(".versatiles", ".mbtiles")

    subprocess.run(
        [
            "tippecanoe",
            "--name",
            "SWR Data Lab Boundaries",
            f"--description=German admin boundaries (VG250) as of {year}-01-01",
            f"--attribution=© BKG ({year}) dl-de/by-2-0",
            "--layer",
            "administrative",
            "--low-detail=10",
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

    subprocess.run(
        ["versatiles", "convert", "--compress=brotli", mbtiles_path, output_path]
    ).check_returncode()

    subprocess.run(["rm", mbtiles_path]).check_returncode()
