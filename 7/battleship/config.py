"""
Game configuration and constants.
"""

# Board configuration
BOARD_SIZE = 10
NUM_SHIPS = 3
SHIP_LENGTH = 3

# Game symbols
SYMBOLS = {
    'EMPTY': '~',
    'SHIP': 'S',
    'HIT': 'X',
    'MISS': 'O'
}

# Game messages
MESSAGES = {
    'WELCOME': "\nLet's play Sea Battle!",
    'SHIPS_REMAINING': 'Try to sink the {} enemy ships.',
    'INVALID_INPUT': 'Oops, input must be exactly two digits (e.g., 00, 34, 98).',
    'INVALID_RANGE': 'Oops, please enter valid row and column numbers between 0 and {}.',
    'ALREADY_GUESSED': 'You already guessed that location!',
    'PLAYER_HIT': 'PLAYER HIT!',
    'PLAYER_MISS': 'PLAYER MISS.',
    'CPU_HIT': 'CPU HIT at {}!',
    'CPU_MISS': 'CPU MISS at {}.',
    'SHIP_SUNK': '{} sunk {} battleship!',
    'GAME_WON': '\n*** CONGRATULATIONS! You sunk all enemy battleships! ***',
    'GAME_LOST': '\n*** GAME OVER! The CPU sunk all your battleships! ***'
} 