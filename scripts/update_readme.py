"""
TODO: Extend the Airflow task to trigger a GH Action (via webhook) which calls this script
It's a little convoluted but lets us easily open a PR against the repo etc
"""

import csv
import re
from io import StringIO

import requests
from tap import Tap


class ArgumentParser(Tap):
    readme_path: str


def main(args: ArgumentParser):
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

    with open(args.readme_path, "r") as f:
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
        else:
            print("nothing to do do, exiting")


if __name__ == "__main__":
    main(ArgumentParser(description=__doc__).parse_args())
