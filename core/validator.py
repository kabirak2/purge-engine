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

# ---- UI ADAPTERS ----

def validate_state(canon=None):
    """
    UI-facing adapter.
    Performs a lightweight validation pass over the current canon state.
    """
    if canon is None:
        return {
            "status": "ok",
            "blocked": [],
            "warned": [],
            "message": "No canon state provided"
        }

    blocked = []
    warned = []

    # Validate each event against rules at its act
    for event in canon.events:
        result = validate_action(
            action={
                "type": "event",
                "value": event.get("name", "")
            },
            canon=canon,
            context={
                "act": event.get("act", 0)
            }
        )

        blocked.extend(result.get("blocked", []))
        warned.extend(result.get("warned", []))

    status = "ok"
    if blocked:
        status = "blocked"
    elif warned:
        status = "warning"

    return {
        "status": status,
        "blocked": blocked,
        "warned": warned
    }
