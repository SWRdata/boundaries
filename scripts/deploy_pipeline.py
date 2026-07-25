"""
Deploy an Airflow pipeline to SWR Data Lab infrastructure
"""

# 1. Find all Dockerfiles in the repo
# 2. Build and push each one to Google's artifact registry (docker.pkg.dev), here: https://console.cloud.google.com/artifacts/docker/swr-datalab-prod/europe-west3/etl-images-airflow-swr-data-lab?project=swr-datalab-prod
# 3. SSH into the Airflow box and pull the new images
# 4. Deploy the ./dag folder to GCS (airflow notices and pulls that itself)

# See: https://docs.cloud.google.com/composer/docs/composer-3/dag-cicd-github#presubmit-check-job

import glob
import os
import re
import secrets
import subprocess
from sys import stdout

from tap import Tap


class ArgumentParser(Tap):
    base_dir: str = "tasks"  # base dir
    registry_base: str  # artifact registry base url
    bucket_name: str = ""  # name of your composer environment's DAGs bucket


def cleanup_registry():
    pass


def cleanup_storage():
    pass


def upload_dag_folder():
    pass


def read_file(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


def main(args: ArgumentParser):

    local_tags: list[str] = []

    dockerfiles = glob.glob(f"{args.base_dir}/**/Dockerfile")
    if not dockerfiles:
        print("No Dockerfiles found, exiting")
        return

    dag_name = read_file("./.github/REPO_NAME").strip().replace("-", "_")
    if not dag_name:
        print("Failed to get DAG name, exiting")
        return

    gcp_token = os.environ.get("GCP_ACCESS_TOKEN")
    if not gcp_token:
        print("Failed to get GCP access token key, exiting")
        return

    for i, path in enumerate([d.strip("Dockerfile") for d in dockerfiles]):
        print(f"building {path}/Dockerfile ({i + 1}/{len(dockerfiles)})")

        image_name = (
            path.replace("/", "_").replace("\\", "_").replace(".", "").strip("_")
        )

        image_tag = f"{args.registry_base}/{dag_name}_fix21_{image_name}:latest"

        subprocess.run(
            [
                "docker",
                "login",
                "--username",
                "oauth2accesstoken",
                "--password",
                gcp_token,
            ],
            stdout=subprocess.DEVNULL,  # supress logs to not leak secrets
        ).check_returncode()

        subprocess.run(
            [
                "docker",
                "build",
                path,
                "--tag",
                image_tag,
                "--secret",
                "id=google_creds,env=GAR_READER_SA_KEY",
                "--push",
            ]
        ).check_returncode()
        local_tags.append(image_tag)

    # It seems to me like we don't really need to SSH into any box,
    # the KubernetesPodOperator will just pull the image itself
    # https://docs.cloud.google.com/composer/docs/composer-3/use-kubernetes-pod-operator#minimal-config

    # upload the dag folder to GCS
    upload_dag_folder()

    # if the repo name changed:
    cleanup_registry()
    cleanup_storage()

    # if task meta changed:
    cleanup_registry()


if __name__ == "__main__":
    main(ArgumentParser(description=__doc__).parse_args())
