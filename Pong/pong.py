import pygame
import pathlib
import os
import sys
sys.path.append(pathlib.Path(__file__).parent.parent.absolute())
from game import Game
import math
import random
import time



class Pong (Game):
    def __init__ (self,):
        folder_path = str(pathlib.Path(__file__).parent.absolute()) + '/'
        
        self.pong_ball_image = pygame.image.load(folder_path+'pong_ball.png')
        self.pong_ball_image = pygame.transform.scale(
            self.pong_ball_image, (30, 30))

        Game.__init__(self, 800, 800, "pong", self.pong_ball_image, 'pong_background.png')

        self.default_font = pygame.font.Font('freesansbold.ttf', 32) 
        self.countdown_font = pygame.font.SysFont("Arial", 128)
        
        self.blue_player_image = pygame.image.load(folder_path+'blue_rectangle.png')
        self.red_player_image = pygame.image.load(folder_path+'red_rectangle.png')
       
        self.blue_player_image = pygame.transform.scale(
            self.blue_player_image, (10, 100))
        self.red_player_image = pygame.transform.scale(
            self.red_player_image, (10, 100))
        
        self.blue_player = Player(self, self.blue_player_image,0)
        self.red_player = Player(self, self.red_player_image, self.xBound-10)
        self.pong_ball = Ball(self, self.pong_ball_image)        
        self.reset_button = Button(
            game=self,
            x=self.xBound-150,
            y=25, 
            text="Reset Game",
            text_size=24
        )

        self.blue_score = 0
        self.red_score = 0

    def game_loop(self, ):
        self.start_game()
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
            elif self.MOUSE_POS:
                if self.reset_button.is_clicked(self.MOUSE_POS):
                    self.reset_game()

            self.update_objects()
            collision = []
            collision.append(self.pong_ball.is_collision(self.blue_player, False))
            collision.append(self.pong_ball.is_collision(self.red_player, True))
            if True in collision:
                self.pong_ball.collision()
            self.draw_score()
            self.resetKeys()            
            self.update_display()
    
    def start_game(self):
        for i in range(3,0, -1):
            self.setMisc()
            red_text = self.countdown_font.render(str(i), True, (255,0,0))
            blue_text = self.countdown_font.render(str(i), True, (0,0,255))
            size = red_text.get_size()
            self.draw(red_text, self.xBound/2, self.yBound/2 - 150)
            self.draw(blue_text, self.xBound/2 - size[0] - 50, self.yBound/2 - 150)

            pygame.display.update()
            time.sleep(1)
            
    def reset_game(self):
        self.reset_objects()
        self.blue_score = 0
        self.red_score = 0
        self.start_game()

    def reset_objects(self):
        self.pong_ball.reset_ball()
        self.blue_player.reset_player()
        self.red_player.reset_player()

    def is_score(self):
        offset = 20
        if self.pong_ball.x_position > self.xBound + offset:  # Blue Score
            self.blue_score += 1
            self.pong_ball.reset_ball()
            time.sleep(1)
            self.reset_objects()
        elif self.pong_ball.x_position < 0 - offset:  # Red Score
            self.red_score += 1
            self.pong_ball.reset_ball()
            time.sleep(1)
            self.reset_objects()

    def draw_score(self):
        font = self.default_font
        blue_score = font.render(str(self.blue_score), True, (0,255,255))
        red_score = font.render(str(self.red_score), True, (255,0,0))
        self.draw(blue_score, self.xBound/2 - 100, 10)
        self.draw(red_score, self.xBound/2 + 35, 10)

    def update_display(self):
        self.red_player.draw_player()
        self.blue_player.draw_player()
        self.pong_ball.draw_ball()
        self.reset_button.draw_button()
        self.clock.tick(60)
        pygame.display.update()
    
    def update_objects(self):
        self.is_score()
        self.blue_player.update_player()
        self.red_player.update_player()
        self.pong_ball.update_postion()
    

