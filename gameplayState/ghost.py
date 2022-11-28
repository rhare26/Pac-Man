from math import floor
from random import random

import pygame
from pygame import Surface

from constants import CHASE, BLUE_IMAGE, SPRITE_MOVE_LEFT, SLOW_GHOST_SPEED
from gameplayState.ghostStrategy import GhostStrategy, ChaseStrategy, FleeStrategy, RandomStrategy
from gameplayState.sprites import Movable, collision

class Ghost(Movable):
    strategy: GhostStrategy

    def __init__(self, surface: Surface, x: int, y: int, speed: int, blocks):
        Movable.__init__(self, surface, x, y, speed, blocks)
        self.direction = SPRITE_MOVE_LEFT
        self.starting_direction = self.direction
        self.is_vulnerable = False

    # This is broken out from constructor since it involves object creation, does not need to be done for clones
    def assign_normal_strategy(self, strategy: int, player):
        self.original_strategy = strategy
        if strategy == CHASE:
            self.strategy = ChaseStrategy(self, player)
        else:
            self.strategy = RandomStrategy(self, player)

    def determine_move(self, joystick_pos, key_presses):
        # make three copies to try three directions (no 180s, would get stuck moving back and forth)
        clones = [self.copy(), self.copy(), self.copy()]

        # clones[0] is already current direction
        clones[1].change_direction_90_degrees()
        clones[2].change_direction_270_degrees()

        valid_moves = []
        for c in clones:
            c.update_position()
            if not collision(c, self.blocks):
                valid_moves.append(c)

        # calls specific strategy to pick best valid move (eg random, chase, etc)
        self.strategy.employ(valid_moves)

    # TODO: possibly move this up to Movable
    def copy(self):
        g: Ghost = Ghost(self.surface, self.rect.x, self.rect.y, self.speed, self.blocks)
        g.speed = self.speed
        g.direction = self.direction
        return g

    def set_blue_state(self):
        self.strategy = FleeStrategy(self, self.strategy.player)
        self.image = pygame.image.load(BLUE_IMAGE)
        self.is_vulnerable = True

    def set_normal_state(self):
        self.assign_normal_strategy(self.original_strategy, self.strategy.player)
        self.image = pygame.image.load(self.original_image_str)
        self.is_vulnerable = False

    def reset(self):
        self.set_normal_state()
        super().reset()


