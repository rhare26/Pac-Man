# https://coderslegacy.com/python/python-pygame-tutorial/
# https://gamedevelopment.tutsplus.com/articles/how-to-build-a-jrpg-a-primer-for-game-developers--gamedev-6676#state

# using pygame mostly for graphics & IO, writing own sprite classes

import sys

import pygame
from pygame import locals

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
    surface = pygame.display.set_mode((screen_width, screen_height))
    GameplayState(surface)
    LoseState(surface)
    WinState(surface)
    current_state = MenuState(surface)

    # Game Loop
    while running:
        pressed_keys = pygame.key.get_pressed()
        current_state = current_state.get_next_state(pressed_keys)
        current_state.update(pressed_keys)

        pygame.display.update()  # When done drawing to surface, update screen
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
        pygame.event.clear()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
