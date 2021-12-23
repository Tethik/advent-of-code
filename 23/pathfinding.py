from queue import PriorityQueue
from collections import defaultdict


def adjacent(height, width, y, x):
    if y > 0:
        yield (y-1, x)
    if y < height - 1:
        yield (y+1, x)
    if x > 0:
        yield (y, x-1)
    if x < width - 1:
        yield (y, x+1)


def paths(height, width, state, source):
    Q = PriorityQueue()
    inf = 1337133713371337
    prevdist = defaultdict(lambda: (inf, None))
    prevdist[source] = (0, None)
    # for y in range(height):
    #     for x in range(width):
    #         v = (y, x)
    #         if v != source:
    #             prevdist[v] = (inf, None)
    #         Q.put((inf, v))
    Q.put((0, source))

    visited = set()
    while not Q.empty():
        u = Q.get()[1]

        if u in visited:
            continue
        visited.add(u)

        for v in adjacent(height, width, *u):
            # check anything in the way
            if state.get(*v) != ".":
                continue

            alt = prevdist[u][0] + 1

            if v not in prevdist or alt < prevdist[v][0]:
                prevdist[v] = (alt, u)
                Q.put((alt, v))

    del prevdist[source]
    return prevdist

    # print(prevdist[end])
