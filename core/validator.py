def evaluate_condition(cond, context):
    if "all" in cond:
        return all(evaluate_condition(c, context) for c in cond["all"])
    return True

def validate_action(action, canon, context):
    blocked = []
    warned = []

    for rule in canon.rules:
        if not evaluate_condition(rule["conditions"], context):
            continue

        constraint = rule["constraint"]
        severity = rule.get("severity", "hard")

        if (
            constraint["type"] == "forbid"
            and constraint["target"] == action["type"]
            and constraint["value"] == action["value"]
        ):
            if severity == "hard":
                blocked.append(rule)
            else:
                warned.append(rule)

        if constraint["type"] == "limit":
            window = rule.get("temporal", {})
            acts = window.get("acts")
            max_events = window.get("max")

            if acts and max_events:
                recent = [
                    e for e in canon.events
                    if abs(e["act"] - context["act"]) <= acts
                ]
                if len(recent) >= max_events:
                    if severity == "hard":
                        blocked.append(rule)
                    else:
                        warned.append(rule)

    return {
        "blocked": blocked,
        "warned": warned
    }
