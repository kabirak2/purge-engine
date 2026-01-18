import json
import os

PROJECTS_DIR = "projects"
DEFAULT_PROJECT = "default.json"


def _project_path(name=DEFAULT_PROJECT):
    os.makedirs(PROJECTS_DIR, exist_ok=True)
    return os.path.join(PROJECTS_DIR, name)


def load_canon(project=DEFAULT_PROJECT):
    """
    Loads a Canon instance from disk.
    Local import is used to avoid circular imports.
    """
    from core.canon import Canon  # ← LOCAL import (important)

    path = _project_path(project)
    canon = Canon()

    if not os.path.exists(path):
        return canon

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    canon.meta = data.get("meta", canon.meta)
    canon.truths = data.get("truths", {})
    canon.rules = data.get("rules", [])
    canon.events = data.get("events", [])

    canon.event_log = data.get("event_log", [])
    canon.snapshots = data.get("snapshots", [])
    canon.integrity = data.get("integrity", {})
    canon.characters = data.get("characters", {})
    canon.fatigue = data.get("fatigue", 0.0)
    canon.telemetry = data.get("telemetry", {})

    return canon


def save_canon(canon, project=DEFAULT_PROJECT):
    """
    Saves Canon state to disk.
    """
    path = _project_path(project)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(canon.to_dict(), f, indent=2)
