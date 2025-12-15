class Tile:
    """Creates a base tile class for use in World methods."""
    def __init__(self, x, y, mine, revealed = False, flagged = False):
        """Initializes default tile variables."""
        self.x = x
        self.y = y
        self.mine = mine
        self.revealed = revealed
        self.flagged = flagged