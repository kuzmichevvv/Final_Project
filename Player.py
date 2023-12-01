import math

from Settings import *
import pygame

class Player():
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle

    def pos(self):
        return (self.x,self.y)

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
            self.angle+=0.05
        if keys[pygame.K_LEFT]:
            self.angle-=0.05
