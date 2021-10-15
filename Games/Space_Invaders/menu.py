import pygame
import pathlib
import json

class Menu():
    """General Menu Class for the menus
    """

    def __init__(self, game, space_invaders, background, states: list, cursorLocation: list):
        self.game = game
        self.space_invaders = space_invaders
        self.background = background
        self.defaultFont = pygame.font.Font('freesansbold.ttf', 32)
        self.bigDefaultFont = pygame.font.Font('freesansbold.ttf', 60)
        self.showDisplay = False
        self.folder_path = str(pathlib.Path(__file__).parent.absolute()) + '/Utils/'

        # Variable that will allow the program to know how to move the cursor
        self.stateDifference = 82

        # States are used for menus that need user selection so the program knows what their cursor is on
        if states:
            self.states = states
            self.state = states[0]

         # Base cursor location normally will be passed in if needed format is [x,y]
        if not cursorLocation:
            self.cursorLocation = [self.game.xBound/2, self.game.yBound/2]
        else:
            self.cursorLocation = cursorLocation

    def drawText(self, text: str, x: int, y: int, font):
        """Used to draw text on the screen

        Args:
            text (str): The text to be displayed
            x (int): x coordinate
            y (int): y coordinate
            font ([fontType]): font used to display the text
        """
        text = font.render(text, True, (0, 255, 0))
        self.game.screen.blit(text, (x, y))

    def createMenu(self, yDifference: int, font):
        """Function used when wanting to create a menu where the user can navigate
        for example the main menu of space invaders

        Args:
            yDifference (int): the difference in y values between the menu options
            font (fontType): font used to display the menu
        """
        self.stateDifference = yDifference
        self.startingPosX = self.game.xBound/2 - 100
        self.startingPosY = self.game.yBound/2 - 50
        for i in range(len(self.states)):
            self.drawText(
                self.states[i], self.startingPosX, self.startingPosY + i * yDifference, font)

    def showMenu(self,):
        """Dispalys the background of menu
        """
        self.game.screen.blit(self.background, (0, 0))

    def drawCursor(self, offset: int):
        """Draws the cursor as a * on the screen

        Args:
            offset (int): Offset the X position of the cursor so it is not ontop of the state
        """
        self.drawText(
            '*', self.cursorLocation[0] + offset, self.cursorLocation[1], self.defaultFont)

    def moveCursorUp(self):
        """Moves the cursor up and updates the cursor location
        """
        if self.shiftState(True):
            self.cursorLocation[1] = self.cursorLocation[1] - \
                self.stateDifference

    def moveCursorDown(self):
        """Moves the cursor down and updates the cursor location
        """
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
        self.space_invaders.mainMenu.showDisplay = True
        self.space_invaders.currentMenu = 'Main'


class MainMenu(Menu,):
    def __init__(self, game: object, space_invaders, background, cursorLocation: list):
        self.states = ['New Game', 'Choose Difficulty',
                       'Highscores', 'Help', 'Quit']
        Menu.__init__(self, game, space_invaders, background, self.states, cursorLocation)

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
            self.space_invaders.difficultyMenu.showDisplay = True
        elif self.state == 'Highscores':
            self.space_invaders.highscoresMenu.showDisplay = True
        elif self.state == 'Help':
            self.space_invaders.helpMenu.showDisplay = True
        elif self.state == 'Quit':
            self.quit()

        self.space_invaders.currentMenu = self.state

    def quit(self):
        pygame.mixer.music.stop()
        self.game.running, self.game.inMenu, self.showDisplay, self.game.inGame = False, False, False, False


class DifficultyMenu(Menu):
    def __init__(self, game, space_invaders, background):
        self.states = ['Easy', 'Medium', 'Hard']
        self.game = game
        Menu.__init__(self, game, space_invaders, background, self.states, [
                      self.game.xBound/2-100, self.game.yBound/2-45])
        self.font = pygame.font.Font('freesansbold.ttf', 45)

    def displayLoop(self):
        while self.showDisplay:
            self.game.screen.fill((0, 0, 0))
            self.showMenu()
            self.createMenu(50, self.font)
            self.drawText('Choose Difficulty:', self.game.xBound /
                          2 - 250, 200, self.bigDefaultFont)
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
        self.space_invaders.difficulty = self.state
        self.exitNotMainMenu()


