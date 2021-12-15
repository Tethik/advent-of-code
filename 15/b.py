import sys
from collections import namedtuple, defaultdict
from queue import PriorityQueue


def printGrid(grid):    
    height, width = len(grid), len(grid[0])
    for y in range(height):
        s = ""
        for x in range(width):
            s += str(grid[y][x])
        print(s)

grid = []
rc = 0
for line in sys.stdin.readlines():
    l = line.strip()
    if l == "":
        continue
    grid.append([int(r) for r in l])

height, width = len(grid), len(grid[0])    
big_grid = []
for y in range(5*height):
    row = []
    # print(5*width, 5*height)    
    for x in range(5*width):            
        v = grid[y % height][x % width] + x // width + y // height        
        if v > 9:
            v = v % 9
        row.append(v)
    # print(row)
    big_grid.append(row)
    rc += 1

# printGrid(big_grid) # this makes computer sad on large inputs
grid = big_grid
height, width = len(grid), len(grid[0])

end = (height - 1, width - 1)
Path = namedtuple("Path", ['cost', 'coordinates', 'visited'])

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
        # print(v)
        # print(prevdist[u])
        alt = prevdist[u][0] + grid[v[0]][v[1]]
        if alt < prevdist[v][0]:
            prevdist[v] = (alt, u)
            Q.put((alt, v))

print(prevdist[end])