# File: AdvGame.py

"""
This module defines the AdvGame class, which records the information
necessary to play a game.
"""

from AdvCharacters import AdvCharacter
from AdvObject import AdvObject
from AdvRoom import MARKER, AdvRoom
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

WILDCARD = "*"


class AdvGame:
    def __init__(self, prefix):
        """Reads the game data from files with the specified prefix."""
        self._rooms = self.readRooms(prefix)
        self._player = AdvCharacter.createRandomCharacter(
            self.getFirstRoom().getName(),
            name="",
            inventory=self.readObjects(prefix),
            isNPC=False,
        )
        self._synonyms = Synonyms(prefix + "Synonyms.txt")

    def getRooms(self):
        """Returns the map of rooms"""
        return self._rooms

    def getFirstRoom(self):
        """Returns the first room in the map"""
        return next(iter(self._rooms.values()))

    def getNextRoom(self, currentRoom, verb):
        """Returns the next room in the destination."""
        passage = currentRoom.getPassage(verb)
        if not passage:
            return None

        # If passage has an object-specific destination, prefer it when player has object.
        if "objDest" in passage:
            required_obj = passage.get("obj")
            for item in self._player.getInventory():
                if item.getName() == required_obj:
                    dest = passage["objDest"]
                    break
            else:
                # required object not present
                # fall back to defaultDest if available, otherwise no passage
                dest = passage.get("defaultDest")
        else:
            dest = passage.get("defaultDest")

        if dest is None:
            return None
        return self.getRoomByName(dest)

    def getRoomByName(self, name):
        """Returns the AdvRoom object by its name"""
        return self._rooms.get(name)

    def createNPC(self, level, room):
        """create"""
        return AdvCharacter.createRandomCharacter(
            room, name=f"npc_{room}", level=level, inventory=[]
        )

    def readRooms(self, prefix):
        """Reads room data from a file and adds them to the game"""
        rooms = {}
        with open(f"{prefix}Rooms.txt") as f:
            while True:
                currentRoom = AdvRoom.readRoom(f)
                if currentRoom is None:
                    break
                rooms[currentRoom.getName()] = currentRoom
        return rooms

    def readObjects(self, prefix):
        inventory = []
        with open(f"{prefix}Objects.txt") as f:
            while True:
                currentObject = AdvObject.readObject(f)
                if currentObject is None:
                    break
                if currentObject.getInitialLocation() == "PLAYER":
                    inventory.append(currentObject)
                else:
                    self._rooms[currentObject.getInitialLocation()].addObject(
                        currentObject
                    )
        return inventory

    def run(self):
        """Plays the adventure game stored in this object."""
        current = self.getFirstRoom()

        # Name the player
        print("Welcome to the Adventure!\n" + "Name your hero:")
        playerName = input("> ").strip().upper()
        self._player.setName(playerName)

        prompt = Prompt()

        while prompt.getVerb() != "QUIT":
            # Handle forced passage
            if current.hasForcedPassage():
                next = self.getNextRoom(current, "FORCED")
                if next is not None:
                    current = next
                    self._player.setPosition(current)
                    print(current.getLongDescription())
                    continue
                else:  # End of world. Game over. -> EXIT.
                    break

            # Handle non-forced passage
            if not prompt.isBuiltin():
                if current.hasBeenVisited():
                    print(current.getShortDescription())
                else:
                    print(current.getLongDescription())
                    if len(current.getContents()) > 0:
                        for obj in current.getContents():
                            print(f"There is {obj.getDescription()} here.")
                    current.setVisited()
                npc = self.createNPC(self._player.getLevel() - 1, current)
                print(f"You encountered a NPC: {npc.getName()}. Fight or Flee?")

            # Get user input
            text = input("> ").strip().upper()
            prompt.setInput(text, self._synonyms)

            # Execute built-in prompt
            if prompt.execute(current, self._player):
                continue

            verb = prompt.getVerb()

            # Handle wildcard passage
            if current.hasPassage(WILDCARD) and not current.hasPassage(verb):
                verb = WILDCARD

            # Handle movement
            next = self.getNextRoom(current, verb)
            if next is None:
                print("You can't go that way.")
            else:
                current = next
                self._player.setPosition(current)


class Prompt:
    """A class representing a prompt, handles user input and executes built-in commands."""

    def __init__(self, input=""):
        self._builtins = {
            "QUIT": self.handleQuit,
            "HELP": self.handleHelp,
            "ME": self.handleMe,
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
        """Sets the input for the prompt."""
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

    def execute(self, room, player):
        """Routes built-in commands to the right handlers; returns True if handled"""
        verb = self.getVerb()
        if verb in self._builtins:
            handler = self._builtins[verb]
            obj = self.getObj()
            handler(obj, room, player)
            return True
        return False

    def handleQuit(self, obj, room, player):
        return

    def handleHelp(self, obj, room, player):
        print("\n".join(HELP_TEXT))

    def handleLook(self, obj, room, player):
        print(room.getLongDescription())
        if room.getContents():
            for item in room.getContents():
                print(f"There is {item.getDescription()}.")

    def handleMe(self, obj, room, player):
        print(f"{player.getName()}: LEVEL {player.getLevel()} @ {player.getPosition()}")
        print(MARKER)
        stats = player.getStats()
        for k, v in stats.items():
            print(f"{k}: {v}")
        print(MARKER)
        self.handleInventory(obj, room, player)

    def handleInventory(self, obj, room, player):
        inventory = player.getInventory()
        if len(inventory) == 0:
            print("You are empty-handed.")
        else:
            print("You are carrying:")
            for item in inventory:
                print(f"{item.getDescription()}")

    def handleTake(self, obj, room, player):
        if not obj:
            print("Take what?")
            return
        for item in room.getContents():
            if item.getName() == obj:
                player.addItem(item)
                room.removeObject(item)
                print("Taken.")
                return

    def handleDrop(self, obj, room, player):
        if not obj:
            print("Drop what?")
            return
        for item in player.getInventory():
            if item.getName() == obj:
                player.removeItem(item)
                room.addObject(item)
                print("Dropped.")
                return


class Synonyms:
    """A class representing a set of synonyms for words."""

    def __init__(self, filename):
        self._synonyms = {}
        try:
            with open(filename, "r") as f:
                for line in f:
                    words = line.strip().split("=")
                    if len(words) > 1:
                        self._synonyms[words[0].strip().upper()] = (
                            words[1].strip().upper()
                        )
        except FileNotFoundError:
            self._synonyms = {}

    def getSynonym(self, word):
        """Returns the synonym for the given word."""
        return self._synonyms.get(word)

    def getSynonyms(self):
        """Returns a dictionary of synonyms."""
        return self._synonyms

    def isSynonym(self, word):
        """Returns True if the given word is a synonym."""
        return word in self._synonyms
