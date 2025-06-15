"""
InputHandler class managing user input and validation.
"""

from battleship.config import BOARD_SIZE, MESSAGES

class InputHandler:
    @staticmethod
    def get_coordinates(prompt, board_size=BOARD_SIZE):
        """Get and validate coordinates from user input."""
        while True:
            try:
                guess = input(prompt)
                if not InputHandler.is_valid_format(guess):
                    print(MESSAGES['INVALID_INPUT'])
                    continue
                
                row, col = map(int, guess)
                if not InputHandler.is_valid_range(row, col, board_size):
                    print(MESSAGES['INVALID_RANGE'].format(board_size - 1))
                    continue
                
                return row, col
            except ValueError:
                print(MESSAGES['INVALID_INPUT'])
    
    @staticmethod
    def is_valid_format(guess):
        """Check if the input format is valid."""
        return len(guess) == 2 and guess.isdigit()
    
    @staticmethod
    def is_valid_range(row, col, board_size):
        """Check if the coordinates are within valid range."""
        return 0 <= row < board_size and 0 <= col < board_size 