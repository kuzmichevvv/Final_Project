from Settings import *
import pygame


text_map =[
'WWWWWWWWWWWW',
'W..........W',
'W.....W....W',
'W..........W',
'W...WW.....W',
'W..........W',
'W..........W',
'WWWWWWWWWWWW'
]
world_map = set()
collision_walls = []

for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char == 'W':
            world_map.add((i*TILE, j*TILE))
            collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
