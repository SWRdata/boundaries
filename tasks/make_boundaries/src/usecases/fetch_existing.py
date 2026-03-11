import re

from google.cloud import storage


def fetch_existing(
    storage_client: storage.Client,
    gcs_bucket: str,
    gcs_path: str,
) -> list[str]:

    print("Fetching existing files...")

    existing_files = [
        b.name.replace(gcs_path, "")
        for b in list(
            storage_client.list_blobs(gcs_bucket, prefix=gcs_path, delimiter="/")
        )
        if b.name != gcs_path
    ]

    print(f"Found {len(existing_files)}: {existing_files}")

    return existing_files
