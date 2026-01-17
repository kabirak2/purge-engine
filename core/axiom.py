import uuid

ALLOWED_CONSTRAINTS = ["forbid", "require", "limit"]

def new_rule():
    return {
        "id": f"rule_{uuid.uuid4().hex[:8]}",
        "scope": "global",
        "conditions": {"all": []},
        "constraint": {
            "type": "forbid",
            "target": "event",
            "value": ""
        },
        "temporal": {
            "acts": None,
            "max": None
        },
        "reason": "",
        "severity": "hard",  # hard | soft
        "metadata": {
            "created_by": "human"
        }
    }

def validate_rule(rule):
    if not rule["reason"]:
        raise ValueError("Rule must have a reason")
    if rule["constraint"]["type"] not in ALLOWED_CONSTRAINTS:
        raise ValueError("Invalid constraint type")
    return True
