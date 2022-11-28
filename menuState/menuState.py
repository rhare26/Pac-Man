from pygame.locals import *

from constants import BG_COLOR, CONTINUE_BUTTON, NEW_BUTTON
from gameplayState.gameplayState import GameplayState
from state import State

BIG_MESSAGE = "MENU"
SMALL_MESSAGE = "S/Green: START | C/Yellow: CONTINUE"


class MenuState(State):
    def __init__(self, surface):
        super().__init__(surface)
        State.menu_state = self

    def update(self, joystick_pos, key_presses):
        self.surface.fill(BG_COLOR)
        self.draw_center_big_message(BIG_MESSAGE)
        self.draw_center_small_message(SMALL_MESSAGE)

    def get_next_state(self, key_presses, buttons):

        # If in menu, continue/start play (will continue any in progress game)
        if key_presses[K_c] or buttons[CONTINUE_BUTTON]:
            return self.gameplay_state
        # If in menu, start new game
        elif key_presses[K_s] or buttons[NEW_BUTTON]:
            self.gameplay_state = GameplayState(self.surface)
            return self.gameplay_state
        return self
