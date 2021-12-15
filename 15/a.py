import sys
from collections import defaultdict
from queue import PriorityQueue

grid = []
for line in sys.stdin.readlines():
    l = line.strip()
    if l != "":
        grid.append([int(r) for r in l])

height, width = len(grid), len(grid[0])
end = (len(grid) - 1, width - 1)
# Path = namedtuple("Path", ['cost', 'coordinates', 'visited'])

def adjacent(y, x):
    if y > 0:
        yield (y-1, x)
    if y < len(grid) - 1:
        yield (y+1, x)
    if x > 0:
        yield (y, x-1)
    if x < width - 1:
        yield (y, x+1)

# Fine, I wont reinvent Dijkstra's algorithm...
Q = PriorityQueue()
inf = 133713371337
prevdist = defaultdict(lambda: (inf, None))
source = (0,0)
prevdist[source] = (0, None)
for y in range(height):
    for x in range(width):
        v = (y,x)
        if v != source:
            prevdist[v] = (inf, None)
        Q.put((inf, v))

visited = set()
while not Q.empty():
    u = Q.get()[1]    

    if u in visited:
        continue
    visited.add(u)

    for v in adjacent(*u):
        print(v)
        print(prevdist[u])
        alt = prevdist[u][0] + grid[v[0]][v[1]]
        if alt < prevdist[v][0]:
            prevdist[v] = (alt, u)
            Q.put((alt, v)) # Not ideal, should update in place, but we work around this by using a set.

print(prevdist[end])