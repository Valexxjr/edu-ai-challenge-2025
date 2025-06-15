import unittest
from enigma import Enigma

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

if __name__ == '__main__':
    unittest.main() 