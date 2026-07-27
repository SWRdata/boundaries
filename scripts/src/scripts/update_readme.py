"""
Update the "Available Timestamps" section in the top-level readme using a manifest file
"""

# TODO: Extend the Airflow task to trigger a GH Action (via webhook) which calls this script
# It's a little convoluted but lets us easily open a PR against the repo etc
# "https://static.datenhub.net/data/boundaries/manifest.csv"

import csv
import re
from io import StringIO
from typing import Optional

import requests
from tap import Tap


class ArgumentParser(Tap):
    readme: str = ""
    readme_path: Optional[str] = None  # noqa: UP045
    manifest: Optional[str] = None  # noqa: UP045
    manifest_url: Optional[str] = None  # noqa: UP045
    quiet: bool = False

    def process_args(self):
        if not (self.manifest or self.manifest_url):
            raise ValueError("must provide either --manifest or --manifest_url")
        if not (self.readme or self.readme_path):
            raise ValueError("must provide either --readme or --readme_path")


def get_manifest(url: str) -> str | None:
    print(f"fetching manifest from {url}")
    r = requests.get(url, verify=True)
    return r.text if r.ok else None


def get_readme(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_readme(path: str, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def log(msg: str, quiet: bool):
    if not quiet:
        print(msg)


def update_readme(args: ArgumentParser) -> str:
    manifest = get_manifest(args.manifest_url) if args.manifest_url else args.manifest
    timestamps: list[str] = []

    with StringIO(manifest) as f:
        for row in csv.DictReader(f):
            m = re.search(r"(?:.+_)(\d+-\d+-\d+)(?:.+)", row["name"])
            if m:
                timestamps.append(m.group(1))

    timestamps = list(dict.fromkeys(timestamps))
    log(f"found {len(timestamps)} timestamps:\n{'\n'.join(timestamps)}", args.quiet)

    old_readme = get_readme(args.readme_path) if args.readme_path else args.readme

    # Update timestamps list
    new_readme = re.sub(
        r"(<!-- BEGIN TIMESTAMPS.+\n)(.+)(\n<!-- END TIMESTAMPS.+)",
        f"\\1{', '.join([f'`{ts}`' for ts in timestamps])}\\3",
        old_readme,
    )

    # Update latest tile URL
    new_readme = re.sub(
        r"(<!-- BEGIN LATEST_URL.+\n`+\n.+admin_boundaries_)((\d){4}-(\d){2}-(\d){2})(.+\n`+\n<!-- END LATEST_URL.+)",
        "\\g<1>" + timestamps[-1] + "\\g<6>",
        new_readme,
    )

    if (new_readme != old_readme) and args.readme_path:
        write_readme(args.readme_path, new_readme)
        log(f"wrote updated readme to {args.readme_path}", args.quiet)

    return new_readme


if __name__ == "__main__":
    update_readme(ArgumentParser(description=__doc__).parse_args())
