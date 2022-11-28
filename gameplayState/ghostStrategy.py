from math import floor
from random import random

from gameplayState.sprites import distance_to_sprite


class GhostStrategy:
    def __init__(self, ghost, player):
        self.ghost = ghost
        self.player = player

    def employ(self, valid_moves):
        pass


class ChaseStrategy(GhostStrategy):
    def __init__(self, ghost, player):
        super().__init__(ghost, player)

    def employ(self, valid_moves):

        closest = valid_moves[0]
        for m in valid_moves:
            if distance_to_sprite(m, self.player) <= distance_to_sprite(closest, self.player):
                closest = m
        self.ghost.set_direction(closest.direction)
        self.ghost.update_position()


class RandomStrategy(GhostStrategy):

    def __init__(self, ghost, player):
        super().__init__(ghost, player)

    def employ(self, valid_moves):
        self.ghost.set_direction(valid_moves[floor(random() * len(valid_moves))].direction)
        self.ghost.update_position()


class FleeStrategy(GhostStrategy):
    def __init__(self, ghost, player):
        super().__init__(ghost, player)

    def employ(self, valid_moves):
        farthest = valid_moves[0]
        for m in valid_moves:
            if distance_to_sprite(m, self.player) >= distance_to_sprite(farthest, self.player):
                farthest = m
        self.ghost.set_direction(farthest.direction)
        self.ghost.update_position()
