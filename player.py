from settings import *
import pygame
import math
from map import collision_walls


class Player:
    def __init__(self, sprites):
        self.x, self.y = player_pos
        self.sprites = sprites
        self.angle = player_angle
        self.sensitivity = 0.004

        self.proj_coeff = PROJ_COEFF
        self.proj_coeff_sprites = 0
        self.delta_speed = 0
        self.jump_v = -2500
        self.jump = False
        self.shift_v = 10000
        self.shift = False
        self.shift_shift = True
        self.take_eye_bool = False
        self.count_of_eye = 0
        self.pos_of_eye = (0, 0)
        self.win = False
        # collision parameters
        self.side = 50
        self.rect = pygame.Rect(*player_pos, self.side, self.side)
        self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  [self.sprites.objects] if obj.blocked]
        self.collision_list = collision_walls + self.collision_sprites

    @property
    def pos(self):
        return self.x, self.y

    def check_death(self, monster):
        xm = monster.x
        ym = monster.y
        dx = self.x - xm
        dy = self.y - ym
        if (dx**2 + dy**2) <= 1000:
            return True

    def get_eye(self, world_map):
        self.count_of_eye += 1
        pos = self.pos_of_eye
        world_map.map[pos] = 6
        if self.count_of_eye == 5:
            self.win = True

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
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
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def movement(self, world_map):
        self.keys_control(world_map)
        self.mouse_control()
        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

    def keys_control(self, world_map):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_w]:
            dx = (player_speed * 1.1 - self.delta_speed) * cos_a
            dy = (player_speed * 1.1 - self.delta_speed) * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_s]:
            dx = -(player_speed - self.delta_speed) * cos_a
            dy = -(player_speed - self.delta_speed) * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = (player_speed - self.delta_speed) * sin_a
            dy = -(player_speed - self.delta_speed) * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -(player_speed - self.delta_speed) * sin_a
            dy = (player_speed - self.delta_speed) * cos_a
            self.detect_collision(dx, dy)

        if keys[pygame.K_SPACE]:
            self.jump = True
        if keys[pygame.K_LSHIFT]:
            self.shift = True
        if keys[pygame.K_RSHIFT]:
            self.shift = True

        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02

        if keys[pygame.K_f] and self.take_eye_bool:
            self.get_eye(world_map)

    def jump_func(self):
        self.proj_coeff += self.jump_v
        self.proj_coeff_sprites -= self.jump_v * 0.005
        self.jump_v += 100
        if self.proj_coeff >= PROJ_COEFF:
            self.proj_coeff = PROJ_COEFF
            self.proj_coeff_sprites = 0
            self.jump = False
            self.jump_v = -2500

    def shift_func_pressed(self):
        if self.shift_shift:
            self.proj_coeff += self.shift_v
            self.proj_coeff_sprites -= self.shift_v * 0.002
            self.delta_speed = 2
            self.shift_shift = False

        keys = pygame.key.get_pressed()
        if not keys[pygame.K_LSHIFT] and not keys[pygame.K_RSHIFT]:
            self.shift = False
            self.proj_coeff -= self.shift_v
            self.proj_coeff_sprites = 0
            self.delta_speed = 0
            self.shift_shift = True

    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * self.sensitivity

