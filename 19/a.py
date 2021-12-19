import sys
import math
from collections import defaultdict

scanners = defaultdict(lambda: set())
scanner = -1
for line in sys.stdin:
    line = line.strip()
    if line == "":
        continue
    if "scanner" in line:
        scanner += 1
        continue

    coordinate = tuple([int(c) for c in line.split(",")])
    scanners[scanner].add(coordinate)

total_scanners = len(scanners.keys())


def opposite(v):
    return tuple(-i for i in v)


def distance(v1, v2):
    return tuple(b-a for a, b in zip(list(v1), list(v2)))


def add(v1, v2):
    return tuple(a+b for a, b in zip(v1, v2))


# distance between beacon should be the same regardless of which scanner detected them
# there will be duplicates..
def compute_distances():
    distances = defaultdict(lambda: defaultdict(lambda: []))
    for s, coords in scanners.items():
        for c1 in coords:
            for c2 in coords:
                if c1 == c2:
                    continue
                d = (c2[0] - c1[0], c2[1] - c1[1], c2[2] - c1[2])
                # d = math.sqrt(d[0]*d[0] + d[1]*d[1] + d[2]*d[2])
                distances[s][d].append((c1, c2))
    return distances


def find_same_distance_pair(distances, s1, s2):
    # Find pair with same distance
    for d1 in distances[s1].keys():
        if len(distances[s1][d1]) > 1:
            # print("too indeterminate")
            continue
        l = distances[s2].get(d1)
        if l and len(l) == 1:
            return d1
    return None


distances = compute_distances()

found = True
while found:
    found = False
    for s1 in scanners.keys():
        for s2 in scanners.keys():
            if s2 == s1:
                continue

            # Find pair with same distance
            d = find_same_distance_pair(distances, s1, s2)
            if not d:
                continue

            print(d, distances[s1][d])

            p1 = distances[s1][d][0][0]
            p2 = distances[s2][d][0][0]
            print(p1, p2)
            diff = opposite(distance(p1, p2))
            print("diff", diff)
            # scanner_pos = add(known_scanner_pos[s1], opposite(diff))
            # known_scanner_pos[s2] = scanner_pos
            print(s2, diff)
            assert add(diff, p2) == p1

            found = True
            break

        if found:
            break

    if found:
        print("Found", s2, diff)
        # merge scanners
        print(len(scanners[s1]), scanners[s1])
        print(len(scanners[s2]), scanners[s2])
        print("Distances", len(distances[s1].keys()))

        for p in scanners[s2]:
            scanners[s1].add(add(diff, p))
        del scanners[s2]

        print("After merge", s2, "->", s1)
        print(len(scanners[s1]), scanners[s1])
        distances = compute_distances()
        print("Distances", len(distances[s1].keys()))

    print()


# for key, coords in scanners.items():
#     for coord in coords:
#         print(coord)
#     print("Number of coordinates:", len(scanners[key]))
print("Finished:", len(scanners.keys()) == 1)
