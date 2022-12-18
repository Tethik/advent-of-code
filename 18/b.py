from functools import lru_cache
import sys
from typing import List


class Voxel:
    def __init__(self, x, y, z) -> None:
        self.x: int = x
        self.y: int = y
        self.z: int = z

    # @lru_cache(None)
    def sides(self):
        for c in [-1, 1]:
            yield Voxel(self.x + c, self.y, self.z)
            yield Voxel(self.x, self.y + c, self.z)
            yield Voxel(self.x, self.y, self.z + c)

    def __eq__(self, __o: object) -> bool:
        return __o.x == self.x and __o.y == self.y and __o.z == self.z

    def __str__(self) -> str:
        return str((self.x, self.y, self.z))

    def __repr__(self) -> str:
        return str(self)

    def __sub__(self, o):
        return Voxel(self.x - o.x, self.y - o.y, self.z - o.z)

    def __add__(self, o):
        return Voxel(self.x + o.x, self.y + o.y, self.z + o.z)

    def __hash__(self) -> int:
        return (self.x, self.y, self.z).__hash__()


blocks = set()
for line in sys.stdin:
    v = Voxel(*[int(c) for c in line.strip().split(",")])
    blocks.add(v)

air = set()
for voxel in blocks:
    for side in voxel.sides():
        if side not in blocks:
            air.add(side)

print(len(air))

bubbles = []
covered = set()
while len(air) > 0:
    voxel = air.pop()

    bubble = set()
    bubble.add(voxel)

    # Explore each pocket
    q = [(1, voxel)]
    while q:
        dc, vx = q.pop()
        sides = list(vx.sides())
        if side in air:
            air.remove(side)
        if dc > 10:
            continue

        if any(s in blocks for s in sides):
            dc = 1
        else:
            dc += 1

        for side in sides:
            if side in blocks:
                continue

            if side not in bubble:
                bubble.add(side)
                q.append((dc, side))

                if side in air:
                    air.remove(side)

    bubbles.append(bubble)

print("# Joining bubbles..")
for i in range(len(bubbles)):
    joined = []
    for j in range(i+1, len(bubbles)):
        if any(v in bubbles[j] for v in bubbles[i]):
            bubbles[i] = bubbles[i] | bubbles[j]
            joined.append(j)
            continue

    for j in joined[::-1]:
        del bubbles[j]


surfaces = []
print("# Calculating surfaces..")
for bubble in bubbles:
    print(len(bubble))
    exposed = 0
    for voxel in bubble:
        for b2 in bubbles:
            if b2 == bubble:
                continue
            if voxel in b2:
                print("wat", voxel, len(b2), len(bubble))
                sys.exit(1)
        for side in voxel.sides():
            if side in blocks:
                exposed += 1
    surfaces.append(exposed)

print(sorted(surfaces))
