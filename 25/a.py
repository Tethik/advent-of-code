import sys

_map = [list(s.strip()) for s in sys.stdin.readlines()]


def nextX(x):
    return (x+1) % len(_map[0])


def nextY(y):
    return (y+1) % len(_map)


print("Initial state")
print(*["".join(s) for s in _map], sep="\n")
print()


changed = True
s = 0
while changed:
    # for _ in range(4):
    changed = False
    handled = set()
    # sidleds
    for y in range(len(_map)):
        row = _map[y].copy()
        for x in range(len(_map[0])):
            if row[x] == ">":
                x1 = nextX(x)
                if row[x1] == ".":
                    _map[y][x] = "."
                    _map[y][x1] = ">"
                    changed = True

    # lodräta
    handled.clear()
    for x in range(len(_map[0])):
        col = []
        for y in range(len(_map)):
            if _map[y][x] == "v":
                y1 = nextY(y)
                if _map[y1][x] == ".":
                    col.append((y, x, y1))
                    changed = True

        for y, x, y1 in col:
            _map[y][x] = "."
            _map[y1][x] = "v"

    s += 1
    # print(f"After {s} steps")
    # print(*["".join(s) for s in _map], sep="\n")
    # print()


print(s)
