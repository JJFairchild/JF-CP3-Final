import random
import time

from Menus.menu import Menu
from Minesweeper.world import World
from Miscellaneous.button import Button
from Miscellaneous.textbox import TextBox
from Miscellaneous.file_handling import *

import pygame

class Game(Menu):
    """Handles switching between the start game screen and the world"""
    def __init__(self, mine_prob, tiles=None, start_time=time.time(), seed="", tilecount=0, mines=0, origin=False):
        """Initializes necessary values and objects"""
        self.started = False
        if tiles is None:
            tiles = {}

        self.world = World(seed, mine_prob, tiles, start_time, tilecount, mines, origin)
        self.seedbox = TextBox(300, 450, 600, 60, mutable=True, limit=25)
        self.keybinds = TextBox(100,1100,1000,75, False, "Controls: LMB = reveal, MMB = flag, RMB = drag, Scroll wheel = zoom", (90, 90, 90), (230, 230, 230), size=42)
        self.game_over = TextBox(25, 1105, 500, 75, False, "Enter username to save score:", (75,75,75), (200,200,200), size=40)
        self.userbox = TextBox(550, 1105, 300, 75, True, color=(75,75,75), text_color=(200,200,200), limit=14)
        self.button = Button(350, 570, 500, 80, text="Generate seed for me", size=50)
        self.quit = Button(900, 1105, 280, 75, (75,75,75), "Save and exit", (200,200,200), 50)
        self.back = Button(50, 50, 100, 50, text="Back", size=50)

    def handleEvent(self, event, mouse):
        """Handles incoming events and forks them to either the world or menu depending on which is being used"""
        if self.started:
            if not self.quit.collidepoint(mouse):
                self.world.handleEvent(event)

            if self.world.game_over:
                self.userbox.handleEvent(event)

                if self.quit.text != "Return":
                    self.quit.text = "Return"
                
                if self.quit.handleEvent(event):
                    if self.userbox.text != "":
                        writeLeaderboard(self.userbox.text, self.world.tilecount, self.world.timer, self.world.flagcount, self.world.mine_prob)
                    return "reset"

            else:
                if self.quit.handleEvent(event):
                    writeGame(self.world.tiles, self.world.manager.seed, self.world.tilecount, self.world.timer, self.world.flagcount, self.world.manager.origin)
                    return "refresh"

        else:
            self.seedbox.handleEvent(event)

            if self.button.handleEvent(event):
                if self.button.text == "Generate seed for me":
                    seed = str(random.randint(-1000000, 1000000))
                else:
                    seed = self.seedbox.text
                self.world.manager.seed = seed
                self.started = True
                self.world.start_time = time.time()
            
            if self.back.handleEvent(event):
                return "start"

        return "game"

    def draw(self, screen, mouse, new_mouse):
        """Draws either the world or the start menu on the screen depending on which is being used."""
        if self.started:
            self.world.draw(screen, mouse, new_mouse)

            if self.world.game_over:
                if self.userbox.text != "" and self.quit.text == "Return":
                    self.quit.text = "Save"
                elif self.userbox.text == "" and self.quit.text == "Save":
                    self.quit.text = "Return"
                self.game_over.draw(screen)
                self.userbox.draw(screen)

            self.quit.draw(screen)

        else:
            if self.seedbox.text == "" and self.button.text != "Generate seed for me":
                self.button = Button(350, 570, 500, 80, text="Generate seed for me", size=50)

            elif self.seedbox.text != "" and self.button.text != "Start":
                self.button = Button(350, 570, 500, 80, text="Start", size=50)

            screen.fill((60,60,60))
            self.button.draw(screen)
            self.back.draw(screen)
            self.keybinds.draw(screen)
            self.seedbox.draw(screen)