class Player():
    def __init__(self, game, image, x_position):
        self.game = game
        self.image = image
        self.y_change = 0
        self.speed = 10
        self.x_starting_position = x_position
        self.y_starting_position = self.game.yBound/2
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
        self.y_change = -self.speed
    
    def move_down(self):
        self.y_change = self.speed
    
    def stop_player(self):
        self.y_change = 0
    
    def reset_player(self):
        self.x_position = self.x_starting_position
        self.y_position = self.y_starting_position


class Ball():
    def __init__(self, game, image):
        self.image = image
        self.game = game
        self.x_position = self.game.yBound/2
        self.y_position = self.game.xBound/2 
        self.x_speed = -12
        self.y_speed = 5
        self.x_change = self.x_speed
        self.y_change =  self.y_speed
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def draw_ball(self):
        self.game.draw(self.image, self.x_position, self.y_position)
    
    def hide_ball(self):
        self.y_position = 10000
    
    def is_collision(self, player: object, red: bool): 
        """ Determines if the ball has hit a player

        Args:
            player (object): The slider 
            red (bool): Determines if the player is red 

        Returns:
            bool : Returns if the player has collided  
        """
        # print(self.y_position - self.height, player.y_position, player.y_position + player.height)
        # print(self.x_position, player.x_position, player.x_position + player.width)
        if not red:
            if ((self.x_position >= player.x_position 
                and self.x_position <= player.x_position + player.width)
                and ((self.y_position >= player.y_position
                and self.y_position <= player.y_position + player.height)
                or (self.y_position + self.height >= player.y_position
                and self.y_position + self.height <= player.y_position + player.height))):
                    # print(self.y_position - self.height, player.y_position, player.y_position + player.height)
                    # print(self.x_position, player.x_position, player.x_position + player.width)
                    return True
        else:
            # print(self.y_position, player.y_position, player.y_position + player.height) 
            # print(self.x_position + self.width, player.x_position - player.width) 
            if  ((self.x_position + self.width >= player.x_position - player.width)
                and ((self.y_position >= player.y_position 
                and self.y_position <= player.y_position + player.height)
                or (self.y_position + self.height >= player.y_position
                and self.y_position + self.height <= player.y_position + player.height))):
                    return True
        return False
            

    def collision(self):
        if self.x_position > self.game.xBound/2:
            self.x_position -= 31
        else:
            self.x_position += 31
        self.negative_reciprical(hit_type="player")

    def negative_reciprical(self, hit_type):
        if hit_type == "boundary":
            self.x_change, self.y_change = self.x_change, -self.y_change
        elif hit_type == "player":
            self.x_change, self.y_change = -self.x_change, self.y_change

    def update_postion(self):
        self.check_boundary()
        self.x_position += self.x_change
        self.y_position += self.y_change

    def check_boundary(self,):
        offset = 20  #This leaves room for saves along the x axis
        if self.y_position < 0: 
            self.y_position += 10
            self.negative_reciprical(hit_type="boundary")
        elif self.y_position > self.game.yBound or self.y_position > self.game.yBound - self.height:
            self.y_position -= 10
            self.negative_reciprical(hit_type="boundary")
        
    
    def reset_ball(self):
        self.x_position = self.game.xBound/2
        self.y_position = random.randint(100, self.game.yBound-100) 
        if 1 == random.randint(0,1):
            self.x_change = -self.x_speed
        else:
            self.x_change = self.x_speed
        if 1 == random.randint(0,1):
            self.y_change = self.y_speed
        else:
            self.y_change = -self.y_speed

class Button:
    def __init__(self, game, x, y, text, text_size = 32) -> None:
        self.x = x
        self.y = y
        self.text_size = text_size
        self.game = game
        self.text = text

        self.generate_button()

    def generate_button(self):
        self.font = pygame.font.SysFont('Arial', self.text_size)
        self.button_text = self.font.render(self.text, True, (128,128,128))
        self.size = self.button_text.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
    
    def draw_button(self):
        self.game.draw(self.button_text, self.x, self.y)
    
    def is_clicked(self, pos: tuple) -> bool:
        """Tests if a point is inside the button

        Args:
            pos (Tuple): Click position

        Returns:
            bool: Returns if its in the button 
        """
        return self.rect.collidepoint(pos[0], pos[1])


if __name__ == '__main__':
    pygame.init()
    pong = Pong()
    pong.game_loop()