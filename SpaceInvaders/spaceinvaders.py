import random
import math

import pygame
from pygame import mixer
from game import Game
from menu import *
import pathlib


folder_path = str(pathlib.Path(__file__).parent.absolute()) + '\\'
# Creating SpaceInvaders


class SpaceInvaders(Game):
    def __init__(self,):
        Game.__init__(self, 800, 800, 'Space Invaders',
                      pygame.image.load(folder_path+"ufo.png"))
        self.numEnemies = 4
        self.difficulty = 'Easy'
        mixer.music.load(folder_path+'background.wav')
        mixer.music.play(-1)
        self.menuBackground = pygame.image.load(folder_path+'menu.png')
        self.menuBackground = pygame.transform.scale(
            self.menuBackground, (self.xBound, self.yBound))
        self.currentMenu = 'Main'
        self.mainMenu = MainMenu(self, self.menuBackground, [220, 400])
        self.helpMenu = HelpMenu(self, self.background,)
        self.highscoresMenu = HighscoresMenu(self, self.background)
        self.difficultyMenu = DifficultyMenu(self, self.background)
        self.textInputMenu = TextInput(self, self.background)
        try:
            with open("highscores.json", 'r') as f:
                self.scores = json.load(f)
        except:
            self.scores = {}

    def createPlayer(self):
        self.player = Player(self)

    def createEnemies(self,):
        self.enemies = []
        if self.difficulty == 'Easy':
            self.numEnemies = 3
        elif self.difficulty == 'Medium':
            self.numEnemies = 4
        else:
            self.numEnemies = 5
        for i in range(self.numEnemies):
            self.enemies.append(Enemy(self))

    def createBullet(self):
        self.bullet = Bullet(self)

    def applyDifficulty(self):
        """
        Easy: Fast Player xChange, Slow Enemy movement, 3 Enemies, Fast bullet movement
        Medium: Normal Player xChange, Normal enemy movement, 4 Enemies, Normal bullet movement
        Hard: Normal Player xChange, Faster enemy movement, 5 Enemies Normal bullet movement
        """
        if self.difficulty == 'Easy':
            self.player.xMovement = 10
            for i in range(self.numEnemies):
                self.enemies[i].xMovement = 2
            self.bullet.yChange = -10

        elif self.difficulty == 'Medium':
            self.player.xMovement = 8
            for i in range(self.numEnemies):
                self.enemies[i].xMovement = 4
            self.bullet.yChange = -8

        elif self.difficulty == 'Hard':
            self.player.xMovement = 8
            for i in range(self.numEnemies):
                self.enemies[i].xMovement = 7
            self.bullet.yChange = -8

        for i in range(self.numEnemies):
            self.enemies[i].xChange = self.enemies[i].xMovement

    def createScoreboard(self):
        self.scoreboard = Scoreboard(self)

    def setMisc(self):
        self.setIcon()
        self.setCaption()
        self.screen.fill((255, 255, 255))
        self.draw(self.background, 0, 0)

    def updateDisplay(self):
        '''
        Updates Display as well as draws the objects used
        '''
        self.draw(self.player.image, self.player.xPos, self.player.yPos)

        if self.bullet.isFired:
            self.draw(self.bullet.image, self.bullet.xPos, self.bullet.yPos)
        for i in range(self.numEnemies):
            self.draw(self.enemies[i].image,
                      self.enemies[i].xPos, self.enemies[i].yPos)

        self.scoreboard.showScore()
        pygame.display.update()

    def gameOver(self) -> None:
        '''
        Intiate game over sequence
        '''
        print('hi')
        text = self.font.render(
            f"GAME OVER: {self.scoreboard.score}", True, (255, 255, 255))
        self.screen.blit(text, (160, 275))
        self.textInputMenu.displayLoop()
        self.inMenu = True

    def menuLoop(self):
        while self.inMenu:
            if self.currentMenu == 'Main':
                self.mainMenu.displayLoop()
            elif self.currentMenu == 'Choose Difficulty':
                self.difficultyMenu.displayLoop()
            elif self.currentMenu == 'Highscores':
                self.highscoresMenu.displayLoop()
            elif self.currentMenu == 'Help':
                self.helpMenu.displayLoop()
            elif self.currentMenu == 'Quit':
                self.running, self.inMenu, self.inGame = False, False
            else:
                self.inGame = True
                self.inMenu = False

    def gameLoop(self):
        while self.inGame:
            self.setMisc()

            # Checking the user input
            self.checkEvents()

            # Shooting/Moving the image based on user input
            if self.AKEY or self.DKEY or self.UPAKEY or self.UPDKEY:
                self.player.changeDirection()
            elif self.SPACEKEY:
                self.bullet.fireBullet(self.player)

            # Updating Player position and checking boundaries
            self.player.updatePos()
            self.player.checkBoundary()

            # Updating Enemies position and checking boundaries
            for i in range(self.numEnemies):
                self.enemies[i].updatePos()
                self.enemies[i].checkBoundary()
                # Checking if an enemy has reached the player
                if self.enemies[i].reachPlayer(self.player):
                    for i in range(self.numEnemies):
                        self.enemies[i].hideEnemy()
                    self.gameOver()

            # Bullet Mechanics
            if self.bullet.isFired:
                self.bullet.updatePos()
                self.bullet.drawBullet()
                # Collision Detection
                self.bullet.isHit(self.enemies, self.scoreboard)
                self.bullet.checkBoundary()

            # Update Display
            self.updateDisplay()
            self.resetKeys()
            self.clock.tick(60)

    def game_loop(self,):
        self.running = True
        while self.running:
            self.clock = pygame.time.Clock()
            self.menuLoop()
            self.createPlayer()
            self.createEnemies()
            self.createBullet()
            self.createScoreboard()
            self.applyDifficulty()
            self.gameLoop()


