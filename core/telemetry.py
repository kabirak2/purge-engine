import json

def export_telemetry(canon):
    return {
        "event_count": len(canon.events),
        "rule_count": len(canon.rules),
        "integrity": canon.integrity,
        "fatigue": canon.fatigue,
    }