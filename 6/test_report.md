# Enigma Machine Test Report

## Test Coverage Summary

- **Overall Coverage**: 68%
- **Lines of Code**: 78
- **Covered Lines**: 53
- **Missing Lines**: 25

## Test Cases

### Core Functionality Tests

1. **Basic Encryption/Decryption** (`test_basic_encryption_decryption`)
   - Verifies that a message can be encrypted and then decrypted back to its original form
   - Tests the fundamental Enigma machine operation

2. **Plugboard Operations** (`test_plugboard_swaps`)
   - Tests the plugboard swap functionality
   - Verifies that characters are correctly swapped according to plugboard settings

3. **Rotor Positions** (`test_different_rotor_positions`)
   - Tests encryption with different rotor starting positions
   - Verifies that rotor position affects encryption

4. **Rotor Stepping** (`test_rotor_stepping`)
   - Verifies that rotors step correctly
   - Tests the mechanical operation of the Enigma machine

5. **Notch Detection** (`test_rotor_at_notch`)
   - Tests the notch detection mechanism
   - Verifies that rotors trigger stepping of adjacent rotors at correct positions

6. **Plugboard Swap Function** (`test_plugboard_swap_function`)
   - Tests individual plugboard swap operations
   - Verifies correct handling of swapped and non-swapped characters

7. **Non-alphabetic Characters** (`test_non_alphabetic_characters`)
   - Tests handling of spaces, numbers, and special characters
   - Verifies that non-alphabetic characters are preserved

8. **Rotor Forward/Backward** (`test_rotor_forward_backward`)
   - Tests the bidirectional operation of rotors
   - Verifies that characters can be encrypted and decrypted through the same rotor

9. **Reflector** (`test_reflector`)
   - Tests the reflector's symmetric property
   - Verifies that double reflection returns to the original character

10. **Ring Settings** (`test_ring_settings`)
    - Tests encryption with different ring settings
    - Verifies that ring settings affect the encryption process

## Coverage Details

### Covered Code
- All core encryption/decryption functionality
- Rotor operations (stepping, forward/backward)
- Plugboard operations
- Character processing
- Utility functions

### Missing Coverage
- Command-line interface (lines 86-101)
- Interactive prompt (lines 104-116)
- Some error handling paths (lines 59, 61)

## Test Environment
- Python 3.11
- pytest 8.0.0
- pytest-cov 4.1.0

## Running Tests
```bash
python -m pytest
```

This will run all tests and generate a coverage report showing:
- Total coverage percentage
- Number of statements covered
- Specific lines that are not covered 