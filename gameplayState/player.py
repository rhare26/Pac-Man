from gameplayState.sprites import collision, STILL, Movable, LEFT, RIGHT, UP, DOWN, DIRECTIONS
from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN,  Surface

PLAYER_SPEED = 10


class Player(Movable):

    def __init__(self, surface: Surface, x: int, y: int, blocks):
        Movable.__init__(self, surface, x, y, PLAYER_SPEED, blocks)
        self.direction = STILL
        self.starting_direction = self.direction

    #  TODO: update to joystick (logic will make better sense bc joystick can only point in one direction)
    def get_direction(self, key_presses):
        if key_presses[K_LEFT]:
            self.direction = LEFT
        elif key_presses[K_RIGHT]:
            self.direction = RIGHT
        elif key_presses[K_UP]:
            self.direction = UP
        elif key_presses[K_DOWN]:
            self.direction = DOWN

    def determine_move(self, joystick_pos, key_presses):
        #clone the player to try out new directions (light clone doesn't copy everything)
        clone: Player = self.copy()
        old_dir = self.direction
        print(joystick_pos)

        clone.get_direction(key_presses)
        clone.update_position()

        # if current or new direction is good, update and return
        if not collision(clone, self.blocks):
            self.get_direction(key_presses)
            self.update_position()
            return

        # else take back last move
        clone.change_direction_180_degrees()
        clone.update_position()

        # try old direction
        clone.direction = old_dir
        clone.update_position()
        if not collision(clone, self.blocks):
            self.update_position()
            return

    def copy(self):
        m: Player = Player(self.surface, self.rect.x, self.rect.y, self.blocks)
        m.speed = self.speed
        m.direction = self.direction
        return m
