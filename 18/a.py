import sys
from typing import List


class Voxel:
    def __init__(self, x, y, z) -> None:
        self.x: int = x
        self.y: int = y
        self.z: int = z

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


seen = set()
for line in sys.stdin:
    v = Voxel(*[int(c) for c in line.strip().split(",")])
    print(v)
    seen.add(v)

# surface = set()
exposed = 0
for voxel in seen:
    for side in voxel.sides():
        if side not in seen:
            exposed += 1
            # surface.add(side)


print(exposed)
