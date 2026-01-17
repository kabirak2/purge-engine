import importlib
import sys
import os
import time

WATCHED_MODULES = [
    "core.validator",
    "core.axiom",
    "core.integrity",
    "core.snapshot",
    "core.replay",
    "core.rule_decay",
    "core.branching",
    "core.dependency_graph",
    "core.event_logger",
]

class HotReloadManager:
    def __init__(self, canon):
        self.canon = canon
        self.last_mtime = {}

    def scan(self):
        reloaded = []

        for name in WATCHED_MODULES:
            module = sys.modules.get(name)
            if not module or not hasattr(module, "__file__"):
                continue

            path = module.__file__
            if not path or not os.path.exists(path):
                continue

            mtime = os.path.getmtime(path)
            last = self.last_mtime.get(path)

            if last is None:
                self.last_mtime[path] = mtime
                continue

            if mtime > last:
                importlib.reload(module)
                self.last_mtime[path] = mtime
                reloaded.append(name)

        if reloaded:
            self.canon.log_event({
                "entry_type": "hot_reload",
                "source": "system",
                "action": {"type": "engine", "value": "hot_reload"},
                "payload": {"modules": reloaded},
                "commit": {"state_preserved": True}
            })

        return reloaded
