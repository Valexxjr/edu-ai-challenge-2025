"""
Player class managing player state and actions.
"""

from battleship.models.board import Board
from battleship.models.ship import Ship
from battleship.config import NUM_SHIPS, SHIP_LENGTH

class Player:
    def __init__(self, name, is_cpu=False):
        self.name = name
        self.is_cpu = is_cpu
        self.board = Board()
        self.guesses = set()
        self.target_queue = []
        self.hunt_mode = True
    
    def place_ships_randomly(self):
        """Place ships randomly on the board."""
        import random
        
        ships_placed = 0
        while ships_placed < NUM_SHIPS:
            orientation = 'horizontal' if random.random() < 0.5 else 'vertical'
            
            if orientation == 'horizontal':
                start_row = random.randint(0, self.board.size - 1)
                start_col = random.randint(0, self.board.size - SHIP_LENGTH)
            else:
                start_row = random.randint(0, self.board.size - SHIP_LENGTH)
                start_col = random.randint(0, self.board.size - 1)
            
            ship = Ship(SHIP_LENGTH)
            if self.board.place_ship(ship, (start_row, start_col), orientation):
                ships_placed += 1
    
    def make_guess(self, position):
        """Make a guess at the given position."""
        row, col = position
        guess_str = f"{row}{col}"
        
        if guess_str in self.guesses:
            return False, 'already_guessed'
        
        self.guesses.add(guess_str)
        return True, guess_str
    
    def update_target_queue(self, position, result):
        """Update the target queue based on the last shot result."""
        if not self.is_cpu:
            return
        
        if result == 'hit':
            self.hunt_mode = False
            row, col = position
            adjacent = [
                (row - 1, col), (row + 1, col),
                (row, col - 1), (row, col + 1)
            ]
            
            for adj_pos in adjacent:
                adj_row, adj_col = adj_pos
                if (0 <= adj_row < self.board.size and 
                    0 <= adj_col < self.board.size and 
                    f"{adj_row}{adj_col}" not in self.guesses):
                    self.target_queue.append((adj_row, adj_col))
        elif not self.target_queue:
            self.hunt_mode = True
    
    def get_next_guess(self):
        """Get the next guess position for CPU player."""
        if not self.is_cpu:
            return None
        
        import random
        
        if not self.hunt_mode and self.target_queue:
            return self.target_queue.pop(0)
        
        while True:
            row = random.randint(0, self.board.size - 1)
            col = random.randint(0, self.board.size - 1)
            if f"{row}{col}" not in self.guesses:
                return (row, col) 