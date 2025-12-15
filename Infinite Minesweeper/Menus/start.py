from Menus.menu import Menu
from Miscellaneous.button import Button
from Miscellaneous.textbox import TextBox
from Miscellaneous.file_handling import *

class Start(Menu):
    def __init__(self):
        self.savedgame = readGame()
        self.gamesaved = bool(self.savedgame)
        self.minesweeper = TextBox(200, 100, 800, 100, False, "Infinite Minesweeper", size=75)
        self.cont = Button(350, 500, 500, 80, text="Continue", size=50)
        self.newgame = Button(350, 600, 500, 80, text="New Game", size=50)
        self.leaderboard = Button(350, 700, 500, 80, text="Leaderboard", size=50)
        self.options = Button(350, 800, 500, 80, text="Options", size=50)
        self.quit = Button(350, 900, 500, 80, text="Quit", size=50)

    def handleEvent(self, event):
        if self.cont.handleEvent(event) and self.gamesaved:
            return "cont"
        if self.newgame.handleEvent(event):
            return "game"
        if self.leaderboard.handleEvent(event):
            return "leaderboard"
        if self.options.handleEvent(event):
            return "options"
        if self.quit.handleEvent(event):
            return "quit"
    
        return "start"

    def draw(self, screen):
        screen.fill((60,60,60))

        if self.gamesaved:
            self.cont.draw(screen)
        self.minesweeper.draw(screen)
        self.newgame.draw(screen)
        self.leaderboard.draw(screen)
        self.options.draw(screen)
        self.quit.draw(screen)