from pong import Pong 
import pygame

if __name__ == '__main__':
    pygame.init()
    pong_game = Pong()
    pong_game.game_loop()
