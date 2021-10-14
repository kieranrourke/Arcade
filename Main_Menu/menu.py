import pathlib
import pygame


class MainMenu():
    def __init__(self, game, pong_game, space_invaders_game, background):
        folder_path = str(pathlib.Path(__file__).parent.absolute()) + '/'

        self.game = game 
        self.pong_game = pong_game 
        self.space_invaders_game = space_invaders_game

        self.running = True
        self.background = background

        # Button coordinates are hard coded and found manually 
        self.pong_button = pygame.Rect((233,421),(306,123))
        self.space_invaders_button = pygame.Rect((194,149),(376,207))

    def display_loop(self):
        while self.running:
            self.game.setMisc()
            self.game.checkEvents()
            if self.game.MOUSE_POS:
                self.check_buttons()
            self.running = False if self.game.QUITKEY else True
            self.update_display()

    def check_buttons(self):
        if self.pong_button.collidepoint(self.game.MOUSE_POS):
            self.start_pong()
        elif self.space_invaders_button.collidepoint(self.game.MOUSE_POS):
            self.start_space_invaders()

    def start_pong(self):
        self.pong_game.game_loop()
        self.game.background=self.background
    
    def start_space_invaders(self):
        self.space_invaders_game.start_game()
        self.game.background = self.background

    def update_display(self):
        self.game.resetKeys()
        pygame.display.update()