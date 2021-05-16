import pygame
from pygame import mixer
from game import Game
import json


class Menu():
    def __init__(self, game, background, states, cursorLocation: list):
        self.game = game
        self.background = background
        self.defaultFont = pygame.font.Font('freesansbold.ttf', 32)
        self.bigDefaultFont = pygame.font.Font('freesansbold.ttf', 60)
        self.showDisplay = False
        self.stateDifference = 82

        if states:
            self.states = states
            self.state = states[0]

        if not cursorLocation:
            self.cursorLocation = [self.game.xBound/2, self.game.yBound/2]
        else:
            self.cursorLocation = cursorLocation

    def drawText(self, text, size, x, y, font):
        text = font.render(text, True, (0, 255, 0))
        self.game.screen.blit(text, (x, y))

    def createMenu(self, yDifference, font):
        self.stateDifference = yDifference
        self.startingPosX = self.game.xBound/2 - 100
        self.startingPosY = self.game.yBound/2 - 50
        for i in range(len(self.states)):
            self.drawText(
                self.states[i], 20, self.startingPosX, self.startingPosY + i * yDifference, font)

    def showMenu(self,):
        self.game.screen.blit(self.background, (0, 0))

    def drawCursor(self, offset):
        self.drawText('*', 30, self.cursorLocation[0] + offset, self.cursorLocation[1], self.defaultFont)

    def moveCursorUp(self):
        if self.shiftState(True):
            self.cursorLocation[1] = self.cursorLocation[1] - \
                self.stateDifference

    def moveCursorDown(self):
        if self.shiftState(False):
            self.cursorLocation[1] = self.cursorLocation[1] + \
                self.stateDifference

    def shiftState(self, direction: bool) -> bool:
        '''
        If direction is True Shift state upwards if it is false move downwards
        returns true if state was shifted
        '''
        if direction:
            if self.state == self.states[0]:
                return False
            for i in range(len(self.states)):
                if self.state == self.states[i]:
                    self.state = self.states[i-1]
                    return True
        else:
            if self.state == self.states[len(self.states)-1]:
                return False
            for i in range(len(self.states)):
                if self.state == self.states[i]:
                    self.state = self.states[i+1]
                    return True

    def exitGame(self):
        self.game.running, self.game.inMenu, self.showDisplay, self.game.inGame = False, False, False, False

    def exitNotMainMenu(self):
        self.showDisplay = False
        self.game.mainMenu.showDisplay = True
        self.game.currentMenu = 'Main'


class MainMenu(Menu,):
    def __init__(self, game: object, background, cursorLocation: list):
        self.states = ['New Game', 'Choose Difficulty',
                       'Highscores', 'Help', 'Quit']
        Menu.__init__(self, game, background, self.states, cursorLocation)

    def displayLoop(self):
        self.showDisplay = True
        while self.showDisplay:
            self.game.screen.fill((0, 0, 0))
            self.showMenu()
            self.drawCursor(0)
            self.game.checkEvents()

            if self.game.SKEY:
                self.moveCursorDown()
            elif self.game.WKEY:
                self.moveCursorUp()
            elif self.game.ENTERKEY:
                self.enterMenu()
            elif self.game.QUITKEY:
                self.exitGame()

            pygame.display.update()
            self.game.resetKeys()

    def enterMenu(self):
        '''
        When the enter key is pressed...
        '''
        self.game.resetKeys()
        self.showDisplay = False

        if self.state == 'New Game':
            pass
        elif self.state == 'Choose Difficulty':
            self.game.difficultyMenu.showDisplay = True
        elif self.state == 'Highscores':
            self.game.highscoresMenu.showDisplay = True
        elif self.state == 'Help':
            self.game.helpMenu.showDisplay = True
        elif self.state == 'Quit':
            self.quit()

        self.game.currentMenu = self.state

    def quit(self):
        self.game.running, self.game.inMenu, self.showDisplay, self.game.inGame = False, False, False, False


class DifficultyMenu(Menu):
    def __init__(self, game, background):
        self.states = ['Easy', 'Medium', 'Hard']
        self.game = game
        Menu.__init__(self, game, background, self.states, [self.game.xBound/2-100, self.game.yBound/2-45])
        self.font = pygame.font.Font('freesansbold.ttf', 45)
        

    def displayLoop(self):
        while self.showDisplay:
            self.game.screen.fill((0, 0, 0))
            self.showMenu()
            self.createMenu(50, self.font)
            self.drawText('Choose Difficulty:', 50, self.game.xBound/2 - 250, 200, self.bigDefaultFont)
            self.drawCursor(-20)
            self.game.checkEvents()
            if self.game.SKEY:
                self.moveCursorDown()
            elif self.game.WKEY:
                self.moveCursorUp()
            elif self.game.ENTERKEY:
                self.enterMenu()
            elif self.game.BACKKEY or self.game.ESCAPEKEY:
                self.exitNotMainMenu()
            elif self.game.QUITKEY:
                self.exitGame()
            pygame.display.update()
            self.game.resetKeys()

    def enterMenu(self):
        self.game.difficulty = self.state
        self.exitNotMainMenu()
        # TODO show user some way of which difficulty they are on


