import pygame
from pygame import mixer
import pathlib
import sys
from ..game import Game, Button
sys.path.append(pathlib.Path(__file__).parent.parent.absolute())
import math
import random
import time


class Pong ():
    def __init__ (self, game):
        self.game = game
        self.folder_path = str(pathlib.Path(__file__).parent.absolute()) + '/Utils/'
        
        self.pong_ball_image = pygame.image.load(self.folder_path+'pong_ball.png')
        self.pong_ball_image = pygame.transform.scale(
            self.pong_ball_image, (30, 30))

        self.background_image = pygame.image.load(self.folder_path+'pong_background.png')
        self.background_image = pygame.transform.scale(self.background_image, (self.game.xBound, self.game.yBound))

        self.default_font = pygame.font.Font('freesansbold.ttf', 32) 
        self.countdown_font = pygame.font.SysFont("Arial", 128)
        
        self.blue_player_image = pygame.image.load(self.folder_path+'blue_rectangle.png')
        self.red_player_image = pygame.image.load(self.folder_path+'red_rectangle.png')
       
        self.blue_player_image = pygame.transform.scale(
            self.blue_player_image, (10, 100))
        self.red_player_image = pygame.transform.scale(
            self.red_player_image, (10, 100))
        
        self.blue_player = Player(game, self.blue_player_image,0)
        self.red_player = Player(game, self.red_player_image, self.game.xBound-10)
        self.pong_ball = Ball(game, self, self.pong_ball_image)        

        self.reset_button = Button(
            game=game,
            x=self.game.xBound-200,
            y=15, 
            text="Reset Game",
            color=(255,165,0),
            text_size=30
        )

        self.quit_button = Button(
            game=game,
            x=0+20,
            y=15,
            text="Quit",
            color=(255,165,0),
            text_size=30
        )

        self.blue_score = 0
        self.red_score = 0

        
        self.player_hit_sound = mixer.Sound(self.folder_path+'pong_hit.wav') 
        self.wall_hit_sound = mixer.Sound(self.folder_path+'pong_wall_hit.wav') 
        self.player_hit_sound.set_volume(0.2)
        self.wall_hit_sound.set_volume(0.2)

    def game_loop(self, ):
        mixer.music.load(self.folder_path+'background.wav')
        mixer.music.set_volume(0.05)
        mixer.music.play(-1)
        self.start_game()
        while self.game.inGame:
            self.game.setMisc()
            self.game.checkEvents()

            if self.game.WKEY:
                self.blue_player.move_up()
            elif self.game.SKEY:
                self.blue_player.move_down()
            elif self.game.UPWKEY or self.game.UPSKEY:
                self.blue_player.stop_player()
            elif self.game.UPARROWKEY:
                self.red_player.move_up()
            elif self.game.DOWNARROwKEY:
                self.red_player.move_down()
            elif self.game.UPUPARROWKEY or self.game.UPDOWNARROWKEY:
                self.red_player.stop_player()
            elif self.game.MOUSE_POS:
                if self.reset_button.is_clicked(self.game.MOUSE_POS):
                    self.reset_game()
                elif self.quit_button.is_clicked(self.game.MOUSE_POS):
                    mixer.music.stop()
                    self.game.inGame = False

            self.update_objects()

            collision = self.pong_ball.is_collision(self.blue_player, False)
            if collision:
                self.pong_ball.collision(self.blue_player)
            collision = self.pong_ball.is_collision(self.red_player, True)
            if collision:
                self.pong_ball.collision(self.red_player)

            self.draw_score()
            self.game.resetKeys()            
            self.update_display()
    
    def start_game(self):
        self.game.inGame=True
        self.game.background = self.background_image
        for i in range(3,0, -1):
            self.game.setMisc()
            red_text = self.countdown_font.render(str(i), True, (255,0,0))
            blue_text = self.countdown_font.render(str(i), True, (0,0,255))
            size = red_text.get_size()
            self.game.draw(red_text, self.game.xBound/2, self.game.yBound/2 - 150)
            self.game.draw(blue_text, self.game.xBound/2 - size[0] - 50, self.game.yBound/2 - 150)

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
        if self.pong_ball.x_position > self.game.xBound + offset:  # Blue Score
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
        self.game.draw(blue_score, self.game.xBound/2 - 100, 10)
        self.game.draw(red_score, self.game.xBound/2 + 35, 10)

    def update_display(self):
        self.red_player.draw_player()
        self.blue_player.draw_player()
        self.pong_ball.draw_ball()
        self.reset_button.draw_button()
        self.quit_button.draw_button()
        self.game.clock.tick(60)
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
    def __init__(self, game, pong_game, image):
        self.pong_game = pong_game
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
            self.pong_game.wall_hit_sound.play()
            self.x_change, self.y_change = self.x_change, -self.y_change
        elif hit_type == "player":
            self.pong_game.player_hit_sound.play()
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