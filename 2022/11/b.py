import math
import yaml
import sys
import re

monkeys = yaml.load(sys.stdin.read().replace(
    "  If", "If"), Loader=yaml.CLoader)

print(monkeys)


# Some preprocessing
totaldiv = 1
for key in monkeys.keys():
    monkey = monkeys[key]
    if isinstance(monkey["Starting items"], int):
        monkey["items"] = [monkey["Starting items"]]
    else:
        monkey["items"] = [int(i) for i in monkey["Starting items"].split(",")]
    monkey["inspect"] = lambda old: eval(monkey["Operation"].replace(
        "new = ", ""), globals(), {"old": old})
    monkey["test"] = lambda new: new % int(
        monkey["Test"].replace("divisible by ", "")) == 0
    totaldiv *= int(
        monkey["Test"].replace("divisible by ", ""))
    monkey["throw"] = lambda o: monkey["If true"].replace(
        "throw to ", "").capitalize() if o else monkey["If false"].replace("throw to ", "").capitalize()
    monkey["inspected"] = 0


for i in range(10000):
    for key in monkeys.keys():
        monkey = monkeys[key]
        # print(key)
        monkey["inspected"] += len(monkey["items"])
        while monkey["items"]:
            item = monkey["items"].pop()
            new = monkey["inspect"](item) % totaldiv
            # new = new % totaldiv

            # print(item, new)
            t = monkey["test"](new)
            # print(t)
            friend = monkey["throw"](t)
            # print(friend)
            assert friend != key, f"{friend} {key}"
            monkeys[friend]["items"].append(new)
        # print()

    # print()
    # print(i)
    # for key in monkeys.keys():
    #     monkey = monkeys[key]
    #     print(key, monkey["inspected"])


times = []
for key in monkeys.keys():
    monkey = monkeys[key]
    times.append(monkey["inspected"])

print(math.prod(sorted(times)[-2:]))
