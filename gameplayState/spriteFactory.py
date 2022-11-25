from constants import PLAYER_START_X, FRUIT_IMAGES, PLAYER_START_Y, GHOST_IMAGES, \
    GHOST_START_Y, GHOST_START_X, FAST_GHOST_SPEED, SLOW_GHOST_SPEED, RANDOM, CHASE, MED_GHOST_SPEED, \
    TILE_SIZE
from gameplayState.ghost import Ghost
from gameplayState.player import Player
from gameplayState.sprites import Sprite

GHOST_SPEEDS = [FAST_GHOST_SPEED, SLOW_GHOST_SPEED, MED_GHOST_SPEED, FAST_GHOST_SPEED] #speeds of 4 ghosts in game
GHOST_STRATEGIES = [RANDOM, CHASE, CHASE, CHASE] # strategies of 4 ghosts in game

class SpriteFactory:

    def __init__(self, max_ghosts, max_fruits, blocks, surface):
        self.ghosts_to_add: list[Ghost] = []
        self.fruits_to_add: list[Sprite] = []
        self.counter = 0
        self.surface = surface
        self.max = max_ghosts
        self.blocks = blocks

        self.player = Player(self.surface, PLAYER_START_X, PLAYER_START_Y, self.blocks)

        for i in range(0, max_ghosts):
            # TODO: make these circular arrays so you can add more than 4 without out of bounds error
            self.ghosts_to_add.append(
                Ghost(surface, GHOST_START_X, GHOST_START_Y, GHOST_SPEEDS[i], blocks))
            self.ghosts_to_add[i].assign_normal_strategy(GHOST_STRATEGIES[i], self.player)
            self.ghosts_to_add[i].assign_normal_image(GHOST_IMAGES[i])

        for i in range(0, max_fruits):
            self.fruits_to_add.append(Sprite(surface, PLAYER_START_X + (TILE_SIZE / 2), PLAYER_START_Y))
            self.fruits_to_add[i].assign_normal_image(FRUIT_IMAGES[i])

    def get_player(self):

        return self.player

    def get_ghost(self):
        self.counter += 1


        return self.ghosts_to_add.pop() # return last ghost added to list

    def get_fruit(self):
        self.counter += 1

        # this always pops the last one
        return self.fruits_to_add.pop() # return last fruit added to list
