import sys
from collections import namedtuple


Coord = namedtuple('Coord', ['x', 'y', 'z'])


class Cuboid:

    def __init__(self, start: Coord, end: Coord) -> None:
        self.start = start
        self.end = end
        self.overlaps = []

    def __len__(self):
        volume = 1
        for a, _ in enumerate(self.start):
            volume *= abs(self.start[a] - (self.end[a]+1))

        overlap_volume = 0
        for o in self.overlaps:
            overlap_volume += len(o)
        return volume - overlap_volume

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

        overlap = Cuboid(Coord(*start), Coord(*end))

        for o in self.overlaps:
            o.overlap(overlap)  # recurses down to each overlap

        self.overlaps.append(overlap)
        return overlap

    def __str__(self) -> str:
        return f"start={self.start},end={self.end}"


cuboids = []
overlaps = []
max_bound = 51
min_bound = -50

for line in sys.stdin:
    if line.strip() == "":
        continue
    value, coords = line.strip().split(" ")
    xr, yr, zr = coords.split(",")

    xs, xe = [int(s) for s in xr.replace("x=", "").split("..")]
    ys, ye = [int(s) for s in yr.replace("y=", "").split("..")]
    zs, ze = [int(s) for s in zr.replace("z=", "").split("..")]

    start = Coord(xs, ys, zs)
    end = Coord(xe, ye, ze)
    cube = Cuboid(start, end)
    # print("New", cube)
    # print(len(cube))
    # print()
    # print("Overlaps")
    overlaps = []
    for c2, val in cuboids.copy():
        overlap = c2.overlap(cube)
        # if overlap:
        #     print(overlap, val, value, len(overlap))

    if value == "on":
        cuboids.append((cube, value))

    # print()
    # print("State")
    # for c, v in cuboids:
    #     print(c, v, len(c))
    # off = sum(len(c) for c, _ in filter(lambda v: v[1] == "off", cuboids))
    # on = sum(len(c) for c, _ in filter(lambda v: v[1] == "on", cuboids))
    # print(on - off)
    # print()

    # print()


area = Cuboid(Coord(-50, -50, -50), Coord(50, 50, 50))

area_on = 0
area_off = 0
on = 0
off = 0
for cube, val in cuboids:
    o = area.overlap(cube)
    if val == "off":
        if o:
            area_off += len(cube)
        off += len(cube)
    else:
        if o:
            area_on += len(cube)
        on += len(cube)

print(area_on - area_off)
print(on - off)
