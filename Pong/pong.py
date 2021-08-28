import pygame
import pathlib
import os
import sys
sys.path.append(pathlib.Path(__file__).parent.parent.absolute())
from game import Game
import math


pygame.init()

class Pong (Game):
    def __init__ (self,):
        folder_path = str(pathlib.Path(__file__).parent.absolute()) + '\\'
        
        self.pong_ball_image = pygame.image.load(folder_path+'pong_ball.png')
        self.pong_ball_image = pygame.transform.scale(
            self.pong_ball_image, (30, 30))

        Game.__init__(self, 800, 800, "pong", self.pong_ball_image, 'pong_background.png')
        
        self.blue_player_image = pygame.image.load(folder_path+'blue_rectangle.png')
        self.red_player_image = pygame.image.load(folder_path+'red_rectangle.png')
       
        self.blue_player_image = pygame.transform.scale(
            self.blue_player_image, (10, 100))
        self.red_player_image = pygame.transform.scale(
            self.red_player_image, (10, 100))
        
        self.blue_player = Player(self, self.blue_player_image,0)
        self.red_player = Player(self, self.red_player_image, self.xBound-10)
        self.pong_ball = Ball(self, self.pong_ball_image)        

    def game_loop(self, ):
        while self.inGame:
            self.setMisc()
            self.checkEvents()

            if self.WKEY:
                self.blue_player.move_up()
            elif self.SKEY:
                self.blue_player.move_down()
            elif self.UPWKEY or self.UPSKEY:
                self.blue_player.stop_player()
            elif self.UPARROWKEY:
                self.red_player.move_up()
            elif self.DOWNARROwKEY:
                self.red_player.move_down()
            elif self.UPUPARROWKEY or self.UPDOWNARROWKEY:
                self.red_player.stop_player()

            self.update_objects()
            collision = self.pong_ball.is_collision(self.blue_player, self.red_player)
            if collision: 
                self.pong_ball.collision()


            self.resetKeys()
            
            self.update_display()
    
    def update_display(self):
        self.red_player.draw_player()
        self.blue_player.draw_player()
        self.pong_ball.draw_ball()
        # self.clock.tick(60)
        pygame.display.update()
    
    def update_objects(self):
        self.blue_player.update_player()
        self.red_player.update_player()
        self.pong_ball.update_postion()



class Player():
    def __init__(self, game, image, x_position):
        self.game = game
        self.image = image
        self.y_change = 0
        self.y_position = self.game.yBound/2
        self.x_position = x_position
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    def update_player(self):
        self.y_position += self.y_change
        self.check_boundary()


    def draw_player(self):
        self.game.draw(self.image, self.x_position, self.y_position)

    def check_boundary(self):
        if self.y_position < 0 or self.y_position > self.game.yBound - self.height:
            self.stop_player()
    
    def move_up(self):
        self.y_change = -2
    
    def move_down(self):
        self.y_change = +2
    
    def stop_player(self):
        self.y_change = 0



class Ball():
    def __init__(self, game, image):
        self.image = image
        self.game = game
        self.x_position = self.game.yBound/2
        self.y_position = self.game.xBound/2 
        self.x_change = -1
        self.y_change = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def draw_ball(self):
        self.game.draw(self.image, self.x_position, self.y_position)
    
    def is_collision(self, blue_player, red_player):
        blue_distance = math.sqrt(math.pow(blue_player.x_position-self.x_position, 2) +
                             math.pow(blue_player.y_position-self.y_position, 2))

        red_distance = math.sqrt(math.pow(red_player.x_position-self.x_position, 2) +
                             math.pow(red_player.y_position-self.y_position, 2))
     
        return blue_distance < 15 or red_distance < 30

    def collision(self):
        self.negative_reciprical()

    def negative_reciprical(self):
        temp = self.y_change
        self.y_change = -self.x_change
        self.x_change = temp

    def update_postion(self):
        self.check_boundary()
        self.x_position += self.x_change
        self.y_position += self.y_change

    def check_boundary(self):
        if self.y_position < 0 or self.y_position > self.game.yBound:
            self.negative_reciprical()

if __name__ == '__main__':
    pong = Pong()
    pong.game_loop()