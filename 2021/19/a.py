import sys
import math
from collections import defaultdict
import itertools
import functools


def opposite(v):
    return tuple(-i for i in v)


def distance(v1, v2):
    return tuple(b-a for a, b in zip(list(v1), list(v2)))


def add(v1, v2):
    return tuple(a+b for a, b in zip(v1, v2))


def normalize(beacons):
    return normalize_around(beacons, 0)


@functools.lru_cache(None)
def normalize_around(beacons, p):
    beacons = list(beacons)
    # bring to origo
    diff = distance(p, tuple(0 for _ in beacons[0]))
    beacons = map(lambda b: add(b, diff), beacons)
    return frozenset(beacons)


@functools.lru_cache(None)
def orient(beacons, orientation):
    new_beacons = []
    for beacon in beacons:
        new_beacon = []
        for o in orientation:
            if o < 0:
                new_beacon.append(-beacon[abs(o) - 1])
            else:
                new_beacon.append(beacon[abs(o) - 1])
        new_beacons.append(tuple(new_beacon))
    return frozenset(new_beacons)


# def distancify(beacons):
#     for b in beacons:
#         distances = set()
#         for b2 in beacons:
#             if b == b2:
#                 continue
#             d = tuple(b2[i] - b[i] for i in range(len(b)))
#             distances.add(d)
#         yield distances

# # distance between beacon should be the same regardless of which scanner detected them
# # there will be duplicates..


# def compute_all_distances():
#     distances = defaultdict(lambda: defaultdict(lambda: []))
#     for s in scanners.keys():
#         distances[s] = compute_distances(s)
#     return distances


# def compute_distances(scanner):
#     distances = defaultdict(lambda: [])
#     beacons = scanners[scanner]

#     for c1 in beacons:
#         for c2 in beacons:
#             if c1 == c2:
#                 continue
#             d = (c2[0] - c1[0], c2[1] - c1[1], c2[2] - c1[2])
#             # d = math.sqrt(d[0]*d[0] + d[1]*d[1] + d[2]*d[2])
#             distances[d].append((c1, c2))
#     return distances


# def find_same_distance_pair(distances, s1, s2):
#     # Find pair with same distance
#     for d1 in distances[s1].keys():
#         if len(distances[s1][d1]) > 1:
#             continue
#         l = distances[s2].get(d1)
#         if l and len(l) == 1:
#             return d1
#     return None


def create_orientations():
    order_of_axis = list(itertools.permutations(
        [1, 2, 3], 3))
    negatives = [[(0,)], [(1,)], [(2,)], list(itertools.combinations(
        [0, 1, 2], 2)), [(0, 1, 2)]]
    negatives = list(itertools.chain.from_iterable(negatives))

    for oa in order_of_axis:
        yield oa
        for neg in negatives:
            copy = list(oa)
            for neg_index in neg:
                copy[neg_index] = -copy[neg_index]
            yield tuple(copy)


# scanner1 = normalize([(-1, -1, 0), (-5, 0, 0), (-2, 1, 0)])
# scanner2 = normalize([(0, 2, 0), (4, 1, 0), (3, 3, 0)])


def match(scanner1, scanner2, threshold):
    for p1 in scanner1:
        beacons = normalize_around(scanner1, p1)
        # for o in ORIENTATIONS:  # maybe we can skip this?
        #     beacons = orient(beacons, o)

        for p2 in scanner2:
            normalized2 = normalize_around(scanner2, p2)
            for o2 in ORIENTATIONS:
                beacons2 = orient(normalized2, o2)

                intersection = beacons & beacons2
                # print(intersection)
                if len(intersection) >= threshold:
                    print(beacons)
                    print(beacons2)
                    print(intersection)
                    # these points are the same. probably.
                    return p1, p2, o2

    return None


def any_match(scanners, threshold):
    keys = sorted(scanners.keys(), key=lambda k: len(scanners[k]))
    for s1 in keys:
        m = False
        for s2 in keys:
            if s1 == s2:
                continue
            m = match(scanners[s1], scanners[s2], threshold)
            if m:
                p1, p2, o2 = m
                return s1, s2, p1, p2, o2
    return False


ORIENTATIONS = frozenset(list(create_orientations()))
THRESHOLD = 3
# print(*sorted(list(orientations), key=str), sep="\n")


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

for key, val in scanners.items():
    scanners[key] = frozenset(val)
# print(scanners)

#
#           Main
#


m = any_match(scanners, THRESHOLD)
while m and len(scanners) > 1:
    print()
    print("match", m)
    s1, s2, p1, p2, orientation = m

    # merge points
    s1set = normalize_around(scanners[s1], p1)
    s2set = normalize_around(scanners[s2], p2)
    s2set = orient(s2set, orientation)
    print("s1set", s1set)
    print("s2set", s2set)
    newset = s1set | s2set
    print("newset", frozenset(newset))
    print("intersect", s1set & s2set)
    print(len(scanners[s1]), len(scanners[s2]), len(newset))
    scanners[s1] = frozenset(newset)
    del scanners[s2]
    print("merged", s2, "into", s1)
    print(len(scanners), "to go!")
    print()
    m = any_match(scanners, THRESHOLD)

    if not m:
        print("No match found!")


print()
for key, val in scanners.items():
    print(key)
    print(val)
    print(len(val))
