# Enigma Machine Python Implementation

## Overview

This project implements the Enigma machine in Python, simulating the encryption and decryption process used during World War II. The implementation includes features such as rotor stepping, plugboard connections, and a reflector.

## Features

- **Rotor Configuration**: Supports multiple rotors with customizable wiring and notch positions.
- **Plugboard**: Allows for character swapping to enhance encryption.
- **Reflector**: Simulates the historical Enigma reflector for bidirectional encryption.
- **Command-Line Interface**: Run the machine interactively or with command-line arguments.

## Usage

### Running the Enigma Machine

1. **Interactive Mode**:
   - Run the script without arguments to enter interactive mode:
     ```bash
     python enigma.py
     ```
   - Follow the prompts to enter your message, rotor positions, ring settings, and plugboard pairs.

2. **Command-Line Mode**:
   - Run the script with a message as an argument for quick testing:
     ```bash
     python enigma.py "HELLO"
     ```
   - This will use default settings (rotor positions `[0, 0, 0]`, ring settings `[0, 0, 0]`, and no plugboard pairs).

## Testing

The implementation includes a comprehensive test suite in `enigma_test.py`. To run the tests:

```bash
python enigma_test.py
```

The test suite covers:
- Basic encryption/decryption functionality
- Plugboard swap operations
- Different rotor position configurations

## Implementation Details

The code is organized into several key components:
- `Rotor` class for individual rotor operations
- `Enigma` class for the main machine functionality
- Utility functions for modular operations

The implementation follows the historical Enigma machine specifications, including:
- Standard rotor wirings
- Notch positions for rotor stepping
- Reflector implementation
- Plugboard functionality

## Fixes

For a list of bug fixes and improvements, see the [fix documentation](fix.md).

## Conclusion

This Python implementation of the Enigma machine provides a robust and accurate simulation of the historical encryption device, suitable for educational and testing purposes.

---

*Note: This implementation is based on the JavaScript version and includes all necessary fixes and improvements.*
