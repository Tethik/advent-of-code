import re
import sys
from collections import namedtuple
from pathlib import Path

lines = sys.stdin.read()
commands = lines.split("$")

cdpattern = re.compile("cd (.+)")
dirpattern = re.compile("dir (.+)")
filepattern = re.compile("(\d+) (.+)")

Node = namedtuple("Node", ["type", "path", "size", "parent", "children"])


# path = Path("/")
root = parent = Node("dir", "/", 0, None, [])
for c in commands:
    lines = c.strip().split("\n")
    if len(lines) == 0:
        continue

    cmd = lines[0].strip()
    # args = cmd.split(" ")
    output = lines[1:]

    print("cwd is " + str(parent.path))
    print("$", cmd)
    m = cdpattern.match(cmd)
    if m:
        name = m.group(1).strip()
        if name == "..":
            parent = parent.parent
            continue
        if name == "/":
            # might need path resolution here
            parent = root
            continue

        if not name in [c.path for c in parent.children]:
            node = Node("dir", name, 0, parent, [])
            parent.children.append(node)
            parent = node
            print("node added", name)
        else:
            print("folder already seen", name)
        continue

    for line in output:
        m = dirpattern.match(line)
        if m:
            continue
        m = filepattern.match(line)
        size, name = m.groups()

        if not name in [c.path for c in parent.children]:
            node = Node("file", name, int(size), parent, [])
            parent.children.append(node)
            print("node added", name)
        else:
            print("file already seen", name)


# Traverse tree
def printTree(node: Node, indent=0):
    print(indent*"  "+"-"+node.path, f"({node.type}, size={node.size})")
    for c in node.children:
        printTree(c, indent=indent+1)


def fileSize(node: Node):
    if node.type == "file":
        return node.size, []

    s = 0
    nodes = []
    for c in node.children:
        size, n = fileSize(c)
        s += size
        nodes += n

    return s, nodes + [(node.path, s)]


print()
printTree(root)

size, nodes = fileSize(root)
print(size)
print(nodes)
nodes = sorted(nodes, key=lambda n: n[1])
# nodes = list(filter(lambda n: n[1] < 100000, nodes))
print(nodes)
print(sum(n[1] for n in nodes))


free_space = 70000000 - size
space_needed = (free_space - 30000000)*-1
print(space_needed)

prev = nodes[-1]
for n in nodes[-2:0:-1]:
    if n[1] < space_needed:
        break
    prev = n

print(prev)
