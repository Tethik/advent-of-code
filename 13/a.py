import sys

folds = []
input_folds = False
grid = dict()
max_x = 0
max_y = 0
for line in sys.stdin:
    if line.strip() == "":
        input_folds = True
        continue

    if input_folds:
        axis, val = line.split(" ")[2].split("=")
        folds.append((axis, int(val)))        
    else:
        x, y = line.split(",")
        max_x = max(max_x, int(x))
        max_y = max(max_y, int(y))
        grid[(int(x),int(y))] = True


# Bet we will need a function for this..
axis, val = folds[0]
print("fold ", axis, "=", val)
keys = list(grid.keys())
if axis == "y": 
    for x,y in keys:
        if y < val:
            continue
        grid[(x, val - (y - val))] = True
        grid[(x, y)] = False
elif axis == "x":
    for x,y in keys:
        if x < val:
            continue
        grid[(val - (x - val), y)] = True
        grid[(x, y)] = False

print(len([v for k,v in grid.items() if v == True]))