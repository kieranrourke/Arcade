import random
import math

import pygame
from pygame import mixer

# Creating the Game Class


class Game:
    def __init__(self, xBound, yBound, caption, icon):
        self.caption = caption
        self.icon = icon
        self.xBound = xBound
        self.yBound = yBound
        self.font = pygame.font.Font('freesansbold.ttf', 64)
        self.background = pygame.image.load('background.png')
        self.background = pygame.transform.scale(
            self.background, (xBound, yBound))
        self.running = True
        self.inMenu = True
        self.inGame = True
        self.screen = pygame.display.set_mode((self.xBound, self.yBound))
        self.WKEY, self.AKEY, self.SKEY, self.DKEY = False, False, False, False
        self.ENTERKEY, self.BACKKEY = False, False
        self.QUITKEY = False
        self.SPACEKEY = False
        self.ESCAPEKEY = False
        self.UPAKEY, self.UPDKEY, = False, False

    def setIcon(self,):
        pygame.display.set_icon(self.icon)

    def setCaption(self,):
        pygame.display.set_caption(self.caption)

    def draw(self, image, x, y):
        self.screen.blit(image, (x, y))

    def checkEvents(self):
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
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.UPAKEY = True
                elif event.key == pygame.K_d:
                    self.UPDKEY = True

    def resetKeys(self):
        self.WKEY, self.AKEY, self.SKEY, self.DKEY, self.ENTERKEY, self.BACKKEY, self.SPACEKEY, self.UPAKEY, self.UPDKEY, self.ESCAPEKEY\
            = False, False, False, False, False, False, False, False, False, False

    