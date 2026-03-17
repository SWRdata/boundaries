import os

import requests


def fetch_unless_cached(url: str, cache_path: str):
    if os.path.exists(cache_path):
        print(f"Found cached data at {cache_path}")
    else:
        print(f"Cache miss, fetching from {url}... ", end="")
        r = requests.get(url)
        with open(cache_path, "wb") as f:
            f.write(r.content)
        print(f"wrote to {cache_path}")
