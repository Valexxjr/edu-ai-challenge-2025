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
     python enigma.py HELLOWORLD
     ```
   - This will use default settings (rotor positions `[0, 0, 0]`, ring settings `[0, 0, 0]`, and no plugboard pairs).

## Testing

The implementation includes a test suite to verify functionality:

- **Basic Encryption/Decryption**: Ensures the machine can encrypt and decrypt messages correctly.
- **Plugboard Functionality**: Tests the machine with plugboard connections.
- **Different Rotor Positions**: Verifies the machine works with various rotor positions.

For detailed test results, see the [test report](test_report.md).

## Fixes

For a list of bug fixes and improvements, see the [fix documentation](fix.md).

## Conclusion

This Python implementation of the Enigma machine provides a robust and accurate simulation of the historical encryption device, suitable for educational and testing purposes.

---

*Note: This implementation is based on the JavaScript version and includes all necessary fixes and improvements.*
