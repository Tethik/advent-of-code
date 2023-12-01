import sys


def compare(left, right, pad=0):
    padding = " " * pad
    print()
    print(padding, "===== Compare ====")
    print(padding, left)
    print(padding, right)
    i = 0

    # If the left list runs out of items first, the inputs are in the right order.
    # If the right list runs out of items first, the inputs are not in the right order.
    # If the lists are the same length and no comparison makes a decision about the order,
    # continue checking the next part of the input.
    result = "unknown"
    # if len(left) > len(right):
    #     print(padding, "len(left) != len(right)", len(
    #         left), len(right), len(left) < len(right))
    #     result = len(left) < len(right)

    while left:
        if not right:
            print(padding, "right ended before left")
            result = False
            break

        l, r = left.pop(0), right.pop(0)

        if all(isinstance(item, int) for item in [l, r]):
            if l > r or l < r:
                result = l < r
                break

        elif any(isinstance(item, list) for item in [l, r]):
            if isinstance(l, int):
                l = [l]
            if isinstance(r, int):
                r = [r]

            subResult, j = compare(l, r, pad=pad+2)
            if subResult != "unknown":
                result = subResult
                i += j
                break
        i += 1

    if not left and right and result == "unknown":
        print(padding, "left ended before right")
        result = True

    print(padding, result, i)
    print(padding, "===== End Compare ====")
    print()
    return result, i


pair = []
pairs = []
for line in sys.stdin:
    line = line.strip()
    if line == "":
        pairs.append(pair)
        pair = []
    else:
        pair.append(eval(line))

if len(pair) > 0:
    pairs.append(pair)

p = 1
ps = []
for pair in pairs:
    assert len(pair) == 2
    # print(pair)
    print(f"== Pair {p} ==")
    correct, i = compare(*pair)
    assert correct != "unknown"
    # print(correct, i)
    if correct:
        ps.append(p)
    p += 1


print(sum(ps))
print(ps)
