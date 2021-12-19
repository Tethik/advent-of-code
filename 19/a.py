import sys
import math
from collections import defaultdict
import itertools

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
def compute_all_distances():
    distances = defaultdict(lambda: defaultdict(lambda: []))
    for s in scanners.keys():
        distances[s] = compute_distances(s)
    return distances


def compute_distances(scanner, orientation=None):
    distances = defaultdict(lambda: [])
    beacons = scanners[scanner]

    # translate all beacons in place
    if orientation:
        new_beacons = []
        for i, beacon in enumerate(beacons):
            new_beacon = []
            for o in orientation:
                if o < 0:
                    new_beacon.append(-beacon[abs(o) - 1])
                else:
                    new_beacon.append(beacon[abs(o) - 1])
            new_beacons.append(tuple(new_beacon))
        scanners[scanner] = new_beacons

    for c1 in beacons:
        for c2 in beacons:
            if c1 == c2:
                continue
            d = (c2[0] - c1[0], c2[1] - c1[1], c2[2] - c1[2])
            # d = math.sqrt(d[0]*d[0] + d[1]*d[1] + d[2]*d[2])
            distances[d].append((c1, c2))
    return distances


def find_same_distance_pair(distances, s1, s2):
    # Find pair with same distance
    for d1 in distances[s1].keys():
        if len(distances[s1][d1]) > 1:
            continue
        l = distances[s2].get(d1)
        if l and len(l) == 1:
            return d1
    return None


def create_orientations():
    order_of_axis = list(itertools.permutations(
        [1, 2, 3], 3))
    negatives = [[(0,)], [(1,)], [(2,)], list(itertools.combinations(
        [0, 1, 2], 2)), [(0, 1, 2)]]
    negatives = list(itertools.chain.from_iterable(negatives))

    # print(order_of_axis)
    # print(negatives)
    for oa in order_of_axis:
        # print("oa", oa)
        yield oa
        for neg in negatives:
            copy = list(oa)  # .copy()
            # print("neg", neg)
            for neg_index in neg:
                print(neg_index)
                copy[neg_index] = -copy[neg_index]
            yield tuple(copy)


orientations = set(list(create_orientations()))

# assert len(o) == 24
distances = compute_all_distances()

found = True
while found:
    found = False

    for s1 in scanners.keys():
        for s2 in scanners.keys():
            if s2 == s1:
                continue

            for o in orientations:
                distances[s2] = compute_distances(s2, o)

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
                print(s2, diff)
                assert add(diff, p2) == p1

                found = True
                break

        if found:
            break

    if found:
        # merge scanners
        print("Found", s2, diff)
        print(len(scanners[s1]), scanners[s1])
        print(len(scanners[s2]), scanners[s2])
        print("Distances", len(distances[s1].keys()))

        for p in scanners[s2]:
            scanners[s1].add(add(diff, p))
        del scanners[s2]

        print("After merge", s2, "->", s1)
        print(len(scanners[s1]), scanners[s1])
        distances = compute_all_distances()
        print("Distances", len(distances[s1].keys()))

    print()


for key, coords in scanners.items():
    for coord in coords:
        print(coord)
    print("Number of coordinates:", len(scanners[key]))
print("Finished:", len(scanners.keys()) == 1)
