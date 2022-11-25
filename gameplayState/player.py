import pygame

from constants import JOYSTICK_LEFT, JOYSTICK_RIGHT, JOYSTICK_UP, JOYSTICK_DOWN, PLAYER_SPEED, DIRECTION_INDEX, \
    PLAYER_IMAGE_OPEN, PLAYER_IMAGE_CLOSED
from gameplayState.sprites import  Movable, collision
from constants import SPRITE_STILL,  SPRITE_MOVE_LEFT, SPRITE_MOVE_RIGHT, SPRITE_MOVE_UP, SPRITE_MOVE_DOWN
from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN,  Surface


class Player(Movable):

    def __init__(self, surface: Surface, x: int, y: int, blocks):
        Movable.__init__(self, surface, x, y, PLAYER_SPEED, blocks)
        self.direction = SPRITE_STILL
        self.starting_direction = self.direction
        self.open_image = pygame.image.load(PLAYER_IMAGE_OPEN)
        self.closed_image = pygame.image.load(PLAYER_IMAGE_CLOSED)
        self.current_image = pygame.image.load(PLAYER_IMAGE_OPEN)
        self.image_counter = 0
        self.open = True
    def draw(self):
        self.image_counter += 1
        if self.image_counter % 4 == 0:
            if self.open:
                self.current_image = self.closed_image
                self.open = False
            else:
                num_quarter_rotations = -self.direction[DIRECTION_INDEX]
                self.current_image = pygame.transform.rotate(self.open_image, 90 * num_quarter_rotations)
                self.open = True
        self.surface.blit(self.current_image, self.rect)

    def get_direction(self, joystick_pos, key_presses):
        if key_presses[K_LEFT] or joystick_pos == JOYSTICK_LEFT:
            self.direction = SPRITE_MOVE_LEFT
        elif key_presses[K_RIGHT] or joystick_pos == JOYSTICK_RIGHT:
            self.direction = SPRITE_MOVE_RIGHT
        elif key_presses[K_UP] or joystick_pos == JOYSTICK_UP:
            self.direction = SPRITE_MOVE_UP
        elif key_presses[K_DOWN] or joystick_pos == JOYSTICK_DOWN:
            self.direction = SPRITE_MOVE_DOWN

    def determine_move(self, joystick_pos, key_presses):
        #clone the player to try out new directions (light clone doesn't copy everything)
        clone: Player = self.copy()
        old_dir = self.direction

        clone.get_direction(joystick_pos, key_presses)
        clone.update_position()

        # if direction from joystick/keypress is good, update and return
        if not collision(clone, self.blocks):
            self.get_direction(joystick_pos, key_presses)
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
