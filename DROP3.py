import random, math, numpy as np
from opensimplex import OpenSimplex

def Depositer(map, pos, amnt):
    y = int(pos[0])
    x = int(pos[1])

    v = y - pos[0]
    u = x - pos[1]

    map[y][x] += amnt * (1-u) * (1-v)
    map[y][x+1] += amnt * u * (1-v)
    map[y+1][x] += amnt * (1-u) * v
    map[y+1][x+1] += amnt * u * v

def Eroder(h, w, pos, map, amnt, radius=2):

    y0 = int(pos[0]) - radius
    x0 = int(pos[1]) - radius
    y_sta = np.maximum(0, y0)
    x_sta = np.maximum(0, x0)
    y_end = np.minimum(h, y0+2*radius+1)
    x_end = np.minimum(w, x0+2*radius+1)

    positions = []
    positions_sum = 0
    for y in range(y_sta,y_end):
        positions.append([])
        for x in range(x_sta,x_end):
            d_y = y-pos[0]
            d_x = x-pos[1]
            dist = math.sqrt(d_y**2 + d_y**2)
            w = np.maximum(0, radius - dist)
            positions[y-y0].append(w)
            positions_sum += w

    for y in range(y_sta,y_end):
        for x in range(x_sta,x_end):
            positions[y-y0][x-x0] /= positions_sum
            map[y][x] -= amnt*positions[y-y0][x-x0]
    
    return positions_sum

def GRAD(h, w, x, y, map):
    if x < w - 2:
        rgt = map[y][x+1]
    else:
        rgt = map[y][x]
    if y < h - 2:
        blw = map[y+1][x]
    else:
        blw = map[y][x]
    
    return np.array([rgt - map[y][x], blw - map[y][x]])

def LINT(pos,x0,y0,x1,y1):
    value = y0*(x1-pos) + y1*(pos-x0)
    return value / (x1-x0)

def H_BINT(x, y, pos, map):

    top = LINT(pos[1], x, map[y][x],x+1, map[y][x+1])
    bot = LINT(pos[1], x, map[y+1][x],x+1, map[y+1][x+1])

    return LINT(pos[0], y, top, y+1, bot)

def GRAD_HIGT(h, w, pos, map):

    y = int(pos[0])
    x = int(pos[1])
    a = pos[0] - y
    b = pos[1] - x
    
    tl = GRAD(h,w,x,y, map)
    tr = GRAD(h,w,x+1,y, map)
    bl = GRAD(h,w,x,y+1, map)
    br = GRAD(h,w,x+1,y+1, map)

    lft = (1-a)*tl + a*bl
    rgt = (1-a)*tr + a*br

    grd = (1-b)*lft + b*rgt
    hgt = H_BINT(x, y, pos, map)
    return grd, hgt

# green = []
# blue = []

# height = 200
# width = 350

# seed1 = OpenSimplex(41)
# seed2 = OpenSimplex(51)
# seed3 = OpenSimplex(61)

# print("Generating Blue Map")
# for y in range(height):
#     blue.append([])
#     green.append([])
#     for x in range(width):
#         # Rojo
#         value1f = seed1.noise2(100+x/48.0, 100+y/48.0)*5
#         value2f = seed2.noise2(x/12.0, y/12.0)
#         value3f = seed3.noise2(x/6.0, y/6.0)*0.5
#         value1 = (value3f+value2f+value1f+5)*0.1
#         blue[y].append(value1)
#         green[y].append(value1)

