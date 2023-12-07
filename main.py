import pygame
from  Settings import *
import Player
from ray_casting import ray_casting
from drawing import Drawing

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock =pygame.time.Clock()
player = Player.Player()
drawing=Drawing(sc)

while(True):
    for event in pygame.event.get():
        if(event.type== pygame.QUIT):
            exit()

    sc.fill(BLACK)

    if player.jump:
        player.jump_func()
    if player.shift:
        player.shift_func()

    player.move()
    drawing.background()

    drawing.world(player.pos(),player.angle, player.proj_coeff)
    drawing.fps(clock)
    # pygame.draw.circle(sc,GREEN,(int(player.x),int(player.y)),12)
    # pygame.draw.line(sc,GREEN,(int(player.x),int(player.y)),((player.x+WIDTH*math.cos(player.angle)),(player.y+WIDTH*math.sin(player.angle))))

    # for x,y in world_map:
    #     pygame.draw.rect(sc,GREEN,(x,y,TILE,TILE), 2)
    pygame.display.flip()
    clock.tick()
