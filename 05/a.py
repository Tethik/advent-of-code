import re
import sys


def contains(p1, p2):
    # Unpack the tuples to get the start and end of each range
    a, b = p1
    c, d = p2

    # Check if the ranges overlap by checking if the end of the first range
    # is greater than the start of the second range, and vice versa
    return (a <= d) and (b >= c)


INPUT_MODE = "stacks"
stacks = []
inst = []
for line in sys.stdin:
    if line.strip() == "":
        if INPUT_MODE == "stacks":
            INPUT_MODE = "instructions"
            continue
        else:
            break

    if INPUT_MODE == "stacks":
        stacks.append(line)
    else:
        inst.append(line.strip())

# Process stacks
last_line = stacks[-1]
n_cols = int(last_line.strip().split()[-1])
print(n_cols)

cols = [[] for _ in range(n_cols)]
for stack in stacks[:-1]:
    for i, col in enumerate(cols):
        c = stack[i*4:i*4+4].strip()
        if c == "":
            continue
        print(i*4, i+4, c)
        col.insert(0, c)

    print()


for ins in inst:
    print(ins)
    m = re.findall("\d+", ins)
    quantity, f, t = [int(v) for v in m]
    print(quantity, f, t)

    for _ in range(quantity):
        cols[t-1].append(cols[f-1].pop())

    for row in cols:
        print(row)
    # f, t = ins[len("move "1 from "):].split(" to ")

msg = ""
for col in cols:
    msg += col[-1]

print(msg.replace("[", "").replace("]", ""))
