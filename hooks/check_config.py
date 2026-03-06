#!/usr/bin/env python3

import sys
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def run_check(script_path, label):
    print(f"\n🔍 Running {label} ...")
    result = subprocess.run(["python", script_path])
    if result.returncode != 0:
        print(f"❌ {label} failed.")
    else:
        print(f"✅ {label} passed.")
    return result.returncode


def main():
    # First: validate YAML structure
    config_check = run_check(
        "hooks/check_configuration_yaml.py", "configuration.yaml check"
    )
    if config_check != 0:
        print("⛔ Aborting further checks.")
        return 1

    # Second: check image_suffix matches folder names
    suffix_check = run_check("hooks/check_task_names.py", "image_suffix check")
    if suffix_check != 0:
        return 1

    print("\n✅ All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
