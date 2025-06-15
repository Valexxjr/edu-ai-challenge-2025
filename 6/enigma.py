import sys

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def mod(n, m):
    return ((n % m) + m) % m

ROTORS = [
    {'wiring': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'notch': 'Q'},  # Rotor I
    {'wiring': 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'notch': 'E'},  # Rotor II
    {'wiring': 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'notch': 'V'},  # Rotor III
]
REFLECTOR = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'

def plugboard_swap(c, pairs):
    for a, b in pairs:
        if c == a:
            return b
        if c == b:
            return a
    return c

class Rotor:
    def __init__(self, wiring, notch, ring_setting=0, position=0):
        self.wiring = wiring
        self.notch = notch
        self.ring_setting = ring_setting
        self.position = position

    def step(self):
        self.position = mod(self.position + 1, 26)

    def at_notch(self):
        return alphabet[self.position] == self.notch

    def forward(self, c):
        idx = mod(alphabet.index(c) + self.position - self.ring_setting, 26)
        return self.wiring[idx]

    def backward(self, c):
        idx = self.wiring.index(c)
        return alphabet[mod(idx - self.position + self.ring_setting, 26)]

class Enigma:
    def __init__(self, rotor_ids, rotor_positions, ring_settings, plugboard_pairs):
        self.rotors = [
            Rotor(
                ROTORS[id]['wiring'],
                ROTORS[id]['notch'],
                ring_settings[i],
                rotor_positions[i]
            )
            for i, id in enumerate(rotor_ids)
        ]
        self.plugboard_pairs = plugboard_pairs

    def step_rotors(self):
        if self.rotors[1].at_notch():
            self.rotors[0].step()
            self.rotors[1].step()
        elif self.rotors[2].at_notch():
            self.rotors[1].step()
        self.rotors[2].step()

    def encrypt_char(self, c):
        if c not in alphabet:
            return c
        
        self.step_rotors()
        
        # First plugboard
        c = plugboard_swap(c, self.plugboard_pairs)
        
        # Forward through rotors
        for rotor in reversed(self.rotors):
            c = rotor.forward(c)
        
        # Through reflector
        c = REFLECTOR[alphabet.index(c)]
        
        # Backward through rotors
        for rotor in self.rotors:
            c = rotor.backward(c)
        
        # Second plugboard
        c = plugboard_swap(c, self.plugboard_pairs)
        
        return c

    def process(self, text):
        return ''.join(self.encrypt_char(c) for c in text.upper())

def prompt_enigma():
    message = input('Enter message: ')
    pos_str = input('Rotor positions (e.g. 0 0 0): ')
    rotor_positions = [int(x) for x in pos_str.split()]
    
    ring_str = input('Ring settings (e.g. 0 0 0): ')
    ring_settings = [int(x) for x in ring_str.split()]
    
    plug_str = input('Plugboard pairs (e.g. AB CD): ')
    plug_pairs = []
    if plug_str:
        pairs = plug_str.upper().split()
        plug_pairs = [[pair[0], pair[1]] for pair in pairs]

    enigma = Enigma([0, 1, 2], rotor_positions, ring_settings, plug_pairs)
    result = enigma.process(message)
    print('Output:', result)

def run_tests():
    print('Running Enigma tests...')
    
    # Test 1: Basic encryption/decryption
    enigma1 = Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], [])
    message1 = 'HELLO'
    encrypted1 = enigma1.process(message1)
    enigma2 = Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], [])
    decrypted1 = enigma2.process(encrypted1)
    print('Test 1:', 'PASS' if message1 == decrypted1 else 'FAIL')
    
    # Test 2: With plugboard
    enigma3 = Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], [['A', 'B']])
    message2 = 'HELLO'
    encrypted2 = enigma3.process(message2)
    enigma4 = Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], [['A', 'B']])
    decrypted2 = enigma4.process(encrypted2)
    print('Test 2:', 'PASS' if message2 == decrypted2 else 'FAIL')
    
    # Test 3: Different rotor positions
    enigma5 = Enigma([0, 1, 2], [1, 2, 3], [0, 0, 0], [])
    message3 = 'HELLO'
    encrypted3 = enigma5.process(message3)
    enigma6 = Enigma([0, 1, 2], [1, 2, 3], [0, 0, 0], [])
    decrypted3 = enigma6.process(encrypted3)
    print('Test 3:', 'PASS' if message3 == decrypted3 else 'FAIL')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        run_tests()
    else:
        prompt_enigma() 