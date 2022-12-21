import sys
from sympy import *

sys.setrecursionlimit(10500)

lines = []
for line in sys.stdin:
    parts = line.strip().split(":")
    name, value = parts[0].strip(), parts[1].strip()
    if name == "root":
        name = "ans"
        value = value.replace("+", "-")
    if name == "humn":
        continue
    lines.append((name, value))

# Simplify equations by removing trivial
solved = dict()
while True:
    before = len(solved)
    new_lines = []
    for name, value in lines:
        if name in solved:
            continue

        for key, val in solved.items():
            value = value.replace(key, str(val))

        new_lines.append((name, value))

        try:
            solved[name] = int(eval(value))
        except:
            pass
    print()
    lines = new_lines
    if before == len(solved):
        break


system = []
vars = []
for name, value in lines:
    if name == "root":
        name = "ans"

    if name in solved:
        continue

    vars.append(name)

    expr_str = name + " - (" + value + ")"
    print(expr_str)
    expr = sympify(expr_str)
    system.append(expr)

print()
print(vars)
print()

result = nonlinsolve(system, symbols(
    " ".join(vars)))

# print(result)
for solution in result:
    # print(solution)
    # print(solution[vars.index("ans")])
    print(solve(solution[vars.index("ans")], symbols("humn"))[0])
