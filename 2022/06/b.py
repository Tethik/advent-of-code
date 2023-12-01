import re
import sys

line = sys.stdin.readline()
buf = []
seen = set()
for i, c in enumerate(line):
    if len(buf) == 14:
        buf.pop()
    buf.insert(0, c)

    if len(set(buf)) == 14:
        print(i+1)
        break
