FEATURE_FLAGS = {
    "diff_engine": True,
    "intent_tracking": True,
    "fatigue_model": True,
    "character_state": True,
    "risk_estimator": True,
    "canon_repair": True,
    "telemetry": True,
    "simulation": True,
}

# What is persisted when saving a project
SAVE_POLICY = {
    "events": True,
    "rules": True,
    "truths": True,

    # OPTIONAL / NON-MANDATORY
    "event_log": False,
    "snapshots": False,
    "analytics": False,
    "telemetry": False,
    "character_states": False,
    "fatigue": False,
}