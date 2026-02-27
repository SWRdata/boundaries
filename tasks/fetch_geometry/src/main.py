import re
import os

import requests
from bs4 import BeautifulSoup
from process_geometry import process_geometry

min_year = 2025
base_url = "https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/"

raw_dir = "./tmp/raw"
processed_dir = "./tmp/processed"


def run():
    os.makedirs(os.path.dirname(raw_dir), exist_ok=True)
    os.makedirs(os.path.dirname(processed_dir), exist_ok=True)

    # 1. Check if new data was published and download it
    # print("Fetching index page... ", end="")
    # r = requests.get(base_url)
    # if not r.status_code == requests.codes.ok:
    #     print(f"Request failed ({r.status_code}), exiting")
    #     return
    # print("done")

    # print("Parsing index page... ", end="")
    # doc = BeautifulSoup(r.text, features="html.parser")
    # print("done")

    # links = [
    #     t
    #     for t in doc.find_all("a", href=re.compile("(\\d+\\/)"))
    #     if int(t.string.replace("/", "")) >= min_year
    #     and not os.path.exists(f"{raw_dir}/{t.string}")
    # ]

    # if len(links) == 0:
    #     print("No new data found, continuing")
    # else:
    #     print(f"Fetching data for {[link.string.replace('/', '') for link in links]}")

    # for year in [L.string.replace("/", "") for L in links]:
    #     output_dir = f"{raw_dir}/{year}/"
    #     os.makedirs(os.path.dirname(output_dir), exist_ok=True)

    #     fn = "vg250_01-01.utm32s.shape.ebenen.zip"
    #     r = requests.get(os.path.join(base_url, year, fn))
    #     with open(os.path.join(output_dir, fn), "wb") as f:
    #         f.write(r.content)
    #     print(f"Wrote {year} data to {output_dir}{fn}")

    # 2. Process any new data
    for year in os.listdir(raw_dir):
        print(year)
        input_path = os.path.join(raw_dir, year, "vg250_01-01.utm32s.shape.ebenen.zip")
        output_path = os.path.join(processed_dir, f"boundaries_{year}_01-01.geojson")

        if os.path.exists(output_path):
            print(f"Found cached data at {output_path}, skipping")
            continue

        print(f"Processing {year} data ({input_path})")
        process_geometry(input_path, output_path)


run()
