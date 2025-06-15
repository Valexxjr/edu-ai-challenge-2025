"""
Ship class representing a battleship in the game.
"""

class Ship:
    def __init__(self, length):
        self.length = length
        self.locations = []
        self.hits = []
    
    def place(self, start_pos, orientation, board_size):
        """Place the ship on the board starting from the given position."""
        row, col = start_pos
        self.locations = []
        self.hits = []
        
        for i in range(self.length):
            if orientation == 'horizontal':
                self.locations.append(f"{row}{col + i}")
            else:
                self.locations.append(f"{row + i}{col}")
            self.hits.append('')
    
    def is_sunk(self):
        """Check if the ship is sunk."""
        return all(hit == 'hit' for hit in self.hits)
    
    def receive_hit(self, position):
        """Record a hit on the ship."""
        if position in self.locations:
            index = self.locations.index(position)
            self.hits[index] = 'hit'
            return True
        return False 