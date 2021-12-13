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


def fold(axis, val):        
    print("fold ", axis, "=", val)
    keys = list(grid.keys())
    if axis == "y": 
        for x,y in keys:
            if y < val:
                continue
            grid[(x, y)] = False
            grid[(x, val - (y - val))] = True
            
    elif axis == "x":
        for x,y in keys:
            if x < val:
                continue
            grid[(x, y)] = False
            grid[(val - (x - val), y)] = True
            

def printGrid():    
    for y in range(max_y):
        s = ""
        for x in range(max_x):
            s += "#" if (x,y) in grid and grid[(x,y)] else "."
        print(s)


for axis, val in folds:
    fold(axis, val)
    printGrid()
    print()


