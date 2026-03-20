import csv
import re
from io import StringIO

import requests


def run():
    manifest_url = "https://static.datenhub.net/data/boundaries/manifest.csv"
    r = requests.get(manifest_url, verify=True)

    if not r.ok:
        print(f"Request failed ({r.status_code}), exiting")
        return

    timestamps: set[str] = set()

    with StringIO(r.text) as f:
        reader = csv.DictReader(f)
        for row in reader:
            m = re.search(r"(?:.+_)(\d+-\d+-\d+)(?:.+)", row["name"])
            if m:
                timestamps.add(m.group(1))

    print(f"Found {len(timestamps)} timestamps:\n{'\n'.join(timestamps)}")

    old_readme: str = ""
    new_readme: str = ""

    with open("../README.md", "r") as f:
        old_readme = f.read()
        new_readme = re.sub(
            r"(<!-- BEGIN TIMESTAMPS.+\n)(.+)(\n<!-- END TIMESTAMPS.+)",
            f"\\1{', '.join([f'`{ts}`' for ts in timestamps])}\\3",
            old_readme,
        )

    if new_readme != old_readme:
        with open("../README.md", "w") as f:
            f.write(new_readme)
            print("Readme updated")


run()
