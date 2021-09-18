import random
import math

import pygame
from pygame import mixer
import pathlib

# Fix Python/Github error
folder_path = str(pathlib.Path(__file__).parent.absolute()) + '/'

# Creating the Game Class
# ! Game class should be used/adjusted for other games in the aracde


class Game:
    """General Game class
    """
    def __init__(self, xBound, yBound, caption, icon, backgroundFileName:str):
        self.caption = caption
        self.icon = icon
        self.xBound = xBound
        self.yBound = yBound
        self.font = pygame.font.Font('freesansbold.ttf', 64)
        self.background = pygame.image.load(folder_path + backgroundFileName)
        self.background = pygame.transform.scale(
            self.background, (xBound, yBound))
        # Sets up the game loop Variables
        self.running = True
        self.inMenu = True
        self.inGame = True
        self.screen = pygame.display.set_mode((self.xBound, self.yBound))
        # The way user input is tracked
        self.WKEY, self.AKEY, self.SKEY, self.DKEY = False, False, False, False
        self.ENTERKEY, self.BACKKEY = False, False
        self.UPARROWKEY, self.DOWNARROwKEY, self.UPUPARROWKEY, self.UPDOWNARROWKEY = False, False, False, False
        self.QUITKEY = False
        self.SPACEKEY = False
        self.ESCAPEKEY = False
        self.UPAKEY, self.UPDKEY, self.UPWKEY, self.UPSKEY = False, False, False, False
        self.clock = pygame.time.Clock()

    def setMisc(self):
        self.setIcon()
        self.setCaption()
        self.screen.fill((255, 255, 255))
        self.draw(self.background, 0, 0)

    def setIcon(self,):
        pygame.display.set_icon(self.icon)

    def setCaption(self,):
        pygame.display.set_caption(self.caption)

    def draw(self, image, x, y):
        self.screen.blit(image, (x, y))

    def checkEvents(self):
        """In pygame user inputs are done by events.
        This function uses the boolean values intialized 
        in the constructor to track user input
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.inMenu, self.QUITKEY, self.inGame = False, False, True, False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.WKEY = True
                elif event.key == pygame.K_a:
                    self.AKEY = True
                elif event.key == pygame.K_s:
                    self.SKEY = True
                elif event.key == pygame.K_d:
                    self.DKEY = True
                elif event.key == pygame.K_BACKSPACE:
                    self.BACKKEY = True
                elif event.key == pygame.K_RETURN:
                    self.ENTERKEY = True
                elif event.key == pygame.K_SPACE:
                    self.SPACEKEY = True
                elif event.key == pygame.K_ESCAPE:
                    self.ESCAPEKEY = True
                elif event.key == pygame.K_UP:
                    self.UPARROWKEY = True
                elif event.key == pygame.K_DOWN:
                    self.DOWNARROwKEY = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.UPAKEY = True
                elif event.key == pygame.K_d:
                    self.UPDKEY = True
                elif event.key == pygame.K_w:
                    self.UPWKEY = True
                elif event.key == pygame.K_s:
                    self.UPSKEY = True
                elif event.key == pygame.K_UP:
                    self.UPUPARROWKEY = True
                elif event.key == pygame.K_DOWN:
                    self.UPDOWNARROWKEY = True


    def resetKeys(self):
        """Reset all keys
        """
        self.WKEY, self.AKEY, self.SKEY, self.DKEY, self.ENTERKEY, self.BACKKEY, self.SPACEKEY, self.UPAKEY, self.UPDKEY, self.ESCAPEKEY, self.UPWKEY, self.UPSKEY, self.UPARROWKEY, self.DOWNARROwKEY, self.UPUPARROWKEY, self.UPDOWNARROWKEY\
        = False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False
