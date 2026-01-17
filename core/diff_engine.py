def diff_canons(a, b):
    return {
        "events_added": [e for e in b.events if e not in a.events],
        "events_removed": [e for e in a.events if e not in b.events],
        "rules_added": [r for r in b.rules if r not in a.rules],
        "rules_removed": [r for r in a.rules if r not in b.rules],
        "truth_delta": {
            k: (a.truths.get(k), b.truths.get(k))
            for k in set(a.truths) | set(b.truths)
            if a.truths.get(k) != b.truths.get(k)
        },
        "integrity_delta": (
            a.integrity if hasattr(a, "integrity") else {},
            b.integrity if hasattr(b, "integrity") else {},
        )
    }