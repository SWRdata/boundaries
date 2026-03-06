#!/usr/bin/env python3

import yaml
import sys
from pathlib import Path

CONFIG_PATH = Path("dag/configuration.yaml")
TASKS_DIR = Path("tasks")


def extract_image_suffixes(config_section):
    if not config_section:
        return []
    return [
        task.get("image_suffix") for task in config_section if isinstance(task, dict)
    ]


def main():
    if not CONFIG_PATH.exists():
        print(f"❌ Konfigurationsdatei {CONFIG_PATH} nicht gefunden.", file=sys.stderr)
        return 1

    if not TASKS_DIR.exists():
        print(f"❌ Aufgabenverzeichnis {TASKS_DIR} nicht gefunden.", file=sys.stderr)
        return 1

    with CONFIG_PATH.open(encoding="utf-8") as f:
        config = yaml.safe_load(f)

    dag_tasks = config.get("dag_task_parameters", {})
    sequential_tasks = extract_image_suffixes(dag_tasks.get("sequential", []))
    parallel_tasks = extract_image_suffixes(dag_tasks.get("parallel", []))

    all_suffixes = set(sequential_tasks + parallel_tasks)

    existing_task_dirs = {p.name for p in TASKS_DIR.iterdir() if p.is_dir()}

    missing = [s for s in all_suffixes if s and s not in existing_task_dirs]

    if missing:
        print(
            "❌ Diese image_suffix-Werte haben keinen entsprechenden Ordner in 'tasks/':"
        )
        for s in missing:
            print(f"  - {s}")
        return 1

    print("✅ Alle image_suffix-Werte stimmen mit Unterordnern in 'tasks/' überein.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
