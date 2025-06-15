"""
Tests for the Ship class.
"""

import unittest
from battleship.models.ship import Ship

class TestShip(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.ship = Ship(length=3)
    
    def test_ship_initialization(self):
        """Test ship initialization."""
        self.assertEqual(self.ship.length, 3)
        self.assertEqual(self.ship.locations, [])
        self.assertEqual(self.ship.hits, [])
        self.assertFalse(self.ship.is_sunk)
    
    def test_ship_placement(self):
        """Test ship placement."""
        self.ship.place((0, 0), 'horizontal', 10)
        expected_locations = ['00', '01', '02']
        self.assertEqual(self.ship.locations, expected_locations)
        self.assertEqual(len(self.ship.hits), 3)
        self.assertFalse(self.ship.is_sunk)
    
    def test_ship_vertical_placement(self):
        """Test vertical ship placement."""
        self.ship.place((0, 0), 'vertical', 10)
        expected_locations = ['00', '10', '20']
        self.assertEqual(self.ship.locations, expected_locations)
    
    def test_ship_receive_hit(self):
        """Test ship receiving hits."""
        self.ship.place((0, 0), 'horizontal', 10)
        
        # Test valid hit
        self.assertTrue(self.ship.receive_hit('00'))
        self.assertEqual(self.ship.hits[0], 'hit')
        
        # Test invalid hit
        self.assertFalse(self.ship.receive_hit('99'))
        
        # Test already hit position
        self.assertFalse(self.ship.receive_hit('00'))
    
    def test_ship_sinking(self):
        """Test ship sinking detection."""
        self.ship.place((0, 0), 'horizontal', 10)
        
        # Hit all positions
        self.ship.receive_hit('00')
        self.ship.receive_hit('01')
        self.ship.receive_hit('02')
        
        self.assertTrue(self.ship.check_if_sunk())
        self.assertTrue(self.ship.is_sunk)
    
    def test_ship_not_sunk(self):
        """Test ship not sunk when not all positions are hit."""
        self.ship.place((0, 0), 'horizontal', 10)
        
        # Hit only two positions
        self.ship.receive_hit('00')
        self.ship.receive_hit('01')
        
        self.assertFalse(self.ship.check_if_sunk())
        self.assertFalse(self.ship.is_sunk)

if __name__ == '__main__':
    unittest.main() 