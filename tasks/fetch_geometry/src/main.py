import re
import os

import requests
from bs4 import BeautifulSoup

min_year = 2023
cache_dir = "./tmp"
base_url = "https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/"


def run():
    os.makedirs(os.path.dirname(cache_dir), exist_ok=True)

    r = requests.get(base_url)
    if not r.status_code == requests.codes.ok:
        print(f"Request failed ({r.status_code}), exiting")
        return

    doc = BeautifulSoup(r.text, features="html.parser")

    links = [
        t
        for t in doc.find_all("a", href=re.compile("(\\d+\\/)"))
        if int(t.string.replace("/", "")) >= min_year
        and not os.path.exists(f"{cache_dir}/{t.string}")
    ]

    if len(links) == 0:
        print("No new geometry found, exiting")
        return

    print(links)

    for link in links:
        os.makedirs(
            os.path.dirname(f"{cache_dir}/{link.string}"),
            exist_ok=True,
        )


run()

# soup = BeautifulSoup("<html>data</html>")
