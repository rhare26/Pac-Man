# https://coderslegacy.com/python/python-pygame-tutorial/
# https://gamedevelopment.tutsplus.com/articles/how-to-build-a-jrpg-a-primer-for-game-developers--gamedev-6676#state

# using pygame mostly for graphics & IO, writing own sprite classes

import sys

import pygame
from pygame import locals, KEYDOWN, K_ESCAPE

from constants import MENU_BUTTON, NEW_BUTTON, CONTINUE_BUTTON
from gameplayState.gameplayState import GameplayState
from loseState.loseState import LoseState
from menuState.menuState import MenuState
from state import State
from winState.winState import WinState

screen_width: int = 780
screen_height: int = 780


def main():
    pygame.init()
    running = True

    # Clock & fps
    clock = pygame.time.Clock()
    fps = 15  # Max of frames per second
    clock.tick(fps)

    joystick = None
    joystick_pos = None

    surface = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pac-Man")

    GameplayState(surface)
    LoseState(surface)
    WinState(surface)
    current_state = MenuState(surface)

    buttons = [0, 0, 0]

    # Game Loop

    while running:

        if joystick:
            for i in range(joystick.get_numaxes()):
                x_dir = joystick.get_axis(0) + joystick.get_axis(2)
                x_dir = round(x_dir)

                y_dir = joystick.get_axis(1) + joystick.get_axis(3)
                y_dir = round(y_dir)

                joystick_pos = (x_dir, y_dir)

        for event in pygame.event.get():
            if (event.type == pygame.locals.QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            if event.type == pygame.JOYBUTTONDOWN:
                buttons = [joystick.get_button(MENU_BUTTON),
                           joystick.get_button(NEW_BUTTON),
                           joystick.get_button(CONTINUE_BUTTON)]
            else:
                buttons = [0, 0, 0]

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joystick = pygame.joystick.Joystick(event.device_index)
                print(f"{joystick.get_name()} #{joystick.get_instance_id()} connected")

        pygame.event.clear()

        # Send to current state
        pressed_keys = pygame.key.get_pressed()
        current_state = current_state.get_next_state(pressed_keys, buttons)
        current_state.update(joystick_pos, pressed_keys)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
