from pygame import Surface

from gameplayState.sprites import Sprite

DOT = 0
BLOCK = 1
ENERGIZER = 2

TILE_SIZE: int = 40
BLOCK_IMAGE = "resources/wall.png"
DOT_IMAGE = "resources/dot.png"
ENERGIZER_IMAGE = "resources/energizer.png"
FRUIT_IMAGES = "resources/cherry.png"

# TODO: add a get_maze() method instead of just using constructor
# TODO: add multiple mazes, maybe load in from file?
class MazeFactory:

    def __init__(self, surface):
        self.energizers: list[Sprite] = []
        self.maze_dimension = 20
        self.blocks: list[Sprite] = []
        self.dots: list[Sprite] = []
        self.fruits: list[Sprite] = []
        self.surface: Surface = surface
        self.matrix = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                       3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3,
                       3, 3, 1, 2, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 1, 3, 3,
                       3, 3, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 3, 3,
                       3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3,
                       3, 3, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 3, 3,
                       3, 3, 1, 0, 1, 1, 0, 1, 0, 3, 3, 0, 1, 0, 1, 1, 0, 1, 3, 3,
                       3, 3, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 3, 3,
                       3, 3, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 3, 3,
                       3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3,
                       3, 3, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 3, 3,
                       3, 3, 1, 0, 1, 0, 1, 1, 0, 3, 3, 0, 1, 1, 0, 1, 0, 1, 3, 3,
                       3, 3, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 3, 3,
                       3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3,
                       3, 3, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 3, 3,
                       3, 3, 1, 2, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 1, 3, 3,
                       3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3,
                       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, ]

        row = 0
        col = 0
        while row < self.maze_dimension:
            val = self.matrix[col + (row * self.maze_dimension)]
            if val == BLOCK:
                self.blocks.append(Sprite(self.surface, col * TILE_SIZE, row * TILE_SIZE))
                self.blocks[-1].assign_normal_image(BLOCK_IMAGE)

            elif val == DOT:
                self.dots.append(Sprite(self.surface, col * TILE_SIZE, row * TILE_SIZE))
                self.dots[-1].assign_normal_image(DOT_IMAGE)

            elif val == ENERGIZER:
                self.energizers.append(Sprite(self.surface, col * TILE_SIZE, row * TILE_SIZE))
                self.energizers[-1].assign_normal_image(ENERGIZER_IMAGE)
            col += 1

            # If at end of row
            if col == self.maze_dimension:
                col = 0
                row += 1
