import functools
import sys


def compare(leftOrig, rightOrig, pad=0):
    padding = " " * pad

    # Hack because we need to keep original arrays
    left = leftOrig.copy()
    right = rightOrig.copy()
    print()
    print(padding, "===== Compare ====")
    print(padding, left)
    print(padding, right)

    result = 0

    while left:
        if not right:
            print(padding, "right ended before left")
            result = 1
            break

        l, r = left.pop(0), right.pop(0)

        if all(isinstance(item, int) for item in [l, r]):
            if l > r or l < r:
                result = (l - r) // abs(l - r)
                break

        elif any(isinstance(item, list) for item in [l, r]):
            if isinstance(l, int):
                l = [l]
            if isinstance(r, int):
                r = [r]

            subResult = compare(l, r, pad=pad+2)
            if subResult != 0:
                result = subResult
                break

    if not left and right and result == 0:
        print(padding, "left ended before right")
        result = -1

    print(padding, result)
    print(padding, "===== End Compare ====")
    print()

    return result


packets = [[[2]], [[6]]]
for line in sys.stdin:
    line = line.strip()
    if line == "":
        continue
    packets.append(eval(line))


print(compare([1, [2, [3, [4, [5, 6, 0]]]], 8, 9], [[[]]]))

packets = sorted(packets, key=functools.cmp_to_key(compare))

for i, p in enumerate(packets):
    print(i+1, p)

print((packets.index([[2]])+1), (packets.index([[6]])+1),
      (packets.index([[2]])+1) * (packets.index([[6]])+1))
