import sys
from collections import defaultdict, Counter
import functools

poly = sys.stdin.readline().strip()

pairs = []

for line in sys.stdin:
    if line.strip() == "":
        continue
    pairs.append(line.strip().split(" -> "))
    

@functools.lru_cache
def compute(polymer: str):
    compute(polymer, steps - 1)
    pass

"""
These numbers are probably too big to populate the entire polymer.
> In the above example, the most common element is B (occurring 2192039569602 times)
> and the least common element is H (occurring 3849876073 times); subtracting these produces 2188189693529.
"""

for step in range(10):
    print(step)
    print("-->", poly)
    inserts = defaultdict(lambda: [])
    counts = defaultdict(lambda: 0)
    for pair, ins in pairs:        
        i = poly.find(pair)
        while i > -1:
            inserts[i+1].append(ins)
            counts[ins] += 1
            i = poly.find(pair, i+1)

    print(counts)      
    # print(inserts)

    p = list(poly)
    idx = sorted(inserts.keys())
    for i in idx[::-1]:
        ins = inserts[i]
        p.insert(i, "".join(ins))
    poly = "".join(p)
    print("<--", poly)
    print()

print()
counter = Counter(poly)
mc = counter.most_common(len(counter.keys()))
lc = mc[-1]
print(lc)
mc = mc[0]
print(mc)

print(mc[1] - lc[1])

