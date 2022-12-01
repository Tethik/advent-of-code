import sys
from collections import defaultdict

bits = defaultdict(lambda: 0)
n = 0
for line in sys.stdin:
    for i, c in enumerate(line):
        if c == "1":
            bits[i] += 1
    n += 1

bitlen = len(bits.keys())
# most common
gamma = [max(0, min(int(bits[i] - n / 2), 1)) for i in range(bitlen)]
print(gamma)
gamma = int("".join(map(str, gamma)), 2)

# least common
epsilon = [max(0, min(int(n / 2 - bits[i]), 1)) for i in range(bitlen)]
print(epsilon)
epsilon = int("".join(map(str, epsilon)), 2)

print(gamma * epsilon)


