##################################################
# Imports
##################################################

import sys
import random
import numpy as np
import pygame


##################################################
# Class Modules
##################################################


class Game:

    def __init__(self):

        # Display Constants
        self.GRID_SIZE = 6  # scale entire pygame panel size
        self.U_WIDTH, self.U_HEIGHT = 150, 55  # full panel proportions (20x19 dino)
        self.REF, self.LOW_BIRD, self.HIGH_BIRD = 2, 18, 28  # proportions for the axis
        self.BG_COLOR = (255, 255, 255)  # white colour (background)
        self.BLOCK_COLOR = (0, 0, 0)  # black colour (sprites)

        # Timing Constants
        self.FPS = 60  # frames per second
        self.UPDATE_WALK_FRAMES = 6  # how many frames to wait before dino switches legs

        # Setup Axis
        self.WIDTH, self.HEIGHT = (
            self.U_WIDTH * self.GRID_SIZE,
            self.U_HEIGHT * self.GRID_SIZE,
        )
        self.REF_AXIS = self.HEIGHT - self.REF * self.GRID_SIZE
        self.LOW_BIRD_AXIS = self.HEIGHT - self.LOW_BIRD * self.GRID_SIZE
        self.HIGH_BIRD_AXIS = self.HEIGHT - self.HIGH_BIRD * self.GRID_SIZE

        # Setup Display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clk = pygame.time.Clock()
        self.start_game = False
        pygame.display.set_caption("DinoJump!")

    def draw(self, curr_object):
        for row in range(curr_object.height):
            for col in range(curr_object.width):
                if curr_object.ARRAY[row, col] == 1:
                    pygame.draw.rect(
                        self.screen,  # The game window or screen
                        self.BLOCK_COLOR,  # Color of the block (RGB or RGBA value)
                        (
                            curr_object.x
                            + col
                            * self.GRID_SIZE,  # X-coordinate of the rectangle's top-left corner
                            curr_object.y
                            + row
                            * self.GRID_SIZE,  # Y-coordinate of the rectangle's top-left corner
                            self.GRID_SIZE,  # Width of the rectangle (in pixels)
                            self.GRID_SIZE,  # Height of the rectangle (in pixels)
                        ),
                    )


class Obstacle(Game):

    def __init__(self, obs_type, speed):
        super().__init__()

        # Generation Constants
        self.x = self.WIDTH  # width of the board is where obstacles generate
        self.obs_type = obs_type
        self.speed = speed  # number of pixels moved per loop

        # Run Initiation
        self.setup_sprites()
        self.setup_parameters()

    def setup_sprites(self):
        if self.obs_type == "c":
            self.ARRAY = np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 0, 0],
                    [1, 1, 0, 1, 1, 0, 1, 1],
                    [1, 1, 0, 1, 1, 0, 1, 1],
                    [1, 1, 0, 1, 1, 0, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [0, 1, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 0, 0],
                ]
            )
        elif self.obs_type == "C":
            self.ARRAY = np.array(
                [
                    [0, 0, 0, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 1, 1],
                    [0, 0, 0, 1, 1, 0, 1, 1],
                    [0, 0, 0, 1, 1, 0, 1, 1],
                    [0, 0, 0, 1, 1, 0, 1, 1],
                    [1, 1, 0, 1, 1, 1, 1, 1],
                    [1, 1, 0, 1, 1, 1, 1, 1],
                    [1, 1, 0, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 1, 1, 0, 0],
                    [0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0],
                ]
            )
        elif self.obs_type == "b":
            self.ARRAY = np.array(
                [
                    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                ]
            )
        else:
            self.ARRAY = np.array(
                [
                    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                ]
            )

    def setup_parameters(self):
        self.height, self.width = self.ARRAY.shape
        if self.obs_type in ("c", "C"):
            self.y = self.REF_AXIS - self.height * self.GRID_SIZE
        elif self.obs_type == "b":
            self.y = self.LOW_BIRD_AXIS - self.height * self.GRID_SIZE
        else:
            self.y = self.HIGH_BIRD_AXIS - self.height * self.GRID_SIZE


class ObstacleInteraction(Game):

    def __init__(self):
        super().__init__()

        self.curr_cooldown = 0  # generates after however long (IN PIXELS)
        self.cooldown_variance = np.linspace(10, 50, 5)  # variance to cooldown time
        self.base_cooldown = 40  # must wait this long before new cacti generates
        self.curr_obs = []  # obstacles generated for the game
        self.possible_speeds = [10]
        self.possible_objects = ["c", "C", "ccc", "CC", "cCc", "cc", "b", "B"]

    def update(self):
        for i, obs in enumerate(self.curr_obs):
            if obs.x + obs.width > 0:
                obs.x -= obs.speed
            else:
                self.curr_obs[i] = ""
        if "" in self.curr_obs:
            self.curr_obs.remove("")

    def make_obstacle_choice(self):
        # choose between cactus arrangement, low bird, or high bird
        return np.random.choice(self.possible_objects), np.random.choice(
            self.possible_speeds
        )

    def generate_obstacle(self):
        if self.curr_cooldown == 0:  # time to generate an object
            new_obstacle, new_speed = self.make_obstacle_choice()
            for i, obs in enumerate(new_obstacle):
                new_obs = Obstacle(obs, new_speed)
                # Note: Need to figure out correct line below to get the cacti close together
                new_obs.x += (new_obs.width + 1) * i * new_obs.GRID_SIZE
                self.curr_obs.append(new_obs)
            self.curr_cooldown = self.base_cooldown + random.choice(
                self.cooldown_variance
            )
        else:
            self.curr_cooldown -= 1


