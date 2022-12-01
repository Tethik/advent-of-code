import sys

m = -1
b = []
mxs = []
for line in sys.stdin:
    i = line.strip()
    print(i)
    if i == "":
        v = sum(b)
        print(b, v)
        if v > m:
            m = v
        b = []
        mxs.append(v)
    else:
        b.append(int(i))


print(mxs[0])


v = sum(b)
print(b, v)
if v > m:
    m = v
mxs.append(v)
mxs = sorted(mxs)

print(mxs[-3:], sum(mxs[-3:]))
print(m)
