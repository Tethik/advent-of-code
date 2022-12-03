import sys

s = 0
group = []
for line in sys.stdin:
    rucksack = line.strip()
    group.append(rucksack)

    if len(group) != 3:
        continue

    seen = set()
    for c in group[0]:
        if c in seen:
            continue

        if all([c in g for g in group]):
            if c < 'a':
                p = ord(c) - ord('A') + 27
            else:
                p = ord(c) - ord('a') + 1
            # print(c, p)
            s += p
        seen.add(c)

    group = []

print(s)
