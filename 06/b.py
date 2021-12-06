from collections import Counter

state = Counter([int(s) for s in input().split(",")])

days = 256

for _ in range(days):
    for i in range(0,9):        
        state[i-1] = state[i]

    state[8] = state[-1]
    state[6] += state[-1]
    state[-1] = 0
    
print(state)
print(sum(state[key] for key in state.keys()))