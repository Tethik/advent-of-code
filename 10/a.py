import math
import sys
from pathlib import Path

program = []
for line in sys.stdin:
    program.append(line.strip())


x = 1


class Cycle:
    def __init__(self, listener) -> None:
        self.val = 0
        self.listener = listener

    def __add__(self, v: int):
        for _ in range(v):
            self.val += 1
            if self.val % 20 == 0:
                self.emit(self.val * x)
        return self

    def emit(self, signal):
        self.listener(self.val, signal)


signals = []
cycle = Cycle(lambda cycle, signal: signals.append((cycle, signal)))

current_inst = program.pop()
while program:
    inst = program.pop(0)

    if inst == "noop":
        cycles = 1
    else:  # addx
        cycles = 2

    for _ in range(cycles):
        cycle += 1

    if inst != "noop":
        x += int(inst.split(" ")[1])

print(signals)

p = 0
for signal in signals:
    print(signal)
    if (signal[0] % 40) - 20 == 0 and signal[0] <= 220:
        print(">", signal[1])
        p += signal[1]

print(p)

# print(sum(filter(lambda signal: (signal[1] - 20) % 40 == 0, signals)))
