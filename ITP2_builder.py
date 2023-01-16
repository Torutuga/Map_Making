from opensimplex import OpenSimplex
import math

red = []
white = []
blue = []
map = []

height = 200
width = 350

seed1 = OpenSimplex(462)
seed2 = OpenSimplex(781)
seed3 = OpenSimplex(523)

for y in range(height):
    red.append([])
    white.append([])
    blue.append([])
    for x in range(width):
        # Rojo
        value1f = seed1.noise2(x/12.0, y/12.0)
        value1 = int((value1f+1)*20)
        red[y].append(value1)
        # Blanco
        value3f = seed3.noise2(x/60.0, y/60.0)
        value3 = int((value3f+1)*10)
        white[y].append(value3)
        # Azul (Blanco con Placas)
        if value3f >= 0:
            blue[y].append(2)
        if value3f < 0 and value3f >= -0.3:
            blue[y].append(1)
        if value3f < -0.3:
            blue[y].append(0)

# Naranja (Combinations)
for y in range(height):
    map.append([])
    for x in range(width):
        if blue[y][x] == 0:
            map[y].append(0)
        if blue[y][x] == 1:
            map[y].append(white[y][x])
        if blue[y][x] == 2:
            distance = 10
            
            for a in range(y-10, y+10):
                for b in range(x-10, x+10):
                    try:
                        point = blue[a][b]
                        if point == 1 or point == 0:
                            dst = math.sqrt((b-x)**2 + (y-a)**2)
                            if dst <= distance:
                                distance = int(dst)
                    except IndexError:
                        pass

            value = white[y][x]*(1-(distance*0.1)) + red[y][x]*(distance*0.1)
            map[y].append(int(value))