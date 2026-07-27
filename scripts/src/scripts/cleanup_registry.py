"""
Delete unused docker images from the registry
"""

from tap import Tap


class ArgumentParser(Tap):
    base_dir: str = "tasks"  # base directory to search for dockerfiles
    registry_base: str  # artifact registry base url


def main(args: ArgumentParser):

    _local_tags: list[str] = []


if __name__ == "__main__":
    main(ArgumentParser(description=__doc__).parse_args())
