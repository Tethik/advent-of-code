import sys

incr = -3
p = -1
q = [-1,-1]
for line in sys.stdin:
    value = int(line.strip())    
    q.insert(0, value)
    s = sum(q)    
    if s > p:
        incr += 1
    print(q, p, s, incr)
    p = s
    q.pop()

print(incr)