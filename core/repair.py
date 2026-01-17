def suggest_repairs(paradoxes):
    suggestions = []
    for p in paradoxes:
        if p["type"] == "missing_precondition":
            suggestions.append(
                f"Add foreshadowing event before {p['event_id']}"
            )
    return suggestions