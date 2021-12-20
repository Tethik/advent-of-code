import sys


def square(y, x):
    return [(y-1, x-1), (y-1, x), (y-1, x+1), (y, x-1), (y, x), (y, x+1), (y+1, x-1), (y+1, x), (y+1, x+1)]


print(square(6, 2))


def iea_string(img, y, x):
    s = ""
    for y1, x1 in square(y, x):
        if y1 > len(img) - 1 or y1 < 0:
            s += "0"
            continue
        if x1 > len(img[y1]) - 1 or x1 < 0:
            s += "0"
            continue

        if img[y1][x1] == "#":
            s += "1"
        else:
            s += "0"
    return int(s, 2)


PADDING = 150  # I'LL GIVE YO PADDING


def pad(img):
    newimg = []
    for _ in range(PADDING):
        newimg.append(["."] * (len(img[0]) + PADDING * 2))
    for row in img:
        newimg.append([*(["."]*PADDING), *row, *(["."]*PADDING)])
    for _ in range(PADDING):
        newimg.append(["."] * (len(img[0]) + PADDING * 2))
    return newimg


algorithm = []
input_image = []

input_mode = False
for line in sys.stdin:
    if line.strip() == "":
        input_mode = True
        continue

    if input_mode:
        input_image.append(line.strip())
    else:
        algorithm.append(line.strip())

algorithm = "".join(algorithm)

# get pixel:


def enhance(img):
    # img = pad(img)
    # print("\n".join(["".join(r) for r in img]))
    # print()
    newimg = [r.copy() for r in img]
    for y in range(len(img)):
        for x in range(len(img[y])):
            idx = iea_string(img, y, x)
            # print(y, x, idx)
            newimg[y][x] = algorithm[idx]
    return newimg


img = pad(input_image)
print("Input")
# print("\n".join(["".join(r) for r in img]))
# print()

for i in range(50):
    img = enhance(img)

    if i % 2 == 1:
        for y in range(len(img)):
            img[y][0] = "."
            img[y][len(img[0]) - 1] = "."
        for x in range(len(img[0])):
            img[0][x] = "."
            img[len(img) - 1][x] = "."

    print(f"Enhance {i}")
    print("\n".join(["".join(r) for r in img]))
    print()

    c = 0
    for y in range(len(img)):
        for x in range(len(img[y])):
            if img[y][x] == "#":
                c += 1

    print(c)
    # print(c - len(img) - len(img[0]) + 1)
