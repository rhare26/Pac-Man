import pygame


from pygame.locals import *

FONT_COLOR = (0xff, 0xff, 0xff)
BIG_FONT_SIZE = 120
SMALL_FONT_SIZE = 24
FONT_FILE = 'freesansbold.ttf'



class State:
    menu_state = None
    gameplay_state = None
    lose_state = None
    lose_life_state = None
    win_state = None

    def __init__(self, surface):

        self.big_font = pygame.font.Font(FONT_FILE, BIG_FONT_SIZE)
        self.small_font = pygame.font.Font(FONT_FILE, SMALL_FONT_SIZE)
        self.surface = surface

    def update(self, joystick_pos, key_presses):
        pass

    def get_next_state(self, key_presses):
        pass

    def draw_center_big_message(self, message):
        big_text = self.big_font.render(str(message), True, FONT_COLOR)
        big_rect = big_text.get_rect()
        big_rect.center = (self.surface.get_width() / 2, self.surface.get_height() / 2)
        self.surface.blit(big_text, big_rect)

    def draw_center_small_message(self, message):
        small_text = self.small_font.render(str(message), True, FONT_COLOR)
        small_rect = small_text.get_rect()
        small_rect.center = (self.surface.get_width() / 2, self.surface.get_height() / 2 + BIG_FONT_SIZE)
        self.surface.blit(small_text, small_rect)