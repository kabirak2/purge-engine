from copy import deepcopy

def merge_branches(base_canon, branch_canon):
    """
    Merge branch_canon into base_canon.
    Conflicts are resolved by:
    - keeping base truths unless branch introduces new ones
    - appending non-duplicate events
    - appending non-duplicate rules
    """

    merged = deepcopy(base_canon)

    # Merge truths
    for k, v in branch_canon.truths.items():
        if k not in merged.truths:
            merged.truths[k] = v

    # Merge rules
    base_rule_ids = {r["id"] for r in merged.rules}
    for r in branch_canon.rules:
        if r["id"] not in base_rule_ids:
            merged.rules.append(r)

    # Merge events
    base_event_ids = {e["id"] for e in merged.events}
    for e in branch_canon.events:
        if e["id"] not in base_event_ids:
            merged.events.append(e)

    merged.log_event({
        "entry_type": "branch_merge",
        "source": "system",
        "payload": {
            "from_branch": branch_canon.active_branch,
            "to_branch": base_canon.active_branch
        }
    })

    return merged