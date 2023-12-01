import sys
from typing import List


rocks = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""

movements = sys.stdin.readline().strip()


class Pos(object):
    def __init__(self, x, y) -> None:
        self.x: int = x
        self.y: int = y

    def __eq__(self, __o: object) -> bool:
        return __o.x == self.x and __o.y == self.y

    def __str__(self) -> str:
        return str((self.x, self.y))

    def __repr__(self) -> str:
        return str(self)

    def __sub__(self, o):
        return Pos(self.x - o.x, self.y - o.y)

    def __add__(self, o):
        return Pos(self.x + o.x, self.y + o.y)

    def __hash__(self) -> int:
        return (self.x, self.y).__hash__()


class Shape(object):
    def __init__(self, blocks: List[Pos]) -> None:
        self.blocks: List[Pos] = blocks
        self.left: int = min(p.x for p in blocks)
        self.right: int = max(p.x for p in blocks)
        self.top: int = max(p.y for p in blocks)
        self.bottom: int = min(p.y for p in blocks)

    def copy(self):
        return Shape(self.blocks.copy())

    def gasMove(self, solids, movement: str):
        newblocks = []
        dir = Pos(1, 0) if movement == '>' else Pos(-1, 0)

        for block in self.blocks:
            b = block + dir
            if b in solids or b.x == 0 or b.x == width - 1:
                return
            newblocks.append(b)
        self.blocks = newblocks

    def moveDown(self, solids):
        newblocks = []
        for block in self.blocks:
            b = block - Pos(0, 1)
            if b in solids:
                print(block, b)
                return False
            newblocks.append(b)
        self.blocks = newblocks
        return True

    """
    Position is based on the bottom left coordinate of the shape
    """

    def setBottomLeftPos(self, bottomLeftPos: Pos):
        diff = bottomLeftPos - Pos(self.left, self.bottom)
        # print(diff)
        self.bottom += diff.y
        self.top += diff.y
        self.left += diff.x
        self.right += diff.x

        for i in range(len(self.blocks)):
            self.blocks[i] = self.blocks[i] + diff

    def __str__(self) -> str:
        s = ""
        for y in range(self.top, self.bottom-1, -1):
            for x in range(self.left, self.right+1):
                if Pos(x, y) in self.blocks:
                    s += "#"
                else:
                    s += "."
            s += "\n"
        return s


def printMap():
    s = ""
    for y in range(floor+6, 0, -1):
        s += "|"
        for x in range(1, width-1):
            p = Pos(x, y)
            if p in solids:
                s += "#"
            elif p in shape.blocks:
                s += '@'
            else:
                s += "."
        s += "|\n"
    s += '+' + '-'*(width-2) + '+'
    print()
    print(s)
    print()


rock_strs = rocks.split("\n\n")
shapes: List[Shape] = []
for rock_str in rock_strs:
    blocks = []
    lines = rock_str.split()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                p = Pos(x, len(lines) - y)
                blocks.append(p)

    # print(blocks)
    shape = Shape(blocks)
    shapes.append(shape)
    print()
    print(shape)

floor = 0
width = 9
solids = set()
for x in range(width):
    solids.add(Pos(x, floor))

times = 2022
mi = 0
for ri in range(times):
    print(ri)
    shape = shapes[ri % len(shapes)].copy()
    shape.setBottomLeftPos(Pos(3, floor + 4))
    # printMap()

    shape.gasMove(solids, movements[mi])
    mi = (mi + 1) % len(movements)
    # printMap()
    # Move down until collision
    while shape.moveDown(solids):
        # printMap()
        shape.gasMove(solids, movements[mi])
        mi = (mi + 1) % len(movements)
        # printMap()

    for block in shape.blocks:
        floor = max(block.y, floor)
        solids.add(block)

printMap()
print(floor)
print(mi)
