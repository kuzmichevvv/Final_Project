import pygame
from settings import *
from collections import deque


class Monsters:
    def __init__(self):
        self.monster_parameters = {
                'sprite': [pygame.image.load(f'sprites/devil/base/{i}.png').convert_alpha() for i in range(8)],
                'shift': -0.2,
                'scale': 1.1,
                'animation': deque(
                    [pygame.image.load(f'sprites/devil/anim/{i}.png').convert_alpha() for i in range(9)]),
                'animation_dist': 150,
                'animation_speed': 10,
                'blocked': True,
            }

        self.objects = SpriteObject(self.monster_parameters, (20, 14.5))


class SpriteObject:
    def __init__(self, parameters, pos):
        self.turn_angle = 0
        self.monster_speed = 2
        self.return_move = 0
        self.flag = False
        self.flag_flag = True
        self.object = parameters['sprite']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.side = 30
        self.animation_count = 0
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.pos = self.x - self.side // 2, self.y - self.side // 2
        self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
        self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player):

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and distance_to_sprite > 30:
            proj_height = min(int(PROJ_COEFF / distance_to_sprite * self.scale), DOUBLE_HEIGHT)
            proj_heighty = min(int(PROJ_COEFF / (distance_to_sprite + player.proj_coeff_sprites) * self.scale), DOUBLE_HEIGHT)
            half_proj_height = proj_height // 2
            half_proj_heighty = proj_heighty // 2
            shift = half_proj_height * self.shift
            # choosing sprite for angle
            if theta < 0:
                theta += DOUBLE_PI
            theta = 360 - int(math.degrees(theta))

            for angles in self.sprite_angles:
                alpha = theta + self.turn_angle
                if alpha <= 0:
                    alpha += 360
                if alpha >= 360:
                    alpha -= 360
                if alpha in angles:
                    self.object = self.sprite_positions[angles]
                    break

            # sprite animation
            sprite_object = self.object
            if self.animation and distance_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            # sprite scale and pos
            sprite_pos = (current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_heighty + shift)
            sprite = pygame.transform.scale(sprite_object, (proj_height, proj_height))
            return distance_to_sprite, sprite, sprite_pos
        else:
            return (False,)

    def move(self, player_pos, player_shift):
        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        if ((dx**2 + dy**2) <= 90000 and (not player_shift or self.flag)) or ((dx**2 + dy**2) <= 2500):
            alpha = math.atan2(dy, dx)
            self.x += self.monster_speed * math.cos(alpha)
            self.y += self.monster_speed * math.sin(alpha)
            self.flag = True
        else:
            if 1460 >= self.y >= 1440 and 1140 <= self.x <= 2260:
                self.x -= self.monster_speed
                self.turn_angle = 0
                self.flag_flag = False
            if 1160 >= self.x >= 1140 and 1460 >= self.y >= 1240:
                self.y -= self.monster_speed
                self.turn_angle = 90
                self.flag_flag = False
            if 1260 >= self.y >= 1240 and 740 <= self.x <= 1160:
                self.x -= self.monster_speed
                self.turn_angle = 0
                self.flag_flag = False
            if 760 >= self.x >= 740 and 1240 <= self.y <= 1460:
                self.y += self.monster_speed
                self.turn_angle = -1 * 90
                self.flag_flag = False
            if 1460 >= self.y >= 1440 and 140 <= self.x <= 760:
                self.x -= self.monster_speed
                self.turn_angle = 0
                self.flag_flag = False
            if 160 >= self.x >= 140 and 140 <= self.y <= 1460:
                self.y -= self.monster_speed
                self.turn_angle = 90
                self.flag_flag = False
            if 160 >= self.y >= 140 and 140 <= self.x <= 560:
                self.x += self.monster_speed
                self.turn_angle = 180
                self.flag_flag = False
            if 560 >= self.x >= 540 and 144 <= self.y <= 460:
                self.y += self.monster_speed
                self.turn_angle = -1 * 90
                self.flag_flag = False
            if 460 >= self.y >= 440 and 540 <= self.x <= 1160:
                self.x += self.monster_speed
                self.turn_angle = 180
                self.flag_flag = False
            if 1160 >= self.x >= 1140 and 440 <= self.y <= 760:
                self.y += self.monster_speed
                self.turn_angle = -1 * 90
                self.flag_flag = False
            if 760 >= self.y >= 740 and 1140 <= self.x <= 1360:
                self.x += self.monster_speed
                self.turn_angle = 180
                self.flag_flag = False
            if 1360 >= self.x >= 1340 and 760 >= self.y >= 140:
                self.y -= self.monster_speed
                self.turn_angle = 90
                self.flag_flag = False
            if 160 >= self.y >= 140 and 1340 <= self.x <= 1660:
                self.x += self.monster_speed
                self.turn_angle = 180
                self.flag_flag = False
            if 1660 >= self.x >= 1640 and 140 <= self.y <= 260:
                self.y += self.monster_speed
                self.turn_angle = 270
                self.flag_flag = False
            if 260 >= self.y >= 240 and 1640 <= self.x <= 1860:
                self.x += self.monster_speed
                self.turn_angle = 180
                self.flag_flag = False
            if 1860 >= self.x >= 1840 and 260 >= self.y >= 140:
                self.y -= self.monster_speed
                self.turn_angle = 90
                self.flag_flag = False
            if 160 >= self.y >= 140 and 1840 <= self.x <= 2260:
                self.x += self.monster_speed
                self.turn_angle = 180
                self.flag_flag = False
            if 2260 >= self.x >= 2240 and 140 <= self.y <= 1460:
                self.y += self.monster_speed
                self.turn_angle = 270
                self.flag_flag = False
            if self.flag_flag:
                self.x -= self.monster_speed
                self.turn_angle = 0
                if self.x <= 150:
                    self.x = 150
                    self.flag_flag = False
            else:
                self.flag_flag = True
