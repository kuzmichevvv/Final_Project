import pygame
import os
import sys
from Settings import *
import Map


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Monsters(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.rect = pygame.Rect(150, 150, self.side, self.side)

    def move(self):
        pass

    def draw(self):
        pygame.draw
