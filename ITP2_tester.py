import pygame, math, random, numpy as np
from opensimplex import OpenSimplex
from DROP3 import Eroder, Depositer, GRAD_HIGT, H_BINT

red = []
green = []
blue = []

height = 200
width = 350

seed1 = OpenSimplex(41)
seed2 = OpenSimplex(51)
seed3 = OpenSimplex(61)

for y in range(height):
    blue.append([])
    green.append([])
    for x in range(width):
        # Rojo
        value1f = seed1.noise2(100+x/48.0, 100+y/48.0)*5
        value2f = seed2.noise2(x/12.0, y/12.0)
        value3f = seed3.noise2(x/6.0, y/6.0)*0.5
        value1 = (value3f+value2f+value1f+5)*0.1
        blue[y].append(value1)
        green[y].append(value1)

##############################################################################################################################################
##############################################################################################################################################

### Hydraulic Erosion :D
# Initial position

inertia = 0.01
min_slope = 0.01
evaporation = 0.1
gravity = 4
erotion = 0.1
deposition = 0.1
capacity = 10
max_path = 60

for drops in range(10):
    drop = np.array([random.uniform(2.0,float(height-1)),random.uniform(2.0,float(width-1))])
    wtr = 1.0
    sed = 0.0
    vel = 1.0
    dir = np.array([0,0])

    for steps in range(max_path):
        g, h = GRAD_HIGT(height, width, drop, blue)
        dir = dir*inertia - g*(1-inertia)
        nrml = dir / math.sqrt(dir[0]**2 + dir[1]**2)
        drop_new = drop + nrml

        if drop_new[0] > height-1 or drop_new[1] > width-1:
            break
        if drop_new[0] < 2 or drop_new[1] < 2:
            break

        h_new = H_BINT(int(drop_new[1]), int(drop_new[0]), drop_new, blue)
        h_dif = h_new - h
        c = np.maximum(-h_dif, min_slope)*vel*wtr*capacity

        if sed > c:
            total_depo = (sed-c)*deposition
            sed -= total_depo 
            Depositer(blue, drop, total_depo)
        else:
            if h_dif < 0.0:
                total_depo = min(sed, h_dif)
                sed -= total_depo
                Depositer(blue, drop, total_depo)
            else:
                total_eros = np.minimum((c-sed)*erotion, -h_dif)
                sed += total_eros
                Eroder(height, width, drop, blue, total_eros)
        try:
            vel = math.sqrt(vel*vel + h_dif*gravity)
        except ValueError:
            break
        wtr = wtr*(1-evaporation)
        drop = drop_new


for y in range(height):
    red.append([])
    for x in range(width):
        red[y].append(int(blue[y][x]*100)-30)

# for x in coordinates:
#     print(x)
#     amnt = int(green[x[0]][x[1]]*100)-30
#     print(f"Red: {red[x[0]][x[1]]} Blue: {amnt}")

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Mapping in Python")

run = True
while run:

    screen.fill((0,0,0))

    # Naranja
    set_x = 20
    set_y = 80
    pos1 = [set_x, set_y]
    pos2 = [set_x, set_y]
    for y in range(height):
        set_y = set_y + y*2
        for x in range(width):
            value = red[y][x]
            color = (0,200,200)
            pos2 = [set_x + x*2, set_y - value]
            if x != 0:
                pygame.draw.line(screen, color, (pos1), (pos2))
                pygame.draw.line(screen, (0,0,0), (pos1[0],pos1[1]+2), (pos2[0],pos2[1]+2), width=2)
            pos1 = pos2
        set_y = 80
        pos1 = [set_x, set_y]
        pos2 = [set_x, set_y]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()