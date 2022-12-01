import sys

rules = [line.strip().split(" contain") for line in sys.stdin]
before = len(rules)

repl = gold = "shiny gold bag"

i = 0
while repl:
    rules = [(r[0].replace(repl+"s", gold), r[1].replace(repl, gold))
             for r in rules if r[0] != gold]
    # print(repl)
    # print(*rules, sep="\n")
    # print()
    repl = next((r[0][:-1] for r in rules if gold in r[1]), False)
    i += 1

after = len(rules)
print(before - after - 1)
