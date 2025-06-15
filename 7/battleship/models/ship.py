"""
Ship class representing a battleship in the game.
"""

class Ship:
    def __init__(self, length):
        self.length = length
        self.locations = []
        self.hits = []
        self.is_sunk = False
    
    def place(self, start_pos, orientation, board_size):
        """Place the ship on the board starting from the given position."""
        row, col = start_pos
        self.locations = []
        self.hits = []
        self.is_sunk = False
        
        for i in range(self.length):
            if orientation == 'horizontal':
                self.locations.append(f"{row}{col + i}")
            else:
                self.locations.append(f"{row + i}{col}")
            self.hits.append('')
    
    def receive_hit(self, position):
        """Record a hit on the ship and check if it's sunk."""
        if position in self.locations:
            index = self.locations.index(position)
            if self.hits[index] != 'hit':  # Only process new hits
                self.hits[index] = 'hit'
                # Check if ship is now sunk
                self.is_sunk = all(hit == 'hit' for hit in self.hits)
                return True
        return False
    
    def check_if_sunk(self):
        """Check if the ship is sunk."""
        return all(hit == 'hit' for hit in self.hits) 