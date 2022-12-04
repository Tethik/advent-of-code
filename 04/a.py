import sys


def contains(p1, p2):
    r = int(p1[1]) >= int(p2[1]) and int(p1[0]) <= int(p2[0])
    if r:
        print(p1, p2)
        print(r)
    return r


s = 0
for line in sys.stdin:
    pairs = [p.split("-") for p in line.strip().split(",")]
    if (contains(pairs[0], pairs[1]) or contains(pairs[1], pairs[0])):
        s += 1


print(s)
