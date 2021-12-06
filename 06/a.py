state = [int(s) for s in input().split(",")]
days = 256

# naive solution
for _ in range(days):
    new_fish = 0
    for i in range(len(state)):        
        state[i] -= 1
        if state[i] == -1:
            state[i] = 6
            new_fish += 1

    state += [8] * new_fish
    # print(state)

print(len(state))