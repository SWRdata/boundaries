"""
Delete unused docker images from the registry
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
    registry_base: str  # artifact registry base url


def main(args: ArgumentParser):

    local_tags: list[str] = []
    pass


if __name__ == "__main__":
    main(ArgumentParser(description=__doc__).parse_args())
