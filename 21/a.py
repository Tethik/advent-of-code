import re
import sys
from functools import lru_cache
from queue import PriorityQueue, Queue
from typing import Dict, List


monkeys = dict()
solved = set()
for line in sys.stdin:
    parts = line.strip().split(":")
    assert parts[0] not in solved
    try:
        monkeys[parts[0].strip()] = int(parts[1])
        solved.add(parts[0].strip())
    except:
        arg = parts[1].strip().replace("/", "//")
        monkeys[parts[0].strip()] = lambda arg=arg: eval(arg)


while "root" not in solved:
    before = len(solved)
    locals().update(monkeys)
    for key, val in list(monkeys.items()):
        if key in solved:
            continue

        print("trying", key, val)
        try:
            monkeys[key] = val()
            print(key, monkeys[key])
            solved.add(key)
            locals().update(monkeys)
        except:
            pass
    print()

    assert before < len(solved)

print(monkeys["root"])
