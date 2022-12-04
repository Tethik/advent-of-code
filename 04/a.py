import sys


def contains(p1, p2):
    # Unpack the tuples to get the start and end of each range
    a, b = p1
    c, d = p2

    # Check if the ranges overlap by checking if the end of the first range
    # is greater than the start of the second range, and vice versa
    return (a <= d) and (b >= c)


s = 0
for line in sys.stdin:
    pairs = [p.split("-") for p in line.strip().split(",")]
    if (contains(pairs[0], pairs[1]) or contains(pairs[1], pairs[0])):
        s += 1


print(s)
