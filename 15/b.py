import sys
import re
from collections import defaultdict

line = sys.stdin.readline().strip()
x_bounds = y_bounds = [int(c) for c in line.split(",")]
print("Bounds set to", x_bounds)


def contains(p1, p2):
    # Unpack the tuples to get the start and end of each range
    a, b = p1
    c, d = p2

    # Check if the ranges overlap by checking if the end of the first range
    # is greater than the start of the second range, and vice versa
    return (a <= d) and (b >= c)


patt = re.compile(
    "Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

lines = defaultdict(lambda: [])
for line in sys.stdin:
    sx, sy, bx, by = [int(c) for c in patt.findall(line)[0]]

    diff = [bx - sx, by - sy]
    radius = sum(abs(c) for c in diff)

    for ty in range(sy - radius, sy + radius):
        if ty < y_bounds[0] or ty > y_bounds[1]:
            continue
        dist = abs(ty - sy)
        lines[ty].append(
            [max(sx - (radius - dist), x_bounds[0]), min(sx + (radius - dist), x_bounds[1])])

print("Got", len(lines.keys()), "lines")

for key, ylines in lines.items():
    ylines = sorted(ylines)
    # print(ylines)
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
    lines[key] = newlines

print("Lines reduced")

for y in range(min(y_bounds), max(y_bounds)):
    l = lines[y]
    # print(y, l)
    s = sum(abs(p[1] - p[0]) + 1 for p in l) - 1
    # print(s)
    if s != max(y_bounds) - min(y_bounds):
        for i, line in enumerate(l):
            if l[i+1][0] != line[1] + 1:
                x = line[1] + 1
                print(x, y)
                print("Frequency", x * 4000000 + y)
                break
        # print(l)
        break
