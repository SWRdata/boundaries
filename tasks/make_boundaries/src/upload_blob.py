from google.cloud import storage


def upload_blob(
    client: storage.Client, source_path: str, bucket_name: str, destination_path: str
):

    bucket = client.bucket(bucket_name)

    blob = bucket.blob(destination_path)
    blob.upload_from_filename(source_path)

    print(f"{source_path} uploaded to {destination_path}")
