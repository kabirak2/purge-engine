def compute_integrity(canon):
    total_events = len(canon.events)
    if total_events == 0:
        return {
            "consistency": 1.0,
            "pacing": 1.0,
            "rule_conflict": 0.0
        }

    irreversible = sum(
        1 for e in canon.events
        if e.get("severity") == "irreversible"
    )

    acts = [e["act"] for e in canon.events]
    density = total_events / max(acts)

    return {
        "consistency": max(0.0, 1.0 - irreversible * 0.15),
        "pacing": max(0.0, 1.0 - max(0, density - 4) * 0.1),
        "rule_conflict": min(1.0, irreversible * 0.1)
    }
