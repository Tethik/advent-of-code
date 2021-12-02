import sys
x = y = 0

for line in sys.stdin:
    p = line.split(" ")    
    if p[0][0] == "f":
        x += int(p[1])
    elif p[0][0] == "u":
        y += int(p[1])
    elif p[0][0] == "d":
        y -= int(p[1])

print(x * -y)