import os
import re
from subprocess import CalledProcessError

from dotenv import load_dotenv
from google.cloud import storage

from fetch_geometry import fetch_geometry
from make_versatiles import make_versatiles
from process_geometry import process_geometry

base_url = "https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/"
gcs_bucket = "datenhub-net-static"
gcs_path = "data/boundaries/"
min_year = 2024

raw_dir = "./tmp/raw/"
processed_dir = "./tmp/processed/"

skip_fetch = True


def run():
    load_dotenv()
    cwd = os.path.dirname(os.path.realpath(__file__))
    os.makedirs(os.path.dirname(raw_dir), exist_ok=True)
    os.makedirs(os.path.dirname(processed_dir), exist_ok=True)

    storage_client = storage.Client(project="swr-data-1")

    # 1. List existing files
    # new_years = fetch_geometry(
    #     min_year, storage_client, gcs_bucket, gcs_path, base_url, raw_dir
    # )

    # if len(new_years) == 0:
    #     print("No new data found, exiting")
    #     return

    new_years = [2025]

    # 2. Process new data
    for i, year in enumerate(new_years):
        input_path = os.path.join(
            raw_dir, str(year), "vg250_01-01.utm32s.shape.ebenen.zip"
        )
        geojson_path = os.path.join(processed_dir, f"boundaries_{year}_01-01.geojson")
        versatiles_path = os.path.join(
            processed_dir, f"boundaries_{year}_01-01.versatiles"
        )

        print(f"Processing {year} data ({i + 1}/{len(new_years)})... ")
        print("Making geojson... ", end="")
        res = process_geometry(input_path)
        res.to_file(geojson_path)
        print(f"wrote to {geojson_path}")

        print("Making versatiles...")
        make_versatiles(geojson_path, versatiles_path)

        # print(f"Uploading to GCS ({output_path})... ", end="")
        # res.to_file(output_path)
        # print("done")


run()
