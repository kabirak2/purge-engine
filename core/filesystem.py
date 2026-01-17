import os
import json
import shutil

BASE_DIR = "projects"


def save_project(canon_dict):
    """
    Save canon to disk.

    Rules:
    - Project title is the ONLY required field
    - Advanced / optional systems are ignored if missing
    - Overwrites only if project title matches existing folder
    - Otherwise creates a forked version
    """

    meta = canon_dict.get("meta", {})
    title = meta.get("title")

    if not title:
        raise ValueError("Project title is required")

    os.makedirs(BASE_DIR, exist_ok=True)

    target_path = os.path.join(BASE_DIR, title)
    canon_path = os.path.join(target_path, "canon.json")

    # -------- sanitize canon (defensive, non-destructive) --------
    safe_canon = {
        "meta": canon_dict.get("meta", {}),
        "truths": canon_dict.get("truths", {}),
        "rules": canon_dict.get("rules", []),
        "events": canon_dict.get("events", []),
    }

    # copy any OPTIONAL keys if present (never required)
    for optional_key in (
        "event_log",
        "snapshots",
        "integrity",
        "branch",
        "dependencies",
        "characters",
        "fatigue",
        "telemetry",
    ):
        if optional_key in canon_dict:
            safe_canon[optional_key] = canon_dict[optional_key]

    # -------- Case 1: project does not exist --------
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        _write_canon(canon_path, safe_canon)
        return target_path, "created"

    # -------- Case 2: project exists → title match --------
    if os.path.exists(canon_path):
        try:
            with open(canon_path, "r") as f:
                existing = json.load(f)
        except Exception:
            existing = {}

        existing_title = existing.get("meta", {}).get("title")

        if existing_title == title:
            _backup(canon_path)
            _write_canon(canon_path, safe_canon)
            return target_path, "overwritten"

    # -------- Case 3: mismatch → fork --------
    versioned_path = _next_available_path(title)
    os.makedirs(versioned_path)
    _write_canon(os.path.join(versioned_path, "canon.json"), safe_canon)

    return versioned_path, "forked"


# ---------------- helpers ----------------

def _write_canon(path, canon_dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(canon_dict, f, indent=2)


def _backup(path):
    backup_path = path + ".bak"
    try:
        shutil.copy(path, backup_path)
    except Exception:
        pass  # backups must never block saving


def _next_available_path(title):
    i = 2
    while True:
        candidate = f"{title}_v{i}"
        path = os.path.join(BASE_DIR, candidate)
        if not os.path.exists(path):
            return path
        i += 1
