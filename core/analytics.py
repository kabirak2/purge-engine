def narrative_analytics(canon):
    """
    Returns high-level narrative metrics
    """

    acts = {}
    severities = {"minor": 0, "major": 0, "irreversible": 0}

    for e in canon.events:
        acts.setdefault(e["act"], 0)
        acts[e["act"]] += 1
        sev = e.get("severity", "minor")
        severities[sev] += 1

    return {
        "total_events": len(canon.events),
        "events_per_act": acts,
        "severity_distribution": severities,
        "rule_count": len(canon.rules),
        "truth_count": len(canon.truths),
    }

# ---- UI ADAPTER ----

def get_metrics(canon=None):
    """
    UI-facing adapter.
    Returns narrative analytics in a UI-safe format.
    """
    if canon is None:
        return {
            "total_events": 0,
            "events_per_act": {},
            "severity_distribution": {},
            "rule_count": 0,
            "truth_count": 0,
        }

    return narrative_analytics(canon)
