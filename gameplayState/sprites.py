from math import floor
from random import random

import pygame
from pygame import Rect, Surface

SPRITE_SIZE = 40

#Directions (index, x movement multiplier, y movement multiplier)
DIRECTION_INDEX = 0 # the first number of the tuple
X_DIRECTION = 1     # the second number of the tuple
Y_DIRECTION = 2     # the third number of the tuple

LEFT = (0, -1, 0)
UP = (1, 0, -1)
RIGHT = (2, 1, 0)
DOWN = (3, 0, 1)
STILL = (4, 0, 0)

DIRECTIONS = [LEFT, UP, RIGHT, DOWN]
NUM_DIR = 4


class Sprite:
    image = None

    def __init__(self, surface: Surface, x: int, y: int):
        self.surface: Surface = surface
        self.rect = Rect((x, y), (SPRITE_SIZE, SPRITE_SIZE))

    def draw(self):
        self.surface.blit(self.image, self.rect)

    # images are separated from constructor so that lighter clone versions can be created easily
    def assign_normal_image(self, image_str: str):
        x = self.rect.x
        y = self.rect.y
        self.image = pygame.image.load(image_str)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_image_str = image_str


class Movable(Sprite):
    speed: int
    direction: tuple
    starting_direction: tuple

    def __init__(self, surface: Surface, x: int, y: int, speed: int, blocks: list[Sprite]):
        Sprite.__init__(self, surface, x, y)
        self.starting_x = x
        self.starting_y = y
        self.speed = speed
        self.blocks = blocks

    def reset(self):
        self.rect.x = self.starting_x
        self.rect.y = self.starting_y
        self.direction = self.starting_direction

    def update_position(self):
        self.rect.x += self.direction[X_DIRECTION] * self.speed
        self.rect.y += self.direction[Y_DIRECTION] * self.speed

    def set_direction(self, direction):
        self.direction = direction

    def determine_move(self, key_presses):
        # player and ghosts determine moves differently
        pass

    def change_direction_90_degrees(self):
        # 1 away from current direction's index in directions array
        self.direction = DIRECTIONS[(self.direction[DIRECTION_INDEX] + 1) % NUM_DIR]

    def change_direction_180_degrees(self):
        # 2 away from current direction's index in directions array
        self.direction = DIRECTIONS[(self.direction[DIRECTION_INDEX] + 2) % NUM_DIR]

    def change_direction_270_degrees(self):
        # 3 away from current direction's index in directions array
        self.direction = DIRECTIONS[(self.direction[DIRECTION_INDEX] + 3) % NUM_DIR]

    def copy(self):
        # TODO: optimize this- call super in player.copy() and ghost.copy()
        pass


def collision(m: Movable, sprites: list[Sprite]):
    for s in sprites:
        if m.rect.colliderect(s.rect):
            # If being used as a boolean, s will evaluate to True (any number besides zero is true in Python)
            return s
    return False


# Manhattan distance
def distance_to_sprite(a: Sprite, b: Sprite) -> int:
    return abs(a.rect.x - b.rect.x) + abs(a.rect.y - b.rect.y)
