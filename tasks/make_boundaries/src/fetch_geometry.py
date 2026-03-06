import os
import re

import requests
from bs4 import BeautifulSoup
from google.cloud import storage


def fetch_geometry(
    min_year: int,
    storage_client: storage.Client,
    gcs_bucket: str,
    gcs_path: str,
    base_url: str,
    output_path: str,
) -> list[int]:

    print("Fetching existing files...")
    existing_files = [
        b.name.replace(gcs_path, "")
        for b in list(
            storage_client.list_blobs(gcs_bucket, prefix=gcs_path, delimiter="/")
        )
        if b.name != gcs_path
    ]

    existing_years = {
        int(re.search(r"(?:\D+_)(.{4})(?:.+)", f).group(1)) for f in existing_files
    }

    print(f"Found {len(existing_files)}: {existing_files}")

    # 2. Check if new data was published and download it
    print("Fetching BKG index... ")

    # verify=False because the government issued itself a broken SSL cert
    r = requests.get(base_url, verify=False)
    if not r.status_code == requests.codes.ok:
        print(f"Request failed ({r.status_code}), exiting")
        return []

    doc = BeautifulSoup(r.text, features="html.parser")
    new_years = [
        int(t.string.replace("/", ""))
        for t in doc.find_all("a", href=re.compile("(\\d+\\/)"))
        if int(t.string.replace("/", "")) >= min_year
        and int(t.string.replace("/", "")) not in existing_years
    ]

    if len(new_years) == 0:
        return []

    for i, year in enumerate(new_years):
        print(f"Fetching {year} data ({i + 1}/{len(new_years)})")
        output_dir = f"{output_path}/{year}/"
        if os.path.exists(output_dir):
            print("Found cached data, skipping")
            continue

        os.makedirs(os.path.dirname(output_dir), exist_ok=True)
        file_name = "vg250_01-01.utm32s.shape.ebenen.zip"

        r = requests.get(f"{base_url}{year}/{file_name}")

        with open(os.path.join(output_dir, file_name), "wb") as f:
            f.write(r.content)
        print(f"Wrote to {output_dir}{file_name}")
    return new_years
