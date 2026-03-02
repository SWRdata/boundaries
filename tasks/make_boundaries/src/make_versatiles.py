import subprocess


def make_versatiles(input_path: str, output_path: str) -> str:
    mbtiles_path = output_path.replace(".versatiles", ".mbtiles")

    subprocess.run(
        [
            "tippecanoe",
            "-zg",
            "--extend-zooms-if-still-dropping ",
            "--coalesce-densest-as-needed ",
            "-f",
            "-o",
            mbtiles_path,
            input_path,
        ]
    ).check_returncode()

    subprocess.run(
        ["versatiles", "convert", "--compress=brotli", mbtiles_path, output_path]
    ).check_returncode()

    subprocess.run("rm", mbtiles_path).check_returncode()
