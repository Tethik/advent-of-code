import sys

s = 0
group = []
for line in sys.stdin:
    rucksack = line.strip()
    group.append(rucksack)

    if len(group) != 3:
        continue

    for c in set(group[0]):
        if all(c in g for g in group):
            if c < 'a':
                p = ord(c) - ord('A') + 27
            else:
                p = ord(c) - ord('a') + 1
            # print(c, p)
            s += p

    group = []

print(s)
