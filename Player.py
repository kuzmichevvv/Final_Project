import math

from Settings import *
import pygame

class Player():
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.proj_coeff=PROJ_COEFF
        self.jump_v = -3000
        self.jump = False
        self.shift_v = 3000
        self.shift = False

    def jump_func(self):
        self.proj_coeff += self.jump_v
        self.jump_v += 200
        if self.proj_coeff >= PROJ_COEFF:
            self.proj_coeff=PROJ_COEFF
            self.jump = False
            self.jump_v = -2000

    def shift_func(self):
        self.proj_coeff += self.shift_v
        # self.shift_v -= 200
        if self.proj_coeff <= PROJ_COEFF:
            self.proj_coeff=PROJ_COEFF
            self.shift = False
            self.shift_v = 2000
        if(self.proj_coeff > PROJ_COEFF):
            pass
    def pos(self):
        return self.x, self.y

    def move(self):
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += player_speed*cos_a
            self.y += player_speed*sin_a
        if keys[pygame.K_a]:
            self.x += player_speed * sin_a
            self.y += -player_speed * cos_a
        if keys[pygame.K_d]:
            self.x += -player_speed * sin_a
            self.y += player_speed * cos_a
        if keys[pygame.K_s]:
            self.x += -player_speed * cos_a
            self.y += -player_speed * sin_a
        if keys[pygame.K_RIGHT]:
            self.angle+=0.01
        if keys[pygame.K_LEFT]:
            self.angle-=0.01
        if keys[pygame.K_SPACE]:
            self.jump = True
        if keys[pygame.K_LSHIFT]:
            self.shift = True
        if keys[pygame.K_RSHIFT]:
            self.shift = True
