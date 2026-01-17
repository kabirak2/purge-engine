class DependencyGraph:
    def __init__(self):
        self.edges = {}  # event_id -> set(event_ids)

    def add_dependency(self, event_id, depends_on):
        self.edges.setdefault(event_id, set()).add(depends_on)

    def causes(self, event_id):
        return self.edges.get(event_id, set())

    def to_dict(self):
        return {k: list(v) for k, v in self.edges.items()}
