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
