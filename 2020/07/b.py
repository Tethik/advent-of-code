import sys
import re

rules = dict()
for line in sys.stdin:
    r1, r2 = line.strip().split(" contain")
    rules[r1] = re.sub(",", "+", r2)
    rules[r1] = re.sub("no other bags", "0", rules[r1])
    rules[r1] = re.sub("\.", "+ 0", rules[r1])

repl = gold = "shiny gold bags"
while repl:
    rules[gold] = re.sub(repl[:-1]+"s?", f"*(1 + {rules[repl]})", rules[gold])
    print(rules[gold])
    repl = next((r for r in rules.keys() if r[:-1] in rules[gold]), False)
    print(repl)


math = re.sub("[a-z]+", "+", rules[gold])
print(math)
print(eval(math))
