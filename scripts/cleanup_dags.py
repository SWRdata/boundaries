"""
Delete unused DAG files in the remote storage
"""

import glob
import os
import re
import secrets
import subprocess
from sys import stdout

from tap import Tap


class ArgumentParser(Tap):
    base_dir: str = "tasks"  # base directory to search for dockerfiles
    bucket_name: str = ""  # name of your Managed Airflow's DAGs bucket


def main(args: ArgumentParser):
    pass


if __name__ == "__main__":
    main(ArgumentParser(description=__doc__).parse_args())
