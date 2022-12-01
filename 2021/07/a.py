import sys

min_sum = (-1,1283798213798213)
for s in stuff:
    _sum = 0
    for s2 in stuff:
        _sum += abs(s - s2)

    if _sum <= min_sum[1]:
        min_sum = (s, _sum)

print(min_sum)