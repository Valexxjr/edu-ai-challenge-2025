"""
Board class managing the game board state.
"""

from battleship.config import BOARD_SIZE, SYMBOLS

class Board:
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.grid = [[SYMBOLS['EMPTY'] for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.ships_remaining = 0
    
    def place_ship(self, ship, start_pos, orientation):
        """Place a ship on the board."""
        row, col = start_pos
        
        # Check if placement is valid
        if not self._is_valid_placement(ship, start_pos, orientation):
            return False
        
        # Place the ship
        ship.place(start_pos, orientation, self.size)
        self.ships.append(ship)
        self.ships_remaining += 1
        
        # Update grid
        for i in range(ship.length):
            if orientation == 'horizontal':
                self.grid[row][col + i] = SYMBOLS['SHIP']
            else:
                self.grid[row + i][col] = SYMBOLS['SHIP']
        
        return True
    
    def receive_shot(self, position):
        """Process a shot at the given position."""
        row, col = position
        if self.grid[row][col] in [SYMBOLS['HIT'], SYMBOLS['MISS']]:
            return False, 'already_shot'
        
        # Check if any ship is hit
        for ship in self.ships:
            if ship.receive_hit(f"{row}{col}"):
                self.grid[row][col] = SYMBOLS['HIT']
                # Check if this hit sunk the ship
                if ship.check_if_sunk():
                    self.ships_remaining -= 1
                return True, 'hit'
        
        self.grid[row][col] = SYMBOLS['MISS']
        return True, 'miss'
    
    def _is_valid_placement(self, ship, start_pos, orientation):
        """Check if ship placement is valid."""
        row, col = start_pos
        
        # Check board boundaries
        if orientation == 'horizontal':
            if col + ship.length > self.size:
                return False
        else:
            if row + ship.length > self.size:
                return False
        
        # Check for collisions
        for i in range(ship.length):
            if orientation == 'horizontal':
                if self.grid[row][col + i] != SYMBOLS['EMPTY']:
                    return False
            else:
                if self.grid[row + i][col] != SYMBOLS['EMPTY']:
                    return False
        
        return True
    
    def get_ships_remaining(self):
        """Get the number of ships that haven't been sunk."""
        return self.ships_remaining 