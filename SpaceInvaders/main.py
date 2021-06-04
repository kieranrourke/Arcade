import pygame
from spaceinvaders import SpaceInvaders
import pathlib
folder_path = pathlib.Path(__file__).parent.absolute()

# Initializing Pygame
pygame.init()

# Initlaizing Game
game = SpaceInvaders()
game.game_loop()
