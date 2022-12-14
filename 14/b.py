import sys


width = 2000
_row = ['.'] * width
_map = []
for _ in range(175):
    _map.append(_row.copy())


def parse_point(s: str):
    parts = s.split(",")
    x = int(parts[0])
    y = int(parts[1])
    return [x, y]


for line in sys.stdin:
    wall = line.strip()

    points = wall.split("->")
    prev = parse_point(points[0])
    for point in points[1:]:
        p = parse_point(point)
        diff = [p[0] - prev[0], p[1] - prev[1]]
        dir = [d if d == 0 else d // abs(d) for d in diff]
        print(dir)
        while prev != p:
            print(prev)
            _map[prev[1]][prev[0]] = "#"
            prev[0] += dir[0]
            prev[1] += dir[1]
        _map[prev[1]][prev[0]] = "#"

        prev = p
    print()

# trim the map
while all(c == '.' for c in _map[-1]):
    _map.pop()
_map.append(_row.copy())
_map.append(["#"] * width)


for row in _map:
    print("".join(row))
print()

# ready
start = [500, 0]
_map[0][500] = 'o'

s = 1
for y in range(1, len(_map) - 1):
    for x in range(len(_map[y])):
        if _map[y][x] == '#':
            continue
        parents = [_map[y - 1][x]]
        if x > 0:
            parents += _map[y - 1][x - 1]
        if x < len(_map[y]) - 1:
            parents += _map[y - 1][x + 1]

        if 'o' in parents:
            _map[y][x] = 'o'
            s += 1

# show map
for row in _map:
    print("".join(row))
print()

print(s)
