import datetime
import os
from typing import Dict, Literal

from dotenv import load_dotenv
from google.cloud import storage
from tap import Tap

from entities.Tileset import Tileset
from usecases.fetch_bkg_years import fetch_bkg_years
from usecases.fetch_existing import fetch_existing
from usecases.make_admin import make_admin
from usecases.make_admin_labels import make_admin_labels
from usecases.upload_blob import upload_blob


class ArgParser(Tap):
    mode: Literal["prod", "dev"]
    """dev mode disables reading/writing to GCS and some data fetches"""
    min_year: int = 2024
    gcs_project: str = "swr-data-1"
    gcs_bucket: str = "datenhub-net-static"
    gcs_path: str = "data/boundaries/"
    raw_dir: str = "./tmp/raw/"
    processed_dir: str = "./tmp/processed/"


def main(args: ArgParser):
    tilesets: Dict[str, Tileset] = {}

    load_dotenv()
    os.makedirs(os.path.dirname(args.raw_dir), exist_ok=True)
    os.makedirs(os.path.dirname(args.processed_dir), exist_ok=True)
    manifest_path = os.path.join(args.processed_dir, "manifest.csv")

    if args.mode == "prod":
        storage_client = storage.Client(project=args.gcs_project)

    if args.mode == "prod":
        print("fetching available bkg files... ", end="")
        available_years = fetch_bkg_years()
    else:
        print("skipping fetching bkg files in dev mode", end="")
        available_years = [2025]
    print(f"found {len(available_years)}\n")

    if args.mode == "prod":
        print("fetching existing files", end="")
        existing_files = fetch_existing(storage_client, args.gcs_bucket, args.gcs_path)
    else:
        print("skipping fetching existing files in dev mode", end="")
        existing_files = []

    if len(existing_files) > 0:
        print(f"found {len(existing_files)}:\n- {'\n- '.join(existing_files)}")
    else:
        print("found none")

    new_files: list[str] = []
    failed_files: list[str] = []

    for y in [y for y in available_years if y >= args.min_year]:
        date = datetime.date(y, 1, 1)

        tilesets[f"admin_boundaries_{date.strftime('%Y-%m-%d')}"] = Tileset(
            name=f"Administrative Boundaries {y}",
            make_fn=make_admin,
            make_args={
                "cache_dir": args.raw_dir,
                "output_dir": args.processed_dir,
                "date": date,
            },
        )

        tilesets[f"admin_labels_{date.strftime('%Y-%m-%d')}"] = Tileset(
            name=f"Administrative Labels {date}",
            make_fn=make_admin_labels,
            make_args={
                "cache_dir": args.raw_dir,
                "output_dir": args.processed_dir,
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
            new_files.extend(f)
        else:
            failed_files.append(k)

    with open(manifest_path, "w") as f:
        f.write(f"name\n{'\n'.join([*existing_files, *new_files])}")
        print(f"Wrote manifest to {manifest_path}")

    if args.mode == "prod":
        for f in [*new_files, manifest_path]:
            upload_blob(
                storage_client,
                f,
                args.gcs_bucket,
                os.path.join(args.gcs_path, os.path.basename(f)),
            )
        print(f"Uploaded {len(new_files)} new files, {len(failed_files)} failed")
    else:
        print(
            f"skipping updloading {len(new_files)} new files, {len(failed_files)} failed in dev mode"
        )


args = ArgParser().parse_args()
main(args)
