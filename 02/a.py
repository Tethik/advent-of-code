import sys

s = 0
ss = {
    "A X": 4,
    "A Y": 8,
    "A Z": 3,
    "B X": 1,
    "B Y": 5,
    "B Z": 9,
    "C X": 7,
    "C Y": 2,
    "C Z": 6
}


for line in sys.stdin:
    i = line.strip()
    print(i, ss[i])
    s += ss[i]

print(s)
