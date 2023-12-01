from collections import defaultdict
from functools import total_ordering
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
    best = 1337
    q = PriorityQueue()
    q.put((0, valve))
    seen = set()
    while not q.empty():
        l, n = q.get()

        seen.add(n)

        if l > best:
            continue

        if n == other and l < best:
            best = l
            continue

        for neigh in valves[n].connections:
            if neigh not in seen:
                q.put((l+1, neigh))

    return best


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

print("# Precomputing distance")
dist_matrix = defaultdict(lambda: dict())
for key in valves_with_value + ["AA"]:
    for neigh in valves_with_value:
        if neigh in dist_matrix[key]:
            continue
        d = dist(key, neigh)
        dist_matrix[key][neigh] = d
        dist_matrix[neigh][key] = d

    print(key, dist_matrix[key])

# Possible shortcuts:
# [open_valves] -> [steps, pressure_released]
# all(open_valves)


@total_ordering
class State:
    open = []
    steps = 0
    position = "AA"
    pressure = 0

    def __str__(self) -> str:
        return json.dumps({"open_valves": list(self.open), "steps": self.steps, "position": self.position, "pressure_released": self.pressure}, indent=4)

    def __lt__(self, other):
        return self.pressure < other.pressure


q = PriorityQueue()
q.put((0, State()))
best = 1337
# visited = dict()
fullcpm = sum(valves[v].flow for v in valves_with_value)

while not q.empty():
    _, state = q.get()

    cpm = sum(valves[v].flow for v in state.open)  # could memoize
    if len(state.open) == len(valves_with_value):
        val = state.pressure - (30 - state.steps) * cpm
        assert state.steps <= 30

        if val < best:
            print(state)
            print(val)
            best = val
        continue

    changed = 0
    for n in filter(lambda x: x not in state.open, valves_with_value):
        new_state = State()
        steps = dist_matrix[state.position][n] + 1
        new_state.steps = state.steps + steps
        if new_state.steps > 30:
            continue
        new_state.open = state.open + [n]
        new_state.pressure = state.pressure - cpm * steps
        new_state.position = n
        q.put((new_state.pressure, new_state))
        changed += 1

    # handle case where no valves could be opened due to time.
    if changed == 0:
        val = state.pressure - (30 - state.steps) * cpm
        if val < best:
            print(state)
            print(val)
            best = val


print()
print(best)
