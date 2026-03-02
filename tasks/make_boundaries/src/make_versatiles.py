import subprocess


def make_versatiles(input_path: str, output_path: str):
    mbtiles_path = output_path.replace(".versatiles", ".mbtiles")

    subprocess.run(
        [
            "tippecanoe",
            "-l",
            "boundaries",
            "--low-detail=10",
            "-zg",
            "--generate-ids",
            "--extend-zooms-if-still-dropping",
            "--coalesce-densest-as-needed",
            "-f",
            "-o",
            mbtiles_path,
            input_path,
        ]
    ).check_returncode()

    subprocess.run(
        ["versatiles", "convert", "--compress=brotli", mbtiles_path, output_path]
    ).check_returncode()

    subprocess.run(["rm", mbtiles_path]).check_returncode()
