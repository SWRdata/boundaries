import datetime as dt
import subprocess


def make_versatiles(
    input_path: str, output_path: str, date: dt.date, tc_args: list[str] = []
):
    mbtiles_path = output_path.replace(".versatiles", ".mbtiles")
    mbtiles_path_tmp = mbtiles_path.replace(".mbtiles", "_tmp.mbtiles")

    print("Building tiles... ", end="")
    subprocess.run(
        [
            "tippecanoe",
            "--name",
            "SWR Data Lab Boundaries",
            f"--description=Administrative boundaries for Germany as of {date.strftime('%Y/%m/%d')}",
            f"--attribution=© BKG ({date.year}) dl-de/by-2-0",
            "--layer",
            "administrative",
            "--low-detail=10",  # Lower than default for better aesthetics at low zooms
            "--minimum-zoom=0",
            "--maximum-zoom=8",
            "--generate-ids",
            "--extend-zooms-if-still-dropping",
            "--coalesce-densest-as-needed",
            "--no-progress-indicator",
            "--quiet",
            "--force",
            *tc_args,
            "-o",
            mbtiles_path,
            input_path,
        ]
    ).check_returncode()

    # Unclear to me why this fixes overzoom but it does
    subprocess.run(["tile-join", "-f", "-o", mbtiles_path_tmp, mbtiles_path])

    print("done")
    print("Converting to versatiles... ", end="")

    subprocess.run(
        [
            "versatiles",
            "convert",
            "--compress=brotli",
            mbtiles_path_tmp,
            output_path,
        ]
    ).check_returncode()
    print("done")

    print("Cleaning up temporary files... ", end="")
    subprocess.run(["rm", mbtiles_path]).check_returncode()
    subprocess.run(["rm", mbtiles_path_tmp]).check_returncode()
    print("done\n")
