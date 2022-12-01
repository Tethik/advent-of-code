import sys
import math
import itertools

_, player1 = input().split(":")
_, player2 = input().split(":")
player1 = int(player1.strip())
player2 = int(player2.strip())

course_size = 10

pos = (player1-1, player2-1)
points = (0, 0)

rolls = [sum(roll) for roll in itertools.product([1,2,3], repeat=3)]
print(rolls)

wins = [0, 0]
states = [dict({(pos, points): 1})]
print(states)

target = 21 # less than 20 steps, surely.

for t in range(1, target):    
    states.append(dict())
    curr_player = (t - 1) % 2
    for state in states[t-1].keys():
        pos, points = state
        for roll in sorted(rolls):
            newpos = list(pos)
            newpoints = list(points)
            newpos[curr_player] = (newpos[curr_player] + roll) % course_size
            newpoints[curr_player] += newpos[curr_player] + 1

            if newpoints[curr_player] >= target:
                wins[curr_player] += states[t-1][state]
                continue

            newstate = (tuple(newpos), tuple(newpoints))
            # print(newstate)            
            if not newstate in states[t]:
                states[t][newstate] = states[t-1][state] 
            else:
                states[t][newstate] += states[t-1][state]

    print(states[t])
    print()
            
print("Was".ljust(40),wins)
print("Expected".ljust(40), [444356092776315, 341960390180808])
print(max(wins))
