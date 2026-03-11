from typing import Callable


class Tileset:
    name: str
    output: str

    def __init__(self, name: str, make_fn: Callable):
        self.name = name
        self.make_fn = make_fn

    def make(self, existing_files: list[str]):
        self.make_fn(existing_files)
