import re
import os

import requests
from bs4 import BeautifulSoup
from google.cloud import storage

from dotenv import load_dotenv
from process_geometry import process_geometry

min_year = 2025
base_url = "https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/"

raw_dir = "./tmp/raw"
processed_dir = "./tmp/processed"


def run():
    load_dotenv()
    os.makedirs(os.path.dirname(raw_dir), exist_ok=True)
    os.makedirs(os.path.dirname(processed_dir), exist_ok=True)

    # 1. List existing files
    print("Fetching existing files...")
    storage_client = storage.Client(project="swr-data-1")
    storage_path = "data/boundaries/"
    existing_files = [
        b.name.replace(storage_path, "")
        for b in list(
            storage_client.list_blobs(
                "datenhub-net-static", prefix=storage_path, delimiter="/"
            )
        )
        if b.name != storage_path
    ]
    print(f"Found {len(existing_files)}: {existing_files}")

    existing_years = [
        int(re.search(r"(?:\D+_)(.{4})(?:.+)", f).group(1)) for f in existing_files
    ]

    # 2. Check if new data was published and download it
    print("Fetching BKG index... ", end="")
    r = requests.get(base_url)
    if not r.status_code == requests.codes.ok:
        print(f"Request failed ({r.status_code}), exiting")
        return

    doc = BeautifulSoup(r.text, features="html.parser")
    new_years = [
        int(t.string.replace("/", ""))
        for t in doc.find_all("a", href=re.compile("(\\d+\\/)"))
        if int(t.string.replace("/", "")) >= min_year
        and int(t.string.replace("/", "")) not in existing_years
    ]

    print("done")

    if len(new_years) == 0:
        print("No new data found, exiting")
        return

    for i, year in enumerate(new_years):
        print(f"Fetching {year} data ({i + 1}/{len(new_years)})")

        output_dir = f"{raw_dir}/{year}/"
        if os.path.exists(output_dir):
            print("Found cached data, skipping")
            continue

        os.makedirs(os.path.dirname(output_dir), exist_ok=True)
        file_name = "vg250_01-01.utm32s.shape.ebenen.zip"

        r = requests.get(f"{base_url}{year}/{file_name}")

        with open(os.path.join(output_dir, file_name), "wb") as f:
            f.write(r.content)
        print(f"Wrote {year} data to {output_dir}{file_name}")

    # 2. Process new data and upload to GCS
    for i, year in enumerate(new_years):
        input_path = os.path.join(
            raw_dir, str(year), "vg250_01-01.utm32s.shape.ebenen.zip"
        )
        # output_path = os.path.join(processed_dir, f"boundaries_{year}_01-01.geojson")
        output_path = (
            f"gs://datenhub-net-static/data/boundaries/boundaries_{year}_0101.geojson"
        )

        print(f"Processing {year} data ({i}/{len(new_years)})", end="")
        res = process_geometry(input_path)
        print("done")

        print(f"Uploading to GCS ({output_path})... ", end="")
        res.to_file(output_path)
        print("done")


run()
