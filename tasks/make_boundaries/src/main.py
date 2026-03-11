import os
from typing import Dict

from dotenv import load_dotenv
from google.cloud import storage

from entities.Tileset import Tileset
from make_versatiles import make_versatiles
from process_geometry import process_geometry
from upload_blob import upload_blob
from usecases.fetch_bkg_years import fetch_bkg_years
from usecases.fetch_existing import fetch_existing
from usecases.make_admin import make_admin

gcs_project = "swr-data-1"
gcs_bucket = "datenhub-net-static"
gcs_path = "data/boundaries/"
min_year = 2024

raw_dir = "./tmp/raw/"
processed_dir = "./tmp/processed/"


tilesets: Dict[str, Tileset] = {}


def run():
    load_dotenv()

    os.makedirs(os.path.dirname(raw_dir), exist_ok=True)
    os.makedirs(os.path.dirname(processed_dir), exist_ok=True)

    storage_client = storage.Client(project=gcs_project)

    available_years = fetch_bkg_years()
    existing_files = fetch_existing(storage_client, gcs_bucket, gcs_path)

    for y in [y for y in available_years if y >= min_year]:
        tilesets[f"admin_labels_{y}"] = Tileset(
            f"Administrative Boundaries {y}", make_admin
        )
        tilesets[f"admin_boundaries_{y}"] = Tileset(
            f"Administrative Labels {y}", make_admin
        )

    for k, v in tilesets.items():
        if f"{k}.versatiles" not in existing_files:
            v.make(existing_files)

    return


run()
