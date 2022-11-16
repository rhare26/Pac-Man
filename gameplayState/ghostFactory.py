from gameplayState.ghost import Ghost, MED_GHOST_SPEED, SLOW_GHOST_SPEED, CHASE, RANDOM, FAST_GHOST_SPEED

# TODO: Make starting positions passed in from GameplayState
GHOST_START_X = 360
GHOST_START_Y = 280
GHOST_SPEEDS = [FAST_GHOST_SPEED, MED_GHOST_SPEED, MED_GHOST_SPEED, SLOW_GHOST_SPEED]
GHOST_STRATEGIES = [RANDOM, RANDOM, CHASE, CHASE]
GHOST_IMAGES = ["resources/ghosts/cyan.png", "resources/ghosts/orange.png", "resources/ghosts/red.png","resources/ghosts/pink.png"]


class GhostFactory:

    def __init__(self, max_ghosts, blocks, player, surface):
        self.ghosts_to_add: list[Ghost] = []
        self.counter = 0
        self.max = max_ghosts

        for i in range(0, max_ghosts):
            # TODO: make these circular arrays so you can add more than 4 without out of bounds error
            self.ghosts_to_add.append(
                Ghost(surface, GHOST_START_X, GHOST_START_Y, GHOST_SPEEDS[i], blocks))
            self.ghosts_to_add[i].assign_normal_strategy(GHOST_STRATEGIES[i], player)
            self.ghosts_to_add[i].assign_normal_image(GHOST_IMAGES[i])

    def get_ghost(self):
        self.counter += 1

        # TODO: this always pops the last one
        return self.ghosts_to_add.pop()
