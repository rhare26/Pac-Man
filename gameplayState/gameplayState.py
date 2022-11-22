import pygame as pygame

from gameplayState.ghostFactory import GhostFactory
from gameplayState.mazeFactory import MazeFactory
from gameplayState.player import Player
from gameplayState.ghost import Ghost
from gameplayState.sprites import collision
from state import State
from pygame import Surface, K_SPACE

BG_COLOR = (0, 0, 0)
SCORE_AREA = 80
FONT_COLOR = (0xff, 0xff, 0xff)
FONT_SIZE = 80
FONT_FILE = 'freesansbold.ttf'

STARTING_SCORE = 0
STARTING_LIVES = 3

DOT_POINTS = 10
ENERGIZER_POINTS = 50
BLUE_STATE_TIME = 10000 #in milliseconds
CAUGHT_BLUE_GHOST_POINTS = 200

POINTS_BEFORE_NEW_GHOST = 100
MAX_GHOSTS: int = 4

POINTS_BEFORE_NEW_FRUIT = 100
MAX_FRUITS: int = 4

#TODO: possibly move this into player class instead
PLAYER_IMAGE = "resources/player.png"
PLAYER_START_X = 380
PLAYER_START_Y = 480


class GameplayState(State):

    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)
        State.gameplay_state = self

        # Game variables
        self.game_over = False
        self.blue_state = False
        self.blue_state_end_time = 0;
        self.score = STARTING_SCORE
        self.lives = STARTING_LIVES

        # Screen
        self.font = pygame.font.Font(FONT_FILE, FONT_SIZE)

        # Maze & dots
        #TODO: make different mazes later and use get_maze()
        self.maze = MazeFactory(surface)

        # Player & ghosts
        self.player = Player(self.surface, PLAYER_START_X, PLAYER_START_Y, self.maze.blocks)
        self.player.assign_normal_image(PLAYER_IMAGE)

        self.ghost_factory = GhostFactory(MAX_GHOSTS, self.maze.blocks, self.player, self.surface)
        self.ghosts: list[Ghost] = [self.ghost_factory.get_ghost()]
        self.num_current_ghosts = 1

        self.next_state = self

    # STATE METHODS #
    def update(self, key_presses):
        # Default next state if nothing is changed
        self.next_state = self

        # Check if blue state is over
        if self.blue_state:
            if self.blue_state_end_time <= pygame.time.get_ticks():
                self.end_blue_state()

        # Update background, maze walls, and dots
        self.surface.fill(BG_COLOR)
        for s in self.maze.blocks + self.maze.dots + self.maze.energizers + self.maze.fruits:
            s.draw()

        # Move sprites
        for s in self.ghosts:
            s.determine_move(key_presses)
            s.draw()

        self.player.determine_move(key_presses)
        self.player.draw()

        # Check collisions
        collided_dot = collision(self.player, self.maze.dots)
        if collided_dot:
            self.maze.dots.remove(collided_dot)
            self.score += DOT_POINTS

            if (self.num_current_ghosts < MAX_GHOSTS) and (self.score % POINTS_BEFORE_NEW_GHOST == 0):
                self.ghosts.append(self.ghost_factory.get_ghost())
                self.num_current_ghosts += 1
            elif self.maze.dots:  #no dots left
                #  TODO: check if won level
                pass
            elif self.score % POINTS_BEFORE_NEW_FRUIT == 0:
                #  TODO: add fruit
                pass

        collided_energizer = collision(self.player, self.maze.energizers)
        if collided_energizer:
            self.maze.energizers.remove(collided_energizer)
            self.score += ENERGIZER_POINTS
            for collided_ghost in self.ghosts:
                collided_ghost.set_blue_state()
                self.blue_state = True
                self.blue_state_end_time = pygame.time.get_ticks() + BLUE_STATE_TIME

        collided_ghost = collision(self.player, self.ghosts)
        if collided_ghost:
            if collided_ghost.is_vulnerable:
                collided_ghost.reset()
                self.score += CAUGHT_BLUE_GHOST_POINTS
            else:
                self.lives -= 1
                if self.lives > 0:
                    self.reset_all_sprites()
                else:
                    self.next_state = self.lose_state

        # Update score area
        self.display_score()
        self.display_lives()

    def get_next_state(self, key_presses):
        # Lose state would have already been updated when checking ghost collisions

        # If you press pause while in gameplay state
        if key_presses[K_SPACE]:
            return self.menu_state

         # If not changed above, next state will still be self
        return self.next_state

    # RESETS #
    def end_blue_state(self):
        for g in self.ghosts:
            g.set_normal_state()
    def reset_all_sprites(self):
        for g in self.ghosts:
            g.reset()
        self.player.reset()

    # DISPLAYING GAME INFO #
    # TODO: give margins to display score and lives
    def display_score(self):
        score_text = self.font.render(str(self.score), True, FONT_COLOR)
        score_rect = score_text.get_rect()
        score_rect.bottomright = (self.surface.get_width(), self.surface.get_height())
        self.surface.blit(score_text, score_rect)

    def display_lives(self):
        life_image = pygame.image.load(PLAYER_IMAGE)
        life_rect = life_image.get_rect()
        for life in range(self.lives):
            # Draw at bottom left (move over for each new life to draw)
            life_rect.bottomleft = (0.25 * life_rect.width + life * life_rect.width * 1.5,
                                    self.surface.get_height() - (0.5 * life_rect.height))
            self.surface.blit(life_image, life_rect)
