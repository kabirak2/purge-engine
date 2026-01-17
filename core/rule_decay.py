def decay_rules(canon, decay_rate=0.05):
    for rule in canon.rules:
        strength = rule.get("strength", 1.0)
        overridden = rule.get("overridden", False)

        if overridden:
            strength -= decay_rate

        rule["strength"] = max(0.0, strength)
