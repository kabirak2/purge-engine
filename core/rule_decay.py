def decay_rules(canon, decay_rate=0.05):
    for rule in canon.rules:
        strength = rule.get("strength", 1.0)
        overridden = rule.get("overridden", False)

        if overridden:
            strength -= decay_rate

        rule["strength"] = max(0.0, strength)

# ---- UI ADAPTERS ----

def list_rules(canon=None):
    """
    UI-facing adapter.
    Returns a list of rules.
    """
    if canon is None:
        return []
    return canon.rules


def update_rule(rule_id, new_text, canon=None):
    """
    UI-facing adapter.
    Updates a rule's definition or description.
    """
    if canon is None:
        return False

    for rule in canon.rules:
        if rule.get("id") == rule_id:
            rule["text"] = new_text
            rule["overridden"] = True
            return True

    return False
