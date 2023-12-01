import sys

scores = {
    "A": 1,
    "B": 2,
    "C": 3,
    "X": 1,
    "Y": 2,
    "Z": 3,
}

win = {
    "A": "Y",
    "B": "Z",
    "C": "X",
}

lose = {
    "B": "X",
    "C": "Y",
    "A": "Z"
}

s = 0

for line in sys.stdin:
    i = line.strip()
    parts = i.split()

    o = parts[0]
    if parts[1] == "X":
        d = 0
        p = lose[o]
        d += scores[p]
    elif parts[1] == "Y":
        d = 3
        d += scores[o]
    else:
        d = 6
        p = win[o]
        d += scores[p]

    s += d

print(s)
