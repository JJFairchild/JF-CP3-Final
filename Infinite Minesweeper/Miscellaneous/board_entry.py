import math

class Entry:
    """Represents an individual entry on the leaderboard."""
    def __init__(self, user, tiles, time, mines, difficulty):
        """Initializes values and calculates overall score."""
        self.user = user
        self.tiles = tiles
        self.time = time
        self.mines = mines
        self.difficulty = difficulty
        self.score = (tiles-9) * ((1 / (1-min(difficulty,0.9999))) ** 1.5)