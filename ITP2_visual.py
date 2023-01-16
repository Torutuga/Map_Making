import pygame
from ITP2_builder import map, height, width

clr_cream = [(167, 190, 211),(241, 255, 196),(245, 213, 203)]
clr_strong = [(0,0,200),(0,200,0),(111,55,0)]

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mapping in Python")

clock = pygame.time.Clock()

off_x = 0
off_y = 0
stage = 0

run = True
pallete = clr_strong
while run:

    screen.fill((0,0,0))

    # Naranja
    set_x = 20
    set_y = 50
    pos1 = [set_x, set_y]
    pos2 = [set_x, set_y]
    for y in range(height):
        set_y = set_y + y*2
        for x in range(width):
            value = map[y][x]
            color = pallete[1]
            if stage >= 1:
                if value > 15:
                    color = pallete[2]
                if value == 0:
                    value = 6
                    color = pallete[0]
            pos2 = [set_x + x*2, set_y - value*stage]
            if x != 0:
                pygame.draw.line(screen, color, (pos1), (pos2))
                pygame.draw.line(screen, (0,0,0), (pos1[0],pos1[1]+2), (pos2[0],pos2[1]+2), width=2)
            pos1 = pos2
        set_y = 50
        pos1 = [set_x, set_y]
        pos2 = [set_x, set_y]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            print(stage)

    if stage <= 1.0:
        stage += 0.1
        
    clock.tick(15)
    pygame.display.update()