class HighscoresMenu(Menu):
    def __init__(self, game, background):
        Menu.__init__(self, game, background, None, None)
        self.yDifference = 50
        self.font = pygame.font.Font('freesansbold.ttf', 60)

    def displayLoop(self):
        while self.showDisplay:
            self.game.screen.fill((0, 0, 0))
            self.showMenu()
            self.drawText('Highscores:', 50, self.game.xBound/2 - 150, 100, self.font)
            self.showHighScores()
            self.game.checkEvents()
            if self.game.QUITKEY:
                self.exitGame()
            elif self.game.BACKKEY or self.game.ESCAPEKEY:
                self.exitNotMainMenu()

            pygame.display.update()
            self.game.resetKeys()

    def showHighScores(self):
        self.xPos = 300
        self.yPos = self.game.yBound/2 - 200
        #TODO sort the scores properly
        self.game.scores = dict(sorted(self.game.scores.items(), key=lambda item: item[1]))
        self.keys = list(self.game.scores.keys())
        self.values = list(self.game.scores.values())
        
        if len(self.keys) <= 10:
            self.displayHighScores(len(self.keys))
        else:
            self.displayHighScores(10)

    def displayHighScores(self, numHighScores:int):
        for i in range(numHighScores): 
            nameLength = len(self.keys[i])
            self.drawText(self.keys[i], 32, self.xPos,
                          self.yPos + self.yDifference * i, self.defaultFont)
            self.drawText(str(self.values[i]), 32, self.xPos + nameLength * 22,
                          self.yPos + self.yDifference * i, self.defaultFont)



class HelpMenu(Menu):
    def __init__(self, game, background):
        Menu.__init__(self, game, background, None, None)
        self.text = "Use keys A and D to Move,To shoot the gun use spacebar,You can only have 1 bullet shot at a time"
        self.font = pygame.font.Font('freesansbold.ttf', 35)
        self.state = False
        self.offset = 50

    def displayLoop(self):
        while self.showDisplay:
            self.game.screen.fill((0, 0, 0))
            self.showMenu()
            self.displayHelpText()
            self.drawText('Help Menu:', 50, self.game.xBound/2 - 200, 200, self.bigDefaultFont)
            self.game.checkEvents()
            if self.game.BACKKEY or self.game.ESCAPEKEY:
                self.exitNotMainMenu()
            elif self.game.QUITKEY:
                self.exitGame()
            pygame.display.update()
            self.game.resetKeys()

    def displayHelpText(self,):
        self.xPos = 50
        self.yPos = self.game.xBound/2 - 100
        helpText = self.font.render(self.text[:25], True, (0, 255, 0))
        self.game.screen.blit(helpText, (self.xPos, self.yPos))
        helpText = self.font.render(self.text[25:55], True, (0, 255, 0))
        self.game.screen.blit(helpText, (self.xPos, self.yPos + self.offset))
        helpText = self.font.render(self.text[55:], True, (0, 255, 0))
        self.game.screen.blit(helpText, (self.xPos, self.yPos + self.offset * 2))

class TextInput(Menu):
    def __init__(self, game, background):
        Menu.__init__(self, game, background, None, None)
        self.game = game
        self.inputs = {}
        self.name = ''
    
    def returnToMainMenu(self):
        self.game.inGame = False
        self.showDisplay = False
        self.game.mainMenu.showDisplay = True
        self.game.currentMenu = 'Main'

    def checkInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running, self.game.inMenu, self.showDisplay, self.game.inGame = False, False, False, False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    firstKey = self.name[0].upper()
                    self.name = firstKey + self.name[1:] + ':'
                    self.saveScore(self.name)
                    self.returnToMainMenu()
                keyPressed = pygame.key.name(event.key)
                self.inputs[keyPressed] = True

    def clearDictionary(self):
        self.inputs = {}
    
    def saveScore(self,name):
        self.game.scores[name] = self.game.scoreboard.score
        with open("highscores.json", 'w+') as f:
            json.dump(self.game.scores, f)

    def displayLoop(self):
        self.showDisplay = True

        while self.showDisplay:
            self.game.screen.fill((0, 0, 0))
            self.showMenu()
            self.checkInput()

            for key, item in self.inputs.items():
                if len(key) <= 1:
                    self.name += key 

            self.clearDictionary()
            self.drawText(self.name,32,self.game.xBound/2, self.game.yBound/2, self.defaultFont)
            pygame.display.update()
            self.game.resetKeys()


        


if __name__ == "__main__":
    pygame.init()
