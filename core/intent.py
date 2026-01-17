def log_intent(canon, intent, outcome_event_id=None):
    canon.intent_log.append({
        "intent": intent,
        "outcome": outcome_event_id
    })