import sys

min_sum = (-1,1283798213798213)
for s in range(min(stuff), max(stuff)):
    _sum = 0
    for s2 in stuff:
        l = abs(s - s2)        
        _sum += (l * (1 + l)) / 2

    if _sum <= min_sum[1]:
        min_sum = (s, _sum)

print(min_sum)