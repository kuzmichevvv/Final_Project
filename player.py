import math

from Settings import *
import pygame
from Map import collision_walls

class Player():
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.proj_coeff = PROJ_COEFF
        self.delta_speed = 0
        self.jump_v = -1000
        self.jump = False
        self.shift_v = 10000
        self.shift = False
        self.shift_shift = True
        self.side = 20
        self.rect = pygame.Rect(*player_pos, self.side, self.side)

    def jump_func(self):
        self.proj_coeff += self.jump_v
        self.jump_v += 20
        if self.proj_coeff >= PROJ_COEFF:
            self.proj_coeff = PROJ_COEFF
            self.jump = False
            self.jump_v = -1000

    def shift_func_pressed(self):
        if self.shift_shift:
            self.proj_coeff += self.shift_v
            self.delta_speed = 0.4 * 3
            self.shift_shift = False

        keys = pygame.key.get_pressed()
        if not keys[pygame.K_LSHIFT] and not keys[pygame.K_RSHIFT]:
            self.shift = False
            self.proj_coeff -= self.shift_v
            self.delta_speed = 0
            self.shift_shift = True

    def pos(self):
        return self.x, self.y

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(collision_walls)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = collision_walls[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_x < delta_y:
                dx = 0

        self.x += dx
        self.y += dy

    def movement(self):
        self.rect.center = self.x, self.y

    def move(self):
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            dx = (player_speed - self.delta_speed) * cos_a
            dy = (player_speed - self.delta_speed) * sin_a
            self.detect_collision(dx, dy)
            self.movement()
        if keys[pygame.K_a]:
            dx = (player_speed - self.delta_speed) * sin_a
            dy = -(player_speed - self.delta_speed) * cos_a
            self.detect_collision(dx, dy)
            self.movement()
        if keys[pygame.K_d]:
            dx = -(player_speed - self.delta_speed) * sin_a
            dy = (player_speed - self.delta_speed) * cos_a
            self.detect_collision(dx, dy)
            self.movement()
        if keys[pygame.K_s]:
            dx = -(player_speed - self.delta_speed) * cos_a
            dy = -(player_speed - self.delta_speed) * sin_a
            self.detect_collision(dx, dy)
            self.movement()
        if keys[pygame.K_RIGHT]:
            self.angle += 0.01
        if keys[pygame.K_LEFT]:
            self.angle -= 0.01
        if keys[pygame.K_SPACE]:
            self.jump = True
        if keys[pygame.K_LSHIFT]:
            self.shift = True
        if keys[pygame.K_RSHIFT]:
            self.shift = True