# Creating the Player Class
class Player():
    def __init__(self, game):
        self.game = game
        self.image = pygame.image.load(folder_path+"player.png")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.xPos = 300
        self.yPos = 800
        self.xChange = 0
        self.xMovement = 0
        self.yChange = 0
        self.width, self.height = self.image.get_rect().size

    def drawPlayer(self,) -> None:
        '''
        Draws an player using its x and y position
        '''
        self.screen.blit(self.image, (self.xPos, self.yPos))

    def changeDirection(self):
        # Might not work
        if self.game.AKEY:
            self.xChange = -self.xMovement
        elif self.game.DKEY:
            self.xChange = self.xMovement
        elif self.game.UPAKEY:
            self.xChange += self.xMovement
        elif self.game.UPDKEY:
            self.xChange -= self.xMovement

    def updatePos(self,):
        self.xPos += self.xChange

    def checkBoundary(self,):
        if self.xPos <= 0:
            self.xPos = 0
        elif self.xPos >= self.game.xBound-self.width:
            self.xPos = self.game.xBound-self.width
        if self.yPos <= 0:
            self.yPos = 0
        elif self.yPos >= self.game.yBound-self.height:
            self.yPos = self.game.yBound - self.height

# Creating the Enemy Class


class Enemy():
    def __init__(self, game):
        self.game = game
        self.image = pygame.image.load(folder_path+"enemy.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.xPos = random.randint(0, 500)
        self.yPos = random.randint(1, 100)
        self.xChange = 0
        self.xMovement = 0
        self.yChange = 100
        self.width, self.height = self.image.get_rect().size

    def drawEnemy(self,) -> None:
        '''
        Draws an enemy using its x and y position
        '''
        self.screen.blit(self.image, (self.xPos, self.yPos))

    def resetEnemy(self,) -> None:
        '''
        Resets the enemy when shot to a random starting location
        '''
        self.xPos = random.randint(0, 800-self.width)
        self.yPos = random.randint(1, 100)

    def hideEnemy(self,) -> None:
        '''
        Hide enemies from the display
        '''
        self.xPos = self.game.xBound + 1000
        self.yPos = self.game.xBound - 2000


    def checkBoundary(self):
        if self.xPos <= 0:
            self.xChange = self.xMovement
            self.yPos += self.yChange
        elif self.xPos >= self.game.xBound-self.width:
            self.xChange = -self.xMovement
            self.yPos += self.yChange

        if self.yPos <= 0:
            self.yPos = 0
        elif self.yPos >= self.game.yBound - self.height:
            self.yPos = self.game.yBound - self.height

    def reachPlayer(self, player):
        '''
        Returns True if enemy has reached player
        '''
        return self.yPos > self.game.yBound - player.height-75

    def updatePos(self):
        self.xPos += self.xChange


# Creating the Bullet Class
class Bullet:
    def __init__(self, game):
        self.game = game
        self.shootingSound = mixer.Sound(folder_path+'shoot.wav')
        self.hitSound = mixer.Sound(folder_path+'invaderhit.wav')
        self.image = pygame.image.load(folder_path+"bullet.png")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.xPos = 0
        self.yPos = 0
        self.yChange = -5
        self.width, self.height = self.image.get_rect().size
        self.isFired = False

    def drawBullet(self,) -> None:
        '''
        Draws an bullet using its x and y position
        '''
        self.game.screen.blit(self.image, (self.xPos, self.yPos))

    def resetBullet(self) -> None:
        '''
        Resets the bullet and updates if it has been fired
        '''
        self.yPos = 0
        self.xPos = 0
        self.isFired = False

    def fireBullet(self, player) -> None:
        '''
        Fires a bullet based on the players positioning
        '''
        self.isFired = True
        self.xPos = player.xPos
        self.yPos = player.yPos - 10
        self.shootingSound.play()

    def updatePos(self,):
        self.yPos += self.yChange

    def isCollision(self, enemyX: float, enemyY: float,) -> bool:
        '''
        Checks to see if the bullet has hit an enemy
        '''
        # Formula to check is a little sus but works decently
        distance = math.sqrt(math.pow(enemyX-self.xPos, 2) +
                             math.pow(enemyY-self.yPos, 2))
        return distance < 65

    def isHit(self, enemies: list, score: object):
        numEnemies = len(enemies)
        for i in range(numEnemies):
            if self.isCollision(enemies[i].xPos, enemies[i].yPos):
                self.hitSound.play()
                self.resetBullet()
                enemies[i].resetEnemy()
                score.score += 1
        if self.yPos < 0 or self.yPos > self.game.yBound:
            self.resetBullet()

    def checkBoundary(self,):
        if self.yPos < 0 or self.yPos > self.game.yBound:
            self.resetBullet()


# Creating the Scoreboard Class
class Scoreboard:
    def __init__(self, game):
        self.game = game
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        # Generating in the top left of the screen
        self.xPos = 10
        self.yPos = 10

    def showScore(self,) -> None:
        '''
        Shows the score on the top left of the sceen
        '''
        score = self.font.render(
            f"Score : {self.score}", True, (255, 255, 255))
        self.game.screen.blit(score, (self.xPos, self.yPos))