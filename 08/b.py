import re
import sys
from collections import namedtuple
from pathlib import Path
import os
import math


karta = []
visible = []

for line in sys.stdin:
    karta.append([int(c) for c in line.strip()])
    visible.append([[] for _ in line.strip()])

for y in range(0, len(karta)):
    print("col", y)

    # Left
    print("left")
    for x in range(len(karta[y])):
        v = karta[y][x]

        scenic = 0
        for p in range(x-1, -1, -1):
            scenic += 1
            if karta[y][p] >= v:
                break
        visible[y][x] += [scenic]
        print(v, scenic)

    # Right
    m = -1
    print("right")
    for x in range(len(karta[y])-1, 0, -1):
        v = karta[y][x]

        scenic = 0
        for p in range(x+1, len(karta[y])):
            scenic += 1
            if karta[y][p] >= v:
                break
        visible[y][x] += [scenic]
        print(v, scenic)
    print()

for x in range(0, len(karta[0])):
    print("row", y)

    # Down
    m = -1
    for y in range(len(karta)):
        v = karta[y][x]

        scenic = 0
        for p in range(y-1, -1, -1):
            scenic += 1
            if karta[p][x] >= v:
                break
        visible[y][x] += [scenic]

        print(v, scenic)

    # Up
    m = -1
    for y in range(len(karta) - 1, 0, -1):
        v = karta[y][x]

        scenic = 0
        for p in range(y+1, len(karta)):
            scenic += 1
            if karta[p][x] >= v:
                break
        visible[y][x] += [scenic]

        print(v, scenic)
    print()


for y, row in enumerate(visible):
    # c += sum(row)
    print(y, "  ", *row)

print()
m = -1
for y, row in enumerate(visible):
    # c += sum(row)
    products = [math.prod(c) for c in row]
    print(y, "  ", *products)
    m = max(m, *products)


print()
print(m)
