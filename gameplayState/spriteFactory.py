from gameplayState.ghost import Ghost, MED_GHOST_SPEED, SLOW_GHOST_SPEED, CHASE, RANDOM, FAST_GHOST_SPEED
from gameplayState.player import Player
from gameplayState.sprites import Sprite

# TODO: Make starting positions passed in from GameplayState
PLAYER_IMAGE = "resources/player_right.png"
PLAYER_START_X = 380
PLAYER_START_Y = 480

GHOST_START_X = 360
GHOST_START_Y = 280

GHOST_SPEEDS = [FAST_GHOST_SPEED, SLOW_GHOST_SPEED, MED_GHOST_SPEED, FAST_GHOST_SPEED]
GHOST_STRATEGIES = [RANDOM, CHASE, CHASE, CHASE]
GHOST_IMAGES = ["resources/ghosts/cyan.png", "resources/ghosts/orange.png", "resources/ghosts/red.png","resources/ghosts/pink.png"]

FRUIT_IMAGES = ["resources/fruits/cherry.png", "resources/fruits/orange.png", "resources/fruits/strawberry.png", "resources/fruits/apple.png"]

class SpriteFactory:

    def __init__(self, max_ghosts, max_fruits, blocks, surface):
        self.ghosts_to_add: list[Ghost] = []
        self.fruits_to_add: list[Sprite] = []
        self.counter = 0
        self.surface = surface
        self.max = max_ghosts
        self.blocks = blocks


        self.player = Player(self.surface, PLAYER_START_X, PLAYER_START_Y, self.blocks)
        self.player.assign_normal_image(PLAYER_IMAGE)

        for i in range(0, max_ghosts):
            # TODO: make these circular arrays so you can add more than 4 without out of bounds error
            self.ghosts_to_add.append(
                Ghost(surface, GHOST_START_X, GHOST_START_Y, GHOST_SPEEDS[i], blocks))
            self.ghosts_to_add[i].assign_normal_strategy(GHOST_STRATEGIES[i], self.player)
            self.ghosts_to_add[i].assign_normal_image(GHOST_IMAGES[i])

        for i in range(0, max_fruits):
            self.fruits_to_add.append(Sprite(surface, PLAYER_START_X + 20, PLAYER_START_Y)) # TODO: fix this
            self.fruits_to_add[i].assign_normal_image(FRUIT_IMAGES[i])

    def get_player(self):

        return self.player

    def get_ghost(self):
        self.counter += 1

        # TODO: this always pops the last one
        return self.ghosts_to_add.pop()

    def get_fruit(self):
        self.counter += 1

        # TODO: this always pops the last one
        return self.fruits_to_add.pop()
