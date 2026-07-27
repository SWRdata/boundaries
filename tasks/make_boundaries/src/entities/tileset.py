from collections.abc import Callable
from typing import Any


class Tileset:
    name: str
    date: str

    def __init__(
        self,
        name: str,
        make_fn: Callable,
        make_args: dict[str, Any],
    ):
        self.name = name
        self.make_fn = make_fn
        self.make_args = make_args

    def make(self) -> list[str] | None:
        return self.make_fn(**self.make_args)
