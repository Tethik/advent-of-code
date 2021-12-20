import math

partX, partY = input().replace("target area:", "").strip().split(", ")
minx,maxx = [int(p) for p in partX.replace("x=", "").split("..")]
miny,maxy = [int(p) for p in partY.replace("y=", "").split("..")]

print(minx,maxx,miny,maxy)

drag = lambda x: x - 1 if x > 0 else x
# print(drag(-1), drag(2))
gravity = lambda y: y - 1

def steps(v):
    c = (0,0)
    # print(c)
    # print(v)
    # print()
    s = 0
    while True:
        c = (c[0] + v[0], c[1] + v[1])
        v = (drag(v[0]), gravity(v[1]))
        s += 1
        # print(c)
        # print(v)
        # print()
        if minx <= c[0] <= maxx and miny <= c[1] <= maxy:
            return s
        if c[1] < miny or c[0] > maxx:
            break
    return None

# print(steps((7,2)))

# naive solution first..
# maxsteps = 0
# for vx in range(minx // 2, maxx):
#     for vy in range(miny, 1000):
#         ydiff = vy 
#         v = (vx,vy)
#         s = steps(v)
#         if s and maxsteps < s:
#             maxsteps = s
#             print(vy, s, sum(vy-i for i in range(vy)))

# naive solution
vxy = 0
yrange = int(abs(maxy)) * 100
print(maxx, yrange)
landed = 0

for x in range(maxx):
    for y in range(yrange):
        v = (x,y)
        s = steps(v)        
        # print(v, s)
        if s:            
            landed += 1
            vxy = max(y, vxy)

print(vxy, (vxy ** 2 + vxy) // 2)
print(vxy, sum(vxy - i for i in range(vxy)))
print(landed)

# def steps_x(v, mi, ma):
#     x = 0    
#     s = 0
#     while x < ma:
#         x += v
#         s += 1
#         if mi <= x <= ma:
#             return s    
#     return None




# # integer solutions..
vxs = []
min_vx = 1
for n in range(1, maxx):    
    end = (n**2 + n) // 2
    # print(n, end)
    min_vx = n
    if end > maxx:
        break

for vx in range(min_vx, maxx+1):
    # how many steps to reach?
    s = steps_x(vx, minx, maxx)    
    print(vx, s)
    print()

    # what is best vy?
    for y in range(maxy, miny+1):
        vy, r = divmod(y, s)
        print(vy, r)
        if r == 0:
            print(vx, vy)

    
    