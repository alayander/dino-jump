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
        self.GRID_SIZE = 10  # scale entire pygame panel size
        self.U_WIDTH, self.U_HEIGHT = 100, 60  # full panel proportions (20x19 dino)
        self.REF = 5  # proportions for the axis
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

        # Setup Display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clk = pygame.time.Clock()
        self.start_game = False
        pygame.display.set_caption("DinoJump!")


class Obstacle(Game):

    def __init__(self, obs_type, speed):
        super().__init__()
        
        # obs_type "CCC" "ccc" "midb" "highb"

        # Generation Constants
        self.X_DIST = self.WIDTH # width of the board is where obstacles generate 
        
        self.obs_type = obs_type

        # Run Initiation
        self.setup_sprites()
        self.setup_parameters()

        # Game Attributes
        self.obs_x = self.X_DIST
        self.speed = speed   # number of pixels moved per loop
        
        
    def setup_sprites(self):
        if self.obs_type == "CCC":
            self.OBS_ARRAY = np.array(
            [
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
            ]
            )
        else: 
            self.OBS_ARRAY = np.array([
                    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
                ]
            )
      
    def setup_parameters(self):
        if self.obs_type == "CCC":
            self.obs_width = len(self.OBS_ARRAY[0])
            self.obs_height = len(self.OBS_ARRAY)
            self.obs_y = self.REF_AXIS - self.obs_height * self.GRID_SIZE
        else:
            self.obs_width = len(self.OBS_ARRAY[0])
            self.obs_height = len(self.OBS_ARRAY)
            self.obs_y = self.REF_AXIS - self.obs_height * self.GRID_SIZE
        
    def draw(self):
        for row in range(self.obs_height):
            for col in range(self.obs_width):
                if self.OBS_ARRAY[row, col] == 1:
                    pygame.draw.rect(
                        self.screen,  # The game window or screen
                        self.BLOCK_COLOR,  # Color of the block (RGB or RGBA value)
                        (
                            self.obs_x
                            + col
                            * self.GRID_SIZE,  # X-coordinate of the rectangle's top-left corner
                            self.obs_y
                            + row
                            * self.GRID_SIZE,  # Y-coordinate of the rectangle's top-left corner
                            self.GRID_SIZE,  # Width of the rectangle (in pixels)
                            self.GRID_SIZE,  # Height of the rectangle (in pixels)
                        ),
                    )    
        
        
        
