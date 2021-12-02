import sys
aim = x = y = 0

for line in sys.stdin:
    p = line.split(" ")    
    v = int(p[1])
    if p[0][0] == "f":
        x += v
        y += aim * v
    elif p[0][0] == "u":
        aim -= v
    elif p[0][0] == "d":
        aim += v

print(x * y)