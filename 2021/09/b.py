import sys
import itertools


risk = 0
_map = []
for line in sys.stdin:    
    vals = [99, *[int(c) for c in line.strip()], 99]
    _map.append(vals)
    
olen = len(_map[0])
_map.insert(0, [99]*olen)
_map.append([99]*olen)


def adjacent(y, x):
    return [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]

startpoints = []
for y in range(1, len(_map) - 1):
    for x in range(1, len(vals) - 1):
        c = _map[y][x]
        if all(c < _map[ya][xa] for ya, xa in adjacent(y, x)):
            startpoints.append((y,x))

print("startpoints", startpoints)

sizes = []
for s in startpoints:
    q = [s]
    visited = set()
    size = 0
    while len(q) > 0:
        pos = y, x = q.pop()
        if pos in visited:            
            continue
        visited.add(pos)
        size += 1
        for ya, xa in adjacent(y, x):
            if _map[ya][xa] > 8:
                continue
            
            if _map[ya][xa] > _map[y][x]:
                print("pos", pos, _map[y][x])
                print("a", (ya,xa), _map[ya][xa])    
                print()            
                q.append((ya, xa))
    sizes.append(size)
    print()


print(*_map)
sizes = sorted(sizes)
print(sizes, sizes[-3:])

p = 1
for s in sizes[-3:]:
    p *= s

print(p)





        
