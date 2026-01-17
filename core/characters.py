class CharacterState:
    def __init__(self, name):
        self.name = name
        self.alive = True
        self.trust = {}
        self.trauma = 0
        self.arc_phase = "setup"

def apply_event_to_character(char, event):
    if event.get("kills") == char.name:
        char.alive = False
        char.arc_phase = "terminated"
