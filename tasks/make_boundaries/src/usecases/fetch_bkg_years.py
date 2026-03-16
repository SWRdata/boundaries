import re

import requests
from bs4 import BeautifulSoup

from globals import BKG_URL

# Fetches a list of available years from the BKG website


def fetch_bkg_years() -> list[int]:

    # verify=False if the government issued itself a broken SSL cert again
    r = requests.get(BKG_URL, verify=True)
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
