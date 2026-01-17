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
