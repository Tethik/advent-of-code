import sys

patterns = {
    2: "1",
    4: "4",
    3: "7",
    7: "8"
}

c = 0
for line in sys.stdin:
    _, p2 = line.split("|")
    seg = p2.split()
    for s in seg:
        if len(set(s)) in patterns:
            c += 1

print(c)