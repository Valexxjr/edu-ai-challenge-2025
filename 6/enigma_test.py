import unittest
from enigma import Enigma, Rotor, plugboard_swap, mod, ROTORS, REFLECTOR

class TestEnigma(unittest.TestCase):
    def setUp(self):
        self.default_rotor_ids = [0, 1, 2]
        self.default_positions = [0, 0, 0]
        self.default_ring_settings = [0, 0, 0]
        self.default_plugboard = []

    def test_basic_encryption_decryption(self):
        enigma1 = Enigma(self.default_rotor_ids, self.default_positions, 
                        self.default_ring_settings, self.default_plugboard)
        message = 'HELLO'
        encrypted = enigma1.process(message)
        enigma2 = Enigma(self.default_rotor_ids, self.default_positions, 
                        self.default_ring_settings, self.default_plugboard)
        decrypted = enigma2.process(encrypted)
        self.assertEqual(message, decrypted)

    def test_plugboard_swaps(self):
        enigma = Enigma(self.default_rotor_ids, self.default_positions, 
                       self.default_ring_settings, [['A', 'B']])
        message = 'HELLO'
        encrypted = enigma.process(message)
        self.assertNotEqual(message, encrypted)

    def test_different_rotor_positions(self):
        enigma = Enigma(self.default_rotor_ids, [1, 2, 3], 
                       self.default_ring_settings, self.default_plugboard)
        message = 'HELLO'
        encrypted = enigma.process(message)
        self.assertEqual(len(message), len(encrypted))

    def test_rotor_stepping(self):
        rotor = Rotor(ROTORS[0]['wiring'], ROTORS[0]['notch'])
        initial_pos = rotor.position
        rotor.step()
        self.assertEqual(rotor.position, mod(initial_pos + 1, 26))

    def test_rotor_at_notch(self):
        rotor = Rotor(ROTORS[0]['wiring'], ROTORS[0]['notch'], position=16)  # Q is at position 16
        self.assertTrue(rotor.at_notch())

    def test_plugboard_swap_function(self):
        pairs = [['A', 'B'], ['C', 'D']]
        self.assertEqual(plugboard_swap('A', pairs), 'B')
        self.assertEqual(plugboard_swap('B', pairs), 'A')
        self.assertEqual(plugboard_swap('C', pairs), 'D')
        self.assertEqual(plugboard_swap('D', pairs), 'C')
        self.assertEqual(plugboard_swap('E', pairs), 'E')  # No swap

    def test_non_alphabetic_characters(self):
        enigma = Enigma(self.default_rotor_ids, self.default_positions, 
                       self.default_ring_settings, self.default_plugboard)
        message = 'HELLO 123!'
        encrypted = enigma.process(message)
        self.assertEqual(len(message), len(encrypted))
        self.assertEqual(encrypted[5:], ' 123!')  # Non-alphabetic chars should be preserved

    def test_rotor_forward_backward(self):
        rotor = Rotor(ROTORS[0]['wiring'], ROTORS[0]['notch'])
        test_char = 'A'
        forward = rotor.forward(test_char)
        backward = rotor.backward(forward)
        self.assertEqual(test_char, backward)

    def test_reflector(self):
        enigma = Enigma(self.default_rotor_ids, self.default_positions, 
                       self.default_ring_settings, self.default_plugboard)
        # Test that reflector is symmetric
        for i, char in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            reflected = REFLECTOR[i]
            reflected_back = REFLECTOR[ord(reflected) - ord('A')]
            self.assertEqual(char, reflected_back)

    def test_ring_settings(self):
        enigma = Enigma(self.default_rotor_ids, self.default_positions, 
                       [1, 2, 3], self.default_plugboard)
        message = 'HELLO'
        encrypted = enigma.process(message)
        self.assertEqual(len(message), len(encrypted))

if __name__ == '__main__':
    unittest.main() 