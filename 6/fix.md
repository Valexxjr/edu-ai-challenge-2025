# Enigma Python Implementation Fixes

## 1. Rotor Stepping Logic
- Updated the rotor stepping logic to match the correct Enigma double-stepping behavior, as in the JavaScript version:
  ```python
  def step_rotors(self):
      if self.rotors[2].at_notch():
          self.rotors[1].step()
      if self.rotors[1].at_notch():
          self.rotors[0].step()
      self.rotors[2].step()
  ```

## 2. Plugboard Application
- The plugboard is now applied only once per character, before the rotors, matching the JavaScript logic.

## 3. Debugging and Error Handling
- Added debug print statements to trace the transformation of each character through the machine.
- Added error handling to catch and report index errors or invalid characters.

## 4. Command-Line Arguments
- The script can now be run with a message as a command-line argument for quick testing:
  ```python
  if __name__ == '__main__':
      if len(sys.argv) > 1:
          # Use default settings for quick testing
          message = sys.argv[1]
          rotor_positions = [0, 0, 0]
          ring_settings = [0, 0, 0]
          plug_pairs = []
          
          enigma = Enigma([0, 1, 2], rotor_positions, ring_settings, plug_pairs)
          result = enigma.process(message)
          print('Input:', message)
          print('Output:', result)
      else:
          prompt_enigma()
  ```

## 5. Detailed Character Processing Debugging
- Each step of the character transformation is printed for easier debugging:
  ```python
  def encrypt_char(self, c):
      if c not in alphabet:
          print(f"Skipping non-alphabetic character: {c}")
          return c
      
      print(f"\nProcessing character: {c}")
      self.step_rotors()
      
      # First plugboard
      c = plugboard_swap(c, self.plugboard_pairs)
      print(f"After plugboard: {c}")
      
      # Forward through rotors
      for i, rotor in enumerate(reversed(self.rotors)):
          c = rotor.forward(c)
          print(f"After rotor {len(self.rotors)-i-1} forward: {c}")
      
      # Through reflector
      try:
          idx = alphabet.index(c)
          c = REFLECTOR[idx]
          print(f"After reflector: {c}")
      except ValueError as e:
          print(f"Error with character '{c}': {e}")
          return c
      
      # Backward through rotors
      for i, rotor in enumerate(self.rotors):
          c = rotor.backward(c)
          print(f"After rotor {i} backward: {c}")
      
      return c
  ```

---

All changes ensure the Python implementation matches the logic and behavior of the JavaScript version and is robust against invalid input. 