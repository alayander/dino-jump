#############################################################################
# IMPORTS
#############################################################################

import sys
import random
import numpy as np
import pygame

from sprites import import_sprite


#############################################################################
# GAME MODULE
#############################################################################


class Game:

    def __init__(self):

        # Editable Constants
        self.GRID_SIZE = 4  # scale entire pygame panel size (only for online display)
        self.WIDTH, self.HEIGHT = (
            150,
            48,
        )  # define pixel height and width for actual board
        self.GROUND_Y, self.LOW_BIRD_Y, self.HIGH_BIRD_Y = (
            2,
            18,
            28,
        )  # proportions for the three axes of obstacles

        # Non-Editable Constants
        self.BG_COLOR = (255, 255, 255)  # white colour (background)
        self.BLOCK_COLOR = (0, 0, 0)  # black colour (sprites)
        self.FPS = 60  # frames per second frames update
        self.GROUND_AXIS = (
            self.HEIGHT - self.GROUND_Y
        )  # defines axis height with (0,0) lower left corner
        self.LOW_BIRD_AXIS = (
            self.HEIGHT - self.LOW_BIRD_Y
        )  # defines axis height with (0,0) lower left corner
        self.HIGH_BIRD_AXIS = (
            self.HEIGHT - self.HIGH_BIRD_Y
        )  # defines axis height with (0,0) lower left corner
        self.start_game = False
        self.game_over = False
        self.close_all = False  # JOSH once this triggers the whole program closes, triggered by pressing space again

        # Setup Display
        self.game_state_array = np.zeros((self.HEIGHT, self.WIDTH))
        self.screen = pygame.display.set_mode(
            (self.WIDTH * self.GRID_SIZE, self.HEIGHT * self.GRID_SIZE)
        )
        self.clk = pygame.time.Clock()
        pygame.display.set_caption("DinoJump!")

        # Initiate the Dino and ObstacleManager Classes
        self.dino = Dino(self.GROUND_AXIS)
        self.all_obstacles = ObstacleManager(
            self.WIDTH, self.GROUND_AXIS, self.LOW_BIRD_AXIS, self.HIGH_BIRD_AXIS
        )

    def update_board_pixels(self, curr_object):

        # Get all the values from the curr_object and the board
        x, y = int(curr_object.x), int(curr_object.y)
        height, width = curr_object.HEIGHT, curr_object.WIDTH
        board_width = self.game_state_array.shape[1]
        min_width, max_width = min(max(x, 0), board_width), max(
            0, min(x + width, board_width)
        )

        # Segment the display section to draw to (especially if cropped)
        left_edge = curr_object.ARRAY[:, -(max_width - min_width) :].astype(int)
        right_edge = curr_object.ARRAY[:, : (max_width - min_width)].astype(int)
        set_location = self.game_state_array[
            y : y + height, min_width:max_width
        ].astype(int)

        # Extract bitwise AND and OR of incorporating the new drawing
        if min_width == 0 and max_width != 0:
            filled_location = np.bitwise_or(left_edge, set_location)
            is_hit = np.sum(np.bitwise_and(left_edge, set_location))
        else:
            filled_location = np.bitwise_or(right_edge, set_location)
            is_hit = np.sum(np.bitwise_and(right_edge, set_location))
        self.game_state_array[y : y + height, min_width:max_width] = filled_location

        # If a hit is detected, we end the game
        if is_hit:
            self.game_over = True

        return

    def draw_to_screen(self):

        # Use GRID_SIZE to increase the software viewing panel
        draw_array = np.repeat(
            np.repeat(self.game_state_array, self.GRID_SIZE, axis=0),
            self.GRID_SIZE,
            axis=1,
        )

        # For each pixel in the game board, draw them in black and white to the screen
        for row in range(draw_array.shape[0]):
            for col in range(draw_array.shape[1]):
                if draw_array[row, col] == 1:
                    pygame.draw.rect(
                        self.screen,
                        self.BLOCK_COLOR,
                        (col, row, 1, 1),
                    )

    def check_start_game(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.start_game = True
                self.dino.is_jumping = True
                self.dino.update_jumping_location()

    def check_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.dino.is_jumping = True
                if event.key == pygame.K_DOWN:
                    self.dino.is_ducking = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.dino.is_jumping = False
                if event.key == pygame.K_DOWN:
                    self.dino.is_ducking = False

    def draw_all(self):
        self.screen.fill(game.BG_COLOR)
        self.game_state_array = np.zeros((game.HEIGHT, game.WIDTH))
        for obs in self.all_obstacles.curr_obs:
            self.update_board_pixels(obs)
        self.update_board_pixels(self.dino)
        self.draw_to_screen()
        pygame.display.flip()
        self.clk.tick(self.FPS)

    def check_close_panel(
        self,
    ):  # JOSH checks for another space bar press to close the whole program
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.close_all = True


#############################################################################
# SINGLE OBSTACLE MODULE
#############################################################################


class SingleObstacle(Game):

    def __init__(
        self, obs_type, speed, init_width, GROUND_AXIS, LOW_BIRD_AXIS, HIGH_BIRD_AXIS
    ):

        # Generation Constants
        self.OBS_TYPE = obs_type  # string, defines c C b B singular obstacle
        self.SPEED = speed  # number of pixels moved to the left per loop
        self.ARRAY = import_sprite(
            self.OBS_TYPE
        )  # calls sprites: with type to get pixel array
        self.x = init_width  # initial position of spirt at right edge of board
        self.HEIGHT, self.WIDTH = (
            self.ARRAY.shape
        )  # height and width of the array to call

        # Inherited from Game
        self.GROUND_AXIS, self.LOW_BIRD_AXIS, self.HIGH_BIRD_AXIS = (
            GROUND_AXIS,
            LOW_BIRD_AXIS,
            HIGH_BIRD_AXIS,
        )

        # Define the y axis this obstacle sprite travels along
        if self.OBS_TYPE in ("c", "C"):
            self.y = self.GROUND_AXIS - self.HEIGHT
        elif self.OBS_TYPE == "b":
            self.y = self.LOW_BIRD_AXIS - self.HEIGHT
        else:
            self.y = self.HIGH_BIRD_AXIS - self.HEIGHT


#############################################################################
# OBSTACLE MANAGEMENT MODULE
#############################################################################


class ObstacleManager(Game):

    def __init__(self, WIDTH, GROUND_AXIS, LOW_BIRD_AXIS, HIGH_BIRD_AXIS):

        # Timing Constants
        self.curr_cooldown = (
            0  # counts the number of frames before next obstacle generated
        )
        self.BASE_COOLDOWN = (
            20  # must wait how many frames before new obstacle generates
        )
        self.COOLDOWN_VARIANCE = np.linspace(
            10, 30, 5
        )  # variance of how many frames to add the to baseline

        # Inherited from game
        self.WIDTH = WIDTH
        self.GROUND_AXIS, self.LOW_BIRD_AXIS, self.HIGH_BIRD_AXIS = (
            GROUND_AXIS,
            LOW_BIRD_AXIS,
            HIGH_BIRD_AXIS,
        )

        # Possible Choices for Compound Obstacles and Speeds
        self.ALL_SPEEDS = [3]
        self.ALL_OBSTACLE_GROUPS = ["c", "C", "ccc", "CC", "cCc", "cc", "b", "B"]

        # Hold all current obstacle objects to keep track of
        self.curr_obs = []

    def update_location(self):

        # Only care about valid obstacles on the game board
        self.curr_obs = [obs for obs in self.curr_obs if (obs.x + obs.WIDTH > 0)]

        # Update each obstacle's location by its speed
        for obs in self.curr_obs:
            obs.x -= obs.SPEED

    def choose_random_obstacle_attributes(self):
        # Choose the next obstacle: cactus arrangement, low bird, or high bird
        return np.random.choice(self.ALL_OBSTACLE_GROUPS), np.random.choice(
            self.ALL_SPEEDS
        )

    def generate_obstacle(self):

        # When the cooldown reaches zero, a new obstacle is generated
        if self.curr_cooldown <= 0:
            new_obstacle, new_speed = self.choose_random_obstacle_attributes()
            for i, obs in enumerate(new_obstacle):
                new_obs = SingleObstacle(
                    obs,
                    new_speed,
                    self.WIDTH,
                    self.GROUND_AXIS,
                    self.LOW_BIRD_AXIS,
                    self.HIGH_BIRD_AXIS,
                )
                new_obs.x += (new_obs.WIDTH + 1) * i
                self.curr_obs.append(new_obs)
            self.curr_cooldown = self.BASE_COOLDOWN + random.choice(
                self.COOLDOWN_VARIANCE
            )

        # Otherwise, we decrement the cooldown timer every loop
        else:
            self.curr_cooldown -= 1


#############################################################################
# DINO MODULE
#############################################################################


class Dino(Game):

    def __init__(self, GROUND_AXIS):

        # Jumping Constants
        self.JUMP_HEIGHT = 25  # specify how many pixels upwards the max-height goes
        self.JUMP_TIME = 500  # specify time in milliseconds dino takes to land
        self.UPDATE_WALK_FRAMES = 3  # how many frames to wait before dino switches legs

        # Inherited from Game
        self.GROUND_AXIS = GROUND_AXIS

        # Get all pixel arrays for the dino from sprite import (dino:20x19)
        self.JUMP_ARRAY = import_sprite("jump")
        self.RRUN_ARRAY = import_sprite("right run")
        self.LRUN_ARRAY = import_sprite("left run")
        self.RDUCK_ARRAY = import_sprite("right duck")
        self.LDUCK_ARRAY = import_sprite("left duck")
        self.DONE_ARRAY = import_sprite("done")

        # Define Array and Dimensions
        self.ARRAY = self.JUMP_ARRAY  # the first array is still dino frame
        self.HEIGHT, self.WIDTH = (
            self.JUMP_ARRAY.shape
        )  # get height and widrh to be able to call
        self.OG_DINO_Y = (
            self.GROUND_AXIS - self.HEIGHT
        )  # define dino's top left pixel height
        self.x = 5  # dino x stays put, how many pixels from left edge
        self.y = self.OG_DINO_Y  # assigned to the y position
        self.is_right_foot_down = (
            True  # used to change between left and right foot arrays displayed
        )
        self.is_jumping = True  # detects if jumping signal is given
        self.is_ducking = False  # detects if ducking signal is given
        self.is_hit = False  # becomes true when obstacle and dino collide
        self.jump_start_time = 0  # used to count time in jumping
        self.curr_walk = (
            self.UPDATE_WALK_FRAMES
        )  # counts how many frames before the legs switch

        # Calculates Time Constants (physically realistic jumping)
        self.TIME_TO_PEAK = self.JUMP_TIME / 2
        self.ACCEL = (2 * self.JUMP_HEIGHT) / (self.TIME_TO_PEAK**2)
        self.INIT_V = self.TIME_TO_PEAK * self.ACCEL
        self.JUMP_COEF = self.JUMP_HEIGHT / (
            self.TIME_TO_PEAK**2 - self.JUMP_TIME * self.TIME_TO_PEAK
        )

    def update_jumping_location(self):
        # Using timing to determine if we are mid jump and y position should be adjusted
        if pygame.time.get_ticks() - self.jump_start_time <= self.JUMP_TIME:
            jump_time = pygame.time.get_ticks() - self.jump_start_time
            self.y = self.OG_DINO_Y - self.JUMP_COEF * (
                jump_time**2 - self.JUMP_TIME * jump_time
            )
        else:
            if self.is_jumping:
                self.jump_start_time = pygame.time.get_ticks()
            else:
                self.y = self.OG_DINO_Y

    def update_frame(self):

        # Determine when the dino foot change happens
        if self.curr_walk <= 0:
            self.is_right_foot_down = not self.is_right_foot_down
            self.curr_walk = self.UPDATE_WALK_FRAMES
        self.curr_walk -= 1

        # Update dino pixel array
        if (
            self.is_jumping
            or pygame.time.get_ticks() - self.jump_start_time < self.JUMP_TIME
        ):
            self.ARRAY = self.JUMP_ARRAY
        elif self.is_ducking and self.is_right_foot_down:
            self.ARRAY = self.RDUCK_ARRAY
        elif self.is_ducking:
            self.ARRAY = self.LDUCK_ARRAY
        elif self.is_right_foot_down:
            self.ARRAY = self.RRUN_ARRAY
        else:
            self.ARRAY = self.LRUN_ARRAY

        # If the game is over, show the dead dino frame
        if game.game_over:
            self.ARRAY = self.DONE_ARRAY  # JOSH a new sprite array for the "done" look


#############################################################################
# VOID SETUP
#############################################################################

# Initialises the Dino Game
game = Game()

# Start Pygame
pygame.init()
game.draw_all()


#############################################################################
# VOID LOOP
#############################################################################

# Wait until first space bar press until the game starts
while not game.start_game:
    game.check_start_game()

# Simulates the whole loop running
while not game.game_over:
    game.check_user_input()
    game.dino.update_jumping_location()
    game.all_obstacles.generate_obstacle()
    game.dino.update_frame()
    game.all_obstacles.update_location()
    game.draw_all()

print("game over!")  # JOSH everything after here is the end game state!
game.dino.update_frame()
game.draw_all()
while not game.close_all:
    game.check_close_panel()


# CURRENT IMPLEMENTATION: DRAW_AND_CHECK_COLLISION_ALL
# Ideally, draw and check_collision would be two separate functions
# However, currently running the two functions separately results in the game ending much earlier than expected
# Current Rationale: Since the function determines the set_location twice for one obs, it could affect future calculations
# Need to see how the data within the obstacles are changed after running the function.

#############################################################################
# END USER WORK AREA
#############################################################################
