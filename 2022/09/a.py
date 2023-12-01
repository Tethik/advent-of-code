import sys
from collections import namedtuple
from pathlib import Path

head = [0, 0]
tail = [0, 0]

directions = {
    "R": [0, 1],
    "L": [0, -1],
    "U": [1, 0],
    "D": [-1, 0],
}


def arrmul(vec, m):
    return [i*m for i in vec]


def arradd(vec, vec2):
    return [vec[i] + vec2[i] for i in range(len(vec))]


def specialdist(vec, vec2):
    return max(abs(vec[i] - vec2[i]) for i in range(len(vec)))


visited = set()
visited.add(tuple(tail))
for line in sys.stdin:
    dir, steps = line.split()
    steps = int(steps)

    # move
    for _ in range(steps):
        prevhead = head.copy()
        vec = directions[dir]
        head = arradd(head, vec)
        if head == tail or specialdist(head, tail) <= 1:
            continue
        tail = prevhead
        visited.add(tuple(tail))

    print(head, tail)


print(len(visited))
