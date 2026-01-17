import json
import os
from core.rehydrate import rehydrate_canon

def reload_project(canon, project_title):
    path = os.path.join("projects", project_title, "canon.json")

    if not os.path.exists(path):
        return False

    with open(path, "r") as f:
        data = json.load(f)

    rehydrate_canon(canon, data)
    return True
