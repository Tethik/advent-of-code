import sys
from queue import PriorityQueue
from collections import namedtuple
from pathfinding import paths


def pad(m):
    m[-1].strip()
    width = len(m[0])
    return list(map(lambda r: r.ljust(width), m))


_input = sys.stdin.readlines()
_input = pad(_input)
_map = []

with open("final") as fp:
    final = fp.readlines()
    final = pad(final)
    final = "".join(final)


energy = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

Amphipod = namedtuple("Amphipod", ["type", "steps", "y", "x"])

# 1. Amphipods will never stop on the space immediately outside any room.
# 2. Amphipods will never move from the hallway into a room unless that room is their destination room and that room contains no amphipods which do not also have that room as their own destination
# 3. Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room.


def in_hallway(y, x):
    return y == 1


dest_room_x = {
    "A": 3,
    "B": 5,
    "C": 7,
    "D": 9
}


def in_dest_room(t, y, x):
    return y in [2, 3] and dest_room_x.get(t) == x


spaces_outside_room = set([(1, x) for x in dest_room_x.values()])


class State:

    def __init__(self, cost=0, amphis=[]) -> None:
        self.cost = cost
        self.amphis = amphis
        self.amphis_d = None

    def __str__(self) -> str:
        s = _map.copy()
        for t, steps, y, x in self.amphis:
            s[y] = s[y][:x] + t + s[y][x+1:]
        return "".join(s)

    def get(self, y, x):
        if not self.amphis_d:
            self.amphis_d = dict(map(lambda a: ((a.y, a.x), a), self.amphis))

        if y >= len(_map) or x >= len(_map[y]):
            return "#"
        if self.amphis_d.get((y, x)):
            return self.amphis_d.get((y, x)).type
        return _map[y][x]

    def next(self, height, width):
        for i, a in enumerate(self.amphis):
            t, s, y, x = a
            if s > 1:
                continue

            if in_dest_room(t, y, x):  # already in place?
                if self.get(3, x) == t:  # avoid blocking in an amphipod
                    continue

            p = paths(height, width, self, (y, x))

            # Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room.
            if in_hallway(y, x):
                # print("in hallway")
                for dest, t2 in p.items():
                    cost, _ = t2
                    if in_dest_room(t, dest[0], dest[1]):
                        # avoid blocking in an amphipod / also doesn't make sense to leave an empty space below
                        if dest[0] == 2 and self.get(3, dest[1]) != t:
                            continue
                        am = self.amphis.copy()
                        am[i] = Amphipod(t, s+1, *dest)
                        yield State(self.cost + cost * energy.get(t), am)
            else:  # Otherwise in start room
                for dest, t2 in p.items():
                    cost, _ = t2
                    if in_hallway(*dest) and dest not in spaces_outside_room:
                        am = self.amphis.copy()
                        am[i] = Amphipod(t, s+1, *dest)
                        yield State(self.cost + cost * energy.get(t), am)

    def __eq__(self, other):
        return other.cost == self.cost

    def __lt__(self, other):
        return self.cost - other.cost


height, width = len(_input), len(_input[0])

amphis = []
for y in range(height):
    r = ""
    for x in range(width):
        c = _input[y][x]
        if c in ["A", "B", "C", "D"]:
            r += "."
            amphis.append(Amphipod(c, 0, y, x))
        else:
            r += c
    _map.append(r)
initial_state = State(0, amphis)
initial_state.amphis = sorted(
    initial_state.amphis, key=lambda a: energy.get(a.type))
# print(initial_state)
# print(final)
# print(str(initial_state) == final)

# for a in initial_state.amphis:
#     d = paths(height, width, initial_state, (a.y, a.x))
#     print(d)

Q = PriorityQueue()
Q.put((0, initial_state))

visited = set()


def hash(state):
    s = ""
    for amphi in state.amphis:
        s += str(amphi.y) + "-" + str(amphi.x) + ","
    return s


while not Q.empty():
    _, state = Q.get()

    h = hash(state)
    if h in visited:
        continue
    visited.add(h)

    # print(state)
    print(state.cost)
    # # print(state.amphis)
    # print()

    if all(in_dest_room(a.type, a.y, a.x) for a in state.amphis):
        print("Finished")
        print(state)
        print(state.cost)
        break

    for ns in state.next(height, width):
        # print(ns, ns.cost)
        # Q.put((steps+1, ns))
        if hash(ns) in visited:
            continue
        Q.put((ns.cost, ns))
