import pygame
import pathlib
import os
import sys
from ..game import Game, Button
sys.path.append(pathlib.Path(__file__).parent.parent.absolute())
import math
import random
import time


class Pong (Game):
    def __init__ (self,):
        folder_path = str(pathlib.Path(__file__).parent.absolute()) + '/'
        
        self.pong_ball_image = pygame.image.load(folder_path+'pong_ball.png')
        self.pong_ball_image = pygame.transform.scale(
            self.pong_ball_image, (30, 30))

        self.background_image = pygame.image.load(folder_path+'pong_background.png')

        Game.__init__(self, 800, 800, "pong", self.pong_ball_image, self.background_image)

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

            collision = self.pong_ball.is_collision(self.blue_player, False)
            if collision:
                self.pong_ball.collision(self.blue_player)
            collision = self.pong_ball.is_collision(self.red_player, True)
            if collision:
                self.pong_ball.collision(self.red_player)

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
            time.sleep(0.5)
            
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
            self.reset_objects()
            time.sleep(0.5)
        elif self.pong_ball.x_position < 0 - offset:  # Red Score
            self.red_score += 1
            self.reset_objects()
            time.sleep(0.5)

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

        # Storing the different speeds for the ball 
        self.player_collision_speed = {'x': 11, 'y': 5}
        self.reset_speed = {'x': 8, 'y': 3}
        self.x_speed = -self.player_collision_speed['x']
        self.y_speed =  self.player_collision_speed['y']
        self.x_change = self.x_speed
        self.y_change =  self.y_speed

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.MAX_BOUNCE_ANGLE = 3 * (math.pi/12)  # 1.3 rad/75*

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
        ball_rectange = self.image.get_rect(topleft=(self.x_position, self.y_position))
        player_rectange = player.image.get_rect(topleft=(player.x_position, player.y_position))
        return ball_rectange.colliderect(player_rectange)
 
    def collision(self, player:object):
        if self.x_position > self.game.xBound/2:
            self.x_position -= 31
        else:
            self.x_position += 31
        self.collision_adjustment(hit_type="player", player=player)

    def collision_adjustment(self, hit_type, player=None):
        if hit_type == "boundary":
            self.x_change, self.y_change = self.x_change, -self.y_change
        elif hit_type == "player":
            self.x_change, self.y_change = self.player_collision_speed['x'], self.player_collision_speed['y']
            self.ball_collision_speed(player)

    def ball_collision_speed(self, player:object):
        """Generates the angle of collision between player and ball then updates player speed

        Args:
            player (object): player that hit the ball 
        """
        middle_ball = self.y_position + self.height/2
        middle_player = player.y_position + player.height/2 
        magnitude_speed = math.hypot(self.x_change, self.y_change) 

        relative_y_intersect = middle_ball - middle_player
        bounce_angle = relative_y_intersect/(player.height/2)
        # To stop the angle from surpassing the maximum angle 
        if bounce_angle > 1:
            bounce_angle = 1
        elif bounce_angle < -1:
            bounce_angle = -1

        
        bounce_angle *= self.MAX_BOUNCE_ANGLE

        if player.x_position > 200:  # Blue Player
            self.x_change, self.y_change = -magnitude_speed*math.cos(bounce_angle), -magnitude_speed*-math.sin(bounce_angle)
        else:
            self.x_change, self.y_change = magnitude_speed*math.cos(bounce_angle), -magnitude_speed*-math.sin(bounce_angle)

    def update_postion(self):
        self.check_boundary()
        self.x_position += self.x_change
        self.y_position += self.y_change

    def check_boundary(self,):
        offset = 20  #This leaves room for saves along the x axis
        if self.y_position < 0: 
            self.y_position += 10
            self.collision_adjustment(hit_type="boundary")
        elif self.y_position > self.game.yBound or self.y_position > self.game.yBound - self.height:
            self.y_position -= 10
            self.collision_adjustment(hit_type="boundary")
        
    
    def reset_ball(self):
        self.x_position = self.game.xBound/2
        self.y_position = random.randint(self.game.yBound/2-50, self.game.yBound/2+50)
        self.x_speed, self.y_speed = self.reset_speed['x'], self.reset_speed['y']
        if 1 == random.randint(0,1):
            self.x_change = -self.x_speed
        else:
            self.x_change = self.x_speed
        if 1 == random.randint(0,1):
            self.y_change = self.y_speed
        else:
            self.y_change = -self.y_speed


if __name__ == '__main__':
    pygame.init()
    pong = Pong()
    pong.game_loop()