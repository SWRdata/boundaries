import datetime
import os
from typing import Dict

from dotenv import load_dotenv
from google.cloud import storage

from entities.Tileset import Tileset
from usecases.fetch_bkg_years import fetch_bkg_years
from usecases.fetch_existing import fetch_existing
from usecases.make_admin import make_admin
from usecases.make_admin_labels import make_admin_labels
from usecases.upload_blob import upload_blob

gcs_project = "swr-data-1"
gcs_bucket = "datenhub-net-static"
gcs_path = "data/boundaries/"
min_year = 2025

raw_dir = "./tmp/raw"
processed_dir = "./tmp/processed"


tilesets: Dict[str, Tileset] = {}


def run():
    load_dotenv()

    os.makedirs(os.path.dirname(raw_dir), exist_ok=True)
    os.makedirs(os.path.dirname(processed_dir), exist_ok=True)

    storage_client = storage.Client(project=gcs_project)

    print("Fetching BKG files... ", end="")
    available_years = fetch_bkg_years()
    # available_years = [2025]
    print(f"found {len(available_years)}\n")

    print("Fetching existing files... ", end="")
    existing_files = fetch_existing(storage_client, gcs_bucket, gcs_path)
    # existing_files = []
    if len(existing_files) > 0:
        print(f"found {len(existing_files)}:\n- {'\n- '.join(existing_files)}")
    else:
        print("found none")

    new_files: list[str] = []
    failed_files: list[str] = []

    for y in [y for y in available_years if y >= min_year]:
        date = datetime.date(y, 1, 1)

        tilesets[f"admin_boundaries_{date.strftime('%Y-%m-%d')}"] = Tileset(
            name=f"Administrative Boundaries {y}",
            make_fn=make_admin,
            make_args={
                "cache_dir": raw_dir,
                "output_dir": processed_dir,
                "date": date,
            },
        )

        tilesets[f"admin_labels_{date.strftime('%Y-%m-%d')}"] = Tileset(
            name=f"Administrative Labels {date}",
            make_fn=make_admin_labels,
            make_args={
                "cache_dir": raw_dir,
                "output_dir": processed_dir,
                "date": date,
            },
        )

    pending_files = [
        k for k in tilesets.keys() if f"{k}.versatiles" not in existing_files
    ]

    if len(pending_files) == 0:
        print("\nNo files to be built, bye!")
        return

    print(
        f"\n{len(pending_files)} files pending:\n- {'\n- '.join([f'{f}.versatiles' for f in pending_files])}\n"
    )

    for k in pending_files:
        print(f"Making {k}...")
        f = tilesets[k].make()
        if f:
            new_files.append(f)
        else:
            failed_files.append(k)

    for f in new_files:
        upload_blob(
            storage_client, f, gcs_bucket, os.path.join(gcs_path, os.path.basename(f))
        )

    print(f"Uploaded {len(new_files)} new files, {len(failed_files)} failed")


run()
