import math
import yaml
import sys
import queue

_map = []
for line in sys.stdin:
    _map.append([c for c in line.strip()])


for y in range(len(_map)):
    for x in range(len(_map[y])):
        if _map[y][x] == 'S':
            _map[y][x] = 'a'
        elif _map[y][x] == 'E':
            s = (y, x)
            _map[y][x] = 'z'


print(s)


q = queue.PriorityQueue()
q.put((0, s))
visited = set()
while not q.empty():
    item = q.get()

    print("item", item)
    dist, pos = item
    visited.add(pos)

    y, x = pos
    val = _map[y][x]

    if val == 'a':
        print(dist, val)
        break

    for n in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        ny, nx = n
        neigh = (y + ny, x + nx)

        if neigh[0] < 0 or neigh[1] < 0:
            continue

        try:
            diff = ord(_map[y + ny][x + nx]) - ord(val)
            # print(neigh, diff, val, _map[y + ny][x + nx])
            if diff >= -1 and neigh not in visited:
                visited.add(neigh)
                q.put((dist+1, neigh))
        except:
            pass
    # break
