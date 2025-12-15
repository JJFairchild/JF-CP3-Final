from Menus.menu import Menu
from Miscellaneous.file_handling import *
from Miscellaneous.button import Button
from Miscellaneous.textbox import TextBox
from Miscellaneous.helpers import difficulty

import copy

class Options(Menu):
    """Class for the leaderboard menu"""
    def __init__(self):
        """Initializes necessary values."""
        self.options = readOptions()
        self.new_options = {"mine_prob": self.options["mine_prob"]}

        self.back = Button(50, 50, 100, 50, text="Back", size=50)
        self.save = Button(1050, 50, 100, 50, text="Save", size=50)
        self.keybinds = TextBox(150,150,900,50, False, "Controls (no keybind customization): LMB = reveal, MMB = flag, RMB = drag, Scroll wheel = zoom", size=25)
        self.minetext = TextBox(50,300,200,50, False, "Mine Probability:")
        self.mineprob = TextBox(300,300,200,50, True, str(self.options["mine_prob"]), (90, 90, 90), (230, 230, 230))

        self.difficulty = TextBox(750, 300, 400, 50, False, f"Estimated difficulty: {difficulty(self.options['mine_prob'])}", (90, 90, 90), (230, 230, 230))

        self.note = TextBox(50,1050,1100,100, False, "Note: Updating options while a game is saved will delete the saved game.", (90, 90, 90), (230, 230, 230), size=40)
    
    def handleEvent(self, event):
        self.mineprob.handleEvent(event)
        if self.mineprob.text != str(self.options["mine_prob"]):
            try:
                if 0.15 <= float(self.mineprob.text) <= 1:
                    self.new_options["mine_prob"] = float(self.mineprob.text)
            except:
                pass

        if self.back.handleEvent(event):
            return "start"
        if self.save.handleEvent(event):
            self.mineprob.text = str(self.new_options["mine_prob"])
            if self.options != self.new_options:
                clearGame()
                self.options = copy.deepcopy(self.new_options)
                self.difficulty = TextBox(750, 300, 400, 50, False, f"Estimated difficulty: {difficulty(self.options['mine_prob'])}", (90, 90, 90), (230, 230, 230))
                writeOptions(self.options)
        
        return "options"

    def draw(self, screen):
        """Draws the leaderboard on the screen"""
        screen.fill((60,60,60))
        self.back.draw(screen)
        self.save.draw(screen)
        self.keybinds.draw(screen)
        self.minetext.draw(screen)
        self.mineprob.draw(screen)
        self.difficulty.draw(screen)
        self.note.draw(screen)