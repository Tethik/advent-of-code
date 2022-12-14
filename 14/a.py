import sys


_row = ['.'] * 100
_map = []
for _ in range(175):
    _map.append(_row.copy())


def parse_point(s: str):
    parts = s.split(",")
    x = int(parts[0]) - 450
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


for row in _map:
    print("".join(row))
print()

# ready
start = [50, 0]
_map[0][50] = '+'

s = 0
out_of_bounds = False
while not out_of_bounds:
    sand = start.copy()
    # move until stop or out of range
    while True:
        x, y = sand
        if y + 1 >= len(_map):
            out_of_bounds = True
            break

        if _map[y + 1][x] == '.':
            sand[1] += 1
            continue
        if _map[y + 1][x - 1] == '.':
            sand[1] += 1
            sand[0] -= 1
            continue
        if _map[y + 1][x + 1] == '.':
            sand[1] += 1
            sand[0] += 1
            continue

        _map[y][x] = 'o'
        break

    # show map
    for row in _map:
        print("".join(row))
    print()

    s += 1
print(s - 1)
