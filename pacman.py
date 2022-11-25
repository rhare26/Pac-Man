# https://coderslegacy.com/python/python-pygame-tutorial/
# https://gamedevelopment.tutsplus.com/articles/how-to-build-a-jrpg-a-primer-for-game-developers--gamedev-6676#state

# using pygame mostly for graphics & IO, writing own sprite classes

import sys

import pygame
from pygame import locals, KEYDOWN, K_ESCAPE

from gameplayState.gameplayState import GameplayState
from loseState.loseState import LoseState
from menuState.menuState import MenuState
from state import State
from winState.winState import WinState

screen_width: int = 800
screen_height: int = 880

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
                print("Joystick button pressed.")

            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joystick = pygame.joystick.Joystick(event.device_index)
                print(f"{joystick.get_name()} #{joystick.get_instance_id()} connected")


            if event.type == pygame.JOYDEVICEREMOVED:
                del joystick
                print(f"Joystick {event.instance_id} disconnected")

        pygame.event.clear()

        # Send to current state
        pressed_keys = pygame.key.get_pressed()
        current_state = current_state.get_next_state(pressed_keys)
        current_state.update(joystick_pos, pressed_keys)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