class HighscoresMenu(Menu):
    def __init__(self, game, space_invaders, background):
        Menu.__init__(self, game, space_invaders, background, None, None)
        self.yDifference = 50
        self.font = pygame.font.Font('freesansbold.ttf', 60)

    def displayLoop(self):
        while self.showDisplay:
            self.game.screen.fill((0, 0, 0))
            self.showMenu()
            self.drawText('Highscores:', self.game.xBound /
                          2 - 150, 100, self.font)
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
        self.game.scores = dict(
            sorted(self.space_invaders.scores.items(), key=lambda item: item[1], reverse=True))
        self.keys = list(self.game.scores.keys())
        self.values = list(self.game.scores.values())

        if len(self.keys) <= 10:
            self.displayHighScores(len(self.keys))
        else:
            self.displayHighScores(10)

    def displayHighScores(self, numHighScores: int):
        for i in range(numHighScores):
            nameLength = len(self.keys[i])
            self.drawText(self.keys[i], self.xPos,
                          self.yPos + self.yDifference * i, self.defaultFont)
            self.drawText(str(self.values[i]), self.xPos + nameLength * 22,
                          self.yPos + self.yDifference * i, self.defaultFont)


class HelpMenu(Menu):
    def __init__(self, game, space_invaders, background):
        Menu.__init__(self, game, space_invaders, background, None, None)
        self.text = "Use keys A and D to Move,To shoot the gun use spacebar,You can only have 1 bullet shot at a time"
        self.font = pygame.font.Font('freesansbold.ttf', 35)
        self.state = False
        self.offset = 50

    def displayLoop(self):
        while self.showDisplay:
            self.game.screen.fill((0, 0, 0))
            self.showMenu()
            self.displayHelpText()
            self.drawText('Help Menu:', self.game.xBound /
                          2 - 200, 200, self.bigDefaultFont)
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
        # So many different help texts in order to display across multiple lines
        helpText = self.font.render(self.text[:25], True, (0, 255, 0))
        self.game.screen.blit(helpText, (self.xPos, self.yPos))
        helpText = self.font.render(self.text[25:55], True, (0, 255, 0))
        self.game.screen.blit(helpText, (self.xPos, self.yPos + self.offset))
        helpText = self.font.render(self.text[55:], True, (0, 255, 0))
        self.game.screen.blit(
            helpText, (self.xPos, self.yPos + self.offset * 2))


class TextInput(Menu):
    def __init__(self, game, space_invaders, background):
        Menu.__init__(self, game, space_invaders, background, None, None)
        self.game = game
        self.inputs = {}
        self.name = ''
        self.inputFont = pygame.font.Font('freesansbold.ttf', 40)

    def returnToMainMenu(self):
        self.game.inGame = False
        self.showDisplay = False
        self.space_invaders.mainMenu.showDisplay = True
        self.space_invaders.currentMenu = 'Main'

    def checkInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running, self.game.inMenu, self.showDisplay, self.game.inGame = False, False, False, False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        self.name = self.name[0].upper() + self.name[1:]+':'
                        self.saveScore()
                        self.returnToMainMenu()
                    except IndexError:
                        self.returnToMainMenu()
                        pass  # Raises on empty name
                # Converts pygame_event to the actualy key name pressed
                keyPressed = pygame.key.name(event.key)
                self.inputs[keyPressed] = True

    def clearDictionary(self):
        self.inputs = {}

    def saveScore(self,):
        """Saves the score of the player
        """
        # Only saves score if it is higher than their previous score
        if self.space_invaders.scores.get(self.name):
            if self.space_invaders.scores[self.name] < self.space_invaders.scoreboard.score:
                self.space_invaders.scores[self.name] = self.space_invaders.scoreboard.score
                with open(self.folder_path+"highscores.json", 'w+') as f:
                    json.dump(self.space_invaders.scores, f)
        else:
            self.space_invaders.scores[self.name] = self.space_invaders.scoreboard.score
            with open(self.folder_path+"highscores.json", "w+") as f:
                json.dump(self.space_invaders.scores, f)

    def displayLoop(self):
        self.name = ''
        self.showDisplay = True

        while self.showDisplay:
            self.game.screen.fill((0, 0, 0))
            self.showMenu()
            self.drawText('Enter Name:', self.game.xBound /
                          2 - 200, 200, self.bigDefaultFont)
            self.checkInput()

            for key, item in self.inputs.items():
                if len(key) <= 1:
                    self.name += key
                elif key == 'backspace':
                    self.name = self.name[0:len(self.name)-1]

            self.clearDictionary()
            self.drawText(self.name, 300, 300, self.inputFont)
            pygame.display.update()
            self.game.resetKeys()
