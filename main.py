import pygame
from  Settings import *
import Player
import math
from Map import world_map
from ray_casting import ray_casting

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock =pygame.time.Clock()
player = Player.Player()

while(True):
    for event in pygame.event.get():
        if(event.type== pygame.QUIT):
            exit()

    sc.fill(BLACK)

    player.move()
    ray_casting(sc,(player.x,player.y),player.angle)
    # pygame.draw.circle(sc,GREEN,(int(player.x),int(player.y)),12)
    # pygame.draw.line(sc,GREEN,(int(player.x),int(player.y)),((player.x+WIDTH*math.cos(player.angle)),(player.y+WIDTH*math.sin(player.angle))))

    # for x,y in world_map:
    #     pygame.draw.rect(sc,GREEN,(x,y,TILE,TILE), 2)
    pygame.display.flip()
    clock.tick(FPS)
