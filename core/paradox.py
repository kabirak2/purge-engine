def detect_paradoxes(canon):
    """
    Detects narrative paradoxes such as:
    - event preconditions not satisfied
    - postconditions contradicting existing truths
    """

    paradoxes = []

    truths = canon.truths.copy()

    for event in canon.events:
        for pre in event.get("preconditions", []):
            if not truths.get(pre, False):
                paradoxes.append({
                    "type": "missing_precondition",
                    "event_id": event["id"],
                    "condition": pre
                })

        for post in event.get("postconditions", []):
            if post in truths and truths[post] is False:
                paradoxes.append({
                    "type": "truth_contradiction",
                    "event_id": event["id"],
                    "truth": post
                })
            truths[post] = True

    return paradoxes