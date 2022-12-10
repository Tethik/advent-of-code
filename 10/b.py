import math
import sys
from pathlib import Path

program = []
for line in sys.stdin:
    program.append(line.strip())


class Pixel:
    def __init__(self) -> None:
        self.val = 1

    def __add__(self, v: int):
        self.val += v
        # self.show()
        return self

    def show(self):
        row = [c for c in "........................................"]
        for i in [self.val - 1, self.val, self.val + 1]:
            if i > -1 and i < len(row):
                row[i] = '#'
        print("".join(row))


class Cycle:
    def __init__(self, listener) -> None:
        self.val = 0
        self.listener = listener

    def __add__(self, v: int):
        for _ in range(v):
            self.listener(self.val)
            self.val += 1
            print(self.val)
        return self


x = Pixel()

image = ""


def crt(cycle):
    global image, x

    pos = cycle % 40
    if cycle > 0 and pos == 0:
        image += "\n"

    x.show()
    print(pos, [x.val-1, x.val, x.val+1])
    if pos in [x.val-1, x.val, x.val+1]:
        pixel = '#'
    else:
        pixel = '.'
    image += pixel
    print()
    print(image)
    print()


cycle = Cycle(crt)

current_inst = program.pop()
while program:
    inst = program.pop(0)

    cycle += 1

    if inst != "noop":
        cycle += 1
        x += int(inst.split(" ")[1])

print()


print(image)
print()
