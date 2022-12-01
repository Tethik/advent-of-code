import sys

pairings = [    
    ('(',')', 3),
    ('[',']', 57),
    ('{','}', 1197),
    ('<','>', 25137),    
]

def findPairing(c):
    for start, end, score in pairings:
        if start == c or end == c:
            return (start, end, score)

points = 0
for i, line in enumerate(sys.stdin):
    stack = []
    found = False
    for j, c in enumerate(line):
        pair = findPairing(c)
        if pair == None:
            continue
        start, end, score = pair

        if end == c:
            _, expected, _ = findPairing(stack.pop())            
            if c != expected:
                print(f"Line: {i}, Col: {j}. Expected {expected} but found {c} instead! ")
                points += score
                found = True           
                break
        else:
            stack.append(c)

        if found:
            break

print(points)
