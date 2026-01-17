from copy import deepcopy

def run_simulation(canon, events):
    sim = deepcopy(canon)
    for e in events:
        sim.add_event(e)
    return sim