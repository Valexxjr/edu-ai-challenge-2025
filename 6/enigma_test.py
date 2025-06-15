import unittest
import coverage
from enigma import Enigma, Rotor, plugboard_swap, mod

# Start coverage measurement
cov = coverage.Coverage()
cov.start()

class TestEnigma(unittest.TestCase):
    def test_basic_encryption_decryption(self):
        enigma1 = Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], [])
        message = 'HELLO'
        encrypted = enigma1.process(message)
        enigma2 = Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], [])
        decrypted = enigma2.process(encrypted)
        self.assertEqual(message, decrypted)

    def test_plugboard_swaps(self):
        enigma = Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], [['A', 'B']])
        message = 'HELLO'
        encrypted = enigma.process(message)
        self.assertNotEqual(message, encrypted)

    def test_different_rotor_positions(self):
        enigma = Enigma([0, 1, 2], [1, 2, 3], [0, 0, 0], [])
        message = 'HELLO'
        encrypted = enigma.process(message)
        self.assertEqual(len(message), len(encrypted))

    def test_rotor_stepping(self):
        rotor = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q')
        initial_pos = rotor.position
        rotor.step()
        self.assertEqual(rotor.position, mod(initial_pos + 1, 26))

    def test_rotor_at_notch(self):
        rotor = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q', position=16)  # Q is at position 16
        self.assertTrue(rotor.at_notch())

    def test_plugboard_swap_function(self):
        pairs = [['A', 'B'], ['C', 'D']]
        self.assertEqual(plugboard_swap('A', pairs), 'B')
        self.assertEqual(plugboard_swap('B', pairs), 'A')
        self.assertEqual(plugboard_swap('C', pairs), 'D')
        self.assertEqual(plugboard_swap('D', pairs), 'C')
        self.assertEqual(plugboard_swap('E', pairs), 'E')  # No swap

    def test_non_alphabetic_characters(self):
        enigma = Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], [])
        message = 'HELLO 123!'
        encrypted = enigma.process(message)
        self.assertEqual(len(message), len(encrypted))
        self.assertEqual(encrypted[5:], ' 123!')  # Non-alphabetic chars should be preserved

if __name__ == '__main__':
    unittest.main()
    
    # Stop coverage measurement and generate report
    cov.stop()
    cov.save()
    print('\nCoverage Report:')
    cov.report() 