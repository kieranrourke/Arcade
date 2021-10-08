from Games.game import Game, Button
import pathlib
import pygame


class MainMenu(Game):
    def __init__(self):
        folder_path = str(pathlib.Path(__file__).parent.absolute()) + '/'

        Game.__init__(
            self, 
            xBound=800, 
            yBound=800, 
            caption="Arcade", 
            icon=pygame.image.load(folder_path+"icon.jpg"),
            background=pygame.image.load(folder_path+"background.jpg")
        )

        self.running = True

        self.pong_button = Button(
            game=self,
            x=300,
            y=300,
            text="Pong",
            text_size=80,
            color=(0,0,0)
        )

    def display_loop(self):
        while self.running:
            self.setMisc()
            self.checkEvents()
            self.update_display()
            if self.MOUSE_POS:
                self.check_buttons()
            self.running = False if self.QUITKEY else True

    def check_buttons(self):
        if self.pong_button.is_clicked(self.MOUSE_POS):
            print('hi')

    def update_display(self):
        self.pong_button.draw_button()
        pygame.display.update()