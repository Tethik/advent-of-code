import re
import sys
from functools import lru_cache
from queue import PriorityQueue, Queue
from typing import List


mixer = []
for line in sys.stdin:
    mixer.append(int(line.strip()))


# class LinkedNode:
#     def __init__(self, val) -> None:
#         self.val = val

#     def shift(self, steps) -> None:
#         pass


message = mixer.copy()
print(mixer.index(0))
print(message)
print()

for i in range(len(mixer)):
    mi = i % len(mixer)

    shift_by = mixer[mi]

    idx = message.index(shift_by)  # O(n) probably
    new_idx = (idx + shift_by)

    if shift_by > 0:
        # compensate for being inserted *before*, whereas we actually want after.
        new_idx += 1

    new_idx = new_idx % len(message)

    if new_idx == 0 and shift_by < 0:
        new_idx = len(message)

    # inserts *before* idx
    message.insert(new_idx, shift_by)

    # delete old idx
    if new_idx < idx:
        del message[idx+1]
    else:
        del message[idx]
    # print(message)
    # print()

print(message)
zpos = message.index(0)
a = message[(zpos + 1000) % len(message)]
b = message[(zpos + 2000) % len(message)]
c = message[(zpos + 3000) % len(message)]

print(a, b, c)
print(sum([a, b, c]))
