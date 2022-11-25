# Game settings
STARTING_LIVES = 3

DOT_POINTS = 10
ENERGIZER_POINTS = 50

POINTS_BEFORE_NEW_GHOST = 400
MAX_GHOSTS = 4
CAUGHT_BLUE_GHOST_POINTS = 150
BLUE_STATE_TIME = 6000  # in milliseconds
GHOST_WARNING_TIME = 1000  # in milliseconds

MAX_FRUITS = 4  # per level
FRUIT_POINTS = 150
POINTS_BEFORE_NEW_FRUIT = 500
FRUIT_STATE_TIME = 7000  # in milliseconds

# Fonts & Display
BG_COLOR = (0, 0, 0)
FONT_COLOR = (0xff, 0xff, 0xff)
BIG_FONT_SIZE = 120
SMALL_FONT_SIZE = 40
FONT_FILE = 'freesansbold.ttf'
SCORE_AREA = 80                 # Height of area underneath maze for lives, points, etc...

# Joystick
JOYSTICK_UP = (0, -1)
JOYSTICK_DOWN = (0, 1)
JOYSTICK_RIGHT = (1, 0)
JOYSTICK_LEFT = (-1, 0)

# Maze
TILE_SIZE: int = 40
BLOCK_IMAGE = "resources/wall.png"
DOT_IMAGE = "resources/dot.png"
ENERGIZER_IMAGE = "resources/energizer.png"

# Sprite Movement
DIRECTION_INDEX = 0 # the first number of the tuple
X_DIRECTION = 1     # the second number of the tuple
Y_DIRECTION = 2     # the third number of the tuple

SPRITE_MOVE_LEFT = (0, -1, 0)   # index, x movement, y movement
SPRITE_MOVE_UP = (1, 0, -1)     # index, x movement, y movement
SPRITE_MOVE_RIGHT = (2, 1, 0)   # index, x movement, y movement
SPRITE_MOVE_DOWN = (3, 0, 1)    # index, x movement, y movement
SPRITE_STILL = (4, 0, 0)        # index, x movement, y movement

DIRECTIONS = [SPRITE_MOVE_LEFT, SPRITE_MOVE_UP, SPRITE_MOVE_RIGHT, SPRITE_MOVE_DOWN]
NUM_DIR = 4

# Player
PLAYER_SPEED = 10
PLAYER_IMAGE = "resources/player_right.png"
PLAYER_START_X = 380
PLAYER_START_Y = 480

# Ghosts
BLUE_IMAGE = 'resources/ghosts/blue.png'
GHOST_IMAGES = ["resources/ghosts/cyan.png", "resources/ghosts/orange.png", "resources/ghosts/red.png","resources/ghosts/pink.png"]
GHOST_START_X = 360
GHOST_START_Y = 280

SLOW_GHOST_SPEED = 4
MED_GHOST_SPEED = 5
FAST_GHOST_SPEED = 8

RANDOM = 0
CHASE = 1
FLEE = 2



# Fruits & Energizers
FRUIT_IMAGES = ["resources/fruits/cherry.png", "resources/fruits/orange.png", "resources/fruits/strawberry.png", "resources/fruits/apple.png"]

