import re
import sys

line = sys.stdin.readline()
buf = []
seen = set()
for i, c in enumerate(line):
    if len(buf) == 4:
        buf.pop()
    buf.insert(0, c)

    if len(set(buf)) == 4:
        print(i+1)
        break
