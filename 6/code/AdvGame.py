# File: AdvGame.py

"""
This module defines the AdvGame class, which records the information
necessary to play a game.
"""

from AdvRoom import AdvRoom

###########################################################################
# Your job in this assignment is to fill in the definitions of the        #
# methods listed in this file, along with any helper methods you need.    #
# Unless you are implementing extensions, you won't need to add new       #
# public methods (i.e., methods called from other modules), but the       #
# amount of code you need to add is large enough that decomposing it      #
# into helper methods will be essential.                                  #
###########################################################################

# Constants
HELP_TEXT = [
    "Welcome to Adventure!",
    "Somewhere nearby is Colossal Cave, where others have found fortunes in",
    "treasure and gold, though it is rumored that some who enter are never",
    "seen again.  Magic is said to work in the cave.  I will be your eyes",
    "and hands.  Direct me with natural English commands; I don't understand",
    "all of the English language, but I do a pretty good job.",
    "",
    "It's important to remember that cave passages turn a lot, and that",
    "leaving a room to the north does not guarantee entering the next from",
    "the south, although it often works out that way.  You'd best make",
    "yourself a map as you go along.",
    "",
    "Much of my vocabulary describes places and is used to move you there.",
    "To move, try words like IN, OUT, EAST, WEST, NORTH, SOUTH, UP, or DOWN.",
    "I also know about a number of objects hidden within the cave which you",
    "can TAKE or DROP.  To see what objects you're carrying, say INVENTORY.",
    "To reprint the detailed description of where you are, say LOOK.  If you",
    "want to end your adventure, say QUIT.",
]


class AdvGame:
    def __init__(self, prefix):
        """Reads the game data from files with the specified prefix."""
        self._rooms = {}  # {name: AdvRoom}
        with open(f"{prefix}Rooms.txt") as f:
            while True:
                currentRoom = AdvRoom.readRoom(f)
                if currentRoom is None:
                    break
                self._rooms[currentRoom.getName()] = currentRoom

    def getRooms(self):
        """Returns the map of rooms"""
        return self._rooms

    def getFirstRoom(self):
        """Returns the first room in the map"""
        return next(iter(self._rooms.values()))

    def getRoomByName(self, name):
        """Returns the AdvRoom object by its name"""
        return self._rooms.get(name)

    def run(self):
        """Plays the adventure game stored in this object."""
        verb = ""
        current = self.getFirstRoom()
        while verb != "QUIT":
            print(current.getLongDescription())
            verb = input("> ").strip().upper()
            next = self.getRoomByName(current.getNextRoom(verb))
            if next is None:
                print("You can't go that way.")
            else:
                current = next
