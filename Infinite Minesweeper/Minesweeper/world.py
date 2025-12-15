import math
import time

from Minesweeper.board_manager import BoardManager
from Minesweeper.camera import Camera
from Miscellaneous.helpers import area
from Miscellaneous.textbox import TextBox

import pygame

class World:
    """Handles Infinite Minesweeper logic"""
    def __init__(self, seed, mine_prob, tiles=None, start_time = time.time(), tilecount=0, flagcount=0, origin=False):
        """Initializes necessary components for use in World methods."""
        self.mine_prob = mine_prob
        if tiles is None:
            tiles = {}
        self.tiles = tiles
        self.start_time = start_time
        self.tilecount = tilecount
        self.flagcount = flagcount
        
        self.timer = 0
        self.game_over = False
        self.needs_update = True
        self.dragging = False
        
        self.manager = BoardManager(tiles, seed, mine_prob)
        self.camera = Camera()

        if origin:
            self.manager.origin = origin

    def reveal(self, x, y):
        """Directly reveals a single tile. Also capable of calling floodRev()."""
        tile = self.manager.getTile(x,y)
        mines = self.manager.parseNeighbors(x,y)["mines"]

        if not tile.revealed:
            tile.revealed = True
            self.tilecount += 1
            if tile.mine:
                self.game_over = True
            elif mines == 0:
                self.floodRev(x,y)
        else:
            self.chordRev(x,y)

    def floodRev(self, x, y):
        """If a tile has 0 surrounding mines, reveals surrounding tiles in a recursive flood effect."""
        stack = [(x, y)]
        for i, j in area(x,y):
            stack.append((i,j))
            
        while stack: # Uses a stack rather than a for loop for efficiency
            cx, cy = stack.pop()
            tile = self.manager.getTile(cx, cy)
            if tile.revealed or tile.flagged: # Skip flags already revealed or flagged for efficiency
                continue

            tile.revealed = True
            self.tilecount += 1
            mines = self.manager.parseNeighbors(cx, cy)["mines"]
            if mines == 0:
                for i, j in area(cx, cy):
                    stack.append((i, j))

    def chordRev(self, x, y):
        """Reveals surrounding tiles of an already revealed tile whose flag quota has been met."""
        tile = self.manager.getTile(x,y)
        flags = self.manager.parseNeighbors(x,y)["flags"]
        mines = self.manager.parseNeighbors(x,y)["mines"]

        if tile.revealed and flags == mines:
            for i, j in area(x, y):
                neighbor = self.manager.getTile(i, j)
                if not neighbor.flagged and not neighbor.revealed:
                    self.reveal(i, j)

    def handleEvent(self, event):
        """Handles incoming events for the world."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.game_over:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    x,y = self.camera.stow(pos[0],pos[1])
                    if self.tiles == {}:
                        self.manager.origin = (x,y)
                    if not self.manager.getTile(x,y).flagged:
                        self.reveal(x,y)
                        self.needs_update = True

                if event.button == 2:
                    pos = pygame.mouse.get_pos()
                    x,y = self.camera.stow(pos[0],pos[1])
                    tile = self.manager.getTile(x,y)
                    if not tile.revealed:
                        if tile.flagged == False:
                            tile.flagged = True
                            self.flagcount += 1
                        else:
                            tile.flagged = False
                            self.flagcount -= 1
                        self.needs_update = True

            if event.button == 3:
                self.dragging = True

        if event.type == pygame.MOUSEWHEEL:
            self.needs_update = True
            pos = pygame.mouse.get_pos()
            self.camera.zoom(event.y, pos[0],pos[1])

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            self.dragging = False

    def draw(self, screen, mouse, new_mouse):
        """Draws the viewable world on the screen"""
        if (self.dragging and mouse != new_mouse) or self.needs_update:
            # Drag movement
            if self.dragging and mouse != new_mouse:
                self.camera.x += (mouse[0] - new_mouse[0])
                self.camera.y += (mouse[1] - new_mouse[1])

            self.needs_update = False
            screen.fill((50,50,50))
            font = pygame.font.Font(None, int(self.camera.spacing/2))

            # Display every tile on the screen
            for x in range(math.floor(1200/(self.camera.spacing))+2):
                for y in range(math.floor(1200/(self.camera.spacing))+2):
                    tx = x*self.camera.spacing - self.camera.x%self.camera.spacing
                    ty = y*self.camera.spacing - self.camera.y%self.camera.spacing
                    tile_coords = self.camera.stow(tx+self.camera.spacing/3, ty+self.camera.spacing/3)
                    tile = self.tiles.get((tile_coords[0], tile_coords[1]))

                    color = (200,200,200)
                    if tile:
                        if tile.revealed:
                            color = (150,150,150)
                            if tile.mine:
                                color = (0,0,0)
                        elif tile.flagged:
                            color = (255, 0, 0)
                    # Create the tile
                    pygame.draw.rect(
                        screen, color, 
                        (tx, ty, self.camera.tile_size, self.camera.tile_size)
                    )

                    # Create the number indicator
                    if tile:
                        mines = self.manager.parseNeighbors(tile_coords[0], tile_coords[1])["mines"]
                        if mines and tile.revealed and not tile.mine:
                            text_surface = font.render(str(mines), True, (0,0,0))
                            tx += (self.camera.tile_size - text_surface.get_width()) // 2
                            ty += (self.camera.tile_size - text_surface.get_height()) // 2
                            screen.blit(text_surface, (tx, ty))

        # Display overlays
        if not self.game_over:
            self.timer = round(time.time()-self.start_time, 1)
        TextBox(75, 25, 300, 75, False, str(self.tilecount), (75,75,75), (200,200,200), size=50).draw(screen)
        TextBox(450, 25, 300, 75, False, str(self.timer), (75,75,75), (200,200,200), size=50).draw(screen)
        TextBox(825, 25, 300, 75, False, str(self.flagcount), (75,75,75), (200,200,200), size=50).draw(screen)
