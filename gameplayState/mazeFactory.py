from pygame import Surface

from constants import ENERGIZER_IMAGE, TILE_SIZE, DOT_IMAGE, BLOCK_IMAGE
from gameplayState.sprites import Sprite

# This must match the number of matrices, and the dimensions of the matrices below
NUM_MATRICES = 3
MATRIX_DIMENSION = 20

# Meanings of the numbers in the matrix
DOT = 0
BLOCK = 1
ENERGIZER = 2
BLANK = 3
GHOST_START = 4

# TODO: read in matrices from file
# Used to create dots, blocks, and energizers
MATRICES = [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
             3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
             3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3,
             3, 3, 1, 2, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 1, 3, 3,
             3, 3, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 1, 0, 1, 0, 4, 4, 0, 1, 0, 1, 1, 0, 1, 3, 3,
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
             3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, ],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
             3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
             3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3,
             3, 3, 1, 2, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 1, 3, 3,
             3, 3, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 3, 3,
             3, 3, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 3, 3,
             3, 3, 1, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 3, 3,
             3, 3, 1, 2, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 2, 1, 3, 3,
             3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3,
             3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
             3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, ],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
             3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
             3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3,
             3, 3, 1, 2, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 2, 1, 3, 3,
             3, 3, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 3, 3,
             3, 3, 1, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 1, 3, 3,
             3, 3, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 3, 3,
             3, 3, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 3, 3,
             3, 3, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 3, 3,
             3, 3, 1, 2, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 1, 3, 3,
             3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3,
             3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
             3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, ]
            ]

class MazeFactory:

    def __init__(self, surface):
        self.surface: Surface = surface
        self.dots = None
        self.blocks = None
        self.energizers = None
        self.maze_counter = 0 # keeps track of which matrix to use when advancing to new levels or starting new games

    #  TODO: use python getters attribute
    def get_blocks(self):
        return self.blocks

    def get_dots(self):
        return self.dots

    def get_energizers(self):
        return self.energizers

    def set_new_maze(self):

        self.energizers: list[Sprite] = []

        self.blocks: list[Sprite] = []
        self.dots: list[Sprite] = []
        matrix = MATRICES[self.maze_counter % NUM_MATRICES]

        row = 0
        col = 0
        while row < MATRIX_DIMENSION:
            val = matrix[col + (row * MATRIX_DIMENSION)]
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
            if col == MATRIX_DIMENSION:
                col = 0
                row += 1

        self.maze_counter += 1
