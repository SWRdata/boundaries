from google.cloud import storage


def fetch_existing(
    storage_client: storage.Client,
    gcs_bucket: str,
    gcs_path: str,
) -> list[str]:

    existing_files = [
        b.name.replace(gcs_path, "")
        for b in list(
            storage_client.list_blobs(gcs_bucket, prefix=gcs_path, delimiter="/")
        )
        if b.name != gcs_path
    ]

    return existing_files
