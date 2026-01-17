def update_fatigue(canon, event):
    weight = event.get("weight", 0.2)
    canon.fatigue = max(0.0, canon.fatigue + weight - 0.1)

def fatigue_blocked(canon):
    return canon.fatigue > 1.0