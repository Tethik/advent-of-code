import sys


class Node:
    def __init__(self, val: str) -> None:
        self.neighbours = []
        self.val = val

    def issmall(self):
        return self.val.islower()

    def connect(self, node):
        self.neighbours.append(node)

    def __str__(self) -> str:
        return self.val


class Path:
    def __init__(self, path=[]) -> None:
        self.path = path

    def finished(self):
        return self.path[-1].val == "end"

    def next(self):
        for neigh in self.path[-1].neighbours:
            if neigh.issmall() and neigh in self.path:
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
