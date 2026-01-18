from core.snapshot import take_snapshot
from core.integrity import compute_integrity
from core.dependency_graph import DependencyGraph
from core.rule_decay import decay_rules
from core.config import SAVE_POLICY
from core.project_store import load_canon, save_canon

class Canon:
    def __init__(self):
        # ---------------- CORE (REQUIRED) ----------------
        self.meta = {
            "title": "",
            "author": "",
            "version": "0.1"
        }
        self.truths = {}
        self.rules = []
        self.events = []

        # ---------------- ADVANCED / OPTIONAL ----------------
        self.event_log = []
        self.snapshots = []
        self.integrity = {}
        self.active_branch = "main"
        self.graph = DependencyGraph()

        # future-safe optional systems (already discussed)
        self.intent_log = []
        self.characters = {}
        self.fatigue = 0.0
        self.telemetry = {}

    # ---------------- RULES ----------------

    def add_rule(self, rule):
        rule.setdefault("strength", 1.0)
        rule.setdefault("overridden", False)
        self.rules.append(rule)

    # ---------------- EVENTS ----------------

    def add_event(self, event):
        self.events.append(event)

        # postconditions
        self.apply_postconditions(event)

        # snapshots & integrity (optional but live)
        try:
            self.snapshots.append(take_snapshot(self, event.get("act", 0)))
            self.integrity = compute_integrity(self)
        except Exception:
            pass  # never block event creation

        # rule decay
        try:
            decay_rules(self)
        except Exception:
            pass

        # dependency graph
        for dep in event.get("depends_on", []):
            self.graph.add_dependency(event["id"], dep)

    def apply_postconditions(self, event):
        for t in event.get("postconditions", []):
            self.truths[t] = True

    # ---------------- LOGGING ----------------

    def log_event(self, entry):
        entry["branch_id"] = self.active_branch
        self.event_log.append(entry)

    # ---------------- SERIALIZATION ----------------

    def to_dict(self):
        """
        NOTHING here is mandatory except core canon.
        SAVE_POLICY controls what extras persist.
        """

        data = {
            "meta": self.meta,
            "truths": self.truths,
            "rules": self.rules,
            "events": self.events,
        }

        if SAVE_POLICY.get("event_log"):
            data["event_log"] = self.event_log

        if SAVE_POLICY.get("snapshots"):
            data["snapshots"] = self.snapshots

        if SAVE_POLICY.get("integrity"):
            data["integrity"] = self.integrity

        if SAVE_POLICY.get("branches"):
            data["branch"] = self.active_branch

        if SAVE_POLICY.get("dependencies"):
            data["dependencies"] = self.graph.to_dict()

        if SAVE_POLICY.get("characters"):
            data["characters"] = self.characters

        if SAVE_POLICY.get("fatigue"):
            data["fatigue"] = self.fatigue

        if SAVE_POLICY.get("telemetry"):
            data["telemetry"] = self.telemetry

        return data

# ---- UI ADAPTER ----

# Simple global canon instance for UI usage
_CANON_INSTANCE = None


def get_canon():
    """
    Returns the active Canon instance (singleton).
    """
    global _CANON_INSTANCE
    if _CANON_INSTANCE is None:
        _CANON_INSTANCE = load_canon()
    return _CANON_INSTANCE


def save_current_canon():
    """
    Persists the active Canon instance to disk.
    """
    global _CANON_INSTANCE
    if _CANON_INSTANCE is not None:
        save_canon(_CANON_INSTANCE)