from collections import defaultdict
from functools import total_ordering
import functools
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
        dist_matrix[key][neigh] = d + [neigh]
        dist_matrix[neigh][key] = d[::-1][1:] + [key, key]

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
        return json.dumps({"open_valves": list(self.open), "steps": self.steps, "position": self.pos, "pressure": self.pressure}, indent=4)

    def __lt__(self, other):
        return self.pressure < other.pressure

    def estimate_max_expected_value(self):
        return self.pressure - (total_minutes - self.steps) * fullcpm

    def hashkey(self):
        return "-".join(str(o) for o in self.open)


def create_state(state, cpm, my_target, e_target):
    e_path = dist_matrix[state.epos].get(e_target)
    my_path = dist_matrix[state.pos].get(my_target)

    new_state = State()
    if e_path and my_path:
        steps = min(len(my_path), len(e_path))
    elif e_path:
        steps = len(e_path)
    elif my_path:
        steps = len(my_path)
    else:
        return None

    new_state.steps = state.steps + steps
    if new_state.steps > total_minutes:
        return None

    new_state.pressure = state.pressure - cpm * steps
    new_state.open = state.open.copy()

    # # print(new_state.open, my_target, e_target)
    # assert e_target not in new_state.open
    # assert my_target not in new_state.open

    # # print(e_path, my_path, steps)
    # assert not ((not e_path or steps < len(e_path))
    #             and (not my_path or steps < len(my_path)))

    opens = []

    if my_path:
        assert not steps > len(my_path)
        new_state.pos = my_path[steps - 1]
        if steps == len(my_path):
            opens.append(my_target)
    else:
        new_state.pos = state.pos

    if e_path:
        assert not steps > len(e_path)
        new_state.epos = e_path[steps - 1]
        if steps == len(e_path):
            opens.append(e_target)
    else:
        new_state.epos = state.epos

    for o in sorted(opens):
        new_state.open += [(o, new_state.epos, new_state.pos, new_state.steps)]
        #  new_state.steps,
        #                     new_state.pressure, new_state.epos, new_state.pos)]
        # , new_state.pressure, cpm)]

    return new_state


total_minutes = 26
q = PriorityQueue()
q.put((0, State()))
best = -1982  # 1337

visited = dict()
fullcpm = sum(
    sorted([valves[v].flow for v in valves_with_value], reverse=True)[:9])

print("Estimate CPM set to", fullcpm)
c = 0
skipped = 0
while not q.empty():
    _, state = q.get()

    if c % 10000 == 0:
        print(q.qsize(), skipped, state.hashkey())
    c += 1

    if state.estimate_max_expected_value() > best:
        continue

    opens = [o[0] for o in state.open]

    cpm = sum(valves[v].flow for v in opens)

    changed = 0
    still_to_open = list(
        filter(lambda x: x not in opens, valves_with_value)) + [None]
    for n in itertools.combinations(still_to_open, 2):
        new_state = create_state(state, cpm, n[0], n[1])
        if new_state and new_state.estimate_max_expected_value() < best:
            # hk = new_state.hashkey()
            # if hk in visited:
            #     skipped += 1
            #     # print(new_state.pressure, visited[hk], hk)
            #     assert new_state.pressure == visited[hk]

            # if not hk in visited:  # or visited[hk] > new_state.pressure:
            # visited[hk] = new_state.pressure
            # visited.add(hk)
            q.put((new_state.pressure, new_state))
            changed += 1

        new_state = create_state(state, cpm, n[1], n[0])
        if new_state and new_state.estimate_max_expected_value() < best:
            # hk = new_state.hashkey()

            # if hk in visited:
            #     skipped += 1
            #     # print(new_state.pressure, visited[hk])
            #     assert new_state.pressure == visited[hk]

            # if not hk in visited:  # or visited[hk] > new_state.pressure:
            #     visited[hk] = new_state.pressure
            # visited.add(hk)
            q.put((new_state.pressure, new_state))
            changed += 1

    # handle case where no valves could be opened due to time.
    if changed == 0:
        val = state.pressure - (total_minutes - state.steps) * cpm
        if val < best:
            print(changed, len(still_to_open))
            print(state)
            print(val)
            best = val


print()
print(best)
