import sys

simple, sliding = -1, -3
q = [-1,-1,-1,-1]
for i, line in enumerate(sys.stdin):
    curr = i % 4    
    q[curr] = int(line.strip())    
    sliding += int(q[curr] > q[(i+1) % 4])    
    simple += int(q[curr] > q[(i-1) % 4])

print(simple, sliding)