import json
import sys


def lazygetnum(line, s, rev=False):
    n = 0
    i = s
    d = -1 if rev else 1
    while i < len(line) and i > -1:
        c = line[i]
        if c in ["[", ",", "]"]:
            if n > 0:
                index = i - d if rev else i - n
                return int(line[index:index+n]), index, n
        else:
            n += 1
        i += d

    raise ValueError("no number here :(")


def explode(line):
    line = line.replace(" ", "")
    brackets = 0
    sb = 0
    while sb < len(line):
        c = line[sb]
        if c == "[":
            brackets += 1
        elif c == "]":
            brackets -= 1

        if brackets > 4:
            break
        sb += 1

    if sb >= len(line):
        return False

    eb = sb  # end brack
    for j in range(sb, len(line)):
        if line[j] == "]":
            eb = j+1
            break

    # print(sb, eb, line[sb:eb])

    # Checking that we didnt grab more than one pair accidentally
    if line[sb:eb].count("[") > 1:
        print(line)
        print(line[sb:eb])
        print(sb, eb)
        raise ValueError("Wat")

    left, right = line[sb+1:eb-1].split(",")

    # l = sb
    # while l > -1:
    #     c = line[l]
    #     if not c in ["[", ",", "]"]:
    #         break
    #     l -= 1

    # r = eb
    # while r < len(line):
    #     c = line[r]
    #     if not c in ["[", ",", "]"]:
    #         break
    #     r += 1

    s = ""

    leftnum = ""
    try:
        leftnum, lefti, length = lazygetnum(line, sb, rev=True)
    except Exception as ex:
        # print(ex)
        pass

    if leftnum != "":
        # print("left", leftnum, line[lefti], lefti, length)
        assert str(leftnum)[0] == line[lefti]
        s += line[:lefti]
        # print(s)
        _sum = str(leftnum + int(left))
        s += _sum
        # print(s)
        # print(line[lefti:lefti+length])
        s += line[lefti+length:sb]
        # print(s)
    else:
        s += line[:sb]

    s += "0"

    rightnum = ""
    try:
        rightnum, righti, length = lazygetnum(line, eb)
    except Exception as ex:
        # print(ex)
        pass

    if rightnum != "":
        # print("right", rightnum, line[righti], righti, length)
        assert str(rightnum)[0] == line[righti]

        s += line[eb:righti]
        _sum = str(rightnum + int(right))
        s += _sum
        s += line[righti+length:]
    else:
        s += line[eb:]

    return s


print("""
##################################
        explode tests
##################################
""")

print(explode("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"))
print()
assert explode(
    "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

# print(explode("[[1010,333],[2,[3,[4,[1000, 1337]]]]]"))
assert explode(
    "[[1010,333],[2,[3,[4,[1000, 1337]]]]]") == "[[1010,333],[2,[3,[1004,0]]]]"

# print(explode(
#     "[[[[12,12],[6,14]],[[15,0],[17,[8,1]]]],[2,9]]"))

# [[[[12,12],[6,14]],[[15,0],[17,0]]],[3,9]]
# [[[[12,12],[6,14]],[[15,0],[25,0]]],[3,9]]

assert explode(
    "[[[[12,12],[6,14]],[[15,0],[17,[8,1]]]],[2,9]]") == "[[[[12,12],[6,14]],[[15,0],[25,0]]],[3,9]]"

assert explode("[[[[[9,8],1],2],3],4]") == "[[[[0,9],2],3],4]"
assert explode("[7,[6,[5,[4,[3,2]]]]]") == "[7,[6,[5,[7,0]]]]"
print(explode("[[6,[5,[4,[3,2]]]],1]"))
assert explode("[[6,[5,[4,[3,2]]]],1]") == "[[6,[5,[7,0]]],3]"
assert explode(
    "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
assert explode(
    "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
print()


def split(line):
    line = line.replace(" ", "")  # lazy fix for some tests
    n = ""
    for i, c in enumerate(line):
        if c in ["[", ",", "]"]:
            if len(n) > 0:
                s = int(n)
                if s > 9:
                    d, r = divmod(s, 2)
                    return line[:i-len(n)] + f"[{d},{d+r}]" + line[i:]
                n = ""
            continue
        n += c

    return False


print("""
##################################
        split tests
##################################
""")

assert split("[10,10]") == "[[5,5],10]"
assert split("[11,10]") == "[[5,6],10]"
assert split("[0,10]") == "[0,[5,5]]"
assert split("[[1,2],10]") == "[[1,2],[5,5]]"
assert split("[[1,10],10]") == "[[1,[5,5]],10]"
assert split(
    "[[1,[1,[1,[1,10]]]],10]") == "[[1,[1,[1,[1,[5,5]]]]],10]"
print()


def reduce(line):
    j = 40
    # print("initial".ljust(j), line)
    while True:
        repl = explode(line)
        if repl:
            # print(f"after explode".ljust(j), repl)
            line = repl
            continue

        repl = split(line)
        if repl:
            # print("after split".ljust(j), repl)
            line = repl
            continue

        break
    # print("after reduce".ljust(j), line)

    return line


def add(line, line2):
    added = f"[{line},{line2}]"
    # print("after addition".ljust(40), added)
    return reduce(added)


print("""
##################################
        reduce tests
##################################
""")

print(add("[[[[4,3],4],4],[7,[[8,4],9]]]",
          "[1,1]"))
print()
assert add("[[[[4,3],4],4],[7,[[8,4],9]]]",
           "[1,1]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"


class Node:
    left = None
    right = None
    parent = None

    def __init__(self, parent, left, right) -> None:
        self.parent = parent
        if isinstance(left, list):
            print(left)
            self.left = Node(self, *left)
        else:
            self.left = left
        if isinstance(right, list):
            self.right = Node(self, *right)
        else:
            self.right = right

    def magnitude(self):
        m1 = 3 * (self.left.magnitude()
                  if isinstance(self.left, Node) else self.left)
        m2 = 2 * (self.right.magnitude()
                  if isinstance(self.right, Node) else self.right)
        return m1 + m2


def magnitude(line):
    n = Node(None, *json.loads(line))
    return n.magnitude()


if __name__ == "__main__":
    print("""
    ##################################
            main
    ##################################
    """)

    fish = None
    for line in sys.stdin:
        if line.strip() == "":
            continue

        if fish == None:
            fish = line.strip()
            continue

        fish = add(fish, line.strip())
        print(fish)
        print()

    print(magnitude(fish))
