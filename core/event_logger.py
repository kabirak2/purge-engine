import uuid
from datetime import datetime

def log_event(
    canon,
    entry_type,
    source,
    action,
    payload=None,
    context=None,
    validation=None,
    commit=None,
    caused_by=None
):
    entry = {
        "log_id": f"log_{uuid.uuid4().hex[:6]}",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "entry_type": entry_type,
        "source": source,
        "action": action,
        "payload": payload or {},
        "context": context or {},
        "validation": validation or {},
        "commit": commit or {},
        "caused_by": caused_by or [],
        "branch_id": canon.active_branch
    }
    canon.log_event(entry)
    return entry
