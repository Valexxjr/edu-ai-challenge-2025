"""
Tests for the Player class.
"""

import unittest
from unittest.mock import patch
from battleship.models.player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.human_player = Player("Human")
        self.cpu_player = Player("CPU", is_cpu=True)
    
    def test_player_initialization(self):
        """Test player initialization."""
        self.assertEqual(self.human_player.name, "Human")
        self.assertFalse(self.human_player.is_cpu)
        self.assertEqual(self.human_player.guesses, set())
        self.assertEqual(self.human_player.target_queue, [])
        self.assertTrue(self.human_player.hunt_mode)
        
        self.assertEqual(self.cpu_player.name, "CPU")
        self.assertTrue(self.cpu_player.is_cpu)
    
    def test_place_ships_randomly(self):
        """Test random ship placement."""
        self.human_player.place_ships_randomly()
        self.assertEqual(len(self.human_player.board.ships), 3)  # NUM_SHIPS = 3
        self.assertEqual(self.human_player.board.ships_remaining, 3)
    
    def test_make_guess(self):
        """Test making guesses."""
        # Test valid guess
        valid, guess = self.human_player.make_guess((0, 0))
        self.assertTrue(valid)
        self.assertEqual(guess, '00')
        self.assertIn('00', self.human_player.guesses)
        
        # Test already guessed position
        valid, guess = self.human_player.make_guess((0, 0))
        self.assertFalse(valid)
        self.assertEqual(guess, 'already_guessed')
    
    def test_cpu_target_queue(self):
        """Test CPU target queue updates."""
        # Initial state
        self.assertTrue(self.cpu_player.hunt_mode)
        self.assertEqual(self.cpu_player.target_queue, [])
        
        # After a hit
        self.cpu_player.update_target_queue((5, 5), 'hit')
        self.assertFalse(self.cpu_player.hunt_mode)
        self.assertEqual(len(self.cpu_player.target_queue), 4)  # 4 adjacent positions
        
        # After a miss with empty queue
        self.cpu_player.target_queue = []
        self.cpu_player.update_target_queue((5, 5), 'miss')
        self.assertTrue(self.cpu_player.hunt_mode)
    
    @patch('random.randint')
    def test_cpu_get_next_guess(self, mock_randint):
        """Test CPU's next guess selection."""
        # Test hunt mode
        mock_randint.side_effect = [5, 5, 6, 6, 7, 7]  # Provide multiple values as integers
        guess = self.cpu_player.get_next_guess()
        self.assertEqual(guess, (5, 5))
        guess = self.cpu_player.get_next_guess()
        self.assertEqual(guess, (6, 6))
        guess = self.cpu_player.get_next_guess()
        self.assertEqual(guess, (7, 7))
    
    def test_human_get_next_guess(self):
        """Test human player's next guess."""
        guess = self.human_player.get_next_guess()
        self.assertIsNone(guess)  # Human player doesn't use get_next_guess

if __name__ == '__main__':
    unittest.main() 