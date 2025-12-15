import math

class Camera:
    """Calculates where the screen should be displayed from coordinates in the minesweeper game"""
    def __init__(self):
        """Initializes values that the camera uses for coordinate calculation"""
        self.x = -656.25
        self.y = -656.25
        self.tile_size = 100
        self.spacing = self.tile_size*9/8

    def stow(self, x,y):
        """Converts screen coordinates to coordinates on the tile grid"""
        pos = ((x+self.x)/self.spacing, (y+self.y)/self.spacing)
        return math.floor(pos[0]), math.floor(pos[1])

    def pan(self, mouse, new_mouse):
        """Moves the offset according to difference in mouse position"""
        self.x += (mouse[0] - new_mouse[0])
        self.y += (mouse[1] - new_mouse[1])

    def zoom(self, scroll, x,y):
        """Changes the size of the viewable grid, while keeping the coordinates of the mouse the same."""
        # Save current tile sizes for use later
        old_tile_size = self.tile_size
        old_spacing = old_tile_size * 9/8

        # Apply zoom
        if scroll > 0 and self.tile_size < 300:
            self.tile_size *= 9/8
        elif scroll < 0 and self.tile_size > 20:
            self.tile_size /= 9/8

        self.spacing = self.tile_size * 9/8

        # Compute new offset so the tile hovered over stays the same
        self.x = (self.x + x) / old_spacing * self.spacing - x
        self.y = (self.y + y) / old_spacing * self.spacing - y