"""
GameManager class managing the game flow and logic.
"""

from battleship.models.player import Player
from battleship.display.display_manager import DisplayManager
from battleship.utils.input_handler import InputHandler

class GameManager:
    def __init__(self):
        self.player = Player("Human")
        self.cpu = Player("CPU", is_cpu=True)
        self.display = DisplayManager()
        self.input_handler = InputHandler()
        # Track previous ship counts
        self.player_ships_remaining = 0
        self.cpu_ships_remaining = 0
    
    def initialize_game(self):
        """Initialize the game by placing ships."""
        self.player.place_ships_randomly()
        self.cpu.place_ships_randomly()
        self.player_ships_remaining = self.player.board.get_ships_remaining()
        self.cpu_ships_remaining = self.cpu.board.get_ships_remaining()
        self.display.print_welcome_message(self.cpu_ships_remaining)
    
    def player_turn(self):
        """Handle player's turn."""
        while True:
            position = self.input_handler.get_coordinates('Enter your guess (e.g., 00): ')
            valid, guess = self.player.make_guess(position)
            
            if not valid:
                self.display.print_already_guessed()
                continue
            
            valid_shot, result = self.cpu.board.receive_shot(position)
            if not valid_shot:
                continue
            
            self.display.print_shot_result(result, position)
            
            # Check if a ship was sunk
            if result == 'hit':
                current_ships = self.cpu.board.get_ships_remaining()
                if current_ships < self.cpu_ships_remaining:
                    self.display.print_ship_sunk()
                    self.cpu_ships_remaining = current_ships
            
            return result
    
    def cpu_turn(self):
        """Handle CPU's turn."""
        position = self.cpu.get_next_guess()
        valid, guess = self.cpu.make_guess(position)
        
        valid_shot, result = self.player.board.receive_shot(position)
        self.display.print_shot_result(result, position, is_player_shot=False)
        
        # Check if a ship was sunk
        if result == 'hit':
            current_ships = self.player.board.get_ships_remaining()
            if current_ships < self.player_ships_remaining:
                self.display.print_ship_sunk(is_player_shot=False)
                self.player_ships_remaining = current_ships
        
        self.cpu.update_target_queue(position, result)
        return result
    
    def is_game_over(self):
        """Check if the game is over."""
        if self.cpu.board.get_ships_remaining() == 0:
            self.display.print_game_over(player_won=True)
            return True
        if self.player.board.get_ships_remaining() == 0:
            self.display.print_game_over(player_won=False)
            return True
        return False
    
    def play(self):
        """Main game loop."""
        self.initialize_game()
        
        while True:
            self.display.print_board(self.player.board, self.cpu.board)
            
            # Player's turn
            self.player_turn()
            if self.is_game_over():
                break
            
            # CPU's turn
            self.cpu_turn()
            if self.is_game_over():
                break
        
        self.display.print_board(self.player.board, self.cpu.board) 