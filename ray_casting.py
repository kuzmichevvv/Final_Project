import math

import pygame
from Settings import *
from Map import world_map
def ray_casting(sc,player_pos,player_angle):
    cur_angle = player_angle-HALF_FOV
    x0,y0 =player_pos
    for ray in range(NUM_RAYS):
        sin_a=math.sin(cur_angle)
        cos_a=math.cos(cur_angle)
        for depth in range(MAX_DEPTH):
            x=x0+depth*cos_a
            y=y0+depth*sin_a
            # pygame.draw.line(sc,WHITE,player_pos,(x,y),2)
            if(x//TILE*TILE,y//TILE*TILE) in world_map:
                depth*=math.cos(player_angle-cur_angle)
                proj_coeff= PROJ_COEFF/depth
                c=255/(1+depth**2*0.0001)
                color=(c,c,c)
                pygame.draw.rect(sc,color,(ray*SCALE, HALF_HEIGHT-proj_coeff/2,SCALE,proj_coeff))
                break
        cur_angle+=DELTA_ANGELS