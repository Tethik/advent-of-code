import sys
import math
import itertools

_, player1 = input().split(":")
_, player2 = input().split(":")
player1 = int(player1.strip())
player2 = int(player2.strip())

course_size = 10
die_sides = 100

pos = [player1-1, player2-1]
points = [0, 0]
curr_player = 0

die = 1
casts = 0

while all(point < 1000 for point in points):
    roll = 0
    for i in range(3):
        roll += die
        die = (die + 1) % die_sides # todo fix overflow
        casts += 1

    print(curr_player)
    print(roll)
    pos[curr_player] = (pos[curr_player] + roll) % course_size
    
        
    print(pos[curr_player])
    points[curr_player] += pos[curr_player] + 1
    print(points[curr_player])
    print()

    curr_player = (curr_player + 1) % 2


print(min(points), casts, min(points) * casts)
