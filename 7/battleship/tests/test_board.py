"""
Tests for the Board class.
"""

import unittest
from battleship.models.board import Board
from battleship.models.ship import Ship

class TestBoard(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.board = Board()
    
    def test_board_initialization(self):
        """Test board initialization."""
        self.assertEqual(len(self.board.grid), 10)
        self.assertEqual(len(self.board.grid[0]), 10)
        self.assertEqual(self.board.ships, [])
        self.assertEqual(self.board.ships_remaining, 0)
    
    def test_valid_ship_placement(self):
        """Test valid ship placement."""
        ship = Ship(length=3)
        success = self.board.place_ship(ship, (0, 0), 'horizontal')
        self.assertTrue(success)
        self.assertEqual(len(self.board.ships), 1)
        self.assertEqual(self.board.ships_remaining, 1)
    
    def test_invalid_ship_placement(self):
        """Test invalid ship placement."""
        ship = Ship(length=3)
        # Try to place ship outside board
        success = self.board.place_ship(ship, (9, 9), 'horizontal')
        self.assertFalse(success)
        self.assertEqual(len(self.board.ships), 0)
        self.assertEqual(self.board.ships_remaining, 0)
    
    def test_ship_overlap(self):
        """Test ship overlap detection."""
        ship1 = Ship(length=3)
        ship2 = Ship(length=3)
        
        # Place first ship
        self.board.place_ship(ship1, (0, 0), 'horizontal')
        
        # Try to place second ship in overlapping position
        success = self.board.place_ship(ship2, (0, 1), 'horizontal')
        self.assertFalse(success)
        self.assertEqual(len(self.board.ships), 1)
    
    def test_receive_shot(self):
        """Test receiving shots."""
        ship = Ship(length=3)
        self.board.place_ship(ship, (0, 0), 'horizontal')
        
        # Test hit
        valid, result = self.board.receive_shot((0, 0))
        self.assertTrue(valid)
        self.assertEqual(result, 'hit')
        
        # Test miss
        valid, result = self.board.receive_shot((5, 5))
        self.assertTrue(valid)
        self.assertEqual(result, 'miss')
        
        # Test already shot position
        valid, result = self.board.receive_shot((0, 0))
        self.assertFalse(valid)
    
    def test_ship_sinking(self):
        """Test ship sinking detection."""
        ship = Ship(length=3)
        self.board.place_ship(ship, (0, 0), 'horizontal')
        
        # Hit all positions of the ship
        self.board.receive_shot((0, 0))
        self.board.receive_shot((0, 1))
        self.board.receive_shot((0, 2))
        
        self.assertEqual(self.board.get_ships_remaining(), 0)
        self.assertEqual(self.board.ships_remaining, 0)
    
    def test_get_ships_remaining(self):
        """Test getting remaining ships count."""
        ship1 = Ship(length=3)
        ship2 = Ship(length=3)
        
        self.board.place_ship(ship1, (0, 0), 'horizontal')
        self.board.place_ship(ship2, (5, 5), 'horizontal')
        
        self.assertEqual(self.board.get_ships_remaining(), 2)
        
        # Sink one ship
        self.board.receive_shot((0, 0))
        self.board.receive_shot((0, 1))
        self.board.receive_shot((0, 2))
        
        self.assertEqual(self.board.get_ships_remaining(), 1)

if __name__ == '__main__':
    unittest.main() 