class Dino(Game):

    def __init__(self):
        super().__init__()

        # Jumping Constants
        self.U_JUMP_HEIGHT = 30  # dino is 20x19 in size
        self.JUMP_TIME = 0.6  # full time to rise up and fall back down, seconds

        # Run Initiation
        self.setup_sprites()
        self.setup_parameters()

        # Game Attributes
        self.ARRAY = self.JUMP_ARRAY
        self.curr_walk = self.UPDATE_WALK_FRAMES
        self.x = 2 * self.GRID_SIZE
        self.y = self.OG_DINO_Y
        self.is_right_foot_down = True
        self.is_jumping = True  # Detects if jumping signal is given
        self.jump_start_time = 0
        self.is_ducking = False  # Detects if ducking signal is given
        self.jumping_coefficient = self.JUMP_HEIGHT / (
            self.TIME_TO_PEAK**2 - self.JUMP_TIME * self.TIME_TO_PEAK
        )

    def setup_sprites(self):
        self.JUMP_ARRAY = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.LRUN_ARRAY = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.RRUN_ARRAY = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.RDUCK_ARRAY = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.LDUCK_ARRAY = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )

    def setup_parameters(self):

        # Converts user ratios for the pygame GUI display
        self.JUMP_HEIGHT = self.U_JUMP_HEIGHT * self.GRID_SIZE

        # Block shape and size
        self.height, self.width = self.JUMP_ARRAY.shape  # all the same size
        self.OG_DINO_Y = self.REF_AXIS - self.height * self.GRID_SIZE

        # Dino Jump - Calculates time related values so it makes sense physically
        self.TIME_TO_PEAK = self.JUMP_TIME / 2
        self.ACCEL = (2 * self.JUMP_HEIGHT) / (self.TIME_TO_PEAK**2)
        self.INIT_V = self.TIME_TO_PEAK * self.ACCEL

    ###################################

    def check_jumping(self):
        # Check if jumping

        # NOTE: JUMP_TIME is given in seconds, whereas pygame records time in milliseconds.
        # This conversion must be kept in mind throughout the coding process
        if pygame.time.get_ticks() - self.jump_start_time <= self.JUMP_TIME * 1000:
            jump_time = (
                pygame.time.get_ticks() - self.jump_start_time
            ) / 1000  # There may be a more efficient way to do this
            # self.dino_y = self.OG_DINO_Y - self.INIT_V * jump_time + self.ACCEL * jump_time**2
            self.y = self.OG_DINO_Y - self.jumping_coefficient * (
                jump_time**2 - self.JUMP_TIME * jump_time
            )  # Tried using the ACCEL and INIT_V function, but it was a little funky
            # Breakdown of formula: intercepts are at t = 0 and t = JUMP_TIME.
            # Thus, a quadratic relation can be drawn using the two intercepts.
        else:
            if self.is_jumping:
                self.jump_start_time = (
                    pygame.time.get_ticks()
                )  # Record the time that the jump started
            else:
                self.y = self.OG_DINO_Y

    def update(self):

        # Update walking state
        if (
            pygame.time.get_ticks() / 1000 * self.FPS - self.curr_walk
            >= game.UPDATE_WALK_FRAMES
        ):  # UPDATE_WALK_FRAMES may be too low
            self.curr_walk = pygame.time.get_ticks() / 1000 * self.FPS
            dino.is_right_foot_down = not dino.is_right_foot_down

        # Update Dino Array
        if (
            dino.is_jumping
            or pygame.time.get_ticks() - self.jump_start_time < self.JUMP_TIME * 1000
        ):
            self.ARRAY = self.JUMP_ARRAY

        elif dino.is_ducking and dino.is_right_foot_down:
            self.ARRAY = self.RDUCK_ARRAY

        elif dino.is_ducking:
            self.ARRAY = self.LDUCK_ARRAY

        elif dino.is_right_foot_down:
            self.ARRAY = self.RRUN_ARRAY

        else:
            self.ARRAY = self.LRUN_ARRAY


##################################################
# Function Modules
##################################################


def check_start_game():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game.start_game = True
            # Start the game with the dino jumping
            dino.is_jumping = True
            dino.check_jumping()


def check_user_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dino.is_jumping = True
            if event.key == pygame.K_DOWN:
                dino.is_ducking = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                dino.is_jumping = False
            if event.key == pygame.K_DOWN:
                dino.is_ducking = False


def draw_all():
    game.screen.fill(game.BG_COLOR)
    for obs in obstacle.curr_obs:
        game.draw(obs)
    game.draw(dino)
    pygame.display.flip()
    game.clk.tick(game.FPS)


##################################################
# VOID SETUP
##################################################

# Initialises the Dino Game
game = Game()
dino = Dino()

obstacle = ObstacleInteraction()

# Start Pygame
pygame.init()


##################################################
# VOID LOOP
##################################################

# Wait until first space bar press until the game starts
while not game.start_game:
    check_start_game()
    draw_all()

# Simulates the whole loop running
while True:
    check_user_input()
    dino.check_jumping()
    obstacle.generate_obstacle()
    dino.update()
    obstacle.update()
    draw_all()


#############################################################################
# END USER WORK AREA
#############################################################################
