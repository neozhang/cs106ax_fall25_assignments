# File: Adventure.py
# ------------------
# This program plays the CS 106AX Adventure game.

from AdvConstant import ADVENTURE_PREFIX
from AdvGame import AdvGame

# Constants


# Main program
def Adventure():
    game = AdvGame(ADVENTURE_PREFIX)
    game.run()


# Startup code
if __name__ == "__main__":
    Adventure()
