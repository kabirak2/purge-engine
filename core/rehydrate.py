def rehydrate_canon(canon, data):
    canon.meta = data.get("meta", canon.meta)
    canon.truths = data.get("truths", canon.truths)
    canon.rules = data.get("rules", canon.rules)
    canon.events = data.get("events", canon.events)
    canon.event_log = data.get("event_log", canon.event_log)
    canon.snapshots = data.get("snapshots", canon.snapshots)
    canon.integrity = data.get("integrity", canon.integrity)
