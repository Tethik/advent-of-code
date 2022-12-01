"""
This code is extremely slow, but it solves the task
without too many assumptions about the input.

real	48m15,791s
user	45m54,283s
sys	2m18,723s
"""

import sys
import json
from collections import namedtuple
from typing import List, Set

vars = ["x", "y", "z", "w"]
Registry = namedtuple("Registry", vars)

ops = {
    "inp": lambda registry, _: registry[3],
    # "set": lambda a, b: b,
    "add": lambda registry, a, b: registry[a]+registry[b],
    "addi": lambda registry, a, b: registry[a]+b,
    "mul": lambda registry, a, b: registry[a]*registry[b],
    "muli": lambda registry, a, b: registry[a]*b,
    "div": lambda registry, a, b: registry[a]//registry[b],
    "divi": lambda registry, a, b: registry[a]//b,
    "mod": lambda registry, a, b: registry[a] % registry[b],
    "modi": lambda registry, a, b: registry[a] % b,
    "eql": lambda registry, a, b: int(registry[a] == registry[b]),
    "eqli": lambda registry, a, b: int(registry[a] == b)
}


def op_to_str(op):
    for key, val in ops.items():
        if val == op:
            return key


class Program:
    def __init__(self, instructions):
        self.instructions = instructions
        self.parameters = self.analyze_parameters()

    def analyze_parameters(self):
        # analyze the program to see which parameters matter
        # potential todo: check for modulo
        not_required = set()
        required = set()
        trimmable_instructions = set()
        for i, ins in enumerate(self.instructions):
            op, args = ins
            sop = op_to_str(op)

            if sop == "muli" and args[1] == 0:
                if args[0] not in required:
                    not_required.add(args[0])

            if sop == "divi" and args[1] == 1:
                trimmable_instructions.add(i)

            if sop == "addi" and args[1] == 0:
                trimmable_instructions.add(i)

            if "i" not in sop:  # this works out for inp also ;)
                required.add(args[1])

        new_instructions = []
        for i, ins in enumerate(self.instructions):
            if i not in trimmable_instructions:
                new_instructions.append(ins)

        self.instructions = new_instructions

        return required - not_required

    def run(self, registry):
        l = list(registry)
        for instruction in self.instructions:
            op, args = instruction
            l[args[0]] = op(l, *args)
            # print(op_to_str(op), args)
            # print(l)
        l[3] = 0
        return Registry(*l)


programs: List[Program] = []
instructions = []
for line in sys.stdin:
    parts = line.strip().split(" ")
    ins = parts[0]
    args = parts[1:]

    for i, a in enumerate(args):
        try:
            args[i] = vars.index(a)
        except:
            args[i] = int(a)
            ins = ins+"i"

    op = ops[ins]
    # print(ins, args)
    if ins == "inp" and len(instructions) > 0:
        programs.append(Program(instructions))
        instructions = []
    instructions.append((op, args))

programs.append(Program(instructions))

for p in programs:
    print(p.parameters)


class State:
    def __init__(self, registry, path) -> None:
        self.registry = registry
        self.path = path


# for each program, solve states
input_states: List[State] = [State(Registry(0, 0, 0, 0), [])]
for p, prog in enumerate(programs):
    print(f"Computering Program {p}...")
    print(len(input_states), "inputs to explore")
    # print(prog)

    next_prog = programs[p+1] if p < len(programs) - 1 else None

    seen_outputs = set()
    output_states = []

    for w in range(1, 10):
        for state in input_states:
            reg = Registry(state.registry.x, state.registry.y,
                           state.registry.z, w)

            # print("Input", reg)
            output = prog.run(reg)
            # print("Output", output)

            if next_prog:
                o = list(output)
                for i, _ in enumerate(output):
                    if i not in next_prog.parameters:
                        o[i] = 0
                output = Registry(*o)
                # print(output)

            if output in seen_outputs:
                continue

            seen_outputs.add(output)
            output_states.append(State(output, [*state.path, w]))
            # print()

    input_states = list(output_states)
    print()


input_states = sorted(input_states, key=lambda s: s.registry.w)
for s in input_states:
    if s.registry.z == 0:
        print(s.path)
