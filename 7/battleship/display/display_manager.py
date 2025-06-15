"""
DisplayManager class handling all game display and output.
"""

from battleship.config import MESSAGES

class DisplayManager:
    @staticmethod
    def print_welcome_message(cpu_ships):
        """Print the welcome message."""
        print(MESSAGES['WELCOME'])
        print(MESSAGES['SHIPS_REMAINING'].format(cpu_ships))
    
    @staticmethod
    def print_board(player_board, cpu_board):
        """Print both game boards."""
        print('\n   --- OPPONENT BOARD ---          --- YOUR BOARD ---')
        
        # Print header
        header = '  ' + ' '.join(str(h) for h in range(player_board.size))
        print(f"{header}     {header}")
        
        # Print rows
        for i in range(player_board.size):
            row_str = f"{i} "
            row_str += ' '.join(cpu_board.grid[i])
            row_str += f"    {i} "
            row_str += ' '.join(player_board.grid[i])
            print(row_str)
        print('\n')
    
    @staticmethod
    def print_shot_result(hit, position, is_player_shot=True):
        """Print the result of a shot."""
        if is_player_shot:
            if hit == 'hit':
                print(MESSAGES['PLAYER_HIT'])
            elif hit == 'miss':
                print(MESSAGES['PLAYER_MISS'])
        else:
            if hit == 'hit':
                print(MESSAGES['CPU_HIT'].format(f"{position[0]}{position[1]}"))
            elif hit == 'miss':
                print(MESSAGES['CPU_MISS'].format(f"{position[0]}{position[1]}"))
    
    @staticmethod
    def print_ship_sunk(is_player_shot=True):
        """Print message when a ship is sunk."""
        if is_player_shot:
            print(MESSAGES['SHIP_SUNK'].format('You', 'an enemy'))
        else:
            print(MESSAGES['SHIP_SUNK'].format('CPU', 'your'))
    
    @staticmethod
    def print_game_over(player_won):
        """Print the game over message."""
        if player_won:
            print(MESSAGES['GAME_WON'])
        else:
            print(MESSAGES['GAME_LOST'])
    
    @staticmethod
    def print_invalid_input():
        """Print invalid input message."""
        print(MESSAGES['INVALID_INPUT'])
    
    @staticmethod
    def print_invalid_range(board_size):
        """Print invalid range message."""
        print(MESSAGES['INVALID_RANGE'].format(board_size - 1))
    
    @staticmethod
    def print_already_guessed():
        """Print already guessed message."""
        print(MESSAGES['ALREADY_GUESSED']) 