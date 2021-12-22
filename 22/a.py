import sys
import itertools
from collections import namedtuple
# import aabbtree


# def cuboid(xr,yr,zr):
#     for x in range(xr, xr+3):
#         for y in range(yr, yr+3):
#             for z in range(zr, zr+3):
#                 yield (x,y,z)

Coord = namedtuple('Coord', ['x', 'y', 'z'])


# def within(coord: Coord, start: Coord, end: Coord):
#     if all([
#         min(start.x, end.x) <= coord.x <= max(start.x, end.x),
#         min(start.y, end.y) <= coord.y <= max(start.y, end.y),
#         min(start.z, end.z) <= coord.z <= max(start.z, end.z)
#     ]):
#         return coord
#     else:
#         return None


class Cuboid:

    def __init__(self, start: Coord, end: Coord) -> None:
        self.start = start
        self.end = end

    def elems(self):
        # too slow, only use for debug
        xd = 1 if xe > xs else -1
        yd = 1 if ye > ys else -1
        zd = 1 if ze > zs else -1
        for x in range(xs, xe + xd):
            for y in range(ys, ye + yd):
                for z in range(zs, ze + zd):
                    yield (x, y, z)

    def __len__(self):
        volume = 1
        for a, _ in enumerate(self.start):
            volume *= abs(self.start[a] - self.end[a])
        return volume
        # return 1 * (abs(self.start.x - self.end.x)) * (abs(self.start.y - self.end.y)) * (abs(self.start.z - self.end.z))

    def overlap(self, cube):
        start = []
        end = []
        for a, _ in enumerate(self.start):
            overlap_min = max(self.start[a], cube.start[a])
            overlap_max = min(self.end[a], cube.end[a])
            if overlap_min >= overlap_max:
                return None
            start.append(overlap_min)
            end.append(overlap_max)

        return Cuboid(Coord(*start), Coord(*end))

    def __str__(self) -> str:
        return f"start={self.start},end={self.end}"


cuboids = []
overlaps = []
max_bound = 51
min_bound = -50


_map = set()
for line in sys.stdin:
    if line.strip() == "":
        continue
    value, coords = line.strip().split(" ")
    xr, yr, zr = coords.split(",")

    xs, xe = [int(s) for s in xr.replace("x=", "").split("..")]
    ys, ye = [int(s) for s in yr.replace("y=", "").split("..")]
    zs, ze = [int(s) for s in zr.replace("z=", "").split("..")]
    xd = 1 if xe > xs else -1
    yd = 1 if ye > ys else -1
    zd = 1 if ze > zs else -1

    for x in range(min_bound, max_bound):
        for y in range(min_bound, max_bound):
            for z in range(min_bound, max_bound):
                if not (min(xs, xe) <= x <= max(xe, xs)):
                    continue
                if not (min(ys, ye) <= y <= max(ys, ye)):
                    continue
                if not (min(zs, ze) <= z <= max(ze, zs)):
                    continue

                if value == "on":
                    # if not (x, y, z) in _map:
                    # print((x, y, z))
                    _map.add((x, y, z))
                else:
                    if (x, y, z) in _map:
                        # print((x, y, z))
                        _map.remove((x, y, z))
    # print()

    # start = Coord(xs, ys, zs)
    # end = Coord(xe+xd, ye+yd, ze+zd)
    # cube = Cuboid(start, end)
    # print("New", cube)
    # print(len(cube))

    # for c2, val in cuboids.copy():
    #     overlap = c2.overlap(cube)
    #     if not overlap:
    #         continue
    #     print(overlap)
    #     print(len(overlap))

    #     if value == "on" and val == "on":
    #         cuboids.append((overlap, "off"))
    #     elif value == "off" and val == "on":
    #         cuboids.append((overlap, "off"))
    #     elif value == "on" and val == "off":
    #         cuboids.append((overlap, "on"))
    #     # elif value == "off" and value == "off":
    #     print()

    # if value == "on":
    #     cuboids.append((cube, value))

    # print()
    # for c, v in cuboids:
    #     print(c, v)
    # off = sum(len(c) for c, _ in filter(lambda v: v[1] == "off", cuboids))
    # on = sum(len(c) for c, _ in filter(lambda v: v[1] == "on", cuboids))
    # print(on - off)

    # print()


# area = Cuboid(Coord(-50, -50, -50), Coord(50, 50, 50))

# on = 0
# off = 0
# for cube, val in cuboids:
#     o = area.overlap(cube)
#     if o:
#         if val == "off":
#             off += len(o)
#         else:
#             on += len(o)

# print(on - off)

print(len(_map))
