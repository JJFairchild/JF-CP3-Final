# Jonas Fairchild, Infinite Minesweeper

# Ensures that pygame exists before trying to use it.
run = True
try:
    import pygame
except:
    print("Failed to import pygame. Type 'pip install pygame' into the terminal.")
    run = False

from Miscellaneous.file_handling import *

import time

class Main:
    """Main class"""
    def run(self):
        """Runs the game"""
        from Menus.game import Game
        from Menus.start import Start
        from Menus.leaderboard import Leaderboard
        from Menus.options import Options

        pygame.init()
        pygame.display.set_caption("Infinite Minesweeper")
        screen = pygame.display.set_mode((1200, 1200))
        mouse = pygame.mouse.get_pos()

        options = Options()
        game = Game(options.options["mine_prob"])
        start = Start()
        leaderboard = Leaderboard()

        menu = "start"

        # Helper functions and maps
        def reset_start(): return Start()
        def reset_game_default(): return Game(options.options["mine_prob"])
        def reset_leaderboard(): return Leaderboard()
        def reset_options(): return Options()

        handlers = {
            "start": lambda e: start.handleEvent(e),
            "game":  lambda e: game.handleEvent(e, mouse),
            "leaderboard": lambda e: leaderboard.handleEvent(e),
            "options": lambda e: options.handleEvent(e)
        }

        drawers = {
            "start": lambda: start.draw(screen),
            "game": lambda: game.draw(screen, mouse, new_mouse),
            "leaderboard": lambda: leaderboard.draw(screen),
            "options": lambda: options.draw(screen)
        }

        resetters = {
            "start": reset_start,
            "game": reset_game_default,
            "leaderboard": reset_leaderboard,
            "options": reset_options
        }

        # Main loop
        running = True
        while running:
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                # Calls the current menu's event handler to get the new menu
                new_menu = handlers.get(menu, lambda e: menu)(event) or menu
                    
                # Handle the special transitions that require extra parameters/actions
                if menu == "start":
                    if new_menu == "cont":
                        tiles, seed, tilecount, timer, mines, origin = readGame()
                        game = Game(options.options["mine_prob"], tiles, time.time()-timer, seed, tilecount, mines, origin)
                        game.started = True
                        new_menu = "game"
                    if new_menu == "quit":
                        running = False
                        break

                if menu == "game":
                    if new_menu == "refresh":
                        game = resetters["game"]()
                        start.gamesaved = True
                        new_menu = "start"
                    elif new_menu == "reset":
                        clearGame()
                        game = resetters["game"]()
                        start.gamesaved = False
                        new_menu = "start"

                # Only reinitialize and switch if the menu is actually changing
                if new_menu != menu:
                    # Reinitialize the target menu before switching to it
                    if new_menu in resetters:
                        if new_menu == "game":
                            if not game.started:
                                game = resetters["game"]()
                        else:
                            # Re-create menus to ensure their data is up-to-date
                            if new_menu == "start":
                                start = resetters["start"]()
                            elif new_menu == "leaderboard":
                                leaderboard = resetters["leaderboard"]()
                            elif new_menu == "options":
                                options = resetters["options"]()
                    menu = new_menu

            # Drawing
            new_mouse = pygame.mouse.get_pos()
            drawers.get(menu, lambda: None)()
            pygame.display.flip()

            mouse = pygame.mouse.get_pos()

if __name__ == "__main__" and run:
    Main().run()