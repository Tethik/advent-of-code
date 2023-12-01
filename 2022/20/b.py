import re
import sys
from functools import lru_cache
from queue import PriorityQueue, Queue
from typing import Dict, List

mixer = []
decryption_key = 811589153
for line in sys.stdin:
    mixer.append(int(line.strip()) * decryption_key)


class LinkedNode:
    def __init__(self, val, original_idx) -> None:
        self.val = val
        self.original_idx = original_idx

    def shift(self, steps) -> None:
        steps = steps % (len(mixer) - 1)

        while steps > 0:
            # Connect left
            self.left.right = self.right
            self.right.left = self.left
            self.left = self.right

            # Connect right
            new_right = self.right.right
            self.right.right = self
            self.right = new_right
            new_right.left = self

            steps -= 1

        while steps < 0:
            # Connect right
            self.right.left = self.left
            self.left.right = self.right
            self.right = self.left

            # Connect left
            new_left = self.left.left
            self.left.left = self
            self.left = new_left
            new_left.right = self

            steps += 1

        return self.left.val, self.right.val

    def index(self, steps):
        n = self
        for _ in range(steps):
            n = n.right
        return n


def vals(n: LinkedNode):
    vals = []
    for _ in range(len(mixer)):
        vals.append(n.val)
        n = n.right
    return vals


def printList(n: LinkedNode):
    print(vals(n))


first = None
prev = None
zeroNode = None
lookup: Dict[int, LinkedNode] = dict()
for i in range(len(mixer)):
    node = LinkedNode(mixer[i], i)
    node.left = prev
    if not first:
        first = node
    if prev:
        prev.right = node
    if node.val == 0:
        zeroNode = node
    prev = node
    lookup[i] = node
first.left = prev
prev.right = first

# printList(first)
# print()

for _ in range(10):
    for i in range(len(mixer)):
        mix = mixer[i]
        node = lookup[i]
        assert node.val == mix
        nl, nr = node.shift(mix)

        print(node.val, "moves between", nl, "and", nr)

        # v = vals(first)
        # for m in mixer:
        #     assert m in v

        # printList(first)
        # print()


a = zeroNode.index(1000).val
b = zeroNode.index(2000).val
c = zeroNode.index(3000).val

print(a, b, c)
print(sum([a, b, c]))
