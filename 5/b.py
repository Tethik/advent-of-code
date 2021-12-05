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
    x1, x2 = v["start"][0], v["end"][0]
    y1, y2 = v["start"][1], v["end"][1]
    if x1 == x2 and y1 == y2:
        visits[tuple(v["start"])] += 1
        continue

    dir = [(x2 - x1), (y2 - y1)]
    if dir[0] != 0:
        dir[0] /= abs(dir[0])
    if dir[1] != 0:
        dir[1] /= abs(dir[1])

    curr = (x1, y1)
    while curr != (x2 + dir[0], y2 + dir[1]):
        visits[curr] += 1
        curr = (curr[0] + dir[0], curr[1] + dir[1])


print(sum(1 for _, c in visits.items() if c > 1))
