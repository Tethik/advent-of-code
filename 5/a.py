import sys
from collections import Counter

vectors = []

for line in sys.stdin:
    if not "->" in line:
        continue
    start, end = line.split("->")
    vector = dict(
        start=[int(s) for s in start.strip().split(",")],
        end=[int(s) for s in end.strip().split(",")])
    vectors.append(vector)

# Naive solution, just count:
visits = Counter()
for v in vectors:
    # Only care about horizontal/vertical lines for now.
    x1, x2 = v["start"][0], v["end"][0]
    y1, y2 = v["start"][1], v["end"][1]
    if x1 == x2 and y1 == y2:
        visits[tuple(v["start"])] += 1
        continue

    if y1 == y2:
        _maxx, _minx = max(x1, x2), min(
            x1, x2)

        for x in range(_minx, _maxx+1):
            visits[(x, y1)] += 1

    if x1 == x2:
        _maxy, _miny = max(y1, y2), min(
            y1, y2)

        for y in range(_miny, _maxy+1):
            visits[(x1, y)] += 1


# print(visits)
print(sum(1 for _, c in visits.items() if c > 1))
