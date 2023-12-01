import sys

s = 0
for line in sys.stdin:
    rucksack = line.strip()
    i = len(rucksack) // 2
    comp1 = rucksack[:i]
    comp2 = rucksack[i:]
    print(comp1, comp2)

    exists = set()
    for c in comp1:
        exists.add(c)

    exists2 = set()
    for c in comp2:
        if c in exists and c not in exists2:
            exists2.add(c)
            if c < 'a':
                p = ord(c) - ord('A') + 27
            else:
                p = ord(c) - ord('a') + 1
            print(c, p)
            s += p


print(s)
