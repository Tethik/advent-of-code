import sys
from collections import defaultdict, Counter

poly = sys.stdin.readline().strip()

pairs = []

for line in sys.stdin:
    if line.strip() == "":
        continue
    pairs.append(line.strip().split(" -> "))
    


for step in range(10):
    print(step)
    print("-->", poly)
    inserts = defaultdict(lambda: [])
    for pair, ins in pairs:        
        i = poly.find(pair)
        while i > -1:
            inserts[i+1].append(ins)
            i = poly.find(pair, i+1)
            
    # print(inserts)
    p = list(poly)
    idx = sorted(inserts.keys())
    for i in idx[::-1]:
        ins = inserts[i]
        p.insert(i, "".join(ins))
    poly = "".join(p)
    print("<--", poly)
    print()

counter = Counter(poly)
mc = counter.most_common(len(counter.keys()))
lc = mc[-1]
print(lc)
mc = mc[0]
print(mc)

print(mc[1] - lc[1])

