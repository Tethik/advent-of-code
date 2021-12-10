import sys
import statistics

pairings = [    
    ('(',')', 3, 1),
    ('[',']', 57, 2),
    ('{','}', 1197, 3),
    ('<','>', 25137, 4),    
]

def findPairing(c):
    for start, end, score, complete_score in pairings:
        if start == c or end == c:
            return (start, end, score, complete_score)

points = 0
complete_scores = []
for i, line in enumerate(sys.stdin):
    stack = []
    corrupted = False
    for j, c in enumerate(line):
        pair = findPairing(c)
        if pair == None:
            continue
        start, end, score, _ = pair

        if end == c:
            _, expected, _, _ = findPairing(stack.pop())            
            if c != expected:
                print(f"Line: {i}, Col: {j}. Expected {expected} but found {c} instead! ")
                points += score
                corrupted = True           
                break
        else:
            stack.append(c)

        if corrupted:
            break
    
    if not corrupted:
        score = 0
        rev = []
        for c in stack[::-1]:
            score *= 5
            _, e, _, s = findPairing(c)
            rev.append(e)
            score += s
            print(c, e, score)
        print(f"Line: {i} is incomplete. {''.join(rev)}. score: {score}")
        # points += score
        complete_scores.append(score)

m = statistics.median(complete_scores)
print(m)
points += m

print(points)
