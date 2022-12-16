from collections import defaultdict
from functools import total_ordering
import itertools
import sys
import re
import json
from queue import PriorityQueue

valvepatt = re.compile(
    "([A-Z]{2})")
flowpatt = re.compile(
    "flow rate=(\d+)")

valves = dict()


def dist(valve, other):
    best = [1]*(len(valves) + 1)
    q = PriorityQueue()
    q.put((0, [valve]))
    seen = set()
    while not q.empty():
        l, n = q.get()
        p = n[-1]

        seen.add(p)

        if l >= len(best) - 1:
            continue

        if p == other and l < len(best):
            best = n
            continue

        for neigh in valves[p].connections:
            if neigh not in seen:
                path = n + [neigh]
                q.put((len(path) - 1, path))
    return best[1:]


class Valve:
    connections = []  # list[str]
    flow = 0

    def __init__(self, connections, flow) -> None:
        self.connections = connections
        self.flow = flow


valves_with_value = []
for line in sys.stdin:
    parts = valvepatt.findall(line)

    connections = parts[1:]
    flow = int(flowpatt.findall(line)[0])
    valve = Valve(connections, flow)
    valves[parts[0]] = valve
    if flow > 0:
        valves_with_value.append(parts[0])

print("# Precomputing paths")
dist_matrix = defaultdict(lambda: dict())
for key in valves.keys():
    for neigh in valves.keys():
        if neigh == key:
            dist_matrix[key][neigh] = [key]
            continue

        if neigh in dist_matrix[key]:
            continue
        d = dist(key, neigh)
        dist_matrix[key][neigh] = d
        dist_matrix[neigh][key] = d[::-1]

    print(key, dist_matrix[key])

# Possible shortcuts:
# [open_valves] -> [steps, pressure_released]
# all(open_valves)


@total_ordering
class State:
    open = []
    steps = 0
    pos = "AA"
    epos = "AA"
    pressure = 0

    def __str__(self) -> str:
        return json.dumps({"open_valves": list(self.open), "steps": self.steps, "position": self.pos, "pressure_released": self.pressure}, indent=4)

    def __lt__(self, other):
        return self.pressure < other.pressure


def create_state(state, cpm, my_target, e_target):
    e_path = dist_matrix[state.pos].get(e_target)
    my_path = dist_matrix[state.pos].get(my_target)

    new_state = State()
    if e_path and my_path:
        steps = min(len(my_path), len(e_path)) + 1
    elif e_path:
        steps = len(e_path) + 1
    elif my_path:
        steps = len(my_path) + 1
    else:
        return None

    new_state.steps = state.steps + steps
    if new_state.steps > total_minutes:
        return None

    new_state.pressure = state.pressure - cpm * steps
    new_state.open = state.open.copy()

    # print(new_state.open, my_target, e_target)
    assert e_target not in new_state.open
    assert my_target not in new_state.open

    if my_path:
        if steps < len(my_path):
            new_state.pos = my_path[steps]
        else:
            new_state.open += [my_target]
            new_state.pos = my_target
    else:
        new_state.pos = state.pos

    if e_path:
        if steps < len(e_path):
            new_state.epos = e_path[steps]
        else:
            new_state.open += [e_target]
            new_state.epos = e_target
    else:
        new_state.epos = state.epos

    return new_state


total_minutes = 26
q = PriorityQueue()
q.put((0, State()))
best = 1337
# visited = dict()
fullcpm = sum(valves[v].flow for v in valves_with_value)

while not q.empty():
    _, state = q.get()

    cpm = sum(valves[v].flow for v in state.open)  # could memoize
    if len(state.open) == len(valves_with_value):
        val = state.pressure - (total_minutes - state.steps) * cpm
        assert state.steps <= total_minutes

        if val < best:
            print(state)
            print(val)
            best = val
        continue

    changed = 0
    still_to_open = list(
        filter(lambda x: x not in state.open, valves_with_value)) + [None]
    for n in itertools.combinations(still_to_open, 2):
        # print(n[0], n[1])
        new_state = create_state(state, cpm, n[0], n[1])
        if new_state:
            q.put((new_state.pressure, new_state))
            changed += 1

        new_state = create_state(state, cpm, n[1], n[0])
        if new_state:
            q.put((new_state.pressure, new_state))
            changed += 1

    # handle case where no valves could be opened due to time.
    if changed == 0:
        val = state.pressure - (total_minutes - state.steps) * cpm
        if val < best:
            print(state)
            print(val)
            best = val


print()
print(best)
