import re

import requests
from bs4 import BeautifulSoup

# Fetches a list of available years from the BKG website


def fetch_bkg_years() -> list[int]:
    base_url = "https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/"

    print("Fetching BKG index... ")

    # verify=False because the government issued itself a broken SSL cert
    r = requests.get(base_url, verify=False)
    if not r.ok:
        print(f"Request failed ({r.status_code}), exiting")
        return []

    doc = BeautifulSoup(r.text, features="html.parser")

    links = doc.find_all("a", href=re.compile("(\\d+\\/)"))

    return [
        year
        for year in [
            int(t.string.replace("/", "")) if t.string else None for t in links
        ]
        if year is not None
    ]
