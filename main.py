from Games.Pong import pong
from Games.Space_Invaders import spaceinvaders 
from Main_Menu.menu import MainMenu
from Games.game import Game
import pygame
import pathlib


pygame.init()

if __name__ == '__main__':
    background_folder_path = str(pathlib.Path(__file__).parent.absolute()) + '/Utils/'

    main_menu_background = pygame.image.load(background_folder_path+'main_menu_background.png')
    pong_background = pygame.image.load(background_folder_path+'pong_background.png')
    space_invaders_background = pygame.image.load(background_folder_path+'space_invaders_background.png') 
    space_invaders_background = pygame.image.load(background_folder_path+'space_invaders_menu_background.png')
    background_music_path = background_folder_path+'background.wav' 

    game = Game(
        xBound=800,
        yBound=800,
        caption="Arcade",
        icon=pygame.image.load(background_folder_path+'icon.jpg'),
        background=main_menu_background
    )

    pong_game = pong.Pong(game)
    space_invaders_game = spaceinvaders.SpaceInvaders(game)
    menu = MainMenu(game, pong_game, space_invaders_game, main_menu_background, background_music_path)
    menu.display_loop()