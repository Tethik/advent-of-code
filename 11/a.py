import sys
import itertools


class Ocotpus:
    def __init__(self, value) -> None:
        self.value = value
        self.links = set()
        self.flash_counter = 0
        self.last_flash_step = -1

    def charge(self, step):
        if self.last_flash_step == step:
            return
        self.value += 1
        if self.value > 9:
            self.flash(step)

    def link(self, octo):
        self.links.add(octo)

    def flash(self, step):
        if self.last_flash_step == step:
            return
        self.last_flash_step = step
        self.value = 0
        self.flash_counter += 1
        for octo in self.links:
            octo.charge(step)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)


def adjacent(y, x):
    return [(y-1, x), (y+1, x), (y, x-1), (y, x+1), (y-1, x-1), (y-1, x+1), (y+1, x-1), (y+1, x+1)]


def printGrid(grid):
    print()
    for y in range(len(grid)):
        s = ""
        for x in range(len(grid[y])):
            s += str(grid[y][x])
        print(s)
    print()


grid = []
for line in sys.stdin:
    row = []
    for c in line.strip():
        row.append(Ocotpus(int(c)))
    grid.append(row)

for y in range(len(grid)):
    for x in range(len(grid[y])):
        o = grid[y][x]
        for y1, x1 in adjacent(y, x):
            if y1 >= len(grid) or y1 < 0:
                continue
            if x1 >= len(grid[y1]) or x1 < 0:
                continue
            octo = grid[y1][x1]
            o.link(octo)


for step in range(100):
    printGrid(grid)
    for o in itertools.chain(*grid):
        o.charge(step)


print(sum(o.flash_counter for o in itertools.chain(*grid)))
