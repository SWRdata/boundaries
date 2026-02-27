#!/usr/bin/env python3
import sys
import yaml
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CONFIG_PATH = Path("dag/configuration.yaml")


def main():
    if not CONFIG_PATH.exists():
        print(f"⚠️ Datei {CONFIG_PATH} nicht gefunden, überspringe YAML-Check.")
        return 0

    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"❌ YAML-Fehler in {CONFIG_PATH}:\n{e}")
        print("Bitte korrigiere die YAML-Syntax bevor du commitest.")
        return 1

    print(f"✅ {CONFIG_PATH} ist syntaktisch korrekt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
