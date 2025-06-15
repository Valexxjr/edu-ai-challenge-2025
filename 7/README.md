# Battleship Game

A Python implementation of the classic Battleship game with a command-line interface. The game features both single-player mode against a CPU opponent and comprehensive test coverage.

## Project Structure

```
battleship/
├── models/         # Core game entities
│   ├── board.py    # Game board implementation
│   ├── player.py   # Player and CPU player logic
│   └── ship.py     # Ship class implementation
├── game/           # Game logic
│   └── game_manager.py  # Main game flow control
├── display/        # User interface
│   └── display_manager.py  # Console display handling
├── utils/          # Utility functions
│   └── input_handler.py   # User input processing
└── tests/          # Test suite
    ├── test_board.py
    ├── test_game_manager.py
    ├── test_player.py
    └── test_ship.py
```

## Features

- Single-player mode against CPU opponent
- Interactive command-line interface
- Ship placement validation
- Smart CPU opponent with strategic moves
- Comprehensive test coverage
- Type hints and documentation

## Requirements

- Python 3.8 or higher
- Development dependencies (specified in requirements-dev.txt):
  - pytest==7.4.3
  - pytest-cov==4.1.0
  - coverage==7.3.2

## Installation

1. Clone the repository
2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

## Running the Game

To start the game, run:
```bash
python -m battleship.main
```

## Running Tests

To run the test suite:
```bash
python -m pytest battleship/tests/ -v
```

To run tests with coverage report:
```bash
python -m pytest battleship/tests/ --cov=battleship
```

## Game Rules

1. The game is played on a 10x10 grid
2. Each player has 3 ships, each 3 cells long
3. Players take turns firing at coordinates
4. A ship is sunk when all its cells are hit
5. The game ends when all ships of one player are sunk

## Controls

- Enter coordinates in the format "00" to "99" (row and column numbers)
- Example: "34" means row 3, column 4
- Follow the on-screen prompts for ship placement and gameplay
- Type 'quit' at any time to exit the game

## Development

The project follows a modular structure with clear separation of concerns:
- Models handle game entities and their behavior
- Game manager controls the game flow
- Display manager handles user interface
- Input handler processes user input
- Tests ensure code quality and functionality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 