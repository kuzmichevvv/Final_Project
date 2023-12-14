import pygame
from Settings import *
import Player
from ray_casting import ray_casting
from drawing import Drawing

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player = Player.Player()
drawing=Drawing(sc)
all_sprites = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    sc.fill(BLACK)

    if player.jump:
        player.jump_func()
    if player.shift:
        player.shift_func_pressed()

    player.move()
    drawing.background()

    drawing.world(player.pos(),player.angle, player.proj_coeff)
    all_sprites.draw(sc)
    drawing.fps(clock)

    pygame.display.flip()
    clock.tick()
