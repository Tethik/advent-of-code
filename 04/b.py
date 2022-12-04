import sys


def overlap(p1, p2):
    for p, b in [(p1, p2), (p2, p1)]:
        if p[0] >= b[0] and p[0] <= b[1]:
            return True
        if p[1] >= b[0] and p[1] <= b[1]:
            return True
    return False


s = 0
for line in sys.stdin:
    pairs = [[int(c) for c in p.split("-")] for p in line.strip().split(",")]
    if (overlap(pairs[0], pairs[1])):
        s += 1


print(s)

assert overlap([0, 1], [1, 1])
assert overlap([0, 2], [1, 1])
assert overlap([0, 2], [1, 2])
assert overlap([1, 2], [0, 4])
assert overlap([0, 4], [1, 2])
assert overlap([0, 4], [1, 2])
