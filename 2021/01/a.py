import sys

incr = -1
p = -1
for line in sys.stdin:
    value = int(line.strip())
    if value > p:
        incr += 1
    p = value

print(incr)