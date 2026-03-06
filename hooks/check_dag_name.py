#!/usr/bin/env python3
# Prüft auf validen Repo-Namen (nur Kleinbuchstaben und Unterstriche)
# Prüft, ob dag_name in dag.py identisch ist mit dem Repo-Namen
import re
import sys
from pathlib import Path
import configparser
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DAG_PATH = Path("dag/dag.py")
GIT_CONFIG_PATH = Path(".git/config")


def extract_dag_name_line():
    """Findet dag_name = ... in dag.py"""
    with DAG_PATH.open(encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        match = re.match(r'(dag_name\s*=\s*["\'])(.+?)(["\'])', line)
        if match:
            return i, match.group(1), match.group(2), match.group(3)

    print("❌  Kein 'dag_name = ...' Eintrag in dag.py gefunden.")
    sys.exit(1)


def get_current_branch():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            check=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return None


def ensure_branch_has_remote(config):
    branch = get_current_branch()
    if not branch:
        print("❌  Aktuellen Branch konnte nicht ermittelt werden.")
        sys.exit(1)

    branch_section = f'branch "{branch}"'
    if branch_section in config and config[branch_section].get("remote"):
        return config[branch_section].get("remote")

    # Kein Remote gesetzt – versuche automatisch zu setzen
    print(
        f"⚠️  Kein Remote für Branch '{branch}' konfiguriert. Setze 'origin' als Remote..."
    )
    try:
        subprocess.run(
            ["git", "branch", "--set-upstream-to", f"origin/{branch}"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("✅  Remote-Zuordnung erfolgreich gesetzt.")
        # Reload config nach Änderung
        config.read(GIT_CONFIG_PATH)
        return "origin"
    except subprocess.CalledProcessError as e:
        print(f"❌  Fehler beim Setzen des Remotes: {e.stderr.decode().strip()}")
        sys.exit(1)


def extract_repo_url(config, remote_name):
    remote_section = f'remote "{remote_name}"'
    if remote_section not in config:
        print(f"❌  Remote '{remote_name}' nicht in .git/config gefunden.")
        sys.exit(1)
    return config[remote_section]["url"]


def extract_repo_name_from_url(url):
    match = re.search(r"/([^/]+?)(\.git)?$", url)
    if not match:
        print(f"❌  Konnte Repository-Namen aus URL '{url}' nicht extrahieren.")
        sys.exit(1)
    return match.group(1)


def is_valid_repo_name(name):
    return re.fullmatch(r"[a-z0-9_]+", name) is not None


def fix_dag_name(new_name, line_number, prefix, suffix):
    with DAG_PATH.open(encoding="utf-8") as f:
        lines = f.readlines()
    lines[line_number] = f"{prefix}{new_name}{suffix}\n"
    with DAG_PATH.open("w", encoding="utf-8") as f:
        f.writelines(lines)


def main():
    if not DAG_PATH.exists():
        print(f"❌  Datei {DAG_PATH} nicht gefunden.")
        return 1
    if not GIT_CONFIG_PATH.exists():
        print(f"❌  Datei {GIT_CONFIG_PATH} nicht gefunden.")
        return 1

    config = configparser.ConfigParser()
    config.read(GIT_CONFIG_PATH)

    remote_name = ensure_branch_has_remote(config)
    url = extract_repo_url(config, remote_name)
    repo_name = extract_repo_name_from_url(url)

    # Repo-Name nach Airflow-Konvention
    airflow_dag_name = repo_name.replace("-", "_").lower()

    if not is_valid_repo_name(airflow_dag_name):
        print(
            f"❌  Repository-Name '{airflow_dag_name}' ist nicht gültig (nur a-z, 0-9 und _ erlaubt)."
        )
        return 1

    line_number, prefix, dag_name_in_file, suffix = extract_dag_name_line()

    if dag_name_in_file != airflow_dag_name:
        print(
            f"⚠️  DAG-Name in dag.py ('{dag_name_in_file}') stimmt nicht mit Repo-Namen ('{airflow_dag_name}') überein."
        )
        fix_dag_name(airflow_dag_name, line_number, prefix, suffix)
        print(f"✅  DAG-Name in dag.py wurde korrigiert zu: {airflow_dag_name}")
    else:
        print("✅  DAG-Name in dag.py ist korrekt.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