class Obstacle_Interaction(Game):

    def __init__(self):
        super().__init__()

        self.curr_cooldown = 30 # generates after however long (IN PIXELS)
        self.cooldown_variance = np.linspace(10, 50, 5) # variance to cooldown time
        self.base_cooldown = 20 # must wait this long before new cacti generates
    
    def update(self, curr_obs):
        updated_obs = []
        for obs in curr_obs:
            if obs.obs_x + obs.obs_width - obs.speed > 0:
                obs.obs_x -= obs.speed
                updated_obs.append(obs)
                # if its still good (x coord is within its width on the board, it's a keep')
                # update the object obs's x coordinate
                # update_obs = # updating procedure
                # if keep:
                # updated_obs.append(update_obs)
        return updated_obs
    
    def generate_obstacle(self):
        if self.curr_cooldown == 0: # time to generate an object
            # pick some object and speed
            speed = 5 # Should be a formula based on the score or other variables
            obs_type = "CCC"
            new_obs = Obstacle(obs_type, speed)
            # 
            self.curr_cooldown = self.base_cooldown + random.choice(self.cooldown_variance)
            return True, new_obs
        else:
            self.curr_cooldown -= 1
            return False, ""
    
    def draw(self, curr_obs):
        for obs in curr_obs:
            obs.draw()


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
        self.dino_array = self.JUMP_ARRAY
        self.curr_walk = self.UPDATE_WALK_FRAMES
        self.dino_x = 2 * self.GRID_SIZE
        self.dino_y = self.OG_DINO_Y
        self.is_right_foot_down = True
        self.is_jumping = True      # Detects if jumping signal is given
        self.jump_start_time = 0
        self.is_ducking = False     # Detects if ducking signal is given
        self.jumping_coefficient = self.JUMP_HEIGHT / (self.TIME_TO_PEAK**2 - self.JUMP_TIME*self.TIME_TO_PEAK) 

    def setup_sprites(self):
        self.JUMP_ARRAY = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.LRUN_ARRAY = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.RRUN_ARRAY = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.RDUCK_ARRAY = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.LDUCK_ARRAY = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )

    def setup_parameters(self):

        # Converts user ratios for the pygame GUI display
        self.JUMP_HEIGHT = self.U_JUMP_HEIGHT * self.GRID_SIZE

        # Block shape and size
        self.DINO_HEIGHT, self.DINO_WIDTH = self.JUMP_ARRAY.shape  # all the same size
        self.OG_DINO_Y = self.REF_AXIS - self.DINO_HEIGHT * self.GRID_SIZE

        # Dino Jump - Calculates time related values so it makes sense physically
        self.TIME_TO_PEAK = self.JUMP_TIME / 2
        self.ACCEL = (2 * self.JUMP_HEIGHT) / (self.TIME_TO_PEAK**2)
        self.INIT_V = self.TIME_TO_PEAK * self.ACCEL

    ###################################

    def check_jumping(self):
        # Check if jumping

        # NOTE: JUMP_TIME is given in seconds, whereas pygame records time in milliseconds. This conversion must be 
        # kept in mind throughout the coding process
        if pygame.time.get_ticks() - self.jump_start_time <= self.JUMP_TIME * 1000: 
            jump_time = (pygame.time.get_ticks() - self.jump_start_time)/1000   # There may be a more efficient way to do this
            # self.dino_y = self.OG_DINO_Y - self.INIT_V * jump_time + self.ACCEL * jump_time**2
            self.dino_y = self.OG_DINO_Y - self.jumping_coefficient*(jump_time**2 - self.JUMP_TIME*jump_time) # Tried using the ACCEL and INIT_V function, but it was a little funky
            # Breakdown of formula: intercepts are at t = 0 and t = JUMP_TIME. Thus, a quadratic relation can be drawn using the two intercepts.
        else:
            if self.is_jumping == True:
                self.jump_start_time = pygame.time.get_ticks() # Record the time that the jump started


    def update(self):
        
        # Update walking state
        if pygame.time.get_ticks()/1000 * self.FPS - self.curr_walk >= game.UPDATE_WALK_FRAMES: # UPDATE_WALK_FRAMES may be too low
            self.curr_walk = pygame.time.get_ticks()/1000 * self.FPS
            dino.is_right_foot_down = not dino.is_right_foot_down

        # Update Dino Array
        if dino.is_jumping or pygame.time.get_ticks() - self.jump_start_time < self.JUMP_TIME * 1000:
            self.dino_array = self.JUMP_ARRAY

        elif dino.is_ducking and dino.is_right_foot_down:
            self.dino_array = self.RDUCK_ARRAY

        elif dino.is_ducking:
            self.dino_array = self.LDUCK_ARRAY

        elif dino.is_right_foot_down:
            self.dino_array = self.RRUN_ARRAY

        else:
            self.dino_array = self.LRUN_ARRAY

    # Takes whichever sprite is dino_array currently and it's current location and draws to the board
    def draw(self):
        for row in range(self.DINO_HEIGHT):
            for col in range(self.DINO_WIDTH):
                if self.dino_array[row, col] == 1:
                    pygame.draw.rect(
                        self.screen,  # The game window or screen
                        self.BLOCK_COLOR,  # Color of the block (RGB or RGBA value)
                        (
                            self.dino_x
                            + col
                            * self.GRID_SIZE,  # X-coordinate of the rectangle's top-left corner
                            self.dino_y
                            + row
                            * self.GRID_SIZE,  # Y-coordinate of the rectangle's top-left corner
                            self.GRID_SIZE,  # Width of the rectangle (in pixels)
                            self.GRID_SIZE,  # Height of the rectangle (in pixels)
                        ),
                    )

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


def draw_all(curr_obs):
    game.screen.fill(game.BG_COLOR)
    dino.draw()
    obstacle.draw(curr_obs)
    pygame.display.flip()
    game.clk.tick(game.FPS)


##################################################
# VOID SETUP
##################################################

# Initialises the Dino Game
game = Game()
dino = Dino()

obstacle = Obstacle_Interaction()
curr_obs = []

# Start Pygame
pygame.init()


##################################################
# VOID LOOP
##################################################

# Wait until first space bar press until the game starts
while not game.start_game:
    check_start_game()
    draw_all(curr_obs )

# Simulates the whole loop running
while True:

    check_user_input()
    
    # checking actions
    
    dino.check_jumping()
    
    # new_obs_generated (boolean), new_obs
    new_obs_generated, new_obs = obstacle.generate_obstacle()
    if new_obs_generated:
        curr_obs.append(new_obs)
    
    # updating all objects
    
    dino.update()
    
    curr_obs = obstacle.update(curr_obs)

    draw_all(curr_obs)


#############################################################################
# END USER WORK AREA
#############################################################################



