import sys
from collections import namedtuple
from pathlib import Path

snek = [[0, 0]] * 10

directions = {
    "R": [0, 1],
    "L": [0, -1],
    "U": [1, 0],
    "D": [-1, 0],
}


def arradd(vec, vec2):
    return [vec[i] + vec2[i] for i in range(len(vec))]


visited = set()
visited.add(tuple(snek[9]))
for line in sys.stdin:
    print("==", line.strip(), "==")
    dir, steps = line.split()
    steps = int(steps)

    # move
    for _ in range(steps):
        prev = None
        for i, segment in enumerate(snek):
            # print(segment)
            if i == 0:
                vec = directions[dir]
                snek[i] = arradd(segment, vec)
                prev = segment.copy()
                continue

            # for a in range(len(segment)):
            #     if isinstance(segment[a] - snek[i - 1][a], float):
            #         print("WTFFF")
            #         print(segment[a], snek[i - 1][a])
            #         print(segment[a] - snek[i - 1][a])
            #         sys.exit(1)
            v = [abs(segment[a] - snek[i - 1][a]) for a in range(len(segment))]

            if max(v) > 1:
                axisChanged = 0
                for a in v:
                    if a > 0:
                        axisChanged += 1

                if axisChanged == 1:
                    diff = [(snek[i - 1][a] - segment[a]) // abs(snek[i - 1]
                                                                 [a] - segment[a]) if val > 0 else 0 for a, val in enumerate(v)]
                    snek[i] = arradd(segment, diff)
                else:
                    diff = [(snek[i - 1][a] - segment[a]) // abs(snek[i - 1]
                                                                 [a] - segment[a]) for a in range(len(segment))]
                    snek[i] = arradd(segment, diff)
                    # elif sum(v) == 3:
                    #     snek[i] = arradd(segment, [c - 1 for c in v])
                    #     prev = segment.copy()

                prev = segment.copy()
                print(segment, snek[i - 1], v, sum(v), snek[i])

            if i == len(snek) - 1:
                visited.add(tuple(snek[i]))

        print()
        print(*snek, sep=" ")
        print()


print(len(visited))
