#########################
# Imports
#########################


import pygame
import sys
import numpy as np
import random



#########################
# Class Modules
#########################


class DinoJump:


    #############################################################################
    # Run on Init
    #############################################################################


    def __init__(self):
        
        # Start Pygame
        pygame.init()

        # Display Constants
        self.GRID_SIZE = 5                        # scale entire pygame panel size
        self.U_WIDTH, self.U_HEIGHT = 150, 60     # full panel proportions (20x19 dino)
        self.FPS = 60                             # frames per second
        self.BG_COLOR = (255, 255, 255)           # white colour (background)
        self.BLOCK_COLOR = (0, 0, 0)              # black colour (sprites)
        self.UPDATE_WALK_FRAMES = 8               # how many frames to wait before dino switches legs
        self.GND, self.REF, self.BIRD = 4, 5, 20  # proportions for how far apart the axis are seperated

        # Game Constants
        self.U_JUMP_HEIGHT = 30                   # dino is 20x19 in size, it should jump around its height, pixels
        self.JUMP_TIME = 0.6                      # full time to rise up and fall back down, seconds
        self.CACTUS_CHANCE = 0.4                  # chance of cactus generation under this, float percent
        self.MID_BIRD_CHANCE = 0.5                # chance of mid bird generation between this and cactus, float percent
        self.ADDITIONAL_COOLDOWN = 0.5            # obstacles won't spawn so dino can't land, this is more wiggle room
        self.ADDITIONAL_MOVING_SPEED = 1          # baseline speed for obstacle movement speed, float magnification

        # Run Initiation
        self.setup_sprites()
        self.setup_parameters()


    def setup_sprites(self):
        self.jump_array = np.array([
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]   
            ])
        self.running_left_array = np.array([
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   
            ])
        self.running_right_array = np.array([
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]   
            ])
        self.ducking_right_array = np.array([
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
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ])
        self.ducking_left_array = np.array([
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
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ])
        self.cactus_array = np.array([
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
        ])
        self.mid_bird_array = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0]
        ])


    def setup_parameters(self):

        # Converts user ratios for the pygame GUI display
        self.JUMP_HEIGHT = self.U_JUMP_HEIGHT * self.GRID_SIZE
        self.WIDTH, self.HEIGHT = self.U_WIDTH * self.GRID_SIZE, self.U_HEIGHT * self.GRID_SIZE

        # Creates reference axis for objects to move along
        self.GND_AXIS = self.HEIGHT - self.GND * self.GRID_SIZE          # ground line in black
        self.REF_AXIS = self.HEIGHT - self.REF * self.GRID_SIZE          # main line the dino and cactus are on
        self.MID_BIRD_AXIS = self.HEIGHT - self.BIRD * self.GRID_SIZE    # mid bird flying line

        # Block shape and size
        self.dino_array = self.jump_array
        self.dino_height, self.dino_width = self.dino_array.shape
        self.dino_x, self.dino_y = 10, self.REF_AXIS - self.dino_height*self.GRID_SIZE
        self.original_dino_y = self.dino_y
        self.cactus_height, self.cactus_width = self.cactus_array.shape
        self.cactus_y = self.REF_AXIS - self.cactus_height*self.GRID_SIZE
        self.mid_bird_height, self.mid_bird_width = self.mid_bird_array.shape
        self.mid_bird_y = self.MID_BIRD_AXIS - self.mid_bird_height*self.GRID_SIZE
        self.curr_walk = self.UPDATE_WALK_FRAMES

        # Dino Jump - Calculates time related values so it makes sense physically
        self.time_to_peak = self.JUMP_TIME / 2
        self.acceleration = (2 * self.JUMP_HEIGHT) / (self.time_to_peak ** 2)
        self.init_velocity = self.time_to_peak * self.acceleration

        # Obstacle Generation - Values for how fast generated obstacles move
        self.COOLDOWN_TIME = self.JUMP_TIME + self.ADDITIONAL_COOLDOWN
        self.min_moving_speed = self.dino_width / (self.JUMP_TIME*5)
        self.real_moving_speed = int(self.min_moving_speed*self.ADDITIONAL_MOVING_SPEED)

        # Set up display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("DinoJump!")
        self.clock = pygame.time.Clock()

        # Game Attributes
        self.start_game = False
        self.is_right_foot_down = True
        self.is_jumping = True
        self.jump_start_time = 0
        self.is_ducking = False
        self.cannot_spawn_object = True
        self.cooldown_start_time = 0
        self.cactus_locs = []
        self.mid_bird_locs = []
        self.high_bird_locs = []


    #############################################################################
    # Drawing Functions
    #############################################################################


    # Draws the black line for the ground
    def draw_ground(self):
        for pixel in range(self.WIDTH):
            pygame.draw.rect(self.screen, self.BLOCK_COLOR, (pixel, self.GND_AXIS, self.GRID_SIZE, self.GRID_SIZE))


    # Takes whichever sprite is dino_array currently and it's current location and draws to the board
    def draw_dino(self):
        for row in range(self.dino_height):
            for col in range(self.dino_width):
                if self.dino_array[row, col] == 1:
                    pygame.draw.rect(self.screen, self.BLOCK_COLOR, (self.dino_x+col*self.GRID_SIZE, self.dino_y+row*self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE))


    # Determines which dino is shown on the board, running LR, jumping, ducking LR, and game over (TODO)
    def determine_and_draw_dino(self):
        self.curr_walk -= 1 # counting down
        if self.is_ducking and self.curr_walk == 0:
            self.curr_walk = self.UPDATE_WALK_FRAMES
            if self.is_right_foot_down: self.is_right_foot_down=False; self.dino_array=self.ducking_left_array
            else: self.is_right_foot_down=True; self.dino_array=self.ducking_right_array
        elif self.is_jumping:
            self.dino_array = self.jump_array
        elif self.curr_walk == 0: 
            self.curr_walk = self.UPDATE_WALK_FRAMES
            if self.is_right_foot_down: self.is_right_foot_down=False; self.dino_array=self.running_left_array
            else: self.is_right_foot_down=True; self.dino_array=self.running_right_array
        self.draw_dino()
        return


    # Draws all cactus obstacles in the array and moves them to the left afterwards
    def draw_cactus(self):
        for x_loc in self.cactus_locs:
            for row in range(self.cactus_height):
                for col in range(self.cactus_width):
                    if self.cactus_array[row, col] == 1:
                        pygame.draw.rect(self.screen, self.BLOCK_COLOR, (x_loc+col*self.GRID_SIZE, self.cactus_y+row*self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE))
        # Moves all cacti still on the board towards the dino at the moving speed
        self.cactus_locs = [cactus-self.real_moving_speed for cactus in self.cactus_locs if cactus-self.real_moving_speed >= -self.cactus_width]


    # Draws all mid bird obstacles in the array and moves them to the left afterwards
    def draw_mid_bird(self):
        for x_loc in self.mid_bird_locs:
            for row in range(self.mid_bird_height):
                for col in range(self.mid_bird_width):
                    if self.mid_bird_array[row, col] == 1:
                        pygame.draw.rect(self.screen, self.BLOCK_COLOR, (x_loc+col*self.GRID_SIZE, self.mid_bird_y+row*self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE))
        # Moves all mid birds still on the board towards the dino at the moving speed
        self.mid_bird_locs = [mid_bird-self.real_moving_speed for mid_bird in self.mid_bird_locs if mid_bird-self.real_moving_speed >= -self.mid_bird_width]


    #############################################################################
    # Helper Functions
    #############################################################################


    # While dino is jumping, based on time, calculates displacement back down, so the jump looks "right"
    def jump_progress(self, elapsed_time):
        if elapsed_time <= self.time_to_peak:
            return int((self.init_velocity * elapsed_time) - (0.5 * self.acceleration * elapsed_time**2))
        else: 
            half_elapsed_time = elapsed_time - self.time_to_peak
            return self.JUMP_HEIGHT - int(0.5 * self.acceleration * half_elapsed_time**2)


    # If possible, an item (cactus, mid bird) will be created and the cooldown will start
    def spawn_item(self):
        if self.cannot_spawn_object: return
        # Otherwise we can spawn a cactus right now
        random_chance = random.uniform(0, 1)
        if random_chance < self.CACTUS_CHANCE: 
            self.cactus_locs.append(self.WIDTH)
            self.cannot_spawn_object = True
            self.cooldown_start_time = pygame.time.get_ticks()
        elif random_chance < self.MID_BIRD_CHANCE: 
            self.mid_bird_locs.append(self.WIDTH)
            self.cannot_spawn_object = True
            self.cooldown_start_time = pygame.time.get_ticks()
        else: 
            return
        return


    #############################################################################
    # Main Loop
    #############################################################################


    def run(self):

        # Wait until first space bar pess until the game starts
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.start_game = True
                    self.jump_start_time = pygame.time.get_ticks()
            if self.start_game: break
            self.screen.fill(self.BG_COLOR)
            self.draw_ground()
            self.determine_and_draw_dino()
            pygame.display.flip()
            self.clock.tick(self.FPS)

        # Simulates the whole loop running
        while True:
            
            # First we detect to see if anything was triggered
            for event in pygame.event.get():
                # Closes the system window
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                # Checks for key press events
                if event.type == pygame.KEYDOWN:
                    # Dino Jump is triggered (space bar)
                    if event.key == pygame.K_SPACE and not self.is_jumping and not self.is_ducking:
                        self.is_jumping = True
                        self.jump_start_time = pygame.time.get_ticks()
                    # Dino duck is triggered (down key)
                    if event.key == pygame.K_DOWN and not self.is_jumping:
                        self.is_ducking = True
                # Checks for key release events
                if event.type == pygame.KEYUP:
                    # Dino duck is released (down key)
                    if event.key == pygame.K_DOWN:
                        self.is_ducking = False

            #############################################################################
            # USER WORK 
            #############################################################################

            # Try to spawn a new object
            self.spawn_item()

            # Calculate the jump position if jumping
            if self.is_jumping:
                elapsed_time = (pygame.time.get_ticks() - self.jump_start_time) / 1000
                if elapsed_time < self.JUMP_TIME:
                    self.dino_y = self.original_dino_y - self.jump_progress(elapsed_time)
                else:
                    self.dino_y = self.original_dino_y
                    self.is_jumping = False
                    self.curr_walk = self.UPDATE_WALK_FRAMES

            # There needs to be a timer related cool down before another can be spawned
            if self.cannot_spawn_object:
                elapsed_time = (pygame.time.get_ticks() - self.cooldown_start_time) / 1000
                if elapsed_time < self.COOLDOWN_TIME:
                    pass
                else: self.cannot_spawn_object = False

            # Draw everything and frame rate cap
            self.screen.fill(self.BG_COLOR)
            self.draw_ground()
            self.determine_and_draw_dino()
            self.draw_cactus()
            self.draw_mid_bird()
            pygame.display.flip()
            self.clock.tick(self.FPS)


            #############################################################################
            # END USER WORK AREA
            #############################################################################



#########################
# MAIN
#########################
print("*******************************\n\n")

if __name__ == "__main__":
    game = DinoJump()
    game.run()


print("\ndone\n*******************************")
#########################
# End
#########################