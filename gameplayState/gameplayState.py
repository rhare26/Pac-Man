import pygame as pygame
import constants
from constants import MAX_GHOSTS, MAX_FRUITS, STARTING_LIVES, DOT_POINTS, ENERGIZER_POINTS, BLUE_STATE_TIME, \
    CAUGHT_BLUE_GHOST_POINTS, FRUIT_POINTS, POINTS_BEFORE_NEW_GHOST, POINTS_BEFORE_NEW_FRUIT, FRUIT_STATE_TIME, \
    GHOST_WARNING_TIME, FONT_FILE, SMALL_FONT_SIZE, BG_COLOR, FONT_COLOR, PLAYER_IMAGE_OPEN
from gameplayState.spriteFactory import SpriteFactory
from gameplayState.mazeFactory import MazeFactory
from gameplayState.ghost import Ghost
from gameplayState.sprites import collision
from state import State
from pygame import Surface, K_SPACE, K_w



class GameplayState(State):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)
        State.gameplay_state = self
        self.level_score = 0
        self.previous_levels_score = 0

        # Game variables
        self.game_over = False
        self.blue_state = False
        self.blue_state_end_time = 0
        self.fruit_state = False
        self.fruit_state_end_time = 0
        self.lives = STARTING_LIVES

        # Screen
        self.font = pygame.font.Font(FONT_FILE, SMALL_FONT_SIZE)

        # Maze & sprites
        self.maze_factory = MazeFactory(self.surface)
        self.maze_factory.set_new_maze()
        self.blocks = self.maze_factory.get_blocks()
        self.energizers = self.maze_factory.get_energizers()
        self.dots = self.maze_factory.get_dots()

        self.sprite_factory = SpriteFactory(MAX_GHOSTS, MAX_FRUITS, self.blocks, self.surface)
        self.player = self.sprite_factory.get_player()
        self.ghosts: list[Ghost] = [self.sprite_factory.get_ghost()]
        self.num_current_ghosts = 1

        self.fruits = []
        self.num_fruits_deployed = 0

        self.next_state = self

    # STATE METHODS #
    def update(self, joystick_pos, key_presses):
        # Default next state if nothing is changed
        self.next_state = self  # default state if nothing changed

        self.move_and_draw(joystick_pos, key_presses)  # move all sprites and blit to surface
        self.check_collisions()  # check for collisions between player and: ghosts, dots, energizers, fruits


        self.check_substates()  # check timers for blue state and fruit state
        self.check_conditions()  # check if time to add a new ghost, add a new fruit, or win the game
        self.update_game_stats_display()  # update score and lives display

    def check_substates(self):
        if self.blue_state:
            if self.blue_state_end_time <= pygame.time.get_ticks():
                self.end_blue_state()

            #  TODO: clean this up
            reset = True
            for g in self.ghosts:
                if g.is_vulnerable:
                    reset = False
            if reset:
                self.blue_state = False

        if self.fruit_state:
            if self.fruit_state_end_time <= pygame.time.get_ticks():
                self.fruits = []
                self.fruit_state = False
    def move_and_draw(self, joystick_pos, key_presses):
        # Update background, maze walls, and dots
        self.surface.fill(BG_COLOR)
        for s in self.blocks + self.dots + self.energizers + self.fruits:
            s.draw()

        # Move sprites
        for s in self.ghosts:
            s.determine_move(joystick_pos, key_presses)
            s.draw()

        self.player.determine_move(joystick_pos, key_presses)
        self.player.draw()

    def check_collisions(self):
        # Dots
        collided_dot = collision(self.player, self.dots)
        if collided_dot:
            self.dots.remove(collided_dot)
            self.level_score += DOT_POINTS

        # Energizers
        collided_energizer = collision(self.player, self.energizers)
        if collided_energizer:
            self.energizers.remove(collided_energizer)
            self.level_score += ENERGIZER_POINTS
            for collided_ghost in self.ghosts:
                collided_ghost.set_blue_state()
            self.blue_state = True
            self.blue_state_end_time = pygame.time.get_ticks() + BLUE_STATE_TIME

        # Ghosts
        collided_ghost = collision(self.player, self.ghosts)
        if collided_ghost:
            if collided_ghost.is_vulnerable:
                collided_ghost.reset()
                self.level_score += CAUGHT_BLUE_GHOST_POINTS
            else:
                self.lives -= 1
                if self.lives > 0:
                    self.reset_all_sprites()
                else:
                    self.next_state = self.lose_state

        # Fruit
        collided_fruit = collision(self.player, self.fruits)
        if collided_fruit:
            self.level_score += FRUIT_POINTS
            self.fruits.remove(collided_fruit)
            self.fruit_state = False

    def check_conditions(self):
        if (self.num_current_ghosts < MAX_GHOSTS) and \
                (self.level_score > self.num_current_ghosts * POINTS_BEFORE_NEW_GHOST):
            self.ghosts.append(self.sprite_factory.get_ghost())
            self.num_current_ghosts += 1
        if (self.num_fruits_deployed < MAX_FRUITS) and \
                (self.level_score > (self.num_fruits_deployed + 1) * POINTS_BEFORE_NEW_FRUIT):
            self.fruits.append(self.sprite_factory.get_fruit())
            self.num_fruits_deployed += 1
            self.fruit_state_end_time = pygame.time.get_ticks() + FRUIT_STATE_TIME
            self.fruit_state = True

    def get_next_state(self, key_presses, buttons):
        # Lose state would have already been updated when checking ghost collisions

        # If you press pause while in gameplay state
        if key_presses[K_SPACE] or buttons[constants.MENU_BUTTON]:
            return self.menu_state

        # If you do the cheatcode
        if key_presses[K_w]:
            return self.win_state

        if not self.dots:  # no dots left
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
        score_text = self.font.render(str(self.get_game_score()), True, FONT_COLOR)
        score_rect = score_text.get_rect()
        score_rect.bottomright = (self.surface.get_width(), self.surface.get_height())
        self.surface.blit(score_text, score_rect)

        life_image = pygame.image.load(PLAYER_IMAGE_OPEN) # fix this
        life_image = pygame.transform.rotate(life_image, 180)
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

    def get_game_score(self):
        return self.previous_levels_score + self.level_score
    #  TODO: this is duplicating constructor code, needs fix
    def reset_keep_score(self):
        # Game variables
        self.game_over = False
        self.blue_state = False
        self.blue_state_end_time = 0
        self.fruit_state = False
        self.fruit_state_end_time = 0
        self.lives = STARTING_LIVES
        self.previous_levels_score += self.level_score
        self.level_score = 0

        # Maze & sprites
        self.maze_factory.set_new_maze()
        self.blocks = self.maze_factory.get_blocks()
        self.energizers = self.maze_factory.get_energizers()
        self.dots = self.maze_factory.get_dots()

        self.sprite_factory = SpriteFactory(MAX_GHOSTS, MAX_FRUITS, self.blocks,  self.surface)
        self.ghosts: list[Ghost] = [self.sprite_factory.get_ghost()]
        self.num_current_ghosts = 1
        self.player = self.player = self.sprite_factory.get_player()

        self.fruits = []
        self.num_fruits_deployed = 0

        self.next_state = self
