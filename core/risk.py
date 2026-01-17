def estimate_risk(canon, event):
    risk = 0.0
    if event.get("severity") == "irreversible":
        risk += 0.4
    if canon.integrity.get("consistency", 1.0) < 0.7:
        risk += 0.3
    if canon.fatigue > 0.8:
        risk += 0.3

    if risk < 0.3:
        return "safe"
    if risk < 0.7:
        return "risky"
    return "catastrophic"