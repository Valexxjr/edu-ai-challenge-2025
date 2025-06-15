"""
Main entry point for the Battleship game.
"""

from battleship.game.game_manager import GameManager

def main():
    game = GameManager()
    game.play()

if __name__ == "__main__":
    main() 