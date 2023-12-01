import re
import sys
from collections import namedtuple
from pathlib import Path
import os


karta = []
visible = []

for line in sys.stdin:
    karta.append([int(c) for c in line.strip()])
    visible.append([0 for _ in line.strip()])

for y in range(0, len(karta)):
    visible[y][0] = 1
    visible[y][len(karta[y]) - 1] = 1

for x in range(0, len(karta)):
    visible[0][x] = 1
    visible[len(karta) - 1][x] = 1

for y in range(0, len(karta)):
    print("col", y)

    # Left
    m = -1
    print("left")
    for x in range(len(karta[y])):
        v = karta[y][x]
        if v > m:
            m = v
            visible[y][x] = 1
        print(v, m, visible[y][x])

    # Right
    m = -1
    print("right")
    for x in range(len(karta[y])-1, 0, -1):
        v = karta[y][x]
        if v > m:
            m = v
            visible[y][x] = 1
        print(v, m, visible[y][x], x, y)
    print()

for x in range(0, len(karta[0])):
    print("row", y)

    # Down
    m = -1
    for y in range(len(karta)):
        v = karta[y][x]
        if v > m:
            m = v
            visible[y][x] = 1
        print(v, m, visible[y][x])

    # Up
    m = -1
    for y in range(len(karta) - 1, 0, -1):
        v = karta[y][x]
        if v > m:
            m = v
            visible[y][x] = 1
        print(v, m, visible[y][x])
    print()

c = 0
for y, row in enumerate(visible):
    c += sum(row)
    print(y, "  ", *row)

print(c)
