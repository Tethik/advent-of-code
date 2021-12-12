import sys
from collections import Counter


class Node:
    def __init__(self, val: str) -> None:
        self.neighbours = []
        self.val = val

    def issmall(self):
        return self.val.islower()

    def connect(self, node):
        if node.val != "start":
            self.neighbours.append(node)

    def __str__(self) -> str:
        return self.val


class Path:
    def __init__(self, path=[], smallc=0) -> None:
        self.path = path
        self.smallc = smallc

    def finished(self):
        return self.path[-1].val == "end"

    def next(self):
        for neigh in self.path[-1].neighbours:
            # a single small cave can be visited at most twice, and the remaining small caves can be visited at most once
            if neigh.issmall():
                small_visits = Counter(
                    filter(str.islower, [n.val for n in self.path]))

                # This could be optimized easily, but no need :)
                if len(small_visits) > 0:
                    has_visited_twice = small_visits.most_common()[0][1] > 1
                    neigh_visits = small_visits.get(neigh.val) or 0
                    if (has_visited_twice and neigh_visits > 0) or neigh_visits > 1:
                        continue

            yield Path([*self.path, neigh])

    def __str__(self) -> str:
        return "-".join([str(n) for n in self.path])


nodes = dict()

for line in sys.stdin:
    a, b = line.strip().split("-")
    if a not in nodes:
        nodes[a] = Node(a)
    if b not in nodes:
        nodes[b] = Node(b)

    nodes[a].connect(nodes[b])
    nodes[b].connect(nodes[a])


q = [Path([nodes["start"]])]
c = 0
while q:
    path = q.pop()
    # print(path)
    # print(path.path[0].neighbours)
    # print()

    if path.finished():
        print(path)
        c += 1
        continue

    for next in path.next():
        q.append(next)

print(c)
