from copy import deepcopy

def replay_until(canon, log_id):
    new_canon = deepcopy(canon)
    new_canon.events = []
    new_canon.truths = {}
    new_canon.snapshots = []

    for entry in canon.event_log:
        if entry["log_id"] == log_id:
            break

        if entry["commit"].get("written_to_canon"):
            payload = entry.get("payload")
            if payload and "act" in payload:
                new_canon.add_event(payload)

    return new_canon

# ---- UI ADAPTER ----

def replay_last(canon=None):
    """
    UI-facing adapter.
    Replays canon up to the most recent log entry.
    """
    if canon is None:
        return "No canon state provided"

    if not hasattr(canon, "event_log") or not canon.event_log:
        return "No event log available"

    last_log = canon.event_log[-1]
    log_id = last_log.get("log_id")

    if log_id is None:
        return "Invalid log entry"

    new_canon = replay_until(canon, log_id)
    return {
        "replayed_until": log_id,
        "event_count": len(new_canon.events),
        "truth_count": len(new_canon.truths),
    }
