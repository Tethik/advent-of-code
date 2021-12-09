import sys
import itertools


risk = 0
_map = []
for line in sys.stdin:    
    vals = [9, *[int(c) for c in line.strip()], 9]
    _map.append(vals)
    
print(_map)
_map.insert(0, [9]*len(_map[0]))
_map.append([9]*len(_map[0]))

for y in range(1, len(_map) - 1):
    for x in range(1, len(vals) - 1):
        c = _map[y][x]
        if all(c < a for a in [_map[y-1][x], _map[y+1][x], _map[y][x-1],  _map[y][x+1]]):
            risk += c + 1

        
print(risk)