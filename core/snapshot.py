import hashlib
import json
from datetime import datetime

def truth_hash(truths):
    raw = json.dumps(truths, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()

def take_snapshot(canon, act):
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "act": act,
        "event_count": len(canon.events),
        "active_rules": [r["id"] for r in canon.rules],
        "truth_hash": truth_hash(canon.truths)
    }
