import sys

lines = sys.stdin.readlines()
bitlen = len(lines[0].strip())

def most_common(lines, b):
    c = 0
    for line in lines:
        if line[b] == "1": 
            c += 1
    return c * 2 >= len(lines)

ogr = lines
for b in range(bitlen):
    if len(ogr) < 2:
        break
    
    mc = "1" if most_common(ogr, b) else "0"
    ogr = list(filter(lambda l: l[b] == mc, ogr))
    print(ogr)    
print()

cgr = lines
for b in range(bitlen):
    if len(cgr) < 2:
        break

    lc = "0" if most_common(cgr, b) else "1"
    cgr = list(filter(lambda l: l[b] == lc, cgr))
    print(cgr)
print()

print(int(ogr[0], 2) * int(cgr[0], 2))

