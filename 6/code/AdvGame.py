# File: AdvGame.py

"""
This module defines the AdvGame class, which records the information
necessary to play a game.
"""

from AdvObject import AdvObject
from AdvRoom import AdvRoom
from tokenscanner import TokenScanner

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

        self._inventory = []
        with open(f"{prefix}Objects.txt") as f:
            while True:
                currentObject = AdvObject.readObject(f)
                if currentObject is None:
                    break
                if currentObject.getInitialLocation() == "PLAYER":
                    self._inventory.append(currentObject)
                else:
                    self._rooms[currentObject.getInitialLocation()].addObject(
                        currentObject
                    )
        self._synonyms = Synonyms(prefix + "Synonyms.txt")

    def getRooms(self):
        """Returns the map of rooms"""
        return self._rooms

    def getFirstRoom(self):
        """Returns the first room in the map"""
        return next(iter(self._rooms.values()))

    def getNextRoom(self, currentRoom, verb):
        """Returns the next room in the destination"""
        passage = currentRoom.getPassage(verb)
        if passage is None:
            return None
        else:
            for item in self._inventory:
                if "obj" in passage and passage["obj"] == item.getName():
                    room = passage["objDest"]
                    break
                else:
                    room = passage["defaultDest"]
            return self.getRoomByName(room)

    def getRoomByName(self, name):
        """Returns the AdvRoom object by its name"""
        return self._rooms.get(name)

    def run(self):
        """Plays the adventure game stored in this object."""
        current = self.getFirstRoom()
        prompt = Prompt()

        while prompt.getVerb() != "QUIT":
            if not prompt.isBuiltin():
                if current.hasBeenVisited():
                    print(current.getShortDescription())
                else:
                    print(current.getLongDescription())
                    if len(current.getContents()) > 0:
                        for obj in current.getContents():
                            print(f"There is {obj.getDescription()} here.")
                    current.setVisited()
            text = input("> ").strip().upper()
            prompt.setInput(text, self._synonyms)
            if prompt.execute(current, self._inventory):
                continue
            next = self.getNextRoom(current, prompt.getVerb())
            if next is None:
                print("You can't go that way.")
            else:
                current = next


class Prompt:
    def __init__(self, input=""):
        self._builtins = {
            "QUIT": self.handleQuit,
            "HELP": self.handleHelp,
            "INVENTORY": self.handleInventory,
            "LOOK": self.handleLook,
            "TAKE": self.handleTake,
            "DROP": self.handleDrop,
        }
        self.setInput(input)

    def getVerb(self):
        return self._tokenized["verb"]

    def getObj(self):
        return self._tokenized["obj"]

    def setInput(self, input, synonyms=None):
        self._raw = input
        self._tokenized = {}
        scanner = TokenScanner(input)
        verb = scanner.nextToken().strip().upper() if scanner.hasMoreTokens() else None
        if synonyms is not None and verb in synonyms.getSynonyms():
            verb = synonyms.getSynonym(verb)
        self._tokenized["verb"] = verb
        self._tokenized["obj"] = ""
        while scanner.hasMoreTokens():
            self._tokenized["obj"] += scanner.nextToken().strip().upper()

    def isBuiltin(self):
        return self._tokenized["verb"] in self._builtins

    def execute(self, room, inventory):
        """Routes built-in commands to the right handlers; returns True if handled"""
        verb = self.getVerb()
        if verb in self._builtins:
            handler = self._builtins[verb]
            obj = self.getObj()
            handler(obj, room, inventory)
            return True
        return False

    def handleQuit(self, obj, room, inventory):
        return

    def handleHelp(self, obj, room, inventory):
        print("\n".join(HELP_TEXT))

    def handleLook(self, obj, room, inventory):
        print(room.getLongDescription())
        if room.getContents():
            for item in room.getContents():
                print(f"There is {item.getDescription()}.")

    def handleInventory(self, obj, room, inventory):
        if len(inventory) == 0:
            print("You are empty-handed.")
        else:
            print("You are carrying:")
            for item in inventory:
                print(f"{item.getDescription()}")

    def handleTake(self, obj, room, inventory):
        for item in room.getContents():
            if item.getName() == obj:
                inventory.append(item)
                room.removeObject(item)
                print("Taken.")
        return inventory

    def handleDrop(self, obj, room, inventory):
        for item in inventory:
            if item.getName() == obj:
                inventory.remove(item)
                room.addObject(item)
                print("Dropped.")
        return


class Synonyms:
    def __init__(self, filename):
        self._synonyms = {}
        try:
            with open(filename, "r") as f:
                for line in f:
                    words = line.strip().split("=")
                    if len(words) > 1:
                        self._synonyms[words[0]] = words[1]
        except FileNotFoundError:
            self._synonyms = {}

    def getSynonym(self, word):
        return self._synonyms.get(word)

    def getSynonyms(self):
        return self._synonyms

    def isSynonym(self, word):
        return word in self._synonyms
