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
        new_beacons.append(orient_point(beacon, orientation))
    return frozenset(new_beacons)


@functools.lru_cache(None)
def orient_point(point, orientation):
    new_point = []
    for o in orientation:
        if o < 0:
            new_point.append(-point[abs(o) - 1])
        else:
            new_point.append(point[abs(o) - 1])
    return tuple(new_point)


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
    # keys = sorted(scanners.keys(), key=lambda k: len(scanners[k]))
    keys = sorted(scanners.keys())
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

total_scanners = len(scanners.keys())
# print(scanners)

#
#           Main
#


# pa = (6, 4)
# pb = (4, 2)
# o = (-2, 1)
# pbo = orient_point(pb, o)
# assert pbo == (-2, 4)
# dab = distance(pbo, pa)
# print(dab)

rel = dict()
m = any_match(scanners, THRESHOLD)
while m and len(scanners) > 1:
    print()
    print("match", m)
    s1, s2, p1, p2, orientation = m

    # distance between the two scanners
    man = distance(orient_point(p2, orientation), p1)
    assert s2 not in rel
    rel[s2] = (s1, man)  # from s1, go this vector

    # merge points
    s1set = normalize_around(scanners[s1], p1)
    s2set = normalize_around(scanners[s2], p2)
    s2set = orient(s2set, orientation)
    print("s1set", s1set)
    print("s2set", s2set)
    newset = frozenset(s1set | s2set)
    print("newset", newset)
    print("intersect", s1set & s2set)
    print(len(scanners[s1]), len(scanners[s2]), len(newset))

    # move back to original points?
    newset = normalize_around(newset, opposite(p1))

    scanners[s1] = newset
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

assert len(scanners) == 1

# Manhattan time
s = list(scanners.keys())[0]
scanner_points = {s: (0, 0, 0)}
while len(scanner_points.keys()) < total_scanners:
    for key, val in rel.items():
        if val[0] in scanner_points:
            scanner_points[key] = add(scanner_points[val[0]], val[1])

print(scanner_points)
combinations = list(itertools.combinations(scanner_points.values(), 2))
print(combinations)
_max = max(map(lambda p: sum(abs(a) for a in distance(*p)), combinations))

print(_max)
