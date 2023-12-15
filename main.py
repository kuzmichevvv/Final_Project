import pygame
from settings import *
from player import Player
from sprite_objects import *
from ray_casting import ray_casting_walls
from drawing import Drawing
from map import world_map, Map

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_visible(False)
sc_map = pygame.Surface(MINIMAP_RES)

monster = Monsters()
clock = pygame.time.Clock()
player = Player(monster)
drawing = Drawing(sc, sc_map)
map = Map(world_map)
font = pygame.font.SysFont('Arial', 30, bold=True)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement(map)

    if player.jump:
        player.jump_func()
    if player.shift:
        player.shift_func_pressed()

    monster.objects.move(player.pos, player.shift)

    if player.check_death(monster.objects):
        for i in range(8):
            sc.fill(BLACK)
            sprite = pygame.transform.scale(monster.monster_parameters['animation'][i], (800 + i * 100, 800 + i * 100))
            sc.blit(sprite, (200 - i * 50, - i * 50))
            pygame.display.flip()
            clock.tick(10)
        sc.fill(BLACK)
        render = font.render('You LOSE', 0, WHITE)
        sc.blit(render, (HALF_WIDTH - 100, HALF_HEIGHT))
        pygame.display.flip()
        clock.tick(1)
        break

    sc.fill(BLACK)

    drawing.background(player.angle)
    walls = ray_casting_walls(player, drawing.textures, map)
    drawing.world(walls + [monster.objects.object_locate(player)])
    drawing.fps(clock)
    drawing.mini_map(player)

    if player.take_eye_bool:
        render = font.render('You may press F and take eye', 0, WHITE)
        sc.blit(render, (500, 650))
    render = font.render(f'Count of eye:{player.count_of_eye}', 0, WHITE)
    sc.blit(render, (20, 20))
    if player.win:
        sc.fill(BLACK)
        render = font.render('You WON', 0, WHITE)
        sc.blit(render, (HALF_WIDTH - 100, HALF_HEIGHT))
        pygame.display.flip()
        clock.tick(1)
        break

    pygame.display.flip()
    clock.tick(FPS)
