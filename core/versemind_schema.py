def validate_proposal_schema(p):
    if not isinstance(p, dict):
        return False

    required = {"type", "payload", "explanation", "confidence"}
    if not required.issubset(p.keys()):
        return False

    if p["type"] not in {"event", "rule", "suggestion"}:
        return False

    if not isinstance(p["confidence"], (int, float)):
        return False

    return True
