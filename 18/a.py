import sys
import json


class Node:
    left = None
    right = None
    parent = None

    def __init__(self, parent, left, right) -> None:
        self.parent = parent
        if isinstance(left, list):
            print(left)
            self.left = Node(self, *left)
        else:
            self.left = left
        if isinstance(right, list):
            self.right = Node(self, *right)
        else:
            self.right = right

    def __iter__(self):
        yield from [self.parent, self.left, self.right]

    def __str__(self) -> str:
        return f"[{self.left},{self.right}]"

    def __repr__(self) -> str:
        return str(self)

    def plain(self) -> bool:
        return not isinstance(self.left, list) and not isinstance(self.right, list)

    def add(self, node):  # __add__
        p = Node(None, self, node)
        self.parent = p
        node.parent = p
        return p

    def __eq__(self, __o: object) -> bool:
        return str(self) == str(__o)  # lazy but should work


"""
    If any pair is nested inside four pairs, the leftmost such pair explodes.
    If any regular number is 10 or greater, the leftmost such regular number splits.

    To explode a pair, the pair's left value is added to the first regular number to the left of the
    exploding pair (if any), and the pair's right value is added to the first regular number to the
    right of the exploding pair (if any).

    >Exploding pairs will always consist of two regular numbers.

    Then, the entire exploding pair is replaced with the regular number 0.
"""


def explode(snailfish):

    def leftmost(f, depth=0):
        if isinstance(f, int):
            return None
        if depth >= 4 and f.plain():
            return f
        return leftmost(f.left, depth+1) or leftmost(f.right, depth+1)

    fish_due_for_exploding = leftmost(snailfish)
    # print(fish_due_for_exploding)

    # q = []
    # q.append((snailfish, 0))
    # while q:
    #     fish, depth = q.pop(-1)
    #     print(depth, fish)
    #     print(fish.left, fish.right)
    #     print()

    #     # if depth > 4, and we can keep going down, do we exlode now or further down?
    #     # "If any pair is nested inside four pairs, the leftmost such pair explodes." what if nested deeper?
    #     # "Exploding pairs will always consist of two regular numbers." Aha ok
    #     if fish.plain() and depth >= 4:
    #         fish_due_for_exploding = fish
    #         break

    #     if isinstance(fish.right, Node):
    #         q.append((fish.right, depth+1))
    #     if isinstance(fish.left, Node):
    #         q.append((fish.left, depth+1))

    if fish_due_for_exploding == None:
        return None

    # Exploding time!

    # Go right, traverse up until no longer rightmost, then take leftmost
    p = fish_due_for_exploding.parent
    n = fish_due_for_exploding
    while p != None and p.right == n:
        n = p
        p = p.parent

    if p != None:
        if isinstance(p.right, int):
            p.right += fish_due_for_exploding.right
        else:
            n = p.right
            while isinstance(n.left, Node):
                n = n.left
            n.left += fish_due_for_exploding.right

    # Now the same for the left
    p = fish_due_for_exploding.parent
    n = fish_due_for_exploding
    while p != None and p.left == n:
        n = p
        p = p.parent

    if p != None:
        if isinstance(p.left, int):
            p.left += fish_due_for_exploding.left
        else:
            n = p.left
            while isinstance(n.right, Node):
                n = n.right
            n.right += fish_due_for_exploding.left

    # Finally, set zero
    if fish_due_for_exploding.parent.right == fish_due_for_exploding:
        fish_due_for_exploding.parent.right = 0
    else:
        fish_due_for_exploding.parent.left = 0

    return fish_due_for_exploding


testcases = [
    ([[[[[9, 8], 1], 2], 3], 4], [[[[0, 9], 2], 3], 4]),
    ([7, [6, [5, [4, [3, 2]]]]], [7, [6, [5, [7, 0]]]]),
    ([[6, [5, [4, [3, 2]]]], 1], [[6, [5, [7, 0]]], 3]),
    ([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]],
     [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]),
    ([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
     [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]),
    # my own testcases
    ([[1, [[[1, 2], 0], 0]], [[[[[3, 4], 0], 0], 0], 0]],
     [[2, [[0, 2], 0]], [[[[[3, 4], 0], 0], 0], 0]]),
    ([[1, [2, [3, [1, 1]]]], [[[[[3, 4], 0], 0], 0], 0]],
     [[1, [2, [4, 0]]], [[[[[4, 4], 0], 0], 0], 0]])
]
for t, a in testcases:
    n = Node(None, *t)
    print(f"Before   ", n)
    fish = explode(n)
    print(f"Exploding", fish)
    print(f"After    ", n)
    print(f"Expected ", a)
    assert str(n) == str(Node(None, *a))
    print()

""""
To split a regular number, replace it with a pair;
the left element of the pair should be the regular number divided by two and rounded down,
while the right element of the pair should be the regular number divided by two and rounded up.

For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
"""


def split(fish):
    if isinstance(fish.left, Node):
        if split(fish.left):
            return fish
    elif fish.left > 9:
        d, r = divmod(fish.left, 2)
        fish.left = Node(fish, d, d+r)
        return fish

    if isinstance(fish.right, Node):
        if split(fish.right):
            return fish
    elif fish.right > 9:
        d, r = divmod(fish.right, 2)
        fish.right = Node(fish, d, d+r)
        return fish

    return False


assert split(Node(None, *[10, 10])) == Node(None, *[[5, 5], 10])
assert split(Node(None, *[11, 10])) == Node(None, *[[5, 6], 10])
assert split(Node(None, *[0, 10])) == Node(None, *[0, [5, 5]])
assert split(Node(None, *[[1, 2], 10])) == Node(None, *[[1, 2], [5, 5]])
assert split(Node(None, *[[1, 10], 10])) == Node(None, *[[1, [5, 5]], 10])
assert split(Node(None, *[[1, [1, [1, [1, 10]]]], 10])
             ) == Node(None, *[[1, [1, [1, [1, [5, 5]]]]], 10])


def reduce(snailfish):
    j = 40
    print("initial".ljust(j), snailfish)
    while True:
        # Explode
        fish = explode(snailfish)
        if fish:
            print(f"after explode ({fish})".ljust(j), snailfish)
            continue

        if split(snailfish):
            print("after split".ljust(j), snailfish)
            continue

        break

    print("after reduce".ljust(j), snailfish)

    return snailfish


a = Node(None, *[[[[4, 3], 4], 4], [7, [[8, 4], 9]]])
b = Node(None, 1, 1)
r = reduce(a.add(b))
assert r == Node(None, *[[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]])

print("""
##########################################
            Testcases done!
##########################################
""")


fish = None
for line in sys.stdin:
    if line.strip() == "":
        continue
    snailfish = json.loads(line)
    woodfish = Node(None, *snailfish)
    if fish == None:
        fish = woodfish
        continue

    # reduce(fish)
    # reduce(woodfish)
    fish = fish.add(woodfish)
    reduce(fish)
    print(fish)
    print()
