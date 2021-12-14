import sys
from collections import Counter
import functools

polymer = sys.stdin.readline().strip()

pairs = dict()

for line in sys.stdin:
    if line.strip() == "":
        continue
    k, v = line.strip().split(" -> ")
    pairs[k] = v


@functools.lru_cache(None)
def compute(poly: str, steps: int):
    if steps <= 0:
        return Counter()
    ins = pairs.get(poly)
    if not ins:
        return Counter()
    # left = poly[0] + ins
    # right = poly[1] + ins
    # print(left)
    # print(right)
    return Counter(ins) + compute(poly[0] + ins, steps - 1) + compute(ins + poly[1], steps - 1)


#
# After step 10, B occurs 1749 times, C occurs 298 times, H occurs 161 times, and N occurs 865 times;
#
steps = 40
total = Counter(polymer)
print(polymer, total)
for i in range(len(polymer) - 1):
    poly = polymer[i:i+2]
    table = compute(poly, steps)
    print(poly, table)
    total += table

print(total)
mc = total.most_common(len(total.keys()))
print(mc[0], mc[-1])
print(mc[0][1] - mc[-1][1])
