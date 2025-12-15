from Menus.menu import Menu
from Miscellaneous.file_handling import *
from Miscellaneous.button import Button
from Miscellaneous.textbox import TextBox
from Miscellaneous.helpers import difficulty
import pygame

class Leaderboard(Menu):
    """Class for the leaderboard menu"""
    def __init__(self):
        self.leaderboard = readLeaderboard()
        self.scroll = 0

        self.back = Button(50, 50, 100, 50, text="Back", size=50)

        self.headers = ["User", "Tiles", "Time", "Mines", "Difficulty"]

    def handleEvent(self, event):
        if self.back.handleEvent(event):
            return "start"

        # Mouse wheel scrolling
        if event.type == pygame.MOUSEWHEEL:
            self.scroll -= event.y * 40
            self.scroll = max(0, self.scroll)

        return "leaderboard"

    def draw(self, screen):
        screen.fill((60, 60, 60))
        self.back.rect.y = 50 - self.scroll
        self.back.draw(screen)

        col_w = [360, 180, 180, 180, 230]

        # Headers
        x = 15
        for i, header in enumerate(self.headers):
            TextBox(
                x, 160 - self.scroll,
                col_w[i], 45,
                False, header,
                size=36
            ).draw(screen)
            x += col_w[i] + 10

        # Entries
        y = 213 - self.scroll

        for entry in self.leaderboard:
            x = 15

            values = [
                entry.user,
                entry.tiles,
                f"{entry.time:.1f}",
                entry.mines,
                difficulty(entry.difficulty)
            ]

            for i, value in enumerate(values):
                TextBox(
                    x, y,
                    col_w[i], 45,
                    False, str(value),
                    (90, 90, 90), (230, 230, 230), size=30
                ).draw(screen)
                x += col_w[i] + 10

            y += 53