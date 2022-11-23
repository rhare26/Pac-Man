import pygame as pygame

from gameplayState.spriteFactory import SpriteFactory
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

STARTING_LIVES = 3

DOT_POINTS = 10

POINTS_BEFORE_NEW_GHOST = 400
MAX_GHOSTS = 4
ENERGIZER_POINTS = 50
CAUGHT_BLUE_GHOST_POINTS = 150
BLUE_STATE_TIME = 6000 # in milliseconds
GHOST_WARNING_TIME = 1000

MAX_FRUITS = 4
FRUIT_POINTS = 100
POINTS_BEFORE_NEW_FRUIT = 500
FRUIT_STATE_TIME = 7000 # in milliseconds

#TODO: move this into SpriteFactory
PLAYER_IMAGE = "resources/player.png"
PLAYER_START_X = 380
PLAYER_START_Y = 480


class GameplayState(State):
    score = 0
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)
        State.gameplay_state = self

        # Game variables
        self.game_over = False
        self.blue_state = False
        self.blue_state_end_time = 0
        self.fruit_state = False
        self.fruit_state_end_time = 0
        self.lives = STARTING_LIVES

        # Screen
        self.font = pygame.font.Font(FONT_FILE, FONT_SIZE)

        # Maze & sprites
        #TODO: make different mazes later and use get_maze()
        self.maze = MazeFactory(surface)

        self.player = Player(self.surface, PLAYER_START_X, PLAYER_START_Y, self.maze.blocks)
        self.player.assign_normal_image(PLAYER_IMAGE)

        self.sprite_factory = SpriteFactory(MAX_GHOSTS, MAX_FRUITS, self.maze.blocks, self.player, self.surface)
        self.ghosts: list[Ghost] = [self.sprite_factory.get_ghost()]
        self.num_current_ghosts = 1

        self.fruits = []
        self.num_fruits_deployed = 0

        self.next_state = self

    # STATE METHODS #
    def update(self, key_presses):
        # Default next state if nothing is changed
        self.next_state = self  # default state if nothing changed
        self.check_substates()  # check timers for blue state and fruit state

        self.move_and_draw(key_presses)  # move all sprites and blit to surface
        self.check_collisions()  # check for collisions between player and: ghosts, dots, energizers, fruits
        self.check_conditions()  # check if time to add a new ghost, add a new fruit, or win the game
        self.update_game_stats_display()  # update score and lives display

    def check_substates(self):
        if self.blue_state:
            if self.blue_state_end_time <= pygame.time.get_ticks():
                self.end_blue_state()

        if self.fruit_state:
            if self.fruit_state_end_time <= pygame.time.get_ticks():
                self.fruits = []
                self.fruit_state = False
    def move_and_draw(self, key_presses):
        # Update background, maze walls, and dots
        self.surface.fill(BG_COLOR)
        for s in self.maze.blocks + self.maze.dots + self.maze.energizers + self.fruits:
            s.draw()

        # Move sprites
        for s in self.ghosts:
            s.determine_move(key_presses)
            s.draw()

        self.player.determine_move(key_presses)
        self.player.draw()

    def check_collisions(self):
        # Dots
        collided_dot = collision(self.player, self.maze.dots)
        if collided_dot:
            self.maze.dots.remove(collided_dot)
            self.score += DOT_POINTS

        # Energizers
        collided_energizer = collision(self.player, self.maze.energizers)
        if collided_energizer:
            self.maze.energizers.remove(collided_energizer)
            self.score += ENERGIZER_POINTS
            for collided_ghost in self.ghosts:
                collided_ghost.set_blue_state()
            self.blue_state = True
            self.blue_state_end_time = pygame.time.get_ticks() + BLUE_STATE_TIME

        # Ghosts
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

        # Fruit
        collided_fruit = collision(self.player, self.fruits)
        if collided_fruit:
            self.score += FRUIT_POINTS
            self.fruits.remove(collided_fruit)
            self.fruit_state = False

    def check_conditions(self):
        if (self.num_current_ghosts < MAX_GHOSTS) and \
                (self.score > self.num_current_ghosts * POINTS_BEFORE_NEW_GHOST):
            self.ghosts.append(self.sprite_factory.get_ghost())
            self.num_current_ghosts += 1
        if (self.num_fruits_deployed < MAX_FRUITS) and \
                (self.score > (self.num_fruits_deployed + 1) * POINTS_BEFORE_NEW_FRUIT):
            self.fruits.append(self.sprite_factory.get_fruit())
            self.num_fruits_deployed += 1
            self.fruit_state_end_time = pygame.time.get_ticks() + FRUIT_STATE_TIME
            self.fruit_state = True

    def get_next_state(self, key_presses):
        # Lose state would have already been updated when checking ghost collisions

        # If you press pause while in gameplay state
        if key_presses[K_SPACE]:
            return self.menu_state

        if not self.maze.dots:  # no dots left
            self.next_state = self.win_state
         # If not changed above, next state will still be self
        return self.next_state

    # RESETS #
    def end_blue_state(self):
        for g in self.ghosts:
            g.set_normal_state()
        self.blue_state = False
    def reset_all_sprites(self):
        for g in self.ghosts:
            g.reset()
        self.player.reset()
        self.fruits = []

    # DISPLAYING GAME INFO #
    # TODO: give margins to display score and lives

    def update_game_stats_display(self):
        score_text = self.font.render(str(self.score), True, FONT_COLOR)
        score_rect = score_text.get_rect()
        score_rect.bottomright = (self.surface.get_width(), self.surface.get_height())
        self.surface.blit(score_text, score_rect)

        life_image = pygame.image.load(PLAYER_IMAGE)
        life_rect = life_image.get_rect()
        for life in range(self.lives):
            # Draw at bottom left (move over for each new life to draw)
            life_rect.bottomleft = (0.25 * life_rect.width + life * life_rect.width * 1.5,
                                    self.surface.get_height() - (0.5 * life_rect.height))
            self.surface.blit(life_image, life_rect)

        if self.blue_state:
            if (self.blue_state_end_time - GHOST_WARNING_TIME) <= pygame.time.get_ticks():
                alert_text = self.font.render("!!!", True, FONT_COLOR)
                alert_rect = alert_text.get_rect()
                alert_rect.midbottom = (self.surface.get_width() / 2, self.surface.get_height())
                self.surface.blit(alert_text, alert_rect)
