import sys
import re

"""
copied from 4
"""


def contains(p1, p2):
    # Unpack the tuples to get the start and end of each range
    a, b = p1
    c, d = p2

    # Check if the ranges overlap by checking if the end of the first range
    # is greater than the start of the second range, and vice versa
    return (a <= d) and (b >= c)


patt = re.compile(
    "Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

ty = 2000000
ylines = []
for line in sys.stdin:
    sx, sy, bx, by = [int(c) for c in patt.findall(line)[0]]

    diff = [bx - sx, by - sy]
    radius = sum(abs(c) for c in diff)
    print(radius)

    dist = abs(ty - sy)
    print(dist)
    if dist > radius:
        continue

    ylines.append([sx - (radius - dist), sx + (radius - dist)])


ylines = sorted(ylines)
print(ylines)
newlines = []
while ylines:
    line = ylines.pop(0)
    if len(ylines) == 0:
        newlines.append(line)
        break

    while ylines and contains(line, ylines[0]):
        nextline = ylines.pop(0)
        combined = line + nextline
        line = [min(combined), max(combined)]

    newlines.append(line)

print(newlines)

print(sum(abs(p[1] - p[0]) for p in newlines))
