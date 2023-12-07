import math

import pygame
from Settings import *
from Map import world_map

def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


def ray_casting(sc, player_pos, player_angle,player_proj_coeff):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - HALF_FOV
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        # verticals
        if(cos_a>0):
            x=xm+TILE
            dx=1
        else:
            x=xm
            dx=-1
        for i in range(0, WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            y = oy + depth_v * sin_a
            if mapping(x + dx, y) in world_map:
                break
            x += dx * TILE

        # horizontals
        if (sin_a > 0):
            y = ym + TILE
            dy = 1
        else:
            y = ym
            dy = -1
        for i in range(0, HEIGHT, TILE):
            depth_h = (y - oy) / sin_a
            x = ox + depth_h * cos_a
            if mapping(x, y + dy) in world_map:
                break
            y += dy * TILE

        # projection
        depth = depth_v if depth_v < depth_h else depth_h
        depth *= math.cos(player_angle - cur_angle) + 0.01
        proj_coeff = player_proj_coeff / depth
        proj_coeff1 = PROJ_COEFF/depth
        c=255/(1+depth**2*0.0001)
        color=(c,c,c)
        pygame.draw.rect(sc,color,(ray*SCALE, HALF_HEIGHT-proj_coeff/2,SCALE,proj_coeff1))
        cur_angle+=DELTA_ANGELS
