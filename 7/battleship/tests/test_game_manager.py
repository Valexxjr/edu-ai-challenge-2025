"""
Tests for the GameManager class.
"""

import unittest
from unittest.mock import patch, MagicMock
from battleship.game.game_manager import GameManager
from battleship.models.ship import Ship

class TestGameManager(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.game = GameManager()
    
    def test_game_initialization(self):
        """Test game initialization."""
        self.assertEqual(self.game.player.name, "Human")
        self.assertEqual(self.game.cpu.name, "CPU")
        self.assertEqual(self.game.player_ships_remaining, 0)
        self.assertEqual(self.game.cpu_ships_remaining, 0)
    
    def test_initialize_game(self):
        """Test game initialization with ships."""
        self.game.initialize_game()
        self.assertEqual(len(self.game.player.board.ships), 3)
        self.assertEqual(len(self.game.cpu.board.ships), 3)
        self.assertEqual(self.game.player_ships_remaining, 3)
        self.assertEqual(self.game.cpu_ships_remaining, 3)
    
    @patch('battleship.utils.input_handler.InputHandler.get_coordinates')
    def test_player_turn(self, mock_get_coordinates):
        """Test player's turn."""
        # Set up the game
        self.game.initialize_game()
        # Reset CPU board and ships
        self.game.cpu.board.grid = [["~" for _ in range(self.game.cpu.board.size)] for _ in range(self.game.cpu.board.size)]
        self.game.cpu.board.ships = []
        self.game.cpu.board.ships_remaining = 0
        ship = Ship(length=3)
        self.game.cpu.board.place_ship(ship, (0, 0), 'horizontal')
        
        # Test hit
        mock_get_coordinates.return_value = (0, 0)
        result = self.game.player_turn()
        self.assertEqual(result, 'hit')
        
        # Test miss
        mock_get_coordinates.return_value = (5, 5)
        result = self.game.player_turn()
        self.assertEqual(result, 'miss')
        
        # Test already guessed position
        mock_get_coordinates.return_value = (0, 0)
        result = self.game.player_turn()
        self.assertEqual(result, 'already_guessed')
    
    @patch('battleship.models.player.Player.get_next_guess')
    def test_cpu_turn(self, mock_get_next_guess):
        """Test CPU's turn."""
        # Set up the game
        self.game.initialize_game()
        # Reset player board and ships
        self.game.player.board.grid = [["~" for _ in range(self.game.player.board.size)] for _ in range(self.game.player.board.size)]
        self.game.player.board.ships = []
        self.game.player.board.ships_remaining = 0
        ship = Ship(length=3)
        self.game.player.board.place_ship(ship, (0, 0), 'horizontal')
        
        # Mock CPU guess to hit the ship
        mock_get_next_guess.return_value = (0, 0)
        # Test hit
        result = self.game.cpu_turn()
        self.assertEqual(result, 'hit')
        
        # Test miss
        mock_get_next_guess.return_value = (5, 5)
        result = self.game.cpu_turn()
        self.assertEqual(result, 'miss')
        
        # Test ship sinking
        # Hit all positions of the ship except the first one
        for i in range(1, ship.length):
            self.game.player.board.receive_shot((0, i))
        # Hit the last position (already guessed)
        mock_get_next_guess.return_value = (0, 0)
        result = self.game.cpu_turn()
        self.assertEqual(result, 'already_guessed')
        self.assertTrue(ship.check_if_sunk())
        self.assertEqual(self.game.player.board.get_ships_remaining(), 0)  # One ship sunk
    
    def test_is_game_over(self):
        """Test game over detection."""
        self.game.initialize_game()
        
        # Game should not be over initially
        self.assertFalse(self.game.is_game_over())
        
        # Sink all CPU ships
        for ship in self.game.cpu.board.ships:
            for location in ship.locations:
                row = int(location[0])
                col = int(location[1])
                self.game.cpu.board.receive_shot((row, col))
        
        # Game should be over with player win
        self.assertTrue(self.game.is_game_over())

if __name__ == '__main__':
    unittest.main() 