from pygame.locals import *
from gameplayState.gameplayState import GameplayState
from state import State

BIG_MESSAGE = "YOU LOSE!"
SMALL_MESSAGE = "M: MENU"
# TODO: better message


class LoseState(State):
    def __init__(self, surface):
        super().__init__(surface)
        State.lose_state = self

    def update(self, joystick_pos, key_presses):
        self.draw_center_big_message(BIG_MESSAGE)
        self.draw_center_small_message(SMALL_MESSAGE)

    def get_next_state(self, key_presses):
        # TODO: change these for hardware buttons
        # If in lose state: reset game, go to menu
        if key_presses[K_m]:
            self.gameplay_state = GameplayState(self.surface)
            return self.menu_state
        return self



